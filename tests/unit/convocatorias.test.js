import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

/**
 * A-5 · Un solo modelo de recuperación.
 *
 * Hasta la 3.8 convivían dos cosas llamadas «recuperación»: volver a calificar
 * una actividad de la parrilla (que cambiaba la nota de la 1ª convocatoria, ya
 * en acta) y teclear notas sueltas por criterio en el panel de la 2ª. El
 * art. 21.5 de la Orden 201/2024 dice cuál es el modelo bueno: en segunda
 * convocatoria los RA no superados se evalúan «utilizando otros instrumentos de
 * evaluación diferentes» — es decir, con ACTIVIDADES nuevas.
 *
 * Estos tests fijan las reglas que hacen que eso sea coherente, incluida la que
 * más costó ver: que las dos convocatorias tienen que usar la misma fórmula.
 */

function cargarMotor() {
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const motor  = fs.readFileSync(path.resolve('renderer/js/core/calificacion.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(`${ceKeys}\n${motor}`, context)
  return context.module.exports
}

const M = cargarMotor()

const ras = [{ id: 'RA1', pond: 100 }]
const cesByRa = { RA1: [{ id: 'CR1' }, { id: 'CR2' }] }

/** CR1 aprobado en el curso (8); CR2 suspenso (3) y recuperado en junio (7). */
const actividades = [
  { id: 1, tipo: 'examen', peso: 50, nota_max: 10, ces: '["RA1|CR1"]', convocatoria: 1 },
  { id: 2, tipo: 'examen', peso: 50, nota_max: 10, ces: '["RA1|CR2"]', convocatoria: 1 },
  { id: 3, tipo: 'examen', peso: 0,  nota_max: 10, ces: '["RA1|CR2"]', convocatoria: 2 },
]
const notas = { 1: 8, 2: 3, 3: 7 }

const ctx = (extra = {}) =>
  M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades, ...extra })

describe('A-5 · Convocatorias', () => {
  it('la actividad de recuperación no toca la nota de la 1ª convocatoria', () => {
    // La 1ª ya está en acta: la prueba de junio no puede cambiarla.
    const st = M.estadoModulo(ctx(), notas)
    expect(st.porRA.RA1.nota).toBeCloseTo(5.5)   // (8 + 3) / 2
  })

  it('en la 2ª convocatoria el criterio vale la mejor de sus dos notas', () => {
    const st = M.estadoModulo(ctx({ convocatoria: 2 }), notas)
    expect(st.porRA.RA1.nota).toBeCloseTo(7.5)   // (8 + 7) / 2
  })

  it('recuperar no puede bajar un criterio ya aprobado (art. 4.3.f)', () => {
    const conRecuperacionMala = [
      ...actividades,
      { id: 4, tipo: 'examen', peso: 0, nota_max: 10, ces: '["RA1|CR1"]', convocatoria: 2 },
    ]
    const st = M.estadoModulo(
      M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades: conRecuperacionMala, convocatoria: 2 }),
      { ...notas, 4: 2 })
    expect(st.porRA.RA1.nota).toBeCloseTo(7.5)   // el 2 de la recuperación se ignora
  })

  it('una base sin la columna convocatoria calcula igual que antes', () => {
    // Migración: `convocatoria` se añade con DEFAULT 1, pero las actividades que
    // lleguen sin ella (bases antiguas, importaciones) no pueden desaparecer.
    const sinColumna = actividades.slice(0, 2).map(({ convocatoria: _c, ...resto }) => resto)
    const st = M.estadoModulo(
      M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades: sinColumna }), notas)
    expect(st.porRA.RA1.nota).toBeCloseTo(5.5)
  })

  it('el mínimo de examen lo levanta la prueba de recuperación, no el olvido', () => {
    // El examen del curso fue un 3 con mínimo 5: en junio bloquea el RA.
    const st1 = M.estadoModulo(ctx({ minExam: 5 }), notas)
    expect(st1.porRA.RA1.minKO).toBe(true)

    // Con un 7 en la prueba de recuperación —el «instrumento diferente» del
    // art. 21.5— el mínimo queda acreditado.
    const st2 = M.estadoModulo(ctx({ minExam: 5, convocatoria: 2 }), notas)
    expect(st2.porRA.RA1.minKO).toBe(false)

    // Pero si no se presenta a la recuperación, sigue bloqueando.
    const st3 = M.estadoModulo(ctx({ minExam: 5, convocatoria: 2 }), { 1: 8, 2: 3 })
    expect(st3.porRA.RA1.minKO).toBe(true)
  })

  it('respeta la ponderación de cada criterio también en la 2ª convocatoria', () => {
    // El fallo que cerró A-5: la 2ª promediaba los criterios a peso igual
    // mientras la 1ª respetaba el art. 4.3.a. Dos convocatorias, dos fórmulas.
    const cesPesados = { RA1: [{ id: 'CR1', peso: 80 }, { id: 'CR2', peso: 20 }] }
    const st = M.estadoModulo(
      M.contextoModulo({ ras, cesByRa: cesPesados, asignaciones: [], actividades, convocatoria: 2 }),
      notas)
    expect(st.porRA.RA1.nota).toBeCloseTo(7.8)   // 8×0,8 + 7×0,2 ≠ 7,5
  })

  it('un criterio dado por alcanzado entra por el motor, no por una media aparte', () => {
    // CR2 sin recuperar, pero el equipo docente lo da por alcanzado: vale 5.
    const soloCurso = actividades.slice(0, 2)
    const st = M.estadoModulo(
      M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades: soloCurso, convocatoria: 2 }),
      { 1: 8, 2: 3 },
      { notaCEOverride: (raId, ceId, calculada) => (ceId === 'CR2' ? Math.max(5, calculada ?? 0) : calculada) })
    expect(st.porRA.RA1.nota).toBeCloseTo(6.5)   // (8 + 5) / 2
  })

  it('separa las actividades por convocatoria', () => {
    expect(M.actividadesDeConvocatoria(actividades, 1).map(a => a.id)).toEqual([1, 2])
    expect(M.actividadesDeConvocatoria(actividades, 2).map(a => a.id)).toEqual([1, 2, 3])
    expect(M.convocatoriaDe({ convocatoria: 2 })).toBe(2)
    expect(M.convocatoriaDe({})).toBe(1)
  })
})

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

function cargarCeKeys() {
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(ceKeys, context)
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

  it('quien suspende todos los RA los tiene todos recuperables en la 2ª', () => {
    // Fallo visto en uso: alumnado con todo suspenso al que la 2ª convocatoria
    // no le ofrecía todos los RA. Se reproduce con los datos reales de OACE
    // (4 RA al 24/24/24/28) y un alumno con 0,9 · 0,0 · 0,0 · 0,0.
    const rasOace = [{ id: 'RA1', pond: 24 }, { id: 'RA2', pond: 24 },
                     { id: 'RA3', pond: 24 }, { id: 'RA4', pond: 28 }]
    const ces = {}
    const acts = []
    let id = 0
    for (const ra of rasOace) {
      ces[ra.id] = [{ id: 'CR1' }, { id: 'CR2' }]
      for (const ce of ['CR1', 'CR2']) {
        acts.push({ id: ++id, tipo: 'examen', peso: 50, nota_max: 10,
                    ces: JSON.stringify([`${ra.id}|${ce}`]), convocatoria: 1 })
      }
    }
    const suspendeTodo = { 1: 0.9, 2: 0.9, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0 }

    const st = M.estadoModulo(
      M.contextoModulo({ ras: rasOace, cesByRa: ces, asignaciones: [], actividades: acts, convocatoria: 2 }),
      suspendeTodo)

    // Los cuatro pendientes, ninguno dado por superado (que es lo que los
    // bloquearía con el candado y los dejaría fuera de la recuperación).
    expect(st.pendientes).toEqual(['RA1', 'RA2', 'RA3', 'RA4'])
    expect(Object.values(st.porRA).filter(v => v.nota !== null && v.nota >= 5)).toEqual([])
  })

  it('el boletín de un trimestre no cuenta lo que aún no se ha dado', () => {
    // RA1 se trabaja en la 1ª evaluación y RA2 en la 3ª. En el boletín de
    // diciembre, RA2 no puede figurar como «sin evaluar»: todavía no tocaba.
    const rasB = [{ id: 'RA1', pond: 50 }, { id: 'RA2', pond: 50 }]
    const cesB = { RA1: [{ id: 'CR1' }], RA2: [{ id: 'CR1' }] }
    const actsB = [
      { id: 1, tipo: 'examen', peso: 100, nota_max: 10, eval: 1, ces: '["RA1|CR1"]', convocatoria: 1 },
      { id: 2, tipo: 'examen', peso: 100, nota_max: 10, eval: 3, ces: '["RA2|CR1"]', convocatoria: 1 },
    ]
    const soloUnaNota = { 1: 7 }

    const hastaLa1a = M.estadoModulo(
      M.contextoModulo({ ras: rasB, cesByRa: cesB, asignaciones: [], actividades: actsB.filter(a => a.eval <= 1) }),
      soloUnaNota)
    expect(hastaLa1a.media).toBeCloseTo(7)
    expect(hastaLa1a.sinNota).toEqual([])

    const cursoEntero = M.estadoModulo(
      M.contextoModulo({ ras: rasB, cesByRa: cesB, asignaciones: [], actividades: actsB }),
      soloUnaNota)
    expect(cursoEntero.sinNota).toContain('RA2')
  })

  it('separa las actividades por convocatoria', () => {
    expect(M.actividadesDeConvocatoria(actividades, 1).map(a => a.id)).toEqual([1, 2])
    expect(M.actividadesDeConvocatoria(actividades, 2).map(a => a.id)).toEqual([1, 2, 3])
    expect(M.convocatoriaDe({ convocatoria: 2 })).toBe(2)
    expect(M.convocatoriaDe({})).toBe(1)
  })
})

describe('Criterios de una actividad: lectura repetida', () => {
  it('devuelve lo mismo aunque se pregunte muchas veces', () => {
    // Los criterios llegan como texto JSON y la pantalla los pide una vez por
    // alumno, por RA y por criterio: en un grupo de 30 eran más de cien mil
    // JSON.parse por repintado. Ahora el resultado se recuerda, y esto fija que
    // recordarlo no cambia la respuesta.
    const ce = cargarCeKeys()
    const act = { id: 1, ra_id: 'RA1', ces: JSON.stringify(['RA1|CR1', 'RA1|CR2']) }
    const primera = ce.actCesLista(act)
    expect(ce.actCesLista(act)).toEqual(primera)
    expect(ce.actCubreCe(act, 'RA1', 'CR1')).toBe(true)
    expect(ce.actCubreCe(act, 'RA2', 'CR1')).toBe(false)
  })

  it('si la actividad cambia de criterios, deja de dar los viejos', () => {
    const ce = cargarCeKeys()
    const act = { id: 2, ra_id: 'RA1', ces: JSON.stringify(['RA1|CR1']) }
    expect(ce.actCubreCe(act, 'RA1', 'CR1')).toBe(true)
    act.ces = JSON.stringify(['RA1|CR9'])
    expect(ce.actCubreCe(act, 'RA1', 'CR1'), 'se quedó con los criterios antiguos').toBe(false)
    expect(ce.actCubreCe(act, 'RA1', 'CR9')).toBe(true)
  })
})

describe('Presentarse a la recuperación no puede salir caro', () => {
  // El caso salió de lanzar miles de combinaciones al azar contra las reglas de
  // la Orden: en algunas, la nota del RA en 2ª convocatoria era MENOR que la que
  // el alumno ya tenía en la 1ª.
  const ras = [{ id: 'RA1', pond: 100 }]
  const ces = { RA1: [{ id: 'CR1' }, { id: 'CR2' }] }

  function estado(acts, notas, conv) {
    const ctx = M.contextoModulo({ ras, cesByRa: ces, asignaciones: [], actividades: acts,
      minExam: null, rasSuperados: null, tieneFaseEmpresa: false, convocatoria: conv })
    return M.estadoModulo(ctx, notas)
  }

  it('un criterio sin calificar durante el curso no hunde el RA en junio', () => {
    // CR1 se trabajó y sacó un 9. CR2 quedó sin calificar. La prueba de junio se
    // creó con «todos» los criterios marcados —lo más cómodo— y sale regular.
    const acts = [
      { id: 1, ra_id: 'RA1', tipo: 'practica', peso: 50, nota_max: 10, eval: 1, convocatoria: 1, ces: ['RA1|CR1'] },
      { id: 2, ra_id: 'RA1', tipo: 'examen',   peso: 50, nota_max: 10, eval: 1, convocatoria: 1, ces: ['RA1|CR2'] },
      { id: 3, ra_id: 'RA1', tipo: 'examen',   peso: 100, nota_max: 10, eval: 1, convocatoria: 2, ces: ['RA1|CR1', 'RA1|CR2'] },
    ]
    const notas = { 1: 9, 3: 4 }          // CR2 sin nota en el curso; recuperación: 4
    const primera = estado(acts, notas, 1).porRA.RA1.nota
    const segunda = estado(acts, notas, 2).porRA.RA1.nota
    expect(primera).toBe(9)
    expect(segunda, 'la recuperación no puede dejarlo peor que antes').toBeGreaterThanOrEqual(primera)
  })

  it('pero si la recuperación mejora, la nota sube', () => {
    const acts = [
      { id: 1, ra_id: 'RA1', tipo: 'examen', peso: 100, nota_max: 10, eval: 1, convocatoria: 1, ces: ['RA1|CR1', 'RA1|CR2'] },
      { id: 2, ra_id: 'RA1', tipo: 'examen', peso: 100, nota_max: 10, eval: 1, convocatoria: 2, ces: ['RA1|CR1', 'RA1|CR2'] },
    ]
    const notas = { 1: 3, 2: 8 }
    expect(estado(acts, notas, 1).porRA.RA1.nota).toBe(3)
    expect(estado(acts, notas, 2).porRA.RA1.nota).toBe(8)
  })

  it('el mínimo de examen tampoco reaparece si mandaba la primera', () => {
    const acts = [
      { id: 1, ra_id: 'RA1', tipo: 'examen', peso: 100, nota_max: 10, eval: 1, convocatoria: 1, ces: ['RA1|CR1'] },
      { id: 2, ra_id: 'RA1', tipo: 'examen', peso: 100, nota_max: 10, eval: 1, convocatoria: 2, ces: ['RA1|CR1'] },
    ]
    const ctx = M.contextoModulo({ ras, cesByRa: { RA1: [{ id: 'CR1' }] }, asignaciones: [],
      actividades: acts, minExam: 5, rasSuperados: null, tieneFaseEmpresa: false, convocatoria: 2 })
    const st = M.estadoModulo(ctx, { 1: 8, 2: 2 })
    expect(st.porRA.RA1.nota).toBe(8)
    expect(st.porRA.RA1.minKO, 'el examen bueno es el de la 1ª, no puede quedar KO').toBe(false)
  })
})

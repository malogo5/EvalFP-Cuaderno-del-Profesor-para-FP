import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

/**
 * Reglas de la Orden 201/2024 en la redacción dada por la Orden 55/2026, de 17
 * de abril (DOCM núm. 78, de 27/04/2026).
 *
 * Estos tests fijan cuatro cosas que un cuaderno de notas hace mal por defecto:
 *
 *  1. Quien pierde el derecho a la evaluación continua NO conserva nada de lo
 *     obtenido antes (art. 3.6). Un cuaderno tiende a arrastrarlo todo.
 *  2. La nota final del ciclo es media ARITMÉTICA, no ponderada por horas
 *     (art. 25.9 y 25.10). Dentro de un módulo sí se pondera, y es fácil
 *     extender esa lógica un nivel de más.
 *  3. Los módulos convalidados sin nota no computan (art. 25.11).
 *  4. La Matrícula de Honor tiene cupo: uno por cada veinte o fracción
 *     (art. 25.12).
 */

function cargarMotor() {
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const motor  = fs.readFileSync(path.resolve('renderer/js/core/calificacion.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(`${ceKeys}\n${motor}`, context)
  return context.module.exports
}

const M = cargarMotor()

describe('Pérdida del derecho a la evaluación continua (art. 3.6)', () => {
  const ras = [{ id: 'RA1', pond: 50 }, { id: 'RA2', pond: 50 }]
  const cesByRa = { RA1: [{ id: 'CR1' }], RA2: [{ id: 'CR1' }] }

  // Durante el curso sacó buenas notas; después perdió la evaluación continua.
  // La prueba objetiva de junio cubre los dos RA y le sale peor.
  const actividades = [
    { id: 1, tipo: 'examen', peso: 50, nota_max: 10, ces: '["RA1|CR1"]', convocatoria: 1 },
    { id: 2, tipo: 'examen', peso: 50, nota_max: 10, ces: '["RA2|CR1"]', convocatoria: 1 },
    { id: 3, tipo: 'examen', peso: 0, nota_max: 10, ces: '["RA1|CR1","RA2|CR1"]',
      convocatoria: 1, prueba_objetiva: 1 },
  ]
  const notas = { 1: 9, 2: 9, 3: 4 }
  const ctx = extra => M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades, ...extra })

  it('con evaluación continua manda lo trabajado durante el curso', () => {
    const st = M.estadoModulo(ctx({}), notas)
    // La prueba objetiva también evalúa esos criterios, así que promedia
    expect(st.media).toBeGreaterThan(4)
    expect(st.media).toBeLessThan(9.01)
  })

  it('perdida la evaluación continua solo cuenta la prueba objetiva', () => {
    const st = M.estadoModulo(ctx({}), notas, { evalContinuaPerdida: true })
    expect(st.media).toBe(4)
    expect(st.resultado).toBe('NO_SUPERADO')
  })

  it('no conserva los RA cerrados como superados en sesiones anteriores', () => {
    // RA1 se cerró con un 9 en la 1ª evaluación. Con evaluación continua ese
    // cierre protege la nota; sin ella, el art. 3.6 lo deja sin efecto.
    const conCierre = ctx({ rasSuperados: { RA1: 9 } })
    expect(M.estadoModulo(conCierre, notas).porRA.RA1.nota).toBe(9)

    const st = M.estadoModulo(conCierre, notas, { evalContinuaPerdida: true })
    expect(st.porRA.RA1.nota).toBe(4)
    expect(st.porRA.RA1.congelado).toBe(false)
  })

  it('no aplica los criterios dados por alcanzados a mano', () => {
    const override = () => 10
    const st = M.estadoModulo(ctx({}), notas, {
      evalContinuaPerdida: true, notaCEOverride: override,
    })
    expect(st.media).toBe(4)
  })

  it('si la prueba objetiva no cubre todos los RA, el módulo no se supera', () => {
    // La prueba solo evalúa RA1: RA2 se queda sin calificar y el módulo queda
    // PENDIENTE. Es la garantía de que la prueba «incluirá la totalidad de los
    // resultados de aprendizaje».
    const parcial = [
      actividades[0], actividades[1],
      { id: 4, tipo: 'examen', peso: 0, nota_max: 10, ces: '["RA1|CR1"]',
        convocatoria: 1, prueba_objetiva: 1 },
    ]
    const c = M.contextoModulo({ ras, cesByRa, asignaciones: [], actividades: parcial })
    const st = M.estadoModulo(c, { 1: 9, 2: 9, 4: 7 }, { evalContinuaPerdida: true })
    expect(st.sinNota).toContain('RA2')
    expect(st.resultado).toBe('PENDIENTE')
  })

  it('un examen normal no vale como prueba objetiva', () => {
    expect(M.esPruebaObjetiva({ tipo: 'examen' })).toBe(false)
    expect(M.esPruebaObjetiva({ tipo: 'examen', prueba_objetiva: 1 })).toBe(true)
    expect(M.esPruebaObjetiva({ prueba_objetiva: true })).toBe(true)
    expect(M.esPruebaObjetiva(null)).toBe(false)
  })
})

describe('Calificación final del ciclo (art. 25.9 y 25.10)', () => {
  it('es media aritmética, NO ponderada por la carga lectiva', () => {
    // Un módulo de 300 h con un 4 y otro de 50 h con un 10. Ponderando por horas
    // saldría 4,86; la norma dice que las horas no cuentan: (4+10)/2 = 7.
    const modulos = [{ nota: 4, horas: 300 }, { nota: 10, horas: 50 }]
    expect(M.notaFinalCiclo(modulos)).toBe(7)
  })

  it('da dos decimales', () => {
    expect(M.notaFinalCiclo([{ nota: 7 }, { nota: 8 }, { nota: 8 }])).toBe(7.67)
  })

  it('no computa los módulos convalidados sin nota (art. 25.11)', () => {
    const modulos = [{ nota: 6 }, { nota: 8 }, { nota: null, convalidado: true }]
    expect(M.notaFinalCiclo(modulos)).toBe(7)
    expect(M.computaEnNotaFinal({ nota: null, convalidado: true })).toBe(false)
  })

  it('un convalidado CON nota sí computa', () => {
    expect(M.computaEnNotaFinal({ nota: 9, convalidado: true })).toBe(true)
    expect(M.notaFinalCiclo([{ nota: 5 }, { nota: 9, convalidado: true }])).toBe(7)
  })

  it('en el título de Técnico Básico quedan fuera los ámbitos', () => {
    const modulos = [
      { nota: 8 }, { nota: 6 },
      { nota: 2, esAmbito: true }, { nota: 2, esAmbito: true },
    ]
    expect(M.notaFinalCiclo(modulos, { soloAmbitoProfesional: true })).toBe(7)
    // Para el acceso a grado medio sí entran (art. 25.9, párrafo tercero)
    expect(M.notaAccesoGradoMedio(modulos)).toBe(4.5)
  })

  it('sin módulos computables devuelve null, no cero', () => {
    expect(M.notaFinalCiclo([])).toBe(null)
    expect(M.notaFinalCiclo([{ nota: null, convalidado: true }])).toBe(null)
  })
})

describe('Matrícula de Honor (art. 25.12)', () => {
  it('una por cada veinte o fracción', () => {
    expect(M.cupoMatriculaHonor(0)).toBe(0)
    expect(M.cupoMatriculaHonor(1)).toBe(1)
    expect(M.cupoMatriculaHonor(20)).toBe(1)
    expect(M.cupoMatriculaHonor(21)).toBe(2)
    expect(M.cupoMatriculaHonor(40)).toBe(2)
    expect(M.cupoMatriculaHonor(41)).toBe(3)
  })

  it('solo optan quienes llegan a 9, ordenados por nota', () => {
    const r = M.candidatosMatriculaHonor([
      { id: 1, notaFinal: 8.99 }, { id: 2, notaFinal: 9 }, { id: 3, notaFinal: 9.8 },
    ], 20)
    expect(r.candidatos.map(a => a.id)).toEqual([3, 2])
    expect(r.cupo).toBe(1)
    expect(r.excedeCupo).toBe(true)
  })

  it('avisa cuando caben todas las candidaturas', () => {
    const r = M.candidatosMatriculaHonor([{ id: 1, notaFinal: 9.5 }], 20)
    expect(r.excedeCupo).toBe(false)
  })
})

describe('Continuidad con materias pendientes (art. 18.5)', () => {
  it('cumple con 3 materias o menos y por debajo del 30 %', () => {
    const r = M.puedeContinuarConPendientes(
      [{ horas: 100 }, { horas: 150 }], 1000)
    expect(r.cumple).toBe(true)
    expect(r.porcentaje).toBe(25)
  })

  it('no cumple con más de tres materias', () => {
    const r = M.puedeContinuarConPendientes(
      [{ horas: 10 }, { horas: 10 }, { horas: 10 }, { horas: 10 }], 1000)
    expect(r.cumple).toBe(false)
    expect(r.motivo).toContain('el máximo son 3')
  })

  it('no cumple si la carga llega al 30 %', () => {
    const r = M.puedeContinuarConPendientes([{ horas: 300 }], 1000)
    expect(r.cumple).toBe(false)
    expect(r.motivo).toContain('30 %')
  })

  it('sin materias pendientes no aplica', () => {
    expect(M.puedeContinuarConPendientes([], 1000).cumple).toBe(false)
  })
})

describe('Fase de empresa del CE de Python (Decreto 79/2025, art. 5.3)', () => {
  // El curso dura 430 horas y tiene 19 RA (5+5+5+4).
  const TOTAL = 430
  const RA = 19

  it('en régimen general la franja es del 20 al 35 % de las horas', () => {
    const f = M.franjaFaseEmpresaCE(TOTAL, 'general')
    expect(f.horasMin).toBe(86)     // 20 % de 430
    expect(f.horasMax).toBe(150)    // 35 % de 430 = 150,5
    expect(f.porcentajeRa).toEqual([10, 20])
  })

  it('en régimen intensivo sube al 35-50 % y al menos el 30 % de los RA', () => {
    const f = M.franjaFaseEmpresaCE(TOTAL, 'intensivo')
    expect(f.horasMin).toBe(151)    // 35 % de 430 = 150,5 → 151
    expect(f.horasMax).toBe(215)    // 50 % de 430
    expect(f.porcentajeRa[0]).toBe(30)
  })

  it('acepta una propuesta que encaja en la norma', () => {
    const r = M.validaFaseEmpresaCE({
      horasEmpresa: 100, horasTotales: TOTAL, raEnEmpresa: 3, raTotales: RA,
    })
    expect(r.valida).toBe(true)
    expect(r.avisos).toEqual([])
  })

  it('rechaza pocas horas y lo explica', () => {
    const r = M.validaFaseEmpresaCE({
      horasEmpresa: 50, horasTotales: TOTAL, raEnEmpresa: 3, raTotales: RA,
    })
    expect(r.valida).toBe(false)
    expect(r.avisos[0]).toContain('entre 86 y 150')
  })

  it('rechaza demasiados RA en empresa para el régimen general', () => {
    const r = M.validaFaseEmpresaCE({
      horasEmpresa: 100, horasTotales: TOTAL, raEnEmpresa: 10, raTotales: RA,
    })
    expect(r.valida).toBe(false)
    expect(r.avisos.join(' ')).toContain('entre el 10 y el 20 %')
  })
})

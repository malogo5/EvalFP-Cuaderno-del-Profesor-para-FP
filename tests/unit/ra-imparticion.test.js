import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

// El motor se apoya en las claves RA|CE de js/utils/ce-keys.js: se cargan en el
// mismo orden que en la aplicación, igual que en evaluation-calculations.test.js
function cargarMotor() {
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const motor  = fs.readFileSync(path.resolve('renderer/js/core/calificacion.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(`${ceKeys}\n${motor}`, context)
  return context.module.exports
}

const {
  contextoModulo, estadoModulo, estadoImparticion,
  reparterPonderaciones, raPendientesDeDecidir, ESTADO_RA,
} = cargarMotor()

/**
 * RF-01 · Estado de impartición del resultado de aprendizaje.
 *
 * El fallo que corrige: `rasActivos` filtraba los RA sin actividad y
 * `estadoModulo` solo recorría esos, así que un RA que nunca se había evaluado
 * no llegaba a `sinNota`, `completo` salía true y el módulo podía darse por
 * SUPERADO. El art. 2.3 de la Orden 201/2024 exige alcanzarlos TODOS.
 *
 * El reparto proporcional de la ponderación de un RA no impartido no es una
 * exigencia normativa, es una regla funcional de EvalFP que debe constar en la
 * programación didáctica. Lo que la norma pide es que la decisión esté
 * documentada: de ahí el motivo obligatorio.
 */

const RAS = [
  { id: 'RA1', pond: 25 },
  { id: 'RA2', pond: 25 },
  { id: 'RA3', pond: 50 },
]

const CES = {
  RA1: [{ id: 'a' }],
  RA2: [{ id: 'a' }],
  RA3: [{ id: 'a' }],
}

// Una actividad por RA, salvo RA3, que se queda sin ninguna.
const ACTS = [
  { id: 1, ra_id: 'RA1', tipo: 'examen', peso: 1, nota_max: 10, eval: 1, convocatoria: 1 },
  { id: 2, ra_id: 'RA2', tipo: 'examen', peso: 1, nota_max: 10, eval: 1, convocatoria: 1 },
]

const NOTAS = { 1: 8, 2: 8 }

const ctxCon = raEstados => contextoModulo({
  ras: RAS, cesByRa: CES, asignaciones: [], actividades: ACTS,
  minExam: null, rasSuperados: null, tieneFaseEmpresa: false,
  convocatoria: 1, raEstados,
})

describe('RF-01 · un RA sin actividad ya no desaparece del cómputo', () => {
  it('el módulo queda PENDIENTE, no SUPERADO, si un RA no se ha evaluado', () => {
    const est = estadoModulo(ctxCon(null), NOTAS)
    expect(est.sinNota).toContain('RA3')
    expect(est.completo).toBe(false)
    expect(est.resultado).toBe('PENDIENTE')
    expect(est.superado).toBe(false)
  })

  it('un RA sin decidir arranca como «previsto», nunca como no impartido', () => {
    const ctx = ctxCon(null)
    expect(ctx.raEstados.RA3).toBe(ESTADO_RA.PREVISTO)
    expect(ctx.rasExcluidos).toEqual([])
  })

  it('el cierre de acta se bloquea mientras quede algún RA en previsto', () => {
    expect(raPendientesDeDecidir(ctxCon(null))).toEqual(['RA3'])
    const todos = {
      RA1: ESTADO_RA.IMPARTIDO,
      RA2: ESTADO_RA.IMPARTIDO,
      RA3: { estado: ESTADO_RA.NO_IMPARTIDO, motivo: 'sin tiempo', fecha: '2026-06-01' },
    }
    expect(raPendientesDeDecidir(ctxCon(todos))).toEqual([])
  })
})

describe('RF-01 · RA marcado como no impartido', () => {
  const ESTADOS = {
    RA1: ESTADO_RA.IMPARTIDO,
    RA2: ESTADO_RA.IMPARTIDO,
    RA3: { estado: ESTADO_RA.NO_IMPARTIDO, motivo: 'no dio tiempo', fecha: '2026-06-01' },
  }

  it('sale del cómputo y el módulo puede superarse con el resto', () => {
    const est = estadoModulo(ctxCon(ESTADOS), NOTAS)
    expect(est.sinNota).toEqual([])
    expect(est.completo).toBe(true)
    expect(est.resultado).toBe('SUPERADO')
    expect(est.rasExcluidos).toEqual(['RA3'])
  })

  it('no cuenta como no superado para el tope de 4 del art. 25.5', () => {
    const est = estadoModulo(ctxCon(ESTADOS), NOTAS)
    expect(est.pendientes).not.toContain('RA3')
    expect(est.acta).toBe(8)
  })

  it('reparte su ponderación proporcionalmente, no a partes iguales', () => {
    const p = ctxCon(ESTADOS).ponderaciones
    expect(p.RA3.efectiva).toBe(0)
    expect(p.RA3.original).toBe(50)
    // RA1 y RA2 tenían 25 cada uno sobre 100: al salir RA3 pasan a 50 y 50.
    expect(p.RA1.efectiva).toBeCloseTo(50)
    expect(p.RA2.efectiva).toBeCloseTo(50)
    expect(p.RA1.original).toBe(25)
  })

  it('conserva pesos desiguales al repartir', () => {
    const ras = [{ id: 'RA1', pond: 10 }, { id: 'RA2', pond: 30 }, { id: 'RA3', pond: 60 }]
    const p = reparterPonderaciones(ras, {
      RA1: ESTADO_RA.IMPARTIDO, RA2: ESTADO_RA.IMPARTIDO, RA3: ESTADO_RA.NO_IMPARTIDO,
    })
    // 10 y 30 sobre 40 → 25 % y 75 % del total.
    expect(p.RA1.efectiva).toBeCloseTo(25)
    expect(p.RA2.efectiva).toBeCloseTo(75)
    expect(p.RA1.efectiva + p.RA2.efectiva).toBeCloseTo(100)
  })
})

describe('RF-01 · el estado no lo decide la existencia de actividades', () => {
  it('crear o borrar actividades no cambia un estado ya declarado', () => {
    const declarado = { RA3: ESTADO_RA.IMPARTIDO }
    // RA3 no tiene ninguna actividad y aun así sigue impartido: lo dijo la docente.
    expect(ctxCon(declarado).raEstados.RA3).toBe(ESTADO_RA.IMPARTIDO)
    // Y un RA con actividades puede declararse no impartido sin que el motor
    // lo contradiga.
    const est = estadoImparticion(RAS, [{ id: 'RA1' }], { RA1: ESTADO_RA.NO_IMPARTIDO })
    expect(est.RA1).toBe(ESTADO_RA.NO_IMPARTIDO)
  })

  it('el valor por defecto solo se usa donde no hay decisión', () => {
    const est = estadoImparticion(RAS, [{ id: 'RA1' }, { id: 'RA2' }], { RA2: ESTADO_RA.PREVISTO })
    expect(est.RA1).toBe(ESTADO_RA.IMPARTIDO)   // tiene actividad
    expect(est.RA2).toBe(ESTADO_RA.PREVISTO)    // declarado a mano
    expect(est.RA3).toBe(ESTADO_RA.PREVISTO)    // sin actividad
  })
})

describe('RF-01 · pérdida del derecho a evaluación continua', () => {
  it('sigue exigiendo todos los RA salvo los no impartidos', () => {
    const estados = {
      RA1: ESTADO_RA.IMPARTIDO,
      RA2: ESTADO_RA.IMPARTIDO,
      RA3: { estado: ESTADO_RA.NO_IMPARTIDO, motivo: 'no dio tiempo' },
    }
    const acts = [
      { id: 9, ra_id: 'RA1', tipo: 'examen', peso: 1, nota_max: 10, convocatoria: 1, prueba_objetiva: 1 },
    ]
    const ctx = contextoModulo({
      ras: RAS, cesByRa: CES, asignaciones: [], actividades: acts,
      convocatoria: 1, raEstados: estados,
    })
    const est = estadoModulo(ctx, { 9: 9 }, { evalContinuaPerdida: true })
    // RA2 no lo cubre la prueba objetiva → PENDIENTE. RA3 no cuenta.
    expect(est.sinNota).toContain('RA2')
    expect(est.sinNota).not.toContain('RA3')
    expect(est.resultado).toBe('PENDIENTE')
  })
})

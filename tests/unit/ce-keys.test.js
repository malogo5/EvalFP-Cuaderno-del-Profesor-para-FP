import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

function loadCeKeys() {
  const source = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(source, context)
  return context.module.exports
}

const ce = loadCeKeys()

// Módulo de juguete con la forma real del catálogo: los criterios de cada RA se
// numeran desde CR1, así que el id suelto se repite en todos los RA.
const DATA = {
  modulo: { eval_count: 3 },
  ras: [{ id: 'RA1' }, { id: 'RA2' }, { id: 'RA3' }],
  ces: {
    RA1: [{ id: 'CR1', texto: 'a' }, { id: 'CR2', texto: 'b' }],
    RA2: [{ id: 'CR1', texto: 'c' }, { id: 'CR2', texto: 'd' }],
    RA3: [{ id: 'CR1', texto: 'e' }],
  },
  uts: [
    { id: 'UT1', eval: 1 },
    { id: 'UT2', eval: 2 },
    { id: 'UT3', eval: 3 },
  ],
  asignaciones: [
    { ut: 'UT1', ra: 'RA1', ces: ['CR1', 'CR2'] },
    { ut: 'UT2', ra: 'RA2', ces: ['CR1'] },
    { ut: 'UT2', ra: 'RA3', ces: ['CR1'] },   // una UT puede trabajar dos RA
  ],
  eval_ras: { 1: ['RA1'], 2: ['RA2', 'RA3'], 3: [] },
}

describe('Clave RA|CE', () => {
  it('identifica un criterio por su RA y su id', () => {
    expect(ce.ceKey('RA2', 'CR1')).toBe('RA2|CR1')
    expect(ce.ceKeyRa('RA2|CR1')).toBe('RA2')
    expect(ce.ceKeyCe('RA2|CR1')).toBe('CR1')
    expect(ce.ceKeyRa('CR1')).toBeNull()
  })

  it('una actividad solo cubre el criterio del RA que le corresponde', () => {
    const act = { ra_id: 'RA2', ces: '["RA2|CR1"]' }
    expect(ce.actCubreCe(act, 'RA2', 'CR1')).toBe(true)
    expect(ce.actCubreCe(act, 'RA1', 'CR1')).toBe(false)
    expect(ce.actCubreCe(act, 'RA3', 'CR1')).toBe(false)
  })
})

describe('RAs de una actividad', () => {
  it('devuelve todos los RA de sus UT, no solo el primero', () => {
    expect(ce.rasDeActividad({ ut_id: 'UT2' }, DATA.asignaciones)).toEqual(['RA2', 'RA3'])
    expect(ce.rasDeActividad({ ut_id: 'UT1,UT2' }, DATA.asignaciones)).toEqual(['RA1', 'RA2', 'RA3'])
  })

  it('sin UT, cae al ra_id', () => {
    expect(ce.rasDeActividad({ ra_id: 'RA1' }, DATA.asignaciones)).toEqual(['RA1'])
    expect(ce.rasDeActividad({}, DATA.asignaciones)).toEqual([])
  })
})

describe('Criterios disponibles de una actividad', () => {
  it('agrupa por RA y respeta lo asignado a la UT', () => {
    const grupos = ce.cesDisponiblesActividad({ ut_id: 'UT2' }, DATA.asignaciones, DATA.ces)
    expect(grupos.map(g => g.raId)).toEqual(['RA2', 'RA3'])
    expect(grupos[0].ces.map(c => c.id)).toEqual(['CR1'])   // CR2 de RA2 no está en la UT
  })
})

describe('Migración de criterios sueltos', () => {
  it('resuelve el id suelto contra el RA de la actividad', () => {
    const act = { ut_id: 'UT1', ces: '["CR1","CR2"]' }
    expect(ce.migrarCesActividad(act, DATA.asignaciones, DATA.ces)).toEqual(['RA1|CR1', 'RA1|CR2'])
  })

  it('en un examen de dos RA conserva el criterio en ambos', () => {
    const act = { ut_id: 'UT2', ces: '["CR1"]' }
    expect(ce.migrarCesActividad(act, DATA.asignaciones, DATA.ces)).toEqual(['RA2|CR1', 'RA3|CR1'])
  })

  it('descarta el criterio que no existe en ningún RA de la actividad', () => {
    const act = { ut_id: 'UT2', ces: '["CR2"]' }   // RA3 no tiene CR2 y RA2 sí, pero…
    expect(ce.migrarCesActividad(act, DATA.asignaciones, DATA.ces)).toEqual(['RA2|CR2'])
  })

  it('no toca lo que ya está migrado', () => {
    expect(ce.migrarCesActividad({ ut_id: 'UT1', ces: '["RA1|CR1"]' }, DATA.asignaciones, DATA.ces)).toBeNull()
    expect(ce.migrarCesActividad({ ut_id: 'UT1', ces: '[]' }, DATA.asignaciones, DATA.ces)).toBeNull()
  })
})

describe('RAs por evaluación', () => {
  it('sigue a la evaluación de las UT que trabajan cada RA', () => {
    expect(ce.rasPorEvaluacion(DATA, 3)).toEqual({ 1: ['RA1'], 2: ['RA2', 'RA3'], 3: [] })
  })

  it('mover una UT de trimestre mueve su RA', () => {
    const movido = { ...DATA, uts: [{ id: 'UT1', eval: 1 }, { id: 'UT2', eval: 3 }, { id: 'UT3', eval: 3 }] }
    expect(ce.rasPorEvaluacion(movido, 3)).toEqual({ 1: ['RA1'], 2: [], 3: ['RA2', 'RA3'] })
  })

  it('un RA sin UT conserva la evaluación del catálogo y no se duplica', () => {
    const suelto = { ...DATA, asignaciones: [{ ut: 'UT1', ra: 'RA1', ces: ['CR1'] }] }
    const mapa = ce.rasPorEvaluacion(suelto, 3)
    expect(mapa).toEqual({ 1: ['RA1'], 2: ['RA2', 'RA3'], 3: [] })
    const todos = Object.values(mapa).flat()
    expect(todos.length).toBe(new Set(todos).size)
  })
})

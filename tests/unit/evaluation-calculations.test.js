import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

function loadEvaluationCalculations() {
  const file = path.resolve('renderer/js/modules/evaluaciones.js')
  const source = fs.readFileSync(file, 'utf8')
  const purePart = source.slice(0, source.indexOf('async function saveMinExam'))
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(`${purePart}\nmodule.exports = { _mediaActs, _calcNotaRA, _calcNotaCE, _raMinExamKO, _actaEntera }`, context)
  return context.module.exports
}

const calc = loadEvaluationCalculations()

describe('Cálculos de evaluación', () => {
  it('pondera actividades calificadas por su peso', () => {
    const acts = [
      { id: 1, tipo: 'practica', peso: 30 },
      { id: 2, tipo: 'examen', peso: 70 },
    ]
    expect(calc._mediaActs(acts, { 1: 8, 2: 5 }, 0.3, 0.7)).toBeCloseTo(5.9)
  })

  it('calcula un RA mediante criterios vinculados y no mezcla otros CEs', () => {
    const acts = [
      { id: 1, ra_id: 'RA1', peso: 100, ces: '["CE1"]' },
      { id: 2, ra_id: 'RA1', peso: 100, ces: '["CE2"]' },
      { id: 3, ra_id: 'RA2', peso: 100, ces: '["CE3"]' },
    ]
    const ces = [{ id: 'CE1' }, { id: 'CE2' }]
    expect(calc._calcNotaRA('RA1', ces, acts, { 1: 8, 2: 4, 3: 10 }, 0.3, 0.7)).toBe(6)
    expect(calc._calcNotaCE('CE2', acts, { 1: 8, 2: 4 }, 0.3, 0.7)).toBe(4)
  })

  it('impide superar un RA si un examen está bajo el mínimo configurado', () => {
    const acts = [
      { id: 1, ra_id: 'RA1', tipo: 'practica', ces: '[]' },
      { id: 2, ra_id: 'RA1', tipo: 'examen', ces: '[]' },
    ]
    expect(calc._raMinExamKO('RA1', [], acts, { 1: 9, 2: 4.5 }, 5)).toBe(true)
    expect(calc._raMinExamKO('RA1', [], acts, { 1: 9, 2: 5 }, 5)).toBe(false)
    expect(calc._raMinExamKO('RA1', [], acts, { 1: 9, 2: 1 }, null)).toBe(false)
  })

  it('convierte a nota de acta sin permitir aprobar un módulo no superado', () => {
    expect(calc._actaEntera(6.5, true)).toBe(7)
    expect(calc._actaEntera(4.6, false)).toBe(4)
    expect(calc._actaEntera(8.9, false)).toBe(4)
    expect(calc._actaEntera(null, false)).toBeNull()
  })
})

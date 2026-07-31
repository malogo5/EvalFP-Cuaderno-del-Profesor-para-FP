import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

function loadEvaluationCalculations() {
  // ce-keys.js va delante: el motor de notas identifica los criterios con la
  // clave RA|CE que define ese archivo.
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const file = path.resolve('renderer/js/modules/evaluaciones.js')
  const source = fs.readFileSync(file, 'utf8')
  const purePart = source.slice(0, source.indexOf('async function saveMinExam'))
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(
    `${ceKeys}\n${purePart}\nmodule.exports = { _mediaActs, _calcNotaRA, _calcNotaCE, _raMinExamKO, _actaEntera, ceKey }`,
    context)
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
    expect(calc._calcNotaCE('RA1', 'CE2', acts, { 1: 8, 2: 4 }, 0.3, 0.7)).toBe(4)
  })

  // Los decretos numeran los criterios dentro de cada RA: CR1 existe en RA1, en
  // RA2 y en todos los demás. Si el motor compara solo el id suelto, la nota de
  // una práctica de RA2 se cuela en RA1 y las notas dejan de ser defendibles.
  describe('criterios con el mismo id en distintos RA', () => {
    const cesRA1 = [{ id: 'CR1' }, { id: 'CR2' }]
    const cesRA2 = [{ id: 'CR1' }, { id: 'CR2' }]
    const acts = [
      { id: 1, ra_id: 'RA1', tipo: 'practica', peso: 100, ces: '["RA1|CR1"]' },
      { id: 2, ra_id: 'RA1', tipo: 'practica', peso: 100, ces: '["RA1|CR2"]' },
      { id: 3, ra_id: 'RA2', tipo: 'practica', peso: 100, ces: '["RA2|CR1","RA2|CR2"]' },
    ]
    const notas = { 1: 8, 2: 6, 3: 2 }

    it('no mezcla el CR1 de RA1 con el CR1 de RA2', () => {
      expect(calc._calcNotaRA('RA1', cesRA1, acts, notas, 0.3, 0.7)).toBe(7)
      expect(calc._calcNotaRA('RA2', cesRA2, acts, notas, 0.3, 0.7)).toBe(2)
    })

    it('da la nota de cada criterio dentro de su RA', () => {
      expect(calc._calcNotaCE('RA1', 'CR1', acts, notas, 0.3, 0.7)).toBe(8)
      expect(calc._calcNotaCE('RA2', 'CR1', acts, notas, 0.3, 0.7)).toBe(2)
    })

    it('un examen suspenso de RA2 no bloquea el RA1', () => {
      const conExamen = [
        { id: 1, ra_id: 'RA1', tipo: 'practica', peso: 100, ces: '["RA1|CR1"]' },
        { id: 2, ra_id: 'RA2', tipo: 'examen', peso: 100, ces: '["RA2|CR1"]' },
      ]
      expect(calc._raMinExamKO('RA1', cesRA1, conExamen, { 1: 9, 2: 3 }, 5)).toBe(false)
      expect(calc._raMinExamKO('RA2', cesRA2, conExamen, { 1: 9, 2: 3 }, 5)).toBe(true)
    })

    it('una clave antigua sin RA solo cuenta en el RA de su actividad', () => {
      const legacy = [{ id: 1, ra_id: 'RA2', tipo: 'practica', peso: 100, ces: '["CR1"]' }]
      expect(calc._calcNotaCE('RA2', 'CR1', legacy, { 1: 4 }, 0.3, 0.7)).toBe(4)
      expect(calc._calcNotaCE('RA1', 'CR1', legacy, { 1: 4 }, 0.3, 0.7)).toBeNull()
    })
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

import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

function loadEvaluationCalculations() {
  // El motor vive en js/core/calificacion.js y se apoya en las claves RA|CE de
  // js/utils/ce-keys.js. Se cargan en el mismo orden que en la aplicación.
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const motor  = fs.readFileSync(path.resolve('renderer/js/core/calificacion.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  vm.runInNewContext(
    `${ceKeys}\n${motor}\nmodule.exports = { _mediaActs: mediaActividades, ` +
    `_calcNotaRA: notaRA, _calcNotaCE: notaCE, _raMinExamKO: raMinExamKO, ` +
    `_actaEntera: actaEntera, ceKey, notaEnEscala10, contextoModulo, estadoModulo }`,
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

  // `nota_max` es la escala del instrumento. Una práctica sobre 5 con un 4 vale
  // un 8, no un 4: durante mucho tiempo el campo se guardaba y no se usaba.
  describe('escala del instrumento (nota_max)', () => {
    it('lleva la nota a la escala 0-10', () => {
      expect(calc.notaEnEscala10(4, 5)).toBe(8)
      expect(calc.notaEnEscala10(20, 20)).toBe(10)
      expect(calc.notaEnEscala10(7, 10)).toBe(7)
    })

    it('no toca lo que no puede normalizar', () => {
      expect(calc.notaEnEscala10(7, 0)).toBe(7)
      expect(calc.notaEnEscala10(7, null)).toBe(7)
      expect(calc.notaEnEscala10(null, 5)).toBeNull()
    })

    it('la media de actividades respeta la escala de cada una', () => {
      const acts = [
        { id: 1, tipo: 'practica', peso: 50, nota_max: 5 },   // 4/5  = 8
        { id: 2, tipo: 'practica', peso: 50, nota_max: 10 },  // 6/10 = 6
      ]
      expect(calc._mediaActs(acts, { 1: 4, 2: 6 }, 0.3, 0.7)).toBe(7)
    })
  })
})

// Todas las pantallas tienen que dar la MISMA nota. Antes cada una calculaba por
// su cuenta y el mismo alumno tenía 6,25 en Evaluaciones, 7,25 en el Dashboard y
// 6,75 en el boletín que se llevaba a casa.
describe('Un solo veredicto para el mismo alumno', () => {
  const ctx = calc.contextoModulo({
    ras: [{ id: 'RA1', pond: 70 }, { id: 'RA2', pond: 30 }],
    cesByRa: { RA1: [{ id: 'CR1' }, { id: 'CR2' }], RA2: [{ id: 'CR1' }, { id: 'CR2' }] },
    asignaciones: [{ ut: 'UT1', ra: 'RA1', ces: ['CR1', 'CR2'] }, { ut: 'UT2', ra: 'RA2', ces: ['CR1', 'CR2'] }],
    actividades: [
      { id: 1, ut_id: 'UT1', ra_id: 'RA1', tipo: 'practica', peso: 30, ces: '["RA1|CR1"]' },
      { id: 2, ut_id: 'UT1', ra_id: 'RA1', tipo: 'examen', peso: 70, ces: '["RA1|CR2"]' },
      { id: 3, ut_id: 'UT2', ra_id: 'RA2', tipo: 'practica', peso: 30, ces: '["RA2|CR1"]' },
      { id: 4, ut_id: 'UT2', ra_id: 'RA2', tipo: 'examen', peso: 70, ces: '["RA2|CR2"]' },
    ],
    minExam: null,
  })

  it('la nota final es la media de los RA ponderada por su peso', () => {
    const st = calc.estadoModulo(ctx, { 1: 9, 2: 4, 3: 8, 4: 8 })
    expect(st.porRA.RA1.nota).toBe(6.5)
    expect(st.porRA.RA2.nota).toBe(8)
    expect(st.media).toBeCloseTo(6.95)   // 6,5×70 + 8×30
    expect(st.superado).toBe(true)
    expect(st.acta).toBe(7)
  })

  it('la media no compensa un RA suspenso y el acta se topa en 4', () => {
    const st = calc.estadoModulo(ctx, { 1: 10, 2: 10, 3: 2, 4: 2 })
    expect(st.media).toBeCloseTo(7.6)     // 10×70 + 2×30
    expect(st.pendientes).toEqual(['RA2'])
    expect(st.superado).toBe(false)
    expect(st.acta).toBe(4)               // art. 25.5: sin todos los RA, máximo 4
  })

  it('un RA sin calificar deja el módulo pendiente y no cuenta como cero', () => {
    const st = calc.estadoModulo(ctx, { 1: 8, 2: 8 })
    expect(st.porRA.RA1.nota).toBe(8)
    expect(st.porRA.RA2.nota).toBeNull()
    expect(st.media).toBe(8)             // reponderado sobre los RA evaluados
    expect(st.sinNota).toEqual(['RA2'])
    expect(st.completo).toBe(false)
    expect(st.superado).toBe(false)
  })
})

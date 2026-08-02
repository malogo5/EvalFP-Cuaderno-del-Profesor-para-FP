import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'

/**
 * El catálogo son 91 módulos con 4.444 criterios copiados de los decretos del
 * DOCM. Nadie los va a revisar a mano cada vez, así que estas comprobaciones
 * fijan lo que tiene que cumplir cualquier módulo para que las pantallas no
 * enseñen huecos ni la nota salga torcida.
 */

const data = JSON.parse(fs.readFileSync(path.resolve('renderer/modules_data.json'), 'utf8'))
const modulos = Object.entries(data.modules)

describe('Catálogo de módulos de Castilla-La Mancha', () => {
  it('tiene los 91 módulos, y el índice concuerda', () => {
    expect(modulos.length).toBe(91)
    expect(data.index.length).toBe(modulos.length)
  })

  it('ninguna ficha se queda sin ciclo, nombre, sigla ni decreto', () => {
    // Cuatro módulos de Informática de Oficina tenían el ciclo vacío y el
    // boletín, que se entrega a la familia, salía con el hueco.
    const faltas = []
    for (const [k, m] of modulos) {
      for (const campo of ['nombre', 'abrev', 'ciclo', 'curso', 'decreto']) {
        if (!String(m.modulo?.[campo] || '').trim()) faltas.push(`${k} sin ${campo}`)
      }
    }
    expect(faltas).toEqual([])
  })

  it('cada resultado de aprendizaje lleva sus criterios y su peso', () => {
    const faltas = []
    for (const [k, m] of modulos) {
      const ras = m.ras || []
      if (!ras.length) { faltas.push(`${k} sin RA`); continue }
      const sinCe = ras.filter(r => !(m.ces?.[r.id] || []).length).map(r => r.id)
      if (sinCe.length) faltas.push(`${k}: ${sinCe.join(',')} sin criterios`)
      const suma = ras.reduce((s, r) => s + Number(r.pond || 0), 0)
      if (Math.abs(suma - 100) > 0.5) faltas.push(`${k}: ponderación ${suma}`)
    }
    expect(faltas).toEqual([])
  })

  it('las unidades y los criterios asignados existen de verdad', () => {
    const faltas = []
    for (const [k, m] of modulos) {
      const raIds = new Set((m.ras || []).map(r => r.id))
      const utIds = new Set((m.uts || []).map(u => u.id))
      for (const a of m.asignaciones || []) {
        if (!raIds.has(a.ra) || !utIds.has(a.ut)) { faltas.push(`${k}: ${a.ut}→${a.ra} huérfana`); continue }
        const disponibles = new Set((m.ces?.[a.ra] || []).map(c => c.id))
        const malos = (a.ces || []).filter(c => !disponibles.has(c))
        if (malos.length) faltas.push(`${k}: ${a.ra} no tiene ${malos.join(',')}`)
      }
    }
    expect(faltas).toEqual([])
  })

  it('cada curso tiene las evaluaciones que le tocan', () => {
    // En 2º el curso acaba antes para ir a la empresa: dos trimestres. Los
    // cursos de especialización duran menos de un año y van igual. Dos módulos
    // de especialización se habían quedado con tres mientras sus compañeros de
    // curso tenían dos, y el boletín del mismo alumno no cuadraba entre módulos.
    const faltas = []
    for (const [k, m] of modulos) {
      const ec = Number(m.modulo?.eval_count || 3)
      const curso = String(m.modulo?.curso || '')
      const esperado = (curso.startsWith('2') || curso.toUpperCase().startsWith('CE')) ? 2 : 3
      if (ec !== esperado) faltas.push(`${k}: ${curso} con ${ec} evaluaciones`)
      const fuera = (m.uts || []).filter(u => Number(u.eval || 1) > ec).map(u => u.id)
      if (fuera.length) faltas.push(`${k}: ${fuera.join(',')} fuera de plazo`)
    }
    expect(faltas).toEqual([])
  })

  it('todos los módulos del mismo curso se organizan igual', () => {
    const porCurso = {}
    for (const [k, m] of modulos) {
      const curso = String(m.modulo?.curso || '')
      ;(porCurso[curso] ||= []).push([k, Number(m.modulo?.eval_count || 3)])
    }
    const discrepan = []
    for (const [curso, lista] of Object.entries(porCurso)) {
      const distintos = [...new Set(lista.map(([, ec]) => ec))]
      if (distintos.length > 1) discrepan.push(`${curso}: ${lista.map(([k, ec]) => `${k}=${ec}`).join(', ')}`)
    }
    expect(discrepan).toEqual([])
  })

  it('las actividades de cada evaluación suman 100 y llevan criterios', () => {
    const faltas = []
    for (const [k, m] of modulos) {
      const porEv = {}
      for (const a of m.actividades || []) {
        porEv[a.eval || 1] = (porEv[a.eval || 1] || 0) + Number(a.peso || 0)
        if (!(a.ces || []).length) faltas.push(`${k}: «${a.descripcion}» sin criterios`)
      }
      for (const [ev, peso] of Object.entries(porEv)) {
        if (Math.abs(peso - 100) > 0.5) faltas.push(`${k}: evaluación ${ev} suma ${peso}`)
      }
    }
    expect(faltas).toEqual([])
  })
})

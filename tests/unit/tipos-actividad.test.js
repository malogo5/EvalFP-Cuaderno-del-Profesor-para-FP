import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'
import vm from 'vm'

/**
 * RF-17 · Tipos de actividad y familia de reparto (docs/rediseno/00-CONTEXTO.md §10).
 *
 * `calificacion.js` no se toca: sigue leyendo `a.tipo === 'practica'|'examen'`
 * tal cual, en `mediaActividades`, `pesosPorTipo` y `examenesQueDeciden`. Lo
 * que cambia es que, antes de llegar ahí, `resolverFamilia` (de
 * renderer/js/utils/tipos-actividad.js) sustituye el tipo real de cada
 * actividad por su familia. Este archivo prueba esa sustitución en sí misma
 * (sin electron, sin IPC) y, sobre todo, que aplicarla a datos que hoy
 * existen no cambia ni una nota.
 */
function cargarMotor() {
  const ceKeys = fs.readFileSync(path.resolve('renderer/js/utils/ce-keys.js'), 'utf8')
  const tipos  = fs.readFileSync(path.resolve('renderer/js/utils/tipos-actividad.js'), 'utf8')
  const motor  = fs.readFileSync(path.resolve('renderer/js/core/calificacion.js'), 'utf8')
  const context = { module: { exports: {} }, console }
  // El trailer une los tres module.exports: el de calificacion.js pisa a los
  // anteriores porque se ejecuta el último, así que se recogen aparte.
  vm.runInNewContext(
    `${ceKeys}\n${tipos}\n${motor}\n` +
    `module.exports = { ...module.exports, resolverFamilia, familiaDeTipo, TIPOS_ACTIVIDAD, DEFECTO_FAMILIA }`,
    context
  )
  return context.module.exports
}

const {
  contextoModulo, estadoModulo, resolverFamilia, familiaDeTipo, TIPOS_ACTIVIDAD,
} = cargarMotor()

const RAS = [
  { id: 'RA1', pond: 40 },
  { id: 'RA2', pond: 60 },
]
const CES = {
  RA1: [{ id: 'a' }, { id: 'b' }],
  RA2: [{ id: 'a' }],
}
// Caso realista: una práctica, un examen, y una actividad de un tipo NUEVO
// (proyecto) que hoy no existe en ninguna base real.
const ACTIVIDADES = [
  { id: 1, ra_id: 'RA1', tipo: 'practica', peso: 30, nota_max: 10, eval: 1, convocatoria: 1,
    ces: ['RA1|a'] },
  { id: 2, ra_id: 'RA1', tipo: 'examen', peso: 70, nota_max: 10, eval: 1, convocatoria: 1,
    ces: ['RA1|a', 'RA1|b'] },
  { id: 3, ra_id: 'RA2', tipo: 'proyecto', peso: 100, nota_max: 10, eval: 1, convocatoria: 1,
    ces: ['RA2|a'] },
]
const NOTAS = { 1: 6, 2: 8, 3: 7 }

const ctxCon = actividades => contextoModulo({
  ras: RAS, cesByRa: CES, asignaciones: [], actividades, convocatoria: 1,
})

describe('RF-17 · TIPOS_ACTIVIDAD, fuente única con RF-02', () => {
  it('son exactamente los siete valores del documento, ni uno más', () => {
    expect(TIPOS_ACTIVIDAD.map(t => t.id)).toEqual([
      'examen', 'practica', 'proyecto', 'observacion', 'exposicion', 'trabajo', 'cuestionario',
    ])
    // 'empresa' ya no es un tipo: es la dualización de ra_catalogo.dual_pct.
    expect(TIPOS_ACTIVIDAD.some(t => t.id === 'empresa')).toBe(false)
  })

  it('cada tipo declara una familia de reparto válida', () => {
    for (const t of TIPOS_ACTIVIDAD) {
      expect(['examen', 'practica']).toContain(t.familiaDefecto)
    }
  })
})

describe('RF-17 · familiaDeTipo — jerarquía override → defecto → cierre', () => {
  it('sin override, usa el defecto del tipo', () => {
    expect(familiaDeTipo('cuestionario', {})).toEqual({ familia: 'examen', disparoDeCierre: false })
    expect(familiaDeTipo('proyecto', {})).toEqual({ familia: 'practica', disparoDeCierre: false })
  })

  it('el override del módulo prevalece sobre el defecto', () => {
    expect(familiaDeTipo('cuestionario', { cuestionario: 'practica' }))
      .toEqual({ familia: 'practica', disparoDeCierre: false })
  })

  it('un tipo que ninguna lista conoce cae en practica, marcado como disparo de cierre', () => {
    const r = familiaDeTipo('un_tipo_inventado', {})
    expect(r.familia).toBe('practica')
    expect(r.disparoDeCierre).toBe(true)
  })
})

describe('RF-17 · resolverFamilia', () => {
  it('sustituye el tipo por la familia y no toca nada más del objeto', () => {
    const { actividades } = resolverFamilia(ACTIVIDADES, {})
    expect(actividades.map(a => a.tipo)).toEqual(['practica', 'examen', 'practica'])
    // El resto de campos, intactos.
    expect(actividades[2]).toMatchObject({ id: 3, ra_id: 'RA2', peso: 100, ces: ['RA2|a'] })
    // El array de entrada no se muta.
    expect(ACTIVIDADES[2].tipo).toBe('proyecto')
  })

  it('un tipo desconocido se reporta en tiposSinClasificar, no se clasifica en silencio', () => {
    const conBasura = [...ACTIVIDADES, { id: 4, ra_id: 'RA2', tipo: 'zzz', peso: 0, nota_max: 10 }]
    const { tiposSinClasificar } = resolverFamilia(conBasura, {})
    expect(tiposSinClasificar).toEqual(['zzz'])
  })

  it('con override, un tipo cambia de familia de verdad', () => {
    const { actividades } = resolverFamilia(ACTIVIDADES, { proyecto: 'examen' })
    expect(actividades[2].tipo).toBe('examen')
  })
})

describe('RF-17 · migrar a resolverFamilia no cambia ninguna nota ya calculada', () => {
  // "Antes de la migración": el camino de hoy, actividades tal cual —
  // válido porque hoy solo existen 'practica' y 'examen', y son también su
  // propia familia.
  const SOLO_HOY = ACTIVIDADES.filter(a => a.tipo !== 'proyecto')

  it('estadoModulo da exactamente el mismo resultado con y sin pasar por resolverFamilia', () => {
    const antes  = estadoModulo(ctxCon(SOLO_HOY), NOTAS)
    const { actividades: actsResueltas } = resolverFamilia(SOLO_HOY, {})
    const despues = estadoModulo(ctxCon(actsResueltas), NOTAS)
    expect(despues).toEqual(antes)
  })

  it('con un tipo nuevo, la ponderación ya no desaparece del reparto', () => {
    // 'proyecto' no es ni 'practica' ni 'examen': mientras la actividad tenga
    // su propio peso, mediaActividades pondera por `a.peso` y no mira el
    // tipo, así que ese caso no lo delata. Donde SÍ desaparece es en el
    // reparto por tipo (pesosPorTipo), que solo entra en juego cuando ninguna
    // actividad calificada tiene peso propio — de ahí la actividad sin peso.
    const sinPeso = ACTIVIDADES.map(a => a.tipo === 'proyecto' ? { ...a, peso: 0 } : a)
    const notaRA2SinResolver = estadoModulo(ctxCon(sinPeso), NOTAS).porRA.RA2.nota
    const { actividades: sinPesoResueltas } = resolverFamilia(sinPeso, {})
    const notaRA2ConResolver = estadoModulo(ctxCon(sinPesoResueltas), NOTAS).porRA.RA2.nota

    expect(notaRA2SinResolver).toBeNull()      // 'proyecto' no es 'practica' ni 'examen': desaparece
    expect(notaRA2ConResolver).toBeCloseTo(7)  // resuelto a 'practica', vuelve a contar
  })
})

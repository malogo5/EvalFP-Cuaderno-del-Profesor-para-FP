import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'

/**
 * La auditoría encontró cuatro motores de cálculo distintos conviviendo: el mismo
 * alumno tenía 6,25 en Evaluaciones, 7,25 en el Dashboard y 6,75 en el boletín.
 * Estos tests no comprueban un resultado, comprueban que no vuelva a pasar: si
 * alguien reimplementa una media de notas fuera de `js/core/calificacion.js`,
 * fallan y explican por qué.
 */

const leer = rel => fs.readFileSync(path.resolve(rel), 'utf8')

const PANTALLAS = [
  'renderer/js/modules/evaluaciones.js',
  'renderer/js/modules/dashboard.js',
  'renderer/js/modules/notas.js',
  'renderer/js/modules/ia.js',
]

describe('Un único motor de calificación', () => {
  it('existe y exporta lo que las pantallas necesitan', () => {
    const motor = leer('renderer/js/core/calificacion.js')
    for (const fn of ['notaCE', 'notaRA', 'raMinExamKO', 'actaEntera',
                      'contextoModulo', 'estadoModulo', 'mediaActividades',
                      'notaEnEscala10', 'etiquetaResultado', 'calificacionCualitativa']) {
      expect(motor, `falta ${fn} en el motor`).toContain(`function ${fn}`)
    }
  })

  it('ninguna pantalla calcula la nota final por su cuenta', () => {
    // El patrón que delataba a los motores paralelos: sumar notas y dividir entre
    // el número de elementos para obtener «la nota» del alumno.
    const sospechoso = /media\s*=\s*ns\.reduce|reduce\(\(a,\s*b\)\s*=>\s*a\s*\+\s*b\s*,\s*0\)\s*\/\s*ns\.length/
    for (const archivo of PANTALLAS) {
      expect(leer(archivo), `${archivo} parece calcular una media propia`).not.toMatch(sospechoso)
    }
  })

  it('las pantallas piden el veredicto al motor, no lo deciden ellas', () => {
    const evaluaciones = leer('renderer/js/modules/evaluaciones.js')
    const dashboard = leer('renderer/js/modules/dashboard.js')
    expect(evaluaciones).toContain('estadoModulo(')
    expect(dashboard).toContain('estadoModulo(')
    // El boletín es el documento que sale del centro: tiene que salir del motor
    expect(dashboard, 'el boletín no usa el motor').toContain('estadoModulo(ctxBol')
  })

  it('la escala del instrumento se aplica en un solo sitio', () => {
    const motor = leer('renderer/js/core/calificacion.js')
    expect(motor).toContain('function notaEnEscala10')
    // Nadie más debe dividir por nota_max a mano
    for (const archivo of PANTALLAS) {
      expect(leer(archivo), `${archivo} normaliza nota_max por su cuenta`)
        .not.toMatch(/\/\s*\(?\s*a\.nota_max/)
    }
  })

  it('la migración de criterios se hace en la base, no en las pantallas', () => {
    expect(leer('db.js')).toContain('_migrarCesDeActividades')
    for (const archivo of PANTALLAS.concat('renderer/js/modules/programacion.js')) {
      expect(leer(archivo), `${archivo} vuelve a migrar datos al cargarse`)
        .not.toContain('_migrarCesActividades(')
    }
  })
})

describe('Criterios de evaluación identificados por RA y CE', () => {
  it('nadie compara criterios por su id suelto', () => {
    // «CR1» existe en todos los RA del módulo: compararlo solo delata el fallo
    // que mezclaba las notas de resultados de aprendizaje distintos.
    const sospechoso = /JSON\.parse\(\s*a\.ces[^)]*\)\s*\.\s*(includes|some)\s*\(/
    for (const archivo of PANTALLAS) {
      expect(leer(archivo), `${archivo} compara criterios sin el RA`).not.toMatch(sospechoso)
    }
  })
})

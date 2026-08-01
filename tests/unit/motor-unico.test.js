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

describe('El superado parcial cuenta como superado (art. 18.4)', () => {
  it('los indicadores de cabecera cuentan también el SP', () => {
    // Visto en uso: la cabecera decía «Superan 0 · No superan 5» mientras dos
    // filas de esa misma tabla ponían APTO/A · SP. Quien ha alcanzado todos los
    // RA y solo tiene pendiente la fase en empresa promociona (art. 18.4).
    const ev = leer('renderer/js/modules/evaluaciones.js')
    expect(ev, '1ª convocatoria').toContain('estados[al.id].superadoParaPromocion')
    expect(ev, '2ª convocatoria').toContain('estados2[al.id].superadoParaPromocion')

    const dash = leer('renderer/js/modules/dashboard.js')
    expect(dash, 'vista de clase').toContain('superado: st.superadoParaPromocion')
  })

  it('nadie decide la etiqueta del acta con un booleano', () => {
    // El art. 12 tiene TRES estados. Un ternario APTO/NO APTO no puede
    // representarlos: el «superado parcial» acaba saliendo como NO APTO/A, que
    // es justo lo que pasaba en la línea de 2ª convocatoria del boletín.
    for (const archivo of ['renderer/js/modules/evaluaciones.js',
                           'renderer/js/modules/dashboard.js']) {
      expect(leer(archivo), `${archivo} decide APTO/NO APTO con un booleano`)
        .not.toMatch(/\?\s*'APTO\/A'\s*:\s*'NO APTO\/A'/)
    }
  })

  it('nadie promedia criterios a mano para la 2ª convocatoria', () => {
    // Se han encontrado ya SIETE sitios calculando su propia 2ª convocatoria:
    // Evaluaciones, el boletín, las tarjetas del Dashboard, su contador de
    // pendientes, sus iconos y el informe de la IA. Todos promediaban los
    // criterios a peso igual, ignorando la ponderación del art. 4.3.a, y ninguno
    // veía las actividades de recuperación.
    const sospechoso = /\bg\.reduce\(|grades\.reduce\(|ceGrades\.reduce\(/
    for (const archivo of PANTALLAS.concat('renderer/js/modules/programacion.js')) {
      expect(leer(archivo), `${archivo} promedia criterios por su cuenta`).not.toMatch(sospechoso)
    }
  })

  it('el motor sigue exponiendo los dos conceptos por separado', () => {
    // `superado` (art. 2.3, todo alcanzado incluida la empresa) y
    // `superadoParaPromocion` (art. 18.4, el SP también) no son lo mismo: el
    // acta necesita distinguirlos.
    const motor = leer('renderer/js/core/calificacion.js')
    expect(motor).toContain('superadoParaPromocion')
    expect(motor).toContain("const superado = resultado === 'SUPERADO'")
  })

  it('el asistente de IA no se calcula sus propias notas por RA', () => {
    // Octavo y noveno motor: el informe individual se construía las notas a
    // mano —sin ver las pruebas de la 2ª convocatoria ni los RA cerrados— y la
    // radiografía del grupo se las calculaba en Python con una media aritmética
    // de las notas crudas, sin peso ni escala de instrumento.
    const ia = leer('renderer/js/modules/ia.js')
    expect(ia, 'el informe de la IA no usa el motor').toContain('contextoModulo(')
    expect(ia, 'el informe de la IA no usa el motor').toContain('estadoModulo(')
    expect(ia, 'el grupo no manda sus notas calculadas').toContain('opts.notasRaJson')

    const py = leer('scripts/ai_asistente.py')
    expect(py, 'Python no acepta las notas por RA de la aplicación').toContain('--notas-ra-json')
  })
})

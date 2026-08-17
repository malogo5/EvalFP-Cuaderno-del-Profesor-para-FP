/**
 * RF-02 · Programación normalizada — tests de `migrarProgramacionNormalizada()`.
 * Ver docs/rediseno/05-PLAN-MIGRACION.md.
 *
 * Solo esquema y migración de datos: nada aquí toca renderer/. El paso 1 de la
 * implementación crea las tablas nuevas y las llena a partir de modulos.data_json,
 * fail-closed, sin que ninguna pantalla llegue todavía a leerlas.
 */
import { describe, it, expect, afterEach } from 'vitest'
import os   from 'os'
import path from 'path'
import fs   from 'fs'

const sqliteDisponible = await import('node:sqlite').then(() => true, () => false)
if (!sqliteDisponible) {
  console.warn(
    `\n⚠️  tests/unit/programacion-normalizada.test.js omitido: este Node (${process.version}) ` +
    'no expone node:sqlite. Para ejecutarlos, usa Node >= 22.5.\n'
  )
}
const db = sqliteDisponible ? await import('../../db.js') : null

afterEach(() => {
  try {
    db.closeDb()
    const dbDir  = path.join(os.tmpdir(), `evalfp-test-${process.pid}`)
    const dbFile = path.join(dbDir, 'evalfp.db')
    if (fs.existsSync(dbFile)) fs.unlinkSync(dbFile)
  } catch {
    // Limpieza best-effort.
  }
})

// ── Fixture: un módulo pequeño pero con todas las formas de dato reales ──────
// (RA con override de ponderación, CE con y sin peso, UT con horas de empresa,
// instrumentos por RA, y actividades que ya llevan sus criterios en RA|CE).
function datosFixture() {
  return {
    modulo: { eval_count: 3 },
    ras: [
      { id: 'RA1', nombre: 'Resultado uno', pond: 40, llave: true, dual: 20 },
      { id: 'RA2', nombre: 'Resultado dos', pond: 60 },
    ],
    ces: {
      RA1: [
        { id: 'CR1', texto: 'Criterio 1 de RA1' },
        { id: 'CR2', texto: 'Criterio 2 de RA1', peso: 50 },
      ],
      RA2: [
        { id: 'CR1', texto: 'Criterio 1 de RA2' },
      ],
    },
    uts: [
      { id: 'UT1', nombre: 'Unidad uno', horas: 20, eval: 1, tags: 'a,b' },
      { id: 'UT2', nombre: 'Unidad dos', horas: 15, horas_empresa: 5, eval: 2 },
    ],
    asignaciones: [
      { ut: 'UT1', ra: 'RA1', ces: ['CR1', 'CR2'] },
      { ut: 'UT2', ra: 'RA2', ces: ['CR1'] },
    ],
    eval_ras: { 1: ['RA1'], 2: ['RA2'] },
    ra_instrumentos: { RA1: ['practica', 'examen'], RA2: ['examen'] },
    actividades: [],
  }
}

function actividadesFixture() {
  return [
    { ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Práctica RA1', instrumento: 'Práctica',
      tipo: 'practica', peso: 5, nota_max: 10, eval: 1, orden: 1, ces: ['RA1|CR1', 'RA1|CR2'] },
    { ut_id: 'UT2', ra_id: 'RA2', descripcion: 'Práctica RA2', instrumento: 'Práctica',
      tipo: 'practica', peso: 5, nota_max: 10, eval: 2, orden: 2, ces: ['RA2|CR1'] },
  ]
}

function crearModulo(key) {
  return db.addModulo({
    key, abrev: key, nombre: `Módulo ${key}`, ciclo: 'CFGS Test', curso: '1', anno: '2026-2027',
    grupo: 'Grupo A', horas: 100, decreto: null,
    actividades: actividadesFixture(), data: datosFixture(),
  })
}

describe.skipIf(!sqliteDisponible)('RF-02 · migrarProgramacionNormalizada()', () => {
  it('una base sin migrar queda correctamente migrada', () => {
    const mid = crearModulo('MOD_OK')
    // Override de ponderación (RF-01): el valor efectivo debe salir de aquí,
    // no del 40 del JSON.
    db.setRaPonderacion(mid, 'RA1', 45)

    const resumen = db.migrarProgramacionNormalizada()

    expect(resumen.modulos).toBe(1)
    expect(resumen.ra_catalogo).toBe(2)                 // RA1, RA2
    expect(resumen.ce_catalogo).toBe(3)                 // RA1·CR1, RA1·CR2, RA2·CR1
    expect(resumen.unidades_trabajo).toBe(2)             // UT1, UT2
    expect(resumen.ut_ce).toBe(3)                        // UT1→RA1·CR1, UT1→RA1·CR2, UT2→RA2·CR1
    expect(resumen.ce_instrumentos_previstos).toBe(5)    // RA1: 2 CE×2 instr=4; RA2: 1 CE×1 instr=1
    expect(resumen.actividad_ce).toBe(3)                 // 2 claves de la 1ª actividad + 1 de la 2ª

    const raw = db.TEST_ONLY_rawDb()
    const ra1 = raw.prepare('SELECT * FROM ra_catalogo WHERE modulo_id=? AND ra_id=?').get(mid, 'RA1')
    expect(ra1.pond).toBe(45)          // el override, no el 40 del JSON
    expect(ra1.llave).toBe(1)
    expect(ra1.dual_pct).toBe(20)

    const ra2 = raw.prepare('SELECT * FROM ra_catalogo WHERE modulo_id=? AND ra_id=?').get(mid, 'RA2')
    expect(ra2.pond).toBe(60)          // sin override, el del JSON

    const cr2 = raw.prepare('SELECT * FROM ce_catalogo WHERE modulo_id=? AND ra_id=? AND ce_id=?')
      .get(mid, 'RA1', 'CR2')
    expect(cr2.peso).toBe(50)
    const cr1 = raw.prepare('SELECT * FROM ce_catalogo WHERE modulo_id=? AND ra_id=? AND ce_id=?')
      .get(mid, 'RA1', 'CR1')
    expect(cr1.peso).toBeNull()        // reparto automático, no 0

    const ut2 = raw.prepare('SELECT * FROM unidades_trabajo WHERE modulo_id=? AND ut_id=?').get(mid, 'UT2')
    expect(ut2.horas_empresa).toBe(5)

    // PRAGMA foreign_key_check queda sin filas (también se comprueba aparte, más abajo).
    expect(raw.prepare('PRAGMA foreign_key_check').all()).toEqual([])
  })

  it('un módulo con un criterio huérfano aborta con ROLLBACK, con el módulo y el motivo en el mensaje', () => {
    const mid = crearModulo('MOD_HUERFANO')
    const raw = db.TEST_ONLY_rawDb()
    const act = raw.prepare('SELECT id FROM actividades WHERE modulo_id=? ORDER BY id LIMIT 1').get(mid)
    // Se corrompe a mano: la actividad pasa a evaluar un CE que no existe en el catálogo.
    raw.prepare('UPDATE actividades SET ces=? WHERE id=?')
      .run(JSON.stringify(['RA1|CR99']), act.id)

    let error = null
    try {
      db.migrarProgramacionNormalizada()
    } catch (e) {
      error = e
    }

    expect(error).not.toBeNull()
    expect(error.message).toContain(String(mid))
    expect(error.message).toContain('MOD_HUERFANO')
    expect(error.message).toContain('RA1|CR99')

    // ROLLBACK de TODA la migración, no solo de este módulo: nada se confirma.
    expect(raw.prepare('SELECT COUNT(*) AS n FROM ra_catalogo').get().n).toBe(0)
    expect(raw.prepare('SELECT COUNT(*) AS n FROM ce_catalogo').get().n).toBe(0)
    expect(raw.prepare('SELECT COUNT(*) AS n FROM unidades_trabajo').get().n).toBe(0)
    expect(raw.prepare('SELECT COUNT(*) AS n FROM ut_ce').get().n).toBe(0)
    expect(raw.prepare('SELECT COUNT(*) AS n FROM ce_instrumentos_previstos').get().n).toBe(0)
    expect(raw.prepare('SELECT COUNT(*) AS n FROM actividad_ce').get().n).toBe(0)
  })

  it('PRAGMA foreign_key_check queda sin filas tras una migración con varios módulos', () => {
    crearModulo('MOD_A')
    crearModulo('MOD_B')
    db.migrarProgramacionNormalizada()

    const raw = db.TEST_ONLY_rawDb()
    expect(raw.prepare('PRAGMA foreign_key_check').all()).toEqual([])
  })

  it('una fila de actividad_ce que cruce módulos es rechazada por las claves foráneas', () => {
    const midA = crearModulo('MOD_CRUCE_A')
    const midB = crearModulo('MOD_CRUCE_B')
    db.migrarProgramacionNormalizada()   // deja ce_catalogo poblado en ambos módulos

    const raw = db.TEST_ONLY_rawDb()
    const actA = raw.prepare('SELECT id FROM actividades WHERE modulo_id=? ORDER BY id LIMIT 1').get(midA)
    // actA (UT1/RA1) ya tiene actividad_ce para RA1|CR1 y RA1|CR2 (de la migración
    // real de arriba): se usa RA2|CR1, que actA no evalúa, para no chocar con esa
    // clave primaria y así aislar el rechazo por la FK, no por duplicado.

    // actividad_id es de MOD_CRUCE_A, pero modulo_id apunta a MOD_CRUCE_B (con un
    // RA|CE que sí existe en B): la FK compuesta (actividad_id, modulo_id) →
    // actividades(id, modulo_id) tiene que rechazarlo igualmente.
    expect(() => {
      raw.prepare('INSERT INTO actividad_ce (actividad_id, modulo_id, ra_id, ce_id) VALUES (?,?,?,?)')
        .run(actA.id, midB, 'RA2', 'CR1')
    }).toThrow(/FOREIGN KEY/i)

    // Y, en el otro sentido: modulo_id correcto pero un CE que no existe en ese módulo.
    expect(() => {
      raw.prepare('INSERT INTO actividad_ce (actividad_id, modulo_id, ra_id, ce_id) VALUES (?,?,?,?)')
        .run(actA.id, midA, 'RA1', 'CR_NO_EXISTE')
    }).toThrow(/FOREIGN KEY/i)
  })

  it('ejecutar la migración dos veces no duplica nada', () => {
    const mid = crearModulo('MOD_DOBLE')
    db.setRaPonderacion(mid, 'RA1', 45)

    const primero = db.migrarProgramacionNormalizada()
    const raw = db.TEST_ONLY_rawDb()
    const contar = tabla => raw.prepare(`SELECT COUNT(*) AS n FROM ${tabla}`).get().n
    const tablas = ['ra_catalogo', 'ce_catalogo', 'unidades_trabajo', 'ut_ce',
                     'ce_instrumentos_previstos', 'actividad_ce']
    const cuentasTrasPrimero = Object.fromEntries(tablas.map(t => [t, contar(t)]))

    const segundo = db.migrarProgramacionNormalizada()
    const cuentasTrasSegundo = Object.fromEntries(tablas.map(t => [t, contar(t)]))

    expect(cuentasTrasSegundo).toEqual(cuentasTrasPrimero)
    expect(segundo).toEqual(primero)

    // El valor con override se mantiene igual, no se duplica ni cambia solo.
    const ra1 = raw.prepare('SELECT pond FROM ra_catalogo WHERE modulo_id=? AND ra_id=?').get(mid, 'RA1')
    expect(ra1.pond).toBe(45)
  })
})

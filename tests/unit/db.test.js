/**
 * Tests unitarios para db.js
 * Framework: Vitest
 *
 * Ejecutar: npm test
 * (requiere npm install primero)
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import os   from 'os'
import path from 'path'
import fs   from 'fs'

// El mock de electron se inyecta en require.cache vía tests/unit/setup.js
// (setupFiles en vitest.config.js) antes de que cualquier módulo cargue.
// `node:sqlite` está disponible en Electron y en Node >= 22.5 (con
// --experimental-sqlite) o Node >= 23.4. Si este Node no lo trae, la suite se
// salta con aviso en lugar de romper toda la ejecución de `npm test`.
const sqliteDisponible = await import('node:sqlite').then(() => true, () => false)
if (!sqliteDisponible) {
  console.warn(
    `\n⚠️  tests/unit/db.test.js omitido: este Node (${process.version}) no expone node:sqlite.\n` +
    '   La app no está afectada (Electron sí lo trae). Para ejecutarlos, usa Node >= 22.5.\n'
  )
}
const db = sqliteDisponible ? await import('../../db.js') : null

// ── Fixtures ─────────────────────────────────────────────────────────────────
const MODULO_FIXTURE = {
  key:    'MOD_TEST_001',
  abrev:  'TST',
  nombre: 'Módulo de Test',
  ciclo:  'CFGM Test',
  curso:  '1',
  anno:   '2024-25',
  grupo:  'Grupo A',
  horas:  120,
  decreto: null,
  actividades: [],
  data: { modulo: { eval_count: 3 }, uts: [], ras: [], ces: [], asignaciones: [], eval_ras: {}, ra_instrumentos: {} },
}

const ALUMNO_FIXTURE = (mid) => ({
  modulo_id:     mid,
  num:           1,
  apellidos:     'García',
  nombre:        'Ana',
  nia:           '12345678A',
  email:         'ana@test.es',
  estado:        'Activo',
  telefono:      '',
  observaciones: '',
  fecha_nacim:   null,
})

// ── Limpieza ──────────────────────────────────────────────────────────────────
afterEach(() => {
  // closeDb() cierra la conexión y resetea _db=null en el singleton.
  // Así cada test empieza con una DB limpia (nueva conexión, fichero vacío).
  try {
    db.closeDb()
    const dbDir  = path.join(os.tmpdir(), `evalfp-test-${process.pid}`)
    const dbFile = path.join(dbDir, 'evalfp.db')
    if (fs.existsSync(dbFile)) fs.unlinkSync(dbFile)
  } catch {
    // Limpieza best-effort: si la base ya se cerró o el fichero no existe, seguimos.
  }
})

// ── Tests: Módulos ─────────────────────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Módulos', () => {
  it('addModulo() inserta y devuelve un ID positivo', () => {
    const id = db.addModulo(MODULO_FIXTURE)
    expect(id).toBeTypeOf('number')
    expect(id).toBeGreaterThan(0)
  })

  it('getModulos() devuelve array con el módulo insertado', () => {
    db.addModulo(MODULO_FIXTURE)
    const modulos = db.getModulos()
    expect(Array.isArray(modulos)).toBe(true)
    expect(modulos.length).toBeGreaterThanOrEqual(1)
    expect(modulos[0].abrev).toBe('TST')
  })

  it('getModulos() no devuelve módulos eliminados', () => {
    const id = db.addModulo(MODULO_FIXTURE)
    db.deleteModulo(id)
    const modulos = db.getModulos()
    expect(modulos.find(m => m.id === id)).toBeUndefined()
  })

  it('addModulo() con key duplicada lanza error (UNIQUE constraint)', () => {
    db.addModulo(MODULO_FIXTURE)
    expect(() => db.addModulo(MODULO_FIXTURE)).toThrow()
  })
})

// ── Tests: Alumnos ─────────────────────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Alumnos', () => {
  let mid

  beforeEach(() => {
    mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_ALU_${Date.now()}` })
  })

  it('saveAlumno() inserta alumno nuevo y devuelve ID', () => {
    const id = db.saveAlumno(ALUMNO_FIXTURE(mid))
    expect(id).toBeTypeOf('number')
    expect(id).toBeGreaterThan(0)
  })

  it('getAlumnos() devuelve los alumnos del módulo', () => {
    db.saveAlumno(ALUMNO_FIXTURE(mid))
    const alumnos = db.getAlumnos(mid)
    expect(alumnos.length).toBe(1)
    expect(alumnos[0].apellidos).toBe('García')
    expect(alumnos[0].nombre).toBe('Ana')
  })

  it('saveAlumno() actualiza alumno existente (UPDATE)', () => {
    const id = db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.saveAlumno({ id, modulo_id: mid, apellidos: 'López', nombre: 'Ana', estado: 'Activo' })
    const alumnos = db.getAlumnos(mid)
    expect(alumnos[0].apellidos).toBe('López')
  })

  it('deleteAlumno() elimina el alumno', () => {
    const id = db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.deleteAlumno(id)
    expect(db.getAlumnos(mid).length).toBe(0)
  })

  it('getAlumnos() no mezcla alumnos de módulos distintos', () => {
    const mid2 = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_ALU2_${Date.now()}` })
    db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.saveAlumno({ ...ALUMNO_FIXTURE(mid2), apellidos: 'Otro' })
    expect(db.getAlumnos(mid).length).toBe(1)
    expect(db.getAlumnos(mid2).length).toBe(1)
  })
})

// ── Tests: Notas ───────────────────────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Notas', () => {
  let mid, alumnoId, actividadId

  beforeEach(() => {
    mid        = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_NTD_${Date.now()}` })
    alumnoId   = db.saveAlumno(ALUMNO_FIXTURE(mid))
    actividadId = db.saveActividad({
      modulo_id:   mid,
      ut_id:       'UT1',
      ra_id:       'RA1',
      descripcion: 'Examen parcial',
      instrumento: 'Examen',
      tipo:        'examen',
      peso:        40,
      nota_max:    10,
      eval:        1,
      orden:       0,
    })
  })

  it('saveNota() guarda nota válida (0-10)', () => {
    db.saveNota(alumnoId, actividadId, 7.5)
    const notas = db.getNotasGrid(mid)
    expect(notas.length).toBe(1)
    expect(notas[0].nota).toBe(7.5)
  })

  it('saveNota() acepta nota 0', () => {
    db.saveNota(alumnoId, actividadId, 0)
    const notas = db.getNotasGrid(mid)
    expect(notas[0].nota).toBe(0)
  })

  it('saveNota() acepta nota 10', () => {
    db.saveNota(alumnoId, actividadId, 10)
    const notas = db.getNotasGrid(mid)
    expect(notas[0].nota).toBe(10)
  })

  it('saveNota() acepta null (borrar nota)', () => {
    db.saveNota(alumnoId, actividadId, 7)
    db.saveNota(alumnoId, actividadId, null)
    const notas = db.getNotasGrid(mid)
    expect(notas[0].nota).toBeNull()
  })

  it('saveNota() hace UPSERT (actualiza si ya existe)', () => {
    db.saveNota(alumnoId, actividadId, 5)
    db.saveNota(alumnoId, actividadId, 9)
    const notas = db.getNotasGrid(mid)
    expect(notas.length).toBe(1)
    expect(notas[0].nota).toBe(9)
  })

  // H6 — recuperación con trazabilidad (nota_rec)
  it('saveNotaRec() guarda la recuperación SIN tocar la nota original', () => {
    db.saveNota(alumnoId, actividadId, 3)
    db.saveNotaRec(alumnoId, actividadId, 6.5)
    const n = db.getNotasGrid(mid)[0]
    expect(n.nota).toBe(3)
    expect(n.nota_rec).toBe(6.5)
  })

  it('saveNotaRec() con null borra la recuperación y conserva la original', () => {
    db.saveNota(alumnoId, actividadId, 4)
    db.saveNotaRec(alumnoId, actividadId, 7)
    db.saveNotaRec(alumnoId, actividadId, null)
    const n = db.getNotasGrid(mid)[0]
    expect(n.nota).toBe(4)
    expect(n.nota_rec).toBeNull()
  })

  it('saveNotaRec() sobre actividad sin nota crea fila con nota original NULL', () => {
    db.saveNotaRec(alumnoId, actividadId, 5.5)
    const n = db.getNotasGrid(mid)[0]
    expect(n.nota).toBeNull()
    expect(n.nota_rec).toBe(5.5)
  })
})

// ── Tests: Config ──────────────────────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Config', () => {
  it('setConfig/getConfig guarda y recupera valor', () => {
    db.setConfig('testKey', 'testValue')
    expect(db.getConfig('testKey')).toBe('testValue')
  })

  it('getAllConfig devuelve objeto con todas las claves', () => {
    db.setConfig('k1', 'v1')
    db.setConfig('k2', 'v2')
    const cfg = db.getAllConfig()
    expect(cfg.k1).toBe('v1')
    expect(cfg.k2).toBe('v2')
  })

  it('setConfig sobreescribe valor existente', () => {
    db.setConfig('overwrite', 'original')
    db.setConfig('overwrite', 'updated')
    expect(db.getConfig('overwrite')).toBe('updated')
  })

  it('getConfig devuelve null para clave inexistente', () => {
    expect(db.getConfig('no_existe_esta_clave')).toBeNull()
  })

  it('deleteConfig elimina una clave de configuración', () => {
    db.setConfig('temporal', 'valor')
    db.deleteConfig('temporal')
    expect(db.getConfig('temporal')).toBeNull()
  })
})

// ── Tests: Integridad referencial ──────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Integridad referencial (CASCADE)', () => {
  // Quitar un módulo lo ARCHIVA: un curso calificado es un documento de
  // evaluación y no debe perderse con un clic. El borrado real sigue estando,
  // pero hay que pedirlo expresamente.
  it('quitar un módulo lo archiva y conserva su alumnado', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_ARCH_${Date.now()}` })
    db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.deleteModulo(mid)

    expect(db.getModulos().some(m => m.id === mid)).toBe(false)          // fuera de la lista
    expect(db.getModulosArchivados().some(m => m.id === mid)).toBe(true) // pero recuperable
    expect(db.getAlumnos(mid).length).toBe(1)                            // sin perder nada
  })

  it('recuperar un módulo archivado lo devuelve al cuaderno', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_REST_${Date.now()}` })
    db.deleteModulo(mid)
    db.restaurarModulo(mid)
    expect(db.getModulos().some(m => m.id === mid)).toBe(true)
    expect(db.getModulosArchivados().some(m => m.id === mid)).toBe(false)
  })

  it('el borrado definitivo sí arrastra a sus alumnos en cascada', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_CAS_${Date.now()}` })
    db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.deleteModulo(mid, { definitivo: true })
    expect(db.getAlumnos(mid).length).toBe(0)
    expect(db.getModulosArchivados().some(m => m.id === mid)).toBe(false)
  })
})

// ── Tests: convocatorias (A-5) ────────────────────────────────────────────────
describe.skipIf(!sqliteDisponible)('Convocatoria de las actividades', () => {
  it('una actividad nace en la 1ª convocatoria si no se dice otra cosa', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_CV1_${Date.now()}` })
    const id = db.saveActividad({
      modulo_id: mid, ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Práctica',
      instrumento: 'Práctica', tipo: 'practica', peso: 50, nota_max: 10, eval: 1, orden: 0,
    })
    const act = db.getActividades(mid).find(a => a.id === id)
    expect(act.convocatoria).toBe(1)
  })

  it('guarda y devuelve las actividades de recuperación de la 2ª', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_CV2_${Date.now()}` })
    db.saveActividad({
      modulo_id: mid, ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Examen de curso',
      instrumento: 'Examen', tipo: 'examen', peso: 100, nota_max: 10, eval: 1, orden: 0,
    })
    db.saveActividad({
      modulo_id: mid, ut_id: null, ra_id: null, descripcion: 'Prueba de recuperación',
      instrumento: 'Examen', tipo: 'examen', peso: 0, nota_max: 10, eval: 1, orden: 1,
      convocatoria: 2,
    })

    expect(db.getActividades(mid).length).toBe(2)              // sin filtro, las dos
    expect(db.getActividades(mid, 1).length).toBe(1)           // la del curso
    const rec = db.getActividades(mid, 2)
    expect(rec.length).toBe(1)
    expect(rec[0].descripcion).toBe('Prueba de recuperación')
  })

  it('editar una actividad no la cambia de convocatoria sin querer', () => {
    // Todas las pantallas antiguas guardan sin mandar `convocatoria`. Si eso
    // devolviera la prueba de junio a la 1ª convocatoria, su nota entraría en un
    // acta ya cerrada.
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_CV3_${Date.now()}` })
    const id = db.saveActividad({
      modulo_id: mid, ut_id: null, ra_id: null, descripcion: 'Recuperación',
      instrumento: 'Examen', tipo: 'examen', peso: 0, nota_max: 10, eval: 1, orden: 0,
      convocatoria: 2,
    })
    const act = db.getActividades(mid).find(a => a.id === id)
    db.saveActividad({ ...act, convocatoria: undefined, descripcion: 'Recuperación (junio)' })

    const despues = db.getActividades(mid).find(a => a.id === id)
    expect(despues.descripcion).toBe('Recuperación (junio)')
    expect(despues.convocatoria).toBe(2)
  })
})

// ── Tests: actividades de partida (V-2 y V-3 de la auditoría en vivo) ─────────
describe.skipIf(!sqliteDisponible)('Actividades de partida de un módulo nuevo', () => {
  it('addModulo guarda los criterios de cada actividad', () => {
    // Sin esto, el módulo llegaba al cuaderno con actividades que no evaluaban
    // ningún criterio: se calificaban y no movían la nota de ningún RA.
    const mid = db.addModulo({
      ...MODULO_FIXTURE, key: `MOD_CES_${Date.now()}`,
      actividades: [{
        ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Examen EV1', instrumento: 'Examen',
        tipo: 'examen', peso: 70, nota_max: 10, eval: 1, orden: 1,
        ces: ['RA1|CR1', 'RA1|CR2'],
      }],
    })
    const act = db.getActividades(mid)[0]
    expect(JSON.parse(act.ces)).toEqual(['RA1|CR1', 'RA1|CR2'])
  })
})

// ── Tests: el mismo módulo para dos grupos (V-1 de la auditoría en vivo) ──────
describe.skipIf(!sqliteDisponible)('Un módulo, varios grupos', () => {
  it('admite el mismo módulo dos veces si el grupo cambia', () => {
    const key = `MOD_GRP_${Date.now()}`
    const a = db.addModulo({ ...MODULO_FIXTURE, key, grupo: '2ºA' })
    const b = db.addModulo({ ...MODULO_FIXTURE, key, grupo: '2ºB' })
    expect(b).not.toBe(a)
    const suyos = db.getModulos().filter(m => m.key === key)
    expect(suyos.map(m => m.grupo).sort()).toEqual(['2ºA', '2ºB'])
  })

  it('rechaza el duplicado exacto de módulo y grupo', () => {
    const key = `MOD_DUP_${Date.now()}`
    db.addModulo({ ...MODULO_FIXTURE, key, grupo: '1ºC' })
    expect(() => db.addModulo({ ...MODULO_FIXTURE, key, grupo: '1ºC' })).toThrow()
  })

  it('el alumnado de cada grupo no se mezcla', () => {
    const key = `MOD_SEP_${Date.now()}`
    const a = db.addModulo({ ...MODULO_FIXTURE, key, grupo: 'A' })
    const b = db.addModulo({ ...MODULO_FIXTURE, key, grupo: 'B' })
    db.saveAlumno({ ...ALUMNO_FIXTURE(a), apellidos: 'De grupo A' })
    expect(db.getAlumnos(a).length).toBe(1)
    expect(db.getAlumnos(b).length).toBe(0)
  })
})

// ── Tests: fichero heredado que no es SQLite ──────────────────────────────────
describe.skipIf(!sqliteDisponible)('Base de datos de una versión muy anterior', () => {
  it('aparta el fichero JSON en vez de dejar la aplicación muerta', () => {
    // Una versión intermedia guardaba `evalfp.db` como JSON. `DatabaseSync`
    // sobre ese fichero lanza «file is not a database» y la app no arranca.
    // La reimportación ya no se mantiene, pero el fichero no puede perderse ni
    // el arranque puede caerse sin explicación.
    const dir    = path.join(os.tmpdir(), `evalfp-test-${process.pid}`)
    const dbPath = path.join(dir, 'evalfp.db')

    db.closeDb()
    const copia = fs.existsSync(dbPath) ? fs.readFileSync(dbPath) : null
    fs.writeFileSync(dbPath, JSON.stringify({ modulos: [], alumnos: [], notas: [] }))

    expect(() => db.getModulos()).not.toThrow()

    const apartados = fs.readdirSync(dir).filter(f => f.startsWith('evalfp-json-legacy-'))
    expect(apartados.length, 'el fichero heredado tiene que conservarse').toBeGreaterThan(0)
    const guardado = JSON.parse(fs.readFileSync(path.join(dir, apartados[0]), 'utf8'))
    expect(guardado).toHaveProperty('modulos')

    // Devolver la base de test a su sitio para el resto de la suite
    db.closeDb()
    apartados.forEach(f => fs.unlinkSync(path.join(dir, f)))
    if (copia) fs.writeFileSync(dbPath, copia)
  })
})

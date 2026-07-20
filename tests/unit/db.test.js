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
const db = await import('../../db.js')

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
describe('Módulos', () => {
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
describe('Alumnos', () => {
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
describe('Notas', () => {
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
describe('Config', () => {
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
describe('Integridad referencial (CASCADE)', () => {
  it('eliminar módulo borra también sus alumnos en cascada', () => {
    const mid = db.addModulo({ ...MODULO_FIXTURE, key: `MOD_CAS_${Date.now()}` })
    db.saveAlumno(ALUMNO_FIXTURE(mid))
    db.deleteModulo(mid)
    // getAlumnos de un módulo eliminado debe devolver array vacío
    expect(db.getAlumnos(mid).length).toBe(0)
  })
})

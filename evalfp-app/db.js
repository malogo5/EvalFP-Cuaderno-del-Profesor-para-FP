/**
 * db.js — Capa de base de datos SQLite (better-sqlite3)
 * EvalFP App — Cuaderno del Profesor independiente de Excel
 */
'use strict'

const Database = require('better-sqlite3')
const path  = require('path')
const { app } = require('electron')

let _db = null

function getDb() {
  if (_db) return _db
  const dbPath = path.join(app.getPath('userData'), 'evalfp.db')
  _db = new Database(dbPath)
  _db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;')
  _initSchema()
  _runMigrations()
  return _db
}

// ── Migraciones / limpiezas puntuales ────────────────────────────────────────
function _runMigrations() {
  // 2026-07-08: borrar actividad residual 108 (RA8 eval=1 "Examen — Evaluación 1")
  //             y sus notas — fue creada por error, los datos reales de RA8 están en act.98 (eval=3)
  const residual = _db.prepare('SELECT id FROM actividades WHERE id = 108').get()
  if (residual) {
    _db.prepare('DELETE FROM notas WHERE actividad_id = 108').run()
    _db.prepare('DELETE FROM actividades WHERE id = 108').run()
    console.log('[migration] Actividad residual 108 (RA8/eval1) eliminada.')
  }
}

function _initSchema() {
  _db.exec(`
    -- Módulos que el profesor imparte
    -- Los datos normativos (RAs, CEs) vienen del DOCM Castilla-La Mancha
    CREATE TABLE IF NOT EXISTS modulos (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      key        TEXT NOT NULL UNIQUE,
      abrev      TEXT NOT NULL,
      nombre     TEXT NOT NULL,
      ciclo      TEXT,
      curso      TEXT,
      anno       TEXT,
      grupo      TEXT DEFAULT 'Grupo A',
      horas      INTEGER DEFAULT 0,
      decreto    TEXT,
      data_json  TEXT,
      activo     INTEGER DEFAULT 1,
      created_at TEXT DEFAULT (datetime('now'))
    );

    -- Alumnos por módulo
    CREATE TABLE IF NOT EXISTS alumnos (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      modulo_id   INTEGER NOT NULL,
      num         INTEGER,
      apellidos   TEXT,
      nombre      TEXT,
      nia         TEXT,
      fecha_nacim TEXT,
      email       TEXT,
      telefono    TEXT,
      estado      TEXT DEFAULT 'Activo',
      observaciones TEXT,
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- Actividades de evaluación (instrumentos)
    CREATE TABLE IF NOT EXISTS actividades (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      modulo_id   INTEGER NOT NULL,
      ut_id       TEXT,
      ra_id       TEXT,
      descripcion TEXT,
      instrumento TEXT,
      tipo        TEXT,
      peso        REAL DEFAULT 0,
      nota_max    REAL DEFAULT 10,
      eval        INTEGER DEFAULT 1,
      orden       INTEGER DEFAULT 0,
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- Notas: una por alumno × actividad
    CREATE TABLE IF NOT EXISTS notas (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      alumno_id    INTEGER NOT NULL,
      actividad_id INTEGER NOT NULL,
      nota         REAL,
      fecha        TEXT DEFAULT (date('now')),
      observaciones TEXT,
      UNIQUE (alumno_id, actividad_id),
      FOREIGN KEY (alumno_id)    REFERENCES alumnos(id)    ON DELETE CASCADE,
      FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE
    );

    -- Configuración general
    CREATE TABLE IF NOT EXISTS config (
      key   TEXT PRIMARY KEY,
      value TEXT
    );

    -- Ponderaciones de RAs por módulo (override del valor por defecto del JSON)
    CREATE TABLE IF NOT EXISTS ra_ponderaciones (
      modulo_id  INTEGER NOT NULL,
      ra_id      TEXT    NOT NULL,
      pond       REAL    NOT NULL,
      PRIMARY KEY (modulo_id, ra_id),
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- Tabla legacy de configuración de claves (fallback cuando keytar no está disponible)
    -- Las claves se almacenan aquí solo si keytar falla. En uso normal se gestionan
    -- con keytar (almacenamiento seguro del SO).
    CREATE TABLE IF NOT EXISTS cfg (
      openaiKey    TEXT DEFAULT '',
      anthropicKey TEXT DEFAULT ''
    );
    -- Insertar fila única si no existe
    INSERT OR IGNORE INTO cfg (openaiKey, anthropicKey) VALUES ('', '');
  `)

  // Migración: añadir columna ces si no existe (actividades → criterios de evaluación)
  try { _db.exec(`ALTER TABLE actividades ADD COLUMN ces TEXT DEFAULT '[]'`) } catch { /* columna ya existe */ }

  // Migración 2026-07: nota de recuperación por actividad (trazabilidad H6).
  // La nota original se conserva en `nota`; la de recuperación en `nota_rec`.
  // La nota efectiva para el cálculo es COALESCE(nota_rec, nota).
  try { _db.exec(`ALTER TABLE notas ADD COLUMN nota_rec REAL`) } catch { /* columna ya existe */ }
}

// ── Módulos ────────────────────────────────────────────────────────────────────
const getModulos = () =>
  getDb().prepare('SELECT * FROM modulos WHERE activo=1 ORDER BY abrev').all()

function addModulo({ key, abrev, nombre, ciclo, curso, anno, grupo, horas, decreto, actividades, data }) {
  const db = getDb()
  const r = db.prepare(`
    INSERT INTO modulos (key,abrev,nombre,ciclo,curso,anno,grupo,horas,decreto,data_json)
    VALUES (?,?,?,?,?,?,?,?,?,?)
  `).run(key, abrev, nombre, ciclo, curso, anno, grupo, horas, decreto || null, JSON.stringify(data))

  const mid = Number(r.lastInsertRowid)
  if (actividades?.length) {
    const s = db.prepare(`
      INSERT INTO actividades (modulo_id,ut_id,ra_id,descripcion,instrumento,tipo,peso,nota_max,eval,orden)
      VALUES (?,?,?,?,?,?,?,?,?,?)
    `)
    actividades.forEach(a =>
      s.run(mid, a.ut_id||null, a.ra_id||null, a.descripcion, a.instrumento,
            a.tipo, a.peso, a.nota_max, a.eval, a.orden))
  }
  return mid
}

const deleteModulo = id => getDb().prepare('DELETE FROM modulos WHERE id=?').run(id)

// ── Alumnos ────────────────────────────────────────────────────────────────────
const getAlumnos = moduloId =>
  getDb().prepare('SELECT * FROM alumnos WHERE modulo_id=? ORDER BY num,apellidos').all(moduloId)

function saveAlumno(a) {
  const db = getDb()
  // Convierte a null todo lo que SQLite no puede bindear (undefined, '', NaN, Infinity,
  // booleanos, objetos…). better-sqlite3 solo acepta: null, integer, real, text, buffer.
  const n = v => {
    if (v === undefined || v === null || v === '') return null
    if (typeof v === 'number') return isFinite(v) ? v : null
    if (typeof v === 'string') return v
    return null  // rechaza boolean, object, array, symbol, etc.
  }
  if (a.id) {
    db.prepare(`UPDATE alumnos SET num=?,apellidos=?,nombre=?,nia=?,fecha_nacim=?,
      email=?,telefono=?,estado=?,observaciones=? WHERE id=?`)
      .run(
        n(a.num),
        n(a.apellidos),
        n(a.nombre),
        n(a.nia),
        n(a.fecha_nacim),
        n(a.email),
        n(a.telefono),
        a.estado || 'Activo',
        n(a.observaciones),
        a.id
      )
    return a.id
  }
  return Number(db.prepare(`INSERT INTO alumnos
    (modulo_id,num,apellidos,nombre,nia,fecha_nacim,email,telefono,estado,observaciones)
    VALUES (?,?,?,?,?,?,?,?,?,?)`)
    .run(a.modulo_id, a.num||null, n(a.apellidos), n(a.nombre), n(a.nia), n(a.fecha_nacim),
         n(a.email), n(a.telefono), a.estado||'Activo', n(a.observaciones)).lastInsertRowid)
}

const deleteAlumno = id => getDb().prepare('DELETE FROM alumnos WHERE id=?').run(id)

// ── Actividades ────────────────────────────────────────────────────────────────
const getActividades = moduloId =>
  getDb().prepare('SELECT * FROM actividades WHERE modulo_id=? ORDER BY eval,orden').all(moduloId)

function saveActividad(a) {
  const db = getDb()
  const cesJson = Array.isArray(a.ces) ? JSON.stringify(a.ces) : (a.ces ?? '[]')
  if (a.id) {
    db.prepare(`UPDATE actividades SET descripcion=?,peso=?,nota_max=?,eval=?,ut_id=?,ra_id=?,ces=?,orden=? WHERE id=?`)
      .run(a.descripcion, a.peso, a.nota_max, a.eval??1, a.ut_id??null, a.ra_id??null, cesJson, a.orden??0, a.id)
    return a.id
  }
  return Number(db.prepare(`INSERT INTO actividades
    (modulo_id,ut_id,ra_id,descripcion,instrumento,tipo,peso,nota_max,eval,orden,ces)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)`)
    .run(a.modulo_id,a.ut_id,a.ra_id,a.descripcion,a.instrumento,
         a.tipo,a.peso,a.nota_max,a.eval,a.orden,cesJson).lastInsertRowid)
}

// ── Notas ──────────────────────────────────────────────────────────────────────
function getNotasGrid(moduloId) {
  return getDb().prepare(`
    SELECT n.alumno_id, n.actividad_id, n.nota, n.nota_rec
    FROM notas n
    JOIN alumnos al ON n.alumno_id = al.id
    WHERE al.modulo_id = ?
  `).all(moduloId)
}

function saveNota(alumnoId, actividadId, nota) {
  const val = nota === '' || nota === null ? null : parseFloat(nota)
  getDb().prepare(`
    INSERT INTO notas (alumno_id, actividad_id, nota)
    VALUES (?,?,?)
    ON CONFLICT (alumno_id, actividad_id)
    DO UPDATE SET nota=excluded.nota, fecha=date('now')
  `).run(alumnoId, actividadId, val)
}

/**
 * Guarda la nota de RECUPERACIÓN de una actividad sin sobrescribir la original.
 * null/'' borra la recuperación (vuelve a valer la nota original).
 */
function saveNotaRec(alumnoId, actividadId, nota) {
  const val = nota === '' || nota === null ? null : parseFloat(nota)
  getDb().prepare(`
    INSERT INTO notas (alumno_id, actividad_id, nota, nota_rec)
    VALUES (?,?,NULL,?)
    ON CONFLICT (alumno_id, actividad_id)
    DO UPDATE SET nota_rec=excluded.nota_rec, fecha=date('now')
  `).run(alumnoId, actividadId, val)
}

// ── Ponderaciones de RAs ───────────────────────────────────────────────────────
const getRaPonderaciones = moduloId =>
  getDb().prepare('SELECT ra_id, pond FROM ra_ponderaciones WHERE modulo_id=?').all(moduloId)

function setRaPonderacion(moduloId, raId, pond) {
  getDb().prepare(`
    INSERT INTO ra_ponderaciones (modulo_id, ra_id, pond) VALUES (?,?,?)
    ON CONFLICT (modulo_id, ra_id) DO UPDATE SET pond=excluded.pond
  `).run(moduloId, raId, pond)
}

// ── Modulo data_json (edición UT/RA/CE) ───────────────────────────────────────
function setModuloDataJson(id, dataJson) {
  getDb().prepare('UPDATE modulos SET data_json=? WHERE id=?').run(JSON.stringify(dataJson), id)
}

const deleteActividad = id => getDb().prepare('DELETE FROM actividades WHERE id=?').run(id)

// ── Config ─────────────────────────────────────────────────────────────────────
const getConfig  = key  => getDb().prepare('SELECT value FROM config WHERE key=?').get(key)?.value ?? null
const setConfig  = (k,v) => getDb().prepare('INSERT OR REPLACE INTO config VALUES(?,?)').run(k,v)
const getAllConfig = ()  => Object.fromEntries(getDb().prepare('SELECT key,value FROM config').all().map(r=>[r.key,r.value]))

// ── Tabla cfg (API keys — fallback cuando keytar no está disponible) ────────────
// main.js debe usar estas funciones en lugar de abrir una conexión raw a otra ruta.
const getCfgKeys = () => getDb().prepare('SELECT openaiKey, anthropicKey FROM cfg LIMIT 1').get()
function setCfgKey(field, value) {
  if (field !== 'openaiKey' && field !== 'anthropicKey') throw new Error('setCfgKey: campo inválido')
  // Usar interpolación controlada: field solo puede ser uno de los dos valores arriba
  getDb().prepare(`UPDATE cfg SET ${field} = ?`).run(value)
}

function closeDb() {
  if (_db) { _db.close(); _db = null }
}

/**
 * Copia online y segura de la DB usando la API nativa de better-sqlite3.
 * A diferencia de fs.copyFileSync, funciona correctamente con WAL mode activo
 * y transacciones en vuelo. Devuelve una Promise.
 * @param {string} destPath — ruta completa del fichero de backup
 */
function backup(destPath) {
  return getDb().backup(destPath)
}

module.exports = {
  getModulos, addModulo, deleteModulo, setModuloDataJson,
  getAlumnos, saveAlumno, deleteAlumno,
  getActividades, saveActividad, deleteActividad,
  getNotasGrid, saveNota, saveNotaRec,
  getRaPonderaciones, setRaPonderacion,
  getConfig, setConfig, getAllConfig,
  getCfgKeys, setCfgKey,
  closeDb, backup,
}

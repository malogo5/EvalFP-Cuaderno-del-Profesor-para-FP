/**
 * db.js — Capa de base de datos SQLite (node:sqlite, Node 22+)
 * EvalFP App — Cuaderno del Profesor independiente de Excel
 */
'use strict'

const { DatabaseSync } = require('node:sqlite')
const fs    = require('fs')
const path  = require('path')
const { app } = require('electron')

let _db = null

/**
 * Una versión intermedia de EvalFP guardó los datos como JSON en el fichero
 * `evalfp.db` (backend sin SQLite). Al volver a SQLite, `new DatabaseSync()`
 * sobre ese fichero falla con «file is not a database» y la app no arranca.
 *
 * Esta función detecta ese caso: si el fichero existe y NO empieza por la
 * cabecera «SQLite format 3», lo aparta con nombre `evalfp-json-legacy-*.json`
 * (nunca lo borra) y devuelve su contenido para reimportarlo.
 * Devuelve null si no hay nada que migrar.
 */
function _apartarJsonLegacy(dbPath) {
  if (!fs.existsSync(dbPath)) return null
  let cabecera = ''
  try {
    const fd = fs.openSync(dbPath, 'r')
    const buf = Buffer.alloc(16)
    fs.readSync(fd, buf, 0, 16, 0)
    fs.closeSync(fd)
    cabecera = buf.toString('utf8')
  } catch { return null }
  if (cabecera.startsWith('SQLite format 3')) return null   // BD SQLite correcta

  // No es SQLite: apartar el fichero y intentar leerlo como JSON
  const respaldo = path.join(
    path.dirname(dbPath),
    `evalfp-json-legacy-${new Date().toISOString().replace(/[:.]/g, '-')}.json`
  )
  let datos = null
  try { datos = JSON.parse(fs.readFileSync(dbPath, 'utf8')) } catch { datos = null }
  try { fs.renameSync(dbPath, respaldo) } catch { return null }
  // Limpiar posibles ficheros WAL/SHM huérfanos del intento anterior
  for (const ext of ['-wal', '-shm']) {
    try { fs.unlinkSync(dbPath + ext) } catch { /* no existen */ }
  }
  console.log(`[db] Fichero no-SQLite apartado en ${path.basename(respaldo)}` +
              (datos ? ' · se reimportarán sus datos' : ' · no se pudo leer como JSON'))
  return datos
}

/** Reimporta a SQLite los datos del backend JSON legacy. */
function _importarJsonLegacy(d) {
  if (!d || typeof d !== 'object') return
  const n = v => (v === undefined ? null : v)
  const tx = () => {
    for (const m of d.modulos || []) {
      _db.prepare(`INSERT OR IGNORE INTO modulos
        (id,key,abrev,nombre,ciclo,curso,anno,grupo,horas,decreto,data_json,activo)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`)
        .run(n(m.id), n(m.key), n(m.abrev), n(m.nombre), n(m.ciclo), n(m.curso), n(m.anno),
             n(m.grupo) ?? 'Grupo A', n(m.horas) ?? 0, n(m.decreto),
             typeof m.data_json === 'string' ? m.data_json : JSON.stringify(m.data_json ?? null),
             n(m.activo) ?? 1)
    }
    for (const a of d.alumnos || []) {
      _db.prepare(`INSERT OR IGNORE INTO alumnos
        (id,modulo_id,num,apellidos,nombre,nia,fecha_nacim,email,telefono,estado,observaciones)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)`)
        .run(n(a.id), n(a.modulo_id), n(a.num), n(a.apellidos), n(a.nombre), n(a.nia),
             n(a.fecha_nacim), n(a.email), n(a.telefono), n(a.estado) ?? 'Activo', n(a.observaciones))
    }
    for (const a of d.actividades || []) {
      _db.prepare(`INSERT OR IGNORE INTO actividades
        (id,modulo_id,ut_id,ra_id,descripcion,instrumento,tipo,peso,nota_max,eval,orden,ces)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`)
        .run(n(a.id), n(a.modulo_id), n(a.ut_id), n(a.ra_id), n(a.descripcion), n(a.instrumento),
             n(a.tipo), n(a.peso) ?? 0, n(a.nota_max) ?? 10, n(a.eval) ?? 1, n(a.orden) ?? 0,
             typeof a.ces === 'string' ? a.ces : JSON.stringify(a.ces ?? []))
    }
    for (const nt of d.notas || []) {
      _db.prepare(`INSERT OR IGNORE INTO notas
        (id,alumno_id,actividad_id,nota,fecha,observaciones,nota_rec)
        VALUES (?,?,?,?,?,?,?)`)
        .run(n(nt.id), n(nt.alumno_id), n(nt.actividad_id), n(nt.nota), n(nt.fecha),
             n(nt.observaciones), n(nt.nota_rec))
    }
    for (const r of d.ra_ponderaciones || []) {
      _db.prepare('INSERT OR IGNORE INTO ra_ponderaciones (modulo_id,ra_id,pond) VALUES (?,?,?)')
        .run(n(r.modulo_id), n(r.ra_id), n(r.pond))
    }
    for (const [k, v] of Object.entries(d.config || {})) {
      _db.prepare('INSERT OR REPLACE INTO config (key,value) VALUES (?,?)').run(k, String(v))
    }
  }
  try {
    _db.exec('BEGIN'); tx(); _db.exec('COMMIT')
    console.log(`[db] Datos legacy reimportados: ${(d.modulos||[]).length} módulos · ` +
                `${(d.alumnos||[]).length} alumnos · ${(d.notas||[]).length} notas`)
  } catch (e) {
    try { _db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    console.error('[db] No se pudieron reimportar los datos legacy:', e.message)
  }
}

function getDb() {
  if (_db) return _db
  const dbPath = path.join(app.getPath('userData'), 'evalfp.db')
  const legacy = _apartarJsonLegacy(dbPath)
  _db = new DatabaseSync(dbPath)
  _db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;')
  _initSchema()

  // Migración: añade nota_rec a bases de datos creadas antes de esta versión
  const cols = _db.prepare("PRAGMA table_info(notas)").all()
  if (!cols.some(c => c.name === 'nota_rec')) {
    _db.exec('ALTER TABLE notas ADD COLUMN nota_rec REAL')
  }

  // Migración: columna `ces` de actividades (criterios de evaluación cubiertos).
  // El renderer la usa para calcular la nota de cada CE; sin ella el motor cae
  // al cálculo por RA y se pierde el detalle por criterio.
  const colsAct = _db.prepare("PRAGMA table_info(actividades)").all()
  if (!colsAct.some(c => c.name === 'ces')) {
    _db.exec(`ALTER TABLE actividades ADD COLUMN ces TEXT DEFAULT '[]'`)
  }

  if (legacy) _importarJsonLegacy(legacy)

  return _db
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
      nota_rec     REAL,
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
  `)
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
  const n = v => (v === undefined || v === '') ? null : v
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
  // `ces` llega como array desde el modal de criterios; se persiste como JSON
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

// Nota de recuperación: se guarda aparte de la nota original, sin sobreescribirla.
// Si la actividad todavía no tiene fila en `notas`, se crea con nota=NULL.
function saveNotaRec(alumnoId, actividadId, notaRec) {
  const val = notaRec === '' || notaRec === null ? null : parseFloat(notaRec)
  getDb().prepare(`
    INSERT INTO notas (alumno_id, actividad_id, nota_rec)
    VALUES (?,?,?)
    ON CONFLICT (alumno_id, actividad_id)
    DO UPDATE SET nota_rec=excluded.nota_rec, fecha=date('now')
  `).run(alumnoId, actividadId, val)
}

// Cierra la conexión activa y resetea el singleton — necesario para que los
// tests puedan aislar cada caso con una base de datos limpia.
function closeDb() {
  if (_db) {
    _db.close()
    _db = null
  }
}

// Crea una copia consistente incluso cuando la base está en modo WAL.
// VACUUM INTO trabaja sobre un snapshot de SQLite, a diferencia de copiar el
// archivo `.db` mientras puede haber escrituras pendientes en el archivo WAL.
function backupTo(destPath) {
  const escapedPath = String(destPath).replace(/'/g, "''")
  getDb().exec(`VACUUM INTO '${escapedPath}'`)
  return destPath
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
const deleteConfig = key => getDb().prepare('DELETE FROM config WHERE key=?').run(key)
const getAllConfig = ()  => Object.fromEntries(getDb().prepare('SELECT key,value FROM config').all().map(r=>[r.key,r.value]))

module.exports = {
  getModulos, addModulo, deleteModulo, setModuloDataJson,
  getAlumnos, saveAlumno, deleteAlumno,
  getActividades, saveActividad, deleteActividad,
  getNotasGrid, saveNota, saveNotaRec, closeDb, backupTo,
  getRaPonderaciones, setRaPonderacion,
  getConfig, setConfig, deleteConfig, getAllConfig,
}

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

  // Notas fuera de escala que hubiera dejado alguna versión anterior: la
  // validación estaba solo en la interfaz y por IPC se podía colar un 99.
  const fuera = _db.prepare(
    'SELECT COUNT(*) AS n FROM notas WHERE nota < 0 OR nota > 10 OR nota_rec < 0 OR nota_rec > 10').get()
  if (fuera && fuera.n > 0) {
    console.warn(`[db] ${fuera.n} nota(s) fuera del rango 0-10; se dejan como están para no perder datos.`)
  }

  if (legacy) _importarJsonLegacy(legacy)

  _migrarCalificacionesCE()
  _migrarCesDeActividades()

  return _db
}

/**
 * Pasa los criterios de las actividades a la clave RA|CE, para todos los módulos
 * y de una vez al arrancar.
 *
 * Antes lo hacía cada pantalla al cargarse: una migración de datos disparada por
 * la interfaz es difícil de auditar —no se sabe cuándo corrió ni sobre qué— y
 * dependía de que el profesorado visitara la sección adecuada.
 */
function _migrarCesDeActividades() {
  let migradas = 0
  try {
    const ceKeys = require('./renderer/js/utils/ce-keys.js')
    const modulos = _db.prepare('SELECT id, data_json FROM modulos').all()
    const upd = _db.prepare('UPDATE actividades SET ces=? WHERE id=?')

    _db.exec('BEGIN')
    for (const m of modulos) {
      let data = null
      try { data = JSON.parse(m.data_json || 'null') } catch { data = null }
      if (!data || !data.ces) continue
      const acts = _db.prepare('SELECT id, ut_id, ra_id, ces FROM actividades WHERE modulo_id=?').all(m.id)
      for (const act of acts) {
        const nuevo = ceKeys.migrarCesActividad(act, data.asignaciones || [], data.ces)
        if (!nuevo) continue
        upd.run(JSON.stringify(nuevo), act.id)
        migradas++
      }
    }
    _db.exec('COMMIT')
    if (migradas) console.log(`[db] Criterios de ${migradas} actividad(es) migrados a la clave RA|CE.`)
  } catch (e) {
    try { _db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    console.error('[db] No se pudieron migrar los criterios de las actividades:', e.message)
  }
  return migradas
}

/**
 * Traslada a la tabla `calificaciones_ce` las notas de 2ª convocatoria y los
 * criterios dados por alcanzados que se guardaban como JSON en `config`.
 * Solo se ejecuta si queda algo por migrar; después borra la clave de `config`
 * para que no haya dos fuentes de verdad.
 */
function _migrarCalificacionesCE() {
  let migradas = 0, ambiguas = 0
  try {
    const filas = _db.prepare(
      "SELECT key, value FROM config WHERE key LIKE 'rec2notas_%' OR key LIKE 'pardones_%'").all()
    if (!filas.length) return 0

    const up = _db.prepare(`INSERT INTO calificaciones_ce
      (alumno_id, ra_id, ce_id, convocatoria, nota, perdonado, motivo)
      VALUES (?,?,?,2,?,?,?)
      ON CONFLICT (alumno_id, ra_id, ce_id, convocatoria)
      DO UPDATE SET nota=COALESCE(excluded.nota, nota),
                    perdonado=MAX(perdonado, excluded.perdonado)`)
    const existeAlumno = _db.prepare('SELECT 1 FROM alumnos WHERE id=?')

    _db.exec('BEGIN')
    for (const fila of filas) {
      let datos = null
      try { datos = JSON.parse(fila.value) } catch { datos = null }
      const esPardon = fila.key.startsWith('pardones_')
      for (const [aid, contenido] of Object.entries(datos || {})) {
        const alumnoId = Number(aid)
        if (!existeAlumno.get(alumnoId)) continue          // alumno ya borrado
        const claves = esPardon ? contenido : Object.keys(contenido || {})
        for (const clave of (claves || [])) {
          const txt = String(clave)
          if (!txt.includes('|')) { ambiguas++; continue } // clave antigua sin RA
          const [raId, ceId] = txt.split('|')
          const nota = esPardon ? null : Number(contenido[txt])
          up.run(alumnoId, raId, ceId,
                 esPardon || isNaN(nota) ? null : nota,
                 esPardon ? 1 : 0,
                 esPardon ? 'Migrado del formato anterior' : null)
          migradas++
        }
      }
      _db.prepare('DELETE FROM config WHERE key=?').run(fila.key)
    }
    _db.exec('COMMIT')
    if (migradas || ambiguas) {
      console.log(`[db] ${migradas} calificaciones por criterio migradas a tabla propia` +
                  (ambiguas ? ` · ${ambiguas} descartadas por no indicar el RA` : '') + '.')
    }
  } catch (e) {
    try { _db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    console.error('[db] No se pudieron migrar las calificaciones por criterio:', e.message)
  }
  return migradas
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

    -- Calificaciones por criterio de evaluación y convocatoria.
    -- Son las notas de la 2ª convocatoria y los criterios que el profesorado da
    -- por alcanzados. Vivían como JSON dentro de la tabla de configuración, fuera
    -- del modelo: por eso el boletín y los informes no las veían y quedaban
    -- huérfanas al borrar un módulo. Aquí tienen clave foránea, fecha y motivo.
    CREATE TABLE IF NOT EXISTS calificaciones_ce (
      alumno_id    INTEGER NOT NULL,
      ra_id        TEXT    NOT NULL,
      ce_id        TEXT    NOT NULL,
      convocatoria INTEGER NOT NULL DEFAULT 2,
      nota         REAL,
      perdonado    INTEGER NOT NULL DEFAULT 0,
      motivo       TEXT,
      fecha        TEXT DEFAULT (datetime('now')),
      PRIMARY KEY (alumno_id, ra_id, ce_id, convocatoria),
      FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
    );

    -- Matrícula del alumnado en el módulo: convocatorias ya gastadas y si arrastra
    -- el módulo de un curso anterior.
    --   · art. 8.2 — máximo 4 convocatorias ordinarias en grado D, 2 en grado E
    --   · art. 11.4 — la renuncia no cuenta; art. 7.4 — la anulación tampoco
    --   · art. 19 — el alumnado con módulos pendientes se evalúa en las sesiones
    --     ordinarias del curso en el que está matriculado
    CREATE TABLE IF NOT EXISTS matricula (
      alumno_id     INTEGER PRIMARY KEY,
      convocatorias INTEGER NOT NULL DEFAULT 0,
      pendiente     INTEGER NOT NULL DEFAULT 0,   -- arrastra el módulo de otro curso
      observaciones TEXT,
      FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
    );

    -- Evidencias de evaluación: dónde está el documento que respalda una nota.
    -- El art. 2.4 de la Orden 201/2024 reconoce al alumnado el derecho a acceder
    -- «a las pruebas y documentos de las evaluaciones que se le realicen», así que
    -- desde la calificación hay que poder llegar al archivo.
    CREATE TABLE IF NOT EXISTS evidencias (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      alumno_id    INTEGER NOT NULL,
      actividad_id INTEGER,
      tipo         TEXT,          -- correccion | examen | trabajo | otro
      ruta         TEXT NOT NULL,
      descripcion  TEXT,
      fecha        TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (alumno_id)    REFERENCES alumnos(id)     ON DELETE CASCADE,
      FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE SET NULL
    );

    -- Fase de formación en empresa u organismo equiparado, por alumno.
    -- La Orden 201/2024 (art. 12) define tres estados de evaluación del módulo:
    -- «superado», «superado parcial» —a falta de esta fase— y «no superado»;
    -- el art. 25.4 obliga a reflejar SP en las actas, y el 18.4 dice que a
    -- efectos de promoción cuenta como superado.
    CREATE TABLE IF NOT EXISTS fase_empresa (
      alumno_id INTEGER PRIMARY KEY,
      estado    TEXT NOT NULL DEFAULT 'pendiente',   -- pendiente|superada|no_superada|exenta
      motivo    TEXT,
      fecha     TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
    );

    -- RA que el equipo docente ha dado por superados en una sesión de evaluación.
    -- «Un resultado de aprendizaje superado no se puede volver a evaluar»
    -- (Orden 201/2024 de CLM, art. 4.3.f): sin este registro, una actividad
    -- posterior volvía a bajar un RA que ya se había comunicado como alcanzado.
    CREATE TABLE IF NOT EXISTS ra_superados (
      alumno_id  INTEGER NOT NULL,
      ra_id      TEXT    NOT NULL,
      nota       REAL    NOT NULL,
      evaluacion INTEGER,
      fecha      TEXT DEFAULT (datetime('now')),
      PRIMARY KEY (alumno_id, ra_id),
      FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
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

/** Módulos archivados, para poder recuperarlos. */
const getModulosArchivados = () =>
  getDb().prepare('SELECT * FROM modulos WHERE activo=0 ORDER BY abrev').all()

const restaurarModulo = id =>
  getDb().prepare('UPDATE modulos SET activo=1 WHERE id=?').run(Number(id))

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

/**
 * Borra el módulo y todo lo suyo. Las cascadas se ocupan de alumnado,
 * actividades, notas y calificaciones por criterio; la configuración por módulo
 * hay que limpiarla a mano porque `config` es una tabla de clave-valor sin
 * relación (antes quedaban ahí el mínimo de examen y avisos huérfanos).
 */
function deleteModulo(id, { definitivo = false } = {}) {
  const db = getDb()
  const mid = Number(id)
  // Por defecto se archiva: un módulo con notas es un documento de evaluación y
  // borrarlo de verdad no debería ser un clic. `getModulos` solo devuelve los
  // activos, así que desaparece de la interfaz igualmente.
  if (!definitivo) {
    db.prepare('UPDATE modulos SET activo=0 WHERE id=?').run(mid)
    return { changes: 1, archivado: true }
  }
  db.prepare('DELETE FROM modulos WHERE id=?').run(mid)
  for (const pref of ['minexam_', 'faltas_', 'recmigra_avisado_', 'rec2notas_', 'pardones_']) {
    db.prepare('DELETE FROM config WHERE key=?').run(`${pref}${mid}`)
  }
  return { changes: 1 }
}

// ── Matrícula: convocatorias gastadas y módulos pendientes ───────────────────
const getMatriculas = moduloId => getDb().prepare(`
  SELECT m.alumno_id, m.convocatorias, m.pendiente, m.observaciones
  FROM matricula m JOIN alumnos a ON a.id = m.alumno_id
  WHERE a.modulo_id = ?
`).all(moduloId)

function setMatricula({ alumnoId, convocatorias = 0, pendiente = 0, observaciones = null }) {
  const c = Math.max(0, parseInt(convocatorias, 10) || 0)
  getDb().prepare(`INSERT INTO matricula (alumno_id, convocatorias, pendiente, observaciones)
    VALUES (?,?,?,?)
    ON CONFLICT (alumno_id) DO UPDATE SET convocatorias=excluded.convocatorias,
      pendiente=excluded.pendiente, observaciones=excluded.observaciones`)
    .run(alumnoId, c, pendiente ? 1 : 0, observaciones)
  return { alumnoId, convocatorias: c, pendiente: pendiente ? 1 : 0 }
}

// ── Evidencias de evaluación ─────────────────────────────────────────────────
const getEvidencias = moduloId => getDb().prepare(`
  SELECT e.id, e.alumno_id, e.actividad_id, e.tipo, e.ruta, e.descripcion, e.fecha
  FROM evidencias e JOIN alumnos a ON a.id = e.alumno_id
  WHERE a.modulo_id = ? ORDER BY e.fecha DESC
`).all(moduloId)

function addEvidencia({ alumnoId, actividadId = null, tipo = 'correccion', ruta, descripcion = null }) {
  if (!ruta) throw new Error('La evidencia necesita una ruta de archivo')
  return Number(getDb().prepare(`INSERT INTO evidencias
    (alumno_id, actividad_id, tipo, ruta, descripcion) VALUES (?,?,?,?,?)`)
    .run(alumnoId, actividadId, tipo, ruta, descripcion).lastInsertRowid)
}

// ── Fase de formación en empresa ─────────────────────────────────────────────
const getFaseEmpresa = moduloId => getDb().prepare(`
  SELECT f.alumno_id, f.estado, f.motivo, f.fecha
  FROM fase_empresa f JOIN alumnos a ON a.id = f.alumno_id
  WHERE a.modulo_id = ?
`).all(moduloId)

function setFaseEmpresa({ alumnoId, estado, motivo = null }) {
  const validos = ['pendiente', 'superada', 'no_superada', 'exenta']
  if (!validos.includes(estado)) throw new Error(`Estado de fase en empresa no válido: ${estado}`)
  getDb().prepare(`INSERT INTO fase_empresa (alumno_id, estado, motivo, fecha)
    VALUES (?,?,?,datetime('now'))
    ON CONFLICT (alumno_id) DO UPDATE SET estado=excluded.estado,
      motivo=excluded.motivo, fecha=excluded.fecha`).run(alumnoId, estado, motivo)
  return { alumnoId, estado, motivo }
}

// ── RA superados y cerrados en una sesión de evaluación ──────────────────────
const getRasSuperados = moduloId => getDb().prepare(`
  SELECT r.alumno_id, r.ra_id, r.nota, r.evaluacion, r.fecha
  FROM ra_superados r JOIN alumnos a ON a.id = r.alumno_id
  WHERE a.modulo_id = ?
`).all(moduloId)

/**
 * Cierra una sesión de evaluación: deja constancia de los RA alcanzados.
 * Nunca baja una nota ya registrada ni borra cierres anteriores.
 */
function cerrarEvaluacionRAs(moduloId, evaluacion, filas) {
  const db = getDb()
  const up = db.prepare(`INSERT INTO ra_superados (alumno_id, ra_id, nota, evaluacion, fecha)
    VALUES (?,?,?,?,datetime('now'))
    ON CONFLICT (alumno_id, ra_id) DO UPDATE SET
      nota = MAX(nota, excluded.nota),
      evaluacion = COALESCE(evaluacion, excluded.evaluacion)`)
  let n = 0
  db.exec('BEGIN')
  try {
    for (const f of (filas || [])) {
      if (f && f.alumnoId && f.raId && f.nota != null) {
        up.run(f.alumnoId, f.raId, f.nota, evaluacion ?? null); n++
      }
    }
    db.exec('COMMIT')
  } catch (e) { db.exec('ROLLBACK'); throw e }
  return n
}

/** Reabre un RA concreto (corrección de un cierre hecho por error). */
const reabrirRaSuperado = (alumnoId, raId) =>
  getDb().prepare('DELETE FROM ra_superados WHERE alumno_id=? AND ra_id=?').run(alumnoId, raId)

// ── Calificaciones por criterio (2ª convocatoria) ─────────────────────────────
const getCalificacionesCE = moduloId => getDb().prepare(`
  SELECT c.alumno_id, c.ra_id, c.ce_id, c.convocatoria, c.nota, c.perdonado, c.motivo, c.fecha
  FROM calificaciones_ce c
  JOIN alumnos a ON a.id = c.alumno_id
  WHERE a.modulo_id = ?
`).all(moduloId)

/**
 * Guarda —o borra— la calificación de un criterio en una convocatoria.
 * Sin nota y sin perdón la fila se elimina: no se guardan huecos.
 */
function setCalificacionCE({ alumnoId, raId, ceId, convocatoria = 2, nota = null, perdonado = 0, motivo = null }) {
  const db = getDb()
  const n = nota === '' || nota === null || nota === undefined ? null : parseFloat(nota)
  const p = perdonado ? 1 : 0
  if (n === null && !p) {
    db.prepare(`DELETE FROM calificaciones_ce
      WHERE alumno_id=? AND ra_id=? AND ce_id=? AND convocatoria=?`)
      .run(alumnoId, raId, ceId, convocatoria)
    return null
  }
  db.prepare(`INSERT INTO calificaciones_ce
    (alumno_id, ra_id, ce_id, convocatoria, nota, perdonado, motivo, fecha)
    VALUES (?,?,?,?,?,?,?,datetime('now'))
    ON CONFLICT (alumno_id, ra_id, ce_id, convocatoria)
    DO UPDATE SET nota=excluded.nota, perdonado=excluded.perdonado,
                  motivo=excluded.motivo, fecha=excluded.fecha`)
    .run(alumnoId, raId, ceId, convocatoria, n, p, motivo)
  return { alumnoId, raId, ceId, convocatoria, nota: n, perdonado: p, motivo }
}

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
    db.prepare(`UPDATE actividades SET descripcion=?,instrumento=COALESCE(?,instrumento),
        tipo=COALESCE(?,tipo),peso=?,nota_max=?,eval=?,ut_id=?,ra_id=?,ces=?,orden=? WHERE id=?`)
      .run(a.descripcion, a.instrumento ?? null, a.tipo ?? null, a.peso, a.nota_max,
           a.eval??1, a.ut_id??null, a.ra_id??null, cesJson, a.orden??0, a.id)
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
  // La escala la valida la interfaz contra `nota_max`, pero la base es la última
  // línea: por IPC se podía guardar un 99 y arrastrarlo a todas las medias.
  if (val !== null && (isNaN(val) || val < 0 || val > 20)) {
    throw new Error(`Nota fuera de rango: ${nota}`)
  }
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
  if (val !== null && (isNaN(val) || val < 0 || val > 20)) {
    throw new Error(`Nota de recuperación fuera de rango: ${notaRec}`)
  }
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
  getModulos, getModulosArchivados, restaurarModulo, addModulo, deleteModulo, setModuloDataJson,
  getAlumnos, saveAlumno, deleteAlumno,
  getActividades, saveActividad, deleteActividad,
  getNotasGrid, saveNota, saveNotaRec, closeDb, backupTo,
  getRaPonderaciones, setRaPonderacion,
  getCalificacionesCE, setCalificacionCE,
  getRasSuperados, cerrarEvaluacionRAs, reabrirRaSuperado,
  getFaseEmpresa, setFaseEmpresa,
  getEvidencias, addEvidencia,
  getMatriculas, setMatricula,
  getConfig, setConfig, deleteConfig, getAllConfig,
}

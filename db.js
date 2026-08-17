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
 * Aquel formato dejó de existir hace muchas versiones y su reimportación ya no
 * se mantiene: lo que queda es la red de seguridad. Si aparece un fichero así,
 * se aparta —nunca se borra— y se dice en claro qué ha pasado y dónde está,
 * en vez de dejar la aplicación muerta con un error de SQLite.
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

  const respaldo = path.join(
    path.dirname(dbPath),
    `evalfp-json-legacy-${new Date().toISOString().replace(/[:.]/g, '-')}.json`
  )
  try { fs.renameSync(dbPath, respaldo) } catch { return null }
  // Limpiar posibles ficheros WAL/SHM huérfanos del intento anterior
  for (const ext of ['-wal', '-shm']) {
    try { fs.unlinkSync(dbPath + ext) } catch { /* no existen */ }
  }
  console.warn(
    `[db] El fichero evalfp.db era de una versión muy anterior de EvalFP y no es una base ` +
    `de datos SQLite. Se ha apartado sin tocarlo en ${path.basename(respaldo)} y se ha creado ` +
    `una base nueva y vacía. Sus datos siguen ahí: para recuperarlos hace falta una versión ` +
    `3.x anterior a la 3.10.0, que todavía sabía leer aquel formato.`)
  return respaldo
}

function getDb() {
  if (_db) return _db
  const dbPath = path.join(app.getPath('userData'), 'evalfp.db')
  _apartarJsonLegacy(dbPath)
  _db = new DatabaseSync(dbPath)
  // `busy_timeout`: si otra ventana está escribiendo —un cierre de evaluación, una
  // copia de seguridad—, SQLite esperaba cero y devolvía «database is locked» al
  // instante, así que la nota que se acababa de teclear no se guardaba. Con cinco
  // segundos de espera, reintenta él solo y el choque desaparece.
  _db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA busy_timeout = 5000;')
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

  // A-5 · Convocatoria a la que pertenece cada actividad.
  //
  // El art. 21.5 de la Orden 201/2024 dice que en segunda convocatoria los RA no
  // superados se evalúan «utilizando otros instrumentos de evaluación diferentes».
  // O sea: la 2ª convocatoria no es una lista de notas sueltas por criterio, son
  // ACTIVIDADES nuevas. Con esta columna, una prueba de recuperación es una
  // actividad como cualquier otra y el motor no necesita un camino aparte.
  //
  // Todo lo que ya existe es de la 1ª convocatoria: DEFAULT 1 y ninguna fila que
  // tocar.
  if (!colsAct.some(c => c.name === 'convocatoria')) {
    _db.exec('ALTER TABLE actividades ADD COLUMN convocatoria INTEGER NOT NULL DEFAULT 1')
  }

  // Prueba objetiva de evaluación completa del módulo.
  //
  // Es la del art. 3.6 de la Orden 201/2024, en la redacción que le da la Orden
  // 55/2026: la que se hace a quien ha perdido el derecho a la evaluación
  // continua, y que «incluirá la totalidad de los resultados de aprendizaje a
  // través de sus criterios de evaluación». No vale marcarla como un examen más:
  // el motor tiene que poder quedarse SOLO con ella y descartar todo lo demás.
  if (!colsAct.some(c => c.name === 'prueba_objetiva')) {
    _db.exec('ALTER TABLE actividades ADD COLUMN prueba_objetiva INTEGER NOT NULL DEFAULT 0')
  }

  // Convalidación del módulo (art. 25.7) y su efecto en la nota final del ciclo.
  //
  // El art. 25.11 —antes 25.12, renumerado por la Orden 55/2026— excluye del
  // cálculo de la calificación final los módulos «convalidados sin nota». Con
  // nota sí computan, así que hacen falta las dos columnas: la marca y la nota.
  const colsMat = _db.prepare('PRAGMA table_info(matricula)').all()
  if (!colsMat.some(c => c.name === 'convalidado')) {
    _db.exec('ALTER TABLE matricula ADD COLUMN convalidado INTEGER NOT NULL DEFAULT 0')
  }
  if (!colsMat.some(c => c.name === 'nota_convalidacion')) {
    _db.exec('ALTER TABLE matricula ADD COLUMN nota_convalidacion REAL')
  }

  _migrarUnicidadModulos()

  // Notas fuera de escala que hubiera dejado alguna versión anterior: la
  // validación estaba solo en la interfaz y por IPC se podía colar un 99.
  const fuera = _db.prepare(
    'SELECT COUNT(*) AS n FROM notas WHERE nota < 0 OR nota > 10 OR nota_rec < 0 OR nota_rec > 10').get()
  if (fuera && fuera.n > 0) {
    console.warn(`[db] ${fuera.n} nota(s) fuera del rango 0-10; se dejan como están para no perder datos.`)
  }

  _migrarCalificacionesCE()
  _migrarCesDeActividades()

  return _db
}

/**
 * Unicidad de `modulos`: un módulo es único por su clave, su grupo y su curso
 * escolar.
 *
 * Han hecho falta dos pasadas. La primera quitó el UNIQUE de `key` a secas, que
 * impedía dar el mismo módulo a dos grupos. La segunda añade el curso escolar:
 * sin él, en septiembre no se podía dar de alta ISO · 1ºA del curso nuevo
 * mientras existiera el del anterior, ni siquiera archivado, porque la
 * restricción mira toda la tabla. Había que borrar el curso pasado para empezar
 * el siguiente.
 *
 * SQLite no permite quitar una restricción con ALTER, así que hay que recrear la
 * tabla — el procedimiento que documenta la propia SQLite: claves foráneas
 * apagadas, dentro de una transacción, y comprobando la integridad antes de
 * confirmar.
 */
function _migrarUnicidadModulos() {
  let sql = ''
  try {
    const fila = _db.prepare(
      "SELECT sql FROM sqlite_master WHERE type='table' AND name='modulos'").get()
    sql = String(fila?.sql || '')
  } catch { return }
  // Ya migrada del todo: la restricción incluye el curso escolar
  if (!sql || /UNIQUE\s*\(\s*key\s*,\s*grupo\s*,\s*anno\s*\)/i.test(sql)) return

  try {
    _db.exec('PRAGMA foreign_keys = OFF')
    _db.exec('BEGIN')
    _db.exec(`
      CREATE TABLE modulos_nuevo (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        key        TEXT NOT NULL,
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
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE (key, grupo, anno)
      );
      INSERT INTO modulos_nuevo
        SELECT id,key,abrev,nombre,ciclo,curso,anno,grupo,horas,decreto,data_json,activo,created_at
        FROM modulos;
      DROP TABLE modulos;
      ALTER TABLE modulos_nuevo RENAME TO modulos;
    `)
    const fallos = _db.prepare('PRAGMA foreign_key_check').all()
    if (fallos.length) throw new Error(`${fallos.length} referencia(s) rota(s)`)
    _db.exec('COMMIT')
    console.log('[db] modulos: la unicidad pasa a ser (módulo, grupo, curso escolar)')
  } catch (e) {
    try { _db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    console.error('[db] No se pudo migrar la unicidad de modulos:', e.message)
  } finally {
    _db.exec('PRAGMA foreign_keys = ON')
  }
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

/**
 * RF-02 · Normaliza la programación de `modulos.data_json` a las tablas con
 * clave foránea (`ra_catalogo`, `ce_catalogo`, `unidades_trabajo`, `ut_ce`,
 * `ce_instrumentos_previstos`, `actividad_ce`). Ver
 * docs/rediseno/05-PLAN-MIGRACION.md §2, §4 y §5 (pasos 2 a 4).
 *
 * Fail-closed, sin excepciones (§2 del plan): un único `BEGIN`/`COMMIT` para
 * TODOS los módulos de la base. Cualquier inconsistencia en cualquier módulo
 * —JSON corrupto, un RA/CE/UT huérfano, una actividad que evalúa un criterio
 * que ya no está en el catálogo— lanza un Error con el módulo y el motivo, y
 * hace `ROLLBACK` de la migración entera, no solo de ese módulo: no hay
 * estado mixto donde unos módulos queden normalizados y otros no.
 *
 * Idempotente: se puede volver a ejecutar sin duplicar nada. Las tablas de
 * catálogo (ra_catalogo, ce_catalogo, unidades_trabajo) hacen upsert por su
 * clave; las de relación (ut_ce, ce_instrumentos_previstos, actividad_ce) usan
 * `INSERT OR IGNORE`.
 *
 * Deliberadamente NO se llama desde `getDb()`: a diferencia de las demás
 * migraciones de este fichero, esta es fail-closed y podría dejar la base sin
 * arrancar para cualquier profesor cuya programación tenga una inconsistencia
 * ya tolerada hoy. Se invoca aparte —de momento solo desde los tests— hasta
 * que la segunda mitad de RF-02 (las pantallas leyendo de estas tablas) esté
 * lista para desplegarse junto con ella.
 *
 * @returns {{modulos:number, ra_catalogo:number, ce_catalogo:number,
 *            unidades_trabajo:number, ut_ce:number,
 *            ce_instrumentos_previstos:number, actividad_ce:number}}
 */
function migrarProgramacionNormalizada() {
  const db = getDb()
  const resumen = {
    modulos: 0, ra_catalogo: 0, ce_catalogo: 0, unidades_trabajo: 0,
    ut_ce: 0, ce_instrumentos_previstos: 0, actividad_ce: 0,
  }

  const modulos = db.prepare('SELECT id, key, abrev, data_json FROM modulos').all()

  const insRa = db.prepare(`
    INSERT INTO ra_catalogo (modulo_id, ra_id, nombre, pond, llave, dual_pct)
    VALUES (?,?,?,?,?,?)
    ON CONFLICT (modulo_id, ra_id) DO UPDATE SET
      nombre=excluded.nombre, pond=excluded.pond, llave=excluded.llave, dual_pct=excluded.dual_pct
  `)
  const insCe = db.prepare(`
    INSERT INTO ce_catalogo (modulo_id, ra_id, ce_id, texto, peso)
    VALUES (?,?,?,?,?)
    ON CONFLICT (modulo_id, ra_id, ce_id) DO UPDATE SET texto=excluded.texto, peso=excluded.peso
  `)
  const insUt = db.prepare(`
    INSERT INTO unidades_trabajo (modulo_id, ut_id, nombre, horas, horas_empresa, eval, tags)
    VALUES (?,?,?,?,?,?,?)
    ON CONFLICT (modulo_id, ut_id) DO UPDATE SET
      nombre=excluded.nombre, horas=excluded.horas, horas_empresa=excluded.horas_empresa,
      eval=excluded.eval, tags=excluded.tags
  `)
  const insUtCe = db.prepare(
    'INSERT OR IGNORE INTO ut_ce (modulo_id, ut_id, ra_id, ce_id) VALUES (?,?,?,?)')
  const insInstr = db.prepare(`
    INSERT OR IGNORE INTO ce_instrumentos_previstos (modulo_id, ra_id, ce_id, instrumento)
    VALUES (?,?,?,?)`)
  const insActCe = db.prepare(
    'INSERT OR IGNORE INTO actividad_ce (actividad_id, modulo_id, ra_id, ce_id) VALUES (?,?,?,?)')
  const selActividades = db.prepare('SELECT id, ces FROM actividades WHERE modulo_id=?')
  const selOverrides = db.prepare('SELECT ra_id, pond FROM ra_ponderaciones WHERE modulo_id=?')

  /** Aborta con un motivo que identifica el módulo, tal y como exige el plan. */
  const fail = (mod, motivo) => {
    throw new Error(`módulo ${mod.id} (${mod.key}): ${motivo}`)
  }

  db.exec('BEGIN')
  try {
    for (const mod of modulos) {
      resumen.modulos++

      let data
      try {
        data = JSON.parse(mod.data_json || '{}')
      } catch (e) {
        fail(mod, `data_json no es JSON válido (${e.message})`)
      }
      if (!data || typeof data !== 'object') data = {}

      const ras = Array.isArray(data.ras) ? data.ras : []
      const ces = data.ces && typeof data.ces === 'object' ? data.ces : {}
      const uts = Array.isArray(data.uts) ? data.uts : []
      const asignaciones = Array.isArray(data.asignaciones) ? data.asignaciones : []
      const raInstrumentos = data.ra_instrumentos && typeof data.ra_instrumentos === 'object'
        ? data.ra_instrumentos : {}

      const raIds = new Set(ras.map(r => String(r?.id)))
      const utIds = new Set(uts.map(u => String(u?.id)))

      // ── 2.1 · ra_catalogo — pond EFECTIVO: override de ra_ponderaciones,
      // si no hay override el del JSON. ──────────────────────────────────
      const overrides = Object.fromEntries(
        selOverrides.all(mod.id).map(r => [r.ra_id, r.pond]))
      for (const ra of ras) {
        if (!ra || !String(ra.id ?? '').trim() || !String(ra.nombre ?? '').trim()) {
          fail(mod, `RA sin id o sin nombre (${JSON.stringify(ra)})`)
        }
        const raId = String(ra.id)
        const pond = overrides[raId] !== undefined ? overrides[raId] : (ra.pond ?? 0)
        insRa.run(mod.id, raId, ra.nombre, Number(pond) || 0, ra.llave ? 1 : 0,
                   ra.dual == null ? null : Number(ra.dual))
        resumen.ra_catalogo++
      }

      // ── 2.2 · ce_catalogo ───────────────────────────────────────────────
      for (const raId of Object.keys(ces)) {
        if (!raIds.has(raId)) fail(mod, `'ces' tiene un RA (${raId}) que no está en 'ras'`)
        for (const ce of ces[raId] || []) {
          insCe.run(mod.id, raId, String(ce.id), ce.texto ?? '',
                     ce.peso == null || ce.peso === '' ? null : Number(ce.peso))
          resumen.ce_catalogo++
        }
      }

      // ── 2.3 · unidades_trabajo ──────────────────────────────────────────
      for (const ut of uts) {
        insUt.run(mod.id, String(ut.id), ut.nombre ?? '', ut.horas ?? 0, ut.horas_empresa ?? 0,
                   ut.eval ?? 1, ut.tags ?? null)
        resumen.unidades_trabajo++
      }

      // ── 2.4 · ut_ce, explota asignaciones ────────────────────────────────
      for (const asig of asignaciones) {
        const utId = String(asig?.ut)
        const raId = String(asig?.ra)
        if (!asig || !utIds.has(utId)) fail(mod, `asignación a la UT '${asig?.ut}', que no existe`)
        if (!raIds.has(raId)) fail(mod, `asignación al RA '${asig?.ra}', que no existe`)
        const ceDisponibles = new Set((ces[raId] || []).map(c => String(c.id)))
        for (const ceId of asig.ces || []) {
          if (!ceDisponibles.has(String(ceId))) {
            fail(mod, `la asignación ${utId}→${raId} referencia el CE '${ceId}', que no ` +
                       `existe en el catálogo de ${raId}`)
          }
          insUtCe.run(mod.id, utId, raId, String(ceId))
          resumen.ut_ce++
        }
      }

      // ── 2.5 · ce_instrumentos_previstos, hereda de RA a cada CE ──────────
      for (const raId of Object.keys(raInstrumentos)) {
        if (!raIds.has(raId)) {
          fail(mod, `'ra_instrumentos' tiene un RA (${raId}) que no está en 'ras'`)
        }
        for (const ce of ces[raId] || []) {
          for (const instrumento of raInstrumentos[raId] || []) {
            insInstr.run(mod.id, raId, String(ce.id), String(instrumento))
            resumen.ce_instrumentos_previstos++
          }
        }
      }

      // ── 2.6 · actividad_ce, desde la tabla VIVA actividades, no data_json ──
      for (const act of selActividades.all(mod.id)) {
        let lista
        try { lista = JSON.parse(act.ces || '[]') } catch { lista = [] }
        if (!Array.isArray(lista)) lista = []
        for (const clave of lista) {
          const s = String(clave)
          const i = s.indexOf('|')
          if (i < 0) {
            fail(mod, `actividad ${act.id}: el criterio '${s}' no tiene la clave compuesta RA|CE`)
          }
          const raId = s.slice(0, i)
          const ceId = s.slice(i + 1)
          const existe = (ces[raId] || []).some(c => String(c.id) === ceId)
          if (!existe) {
            fail(mod, `actividad ${act.id}: evalúa el criterio '${raId}|${ceId}', que ya no ` +
                       'está en el catálogo')
          }
          insActCe.run(act.id, mod.id, raId, ceId)
          resumen.actividad_ce++
        }
      }
    }

    // ── Paso 4 del plan: verificar antes de confirmar ──────────────────────
    const rotas = db.prepare('PRAGMA foreign_key_check').all()
    if (rotas.length) {
      throw new Error(
        `PRAGMA foreign_key_check encontró ${rotas.length} referencia(s) rota(s) tras migrar; ` +
        'no se confirma la migración')
    }

    db.exec('COMMIT')
  } catch (e) {
    try { db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    throw e
  }

  return resumen
}

// ── RF-02 · Programación normalizada — lectura y edición ──────────────────────
// (docs/rediseno/05-PLAN-MIGRACION.md). Un módulo sin filas en ra_catalogo no
// está migrado: quien llama a esto decide qué hacer (avisar y remitir a
// Ajustes, típicamente), no se inventa nada aquí.

/** RA del catálogo normalizado de un módulo. [] si el módulo no está migrado. */
function getRaCatalogo(moduloId) {
  return getDb().prepare(
    'SELECT ra_id, nombre, pond, llave, dual_pct FROM ra_catalogo WHERE modulo_id=? ORDER BY ra_id'
  ).all(moduloId)
}

function setRaCatalogoPond(moduloId, raId, pond) {
  const r = getDb().prepare('UPDATE ra_catalogo SET pond=? WHERE modulo_id=? AND ra_id=?')
    .run(Number(pond) || 0, moduloId, raId)
  if (!r.changes) throw new Error(`RA ${raId} no está en el catálogo normalizado del módulo ${moduloId}`)
}

function setRaCatalogoLlave(moduloId, raId, llave) {
  const r = getDb().prepare('UPDATE ra_catalogo SET llave=? WHERE modulo_id=? AND ra_id=?')
    .run(llave ? 1 : 0, moduloId, raId)
  if (!r.changes) throw new Error(`RA ${raId} no está en el catálogo normalizado del módulo ${moduloId}`)
}

function setRaCatalogoDual(moduloId, raId, dualPct) {
  const limpio = dualPct == null || dualPct === '' ? null : Number(dualPct)
  const r = getDb().prepare('UPDATE ra_catalogo SET dual_pct=? WHERE modulo_id=? AND ra_id=?')
    .run(limpio, moduloId, raId)
  if (!r.changes) throw new Error(`RA ${raId} no está en el catálogo normalizado del módulo ${moduloId}`)
}

/** CE del catálogo normalizado de un módulo. */
function getCeCatalogo(moduloId) {
  return getDb().prepare(
    'SELECT ra_id, ce_id, texto, peso FROM ce_catalogo WHERE modulo_id=? ORDER BY ra_id, ce_id'
  ).all(moduloId)
}

/** Peso de un CE dentro de su RA. NULL = reparto automático (no 0). */
function setCeCatalogoPeso(moduloId, raId, ceId, peso) {
  const limpio = peso == null || peso === '' ? null : Number(peso)
  const r = getDb().prepare('UPDATE ce_catalogo SET peso=? WHERE modulo_id=? AND ra_id=? AND ce_id=?')
    .run(limpio, moduloId, raId, ceId)
  if (!r.changes) throw new Error(`CE ${raId}|${ceId} no está en el catálogo normalizado del módulo ${moduloId}`)
}

/** Instrumentos previstos del módulo, por CE. */
function getCeInstrumentosPrevistos(moduloId) {
  return getDb().prepare(
    'SELECT ra_id, ce_id, instrumento FROM ce_instrumentos_previstos WHERE modulo_id=? ' +
    'ORDER BY ra_id, ce_id, instrumento'
  ).all(moduloId)
}

/** Fija los instrumentos previstos de UN CE (sustituye los que hubiera): la excepción puntual por CE de RF-02. */
function setCeInstrumentos(moduloId, raId, ceId, instrumentos) {
  const db = getDb()
  db.exec('BEGIN')
  try {
    db.prepare('DELETE FROM ce_instrumentos_previstos WHERE modulo_id=? AND ra_id=? AND ce_id=?')
      .run(moduloId, raId, ceId)
    const ins = db.prepare(
      'INSERT INTO ce_instrumentos_previstos (modulo_id, ra_id, ce_id, instrumento) VALUES (?,?,?,?)')
    const limpios = [...new Set((instrumentos || []).map(i => String(i || '').trim()).filter(Boolean))]
    for (const instr of limpios) ins.run(moduloId, raId, ceId, instr)
    db.exec('COMMIT')
  } catch (e) {
    try { db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    throw e
  }
}

/**
 * Declara los instrumentos previstos de un RA: los hereda CADA CE del RA
 * (RF-02: "se declara por RA, lo heredan sus CE, con excepción puntual por
 * CE"). Sustituye lo que hubiera en cada CE — incluida una excepción puntual
 * que ya existiera, porque esto es precisamente "volver a declarar por RA".
 */
function setRaInstrumentos(moduloId, raId, instrumentos) {
  const db = getDb()
  const ces = db.prepare('SELECT ce_id FROM ce_catalogo WHERE modulo_id=? AND ra_id=?').all(moduloId, raId)
  const limpios = [...new Set((instrumentos || []).map(i => String(i || '').trim()).filter(Boolean))]
  db.exec('BEGIN')
  try {
    const del = db.prepare(
      'DELETE FROM ce_instrumentos_previstos WHERE modulo_id=? AND ra_id=? AND ce_id=?')
    const ins = db.prepare(
      'INSERT INTO ce_instrumentos_previstos (modulo_id, ra_id, ce_id, instrumento) VALUES (?,?,?,?)')
    for (const ce of ces) {
      del.run(moduloId, raId, ce.ce_id)
      for (const instr of limpios) ins.run(moduloId, raId, ce.ce_id, instr)
    }
    db.exec('COMMIT')
  } catch (e) {
    try { db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    throw e
  }
}

// ── RF-17 · Familia de reparto por tipo de actividad ──────────────────────────
// (docs/rediseno/00-CONTEXTO.md §10). La lista de tipos válidos vive en
// renderer/js/utils/tipos-actividad.js, la misma que usa RF-02 para
// "instrumento previsto" — se valida aquí contra esa fuente, no una copia.

/** { tipo, familia } por módulo. [] si el módulo no ha fijado ningún override. */
const getTipoFamilia = moduloId =>
  getDb().prepare('SELECT tipo, familia FROM tipo_familia WHERE modulo_id=?').all(moduloId)

function setTipoFamilia(moduloId, tipo, familia) {
  const { TIPOS_ACTIVIDAD } = require('./renderer/js/utils/tipos-actividad.js')
  if (!TIPOS_ACTIVIDAD.some(t => t.id === tipo)) {
    throw new Error(`tipo de actividad desconocido: ${tipo}`)
  }
  if (familia !== 'examen' && familia !== 'practica') {
    throw new Error(`familia de reparto inválida: ${familia} (solo 'examen' o 'practica')`)
  }
  getDb().prepare(`
    INSERT INTO tipo_familia (modulo_id, tipo, familia) VALUES (?,?,?)
    ON CONFLICT (modulo_id, tipo) DO UPDATE SET familia=excluded.familia
  `).run(moduloId, tipo, familia)
}

// ── RF-02 · Unidades de trabajo normalizadas (segunda parte) ──────────────────
// (docs/rediseno/04-REDISENO-PANTALLAS.md §1.2-§1.4). Sustituyen a data_json.uts
// y data_json.asignaciones para la vista de Unidades de Trabajo. El resto de
// Programación (plan de actividades, distribución, mapa) sigue en data_json
// hasta que le llegue su turno — mismo patrón que ra_catalogo/ce_catalogo.

/** UT de un módulo, ordenadas por id. [] si el módulo no está migrado. */
const getUnidadesTrabajo = moduloId => getDb().prepare(
  'SELECT ut_id, nombre, horas, horas_empresa, eval, tags FROM unidades_trabajo WHERE modulo_id=? ORDER BY ut_id'
).all(moduloId)

/**
 * Crea o actualiza una UT. Sin `utId` genera el siguiente libre (UT1, UT2…),
 * saltando huecos de UT borradas para no reutilizar un id que ya significó
 * otra cosa.
 * @returns {string} el ut_id, nuevo o el mismo que se pasó
 */
function setUnidadTrabajo(moduloId, utId, campos) {
  const db = getDb()
  const { nombre, horas, horasEmpresa, eval: evalNum, tags } = campos || {}
  let id = utId
  if (!id) {
    const existentes = new Set(db.prepare('SELECT ut_id FROM unidades_trabajo WHERE modulo_id=?')
      .all(moduloId).map(r => r.ut_id))
    let n = existentes.size + 1
    while (existentes.has(`UT${n}`)) n++
    id = `UT${n}`
  }
  db.prepare(`
    INSERT INTO unidades_trabajo (modulo_id, ut_id, nombre, horas, horas_empresa, eval, tags)
    VALUES (?,?,?,?,?,?,?)
    ON CONFLICT (modulo_id, ut_id) DO UPDATE SET
      nombre=excluded.nombre, horas=excluded.horas, horas_empresa=excluded.horas_empresa,
      eval=excluded.eval, tags=excluded.tags
  `).run(moduloId, id, nombre ?? '', Number(horas) || 0, Number(horasEmpresa) || 0,
         Number(evalNum) || 1, tags ?? null)
  return id
}

/**
 * Borra una UT. `ut_ce` cae en cascada por FK. Las actividades que la tuvieran
 * asignada NO se tocan — `actividades.ut_id` es texto libre, sin FK a esta
 * tabla (RF-02 no lo normaliza, ver docs/rediseno/05-PLAN-MIGRACION.md §8):
 * quedan con el id de una unidad que ya no existe en el catálogo, que es
 * justo lo que tiene que pasar («lo evaluado es hecho», §1.3).
 */
const deleteUnidadTrabajo = (moduloId, utId) =>
  getDb().prepare('DELETE FROM unidades_trabajo WHERE modulo_id=? AND ut_id=?').run(moduloId, utId)

/** {ra_id, ce_id}[] asignados a una UT. */
const getUtCe = (moduloId, utId) => getDb().prepare(
  'SELECT ra_id, ce_id FROM ut_ce WHERE modulo_id=? AND ut_id=?'
).all(moduloId, utId)

/** Toda la asignación UT→CE de un módulo, para el indicador de cobertura. */
const getUtCeModulo = moduloId => getDb().prepare(
  'SELECT ut_id, ra_id, ce_id FROM ut_ce WHERE modulo_id=?'
).all(moduloId)

/**
 * Sustituye TODA la asignación de CE de una UT. No toca `actividad_ce`: quitar
 * un CE de una UT no desvincula lo que una actividad ya evaluó con él.
 */
function setUtCe(moduloId, utId, pares) {
  const db = getDb()
  db.exec('BEGIN')
  try {
    db.prepare('DELETE FROM ut_ce WHERE modulo_id=? AND ut_id=?').run(moduloId, utId)
    const ins = db.prepare('INSERT INTO ut_ce (modulo_id, ut_id, ra_id, ce_id) VALUES (?,?,?,?)')
    for (const { ra_id, ce_id } of (pares || [])) ins.run(moduloId, utId, ra_id, ce_id)
    db.exec('COMMIT')
  } catch (e) {
    try { db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    throw e
  }
}

/** {ra_id, ce_id}[] que evalúa una actividad. */
const getActividadCe = actividadId => getDb().prepare(
  'SELECT ra_id, ce_id FROM actividad_ce WHERE actividad_id=?'
).all(actividadId)

/** Toda la relación actividad→CE de un módulo, para el indicador de cobertura. */
const getActividadCeModulo = moduloId => getDb().prepare(
  'SELECT actividad_id, ra_id, ce_id FROM actividad_ce WHERE modulo_id=?'
).all(moduloId)

/** Sustituye los CE que evalúa una actividad. */
function setActividadCe(actividadId, moduloId, pares) {
  const db = getDb()
  db.exec('BEGIN')
  try {
    db.prepare('DELETE FROM actividad_ce WHERE actividad_id=?').run(actividadId)
    const ins = db.prepare(
      'INSERT INTO actividad_ce (actividad_id, modulo_id, ra_id, ce_id) VALUES (?,?,?,?)')
    for (const { ra_id, ce_id } of (pares || [])) ins.run(actividadId, moduloId, ra_id, ce_id)
    db.exec('COMMIT')
  } catch (e) {
    try { db.exec('ROLLBACK') } catch { /* sin transacción activa */ }
    throw e
  }
}

function _initSchema() {
  _db.exec(`
    -- Módulos que el profesor imparte
    -- Los datos normativos (RAs, CEs) vienen del DOCM Castilla-La Mancha
    CREATE TABLE IF NOT EXISTS modulos (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      -- La clave del módulo NO es única por sí sola: el mismo módulo se da a
      -- varios grupos y cada grupo es un cuaderno distinto. Lo único que no
      -- puede repetirse es la pareja módulo+grupo (ver UNIQUE al final).
      key        TEXT NOT NULL,
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
      created_at TEXT DEFAULT (datetime('now')),
      UNIQUE (key, grupo, anno)
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
      -- 1 = actividad del curso · 2 = prueba de recuperación de la 2ª
      -- convocatoria (Orden 201/2024, art. 21.5)
      convocatoria INTEGER NOT NULL DEFAULT 1,
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

    -- Pérdida del derecho a la evaluación continua, por alumno y módulo.
    --
    -- Orden 201/2024, art. 3.6 (redacción de la Orden 55/2026): quien lo pierde
    -- «tendrá derecho a la realización de las pruebas objetivas que determine el
    -- equipo docente […] sin que pueda considerarse la conservación de
    -- calificaciones parciales obtenidas con anterioridad».
    --
    -- Se guarda la fecha y el motivo porque es una decisión que hay que poder
    -- justificar: es la que deja a alguien sin la nota que ya había sacado.
    CREATE TABLE IF NOT EXISTS evaluacion_continua (
      alumno_id INTEGER PRIMARY KEY,
      perdida   INTEGER NOT NULL DEFAULT 0,
      fecha     TEXT DEFAULT (datetime('now')),
      motivo    TEXT,
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

    -- RF-01 · Estado de impartición del RA (Orden 201/2024, art. 2.3).
    -- Es de GRUPO, no de alumno: o el RA se da al módulo entero o no se da.
    -- 'previsto' | 'impartido' | 'no_impartido'. El estado no se deduce de que
    -- existan actividades; la ausencia de un RA tiene que ser una decisión
    -- fechada y motivada, no un efecto colateral de no haberlo programado.
    CREATE TABLE IF NOT EXISTS ra_estado (
      modulo_id  INTEGER NOT NULL,
      ra_id      TEXT    NOT NULL,
      estado     TEXT    NOT NULL DEFAULT 'previsto',
      motivo     TEXT,
      fecha      TEXT,
      PRIMARY KEY (modulo_id, ra_id),
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- ═══════════════════════════════════════════════════════════════════════
    -- RF-02 · Programación normalizada (ver docs/rediseno/05-PLAN-MIGRACION.md)
    -- ═══════════════════════════════════════════════════════════════════════
    -- Sustituyen, tabla a tabla, a lo que hoy vive dentro de modulos.data_json.
    -- Se crean aquí (aditivo, no toca ninguna fila existente) pero todavía no
    -- las llena nadie automáticamente: eso lo hace migrarProgramacionNormalizada(),
    -- que hay que invocar aparte. El renderer sigue leyendo data_json hasta la
    -- segunda mitad de RF-02.

    -- Catálogo de RA del módulo. 'pond' es el valor EFECTIVO: fusión del
    -- 'pond' del JSON con el override que hoy vive en ra_ponderaciones.
    CREATE TABLE IF NOT EXISTS ra_catalogo (
      modulo_id INTEGER NOT NULL,
      ra_id     TEXT    NOT NULL,
      nombre    TEXT    NOT NULL,
      pond      REAL    NOT NULL DEFAULT 0,
      llave     INTEGER NOT NULL DEFAULT 0,   -- necesario para la fase de empresa (art. 4.3.a)
      dual_pct  REAL,                          -- % del RA que se acredita en empresa; NULL = nada
      PRIMARY KEY (modulo_id, ra_id),
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- Catálogo de CE del módulo. 'peso' NULL = reparto automático entre los CE
    -- del mismo RA: una casilla en blanco no es un dato que falta.
    CREATE TABLE IF NOT EXISTS ce_catalogo (
      modulo_id INTEGER NOT NULL,
      ra_id     TEXT    NOT NULL,
      ce_id     TEXT    NOT NULL,
      texto     TEXT    NOT NULL,
      peso      REAL,
      PRIMARY KEY (modulo_id, ra_id, ce_id),
      FOREIGN KEY (modulo_id, ra_id) REFERENCES ra_catalogo(modulo_id, ra_id) ON DELETE CASCADE
    );

    -- Unidades de trabajo.
    CREATE TABLE IF NOT EXISTS unidades_trabajo (
      modulo_id     INTEGER NOT NULL,
      ut_id         TEXT    NOT NULL,
      nombre        TEXT    NOT NULL,
      horas         INTEGER DEFAULT 0,
      horas_empresa INTEGER DEFAULT 0,
      eval          INTEGER NOT NULL DEFAULT 1,
      tags          TEXT,
      PRIMARY KEY (modulo_id, ut_id),
      FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
    );

    -- Asignación UT→CE, explotada a una fila por CE: no puede existir una
    -- asignación UT–RA que contradiga la relación UT–CE, porque el RA de una
    -- UT se DERIVA agrupando estas filas, no se declara aparte.
    CREATE TABLE IF NOT EXISTS ut_ce (
      modulo_id INTEGER NOT NULL,
      ut_id     TEXT    NOT NULL,
      ra_id     TEXT    NOT NULL,
      ce_id     TEXT    NOT NULL,
      PRIMARY KEY (modulo_id, ut_id, ra_id, ce_id),
      FOREIGN KEY (modulo_id, ut_id) REFERENCES unidades_trabajo(modulo_id, ut_id) ON DELETE CASCADE,
      FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
        ON DELETE CASCADE
    );

    -- Instrumento previsto, resuelto A NIVEL DE CE (art. 4.3.b) aunque hoy se
    -- declare por RA en la interfaz. Un CE puede tener varios instrumentos.
    CREATE TABLE IF NOT EXISTS ce_instrumentos_previstos (
      modulo_id   INTEGER NOT NULL,
      ra_id       TEXT    NOT NULL,
      ce_id       TEXT    NOT NULL,
      instrumento TEXT    NOT NULL,
      PRIMARY KEY (modulo_id, ra_id, ce_id, instrumento),
      FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
        ON DELETE CASCADE
    );

    -- Índice único auxiliar: 'id' ya es única por sí sola (PK de actividades),
    -- pero SQLite exige un índice que cubra EXACTAMENTE las columnas de una
    -- referencia compuesta. Sin él no se puede declarar la FK de abajo.
    CREATE UNIQUE INDEX IF NOT EXISTS idx_actividades_id_modulo ON actividades(id, modulo_id);

    -- Relación actividad→CE, sustituye a la columna actividades.ces (JSON de
    -- claves "RA|CE"). modulo_id no es redundante: junto con la FK compuesta de
    -- abajo, obliga a que la actividad y el CE sean del MISMO módulo — sin ella,
    -- nada impedía una fila con el modulo_id de un módulo y el actividad_id de
    -- otro, y las FK por separado la habrían dejado pasar.
    CREATE TABLE IF NOT EXISTS actividad_ce (
      actividad_id INTEGER NOT NULL,
      modulo_id    INTEGER NOT NULL,
      ra_id        TEXT    NOT NULL,
      ce_id        TEXT    NOT NULL,
      PRIMARY KEY (actividad_id, ra_id, ce_id),
      FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE,
      FOREIGN KEY (actividad_id, modulo_id) REFERENCES actividades(id, modulo_id),
      FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
        ON DELETE CASCADE
    );

    -- RF-17 · Familia de reparto de cada tipo de actividad, por módulo
    -- (docs/rediseno/00-CONTEXTO.md §10). Dispersa: una fila solo existe
    -- cuando el módulo decide una familia distinta del defecto de
    -- renderer/js/utils/tipos-actividad.js. Sin ninguna fila, todos los
    -- tipos usan su defecto — es el estado de cualquier base existente.
    CREATE TABLE IF NOT EXISTS tipo_familia (
      modulo_id INTEGER NOT NULL,
      tipo      TEXT    NOT NULL,
      familia   TEXT    NOT NULL,
      PRIMARY KEY (modulo_id, tipo),
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
    // `ces` va en el INSERT: sin ella, las actividades de partida llegaban al
    // cuaderno sin criterios y no entraban en la nota de ningún RA — se podía
    // calificar un examen y que no moviera la calificación del módulo.
    const s = db.prepare(`
      INSERT INTO actividades (modulo_id,ut_id,ra_id,descripcion,instrumento,tipo,peso,nota_max,eval,orden,ces)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)
    `)
    actividades.forEach(a =>
      s.run(mid, a.ut_id||null, a.ra_id||null, a.descripcion, a.instrumento,
            a.tipo, a.peso, a.nota_max, a.eval, a.orden,
            JSON.stringify(Array.isArray(a.ces) ? a.ces : [])))
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

// ── Pérdida del derecho a la evaluación continua (art. 3.6) ──────────────────
const getEvaluacionContinua = moduloId => getDb().prepare(`
  SELECT e.alumno_id, e.perdida, e.motivo, e.fecha
  FROM evaluacion_continua e JOIN alumnos a ON a.id = e.alumno_id
  WHERE a.modulo_id = ?
`).all(moduloId)

/**
 * Marca o levanta la pérdida del derecho a la evaluación continua.
 *
 * Quitar la marca devuelve al alumnado a la evaluación ordinaria y recupera lo
 * calificado durante el curso, que sigue guardado: aquí no se borra nada. Lo que
 * hace el art. 3.6 es impedir que esas notas se tengan en cuenta mientras la
 * pérdida esté vigente, no eliminarlas.
 */
function setEvaluacionContinua({ alumnoId, perdida, motivo = null }) {
  const v = perdida ? 1 : 0
  getDb().prepare(`INSERT INTO evaluacion_continua (alumno_id, perdida, motivo, fecha)
    VALUES (?,?,?,datetime('now'))
    ON CONFLICT (alumno_id) DO UPDATE SET perdida=excluded.perdida,
      motivo=excluded.motivo, fecha=excluded.fecha`).run(alumnoId, v, motivo)
  return { alumnoId, perdida: v, motivo }
}

// ── Convalidación de módulos (art. 25.7 y 25.11) ─────────────────────────────
const getConvalidaciones = moduloId => getDb().prepare(`
  SELECT m.alumno_id, m.convalidado, m.nota_convalidacion
  FROM matricula m JOIN alumnos a ON a.id = m.alumno_id
  WHERE a.modulo_id = ? AND m.convalidado = 1
`).all(moduloId)

/**
 * Convalida un módulo, con nota o sin ella.
 *
 * La diferencia importa: el art. 25.11 excluye del cálculo de la calificación
 * final los convalidados **sin nota**. Con nota, computan como cualquier otro.
 */
function setConvalidacion({ alumnoId, convalidado, nota = null }) {
  const v = convalidado ? 1 : 0
  const n = (nota === null || nota === undefined || nota === '') ? null : Number(nota)
  if (n !== null && (!isFinite(n) || n < 0 || n > 10)) {
    throw new Error('La nota de convalidación tiene que estar entre 0 y 10')
  }
  getDb().prepare(`INSERT INTO matricula (alumno_id, convalidado, nota_convalidacion)
    VALUES (?,?,?)
    ON CONFLICT (alumno_id) DO UPDATE SET convalidado=excluded.convalidado,
      nota_convalidacion=excluded.nota_convalidacion`).run(alumnoId, v, n)
  return { alumnoId, convalidado: v, nota: n }
}

/**
 * Fase de formación en empresa del CE de Desarrollo de aplicaciones en Python.
 *
 * Decreto 79/2025, art. 5.3: es potestativa, «a propuesta del centro educativo»,
 * y en régimen general debe durar «entre el 20 y 35 %» de las 430 horas del
 * curso. De ahí la franja de 86 a 150 horas: el decreto fija los límites, el
 * centro elige el número.
 *
 * Las horas se reparten entre los cuatro módulos en proporción a su duración y
 * se guardan como `horas_aula`, que es lo que el motor usa para saber que un
 * módulo tiene fase de empresa. Poner 0 significa no ofertarla.
 */
const CE_PYTHON_TOTAL = 430
const CE_PYTHON_MIN = 86
const CE_PYTHON_MAX = 150

function setFaseEmpresaPython(horasEmpresa) {
  const h = Number(horasEmpresa) || 0
  if (h !== 0 && (h < CE_PYTHON_MIN || h > CE_PYTHON_MAX)) {
    throw new Error(
      `La fase de empresa del CE de Python debe estar entre ${CE_PYTHON_MIN} y ` +
      `${CE_PYTHON_MAX} horas en régimen general (Decreto 79/2025, art. 5.3), ` +
      'o 0 si no se oferta.')
  }
  const db = getDb()
  const filas = db.prepare("SELECT id, data_json FROM modulos WHERE key LIKE 'ce_python_%'").all()
  let tocados = 0
  for (const f of filas) {
    let data
    try { data = JSON.parse(f.data_json || '{}') } catch { continue }
    const m = data.modulo
    if (!m) continue
    const total = Number(m.total_horas) || 0
    // Reparto proporcional a la duración de cada módulo, redondeando al alza
    const empresa = h === 0 ? 0 : Math.round((h * total) / CE_PYTHON_TOTAL)
    m.horas_aula = h === 0 ? 0 : Math.max(1, total - empresa)
    db.prepare('UPDATE modulos SET data_json=? WHERE id=?').run(JSON.stringify(data), f.id)
    tocados++
  }
  setConfig('ce_python_horas_empresa', String(h))
  return { horas: h, modulos: tocados }
}

const getFaseEmpresaPython = () => ({
  horas: Number(getConfig('ce_python_horas_empresa') || 0),
  min: CE_PYTHON_MIN, max: CE_PYTHON_MAX, total: CE_PYTHON_TOTAL,
})

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
/**
 * Actividades del módulo. Sin filtro devuelve las dos convocatorias, porque las
 * pantallas necesitan verlo todo junto; `convocatoria` acota cuando hace falta
 * (la parrilla de la 1ª no debe enseñar la prueba de recuperación de junio).
 */
const getActividades = (moduloId, convocatoria = null) =>
  convocatoria == null
    ? getDb().prepare('SELECT * FROM actividades WHERE modulo_id=? ORDER BY convocatoria,eval,orden').all(moduloId)
    : getDb().prepare('SELECT * FROM actividades WHERE modulo_id=? AND convocatoria=? ORDER BY eval,orden')
        .all(moduloId, Number(convocatoria))

/**
 * Deja los números de una actividad dentro de lo que tiene sentido.
 *
 * Un peso negativo resta de la media en vez de sumar; una escala de 0 hace que
 * cualquier nota valga infinito al pasarla a base 10; una evaluación 99 crea una
 * columna que ninguna pantalla enseña, con notas dentro. La interfaz ya lo
 * comprueba, pero la base tiene que ser la última línea, no la única.
 */
function _saneaActividad(a) {
  const num = (v, def) => { const n = Number(v); return isFinite(n) ? n : def }
  const peso = Math.max(0, Math.min(100, num(a.peso, 0)))
  const notaMax = Math.max(0.1, Math.min(100, num(a.nota_max, 10)))
  const evalNum = Math.max(1, Math.min(3, Math.round(num(a.eval, 1))))
  return { peso, notaMax, evalNum }
}

function saveActividad(a) {
  const db = getDb()
  // `ces` llega como array desde el modal de criterios; se persiste como JSON
  const cesJson = Array.isArray(a.ces) ? JSON.stringify(a.ces) : (a.ces ?? '[]')
  const { peso, notaMax, evalNum } = _saneaActividad(a)
  // COALESCE en convocatoria: quien no la manda (todas las pantallas antiguas)
  // no debe cambiar de convocatoria una actividad por guardar su descripción.
  const conv = a.convocatoria == null ? null : Number(a.convocatoria)
  // Prueba objetiva del art. 3.6: igual que la convocatoria, COALESCE para que
  // guardar la descripción de una actividad no le quite la marca.
  const po = a.prueba_objetiva == null ? null : (a.prueba_objetiva ? 1 : 0)
  if (a.id) {
    db.prepare(`UPDATE actividades SET descripcion=?,instrumento=COALESCE(?,instrumento),
        tipo=COALESCE(?,tipo),peso=?,nota_max=?,eval=?,ut_id=?,ra_id=?,ces=?,orden=?,
        convocatoria=COALESCE(?,convocatoria),
        prueba_objetiva=COALESCE(?,prueba_objetiva) WHERE id=?`)
      .run(a.descripcion, a.instrumento ?? null, a.tipo ?? null, peso, notaMax,
           evalNum, a.ut_id??null, a.ra_id??null, cesJson, a.orden??0, conv, po, a.id)
    return a.id
  }
  return Number(db.prepare(`INSERT INTO actividades
    (modulo_id,ut_id,ra_id,descripcion,instrumento,tipo,peso,nota_max,eval,orden,ces,
     convocatoria,prueba_objetiva)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)`)
    .run(a.modulo_id,a.ut_id,a.ra_id,a.descripcion,a.instrumento,
         a.tipo,peso,notaMax,evalNum,a.orden,cesJson, conv ?? 1, po ?? 0).lastInsertRowid)
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

/**
 * Convierte a número lo que llegue como nota, admitiendo la coma decimal.
 *
 * En español se escribe «7,5». Con `parseFloat` eso valía 7: medio punto perdido
 * y sin avisar a nadie.
 */
function _numeroDeNota(v) {
  if (v === '' || v === null || v === undefined) return null
  const t = String(v).trim()
  return parseFloat(t.includes(',') && !t.includes('.') ? t.replace(',', '.') : t)
}

function saveNota(alumnoId, actividadId, nota) {
  const val = _numeroDeNota(nota)
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
  const val = _numeroDeNota(notaRec)
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
  // Una ponderación de 1000 o de «mucho» descuadra la media de todo el módulo.
  const n = Number(pond)
  const limpia = isFinite(n) ? Math.max(0, Math.min(100, n)) : 0
  getDb().prepare(`
    INSERT INTO ra_ponderaciones (modulo_id, ra_id, pond) VALUES (?,?,?)
    ON CONFLICT (modulo_id, ra_id) DO UPDATE SET pond=excluded.pond
  `).run(moduloId, raId, limpia)
}

// ── RF-01 · Estado de impartición del RA ──────────────────────────────────────

const ESTADOS_RA = ['previsto', 'impartido', 'no_impartido']

/** { raId: { estado, motivo, fecha } } de un módulo. */
function getRaEstados(moduloId) {
  const filas = getDb()
    .prepare('SELECT ra_id, estado, motivo, fecha FROM ra_estado WHERE modulo_id=?')
    .all(moduloId)
  const out = {}
  for (const f of filas) out[f.ra_id] = { estado: f.estado, motivo: f.motivo, fecha: f.fecha }
  return out
}

/**
 * Fija el estado de impartición de un RA.
 *
 * Marcar «no impartido» exige motivo: es lo que hace defendible que ese RA no
 * compute. Sin motivo se rechaza, porque un RA que desaparece de la calificación
 * sin explicación es exactamente el problema que RF-01 viene a corregir.
 */
function setRaEstado(moduloId, raId, estado, motivo) {
  if (!ESTADOS_RA.includes(estado)) {
    throw new Error(`Estado de RA no válido: ${estado}`)
  }
  const txt = (motivo == null ? '' : String(motivo)).trim()
  if (estado === 'no_impartido' && !txt) {
    throw new Error('Marcar un RA como no impartido exige indicar el motivo.')
  }
  getDb().prepare(`
    INSERT INTO ra_estado (modulo_id, ra_id, estado, motivo, fecha)
    VALUES (?,?,?,?,date('now'))
    ON CONFLICT (modulo_id, ra_id) DO UPDATE SET
      estado = excluded.estado,
      motivo = excluded.motivo,
      fecha  = excluded.fecha
  `).run(moduloId, raId, estado, estado === 'no_impartido' ? txt : (txt || null))
}

// ── Modulo data_json (edición UT/RA/CE) ───────────────────────────────────────

/**
 * Guarda la programación y deja las actividades en consonancia con ella.
 *
 * Al quitar un criterio o un RA de la programación, las actividades seguían
 * apuntando a lo que ya no existía:
 *
 *  · un criterio fantasma se quedaba marcado en la actividad, invisible, y
 *    reaparecía solo si alguien volvía a crear un criterio con ese mismo id;
 *  · una actividad cuyo RA desaparecía se quedaba sin calificar nada, pero
 *    seguía en la parrilla con sus notas puestas: quien las metió da por hecho
 *    que cuentan, y no cuentan.
 *
 * Lo primero se limpia sin más, que no se pierde nada. Lo segundo no se puede
 * arreglar solo —hay notas de por medio—, así que se devuelve para que la
 * pantalla lo diga.
 *
 * @returns {{criteriosLimpiados: number, cierresRetirados: number,
 *            huerfanas: Array<{id:number, descripcion:string, ra_id:string}>}}
 */
function setModuloDataJson(id, dataJson) {
  const db = getDb()
  db.prepare('UPDATE modulos SET data_json=? WHERE id=?').run(JSON.stringify(dataJson), id)

  const data = dataJson && typeof dataJson === 'object' ? dataJson : {}
  const raIds = new Set((data.ras || []).map(r => String(r.id)))
  const validas = new Set()
  for (const [ra, lst] of Object.entries(data.ces || {})) {
    for (const ce of lst || []) validas.add(`${ra}|${ce.id}`)
  }

  let criteriosLimpiados = 0
  const huerfanas = []

  // Los cierres de evaluación de un RA que ya no existe no sirven para nada, y
  // si algún día se vuelve a crear un RA con ese mismo identificador reviven:
  // el RA nuevo nacería congelado con una nota antigua que nadie recuerda haber
  // puesto. Se retiran, y se cuentan para poder decirlo.
  let cierresRetirados = 0
  if (raIds.size) {
    const marcador = [...raIds].map(() => '?').join(',')
    const alumnos = db.prepare('SELECT id FROM alumnos WHERE modulo_id=?').all(id).map(a => a.id)
    if (alumnos.length) {
      const inAl = alumnos.map(() => '?').join(',')
      const cuantos = db.prepare(
        `SELECT COUNT(*) AS n FROM ra_superados WHERE alumno_id IN (${inAl}) AND ra_id NOT IN (${marcador})`
      ).get(...alumnos, ...raIds)
      cierresRetirados = cuantos ? cuantos.n : 0
      if (cierresRetirados) {
        db.prepare(
          `DELETE FROM ra_superados WHERE alumno_id IN (${inAl}) AND ra_id NOT IN (${marcador})`
        ).run(...alumnos, ...raIds)
      }
    }
  }
  const acts = db.prepare('SELECT id, ra_id, descripcion, ces FROM actividades WHERE modulo_id=?').all(id)
  const upd = db.prepare('UPDATE actividades SET ces=? WHERE id=?')
  for (const a of acts) {
    let lista = []
    try { lista = JSON.parse(a.ces || '[]') } catch { lista = [] }
    if (Array.isArray(lista) && lista.length) {
      // Solo se tocan las claves compuestas RA|CE: un id suelto es de una base
      // antigua y lo resuelve su propia migración.
      const limpia = lista.filter(k => !String(k).includes('|') || validas.has(String(k)))
      if (limpia.length !== lista.length) {
        criteriosLimpiados += lista.length - limpia.length
        upd.run(JSON.stringify(limpia), a.id)
      }
    }
    if (a.ra_id && !raIds.has(String(a.ra_id))) {
      huerfanas.push({ id: a.id, descripcion: a.descripcion, ra_id: a.ra_id })
    }
  }
  if (criteriosLimpiados) {
    console.log(`[db] ${criteriosLimpiados} criterio(s) que ya no existen, quitados de las actividades.`)
  }
  if (cierresRetirados) {
    console.log(`[db] ${cierresRetirados} cierre(s) de evaluación de resultados que ya no existen, retirados.`)
  }
  return { criteriosLimpiados, huerfanas, cierresRetirados }
}

const deleteActividad = id => getDb().prepare('DELETE FROM actividades WHERE id=?').run(id)

// ── Config ─────────────────────────────────────────────────────────────────────
const getConfig  = key  => getDb().prepare('SELECT value FROM config WHERE key=?').get(key)?.value ?? null
const setConfig  = (k,v) => getDb().prepare('INSERT OR REPLACE INTO config VALUES(?,?)').run(k,v)
const deleteConfig = key => getDb().prepare('DELETE FROM config WHERE key=?').run(key)
const getAllConfig = ()  => Object.fromEntries(getDb().prepare('SELECT key,value FROM config').all().map(r=>[r.key,r.value]))

/**
 * SOLO PARA TESTS. Da la conexión cruda —lectura y escritura, sin pasar por
 * ninguna de las funciones de arriba—, que es lo que necesitan los tests de
 * `migrarProgramacionNormalizada()` para corromper una fila a mano (§2 de la
 * migración) o para forzar un INSERT que debe violar una clave foránea
 * compuesta (`actividad_ce`, §1). Una función de solo lectura no habría
 * bastado para esos dos casos.
 *
 * Nunca se importa desde main.js, preload.js ni el renderer: ninguno de esos
 * necesita SQL crudo, todos pasan por las funciones validadas de este
 * fichero. Para que un despiste no lo use fuera de un test, se niega a
 * devolver nada si `VITEST` no está activo (lo pone Vitest solo, no hay que
 * configurarlo).
 */
function TEST_ONLY_rawDb() {
  if (!process.env.VITEST) {
    throw new Error('TEST_ONLY_rawDb() solo puede llamarse desde los tests (VITEST no está activo)')
  }
  return getDb()
}

module.exports = {
  getModulos, getModulosArchivados, restaurarModulo, addModulo, deleteModulo, setModuloDataJson,
  getAlumnos, saveAlumno, deleteAlumno,
  getActividades, saveActividad, deleteActividad,
  getNotasGrid, saveNota, saveNotaRec, closeDb, backupTo,
  getRaPonderaciones, setRaPonderacion,
  getRaEstados, setRaEstado,
  getCalificacionesCE, setCalificacionCE,
  getRasSuperados, cerrarEvaluacionRAs, reabrirRaSuperado,
  getFaseEmpresa, setFaseEmpresa,
  getEvaluacionContinua, setEvaluacionContinua,
  getConvalidaciones, setConvalidacion,
  getFaseEmpresaPython, setFaseEmpresaPython,
  getEvidencias, addEvidencia,
  getMatriculas, setMatricula,
  getConfig, setConfig, deleteConfig, getAllConfig,
  // RF-02 · programación normalizada (docs/rediseno/05-PLAN-MIGRACION.md)
  migrarProgramacionNormalizada,
  getRaCatalogo, setRaCatalogoPond, setRaCatalogoLlave, setRaCatalogoDual,
  getCeCatalogo, setCeCatalogoPeso,
  getCeInstrumentosPrevistos, setCeInstrumentos, setRaInstrumentos,
  // RF-17 · tipos de actividad y familia de reparto
  getTipoFamilia, setTipoFamilia,
  // RF-02 · unidades de trabajo normalizadas (segunda parte)
  getUnidadesTrabajo, setUnidadTrabajo, deleteUnidadTrabajo,
  getUtCe, getUtCeModulo, setUtCe,
  getActividadCe, getActividadCeModulo, setActividadCe,
  TEST_ONLY_rawDb,
}

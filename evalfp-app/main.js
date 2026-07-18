'use strict'
const { app, BrowserWindow, ipcMain, shell } = require('electron')
const path   = require('path')
const { spawn } = require('child_process')
const fs     = require('fs')
const os     = require('os')
const Database = require('better-sqlite3')
const schedule = require('node-schedule')
const logger = require('./main/logger')

// ── Modo test E2E (EVALFP_TEST=1) ────────────────────────────────────────────
// userData aislado en un directorio temporal por proceso: los tests e2e nunca
// tocan la base de datos real del profesor ni generan backups.
const IS_E2E = process.env.EVALFP_TEST === '1'
if (IS_E2E) {
  const testDir = path.join(os.tmpdir(), `evalfp-e2e-${process.pid}`)
  fs.mkdirSync(testDir, { recursive: true })
  app.setPath('userData', testDir)
}

// ── Lazy Load Keytar (Safe Mode) ───────────────────────────────────────────
// Keytar is loaded lazily when needed, preventing app crash if module is broken
let keytarSafe = null
let keytarReady = false

async function getKeytarSafe() {
  if (keytarSafe) return keytarSafe
  
  try {
    keytarSafe = require('./main/keytar-safe')
    const success = await keytarSafe.initialize()
    keytarReady = success
    logger.logEvent('KEYTAR_INIT_COMPLETE', { 
      status: success ? 'available' : 'unavailable',
      mode: success ? 'native' : 'database_fallback'
    })
    return keytarSafe
  } catch (err) {
    logger.logEvent('KEYTAR_INIT_ERROR', { message: err.message })
    keytarReady = false
    // Return null on error - caller will handle fallback
    return null
  }
}

// ── Central Error Handler & Audit Logging ─────────────────────────────────
function handleError(error, context = '') {
  const sanitizedMessage = error.message
    .replace(/password/gi, '****')
    .replace(/token/gi, '****')
    .replace(/key/gi, '****')
    .replace(/secret/gi, '****')
  
  logger.logError(`[${context}] ${sanitizedMessage}`, error)
  
  // Map technical errors to user-friendly messages
  if (error.message.includes('ENOENT')) {
    return { success: false, message: 'File not found' }
  }
  if (error.message.includes('EACCES')) {
    return { success: false, message: 'Permission denied' }
  }
  if (error.message.includes('SQLITE')) {
    return { success: false, message: 'Database error' }
  }
  if (error.message.includes('timeout')) {
    return { success: false, message: 'Operation timed out' }
  }
  
  return { success: false, message: 'An error occurred' }
}

// Audit log for sensitive operations
function auditLog(operation, userId = 'system', data = {}) {
  logger.logEvent(`AUDIT_${operation}`, {
    timestamp: new Date().toISOString(),
    user: userId,
    ...data
  })
}

// ── Global Error Handlers ──────────────────────────────────────────────────
process.on('uncaughtException', (error) => {
  logger.logError('UNCAUGHT_EXCEPTION', error)
  console.error('Uncaught Exception:', error)
})

process.on('unhandledRejection', (reason, promise) => {
  logger.logError('UNHANDLED_REJECTION', new Error(reason))
  console.error('Unhandled Rejection at:', promise, 'reason:', reason)
})

const scriptsDir = () => app.isPackaged
  ? path.join(process.resourcesPath, 'scripts')
  : path.join(__dirname, '..', 'scripts')

// JSON pre-horneado con todos los módulos (generado por prebake_modules.py)
const modulesDataPath = () => path.join(__dirname, 'renderer', 'modules_data.json')

const outputDir = () => path.join(os.homedir(), 'Documents', 'EvalFP')
const python    = () => process.platform === 'win32' ? 'python' : 'python3'

// ── Secure API Key Storage with keytar (or database fallback) ──────────────────────
async function loadApiKeysFromSecureStorage() {
  try {
    let openaiKey = ''
    let anthropicKey = ''
    const ks = await getKeytarSafe()
    
    if (ks && ks.isAvailable()) {
      // Primary: Use keytar for secure OS-level storage
      try {
        openaiKey = await ks.getPassword('EvalFP', 'openai_api_key') || ''
        anthropicKey = await ks.getPassword('EvalFP', 'anthropic_api_key') || ''
        if (openaiKey || anthropicKey) {
          logger.logEvent('API_KEYS_LOADED_FROM_KEYTAR', { source: 'keytar' })
        }
      } catch (keytarErr) {
        logger.logEvent('KEYTAR_READ_FAILED', { message: keytarErr.message })
      }
    }
    
    // Always try database as fallback (or if keytar not available)
    if (!openaiKey || !anthropicKey) {
      logger.logEvent('LOADING_API_KEYS_FROM_DATABASE', { 
        keytar_available: ks && ks.isAvailable(),
        source: 'database'
      })
      try {
        // Usar el módulo db (que inicializa el schema) en lugar de abrir una
        // conexión raw a una ruta distinta que no tendría la tabla cfg creada.
        const cfg = db.getCfgKeys()
        if (cfg) {
          if (!openaiKey) openaiKey = cfg.openaiKey || ''
          if (!anthropicKey) anthropicKey = cfg.anthropicKey || ''
          logger.logEvent('API_KEYS_LOADED_FROM_DATABASE_SUCCESS', {
            hasOpenAI: !!openaiKey,
            hasAnthropic: !!anthropicKey
          })
        }
      } catch (dbErr) {
        logger.logError('Failed to load API keys from database', dbErr)
      }
    }
    
    if (openaiKey) process.env.OPENAI_API_KEY = openaiKey
    if (anthropicKey) process.env.ANTHROPIC_API_KEY = anthropicKey
    
    logger.logEvent('API_KEYS_LOADED_TO_ENV', { 
      hasOpenAI: !!openaiKey, 
      hasAnthropic: !!anthropicKey,
      source: (ks && ks.isAvailable()) ? 'keytar_or_db' : 'database_only'
    })
  } catch (e) {
    logger.logError('Failed to load API keys from secure storage', e)
  }
}

// ── Automatic Database Backups ────────────────────────────────────────────────
const backupsDir = () => path.join(os.homedir(), 'Documents', 'EvalFP', 'backups')
const dbPath = () => path.join(os.homedir(), 'Documents', 'EvalFP', 'evalfp.db')

function setupBackups() {
  if (IS_E2E) return   // sin backups en modo test: la BD es temporal
  try {
    // Crear directorio de backups si no existe
    fs.mkdirSync(backupsDir(), { recursive: true })
    
    // Ejecutar backup diario a las 2 AM
    schedule.scheduleJob('0 2 * * *', async () => {
      logger.logEvent('AUTOMATIC_BACKUP_STARTED')
      try {
        await performBackup()
        await cleanOldBackups()
      } catch (e) {
        logger.logError('Automatic backup failed', e)
      }
    })
    
    // También ejecutar backup al cierre (graceful shutdown)
    process.on('SIGINT', async () => {
      logger.logEvent('GRACEFUL_SHUTDOWN', { message: 'Final backup before closing' })
      try {
        await performBackup()
      } catch (e) {
        logger.logError('Error in final backup', e)
      }
      process.exit(0)
    })
    
    logger.info('Automatic backups initialized', { schedule: 'daily at 2 AM' })
  } catch (e) {
    logger.logError('Error initializing backups', e)
  }
}

async function performBackup() {
  try {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
    const dest = path.join(backupsDir(), `evalfp_${timestamp}.db`)
    // Usar la API backup() de better-sqlite3: copia online y segura aunque
    // haya transacciones activas (WAL mode). Evita copias inconsistentes.
    await db.backup(dest)
    logger.info('Backup created', { filename: path.basename(dest) })
    return dest
  } catch (e) {
    throw new Error(`Failed to create backup: ${e.message}`)
  }
}

async function cleanOldBackups() {
  try {
    const files = fs.readdirSync(backupsDir())
      .filter(f => f.startsWith('evalfp_') && f.endsWith('.db'))
      .map(f => ({
        name: f,
        path: path.join(backupsDir(), f),
        time: fs.statSync(path.join(backupsDir(), f)).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time) // Newest first
    
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000)
    let deleted = 0
    
    for (const file of files) {
      if (file.time < thirtyDaysAgo) {
        fs.unlinkSync(file.path)
        deleted++
        logger.debug(`Old backup deleted: ${file.name}`)
      }
    }
    
    if (deleted > 0) {
      logger.info('Backup cleanup completed', { backupsDeleted: deleted })
    }
  } catch (e) {
    logger.logError('Error cleaning old backups', e)
  }
}

// Cache en memoria del JSON de módulos
let _modulesData = null
function getModulesData() {
  if (!_modulesData) {
    const raw = fs.readFileSync(modulesDataPath(), 'utf8')
    _modulesData = JSON.parse(raw)
  }
  return _modulesData
}

// ── Ventana ───────────────────────────────────────────────────────────────────
let win
function createWindow() {
  win = new BrowserWindow({
    width: 1280, height: 800, minWidth: 960, minHeight: 640,
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#0f1b2d',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'))
}

app.whenReady().then(async () => {
  await loadApiKeysFromSecureStorage()
  setupBackups()
  createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })

// Backup final al cerrar la app (Cmd+Q, cerrar ventana, etc.)
// SIGINT ya tiene su propio handler en setupBackups(); before-quit cubre el resto.
app.on('before-quit', async (e) => {
  e.preventDefault()
  try {
    await performBackup()
    logger.logEvent('SHUTDOWN_BACKUP_OK')
  } catch (err) {
    logger.logError('Shutdown backup failed', err)
  }
  app.exit(0)
})

// ── Helper Python ─────────────────────────────────────────────────────────────
function runPython(event, scriptName, args, replyChannel, onFinish) {
  const sd  = scriptsDir()
  const env = { ...process.env, PYTHONPATH: sd }
  fs.mkdirSync(outputDir(), { recursive: true })
  const proc = spawn(python(), [path.join(sd, scriptName), ...args], { cwd: sd, env })
  proc.stdout.on('data', d => event.reply(replyChannel, { type:'stdout', text:d.toString() }))
  proc.stderr.on('data', d => event.reply(replyChannel, { type:'stderr', text:d.toString() }))
  proc.on('close', code => { if (onFinish) onFinish(); event.reply(replyChannel, { type:'done', code }) })
  proc.on('error', err  => { if (onFinish) onFinish(); event.reply(replyChannel, { type:'error', text:err.message }) })
}

function runPythonSync(scriptName, args) {
  const sd  = scriptsDir()
  const env = { ...process.env, PYTHONPATH: sd }
  const result = require('child_process').spawnSync(
    python(), [path.join(sd, scriptName), ...args], { cwd: sd, env, encoding: 'utf8' }
  )
  if (result.error) throw result.error
  return result.stdout
}

// ── IPC: Módulos ──────────────────────────────────────────────────────────────
const db = require('./db')

ipcMain.handle('db:getModulos', () => db.getModulos())

ipcMain.handle('db:listModulosDisponibles', () => {
  return getModulesData().index
})

ipcMain.handle('db:getModuloData', (_, key) => {
  const data = getModulesData().modules[key]
  if (!data) throw new Error(`Módulo no encontrado: ${key}`)
  return data
})

ipcMain.handle('db:addModulo', (_, payload) => db.addModulo(payload))
ipcMain.handle('db:deleteModulo', (_, id) => db.deleteModulo(id))

// ── IPC: API Keys (Secure Storage with Fallback) ────────────────────────────
ipcMain.handle('api:saveKeys', async (_, keys) => {
  try {
    let saved = false
    const ks = await getKeytarSafe()
    
    // Try keytar first if available
    if (ks && ks.isAvailable()) {
      try {
        if (keys.openai) {
          await ks.setPassword('EvalFP', 'openai_api_key', keys.openai)
          process.env.OPENAI_API_KEY = keys.openai
        }
        if (keys.anthropic) {
          await ks.setPassword('EvalFP', 'anthropic_api_key', keys.anthropic)
          process.env.ANTHROPIC_API_KEY = keys.anthropic
        }
        logger.logEvent('API_KEYS_SAVED_TO_KEYTAR', { source: 'keytar' })
        saved = true
      } catch (keytarErr) {
        logger.logEvent('KEYTAR_WRITE_FAILED', { message: keytarErr.message })
        // Fall through to database
      }
    }
    
    // Save to database as backup or primary storage
    if (!saved) {
      logger.logEvent('SAVING_API_KEYS_TO_DATABASE', {
        keytar_available: ks && ks.isAvailable(),
        source: 'database'
      })
      try {
        // Usar db.setCfgKey (módulo db con schema inicializado) en lugar de
        // abrir una conexión raw a ~/Documents/EvalFP/evalfp.db (ruta distinta,
        // sin schema → "no such table: cfg").
        if (keys.openai) {
          db.setCfgKey('openaiKey', keys.openai)
          process.env.OPENAI_API_KEY = keys.openai
        }
        if (keys.anthropic) {
          db.setCfgKey('anthropicKey', keys.anthropic)
          process.env.ANTHROPIC_API_KEY = keys.anthropic
        }
        logger.logEvent('API_KEYS_SAVED_TO_DATABASE', { success: true })
        saved = true
      } catch (dbErr) {
        logger.logError('Failed to save API keys to database', dbErr)
      }
    }
    
    return { 
      success: saved, 
      message: saved 
        ? ((ks && ks.isAvailable()) ? 'Keys saved securely' : 'Keys saved to database')
        : 'Failed to save keys'
    }
  } catch (e) {
    logger.logError('Error saving API keys', e)
    return { success: false, error: e.message }
  }
})

// ── IPC: Alumnos ──────────────────────────────────────────────────────────────
ipcMain.handle('db:getAlumnos',    (_, mid)  => db.getAlumnos(mid))
ipcMain.handle('db:saveAlumno',    (_, a)    => db.saveAlumno(a))
ipcMain.handle('db:deleteAlumno',  (_, id)   => db.deleteAlumno(id))

// ── IPC: Actividades ──────────────────────────────────────────────────────────
ipcMain.handle('db:getActividades',   (_, mid)  => db.getActividades(mid))
ipcMain.handle('db:saveActividad',    (_, a)    => db.saveActividad(a))
ipcMain.handle('db:deleteActividad',  (_, id)   => db.deleteActividad(id))

// ── IPC: Notas ────────────────────────────────────────────────────────────────
ipcMain.handle('db:getNotasGrid',  (_, mid)             => db.getNotasGrid(mid))
ipcMain.handle('db:saveNota',      (_, aid, actId, nota) => db.saveNota(aid, actId, nota))
ipcMain.handle('db:saveNotaRec',   (_, aid, actId, nota) => db.saveNotaRec(aid, actId, nota))

// ── IPC: Ponderaciones RA ─────────────────────────────────────────────────────
ipcMain.handle('db:getRaPonderaciones',  (_, mid)             => db.getRaPonderaciones(mid))
ipcMain.handle('db:setRaPonderacion',    (_, mid, raId, pond) => db.setRaPonderacion(mid, raId, pond))
ipcMain.handle('db:setModuloDataJson',   (_, id, data)        => db.setModuloDataJson(id, data))

// ── IPC: Config ───────────────────────────────────────────────────────────────
ipcMain.handle('db:getAllConfig', () => {
  const cfg = db.getAllConfig()
  // Añadir indicadores de presencia de keys SIN revelar los valores
  cfg.hasOpenAI    = !!process.env.OPENAI_API_KEY
  cfg.hasAnthropic = !!process.env.ANTHROPIC_API_KEY
  // Eliminar valores sensibles del objeto devuelto al renderer
  delete cfg.openaiKey
  delete cfg.anthropicKey
  return cfg
})
ipcMain.handle('db:setConfig',   (_, k, v) => {
  // No permitir guardar API keys en texto plano via setConfig
  if (k === 'openaiKey' || k === 'anthropicKey') return
  db.setConfig(k, v)
})

// ── Sanitización de argumentos para spawn ─────────────────────────────────────
// spawn() no ejecuta shell, pero sanitizamos igualmente para prevenir
// path traversal y caracteres nulos que pueden truncar la cadena en C.
function _sanitizeArg(value, maxLen = 500) {
  if (value === null || value === undefined) return null
  return String(value)
    .slice(0, maxLen)
    .replace(/[\0\r\n]/g, '')   // strip null bytes y saltos de línea
}

const VALID_IA_COMMANDS    = new Set(['rubrica', 'actividad', 'informe', 'todo'])
// El script ai_asistente.py acepta: auto | claude | openai | demo
const VALID_IA_PROVEEDORES = new Set(['auto', 'claude', 'openai', 'demo'])

// ── Helper: aviso si no hay API key configurada ───────────────────────────────
function _warnNoApiKey(event, replyChannel) {
  const hasAnthropic = !!process.env.ANTHROPIC_API_KEY
  const hasOpenAI    = !!process.env.OPENAI_API_KEY
  if (!hasAnthropic && !hasOpenAI) {
    event.reply(replyChannel, {
      type: 'stderr',
      text: '⚠️  SIN API KEY CONFIGURADA — El contenido generado será texto de ejemplo (modo DEMO).\n' +
            '   Ve a Ajustes → Integraciones IA y configura tu clave de Anthropic o OpenAI para obtener contenido real.'
    })
    return true  // sin clave
  }
  return false  // hay clave
}

// ── IPC: IA + Apuntes ─────────────────────────────────────────────────────────
// Carpeta única de material generado por IA, organizada en subcarpetas:
//   Material IA/<ABREV>/{rubricas,actividades,informes,apuntes}/
const materialDir = () => path.join(outputDir(), 'Material IA')

/**
 * Exporta la programación REAL del módulo desde SQLite a un JSON temporal
 * (RAs con ponderaciones editadas, UTs, CEs con texto, plan de actividades)
 * para que los scripts de IA trabajen con datos rigurosos, no con la
 * plantilla estática. Devuelve { tmpDatos, abrev } (tmpDatos null si falla).
 */
function _exportModuloJson(moduloKey) {
  const mod = db.getModulos().find(m => m.key === moduloKey)
  if (!mod) return { tmpDatos: null, abrev: null }
  const dataJson = typeof mod.data_json === 'string'
    ? JSON.parse(mod.data_json) : (mod.data_json || {})
  // Ponderaciones de RA editadas por el profesor (override de la plantilla)
  const ponds = {}
  try { db.getRaPonderaciones(mod.id).forEach(r => { ponds[r.ra_id] = r.pond }) } catch { /* sin overrides */ }
  const modData = {
    key: mod.key, abrev: mod.abrev, nombre: mod.nombre,
    ciclo: mod.ciclo || '', curso: mod.curso || '', anno: mod.anno || '',
    grupo: mod.grupo || '', horas: mod.horas || 0, decreto: mod.decreto || '',
    uts: dataJson.uts || [],
    ras: (dataJson.ras || []).map(r => ({ ...r, pond: ponds[r.id] !== undefined ? ponds[r.id] : r.pond })),
    ces: dataJson.ces || {},
    asignaciones: dataJson.asignaciones || [],
    eval_ras: dataJson.eval_ras || {},
    actividades: db.getActividades(mod.id) || [],
    minexam: db.getConfig(`minexam_${mod.id}`) || null,
  }
  const tmpDatos = path.join(os.tmpdir(), `evalfp_ia_${Date.now()}.json`)
  fs.writeFileSync(tmpDatos, JSON.stringify(modData), 'utf8')
  return { tmpDatos, abrev: mod.abrev }
}

const _safeDirName = s => String(s || 'modulo').replace(/[^\wÁÉÍÓÚÑáéíóúñüÜ. -]/g, '_').trim() || 'modulo'

ipcMain.on('gen-ia', (event, { comando, modulo, ra, n, alumno, notas, proveedor }) => {
  // Validar comando
  if (!VALID_IA_COMMANDS.has(comando)) {
    event.reply('gen-ia-reply', { type: 'error', text: 'Comando IA inválido' })
    return
  }
  if (proveedor !== 'demo') _warnNoApiKey(event, 'gen-ia-reply')

  const safeModulo = _sanitizeArg(modulo) || 'modulo'

  // Programación real desde SQLite → JSON temporal (--datos)
  let tmpDatos = null, abrev = null
  try {
    ;({ tmpDatos, abrev } = _exportModuloJson(modulo))
  } catch (e) {
    event.reply('gen-ia-reply', { type: 'stderr', text: `⚠️  No se pudo exportar la programación del módulo: ${e.message}\n(Se usará la plantilla estática.)` })
  }

  const salida = path.join(materialDir(), _safeDirName(abrev || safeModulo.replace(/_data$/, '').toUpperCase()))
  fs.mkdirSync(salida, { recursive: true })

  const args = [comando, '--salida', salida]
  if (tmpDatos)      args.push('--datos',  tmpDatos)
  else if (modulo)   args.push('--modulo', safeModulo)
  if (ra)        args.push('--ra',        _sanitizeArg(ra))
  if (n)         args.push('--n',         String(Math.max(1, Math.min(10, parseInt(n) || 3))))
  if (alumno)    args.push('--alumno',    _sanitizeArg(alumno))
  if (notas)     args.push('--notas',     _sanitizeArg(notas, 2000))
  if (proveedor && VALID_IA_PROVEEDORES.has(proveedor)) args.push('--proveedor', proveedor)

  runPython(event, 'ai_asistente.py', args, 'gen-ia-reply', () => {
    if (tmpDatos) { try { fs.unlinkSync(tmpDatos) } catch { /* ya no existe */ } }
  })
})

ipcMain.on('open-material', () => {
  fs.mkdirSync(materialDir(), { recursive: true })
  shell.openPath(materialDir())
})

ipcMain.on('gen-apuntes', (event, { modulo, ut, proveedor }) => {
  if (proveedor !== 'demo') _warnNoApiKey(event, 'gen-apuntes-reply')

  // Serializar datos reales del módulo desde SQLite → JSON temporal para Python
  let tmpDatos = null, abrev = null
  try {
    ;({ tmpDatos, abrev } = _exportModuloJson(modulo))
  } catch (e) {
    event.reply('gen-apuntes-reply', { type: 'stderr', text: `⚠️  Error cargando módulo desde BD: ${e.message}` })
  }

  // Carpeta unificada: Material IA/<ABREV>/apuntes/
  const salida = path.join(materialDir(),
    _safeDirName(abrev || String(modulo || '').replace(/_data$/, '').toUpperCase()), 'apuntes')
  fs.mkdirSync(salida, { recursive: true })

  const args = ['--salida', salida]
  if (tmpDatos)      args.push('--datos',     tmpDatos)           // datos reales SQLite
  else if (modulo)   args.push('--modulo',    _sanitizeArg(modulo)) // fallback legado
  if (ut)            args.push('--ut',        _sanitizeArg(ut))
  if (proveedor && VALID_IA_PROVEEDORES.has(proveedor)) args.push('--proveedor', proveedor)

  // Limpiar el JSON temporal al terminar (éxito o error)
  const sd  = scriptsDir()
  const env = { ...process.env, PYTHONPATH: sd }
  fs.mkdirSync(outputDir(), { recursive: true })
  const proc = spawn(python(), [path.join(sd, 'build_apuntes.py'), ...args], { cwd: sd, env })
  proc.stdout.on('data', d => event.reply('gen-apuntes-reply', { type:'stdout', text:d.toString() }))
  proc.stderr.on('data', d => event.reply('gen-apuntes-reply', { type:'stderr', text:d.toString() }))
  proc.on('close', code => {
    if (tmpDatos) { try { fs.unlinkSync(tmpDatos) } catch(_) { /* ya no existe */ } }
    event.reply('gen-apuntes-reply', { type:'done', code })
  })
  proc.on('error', err => {
    if (tmpDatos) { try { fs.unlinkSync(tmpDatos) } catch(_) { /* ya no existe */ } }
    event.reply('gen-apuntes-reply', { type:'error', text:err.message })
  })
})

ipcMain.on('open-output', () => shell.openPath(outputDir()))

// ── IPC: PDF Boletín ──────────────────────────────────────────────────────────
ipcMain.handle('pdf:exportBoletin', async (_, htmlContent, alumnoNombre) => {
  const od  = path.join(outputDir(), 'boletines')
  fs.mkdirSync(od, { recursive: true })
  const safeNombre = (alumnoNombre || 'alumno').slice(0, 50).replace(/[^a-zA-Z0-9]/g, '_')
  const filename = `boletin_${safeNombre}_${Date.now()}.pdf`
  const outPath  = path.join(od, filename)
  // Crear ventana oculta para imprimir
  const pdfWin = new BrowserWindow({ show: false, webPreferences: { offscreen: true } })
  await pdfWin.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(htmlContent)}`)
  const pdfData = await pdfWin.webContents.printToPDF({ printBackground: true, pageSize: 'A4' })
  pdfWin.close()
  fs.writeFileSync(outPath, pdfData)
  shell.openPath(outPath)
  return outPath
})

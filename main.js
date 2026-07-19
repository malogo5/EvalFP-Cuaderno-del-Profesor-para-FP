// SPDX-License-Identifier: GPL-3.0-or-later
'use strict'
const { app, BrowserWindow, ipcMain, shell } = require('electron')
const path   = require('path')
const { spawn, spawnSync } = require('child_process')
const fs     = require('fs')
const os     = require('os')
const pkg    = require('./package.json')
const schedule = require('node-schedule')
const logger = require('./main/logger')
const keytarSafe = require('./main/keytar-safe')
const db = require('./db')

// Los tests E2E nunca deben usar la base de datos real del profesor.
if (process.env.EVALFP_TEST === '1') {
  app.setPath('userData', path.join(os.tmpdir(), `evalfp-test-${process.pid}`))
}

// ── Initialize Keytar (Safe Mode) ──────────────────────────────────────────
// Keytar is optional. Initialize it but don't crash if unavailable.
async function initializeKeytar() {
  try {
    const success = await keytarSafe.initialize()
    logger.logEvent('KEYTAR_INIT_COMPLETE', { 
      status: success ? 'available' : 'unavailable',
      mode: success ? 'native' : 'database_fallback'
    })
    return success
  } catch (err) {
    logger.logEvent('KEYTAR_INIT_ERROR', { message: err.message })
    return false
  }
}

const keytarInitialization = initializeKeytar().catch(err => {
  logger.logError('Failed to initialize keytar', err)
  return false
})

// ── Rutas ─────────────────────────────────────────────────────────────────────
const scriptsDir = () => app.isPackaged
  ? path.join(process.resourcesPath, 'scripts')
  : path.join(__dirname, 'scripts')

// JSON pre-horneado con todos los módulos (generado por prebake_modules.py)
const modulesDataPath = () => path.join(__dirname, 'renderer', 'modules_data.json')

const outputDir = () => path.join(os.homedir(), 'Documents', 'EvalFP')
const materialDir = () => path.join(outputDir(), 'Material IA')
const python    = () => process.platform === 'win32' ? 'python' : 'python3'

// ── Secure API Key Storage with keytar (or database fallback) ──────────────────────
async function loadApiKeysFromSecureStorage() {
  try {
    let openaiKey = ''
    let anthropicKey = ''
    
    if (keytarSafe.isAvailable()) {
      // Primary: Use keytar for secure OS-level storage
      try {
        openaiKey = await keytarSafe.getPassword('EvalFP', 'openai_api_key') || ''
        anthropicKey = await keytarSafe.getPassword('EvalFP', 'anthropic_api_key') || ''
        if (openaiKey || anthropicKey) {
          logger.logEvent('API_KEYS_LOADED_FROM_KEYTAR', { source: 'keytar' })
        }
      } catch (keytarErr) {
        logger.logEvent('KEYTAR_READ_FAILED', { message: keytarErr.message })
      }
    }
    
    // No se almacenan claves en SQLite: un fichero local no ofrece el nivel de
    // protección del llavero del sistema operativo.
    if (!openaiKey || !anthropicKey) {
      logger.logEvent('API_KEYS_NOT_AVAILABLE', {
        hasKeytar: keytarSafe.isAvailable()
      })
    }
    
    if (openaiKey) process.env.OPENAI_API_KEY = openaiKey
    if (anthropicKey) process.env.ANTHROPIC_API_KEY = anthropicKey
    
    logger.logEvent('API_KEYS_LOADED_TO_ENV', { 
      hasOpenAI: !!openaiKey, 
      hasAnthropic: !!anthropicKey,
      source: keytarSafe.isAvailable() ? 'keytar_or_db' : 'database_only'
    })
  } catch (e) {
    logger.logError('Failed to load API keys from secure storage', e)
  }
}

const SENSITIVE_CONFIG_KEYS = new Set(['openaiKey', 'anthropicKey'])
const SAFE_CONFIG_KEY = /^(proveedor|theme|sidebarWidth|aboutSeenVersion|minexam_\d+|pardones_\d+|rec2notas_\d+|recmigra_avisado_\d+)$/
const PROVIDERS = new Set(['auto', 'claude', 'openai', 'demo'])

function assertSafeConfigKey(key) {
  if (typeof key !== 'string' || !SAFE_CONFIG_KEY.test(key)) throw new Error('Clave de configuración no permitida')
}

function assertTrustedSender(event) {
  const url = event.senderFrame?.url || ''
  if (!url.startsWith('file:')) throw new Error('Origen IPC no permitido')
}

async function migrateLegacyApiKeys() {
  for (const [configKey, account] of [['openaiKey', 'openai_api_key'], ['anthropicKey', 'anthropic_api_key']]) {
    const legacyKey = db.getConfig(configKey)
    if (!legacyKey) continue
    if (keytarSafe.isAvailable()) {
      const stored = await keytarSafe.getPassword('EvalFP', account)
      if (!stored) await keytarSafe.setPassword('EvalFP', account, legacyKey)
      db.deleteConfig(configKey)
      logger.logEvent('LEGACY_API_KEY_MIGRATED', { key: configKey })
    } else {
      // No conservar secretos sin cifrar: se pedirá introducirlos de nuevo cuando
      // el llavero del sistema esté disponible.
      db.deleteConfig(configKey)
      logger.logEvent('LEGACY_API_KEY_REMOVED', { key: configKey })
    }
  }
}

async function getPublicConfig() {
  const config = db.getAllConfig()
  for (const key of SENSITIVE_CONFIG_KEYS) delete config[key]
  config.hasOpenAI = keytarSafe.isAvailable() && !!await keytarSafe.getPassword('EvalFP', 'openai_api_key')
  config.hasAnthropic = keytarSafe.isAvailable() && !!await keytarSafe.getPassword('EvalFP', 'anthropic_api_key')
  return config
}

function getAppInfo() {
  return {
    name: app.getName(),
    productName: pkg.build?.productName || app.getName(),
    version: app.getVersion(),
    license: pkg.license || 'GPL-3.0-or-later',
    copyright: pkg.build?.copyright || '',
    releaseNotes: [
      'Instalador y documentación base incluidos en el paquete final.',
      'Modal "Acerca de" con versión y licencia visibles dentro de la app.',
      'Autoapertura del aviso una sola vez por versión nueva.',
    ],
  }
}

// ── Automatic Database Backups ────────────────────────────────────────────────
const backupsDir = () => path.join(app.getPath('userData'), 'backups')
const dbPath = () => path.join(app.getPath('userData'), 'evalfp.db')

function setupBackups() {
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

    db.backupTo(dest)
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
      sandbox: true,
    },
  })
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'))
}

app.whenReady().then(async () => {
  await keytarInitialization
  await migrateLegacyApiKeys()
  await loadApiKeysFromSecureStorage()
  setupBackups()
  createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })

let isQuitting = false
app.on('before-quit', event => {
  if (isQuitting) return
  event.preventDefault()
  isQuitting = true
  performBackup()
    .catch(err => logger.logError('Final backup failed', err))
    .finally(() => app.quit())
})

// ── Helper Python ─────────────────────────────────────────────────────────────
function runPython(event, scriptName, args, replyChannel) {
  const sd  = scriptsDir()
  const env = { ...process.env, PYTHONPATH: sd }
  fs.mkdirSync(outputDir(), { recursive: true })
  const proc = spawn(python(), [path.join(sd, scriptName), ...args], { cwd: sd, env })
  proc.stdout.on('data', d => event.reply(replyChannel, { type:'stdout', text:d.toString() }))
  proc.stderr.on('data', d => event.reply(replyChannel, { type:'stderr', text:d.toString() }))
  proc.on('close', code => event.reply(replyChannel, { type:'done', code }))
  proc.on('error', err  => event.reply(replyChannel, { type:'error', text:err.message }))
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
ipcMain.handle('db:getModulos', event => { assertTrustedSender(event); return db.getModulos() })

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
ipcMain.handle('api:saveKeys', async (event, keys) => {
  try {
    assertTrustedSender(event)
    if (!keys || typeof keys !== 'object') throw new Error('Claves inválidas')
    for (const key of [keys.openai, keys.anthropic]) {
      if (key !== undefined && (typeof key !== 'string' || key.length < 10 || key.length > 500)) {
        throw new Error('Formato de clave inválido')
      }
    }
    let saved = false
    
    // Try keytar first if available
    if (keytarSafe.isAvailable()) {
      try {
        if (keys.openai) {
          await keytarSafe.setPassword('EvalFP', 'openai_api_key', keys.openai)
          process.env.OPENAI_API_KEY = keys.openai
        }
        if (keys.anthropic) {
          await keytarSafe.setPassword('EvalFP', 'anthropic_api_key', keys.anthropic)
          process.env.ANTHROPIC_API_KEY = keys.anthropic
        }
        logger.logEvent('API_KEYS_SAVED_TO_KEYTAR', { source: 'keytar' })
        saved = true
      } catch (keytarErr) {
        logger.logEvent('KEYTAR_WRITE_FAILED', { message: keytarErr.message })
        // Fall through to database
      }
    }
    
    if (!saved) {
      return {
        success: false,
        error: 'El almacenamiento seguro del sistema no está disponible. No se guardarán claves en texto plano.'
      }
    }
    
    return { 
      success: saved, 
      message: saved 
        ? 'Keys saved securely'
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
ipcMain.handle('db:getAllConfig', async event => {
  assertTrustedSender(event)
  return getPublicConfig()
})
ipcMain.handle('app:getInfo', () => getAppInfo())
ipcMain.handle('db:setConfig',   (event, k, v) => {
  assertTrustedSender(event)
  assertSafeConfigKey(k)
  if (typeof v !== 'string' || v.length > 60000) throw new Error('Valor de configuración inválido')
  db.setConfig(k, v)
})

ipcMain.handle('system:pythonStatus', event => {
  assertTrustedSender(event)
  const result = spawnSync(python(), ['--version'], { encoding: 'utf8', timeout: 5_000 })
  return { available: !result.error && result.status === 0, version: (result.stdout || result.stderr || '').trim() }
})

// ── IPC: IA + Apuntes ─────────────────────────────────────────────────────────
ipcMain.on('gen-ia', (event, { comando, modulo, ra, n, alumno, notas, proveedor, consent, anonimizar }) => {
  assertTrustedSender(event)
  if (!['rubrica', 'actividad', 'informe', 'todo'].includes(comando)) throw new Error('Comando IA no permitido')
  if (typeof modulo !== 'string' || !getModulesData().modules[modulo]) throw new Error('Módulo IA no válido')
  if (!PROVIDERS.has(proveedor || 'auto')) throw new Error('Proveedor IA no válido')
  if (comando === 'informe' && consent !== true) throw new Error('Debes confirmar el envío de datos académicos')
  if (n != null && (!Number.isInteger(Number(n)) || Number(n) < 1 || Number(n) > 10)) throw new Error('Número de actividades no válido')
  const od = outputDir()
  const salida = path.join(od, 'ia_output', modulo || 'modulo')
  fs.mkdirSync(salida, { recursive: true })
  const args = [comando]
  if (modulo)    args.push('--modulo', modulo)
  if (ra)        args.push('--ra', ra)
  if (n)         args.push('--n', String(n))
  if (alumno)    args.push('--alumno', anonimizar ? 'Alumno/a' : alumno)
  if (notas)     args.push('--notas', notas)
  if (proveedor) args.push('--proveedor', proveedor)
  if (comando === 'todo') args.push('--salida', salida)
  runPython(event, 'ai_asistente.py', args, 'gen-ia-reply')
})

ipcMain.on('gen-apuntes', (event, { modulo, ut, proveedor }) => {
  assertTrustedSender(event)
  if (typeof modulo !== 'string' || !getModulesData().modules[modulo]) throw new Error('Módulo de apuntes no válido')
  if (!PROVIDERS.has(proveedor || 'auto')) throw new Error('Proveedor IA no válido')
  if (ut != null && (typeof ut !== 'string' || ut.length > 30 || !/^[A-Za-z0-9_-]+$/.test(ut))) throw new Error('UT no válida')
  const salida = path.join(outputDir(), 'apuntes')
  fs.mkdirSync(salida, { recursive: true })
  const args = ['--salida', salida]
  if (modulo)    args.push('--modulo', modulo)
  if (ut)        args.push('--ut', ut)
  if (proveedor) args.push('--proveedor', proveedor)
  runPython(event, 'build_apuntes.py', args, 'gen-apuntes-reply')
})

ipcMain.on('open-output', () => shell.openPath(outputDir()))
ipcMain.on('open-material', () => {
  fs.mkdirSync(materialDir(), { recursive: true })
  shell.openPath(materialDir())
})

// ── IPC: PDF Boletín ──────────────────────────────────────────────────────────
ipcMain.handle('pdf:exportBoletin', async (_, htmlContent, alumnoNombre) => {
  const od  = path.join(outputDir(), 'boletines')
  fs.mkdirSync(od, { recursive: true })
  const filename = `boletin_${alumnoNombre.replace(/[^a-zA-Z0-9]/g,'_')}_${Date.now()}.pdf`
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

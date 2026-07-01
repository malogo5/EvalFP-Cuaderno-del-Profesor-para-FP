'use strict'
const { app, BrowserWindow, ipcMain, shell } = require('electron')
const path   = require('path')
const { spawn } = require('child_process')
const fs     = require('fs')
const os     = require('os')

// ── Rutas ─────────────────────────────────────────────────────────────────────
const scriptsDir = () => app.isPackaged
  ? path.join(process.resourcesPath, 'scripts')
  : path.join(__dirname, '..', 'scripts')

// JSON pre-horneado con todos los módulos (generado por prebake_modules.py)
const modulesDataPath = () => path.join(__dirname, 'renderer', 'modules_data.json')

const outputDir = () => path.join(os.homedir(), 'Documents', 'EvalFP')
const python    = () => process.platform === 'win32' ? 'python' : 'python3'

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

app.whenReady().then(() => {
  createWindow()
  // Cargar config API keys al entorno
  try {
    const db = require('./db')
    const cfg = db.getAllConfig()
    if (cfg.openaiKey)    process.env.OPENAI_API_KEY    = cfg.openaiKey
    if (cfg.anthropicKey) process.env.ANTHROPIC_API_KEY = cfg.anthropicKey
  } catch {}
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })

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

// ── IPC: Ponderaciones RA ─────────────────────────────────────────────────────
ipcMain.handle('db:getRaPonderaciones',  (_, mid)             => db.getRaPonderaciones(mid))
ipcMain.handle('db:setRaPonderacion',    (_, mid, raId, pond) => db.setRaPonderacion(mid, raId, pond))
ipcMain.handle('db:setModuloDataJson',   (_, id, data)        => db.setModuloDataJson(id, data))

// ── IPC: Config ───────────────────────────────────────────────────────────────
ipcMain.handle('db:getAllConfig', ()      => db.getAllConfig())
ipcMain.handle('db:setConfig',   (_, k, v) => {
  db.setConfig(k, v)
  if (k === 'openaiKey')    process.env.OPENAI_API_KEY    = v
  if (k === 'anthropicKey') process.env.ANTHROPIC_API_KEY = v
})

// ── IPC: IA + Apuntes ─────────────────────────────────────────────────────────
ipcMain.on('gen-ia', (event, { comando, modulo, ra, n, alumno, notas, proveedor }) => {
  const od = outputDir()
  const salida = path.join(od, 'ia_output', modulo || 'modulo')
  fs.mkdirSync(salida, { recursive: true })
  const args = [comando]
  if (modulo)    args.push('--modulo', modulo)
  if (ra)        args.push('--ra', ra)
  if (n)         args.push('--n', String(n))
  if (alumno)    args.push('--alumno', alumno)
  if (notas)     args.push('--notas', notas)
  if (proveedor) args.push('--proveedor', proveedor)
  if (comando === 'todo') args.push('--salida', salida)
  runPython(event, 'ai_asistente.py', args, 'gen-ia-reply')
})

ipcMain.on('gen-apuntes', (event, { modulo, ut, proveedor }) => {
  const salida = path.join(outputDir(), 'apuntes')
  fs.mkdirSync(salida, { recursive: true })
  const args = ['--salida', salida]
  if (modulo)    args.push('--modulo', modulo)
  if (ut)        args.push('--ut', ut)
  if (proveedor) args.push('--proveedor', proveedor)
  runPython(event, 'build_apuntes.py', args, 'gen-apuntes-reply')
})

ipcMain.on('open-output', () => shell.openPath(outputDir()))

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

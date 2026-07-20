// SPDX-License-Identifier: GPL-3.0-or-later
'use strict'
const { contextBridge, ipcRenderer } = require('electron')

// ── Validación en preload (contexto aislado, sin acceso a validators.js) ──────
function _isPositiveInt(v) {
  const n = typeof v === 'string' ? parseInt(v, 10) : v
  return Number.isInteger(n) && n > 0
}
function _isStr(v, maxLen = 500) {
  return typeof v === 'string' && v.length <= maxLen
}
function _validateId(id, label = 'id') {
  if (!_isPositiveInt(id)) throw new Error(`${label} inválido`)
}
function _validateAlumno(a) {
  if (!a || typeof a !== 'object') throw new Error('alumno inválido')
  if (!a.id && !_isPositiveInt(a.modulo_id)) throw new Error('modulo_id inválido')
  if (a.apellidos !== null && a.apellidos !== undefined && !_isStr(a.apellidos, 100)) throw new Error('apellidos muy largo')
  if (a.nombre !== null && a.nombre !== undefined && !_isStr(a.nombre, 100)) throw new Error('nombre muy largo')
  if (a.estado !== null && a.estado !== undefined && !['Activo','Pendiente','Baja'].includes(a.estado)) throw new Error('estado inválido')
  if (a.email !== null && a.email !== undefined && !_isStr(a.email, 200)) throw new Error('email muy largo')
  if (a.nia !== null && a.nia !== undefined && !_isStr(a.nia, 20)) throw new Error('NIA muy largo')
}
function _validateNota(n) {
  if (n === null || n === undefined) return
  const num = typeof n === 'string' ? parseFloat(n) : n
  if (isNaN(num) || num < 0 || num > 10) throw new Error('nota fuera de rango 0-10')
}
function _validatePond(pond) {
  const p = typeof pond === 'string' ? parseFloat(pond) : pond
  if (isNaN(p) || p < 0 || p > 100) throw new Error('ponderación fuera de rango 0-100')
}

contextBridge.exposeInMainWorld('api', {
  // ── Módulos ──────────────────────────────────────────────────────────────────
  getModulos:              ()            => ipcRenderer.invoke('db:getModulos'),
  listModulosDisponibles:  ()            => ipcRenderer.invoke('db:listModulosDisponibles'),
  getModuloData:           key           => {
    if (!_isStr(key, 100)) throw new Error('key inválida')
    return ipcRenderer.invoke('db:getModuloData', key)
  },
  addModulo:               payload       => ipcRenderer.invoke('db:addModulo', payload),
  deleteModulo:            id            => {
    _validateId(id, 'modulo id')
    return ipcRenderer.invoke('db:deleteModulo', id)
  },

  // ── Alumnos ──────────────────────────────────────────────────────────────────
  getAlumnos:   mid  => {
    _validateId(mid, 'modulo_id')
    return ipcRenderer.invoke('db:getAlumnos', mid)
  },
  saveAlumno:   a    => {
    _validateAlumno(a)
    return ipcRenderer.invoke('db:saveAlumno', a)
  },
  deleteAlumno: id   => {
    _validateId(id, 'alumno id')
    return ipcRenderer.invoke('db:deleteAlumno', id)
  },

  // ── Actividades ───────────────────────────────────────────────────────────────
  getActividades:   mid => {
    _validateId(mid, 'modulo_id')
    return ipcRenderer.invoke('db:getActividades', mid)
  },
  saveActividad:    a   => ipcRenderer.invoke('db:saveActividad', a),
  deleteActividad:  id  => {
    _validateId(id, 'actividad id')
    return ipcRenderer.invoke('db:deleteActividad', id)
  },

  // ── Notas ─────────────────────────────────────────────────────────────────────
  getNotasGrid: mid           => {
    _validateId(mid, 'modulo_id')
    return ipcRenderer.invoke('db:getNotasGrid', mid)
  },
  saveNota:     (aid, actId, n) => {
    _validateId(aid, 'alumno_id')
    _validateId(actId, 'actividad_id')
    _validateNota(n)
    return ipcRenderer.invoke('db:saveNota', aid, actId, n)
  },
  // Nota de recuperación (no sobrescribe la original — trazabilidad)
  saveNotaRec:  (aid, actId, n) => {
    _validateId(aid, 'alumno_id')
    _validateId(actId, 'actividad_id')
    _validateNota(n)
    return ipcRenderer.invoke('db:saveNotaRec', aid, actId, n)
  },

  // ── Ponderaciones RA ──────────────────────────────────────────────────────────
  getRaPonderaciones: mid              => {
    _validateId(mid, 'modulo_id')
    return ipcRenderer.invoke('db:getRaPonderaciones', mid)
  },
  setRaPonderacion:   (mid, raId, pond) => {
    _validateId(mid, 'modulo_id')
    _validatePond(pond)
    return ipcRenderer.invoke('db:setRaPonderacion', mid, raId, pond)
  },

  // ── Edición UT/RA/CE ──────────────────────────────────────────────────────────
  setModuloDataJson: (id, data) => {
    _validateId(id, 'modulo id')
    return ipcRenderer.invoke('db:setModuloDataJson', id, data)
  },

  // ── Config ────────────────────────────────────────────────────────────────────
  getAllConfig: ()      => ipcRenderer.invoke('db:getAllConfig'),
  getAppInfo:   ()      => ipcRenderer.invoke('app:getInfo'),
  isTestMode:   ()      => process.env.EVALFP_TEST === '1',
  setConfig:   (k, v)  => {
    if (!_isStr(k, 50))     throw new Error('config key inválida')
    if (!_isStr(v, 60000))  throw new Error('config value demasiado largo')
    return ipcRenderer.invoke('db:setConfig', k, v)
  },

  // ── API Keys (Secure Storage) ─────────────────────────────────────────────────
  saveApiKeys: keys => ipcRenderer.invoke('api:saveKeys', keys),
  getPythonStatus: () => ipcRenderer.invoke('system:pythonStatus'),

  // ── IA ────────────────────────────────────────────────────────────────────────
  genIA:      opts  => ipcRenderer.send('gen-ia', opts),
  onIA:       cb    => ipcRenderer.on('gen-ia-reply', (_, d) => cb(d)),
  genApuntes: opts  => ipcRenderer.send('gen-apuntes', opts),
  onApuntes:  cb    => ipcRenderer.on('gen-apuntes-reply', (_, d) => cb(d)),
  openOutput: ()    => ipcRenderer.send('open-output'),
  // Abre la carpeta unificada "Material IA" (rubricas/actividades/informes/apuntes)
  openMaterial: ()  => ipcRenderer.send('open-material'),

  // ── PDF ───────────────────────────────────────────────────────────────────────
  exportBoletin: (html, nombre) => {
    if (!_isStr(html, 2_000_000)) throw new Error('HTML demasiado largo')
    if (!_isStr(nombre, 100))     throw new Error('nombre de archivo inválido')
    return ipcRenderer.invoke('pdf:exportBoletin', html, nombre)
  },
})

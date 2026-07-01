'use strict'
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  // Módulos
  getModulos:            ()            => ipcRenderer.invoke('db:getModulos'),
  listModulosDisponibles:()            => ipcRenderer.invoke('db:listModulosDisponibles'),
  getModuloData:         key           => ipcRenderer.invoke('db:getModuloData', key),
  addModulo:             payload       => ipcRenderer.invoke('db:addModulo', payload),
  deleteModulo:          id            => ipcRenderer.invoke('db:deleteModulo', id),

  // Alumnos
  getAlumnos:            mid           => ipcRenderer.invoke('db:getAlumnos', mid),
  saveAlumno:            a             => ipcRenderer.invoke('db:saveAlumno', a),
  deleteAlumno:          id            => ipcRenderer.invoke('db:deleteAlumno', id),

  // Actividades
  getActividades:        mid           => ipcRenderer.invoke('db:getActividades', mid),
  saveActividad:         a             => ipcRenderer.invoke('db:saveActividad', a),
  deleteActividad:       id            => ipcRenderer.invoke('db:deleteActividad', id),

  // Notas
  getNotasGrid:          mid           => ipcRenderer.invoke('db:getNotasGrid', mid),
  saveNota:              (aid,actId,n) => ipcRenderer.invoke('db:saveNota', aid, actId, n),

  // Ponderaciones RA
  getRaPonderaciones:    mid              => ipcRenderer.invoke('db:getRaPonderaciones', mid),
  setRaPonderacion:      (mid,raId,pond)  => ipcRenderer.invoke('db:setRaPonderacion', mid, raId, pond),

  // Edición UT/RA/CE
  setModuloDataJson:     (id, data)       => ipcRenderer.invoke('db:setModuloDataJson', id, data),

  // Config
  getAllConfig:           ()            => ipcRenderer.invoke('db:getAllConfig'),
  setConfig:             (k,v)         => ipcRenderer.invoke('db:setConfig', k, v),

  // IA
  genIA:                 opts          => ipcRenderer.send('gen-ia', opts),
  onIA:                  cb            => ipcRenderer.on('gen-ia-reply', (_,d) => cb(d)),
  genApuntes:            opts          => ipcRenderer.send('gen-apuntes', opts),
  onApuntes:             cb            => ipcRenderer.on('gen-apuntes-reply', (_,d) => cb(d)),
  openOutput:            ()            => ipcRenderer.send('open-output'),

  // PDF
  exportBoletin:         (html,nombre) => ipcRenderer.invoke('pdf:exportBoletin', html, nombre),
})

// ASISTENTE IA
// ═══════════════════════════════════════════════════════════════

// Guarda el comando activo para enrutar respuestas al terminal correcto
let _activeIaCmd = null
let _activeIaBannerType = null
let _iaProgressTimer = null
let _iaProgressPhase = 0

// IDs de los selects de módulo en cada pestaña
const IA_MOD_SELS = ['ia-r-mod', 'ia-a-mod', 'ia-i-mod', 'ia-p-mod', 'ia-g-mod',
                     'ia-e-mod', 'ia-c-mod', 'ia-ap-mod', 'ia-t-mod']

// Módulos cuyo --modulo necesita RAs en el select
const IA_MOD_TO_RA = {
  'ia-r-mod': 'ia-r-ra',
  'ia-a-mod': 'ia-a-ra',
  'ia-e-mod': 'ia-e-ra',
}

// ── Inicialización de la sección ──────────────────────────────────────────────
function initIaSection() {
  _refreshPythonStatus()
  if (!_modulos.length) {
    IA_MOD_SELS.forEach(id => {
      const el = document.getElementById(id)
      if (el) el.innerHTML = '<option value="">Sin módulos</option>'
    })
    return
  }

  // Construir opciones de módulo a partir de _modulos (que ya están cargados en memoria)
  const modOpts = _modulos.map(m =>
    `<option value="${esc(m.key)}">${esc(m.abrev)}${m.grupo ? ' · '+esc(m.grupo) : ''}</option>`
  ).join('')

  // Rellenar todos los selects de módulo — el módulo activo del sidebar
  // (_curMod) tiene prioridad sobre la selección previa de cada pestaña
  IA_MOD_SELS.forEach(id => {
    const el = document.getElementById(id)
    if (!el) return
    const prev = el.value
    el.innerHTML = modOpts
    if (_curMod && _modulos.find(m => m.key === _curMod.key)) el.value = _curMod.key
    else if (_modulos.find(m => m.key === prev)) el.value = prev
  })

  // Rellenar selects de RA para el módulo seleccionado
  _updateIaRas('ia-r-mod')
  _updateIaRas('ia-a-mod')
  _updateIaRas('ia-e-mod')
  // Informe y plan dependen del módulo: recargar su alumnado
  if (typeof iaInformeLoadAlumnos === 'function') iaInformeLoadAlumnos()
  if (typeof iaPlanLoadAlumnos === 'function') iaPlanLoadAlumnos()
  if (typeof iaCorregirLoad === 'function') iaCorregirLoad()

  // Wiring: cambio de módulo → actualizar RAs
  Object.keys(IA_MOD_TO_RA).forEach(modSelId => {
    const el = document.getElementById(modSelId)
    if (el) el.onchange = () => _updateIaRas(modSelId)
  })
}

function _refreshPythonStatus() {
  const el = document.getElementById('ia-python-status')
  if (!el) return
  window.api.getPythonStatus()
    .then(({ available, version }) => {
      el.textContent = available
        ? `✓ Entorno Python disponible (${version}). Para IA real instala las dependencias de requirements.txt y configura una clave API.`
        : '⚠️ Python 3 no está disponible. La generación de IA y apuntes requiere instalar Python 3.10+ y ejecutar “pip install -r requirements.txt”.'
      el.style.color = available ? 'var(--green)' : 'var(--amber)'
    })
    .catch(() => {
      el.textContent = '⚠️ No se pudo comprobar Python. La generación de IA puede no estar disponible.'
      el.style.color = 'var(--amber)'
    })
}

// Actualiza el select de RAs correspondiente al select de módulo dado
function _updateIaRas(modSelId) {
  const raSelId = IA_MOD_TO_RA[modSelId]
  if (!raSelId) return
  const raEl = document.getElementById(raSelId)
  if (!raEl) return

  const modKey = document.getElementById(modSelId)?.value
  const mod = _modulos.find(m => m.key === modKey)
  if (!mod) return

  let ras = []
  try {
    const data = typeof mod.data_json === 'string'
      ? JSON.parse(mod.data_json)
      : mod.data_json
    ras = data?.ras || []
  } catch (_) { /* data_json puede ser null en módulos sin datos normativos */ }

  if (!ras.length) {
    raEl.innerHTML = '<option value="">Sin RAs</option>'
    return
  }

  raEl.innerHTML = ras.map(r =>
    `<option value="${esc(r.id)}">${esc(r.id)}: ${esc(r.nombre)}</option>`
  ).join('')
}

// ── Navegación de tabs ────────────────────────────────────────────────────────
function iaTab(el, id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'))
  el.classList.add('active')
  IA_TABS.forEach(t => document.getElementById('ia-'+t).style.display = t===id ? '' : 'none')
}

// ── Terminal ──────────────────────────────────────────────────────────────────
// Todos los avisos normativos que puede emitir el motor, con su gravedad.
// Si el motor añade uno nuevo y no está aquí, se muestra igualmente su texto tal cual:
// más vale un mensaje en bruto que un aviso que no llega.
const IA_CODIGOS = [
  ['RA_NO_EVALUADO',      'error',   'Faltan calificaciones en algunos Resultados de Aprendizaje. Completa la pestaña de Notas antes de generar el informe.'],
  ['PONDERACION_CERO',    'error',   'La suma de las ponderaciones de los RA es 0%. Revisa la configuración del módulo.'],
  ['NOTA_INVALIDA',       'error',   'Se ha detectado un formato o rango de nota incorrecto (debe estar entre 0 y 10).'],
  ['ERROR_RED',           'error',   'No se ha podido conectar con el servidor de IA. Revisa tu conexión a internet o inténtalo más tarde.'],
  ['SIN_DATOS',           'error',   'Faltan datos para generar esto. Revisa que el módulo tenga alumnado, actividades y notas.'],
  ['RESPUESTA_NO_VALIDA', 'error',   'La respuesta del modelo no ha llegado en el formato esperado. Vuelve a intentarlo.'],
  ['RA_NO_ENCONTRADO',    'error',   'El resultado de aprendizaje seleccionado no existe en este módulo.'],
  ['SIN_IMAGENES',        'error',   'No he recibido ninguna foto del examen.'],
  ['DEMASIADAS_IMAGENES', 'error',   'Demasiadas páginas para un solo examen (máximo 12).'],
  ['IMAGEN_GRANDE',       'error',   'Alguna foto pesa más de 5 MB. Redúcela antes de corregir.'],
  ['RA_SUSPENDIDO',       'warning', 'Hay algún RA suspenso: el resultado normativo es NO APTO aunque la media llegue a 5.'],
  ['ABSENTISMO_CRITICO',  'warning', 'Absentismo por encima del umbral: puede implicar pérdida del derecho a la evaluación continua.'],
  ['RA_LLAVE_SUSPENDIDO', 'warning', 'Ha suspendido un RA marcado como llave: el módulo queda NO APTO por ese solo motivo.'],
]

/** Todos los códigos presentes en el texto, en el orden en que los emite Python. */
function _codigosEnTexto(text) {
  const raw = String(text || '')
  const vistos = []
  for (const [codigo, tipo, msg] of IA_CODIGOS) {
    // El motor los emite como «CODIGO: detalle»
    const m = raw.match(new RegExp(`${codigo}:?\\s*([^\\n]*)`))
    if (m) vistos.push({ codigo, tipo, msg, detalle: (m[1] || '').trim() })
  }
  return vistos
}

function _humanizeIaMessage(text) {
  const encontrados = _codigosEnTexto(text)
  if (!encontrados.length) return String(text || '').trim()
  return encontrados.map(c => c.msg + (c.detalle ? `\n   ${c.detalle}` : '')).join('\n\n')
}

function _showIaAlert(type, rawText) {
  const cmd = _activeIaCmd || 'informe'
  const el = document.getElementById(`ia-${cmd}-term`)
  if (!el) return

  const text = _humanizeIaMessage(rawText)
  const existing = el.querySelector('.ia-alert-banner')
  if (existing) existing.remove()

  const banner = document.createElement('div')
  banner.className = `ia-alert-banner ia-alert-${type === 'warning' ? 'warning' : 'error'}`
  banner.setAttribute('role', type === 'warning' ? 'status' : 'alert')
  banner.style.display = 'flex'
  banner.style.gap = '12px'
  banner.style.alignItems = 'flex-start'
  banner.style.padding = '12px 14px'
  banner.style.margin = '0 0 12px 0'
  banner.style.borderRadius = '12px'
  banner.style.border = type === 'warning' ? '1px solid #d9b200' : '1px solid #cc3d3d'
  banner.style.background = type === 'warning' ? '#fff7d6' : '#ffe2e2'
  banner.style.color = '#1f2937'
  banner.style.boxShadow = '0 8px 24px rgba(0,0,0,0.08)'
  banner.style.fontSize = '14px'

  const icon = type === 'warning' ? '⚠️' : '⛔'
  const iconWrap = document.createElement('div')
  iconWrap.className = 'ia-alert-banner__icon'
  iconWrap.textContent = icon
  iconWrap.style.fontSize = '18px'
  iconWrap.style.lineHeight = '1.2'
  iconWrap.style.flex = '0 0 auto'

  const body = document.createElement('div')
  body.className = 'ia-alert-banner__body'
  body.style.display = 'flex'
  body.style.flexDirection = 'column'
  body.style.gap = '4px'

  const title = document.createElement('div')
  title.className = 'ia-alert-banner__title'
  title.textContent = type === 'warning' ? 'Advertencia' : 'Error bloqueante'
  title.style.fontWeight = '700'
  title.style.fontSize = '14px'

  const msg = document.createElement('div')
  msg.className = 'ia-alert-banner__text'
  msg.textContent = text
  msg.style.whiteSpace = 'pre-wrap'
  msg.style.lineHeight = '1.4'
  body.appendChild(title)
  body.appendChild(msg)
  banner.appendChild(iconWrap)
  banner.appendChild(body)
  el.prepend(banner)
  el.scrollTop = 0
}

function _setIaLoading(cmd, active) {
  if (!active) {
    if (_iaProgressTimer) {
      clearInterval(_iaProgressTimer)
      _iaProgressTimer = null
    }
    _iaProgressPhase = 0
    document.querySelectorAll('.ia-loading-banner').forEach(b => b.remove())
    return
  }

  const termId = cmd ? `ia-${cmd}-term` : 'ia-todo-term'
  const el = document.getElementById(termId)
  if (!el) return

  const phases = [
    'Fase 1: Validando expediente…',
    'Fase 2: Conectando con el motor de IA…',
    'Fase 3: Redactando informe…',
  ]

  const render = () => {
    let banner = el.querySelector('.ia-loading-banner')
    if (!banner) {
      banner = document.createElement('div')
      banner.className = 'ia-loading-banner'
      banner.style.display = 'flex'
      banner.style.gap = '12px'
      banner.style.alignItems = 'center'
      banner.style.padding = '12px 14px'
      banner.style.margin = '0 0 12px 0'
      banner.style.borderRadius = '12px'
      banner.style.border = '1px solid #9ab7e6'
      banner.style.background = '#eef5ff'
      banner.style.color = '#1f2937'
      banner.style.boxShadow = '0 8px 24px rgba(0,0,0,0.06)'
      const spin = document.createElement('div')
      spin.className = 'ia-loading-spinner'
      spin.textContent = '⏳'
      spin.style.fontSize = '18px'
      spin.style.lineHeight = '1'
      const body = document.createElement('div')
      body.className = 'ia-loading-body'
      const title = document.createElement('div')
      title.textContent = 'Procesando IA'
      title.style.fontWeight = '700'
      const msg = document.createElement('div')
      msg.className = 'ia-loading-msg'
      msg.style.marginTop = '4px'
      body.appendChild(title)
      body.appendChild(msg)
      banner.appendChild(spin)
      banner.appendChild(body)
      el.prepend(banner)
    }
    const msg = banner.querySelector('.ia-loading-msg')
    if (msg) msg.textContent = phases[_iaProgressPhase % phases.length]
  }

  render()
  if (_iaProgressTimer) clearInterval(_iaProgressTimer)
  _iaProgressTimer = setInterval(() => {
    _iaProgressPhase = (_iaProgressPhase + 1) % phases.length
    render()
  }, 1800)
}

function _isValidNotasClientFormat(text) {
  const raw = String(text || '').trim()
  if (!raw) return false
  return /^(?:[A-Za-z0-9_]+:\s*(?:10(?:\.0+)?|[0-9](?:\.[0-9]+)?))(?:\s*,\s*[A-Za-z0-9_]+:\s*(?:10(?:\.0+)?|[0-9](?:\.[0-9]+)?))*$/.test(raw)
}

function _extractMetaFromMod(mod) {
  try {
    return typeof mod?.data_json === 'string' ? JSON.parse(mod.data_json) : (mod?.data_json || {})
  } catch (_) {
    return {}
  }
}

function _extractRaLlave(mod) {
  const data = _extractMetaFromMod(mod)
  const raw = data?.ras_llave ?? data?.rasLlave ?? data?.ra_llave ?? data?.raLlave ?? ''
  if (Array.isArray(raw)) return raw.map(String).filter(Boolean).join(',')
  return String(raw || '').trim()
}

async function _extractFaltasPorcentaje(mod) {
  const data = _extractMetaFromMod(mod)
  const raw = data?.faltas_porcentaje ?? data?.faltasPorcentaje ?? data?.absentismo ?? ''
  if (raw != null && String(raw).trim() !== '') return String(raw).trim()
  try {
    const cfgAll = await window.api.getAllConfig()
    const cfgKey = `faltas_${mod?.id}`
    if (cfgAll?.[cfgKey] != null && String(cfgAll[cfgKey]).trim() !== '') return String(cfgAll[cfgKey]).trim()
  } catch (_) { /* sin configuración de absentismo */ }
  return ''
}

function _hasNormativeCode(text) {
  const encontrados = _codigosEnTexto(text)
  return encontrados.length ? encontrados[0].codigo : null
}

/** Gravedad del conjunto: si hay un solo error, el banner es de error. */
function _iaAlertTypeForText(text) {
  const encontrados = _codigosEnTexto(text)
  if (!encontrados.length) return null
  return encontrados.some(c => c.tipo === 'error') ? 'error' : 'warning'
}

function _iaAlertTypeForCode(code) {
  if (code === 'RA_SUSPENDIDO') return 'warning'
  if (code === 'RA_NO_EVALUADO' || code === 'NOTA_INVALIDA' || code === 'PONDERACION_CERO' || code === 'ERROR_RED') return 'error'
  return null
}

function termAppend(id, d) {
  const el = document.getElementById(id)
  if (!el) return
  if (el.querySelector('.placeholder')) el.innerHTML = ''
  const line = document.createElement('div')
  if      (d.type === 'stdout') { line.className = 'line-out';  line.textContent = d.text.trimEnd() }
  else if (d.type === 'stderr') { line.className = 'line-err';  line.textContent = d.text.trimEnd() }
  else if (d.type === 'done')   {
    line.className  = d.code === 0 ? 'line-done' : 'line-fail'
    line.textContent = d.code === 0 ? '✅ Completado' : '❌ Error (código ' + d.code + ')'
  }
  else { line.className = 'line-err'; line.textContent = '⚠️ ' + d.text }
  el.appendChild(line)
  el.scrollTop = el.scrollHeight
}

// ── Ejecutar comandos IA ──────────────────────────────────────────────────────
async function runIA(cmd) {
  const VALID = ['rubrica', 'actividad', 'informe', 'plan', 'grupo', 'examen', 'todo']
  if (!VALID.includes(cmd)) return

  // Limpiar terminal
  const termEl = document.getElementById('ia-' + cmd + '-term')
  if (termEl) termEl.innerHTML = ''

  const opts = { comando: cmd }

  if (cmd === 'rubrica') {
    opts.modulo    = v('ia-r-mod')
    opts.ra        = v('ia-r-ra')
    opts.proveedor = v('ia-r-prov')
    if (!opts.modulo) { alert('Selecciona un módulo para generar la rúbrica.'); return }
    if (!opts.ra)     { alert('Selecciona un RA para generar la rúbrica.'); return }
  }

  if (cmd === 'actividad') {
    opts.modulo    = v('ia-a-mod')
    opts.ra        = v('ia-a-ra')
    opts.n         = v('ia-a-n') || '3'
    opts.proveedor = v('ia-a-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    if (!opts.ra)     { alert('Selecciona un RA.'); return }
  }

  if (cmd === 'informe') {
    opts.modulo    = v('ia-i-mod')
    opts.alumno    = v('ia-i-alumno-sel').trim()
    opts.notas     = v('ia-i-notas').trim()
    opts.proveedor = v('ia-i-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    if (!opts.alumno) { alert('Selecciona un alumno/a.'); return }
    if (!opts.notas)  { alert('Las notas por RA están vacías. Selecciona un alumno/a con notas guardadas.'); return }
    if (!_isValidNotasClientFormat(opts.notas)) {
      _showIaAlert('error', 'El formato de las notas en el cliente es incorrecto. Limpie los caracteres extraños antes de enviar.')
      return
    }
    const minExam = document.getElementById('ia-i-notas')?.dataset?.minExam
    if (minExam != null && String(minExam).trim() !== '') opts.minExam = String(minExam).trim()
    const pondStr = document.getElementById('ia-i-notas')?.dataset?.ponderaciones
    if (pondStr != null && String(pondStr).trim() !== '') opts.ponderaciones = String(pondStr).trim()
    opts.consent = document.getElementById('ia-i-consent')?.checked === true
    opts.anonimizar = document.getElementById('ia-i-anonimizar')?.checked === true
    if (!opts.consent) { alert('Confirma que entiendes el envío de datos académicos al proveedor IA.'); return }

    const mod = _modulos.find(m => m.key === opts.modulo)
    if (mod) {
      const faltasPorcentaje = await _extractFaltasPorcentaje(mod)
      if (faltasPorcentaje) opts.faltasPorcentaje = faltasPorcentaje
      const rasLlave = _extractRaLlave(mod)
      if (rasLlave) opts.rasLlave = rasLlave
      // Notas actividad a actividad del alumno/a: sin esto la IA solo ve medias
      // por RA y no puede decir en qué falló exactamente.
      const det = await _detalleActividadesAlumno(mod, opts.alumno)
      if (det) opts.detalleJson = det
    }
  }

  if (cmd === 'plan') {
    opts.modulo    = v('ia-p-mod')
    opts.alumno    = v('ia-p-alumno-sel').trim()
    opts.notas     = v('ia-p-notas').trim()
    opts.semanas   = v('ia-p-semanas') || '4'
    opts.proveedor = v('ia-p-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    if (!opts.alumno) { alert('Selecciona un alumno/a.'); return }
    if (!opts.notas)  { alert('No hay notas guardadas de este alumno/a.'); return }
    if (!_isValidNotasClientFormat(opts.notas)) {
      _showIaAlert('error', 'El formato de las notas es incorrecto.')
      return
    }
    opts.consent    = document.getElementById('ia-p-consent')?.checked === true
    opts.anonimizar = document.getElementById('ia-p-anonimizar')?.checked === true
    if (!opts.consent) { alert('Confirma que entiendes el envío de datos académicos al proveedor IA.'); return }
    const mod = _modulos.find(m => m.key === opts.modulo)
    if (mod) {
      const det = await _detalleActividadesAlumno(mod, opts.alumno)
      if (det) opts.detalleJson = det
    }
  }

  if (cmd === 'grupo') {
    opts.modulo    = v('ia-g-mod')
    opts.proveedor = v('ia-g-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    if (document.getElementById('ia-g-consent')?.checked !== true) {
      alert('Confirma que entiendes el envío de las calificaciones del grupo al proveedor IA.')
      return
    }
    const mod = _modulos.find(m => m.key === opts.modulo)
    if (!mod) return
    try {
      const alumnos = (await window.api.getAlumnos(mod.id)).filter(a => a.estado === 'Activo')
      // Al grupo no le hacen falta los nombres: solo los identificadores internos
      opts.alumnosJson     = JSON.stringify(alumnos.map(a => ({ id: a.id })))
      opts.notasGridJson   = JSON.stringify(await window.api.getNotasGrid(mod.id))
      opts.actividadesJson = JSON.stringify(await window.api.getActividades(mod.id))
    } catch (e) {
      _showIaAlert('error', 'No he podido leer las notas del grupo: ' + e.message)
      return
    }
  }

  if (cmd === 'examen') {
    opts.modulo    = v('ia-e-mod')
    opts.ra        = v('ia-e-ra')
    opts.n         = v('ia-e-n') || '8'
    opts.tipo      = v('ia-e-tipo') || 'mixto'
    opts.duracion  = v('ia-e-duracion') || '50'
    opts.proveedor = v('ia-e-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    if (!opts.ra)     { alert('Selecciona el RA que quieres evaluar.'); return }
  }

  if (cmd === 'todo') {
    opts.modulo    = v('ia-t-mod')
    opts.proveedor = v('ia-t-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
    const mod = _modulos.find(m => m.key === opts.modulo)
    if (mod) {
      try {
        const alumnos = (await window.api.getAlumnos(mod.id)).filter(a => a.estado === 'Activo')
        opts.alumnosJson = JSON.stringify(alumnos)
        opts.notasGridJson = JSON.stringify(await window.api.getNotasGrid(mod.id))
        opts.actividadesJson = JSON.stringify(await window.api.getActividades(mod.id))
      } catch (_) { /* sin exportación de datos auxiliares */ }
    }
  }

  _activeIaCmd = cmd
  _setIaLoading(cmd, true)
  window.api.genIA(opts)
}

// Registrar listener de respuestas IA (una sola vez al cargar el módulo)
window.api.onIA(d => {
  const termId = _activeIaCmd ? `ia-${_activeIaCmd}-term` : 'ia-todo-term'
  const rawText = d && typeof d.text === 'string' ? d.text : ''
  const normCode = _hasNormativeCode(rawText)

  if (normCode) {
    const type = _iaAlertTypeForText(rawText)
    if (type) {
      _activeIaBannerType = type
      _showIaAlert(type, rawText)
      if (type === 'error') {
        if (d.type === 'done' || d.type === 'error') _activeIaCmd = null
        return
      }
    }
  }

  if (_activeIaBannerType === 'error' && (d.type === 'stdout' || d.type === 'stderr')) return

  termAppend(termId, d)
  // Al terminar con éxito: acceso directo a la carpeta de material
  if (d.type === 'done' && d.code === 0) _addMaterialBtn(termId)
  if (d.type === 'done' || d.type === 'error') {
    _activeIaCmd = null
    _activeIaBannerType = null
    _setIaLoading(null, false)
  }
})

/** Añade al terminal un botón para abrir la carpeta "Material IA". */
function _addMaterialBtn(termId) {
  const el = document.getElementById(termId)
  if (!el || el.querySelector('.btn-material')) return
  const btn = document.createElement('button')
  btn.className = 'btn btn-ghost btn-sm btn-material'
  btn.style.marginTop = '10px'
  btn.textContent = '📂 Abrir carpeta de material'
  btn.onclick = () => window.api.openMaterial()
  el.appendChild(document.createElement('br'))
  el.appendChild(btn)
  el.scrollTop = el.scrollHeight
}

// ── Apuntes HTML ──────────────────────────────────────────────────────────────
function runApuntes() {
  const modulo = v('ia-ap-mod')
  if (!modulo) { alert('Selecciona un módulo para generar apuntes.'); return }
  const termEl = document.getElementById('ia-apuntes-term')
  if (termEl) termEl.innerHTML = ''
  window.api.genApuntes({
    modulo,
    ut:        v('ia-ap-ut').trim() || null,
    proveedor: v('ia-ap-prov'),
  })
}

// Registrar listener de apuntes (una sola vez al cargar el módulo)
window.api.onApuntes(d => {
  const TID = 'ia-apuntes-term'

  // Sin API key → alert
  if (d.type === 'stdout' && d.text.startsWith('EVALFP_NO_KEY:')) {
    const msg = d.text.replace('EVALFP_NO_KEY:', '').trim()
    alert('⚠️ Sin API key\n\n' + msg)
    return
  }

  // Tags de progreso → estilos visuales propios
  if (d.type === 'stdout') {
    const tags = [
      { prefix: 'EVALFP_FASE:', cls: 'line-phase' },
      { prefix: 'EVALFP_PASO:', cls: 'line-step'  },
      { prefix: 'EVALFP_OK:',   cls: 'line-ok'    },
      { prefix: 'EVALFP_CONT:', cls: 'line-cont'  },
    ]
    for (const { prefix, cls } of tags) {
      if (d.text.startsWith(prefix)) {
        _termLine(TID, d.text.slice(prefix.length).trim(), cls)
        return
      }
    }
  }

  if (d.type === 'done') {
    termAppend(TID, d)
    if (d.code === 0) {
      // Añadir botón para abrir la carpeta de apuntes
      _addMaterialBtn(TID)
    }
    _setIaLoading(null, false)
    return
  }

  termAppend(TID, d)
})

/**
 * Notas actividad a actividad de un alumno/a, con su UT y su RA. Es lo que
 * permite que el informe y el plan citen evidencias concretas en vez de medias.
 * Devuelve JSON listo para enviar, o null si no hay nada que contar.
 */
async function _detalleActividadesAlumno(mod, nombreAlumno) {
  try {
    const alumnos = await window.api.getAlumnos(mod.id)
    const alumno = alumnos.find(a =>
      `${a.apellidos || ''}${a.apellidos && a.nombre ? ', ' : ''}${a.nombre || ''}` === nombreAlumno)
    if (!alumno) return null
    const grid = await window.api.getNotasGrid(mod.id)
    const acts = await window.api.getActividades(mod.id)
    const detalle = grid.filter(g => g.alumno_id === alumno.id).map(g => {
      const act = acts.find(a => a.id === g.actividad_id) || {}
      return {
        descripcion: act.descripcion || '',
        ut_id: act.ut_id || '', ra_id: act.ra_id || '',
        nota: g.nota_rec != null ? g.nota_rec : g.nota,
      }
    }).filter(d => d.nota != null && d.ra_id)
    return detalle.length ? JSON.stringify(detalle) : null
  } catch (_) {
    return null   // informe y plan funcionan igual sin el detalle
  }
}

// ── Informe y plan: cargan alumnado del módulo y auto-rellenan notas por RA ──
// Comparten lógica: cambia solo el prefijo de los identificadores ('i' / 'p').

async function iaPlanLoadAlumnos() { return iaInformeLoadAlumnos('p') }
async function iaPlanAutoNotas()   { return iaInformeAutoNotas('p') }


async function iaInformeLoadAlumnos(pref = 'i') {
  const key = v(`ia-${pref}-mod`)
  const sel = document.getElementById(`ia-${pref}-alumno-sel`)
  if (!sel) return
  if (!key) { sel.innerHTML = '<option value="">— selecciona módulo —</option>'; return }

  try {
    const mod = _modulos.find(m => m.key === key)
    if (!mod) return
    const alumnos = (await window.api.getAlumnos(mod.id)).filter(a => a.estado === 'Activo')
    sel.innerHTML = '<option value="">— selecciona alumno/a —</option>' +
      alumnos.map(a =>
        `<option value="${esc(a.apellidos||'')}${a.apellidos&&a.nombre?', ':''}${esc(a.nombre||'')}" data-id="${a.id}">`+
        `${esc(a.apellidos||'')}${a.apellidos&&a.nombre?', ':''}${esc(a.nombre||'')}</option>`
      ).join('')
  } catch(_) { /* sin alumnos */ }
  const campo = document.getElementById(`ia-${pref}-notas`)
  if (campo) campo.value = ''
}

async function iaInformeAutoNotas(pref = 'i') {
  const key     = v(`ia-${pref}-mod`)
  const alumnoName = v(`ia-${pref}-alumno-sel`)
  if (!key || !alumnoName) return

  try {
    const mod = _modulos.find(m => m.key === key)
    if (!mod) return

    // Obtener datos del módulo para saber los RAs
    const modData = _getModData(mod.id)
    const ras     = modData?.ras || []
    if (!ras.length) return

    // Obtener notas y actividades
    const notasArr = await window.api.getNotasGrid(mod.id)
    const acts     = await window.api.getActividades(mod.id)
    const alumnos  = await window.api.getAlumnos(mod.id)
    const alumno   = alumnos.find(a =>
      `${a.apellidos||''}${a.apellidos&&a.nombre?', ':''}${a.nombre||''}` === alumnoName
    )
    if (!alumno) return

    // Construir mapa nota_alumno[actividad_id] (nota efectiva)
    // H6: nota efectiva = nota_rec (recuperación) si existe.
    const ng = {}
    notasArr.forEach(n => { if (n.alumno_id === alumno.id) ng[n.actividad_id] = n.nota_rec ?? n.nota })

    // Calcular notas por RA con el mismo motor que Evaluaciones (H4/H6) y
    // preparar también una "nota de examen por RA" para validar mínimos en Python.
    //
    // Nota: en la app, el mínimo se aplica por actividades tipo examen (si alguna
    // queda por debajo del mínimo, el RA no se considera superado). Para poder
    // replicarlo en Python sin pasar todas las actividades, enviamos por cada RA
    // el mínimo de sus exámenes como "<RA>_EX:<nota>" (si existe).
    const cesByRa = modData?.ces || {}

    // Pesos globales por tipo (fallback si no hay pesos en actividades)
    const sumPP = acts.filter(a => a.tipo === 'practica').reduce((s, a) => s + (a.peso || 0), 0)
    const sumPE = acts.filter(a => a.tipo === 'examen').reduce((s, a) => s + (a.peso || 0), 0)
    const totP  = sumPP + sumPE
    const PRAC  = totP > 0 ? sumPP / totP : 0.30
    const EXAM  = totP > 0 ? sumPE / totP : 0.70

    // Mínimo de examen configurado por módulo (si existe)
    const cfgAll  = await window.api.getAllConfig()
    const minRaw  = cfgAll[`minexam_${mod.id}`]
    const minExam = minRaw != null && String(minRaw).trim() !== '' ? parseFloat(minRaw) : null

    // Overrides de ponderación por RA (si existen)
    let raPondOverrides = {}
    try {
      const rows = await window.api.getRaPonderaciones(mod.id)
      rows.forEach(r => { raPondOverrides[r.ra_id] = r.pond })
    } catch { /* sin overrides */ }

    const notasPairs = []
    ras.forEach(ra => {
      const pond = raPondOverrides[ra.id] !== undefined ? raPondOverrides[ra.id] : (ra.pond || 0)
      // Guardar pond en ra para que el informe pueda incluirlo si lo necesita.
      ra.pond = pond

      // Nota RA (H4): media ponderada por peso / fallback por tipo
      const raNota = typeof _calcNotaRA === 'function'
        ? _calcNotaRA(ra.id, cesByRa[ra.id] || [], acts, ng, PRAC, EXAM)
        : null
      if (raNota !== null && raNota !== undefined) {
        notasPairs.push(`${ra.id}:${raNota.toFixed(1)}`)
      }

      // Nota mínima de examen por RA: min(nota) entre actividades examen del RA/CE
      const examNotas = acts.filter(a => {
        if (a.tipo !== 'examen') return false
        if (String(a.ra_id) === String(ra.id)) return true
        // Si va por CEs, incluir exámenes que toquen CEs del RA
        const ceList = cesByRa[ra.id] || []
        const ceIdSet = new Set(ceList.map(c => c.id))
        try { return JSON.parse(a.ces || '[]').some(id => ceIdSet.has(id)) } catch { return false }
      }).map(a => ng[a.id]).filter(n => n != null)
      if (examNotas.length) {
        const minEx = Math.min(...examNotas)
        notasPairs.push(`${ra.id}_EX:${minEx.toFixed(1)}`)
      }
    })

    // Rellenar campo notas y mostrar recordatorio de criterio
    const campoNotas = document.getElementById(`ia-${pref}-notas`)
    if (campoNotas) campoNotas.value = notasPairs.join(',')
    const hint = document.getElementById(pref === 'i' ? 'ia-i-notas-hint' : 'ia-p-hint')
    if (hint) {
      hint.textContent = minExam != null
        ? `Criterio: APTO exige todos los RA >=5 y exámenes >=${minExam}.`
        : 'Criterio: APTO exige todos los RA >=5 (la media no compensa un RA suspenso).'
    }
    const notasEl = document.getElementById(`ia-${pref}-notas`)
    if (notasEl) {
      notasEl.dataset.minExam = minExam != null ? String(minExam) : ''
      const pondPairs = ras.map(ra => `${ra.id}:${(raPondOverrides[ra.id] !== undefined ? raPondOverrides[ra.id] : (ra.pond || 0))}`)
      notasEl.dataset.ponderaciones = pondPairs.join(',')
    }
  } catch(_) { /* sin notas disponibles */ }
}

/** Añade una línea con clase CSS específica al terminal de apuntes */
function _termLine(termId, text, cls) {
  const el = document.getElementById(termId)
  if (!el) return
  if (el.querySelector('.placeholder')) el.innerHTML = ''
  const line = document.createElement('span')
  line.className = cls
  line.textContent = text
  el.appendChild(line)
  el.appendChild(document.createElement('br'))
  el.scrollTop = el.scrollHeight
}

// ═══════════════════════════════════════════════════════════════
// CORRECCIÓN DE EXÁMENES DESDE FOTO
// ═══════════════════════════════════════════════════════════════
// Sigue los principios del prompt maestro de corrección: un examen es de un solo
// alumno, la rúbrica son los criterios del decreto, y la nota que devuelve la IA
// es una PROPUESTA que el profesorado revisa antes de que entre en el cuaderno.

let _fotosExamen = []
let _notaPropuesta = null

/** Carga RAs, alumnado y actividades del módulo elegido en la pestaña. */
async function iaCorregirLoad() {
  const key = v('ia-c-mod')
  const mod = _modulos.find(m => m.key === key)
  const selRa  = document.getElementById('ia-c-ra')
  const selAl  = document.getElementById('ia-c-alumno')
  const selAct = document.getElementById('ia-c-actividad')
  if (!mod) return

  let ras = []
  try {
    const data = typeof mod.data_json === 'string' ? JSON.parse(mod.data_json) : mod.data_json
    ras = data?.ras || []
  } catch (_) { /* módulo sin datos normativos */ }
  if (selRa) {
    selRa.innerHTML = ras.length
      ? ras.map(r => `<option value="${esc(r.id)}">${esc(r.id)}: ${esc(r.nombre)}</option>`).join('')
      : '<option value="">Sin RAs</option>'
  }

  try {
    const alumnos = (await window.api.getAlumnos(mod.id)).filter(a => a.estado === 'Activo')
    if (selAl) {
      selAl.innerHTML = '<option value="">— selecciona alumno/a —</option>' + alumnos.map(a =>
        `<option value="${a.id}">${esc(a.apellidos || '')}${a.apellidos && a.nombre ? ', ' : ''}${esc(a.nombre || '')}</option>`
      ).join('')
    }
    const acts = await window.api.getActividades(mod.id)
    if (selAct) {
      selAct.innerHTML = '<option value="">— actividad donde guardarla —</option>' + acts.map(a =>
        `<option value="${a.id}">${esc(a.descripcion || '')}${a.ra_id ? ' · ' + esc(a.ra_id) : ''}</option>`
      ).join('')
    }
  } catch (_) { /* módulo sin alumnado todavía */ }
}

/** Diálogo nativo para elegir las páginas del examen. */
async function iaElegirFotos() {
  try {
    const rutas = await window.api.elegirFotosExamen()
    _fotosExamen = Array.isArray(rutas) ? rutas : []
    const el = document.getElementById('ia-c-fotos')
    if (!el) return
    el.textContent = _fotosExamen.length
      ? `${_fotosExamen.length} página(s): ${_fotosExamen.map(p => p.split('/').pop()).join(' · ')}`
      : 'Ninguna foto seleccionada. Elige las páginas de un solo alumno, en orden.'
  } catch (e) {
    _showIaAlert('error', 'No he podido abrir el selector de fotos: ' + e.message)
  }
}

async function runCorreccion() {
  const modulo = v('ia-c-mod')
  const ra     = v('ia-c-ra')
  const aid    = v('ia-c-alumno')
  if (!modulo) { alert('Selecciona un módulo.'); return }
  if (!ra)     { alert('Selecciona el RA que evalúa este examen.'); return }
  if (!_fotosExamen.length) { alert('Elige primero las fotos del examen.'); return }
  if (document.getElementById('ia-c-consent')?.checked !== true) {
    alert('Confirma que entiendes que las fotos se envían al proveedor IA.')
    return
  }

  const sel = document.getElementById('ia-c-alumno')
  const nombre = sel && sel.selectedIndex > 0 ? sel.options[sel.selectedIndex].text : 'Alumno/a'
  const term = document.getElementById('ia-corregir-term')
  if (term) term.innerHTML = ''
  document.getElementById('ia-c-propuesta').style.display = 'none'
  _notaPropuesta = null
  _activeIaCmd = 'corregir'
  _setIaLoading('corregir', true)

  window.api.genCorreccion({
    modulo, ra, alumno: nombre,
    numero: v('ia-c-numero'),
    imagenes: _fotosExamen,
    proveedor: v('ia-c-prov'),
    anonimizar: document.getElementById('ia-c-anonimizar')?.checked === true,
    enunciado: v('ia-c-enunciado'),
  })
  void aid
}

// Respuestas del corrector: mismo terminal, y captura de la nota propuesta
window.api.onCorreccion(d => {
  const term = document.getElementById('ia-corregir-term')
  if (!term) return
  const texto = d && typeof d.text === 'string' ? d.text : ''
  const marca = texto.match(/NOTA_PROPUESTA:([\d.,]+)/)
  if (marca) {
    _notaPropuesta = parseFloat(String(marca[1]).replace(',', '.'))
    const caja = document.getElementById('ia-c-propuesta')
    const nota = document.getElementById('ia-c-nota')
    if (nota) nota.textContent = isNaN(_notaPropuesta) ? '—' : _notaPropuesta.toFixed(2)
    if (caja) caja.style.display = ''
  }
  termAppend('ia-corregir-term', d)
  if (d && d.type === 'done') {
    _setIaLoading('corregir', false)
    if (typeof _loteExamenTerminado === 'function' && _loteActual != null) {
      _loteExamenTerminado(_notaPropuesta)
      _notaPropuesta = null
    }
  }
})

/** La nota solo entra en el cuaderno cuando el profesorado pulsa aquí. */
async function iaGuardarNotaPropuesta() {
  const actId = Number(v('ia-c-actividad'))
  const aid   = Number(v('ia-c-alumno'))
  const aviso = document.getElementById('ia-c-guardado')
  if (!actId) { alert('Elige en qué actividad quieres guardar la nota.'); return }
  if (!aid)   { alert('Elige el alumno/a.'); return }
  if (_notaPropuesta == null || isNaN(_notaPropuesta)) { alert('Todavía no hay ninguna nota propuesta.'); return }
  try {
    await window.api.saveNota(aid, actId, Math.round(_notaPropuesta * 100) / 100)
    if (aviso) {
      aviso.textContent = '✓ Guardada. Revísala en Notas.'
      setTimeout(() => { aviso.textContent = '' }, 6000)
    }
  } catch (e) {
    alert('No se ha podido guardar: ' + e.message)
  }
}

// ── Corrección por lotes ─────────────────────────────────────────────────────
// El orden importa: primero se reparten las fotos y el reparto se VERIFICA en
// pantalla (sin gastar nada), después se corrige uno para calibrar el criterio y
// solo entonces se lanza el resto con los ajustes acordados.

let _lote = []            // [{numero, rutas, archivos, aviso, alumnoId, nota, estado}]
let _loteCola = []        // índices pendientes de corregir
let _loteActual = null
let _lotePausado = false  // pausa entre exámenes: el que está en curso termina

async function iaAgruparFotos() {
  const caja = document.getElementById('ia-c-lote')
  if (!_fotosExamen.length) { alert('Elige primero las fotos de la tanda.'); return }
  try {
    const r = await window.api.agruparFotos({
      imagenes: _fotosExamen,
      modo: v('ia-c-modo'),
      paginas: Number(v('ia-c-paginas')) || 0,
    })
    if (r.error) { caja.textContent = r.error; return }

    _lote = r.grupos.map(g => ({ ...g, alumnoId: '', nota: null, estado: '' }))
    const alumnos = await _alumnosDelModulo()
    const opciones = a => '<option value="">— sin asignar —</option>' + alumnos.map(al =>
      `<option value="${al.id}"${String(a) === String(al.id) ? ' selected' : ''}>` +
      `${esc(al.apellidos || '')}${al.apellidos && al.nombre ? ', ' : ''}${esc(al.nombre || '')}</option>`).join('')

    caja.innerHTML = `
      <div style="margin-bottom:6px">
        <b>${r.total_examenes}</b> exámenes · ${r.total_fotos} fotos ·
        ${r.paginas_por_examen} páginas por examen
        ${r.incidencias.length ? `<span style="color:var(--red)"> · ⚠ revisa ${r.incidencias.join(', ')}</span>` : ' · todo cuadra'}
      </div>
      <table style="width:100%;font-size:11px;border-collapse:collapse">
        <tr><th style="text-align:left">Nº</th><th style="text-align:left">Fotos</th>
            <th style="text-align:left">Alumno/a</th><th style="text-align:left">Estado</th></tr>
        ${_lote.map((g, i) => `
          <tr style="border-top:1px solid var(--border)">
            <td style="padding:3px 6px"><b>${esc(g.numero)}</b></td>
            <td style="padding:3px 6px;color:${g.aviso ? 'var(--red)' : 'var(--text3)'}">
              ${esc(g.archivos.join(' · '))}${g.aviso ? ' ⚠ ' + esc(g.aviso) : ''}</td>
            <td style="padding:3px 6px"><select onchange="iaAsignarAlumno(${i}, this.value)">${opciones(g.alumnoId)}</select></td>
            <td style="padding:3px 6px" id="ia-c-estado-${i}">—</td>
          </tr>`).join('')}
      </table>`
    document.getElementById('ia-c-lote-acciones').style.display = ''
    document.getElementById('ia-c-calibrado').style.display = 'none'
    document.getElementById('ia-c-resultados').style.display = 'none'
  } catch (e) {
    caja.textContent = 'No he podido agrupar: ' + e.message
  }
}

async function _alumnosDelModulo() {
  const mod = _modulos.find(m => m.key === v('ia-c-mod'))
  if (!mod) return []
  try {
    return (await window.api.getAlumnos(mod.id)).filter(a => a.estado === 'Activo')
  } catch { return [] }
}

function iaAsignarAlumno(i, id) { if (_lote[i]) _lote[i].alumnoId = id }

/** Atajo: el examen 01 al primero de la lista, el 02 al segundo… */
async function iaAsignarPorOrden() {
  if (!_lote.length) { alert('Verifica primero el reparto de las fotos.'); return }
  const alumnos = await _alumnosDelModulo()
  _lote.forEach((g, i) => { g.alumnoId = alumnos[i] ? String(alumnos[i].id) : '' })
  await iaAgruparFotos()   // repinta con las asignaciones ya puestas
  _lote.forEach((g, i) => { const s = document.querySelectorAll('#ia-c-lote select')[i]; if (s) s.value = g.alumnoId })
}

function _puedeCorregirLote() {
  if (!_lote.length) { alert('Verifica primero el reparto de las fotos.'); return false }
  if (!v('ia-c-ra')) { alert('Selecciona el RA que evalúa este examen.'); return false }
  if (document.getElementById('ia-c-consent')?.checked !== true) {
    alert('Confirma que entiendes que las fotos se envían al proveedor IA.')
    return false
  }
  return true
}

/** Refresca el contador y qué botones tienen sentido ahora mismo. */
function _pintarEstadoCola() {
  const hechos = _lote.filter(g => g.nota != null).length
  const prog = document.getElementById('ia-c-progreso')
  const pausar = document.getElementById('ia-c-pausar')
  const reanudar = document.getElementById('ia-c-reanudar')
  const descartar = document.getElementById('ia-c-descartar')
  const enCurso = _loteActual != null
  const quedan = _loteCola.length

  if (prog) {
    prog.textContent = !_lote.length ? ''
      : _lotePausado && quedan ? `en pausa · ${hechos} de ${_lote.length} corregidos · quedan ${quedan}`
      : enCurso ? `corrigiendo ${hechos + 1} de ${_lote.length}…`
      : `${hechos} de ${_lote.length} corregidos`
  }
  if (pausar)    pausar.style.display    = (enCurso || quedan) && !_lotePausado ? '' : 'none'
  if (reanudar)  reanudar.style.display  = _lotePausado && quedan ? '' : 'none'
  if (descartar) descartar.style.display = _lotePausado && quedan ? '' : 'none'
}

/** Pausa entre exámenes: el que ya está enviado se termina y se guarda. */
function iaPausarLote() {
  _lotePausado = true
  _pintarEstadoCola()
}

function iaReanudarLote() {
  if (!_loteCola.length) { _lotePausado = false; _pintarEstadoCola(); return }
  _lotePausado = false
  const siguiente = _loteCola.shift()
  _lanzarCorreccion(siguiente)
  _pintarEstadoCola()
}

/** Deja la tanda donde está: lo corregido se conserva y se puede guardar. */
function iaDescartarCola() {
  _loteCola = []
  _lotePausado = false
  _pintarEstadoCola()
  _pintarResultadosLote()
}

function _lanzarCorreccion(i) {
  const g = _lote[i]
  _loteActual = i
  const celda = document.getElementById(`ia-c-estado-${i}`)
  if (celda) celda.textContent = 'corrigiendo…'
  _pintarEstadoCola()
  _activeIaCmd = 'corregir'
  _setIaLoading('corregir', true)
  window.api.genCorreccion({
    modulo: v('ia-c-mod'), ra: v('ia-c-ra'),
    alumno: 'Alumno/a', numero: g.numero,
    imagenes: g.rutas,
    proveedor: v('ia-c-prov'),
    anonimizar: document.getElementById('ia-c-anonimizar')?.checked === true,
    enunciado: v('ia-c-enunciado'),
    ajustes: v('ia-c-ajustes'),
  })
}

function iaCorregirPrimero() {
  if (!_puedeCorregirLote()) return
  _loteCola = []
  _lotePausado = false
  document.getElementById('ia-corregir-term').innerHTML = ''
  _lanzarCorreccion(0)
}

function iaCorregirResto() {
  if (!_puedeCorregirLote()) return
  _loteCola = _lote.map((_, i) => i).filter(i => i > 0 && _lote[i].nota == null)
  if (!_loteCola.length) { alert('No queda ningún examen por corregir.'); return }
  _lotePausado = false
  const siguiente = _loteCola.shift()
  _lanzarCorreccion(siguiente)
}

/** Se llama al terminar cada examen de la tanda. */
function _loteExamenTerminado(nota) {
  if (_loteActual == null) return
  const g = _lote[_loteActual]
  if (g) {
    g.nota = nota
    g.estado = nota == null ? 'sin nota' : `${nota}`
    const celda = document.getElementById(`ia-c-estado-${_loteActual}`)
    if (celda) celda.textContent = g.estado
  }
  const primero = _loteActual === 0
  _loteActual = null

  if (_loteCola.length && _lotePausado) {
    // La pausa se pidió mientras este examen estaba en marcha: se guarda lo hecho
    // y la cola espera. Nada se pierde.
    _pintarEstadoCola()
    _pintarResultadosLote()
    return
  }
  if (_loteCola.length) {
    const siguiente = _loteCola.shift()
    setTimeout(() => _lanzarCorreccion(siguiente), 600)
    return
  }
  _pintarEstadoCola()
  if (primero) {
    // Calibración: ahora decide ella si hay que ajustar antes de seguir
    document.getElementById('ia-c-calibrado').style.display = ''
  }
  _pintarResultadosLote()
}

function _pintarResultadosLote() {
  const corregidos = _lote.filter(g => g.nota != null)
  if (!corregidos.length) return
  const caja = document.getElementById('ia-c-resultados')
  caja.style.display = ''
  caja.innerHTML = `
    <div style="font-size:12px;font-weight:700;margin-bottom:6px">
      Notas propuestas · marca las que aceptas</div>
    <table style="width:100%;font-size:11px;border-collapse:collapse">
      ${_lote.map((g, i) => g.nota == null ? '' : `
        <tr style="border-top:1px solid var(--border)">
          <td style="padding:3px 6px"><input type="checkbox" id="ia-c-ok-${i}" checked/></td>
          <td style="padding:3px 6px"><b>${esc(g.numero)}</b></td>
          <td style="padding:3px 6px">${g.alumnoId ? '' : '<span style="color:var(--red)">sin asignar</span>'}</td>
          <td style="padding:3px 6px"><input type="number" min="0" max="10" step="0.1"
              id="ia-c-nota-${i}" value="${g.nota}" style="width:64px"/></td>
        </tr>`).join('')}
    </table>
    <div class="form-row" style="margin-top:8px;align-items:flex-end">
      <div class="field" style="max-width:280px"><label>Actividad donde guardarlas</label>
        <select id="ia-c-act-lote"></select></div>
      <button class="btn btn-success btn-sm" onclick="iaGuardarNotasLote()">Guardar las marcadas</button>
      <span id="ia-c-lote-guardado" style="font-size:12px;color:var(--green)"></span>
    </div>`
  const origen = document.getElementById('ia-c-actividad')
  const destino = document.getElementById('ia-c-act-lote')
  if (origen && destino) destino.innerHTML = origen.innerHTML
}

async function iaGuardarNotasLote() {
  const actId = Number(v('ia-c-act-lote'))
  if (!actId) { alert('Elige en qué actividad se guardan.'); return }
  let n = 0, sinAsignar = 0
  for (let i = 0; i < _lote.length; i++) {
    const g = _lote[i]
    if (g.nota == null) continue
    if (document.getElementById(`ia-c-ok-${i}`)?.checked !== true) continue
    if (!g.alumnoId) { sinAsignar++; continue }
    const nota = parseFloat(document.getElementById(`ia-c-nota-${i}`).value)
    if (isNaN(nota)) continue
    try {
      await window.api.saveNota(Number(g.alumnoId), actId, Math.round(nota * 100) / 100)
      n++
    } catch (e) { console.error('nota no guardada', e) }
  }
  const aviso = document.getElementById('ia-c-lote-guardado')
  if (aviso) {
    aviso.textContent = `✓ ${n} nota(s) guardada(s)` +
      (sinAsignar ? ` · ${sinAsignar} sin alumno asignado` : '')
    setTimeout(() => { aviso.textContent = '' }, 8000)
  }
}

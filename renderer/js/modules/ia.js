// ASISTENTE IA
// ═══════════════════════════════════════════════════════════════

// Guarda el comando activo para enrutar respuestas al terminal correcto
let _activeIaCmd = null
let _activeIaBannerType = null
let _iaProgressTimer = null
let _iaProgressPhase = 0

// IDs de los selects de módulo en cada pestaña
const IA_MOD_SELS = ['ia-r-mod', 'ia-a-mod', 'ia-i-mod', 'ia-ap-mod', 'ia-t-mod']

// Módulos cuyo --modulo necesita RAs en el select
const IA_MOD_TO_RA = {
  'ia-r-mod': 'ia-r-ra',
  'ia-a-mod': 'ia-a-ra',
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
  // La pestaña Informe depende del módulo: recargar sus alumnos
  if (typeof iaInformeLoadAlumnos === 'function') iaInformeLoadAlumnos()

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
function _humanizeIaMessage(text) {
  const raw = String(text || '')
  const map = [
    ['RA_NO_EVALUADO', 'Faltan calificaciones en algunos Resultados de Aprendizaje. Completa la pestaña de Notas antes de generar el informe.'],
    ['RA_SUSPENDIDO', 'El alumno no cumple los criterios mínimos en algún RA. El resultado normativo es NO APTO.'],
    ['NOTA_INVALIDA', 'Se ha detectado un formato o rango de nota incorrecto (debe ser entre 0 y 10).'],
    ['PONDERACION_CERO', 'La suma de las ponderaciones de los RA es 0%. Revisa la configuración del módulo.'],
    ['ERROR_RED', 'No se ha podido conectar con el servidor de IA. Revisa tu conexión a internet o inténtalo más tarde.'],
  ]
  for (const [prefix, msg] of map) {
    if (raw.includes(prefix)) return msg
  }
  return raw.trim()
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
  const raw = String(text || '')
  return ['RA_NO_EVALUADO', 'RA_SUSPENDIDO', 'NOTA_INVALIDA', 'PONDERACION_CERO']
    .find(prefix => raw.includes(prefix)) || null
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
  const VALID = ['rubrica', 'actividad', 'informe', 'todo']
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
    }
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
    const type = _iaAlertTypeForCode(normCode)
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

// ── Informe: carga alumnos del módulo y auto-rellena notas por RA ────────────

async function iaInformeLoadAlumnos() {
  const key = v('ia-i-mod')
  const sel = document.getElementById('ia-i-alumno-sel')
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
  document.getElementById('ia-i-notas').value = ''
}

async function iaInformeAutoNotas() {
  const key     = v('ia-i-mod')
  const alumnoName = v('ia-i-alumno-sel')
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
    document.getElementById('ia-i-notas').value = notasPairs.join(',')
    const hint = document.getElementById('ia-i-notas-hint')
    if (hint) {
      hint.textContent = minExam != null
        ? `Criterio: APTO exige todos los RA >=5 y exámenes >=${minExam}.`
        : 'Criterio: APTO exige todos los RA >=5 (la media no compensa un RA suspenso).'
    }
    const notasEl = document.getElementById('ia-i-notas')
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

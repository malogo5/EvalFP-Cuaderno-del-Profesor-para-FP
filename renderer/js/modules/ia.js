// ASISTENTE IA
// ═══════════════════════════════════════════════════════════════

// Guarda el comando activo para enrutar respuestas al terminal correcto
let _activeIaCmd = null

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
function runIA(cmd) {
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
    opts.consent = document.getElementById('ia-i-consent')?.checked === true
    opts.anonimizar = document.getElementById('ia-i-anonimizar')?.checked === true
    if (!opts.consent) { alert('Confirma que entiendes el envío de datos académicos al proveedor IA.'); return }
  }

  if (cmd === 'todo') {
    opts.modulo    = v('ia-t-mod')
    opts.proveedor = v('ia-t-prov')
    if (!opts.modulo) { alert('Selecciona un módulo.'); return }
  }

  _activeIaCmd = cmd
  window.api.genIA(opts)
}

// Registrar listener de respuestas IA (una sola vez al cargar el módulo)
window.api.onIA(d => {
  const termId = _activeIaCmd ? `ia-${_activeIaCmd}-term` : 'ia-todo-term'
  termAppend(termId, d)
  // Al terminar con éxito: acceso directo a la carpeta de material
  if (d.type === 'done' && d.code === 0) _addMaterialBtn(termId)
  if (d.type === 'done' || d.type === 'error') _activeIaCmd = null
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

    // Construir mapa nota_alumno[actividad_id]
    // H6: nota efectiva = nota_rec (recuperación) si existe
    const ng = {}
    notasArr.forEach(n => { if (n.alumno_id === alumno.id) ng[n.actividad_id] = n.nota_rec ?? n.nota })

    // Nota por RA con el MISMO motor que Evaluaciones (ponderada por peso
    // de actividad, H4) — no media simple, para que el informe sea coherente
    const notasPorRA = ras.map(ra => {
      const actsRA = acts.filter(a => a.ra_id === ra.id)
      const graded = actsRA.map(a => ({ n: ng[a.id], p: a.peso || 0 })).filter(x => x.n != null)
      if (!graded.length) return null
      const totP  = graded.reduce((s, x) => s + x.p, 0)
      const media = totP > 0
        ? graded.reduce((s, x) => s + x.n * x.p, 0) / totP
        : graded.reduce((s, x) => s + x.n, 0) / graded.length
      return `${ra.id}:${media.toFixed(1)}`
    }).filter(Boolean)

    document.getElementById('ia-i-notas').value = notasPorRA.join(',')
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

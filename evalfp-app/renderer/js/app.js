// ═══════════════════════════════════════════════════════════════
// Estado global
// ═══════════════════════════════════════════════════════════════
let _modulos = []       // módulos activos del profesor
let _curMod  = null     // módulo activo seleccionado
let _alumnos = []
let _actividades = []
let _notasGrid = {}     // {alumno_id: {act_id: nota}}

const SECS = ['inicio','modulos','programacion','alumnos','notas','evaluaciones','dashboard','ia','ajustes']
const TITLES = {inicio:'Inicio',modulos:'Módulos',programacion:'Programación del Módulo',alumnos:'Alumnos',notas:'Registro de Notas',
  evaluaciones:'Evaluaciones',dashboard:'Dashboard',ia:'Asistente IA',ajustes:'Ajustes'}

let _modsDisponibles = []
let _modData = null
let _updateTimers = {}
const IA_TABS = ['rubrica','actividad','informe','apuntes','todo']
let _raPondTimers = {}
let _pesoTimers = {}
let _utRasState = null
let _toastTimer = null
let _toastEl = null

// ═══════════════════════════════════════════════════════════════
// Navegación
// ═══════════════════════════════════════════════════════════════
function go(el) {
  const sec = el.dataset.sec
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'))
  el.classList.add('active')
  goSection(sec)
}

function goSection(sec) {
  // Sincronizar nav-item activo
  document.querySelectorAll('.nav-item').forEach(n => {
    if (n.dataset.sec === sec) n.classList.add('active')
    else n.classList.remove('active')
  })
  SECS.forEach(s => document.getElementById('sec-'+s).style.display = s===sec ? '' : 'none')
  document.getElementById('topbar-title').textContent = TITLES[sec] || sec
  document.getElementById('topbar-sub').textContent = ''
  // Cargar datos de la sección
  if (sec === 'modulos')      renderModulos().then(() => renderModRasPanel(_curMod))
  if (sec === 'programacion') initModSelect('prog-mod-sel', loadProgramacion)
  if (sec === 'alumnos')      initModSelect('alumnos-mod-sel', loadAlumnos)
  if (sec === 'notas')        initModSelect('notas-mod-sel',   loadNotas)
  if (sec === 'evaluaciones') initModSelect('eval-mod-sel',    loadEvaluaciones)
  if (sec === 'dashboard')    initModSelect('dash-mod-sel',    loadDashboard)
  if (sec === 'ia')           initIaSection()
  if (sec === 'ajustes')      loadAjustes()
}

function initModSelect(selId, cb) {
  const sel = document.getElementById(selId)
  const prev = sel.value
  sel.innerHTML = _modulos.length
    ? _modulos.map(m => `<option value="${m.id}">${[m.abrev, m.curso||null, m.grupo].filter(Boolean).join(' · ')}</option>`).join('')
    : '<option value="">Sin módulos</option>'
  // El módulo activo del sidebar (_curMod) es la fuente de verdad: si el
  // profesor cambia de módulo en el desplegable lateral, TODAS las secciones
  // deben reflejarlo. (Antes `prev` tenía prioridad y las secciones ya
  // visitadas se quedaban clavadas en el módulo anterior.)
  if (_curMod && _modulos.find(m => m.id == _curMod.id)) sel.value = _curMod.id
  else if (prev && _modulos.find(m => m.id == prev)) sel.value = prev
  cb()
}

// ═══════════════════════════════════════════════════════════════
// Utils
// ═══════════════════════════════════════════════════════════════
const v   = id => { const e=document.getElementById(id); return e?e.value:'' }
const esc = s  => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')

// ═══════════════════════════════════════════════════════════════
// Bootstrap
// ═══════════════════════════════════════════════════════════════
const MODULE_SCRIPTS = [
  'js/utils/validators.js',
  'js/utils/rate-limiter.js',
  // csrf-token.js y session-manager.js eliminados: son utilidades web sin uso
  // en una app Electron local sin servidor ni autenticación de usuarios.
  // password-validator.js eliminado: la validación de API keys la hace validators.js.
  'js/modules/modulos.js',
  'js/modules/programacion.js',
  'js/modules/alumnos.js',
  'js/modules/notas.js',
  'js/modules/evaluaciones.js',
  'js/modules/dashboard.js',
  'js/modules/ia.js',
  'js/modules/ajustes.js',
]

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement('script')
    s.src = src
    s.onload = resolve
    s.onerror = () => reject(new Error('No se pudo cargar ' + src))
    document.body.appendChild(s)
  })
}

function registerWindowHandlers() {
  Object.assign(window, {
    go, goSection, initModSelect,
    renderModulos, selectMod, updateModBadge, renderModDropdown, toggleModDropdown, closeModDropdown,
    renderModRasPanel, delModulo, openAddModulo, confirmAddModulo, closeModal,
    selectCatCiclo, filterCatalogo, selectCatCard,
    loadProgramacion, updateRaPond, _refreshRaPondTotal, updateActividadPeso, updateActividadDesc,
    setEvalCount, addActividad, deleteActividadRow, _refreshPesoTotal, _getModData, _saveModData,
    saveUtField, addUt, deleteUt, openUtRasModal, _refreshUtHoras, _toggleRaSection, saveUtRas,
    closeUtRasModal, applyModuloPesos,
    loadAlumnos, renderAlumnosTable, updateAlumno, addAlumno, importAlumnos, confirmImportAlumnos, removeAlumno,
    loadNotas, renderNotasGrid, onNotaChange, colorNota, exportNotasPDF, toggleRecMode,
    loadEvaluaciones, setEvalTab, toggleEvalCard, toggleEvalCard2, toggleOrd2ShowAll, saveMinExam,
    loadDashboard, genBoletin, togglePardonCe, saveRec2Nota, setRecSort, toggleRecCard, setOrd1Sort, toggleOrd1Card,
    initIaSection, iaTab, termAppend, runIA, runApuntes,
    iaInformeLoadAlumnos, iaInformeAutoNotas,
    loadAjustes, saveAjustes, setTheme,
    v, esc, showSaved, evalLabel,
  })
}

// ═══════════════════════════════════════════════════════════════
// Init
// ═══════════════════════════════════════════════════════════════
async function init() {
  _modulos = await window.api.getModulos()
  if (_modulos.length) {
    _curMod = _modulos[0]
    updateModBadge()
    goSection('programacion')
  } else {
    goSection('modulos')
  }
}

// ═══════════════════════════════════════════════════════════════
// EDICIÓN INLINE — comportamiento tipo Excel
// ═══════════════════════════════════════════════════════════════

function setupInlineEditing() {
  // ── Toast "Guardado ✓" ──────────────────────────────────────────
  _toastEl = document.createElement('div')
  _toastEl.id = 'toast-saved'
  _toastEl.innerHTML = '✓ Guardado'
  document.body.appendChild(_toastEl)

  // Parchear updateAlumno para mostrar toast
  const _origUpdateAlumno = updateAlumno
  window.updateAlumno = function(id, field, val) {
    _origUpdateAlumno(id, field, val)
    showSaved()
  }

  // Parchear onNotaChange para mostrar toast
  const _origOnNotaChange = onNotaChange
  window.onNotaChange = function(el) {
    _origOnNotaChange(el)
    showSaved()
  }
}

function showSaved() {
  clearTimeout(_toastTimer)
  _toastEl.classList.add('show')
  _toastTimer = setTimeout(() => _toastEl.classList.remove('show'), 1400)
}

// Etiqueta canónica de evaluación: 1 → "1ª Evaluación", 2 → "2ª Evaluación"…
function evalLabel(n) {
  const ord = ['', '1ª', '2ª', '3ª', '4ª', '5ª'][n] || `${n}ª`
  return `${ord} Evaluación`
}

// ═══════════════════════════════════════════════════════════════
// Sidebar redimensionable
// ═══════════════════════════════════════════════════════════════
function initSidebarResize() {
  const sidebar  = document.getElementById('sidebar')
  const resizer  = document.getElementById('sidebar-resizer')
  if (!sidebar || !resizer) return

  // Restaurar ancho y tema guardados
  window.api.getAllConfig().then(cfg => {
    const w = parseInt(cfg.sidebarWidth)
    if (w >= 160 && w <= 400) {
      sidebar.style.width = w + 'px'
      document.documentElement.style.setProperty('--sidebar-w', w + 'px')
    }
    const theme = (cfg.theme || '').trim()
    if (theme) document.documentElement.dataset.theme = theme
  }).catch(() => {})

  let startX, startW
  resizer.addEventListener('mousedown', e => {
    e.preventDefault()
    startX = e.clientX
    startW = sidebar.offsetWidth
    resizer.classList.add('dragging')
    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'

    function onMove(e) {
      const w = Math.min(400, Math.max(160, startW + e.clientX - startX))
      sidebar.style.width = w + 'px'
      document.documentElement.style.setProperty('--sidebar-w', w + 'px')
    }
    function onUp() {
      resizer.classList.remove('dragging')
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
      document.removeEventListener('mousemove', onMove)
      document.removeEventListener('mouseup', onUp)
      window.api.setConfig('sidebarWidth', String(sidebar.offsetWidth)).catch(() => {})
    }
    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
  })
}

async function bootstrap() {
  for (const src of MODULE_SCRIPTS) await loadScript(src)
  registerWindowHandlers()
  init()
  setupInlineEditing()
  initSidebarResize()
}

bootstrap()

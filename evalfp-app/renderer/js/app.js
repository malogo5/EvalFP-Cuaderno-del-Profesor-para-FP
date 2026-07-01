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
  document.getElementById('topbar-sub').textContent = _curMod
    ? ([_curMod.abrev, _curMod.curso||null, _curMod.grupo].filter(Boolean).join(' · ')) : ''
  // Cargar datos de la sección
  if (sec === 'modulos')      renderModulos().then(() => renderModRasPanel(_curMod))
  if (sec === 'programacion') initModSelect('prog-mod-sel', loadProgramacion)
  if (sec === 'alumnos')      initModSelect('alumnos-mod-sel', loadAlumnos)
  if (sec === 'notas')        initModSelect('notas-mod-sel',   loadNotas)
  if (sec === 'evaluaciones') initModSelect('eval-mod-sel',    loadEvaluaciones)
  if (sec === 'dashboard')    initModSelect('dash-mod-sel',    loadDashboard)
  if (sec === 'ajustes')      loadAjustes()
}

function initModSelect(selId, cb) {
  const sel = document.getElementById(selId)
  const prev = sel.value
  sel.innerHTML = _modulos.length
    ? _modulos.map(m => `<option value="${m.id}">${[m.abrev, m.curso||null, m.grupo].filter(Boolean).join(' · ')}</option>`).join('')
    : '<option value="">Sin módulos</option>'
  if (prev && _modulos.find(m => m.id == prev)) sel.value = prev
  else if (_curMod) sel.value = _curMod.id
  cb()
}

// ═══════════════════════════════════════════════════════════════
// MÓDULOS
// ═══════════════════════════════════════════════════════════════
async function renderModulos() {
  _modulos = await window.api.getModulos()
  const el = document.getElementById('mod-cards-list')
  if (!_modulos.length) {
    el.innerHTML = '<div style="color:var(--text2);padding:20px;grid-column:1/-1">No hay módulos. Añade uno para empezar.</div>'
    document.getElementById('mod-badge').style.display = 'none'
    return
  }
  el.innerHTML = _modulos.map(m => `
    <div class="mod-card ${_curMod?.id===m.id?'active-mod':''}" onclick="selectMod(${m.id})">
      <button class="mod-card-del" onclick="event.stopPropagation();delModulo(${m.id})" title="Eliminar">✕</button>
      <div class="mod-card-abrev">${m.abrev}</div>
      <div class="mod-card-nombre">${m.nombre}</div>
      <div class="mod-card-meta">
        ${m.ciclo||''} · ${m.curso||''} · ${m.anno||''}<br>
        Grupo: <b>${m.grupo}</b>
        ${m.decreto ? `<br><span style="color:var(--accent2)">${m.decreto}</span>` : ''}
      </div>
    </div>
  `).join('')
  // Actualizar badge sidebar
  if (_curMod) {
    updateModBadge()
  }
}

function selectMod(id) {
  _curMod = _modulos.find(m => m.id === id)
  updateModBadge()
  renderModulos()
  renderModRasPanel(_curMod)
  closeModDropdown()
}

// ── Dropdown sidebar ────────────────────────────────────────────
function updateModBadge() {
  // Badge oculto por diseño — solo actualizamos el nombre interno para que el JS no rompa
  if (_curMod) {
    document.getElementById('mod-badge-name').textContent =
      _curMod.abrev + ' · ' + (_curMod.curso || '') + (_curMod.grupo ? ' · ' + _curMod.grupo : '')
  }
}

function renderModDropdown() {
  const dd = document.getElementById('mod-dropdown')
  if (!dd) return
  dd.innerHTML = _modulos.map(m => `
    <div class="mod-dd-item ${m.id === _curMod?.id ? 'sel' : ''}"
         onclick="event.stopPropagation();selectMod(${m.id})">
      <span class="mod-dd-abrev">${m.abrev}</span>
      <div class="mod-dd-info">
        <div class="mod-dd-nombre">${m.nombre}</div>
        <div class="mod-dd-meta">${[m.curso, m.grupo].filter(Boolean).join(' · ')}</div>
      </div>
    </div>
  `).join('')
}

function toggleModDropdown(e) {
  e.stopPropagation()
  const badge = document.getElementById('mod-badge')
  const isOpen = badge.classList.contains('open')
  if (!isOpen) renderModDropdown()
  badge.classList.toggle('open', !isOpen)
}

function closeModDropdown() {
  document.getElementById('mod-badge')?.classList.remove('open')
}

// Cerrar al hacer clic fuera
document.addEventListener('click', () => closeModDropdown())

function renderModRasPanel(mod) {
  const panel = document.getElementById('mod-ras-panel')
  if (!mod) { panel.innerHTML = ''; return }
  const data = mod.data_json ? JSON.parse(mod.data_json) : null
  if (!data?.ras?.length) { panel.innerHTML = ''; return }
  const ras = data.ras
  const ces = data.ces || {}
  let html = `
    <div style="font-size:12px;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px">
      RAs y Criterios de Evaluación — ${mod.abrev}
    </div>
    <div style="display:flex;flex-direction:column;gap:8px">`
  for (const ra of ras) {
    const raCes = ces[ra.id] || []
    html += `
      <div class="card" style="border-left:3px solid var(--accent2);padding:12px 16px">
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:${raCes.length?'8px':'0'}">
          <span style="font-size:12px;font-weight:700;color:var(--accent2);min-width:34px">${ra.id}</span>
          <span style="font-size:12px;font-weight:600;flex:1">${ra.nombre}</span>
          ${ra.pond ? `<span style="font-size:11px;background:var(--navy3);padding:2px 7px;border-radius:10px;color:var(--accent)">${ra.pond}%</span>` : ''}
        </div>
        ${raCes.length ? `<div style="margin-left:44px">${raCes.map(ce => `
          <div style="display:flex;gap:8px;padding:3px 0;border-top:1px solid var(--border);font-size:11px;color:var(--text2)">
            <span style="color:var(--accent);font-weight:600;min-width:26px">${ce.id}</span>
            <span>${ce.texto}</span>
          </div>`).join('')}</div>` : ''}
      </div>`
  }
  html += '</div>'
  panel.innerHTML = html
}

async function delModulo(id) {
  if (!confirm('¿Eliminar este módulo? Se borrarán también los alumnos y notas asociados.')) return
  await window.api.deleteModulo(id)
  if (_curMod?.id === id) _curMod = null
  await renderModulos()
  renderModRasPanel(_curMod)
}

// ── Modal añadir módulo ──
let _modsDisponibles = []
let _modData = null

async function openAddModulo() {
  _modsDisponibles = await window.api.listModulosDisponibles()
  const sel = document.getElementById('add-mod-key')

  // Agrupar por ciclo_clave
  const CICLO_LABELS = {
    'CFGB':     'CFGB — Informática de Oficina',
    'SMR':      'CFGM — Sistemas Microinformáticos y Redes (SMR)',
    'ASIR':     'CFGS — Administración de Sistemas Informáticos en Red (ASIR)',
    'DAM':      'CFGS — Desarrollo de Aplicaciones Multiplataforma (DAM)',
    'DAW':      'CFGS — Desarrollo de Aplicaciones Web (DAW)',
    'CE_CIBER': 'CE — Ciberseguridad en Entornos de las TI',
    'CE_IABD':   'CE — Inteligencia Artificial y Big Data',
    'CE_PYTHON': 'CE — Desarrollo de Aplicaciones en Python',
    'OTRO':     'Otros módulos',
  }
  const grupos = {}
  for (const m of _modsDisponibles) {
    const clave = m.ciclo_clave || 'OTRO'
    if (!grupos[clave]) grupos[clave] = []
    grupos[clave].push(m)
  }
  const orden = ['CFGB','SMR','ASIR','DAM','DAW','CE_CIBER','CE_IABD','CE_PYTHON','OTRO']
  let html = '<option value="">— Selecciona un módulo —</option>'
  for (const clave of orden) {
    if (!grupos[clave]) continue
    const label = CICLO_LABELS[clave] || clave
    html += `<optgroup label="${label}">`
    for (const m of grupos[clave]) {
      html += `<option value="${m.key}">${m.abrev} — ${m.nombre}${m.curso ? ' ('+m.curso+')' : ''}</option>`
    }
    html += '</optgroup>'
  }
  sel.innerHTML = html

  document.getElementById('add-mod-preview').textContent = 'Selecciona un módulo para ver sus datos.'
  document.getElementById('add-mod-grupo').value = ''
  document.getElementById('add-mod-grupo').style.opacity = '0.6'
  _modData = null
  document.getElementById('modal-add-mod').classList.add('open')
}

async function previewModulo() {
  const key = document.getElementById('add-mod-key').value
  if (!key) { _modData = null; return }
  document.getElementById('add-mod-preview').textContent = 'Cargando datos normativos…'
  try {
    _modData = await window.api.getModuloData(key)
    const m = _modData.modulo
    const horas = m.total_horas || m.horas || '?'
    document.getElementById('add-mod-preview').innerHTML =
      `<b style="color:var(--ice)">${m.abrev} — ${m.nombre}</b><br>
      ${[m.ciclo, m.curso, m.anno].filter(Boolean).join(' · ')}<br>
      ${horas}h · ${_modData.ras.length} RAs · ${_modData.uts.length} UTs · ${_modData.actividades.length} actividades`
    if (m.decreto) document.getElementById('add-mod-preview').innerHTML +=
      `<br><span style="color:var(--accent2)">${m.decreto}</span>`
  } catch(e) {
    document.getElementById('add-mod-preview').textContent = '⚠️ Error cargando módulo: ' + e.message
    _modData = null
  }
}

async function confirmAddModulo() {
  if (!_modData) return alert('Selecciona un módulo primero.')
  const key = document.getElementById('add-mod-key').value
  // Comprobar si ya existe
  if (_modulos.find(m => m.key === key)) {
    return alert(`El módulo "${key.replace('_data','').toUpperCase()}" ya está añadido.\nPara cambiar el grupo, elimínalo y vuelve a añadirlo.`)
  }
  const m = _modData.modulo
  const grupo = document.getElementById('add-mod-grupo').value.trim()
  try {
    await window.api.addModulo({
      key,
      abrev:  m.abrev,
      nombre: m.nombre,
      ciclo:  m.ciclo,
      curso:  m.curso,
      anno:   m.anno,
      grupo,
      horas:  m.total_horas || m.horas || 0,
      decreto: m.decreto || null,
      actividades: _modData.actividades,
      data: _modData,
    })
    closeModal()
    _modulos = await window.api.getModulos()
    _curMod  = _modulos.find(m => m.key === key) || _modulos[0]
    renderModulos()
  } catch(e) {
    alert('Error al guardar el módulo: ' + e.message)
  }
}

function closeModal() {
  document.getElementById('modal-add-mod').classList.remove('open')
}

// ═══════════════════════════════════════════════════════════════
// ALUMNOS
// ═══════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════
// PROGRAMACIÓN — Vista completa tipo Excel
// ═══════════════════════════════════════════════════════════════
async function loadProgramacion() {
  const mid = document.getElementById('prog-mod-sel').value
  if (!mid) return
  const mod = _modulos.find(m => m.id == mid)
  if (!mod) return
  const data = mod.data_json ? JSON.parse(mod.data_json) : null
  const panel = document.getElementById('prog-panel')
  if (!data || !data.ras?.length) {
    panel.innerHTML = '<div style="color:var(--text2);padding:20px">Este módulo no tiene datos de RAs/CEs cargados.</div>'
    return
  }

  const ras        = data.ras        || []
  const ces        = data.ces        || {}
  const uts        = data.uts        || []
  const asigs      = data.asignaciones || []  // [{ut,ra,ces:[CRx...]}]
  const evalRas    = data.eval_ras   || {}    // {1:[RA1,RA2], 2:[RA3]}
  const raInstr    = data.ra_instrumentos || {}
  // Cargar actividades desde BD (tienen los pesos reales editados por el profesor)
  const actividades = (await window.api.getActividades(parseInt(mid))) || data.actividades || []

  // Cargar overrides de ponderación de RAs y mezclar con los defaults del JSON
  const raPondOverrides = {}
  try {
    const rows = await window.api.getRaPonderaciones(parseInt(mid))
    rows.forEach(r => { raPondOverrides[r.ra_id] = r.pond })
  } catch(e) {}
  // Aplicar overrides al raMap
  ras.forEach(ra => {
    if (raPondOverrides[ra.id] !== undefined) ra.pond = raPondOverrides[ra.id]
  })

  // índices rápidos
  const utMap  = Object.fromEntries(uts.map(u => [u.id, u]))
  const raMap  = Object.fromEntries(ras.map(r => [r.id, r]))
  const evalCount = data.modulo?.eval_count || [...new Set(uts.map(u => u.eval||1))].length || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)

  // ── cabecera ──────────────────────────────────────────────────
  let h = `
  <div class="card" style="margin-bottom:16px;padding:16px 20px;border-left:4px solid var(--accent)">
    <div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap">
      <span style="font-size:24px;font-weight:800;color:var(--accent2)">${mod.abrev}</span>
      <span style="font-size:15px;font-weight:600">${mod.nombre}</span>
      <span style="font-size:12px;background:var(--navy3);padding:2px 10px;border-radius:10px;color:var(--text2)">${mod.horas||'?'} h</span>
      <span style="font-size:12px;background:var(--navy3);padding:2px 10px;border-radius:10px;color:var(--text2)">${ras.length} RAs · ${uts.length} UTs</span>
    </div>
    ${mod.decreto ? `<div style="font-size:11px;color:var(--accent2);margin-top:6px">📜 ${mod.decreto}</div>` : ''}
  </div>`

  // ── 1. TABLA DE UNIDADES DE TRABAJO ──────────────────────────
  const _sumUtH  = uts.reduce((s,u) => s+(u.horas||0), 0)
  const _modH    = mod.horas || 0
  const _hOk     = _sumUtH === _modH
  const _hBadgeSt = _hOk
    ? 'background:rgba(16,185,129,.12);color:var(--green)'
    : 'background:rgba(245,158,11,.15);color:var(--amber)'
  h += `<div class="card" style="margin-bottom:16px">
    <div class="prog-section-title" style="display:flex;align-items:center;gap:10px">
      📚 Unidades de Trabajo
      <span id="ut-horas-badge" style="font-size:10.5px;padding:2px 10px;border-radius:8px;font-weight:700;${_hBadgeSt}">
        Σ ${_sumUtH}h / ${_modH}h${_hOk?' ✓':' ⚠'}
      </span>
    </div>
    <div style="overflow-x:auto">
    <table class="prog-table">
      <thead><tr>
        <th style="width:52px">UT</th>
        <th>Nombre</th>
        <th style="width:62px;text-align:center">Horas</th>
        <th style="width:48px;text-align:center">Eval</th>
        <th style="width:52px;text-align:center">RA</th>
        <th>Contenidos clave</th>
        <th style="width:96px;text-align:center">Acciones</th>
      </tr></thead>
      <tbody>`
  for (const ut of uts) {
    const asig = asigs.find(a => a.ut === ut.id)
    const raId = asig ? asig.ra : '—'
    const raColor = raId !== '—' ? 'var(--accent2)' : 'var(--text2)'
    h += `<tr>
      <td style="font-weight:700;color:var(--accent2);white-space:nowrap">${ut.id}</td>
      <td><input class="nota-cell" type="text" value="${esc(ut.nombre)}"
        style="width:100%;min-width:160px;text-align:left;font-weight:500"
        onchange="saveUtField(${mid},'${ut.id}','nombre',this.value)"/></td>
      <td style="text-align:center">
        <input class="peso-cell ut-horas-inp" type="number" min="0" max="999" value="${ut.horas||0}"
          oninput="_refreshUtHoras(this,${_modH})"
          onchange="saveUtField(${mid},'${ut.id}','horas',this.value)"/></td>
      <td style="text-align:center">
        <select class="nota-cell" style="width:46px;padding:3px 2px;text-align:center;font-weight:600"
          onchange="saveUtField(${mid},'${ut.id}','eval',this.value)">
          ${evals.map(e=>`<option value="${e}"${ut.eval==e?' selected':''}>${e}</option>`).join('')}
        </select></td>
      <td style="text-align:center;font-weight:700;color:${raColor}">${raId}</td>
      <td><input class="nota-cell" type="text" value="${esc(ut.tags||'')}"
        style="width:100%;text-align:left;font-size:11px;color:var(--text2)"
        onchange="saveUtField(${mid},'${ut.id}','tags',this.value)"/></td>
      <td style="text-align:center;white-space:nowrap">
        <button onclick="openUtRasModal(${mid},'${ut.id}')" title="Asignar RAs y CEs"
          style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:3px 9px;font-size:11px;font-weight:700;cursor:pointer;margin-right:4px">RA/CE</button>
        <button onclick="deleteUt(${mid},'${ut.id}')" title="Eliminar UT"
          style="background:transparent;color:#ef4444;border:1px solid rgba(239,68,68,.35);border-radius:6px;padding:3px 8px;font-size:11px;cursor:pointer">✕</button>
      </td>
    </tr>`
  }
  h += `</tbody></table></div>
    <div style="padding:10px 2px 2px">
      <button onclick="addUt(${mid})"
        style="background:transparent;color:var(--accent);border:1.5px solid var(--accent);border-radius:8px;padding:5px 16px;font-size:12px;font-weight:700;cursor:pointer">+ Añadir UT</button>
    </div>
  </div>`

  // ── 2. RESULTADOS DE APRENDIZAJE Y CRITERIOS DE EVALUACIÓN ───
  const totalRaPond = ras.reduce((s, r) => s + (r.pond || 0), 0)
  const raPondOk    = ras.every(r => r.pond) && Math.abs(totalRaPond - 100) < 0.1
  const raSumBadge  = ras.some(r => r.pond)
    ? (raPondOk
        ? `<span data-rapond-total style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700;margin-left:auto">✓ 100%</span>`
        : `<span data-rapond-total style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700;margin-left:auto">⚠ suma ${totalRaPond}%</span>`)
    : ''

  h += `<div class="card" style="margin-bottom:16px">
    <div class="prog-section-title">🎯 Resultados de Aprendizaje y Criterios de Evaluación
      ${raSumBadge}
    </div>
    <div style="display:flex;flex-direction:column;gap:10px">`

  for (const ra of ras) {
    const raCes = ces[ra.id] || []
    // saber en qué eval cae este RA
    let raEval = '—'
    for (const [ev, raList] of Object.entries(evalRas)) {
      if (raList.includes(ra.id)) { raEval = `Eval ${ev}`; break }
    }
    const instrList = raInstr[ra.id] || []
    const instrStr  = instrList.map(i =>
      i==='practica'?'Práctica':i==='examen'?'Examen':i==='proyecto'?'Proyecto':
      i==='informe'?'Informe':i==='presentacion'?'Presentación':i
    ).join(' + ')
    // qué UT(s) evalúa
    const utAsigs = asigs.filter(a => a.ra === ra.id).map(a => a.ut)

    // Input editable de ponderación (con tooltip explicativo)
    const pondInput = `<span style="display:inline-flex;align-items:center;gap:4px;background:rgba(0,0,0,.15);border-radius:8px;padding:2px 8px 2px 4px">
      <input class="ra-pond-cell" type="number" min="0" max="100" step="1"
        value="${ra.pond || ''}" placeholder="—"
        data-mid="${mid}" data-raid="${ra.id}"
        oninput="_refreshRaPondTotal(this)"
        onchange="updateRaPond(this)"
        title="Ponderación de este RA en la nota final (%)"/>
      <span style="font-size:11px;color:rgba(255,255,255,.6);font-weight:600">%</span>
    </span>`

    h += `<div style="border:1px solid var(--border);border-left:4px solid var(--accent2);border-radius:8px;overflow:hidden">
      <div style="background:var(--bg3);padding:10px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
        <span style="font-size:13px;font-weight:800;color:var(--accent2);min-width:38px">${ra.id}</span>
        <span style="font-size:13px;font-weight:600;flex:1">${ra.nombre}</span>
        ${pondInput}
        <span class="badge">${raEval}</span>
        ${utAsigs.length ? `<span class="badge">${utAsigs.join(', ')}</span>` : ''}
        ${instrStr ? `<span class="badge badge-green">${instrStr}</span>` : ''}
      </div>`

    if (raCes.length) {
      h += `<div style="padding:8px 16px 10px 16px">
        <table style="width:100%;border-collapse:collapse">`
      for (const ce of raCes) {
        h += `<tr style="border-top:1px solid var(--border)">
          <td style="padding:4px 10px 4px 0;font-size:12px;font-weight:700;color:var(--accent);white-space:nowrap;vertical-align:top">${ce.id}</td>
          <td style="padding:4px 0;font-size:12px;color:var(--text2);line-height:1.5">${ce.texto}</td>
        </tr>`
      }
      h += `</table></div>`
    }
    h += `</div>`
  }
  h += `</div></div>`

  // ── 3. MAPA DE ASIGNACIONES UT → RA → CEs ────────────────────
  if (asigs.length) {
    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title">🔗 Mapa UT → RA → Criterios</div>
      <div style="overflow-x:auto">
      <table class="prog-table">
        <thead><tr>
          <th style="width:50px">UT</th>
          <th style="width:110px">Unidad</th>
          <th style="width:50px;text-align:center">RA</th>
          <th>Criterios de evaluación asignados</th>
        </tr></thead>
        <tbody>`
    for (const a of asigs) {
      const ut = utMap[a.ut] || {}
      const ra = raMap[a.ra] || {}
      const ceList = (ces[a.ra] || []).filter(ce => a.ces.includes(ce.id))
      h += `<tr>
        <td style="font-weight:700;color:var(--accent2);vertical-align:top;padding-top:8px">${a.ut}</td>
        <td style="font-size:11px;color:var(--text2);vertical-align:top;padding-top:8px;line-height:1.4">${ut.nombre||''}</td>
        <td style="text-align:center;font-weight:700;color:var(--accent2);vertical-align:top;padding-top:8px">${a.ra}</td>
        <td style="padding:4px 0">${ceList.map(ce =>
          `<div style="display:flex;gap:6px;padding:3px 0;border-top:1px solid var(--border);font-size:11px">
            <span style="color:var(--accent);font-weight:700;white-space:nowrap">${ce.id}</span>
            <span style="color:var(--text2)">${ce.texto}</span>
          </div>`
        ).join('')}</td>
      </tr>`
    }
    h += `</tbody></table></div></div>`
  }

  // ── 4. PLAN DE ACTIVIDADES POR EVALUACIÓN ────────────────────
  {
    const _e0acts = actividades.filter(a => a.eval === evals[0])
    const _initPrac = Math.round(_e0acts.filter(a => a.tipo==='practica').reduce((s,a)=>s+(a.peso||0),0)) || 30
    const _initExam = Math.round(_e0acts.filter(a => a.tipo==='examen'  ).reduce((s,a)=>s+(a.peso||0),0)) || 70
    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
        📝 Plan de Actividades y Evaluación
        <span style="margin-left:auto;display:flex;align-items:center;gap:7px;font-size:12px;font-weight:400">
          <span style="color:var(--text2)">Evaluaciones</span>
          <select onchange="setEvalCount(${mid},this.value)"
            style="border:1.5px solid var(--border2);border-radius:8px;padding:3px 10px;font-size:12px;font-weight:700;color:var(--text);background:var(--bg);cursor:pointer;font-family:inherit">
            ${[2,3].map(n=>`<option value="${n}"${evalCount==n?' selected':''}>${n}</option>`).join('')}
          </select>
        </span>
      </div>
      <div style="display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--bg4);border:1px solid var(--border2);border-radius:10px;margin:10px 0 18px;flex-wrap:wrap">
        <span style="font-size:12px;font-weight:700;color:var(--text2);white-space:nowrap">Ponderación del módulo</span>
        <div style="display:flex;align-items:center;gap:6px">
          <span style="font-size:12px;color:var(--text2)">Prácticas</span>
          <input id="mod-peso-prac" type="number" min="0" max="100" step="5" value="${_initPrac}" class="peso-cell" style="width:58px"
            oninput="const e=document.getElementById('mod-peso-exam');if(e)e.value=Math.max(0,100-(+this.value||0))"/>
          <span style="font-size:11px;color:var(--text3)">%</span>
        </div>
        <span style="color:var(--text3)">/</span>
        <div style="display:flex;align-items:center;gap:6px">
          <span style="font-size:12px;color:var(--text2)">Exámenes</span>
          <input id="mod-peso-exam" type="number" min="0" max="100" step="5" value="${_initExam}" class="peso-cell" style="width:58px"
            oninput="const e=document.getElementById('mod-peso-prac');if(e)e.value=Math.max(0,100-(+this.value||0))"/>
          <span style="font-size:11px;color:var(--text3)">%</span>
        </div>
        <button onclick="applyModuloPesos()" style="background:var(--accent);color:#fff;border:none;border-radius:8px;padding:5px 14px;font-size:12px;font-weight:700;cursor:pointer">Aplicar a todo el módulo</button>
      </div>`

    // qué RAs caen en cada eval (desde evalRas o inferido de UTs)
    const evalRasMap = {}
    if (Object.keys(evalRas).length) {
      for (const [ev, raList] of Object.entries(evalRas))
        evalRasMap[String(ev)] = raList
    } else {
      // inferir desde asigs+uts
      for (const ut of uts) {
        const ev = String(ut.eval||1)
        const asig = asigs.find(a => a.ut === ut.id)
        if (asig) {
          if (!evalRasMap[ev]) evalRasMap[ev] = []
          if (!evalRasMap[ev].includes(asig.ra)) evalRasMap[ev].push(asig.ra)
        }
      }
    }

    for (const ev of evals) {
      const acts = actividades.filter(a => a.eval === ev).sort((a,b) => {
        if (a.tipo !== b.tipo) return a.tipo === 'practica' ? -1 : 1
        return (a.orden||0) - (b.orden||0)
      })
      const rasEv = evalRasMap[String(ev)] || []
      const rasEvalStr = rasEv.map(raId => {
        const ra = raMap[raId] || {}
        return `${raId}${ra.pond ? ` (${ra.pond}%)` : ''}`
      }).join(' · ')

      const totalPeso = acts.reduce((s,a) => s + (a.peso||0), 0)
      const pesoOk = Math.abs(totalPeso - 100) < 0.1
      const pesoWarn = acts.length
        ? (!pesoOk
          ? `<span data-pesobadge style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700;margin-left:8px">⚠ suma ${totalPeso}%</span>`
          : `<span data-pesobadge style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700;margin-left:8px">✓ 100%</span>`)
        : ''
      const btnSt = 'border:none;border-radius:7px;padding:4px 12px;font-size:11.5px;font-weight:700;cursor:pointer'
      h += `<div style="margin-bottom:14px">
        <div style="font-size:12px;font-weight:700;color:var(--ice);background:var(--navy3);padding:7px 14px;border-radius:6px;margin-bottom:6px;display:flex;gap:12px;align-items:center">
          <span>Evaluación ${ev}</span>
          ${rasEvalStr ? `<span style="font-size:11px;font-weight:400;color:var(--text2)">${rasEvalStr}</span>` : ''}
          ${pesoWarn}
        </div>`
      if (acts.length) {
        h += `<table class="prog-table">
          <thead><tr>
            <th style="width:30px">#</th>
            <th>Actividad</th>
            <th style="width:80px;text-align:center">Instrumento</th>
            <th style="width:55px;text-align:center">Tipo</th>
            <th class="th-editable" style="width:70px;text-align:center">Peso %</th>
            <th class="th-editable" style="width:70px;text-align:center">Nota máx</th>
            <th style="width:50px;text-align:center">UT/RA</th>
            <th style="width:30px"></th>
          </tr></thead>
          <tbody>`
        for (const act of acts) {
          const badge = act.tipo==='examen'
            ? 'background:rgba(224,160,58,.2);color:var(--amber)'
            : 'background:rgba(74,144,217,.15);color:var(--accent2)'
          const actId = act.id || ''
          h += `<tr>
            <td style="text-align:center;color:var(--text2);font-size:11px">${act.orden||''}</td>
            <td>${actId
              ? `<input class="nota-cell" type="text" value="${esc(act.descripcion)}"
                  data-actid="${actId}" data-field="descripcion"
                  style="width:100%;text-align:left;font-size:12px"
                  onchange="updateActividadDesc(this)"/>`
              : `<span style="font-size:12px">${esc(act.descripcion)}</span>`}
            </td>
            <td style="text-align:center"><span style="font-size:11px;padding:2px 7px;border-radius:8px;${badge}">${act.instrumento}</span></td>
            <td style="text-align:center;font-size:11px;color:var(--text2)">${act.tipo}</td>
            <td style="text-align:center">
              ${actId ? `<input class="peso-cell" type="number" min="0" max="100" step="1"
                value="${act.peso}" data-actid="${actId}"
                oninput="_refreshPesoTotal(this,[])"
                onchange="updateActividadPeso(this)"
                title="Peso (%)"/>` : `<span style="font-weight:700;color:var(--accent)">${act.peso}%</span>`}
            </td>
            <td style="text-align:center">
              ${actId ? `<input class="peso-cell" type="number" min="0" max="10" step="0.5"
                value="${act.nota_max}" data-actid="${actId}" data-field="nota_max"
                onchange="updateActividadPeso(this)"
                title="Nota máxima"/>` : `<span style="color:var(--text2)">${act.nota_max}</span>`}
            </td>
            <td style="text-align:center;font-size:11px;color:var(--text2)">${act.ut_id||act.ra_id||'—'}</td>
            <td style="text-align:center">${actId
              ? `<button onclick="deleteActividadRow(${actId})" title="Eliminar"
                  style="background:transparent;color:#ef4444;border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:2px 6px;font-size:11px;cursor:pointer;line-height:1">✕</button>`
              : ''}</td>
          </tr>`
        }
        h += `</tbody></table>`
      }
      h += `<div style="display:flex;gap:8px;padding:8px 2px 2px">
          <button onclick="addActividad(${mid},${ev},'practica')"
            style="${btnSt}background:rgba(74,144,217,.12);color:var(--accent2)">+ Práctica</button>
          <button onclick="addActividad(${mid},${ev},'examen')"
            style="${btnSt}background:rgba(224,160,58,.12);color:var(--amber)">+ Examen</button>
        </div>
      </div>`
    }
    h += `</div>`
  }

  // ── 5. DISTRIBUCIÓN EVALUACIÓN (RAs por eval) ─────────────────
  // Distribución derivada de las UTs: qué RA está asignado a cada UT y en qué eval está
  const distRasMap = {}
  for (let e = 1; e <= evalCount; e++) distRasMap[e] = []
  for (const ut of uts) {
    const ev = ut.eval || 1
    if (ev < 1 || ev > evalCount) continue
    const asig = asigs.find(a => a.ut === ut.id)
    if (asig?.ra && !distRasMap[ev].includes(asig.ra)) distRasMap[ev].push(asig.ra)
  }

  // Renderizar todas las evaluaciones activas
  if (evals.length) {
    h += `<div class="card" style="margin-bottom:8px">
      <div class="prog-section-title">📊 Distribución de RAs por Evaluación</div>
      <div style="display:flex;gap:12px;flex-wrap:wrap">`
    for (const ev of evals) {
      const raList = distRasMap[ev] || []
      const totalPond = raList.reduce((s, raId) => s + (raMap[raId]?.pond||0), 0)
      h += `<div style="flex:1;min-width:180px;background:var(--navy3);border-radius:8px;padding:12px 16px">
        <div style="font-size:12px;font-weight:700;color:var(--ice);margin-bottom:8px">Evaluación ${ev}
          <span style="font-weight:400;color:var(--text2);font-size:11px;margin-left:6px">${totalPond}% del módulo</span>
        </div>`
      if (!raList.length) {
        h += `<div style="font-size:11px;color:var(--text2);padding:4px 0;font-style:italic">Sin RAs asignados</div>`
      }
      for (const raId of raList) {
        const ra = raMap[raId] || {}
        const instrList = raInstr[raId] || []
        const instrStr = instrList.map(i =>
          i==='practica'?'Práctica':i==='examen'?'Examen':i==='proyecto'?'Proyecto':
          i==='informe'?'Informe':i==='presentacion'?'Presentación':i
        ).join('+')
        h += `<div style="display:flex;gap:8px;padding:4px 0;border-top:1px solid var(--border);align-items:baseline">
          <span style="font-weight:700;color:var(--accent2);min-width:34px">${raId}</span>
          <span style="font-size:11px;color:var(--text2);flex:1;line-height:1.3">${ra.nombre||''}</span>
          <span class="badge badge-accent">${ra.pond||0}%</span>
        </div>`
      }
      h += `</div>`
    }
    h += `</div></div>`
  }

  panel.innerHTML = h
}

async function loadAlumnos() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) return
  _alumnos = await window.api.getAlumnos(mid)
  renderAlumnosTable()
}

function renderAlumnosTable() {
  const tbody = document.getElementById('alumnos-tbody')
  const mod = _modulos.find(m => m.id == document.getElementById('alumnos-mod-sel').value)
  if (!_alumnos.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="color:var(--text2);text-align:center;padding:20px">Sin alumnos. Añade el primero.</td></tr>'
    document.getElementById('alumnos-footer').textContent = ''
    return
  }
  tbody.innerHTML = _alumnos.map(a => `
    <tr>
      <td><input value="${a.num||''}" style="width:36px" onblur="updateAlumno(${a.id},'num',this.value)"/></td>
      <td><input value="${esc(a.apellidos||'')}" onblur="updateAlumno(${a.id},'apellidos',this.value)"/></td>
      <td><input value="${esc(a.nombre||'')}" onblur="updateAlumno(${a.id},'nombre',this.value)"/></td>
      <td><input value="${esc(a.nia||'')}" onblur="updateAlumno(${a.id},'nia',this.value)"/></td>
      <td><input value="${esc(a.email||'')}" onblur="updateAlumno(${a.id},'email',this.value)"/></td>
      <td>
        <select onchange="updateAlumno(${a.id},'estado',this.value)">
          <option ${a.estado==='Activo'?'selected':''}>Activo</option>
          <option ${a.estado==='Pendiente'?'selected':''}>Pendiente</option>
          <option ${a.estado==='Baja'?'selected':''}>Baja</option>
        </select>
      </td>
      <td><button class="btn btn-ghost btn-sm" onclick="removeAlumno(${a.id})" style="padding:3px 8px">✕</button></td>
    </tr>
  `).join('')
  const activos = _alumnos.filter(a => a.estado === 'Activo').length
  document.getElementById('alumnos-footer').textContent =
    `${_alumnos.length} alumnos/as · ${activos} activos`
}

let _updateTimers = {}
function updateAlumno(id, field, val) {
  clearTimeout(_updateTimers[id+field])
  _updateTimers[id+field] = setTimeout(async () => {
    const a = _alumnos.find(x => x.id === id)
    if (!a) return
    a[field] = field === 'num' ? (parseInt(val)||null) : val
    await window.api.saveAlumno(a)
  }, 400)
}

async function addAlumno() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  try {
    const nextNum = _alumnos.length ? Math.max(..._alumnos.map(a=>a.num||0)) + 1 : 1
    const id = await window.api.saveAlumno({ modulo_id: parseInt(mid), num: nextNum, estado: 'Activo' })
    _alumnos.push({ id, modulo_id: parseInt(mid), num: nextNum, estado: 'Activo',
      apellidos:'', nombre:'', nia:'', email:'', telefono:'', observaciones:'' })
    renderAlumnosTable()
    setTimeout(() => {
      const rows = document.getElementById('alumnos-tbody').querySelectorAll('tr')
      const last = rows[rows.length-1]
      last?.querySelectorAll('input')[1]?.focus()
    }, 50)
  } catch(e) {
    alert('Error al guardar alumno: ' + e.message)
    console.error(e)
  }
}

function importAlumnos() {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  document.getElementById('import-alumnos-txt').value = ''
  document.getElementById('dlg-import-alumnos').showModal()
}

async function confirmImportAlumnos() {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  const txt = document.getElementById('import-alumnos-txt').value
  if (!txt.trim()) return
  document.getElementById('dlg-import-alumnos').close()
  try {
    const lines = txt.trim().split('\n').filter(Boolean)
    for (let i = 0; i < lines.length; i++) {
      const parts = lines[i].split(',').map(s => s.trim())
      const apellidos = parts[0] || ''
      const nombre = parts[1] || ''
      const num = _alumnos.length + i + 1
      const id = await window.api.saveAlumno({ modulo_id: mid, num, apellidos, nombre, estado:'Activo' })
      _alumnos.push({ id, modulo_id: mid, num, apellidos, nombre, estado:'Activo',
        nia:'', email:'', telefono:'', observaciones:'' })
    }
    renderAlumnosTable()
  } catch(e) {
    alert('Error al importar: ' + e.message)
    console.error(e)
  }
}

async function removeAlumno(id) {
  if (!confirm('¿Eliminar este alumno y todas sus notas?')) return
  await window.api.deleteAlumno(id)
  _alumnos = _alumnos.filter(a => a.id !== id)
  renderAlumnosTable()
}

// ═══════════════════════════════════════════════════════════════
// NOTAS
// ═══════════════════════════════════════════════════════════════
async function loadNotas() {
  const mid = document.getElementById('notas-mod-sel').value
  if (!mid) return

  // Actualizar selector de evaluación según eval_count del módulo
  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || 3
  const evSel     = document.getElementById('notas-ev-sel')
  const prevEv    = evSel.value
  evSel.innerHTML = '<option value="0">Todas</option>' +
    Array.from({length: evalCount}, (_, i) =>
      `<option value="${i+1}"${prevEv == i+1 ? ' selected' : ''}>EV ${i+1}</option>`
    ).join('')
  if (parseInt(evSel.value) > evalCount) evSel.value = '0'

  _alumnos = await window.api.getAlumnos(mid)
  _actividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  _notasGrid = {}
  notasArr.forEach(n => {
    if (!_notasGrid[n.alumno_id]) _notasGrid[n.alumno_id] = {}
    _notasGrid[n.alumno_id][n.actividad_id] = n.nota
  })
  renderNotasGrid()
}

function renderNotasGrid() {
  const ev = parseInt(document.getElementById('notas-ev-sel').value)
  const acts = ev ? _actividades.filter(a => a.eval === ev) : _actividades
  const alumnos = _alumnos.filter(a => a.estado === 'Activo')
  const wrap = document.getElementById('notas-grid-wrap')
  if (!acts.length || !alumnos.length) {
    wrap.innerHTML = '<div style="color:var(--text2);padding:20px">Sin datos.</div>'
    return
  }
  const thead = `<tr>
    <th class="sticky-col">Alumno/a</th>
    ${acts.map(a => `<th title="${a.descripcion}" style="text-align:center;min-width:58px">
      <div style="font-size:10px;max-width:56px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${a.instrumento}</div>
      <div style="font-size:9px;color:var(--text2)">${a.ut_id||'EV'+a.eval}</div>
    </th>`).join('')}
    <th style="min-width:58px;text-align:center">Media</th>
  </tr>`

  const tbody = alumnos.map(al => {
    const notas = acts.map(act => {
      const nota = _notasGrid[al.id]?.[act.id] ?? ''
      const cls = nota==='' ? '' : nota>=5 ? 'nota-apto' : nota>=4 ? 'nota-riesgo' : 'nota-noapto'
      return `<td style="text-align:center">
        <input class="nota-cell ${cls}" type="number" min="0" max="10" step="0.1"
          value="${nota}" data-aid="${al.id}" data-actid="${act.id}"
          onchange="onNotaChange(this)" oninput="colorNota(this)"/>
      </td>`
    }).join('')
    const vals = acts.map(act => _notasGrid[al.id]?.[act.id]).filter(n => n != null && n !== '')
    const media = vals.length ? (vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(1) : '—'
    const mediaCls = media==='—' ? '' : media>=5 ? 'nota-apto' : media>=4 ? 'nota-riesgo' : 'nota-noapto'
    return `<tr>
      <td class="sticky-col">${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}</td>
      ${notas}
      <td style="text-align:center;font-weight:700" class="${mediaCls}">${media}</td>
    </tr>`
  }).join('')

  wrap.innerHTML = `<div class="notas-grid"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div>`
}

function onNotaChange(el) {
  colorNota(el)
  const aid = parseInt(el.dataset.aid)
  const actId = parseInt(el.dataset.actid)
  const val = el.value.trim()
  window.api.saveNota(aid, actId, val === '' ? null : parseFloat(val))
  // Actualizar caché local
  if (!_notasGrid[aid]) _notasGrid[aid] = {}
  _notasGrid[aid][actId] = val === '' ? null : parseFloat(val)
}

function colorNota(el) {
  el.classList.remove('nota-apto','nota-riesgo','nota-noapto')
  const n = parseFloat(el.value)
  if (!isNaN(n)) el.classList.add(n>=5?'nota-apto':n>=4?'nota-riesgo':'nota-noapto')
}

// ═══════════════════════════════════════════════════════════════
// EVALUACIONES
// ═══════════════════════════════════════════════════════════════
async function loadEvaluaciones() {
  const mid = document.getElementById('eval-mod-sel').value
  if (!mid) return
  const alumnos = (await window.api.getAlumnos(mid)).filter(a => a.estado === 'Activo')
  const actividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  const ng = {}
  notasArr.forEach(n => { if(!ng[n.alumno_id])ng[n.alumno_id]={}; ng[n.alumno_id][n.actividad_id]=n.nota })

  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || [...new Set(actividades.map(a=>a.eval))].length || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)

  const html = evals.map(ev => {
    const acts = actividades.filter(a => a.eval === ev)
    const rows = alumnos.map(al => {
      // Media ponderada de actividades de esta evaluación
      let sumPeso = 0, sumNota = 0
      acts.forEach(act => {
        const n = ng[al.id]?.[act.id]
        if (n != null) { sumNota += n * act.peso; sumPeso += act.peso }
      })
      const media = sumPeso > 0 ? (sumNota / sumPeso).toFixed(2) : '—'
      const cls = media==='—' ? '' : media>=5?'nota-apto':media>=4?'nota-riesgo':'nota-noapto'
      return `<tr>
        <td>${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}</td>
        <td style="text-align:center;font-weight:700" class="${cls}">${media}</td>
      </tr>`
    }).join('')

    return `<div class="card">
      <div class="card-title">Evaluación ${ev}</div>
      <div class="tbl-wrap"><table>
        <thead><tr><th>Alumno/a</th><th style="text-align:center;width:100px">Nota EV${ev}</th></tr></thead>
        <tbody>${rows}</tbody>
      </table></div>
    </div>`
  }).join('')

  document.getElementById('eval-content').innerHTML = html || '<div style="color:var(--text2);padding:20px">Sin datos de notas aún.</div>'
}

// ═══════════════════════════════════════════════════════════════
// DASHBOARD
// ═══════════════════════════════════════════════════════════════
async function loadDashboard() {
  const mid = document.getElementById('dash-mod-sel').value
  if (!mid) return
  const alumnos = (await window.api.getAlumnos(mid)).filter(a => a.estado === 'Activo')
  const allActividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  const ng = {}
  notasArr.forEach(n => { if(!ng[n.alumno_id])ng[n.alumno_id]={}; ng[n.alumno_id][n.actividad_id]=n.nota })

  // Solo incluir actividades de las evaluaciones activas
  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)
  const actividades = allActividades.filter(a => evals.includes(a.eval))

  // Calcular media global por alumno
  const resumen = alumnos.map(al => {
    const ns = actividades.map(a => ng[al.id]?.[a.id]).filter(n => n!=null)
    const media = ns.length ? ns.reduce((a,b)=>a+b,0)/ns.length : null
    return { ...al, media }
  })

  const conNota = resumen.filter(a => a.media !== null)
  const aptos   = conNota.filter(a => a.media >= 5).length
  const noAptos = conNota.filter(a => a.media < 5).length
  const enRiesgo= conNota.filter(a => a.media >= 4 && a.media < 5).length
  const mediaGlobal = conNota.length ? (conNota.reduce((s,a)=>s+(a.media||0),0)/conNota.length).toFixed(1) : '—'

  const kpis = `<div class="kpi-grid">
    <div class="kpi"><div class="kpi-val">${alumnos.length}</div><div class="kpi-label">Activos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--green)">${aptos}</div><div class="kpi-label">Aptos (≥5)</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--red)">${noAptos}</div><div class="kpi-label">No Aptos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--amber)">${enRiesgo}</div><div class="kpi-label">En Riesgo</div></div>
    <div class="kpi"><div class="kpi-val">${mediaGlobal}</div><div class="kpi-label">Media Grupo</div></div>
  </div>`

  const filas = resumen.map(a => {
    const m = a.media
    const cls = m===null?'':m>=5?'sem-green':m>=4?'sem-amber':'sem-red'
    const nota = m===null ? '—' : m.toFixed(1)
    const notaCls = m===null?'':m>=5?'nota-apto':m>=4?'nota-riesgo':'nota-noapto'
    return `<tr>
      <td><span class="semaforo ${cls}"></span>${esc(a.apellidos||'')}${a.apellidos&&a.nombre?', ':''}${esc(a.nombre||'')}</td>
      <td style="text-align:center;font-weight:700" class="${notaCls}">${nota}</td>
      <td style="text-align:center">
        <button class="btn btn-ghost btn-sm" onclick="genBoletin(${a.id})">📄 Boletín PDF</button>
      </td>
    </tr>`
  }).join('')

  document.getElementById('dash-content').innerHTML = kpis + `
    <div class="card">
      <div class="card-title">Seguimiento individual</div>
      <div class="tbl-wrap"><table>
        <thead><tr><th>Alumno/a</th><th style="text-align:center;width:80px">Media</th><th style="width:130px"></th></tr></thead>
        <tbody>${filas}</tbody>
      </table></div>
    </div>`
}

async function genBoletin(alumnoId) {
  const a = _alumnos.find(x => x.id === alumnoId) || { apellidos:'', nombre:'' }
  const nombre = `${a.apellidos}, ${a.nombre}`
  // HTML básico del boletín
  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"/>
    <style>body{font-family:Arial,sans-serif;padding:40px;color:#222}
    h1{color:#0f1b2d;border-bottom:2px solid #4a90d9;padding-bottom:8px}
    table{width:100%;border-collapse:collapse;margin-top:20px}
    th{background:#162236;color:#fff;padding:8px;text-align:left}
    td{padding:8px;border-bottom:1px solid #eee}</style></head>
    <body><h1>Boletín de Evaluación</h1>
    <p><b>Alumno/a:</b> ${nombre}</p>
    <p><i>Generado: ${new Date().toLocaleDateString('es-ES')}</i></p>
    </body></html>`
  await window.api.exportBoletin(html, nombre)
}

// ═══════════════════════════════════════════════════════════════
// ASISTENTE IA
// ═══════════════════════════════════════════════════════════════
const IA_TABS = ['rubrica','actividad','informe','apuntes','todo']
function iaTab(el, id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'))
  el.classList.add('active')
  IA_TABS.forEach(t => document.getElementById('ia-'+t).style.display = t===id?'':'none')
}

function termAppend(id, d) {
  const el = document.getElementById(id)
  if (el.querySelector('.placeholder')) el.innerHTML = ''
  const line = document.createElement('div')
  if      (d.type==='stdout') { line.className='line-out';  line.textContent=d.text.trimEnd() }
  else if (d.type==='stderr') { line.className='line-err';  line.textContent=d.text.trimEnd() }
  else if (d.type==='done')   { line.className=d.code===0?'line-done':'line-fail'; line.textContent=d.code===0?'✅ Completado':'❌ Error (código '+d.code+')' }
  else                        { line.className='line-err';  line.textContent='⚠️ '+d.text }
  el.appendChild(line)
  el.scrollTop = el.scrollHeight
}

function runIA(cmd) {
  const termId = 'ia-'+cmd+'-term'
  document.getElementById(termId).innerHTML = ''
  const opts = { comando: cmd }
  if (cmd==='rubrica')   { opts.modulo=v('ia-r-mod'); opts.ra=v('ia-r-ra'); opts.proveedor=v('ia-r-prov') }
  if (cmd==='actividad') { opts.modulo=v('ia-a-mod'); opts.ra=v('ia-a-ra'); opts.n=v('ia-a-n'); opts.proveedor=v('ia-a-prov') }
  if (cmd==='informe')   { opts.alumno=v('ia-i-alumno'); opts.notas=v('ia-i-notas'); opts.proveedor=v('ia-i-prov') }
  if (cmd==='todo')      { opts.modulo=v('ia-t-mod'); opts.proveedor=v('ia-t-prov') }
  window.api.genIA(opts)
}
window.api.onIA(d => {
  const active = document.querySelector('#sec-ia .tab.active')?.textContent || ''
  const map = {'📋 Rúbrica':'ia-rubrica-term','🔧 Actividades':'ia-actividad-term','📝 Informe':'ia-informe-term','📄 Apuntes HTML':'ia-apuntes-term','🚀 Todo el módulo':'ia-todo-term'}
  const termId = Object.entries(map).find(([k]) => active.includes(k.slice(3)))?.[1] || 'ia-todo-term'
  termAppend(termId, d)
})

function runApuntes() {
  document.getElementById('ia-apuntes-term').innerHTML = ''
  window.api.genApuntes({ modulo:v('ia-ap-mod'), ut:v('ia-ap-ut').trim()||null, proveedor:v('ia-ap-prov') })
}
window.api.onApuntes(d => termAppend('ia-apuntes-term', d))

// ═══════════════════════════════════════════════════════════════
// AJUSTES
// ═══════════════════════════════════════════════════════════════
async function loadAjustes() {
  const cfg = await window.api.getAllConfig()
  if (cfg.openaiKey)    document.getElementById('cfg-openai').value    = cfg.openaiKey
  if (cfg.anthropicKey) document.getElementById('cfg-anthropic').value = cfg.anthropicKey
  if (cfg.proveedor)    document.getElementById('cfg-prov').value      = cfg.proveedor
}

async function saveAjustes() {
  const keys = { openaiKey:'cfg-openai', anthropicKey:'cfg-anthropic', proveedor:'cfg-prov' }
  for (const [k, id] of Object.entries(keys))
    await window.api.setConfig(k, document.getElementById(id).value)
  const st = document.getElementById('ajustes-ok')
  st.textContent = '✅ Guardado'
  setTimeout(() => st.textContent = '', 2500)
}

// ═══════════════════════════════════════════════════════════════
// Utils
// ═══════════════════════════════════════════════════════════════
const v   = id => { const e=document.getElementById(id); return e?e.value:'' }
const esc = s  => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')

// ═══════════════════════════════════════════════════════════════
// Init
// ═══════════════════════════════════════════════════════════════
async function init() {
  _modulos = await window.api.getModulos()
  if (_modulos.length) {
    _curMod = _modulos[0]
    updateModBadge()
  }
}
init()

// ═══════════════════════════════════════════════════════════════
// PONDERACIONES DE RAs
// ═══════════════════════════════════════════════════════════════
let _raPondTimers = {}
async function updateRaPond(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const pond = parseFloat(el.value)
  if (!mid || !raId || isNaN(pond) || pond < 0) return

  clearTimeout(_raPondTimers[mid + raId])
  _raPondTimers[mid + raId] = setTimeout(async () => {
    try {
      await window.api.setRaPonderacion(mid, raId, pond)
      showSaved()
    } catch(e) { console.error('Error guardando ponderación RA:', e) }
  }, 350)
}

function _refreshRaPondTotal(el) {
  // Recalcular suma de todas las ponderaciones de RAs en el DOM
  const card = el.closest('.card')
  if (!card) return
  const inputs = Array.from(card.querySelectorAll('input.ra-pond-cell'))
  const suma   = inputs.reduce((s, inp) => s + (parseFloat(inp.value) || 0), 0)
  const ok     = inputs.length > 0 && Math.abs(suma - 100) < 0.1
  const badge  = card.querySelector('[data-rapond-total]')
  if (badge) {
    badge.textContent   = ok ? '✓ 100%' : `⚠ suma ${Math.round(suma * 10) / 10}%`
    badge.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(245,158,11,.15)'
    badge.style.color      = ok ? 'var(--green)'         : 'var(--amber)'
  }
}

// ═══════════════════════════════════════════════════════════════
// PESOS DE ACTIVIDADES
// ═══════════════════════════════════════════════════════════════
let _pesoTimers = {}
async function updateActividadPeso(el) {
  const actId = parseInt(el.dataset.actid)
  const field  = el.dataset.field || 'peso'
  const val    = parseFloat(el.value)
  if (isNaN(val) || val < 0) return

  clearTimeout(_pesoTimers[actId + field])
  _pesoTimers[actId + field] = setTimeout(async () => {
    try {
      // Buscar modulo_id desde cualquier selector activo
      const mid = parseInt(
        document.getElementById('prog-mod-sel')?.value ||
        document.getElementById('eval-mod-sel')?.value || 0
      )
      if (!mid) return
      const acts = await window.api.getActividades(mid)
      const act  = acts.find(a => a.id === actId)
      if (!act) return
      act[field] = val
      await window.api.saveActividad(act)
      showSaved()
      _refreshPesoTotal(el, acts)
    } catch(e) { console.error('Error guardando actividad:', e) }
  }, 350)
}

async function updateActividadDesc(el) {
  const actId = parseInt(el.dataset.actid)
  if (!actId) return
  const mid = parseInt(document.getElementById('prog-mod-sel')?.value || document.getElementById('eval-mod-sel')?.value || 0)
  if (!mid) return
  clearTimeout(_pesoTimers['desc' + actId])
  _pesoTimers['desc' + actId] = setTimeout(async () => {
    try {
      const acts = await window.api.getActividades(mid)
      const act  = acts.find(a => a.id === actId)
      if (!act) return
      act.descripcion = el.value
      await window.api.saveActividad(act)
      showSaved()
    } catch(e) { console.error('Error guardando descripción:', e) }
  }, 400)
}

async function setEvalCount(mid, count) {
  const newCount  = parseInt(count)
  const data      = _getModData(mid)
  if (!data) return
  const oldCount  = data.modulo?.eval_count || evals?.length || 3
  data.modulo     = data.modulo || {}
  data.modulo.eval_count = newCount

  // ── Redistribuir UTs ──────────────────────────────────────────
  // Siempre redistribuye proporcionalmente: ninguna UT se pierde
  const uts = data.uts || []
  if (uts.length) {
    const sorted = uts.slice().sort((a,b) => (a.eval||1)-(b.eval||1) || (a.orden||0)-(b.orden||0))
    const perEval = Math.ceil(sorted.length / newCount)
    sorted.forEach((ut, i) => { ut.eval = Math.min(Math.floor(i / perEval) + 1, newCount) })
  }

  // ── Redistribuir eval_ras ─────────────────────────────────────
  // Siempre redistribuye proporcionalmente: ningún RA se pierde.
  // Todos los evals 1..newCount quedan con entrada (aunque sea vacía).
  if (data.eval_ras && Object.keys(data.eval_ras).length) {
    const allRas = [...new Set(
      Object.entries(data.eval_ras)
        .sort(([a],[b]) => parseInt(a)-parseInt(b))
        .flatMap(([,list]) => list)
    )]
    const newEvalRas = {}
    for (let e = 1; e <= newCount; e++) newEvalRas[e] = []   // inicializar vacíos
    if (allRas.length) {
      const perEval = Math.ceil(allRas.length / newCount)
      allRas.forEach((raId, i) => {
        const ev = Math.min(Math.floor(i / perEval) + 1, newCount)
        newEvalRas[ev].push(raId)
      })
    }
    data.eval_ras = newEvalRas
  }

  // ── Redistribuir Actividades (en BD) ─────────────────────────
  // Siempre redistribuye proporcionalmente por eval+orden: ninguna actividad se pierde
  const acts = await window.api.getActividades(parseInt(mid))
  if (acts.length) {
    const sorted = acts.slice().sort((a,b) => (a.eval||1)-(b.eval||1) || (a.orden||0)-(b.orden||0))
    const perEval = Math.ceil(sorted.length / newCount)
    for (const [i, act] of sorted.entries()) {
      const newEval = Math.min(Math.floor(i / perEval) + 1, newCount)
      if (newEval !== (act.eval||1)) {
        act.eval = newEval
        await window.api.saveActividad(act)
      }
    }
  }

  await _saveModData(mid, data, true)
}

async function addActividad(mid, ev, tipo) {
  const instrumento = tipo === 'examen' ? 'Examen' : 'Práctica'
  const allActs = await window.api.getActividades(parseInt(mid))
  const maxOrden = allActs.reduce((m,a) => Math.max(m, a.orden||0), 0)
  const evActs = allActs.filter(a => a.eval === ev)
  const sameType = evActs.filter(a => a.tipo === tipo)
  const desc = sameType.length
    ? `${instrumento} ${sameType.length + 1} — Evaluación ${ev}`
    : `${instrumento} — Evaluación ${ev}`
  await window.api.saveActividad({
    modulo_id: parseInt(mid), ut_id: null, ra_id: null,
    descripcion: desc, instrumento, tipo,
    peso: 0, nota_max: 10, eval: ev, orden: maxOrden + 1
  })
  showSaved()
  loadProgramacion()
}

async function deleteActividadRow(actId) {
  if (!confirm('¿Eliminar esta actividad?')) return
  await window.api.deleteActividad(actId)
  showSaved()
  loadProgramacion()
}

function _refreshPesoTotal(changedInput, acts) {
  // Recalcular en tiempo real la suma de pesos por evaluación leyendo los inputs del DOM
  // (así refleja cambios no guardados aún en otros inputs)
  const table  = changedInput.closest('table')
  if (!table) return
  const allPesoInputs = Array.from(table.querySelectorAll('.peso-cell:not([data-field])'))
  const suma   = allPesoInputs.reduce((s, inp) => s + (parseFloat(inp.value) || 0), 0)
  const ok     = Math.abs(suma - 100) < 0.1
  // Buscar el badge de total en el encabezado inmediatamente anterior a esta tabla
  const wrapper = table.closest('div[style*="margin-bottom"]')
  const badge   = wrapper?.querySelector('span[data-pesobadge]')
  if (badge) {
    badge.textContent = ok ? '✓ 100%' : `⚠ suma ${Math.round(suma*10)/10}%`
    badge.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(245,158,11,.15)'
    badge.style.color       = ok ? 'var(--green)'        : 'var(--amber)'
  }
}

// ═══════════════════════════════════════════════════════════════
// EDICIÓN DE UTs — añadir / quitar / asignar RA+CE
// ═══════════════════════════════════════════════════════════════
let _utRasState = null

function _getModData(mid) {
  const mod = _modulos.find(m => m.id == mid)
  if (!mod?.data_json) return null
  try { return JSON.parse(mod.data_json) } catch { return null }
}

async function _saveModData(mid, data, reload) {
  await window.api.setModuloDataJson(parseInt(mid), data)
  _modulos = await window.api.getModulos()
  showSaved()
  if (reload) loadProgramacion()
}

async function saveUtField(mid, utId, field, value) {
  const data = _getModData(mid)
  if (!data) return
  const ut = (data.uts||[]).find(u => u.id === utId)
  if (!ut) return
  ut[field] = (field === 'horas' || field === 'eval') ? (parseInt(value)||0) : value
  // Recargar programación al cambiar eval → actualiza distribución de RAs
  await _saveModData(mid, data, field === 'eval')
}

async function addUt(mid) {
  const data = _getModData(mid)
  if (!data) return
  const n = (data.uts?.length || 0) + 1
  data.uts = [...(data.uts||[]), {id:`UT${n}`, nombre:'Nueva unidad de trabajo', horas:0, eval:1, tags:''}]
  await _saveModData(mid, data, true)
}

async function deleteUt(mid, utId) {
  if (!confirm(`¿Eliminar ${utId} del módulo?`)) return
  const data = _getModData(mid)
  if (!data) return
  data.uts          = (data.uts||[]).filter(u => u.id !== utId)
  data.asignaciones = (data.asignaciones||[]).filter(a => a.ut !== utId)
  await _saveModData(mid, data, true)
}

function openUtRasModal(mid, utId) {
  const data = _getModData(mid)
  if (!data) return
  const ut = (data.uts||[]).find(u => u.id === utId)
  if (!ut) return
  _utRasState = {mid, data, utId}

  document.getElementById('ut-ras-title').textContent = `${utId} — ${ut.nombre}`

  const currentAsigs = (data.asignaciones||[]).filter(a => a.ut === utId)
  const asigMap = Object.fromEntries(currentAsigs.map(a => [a.ra, a.ces||[]]))
  const cesData = data.ces || {}

  let html = ''
  for (const ra of (data.ras||[])) {
    const checked = ra.id in asigMap
    const raCEs   = cesData[ra.id] || []
    const selCEs  = asigMap[ra.id] || []
    html += `
    <div style="margin-bottom:10px;padding:10px 12px;background:var(--bg3);border-radius:10px;border:1px solid var(--border)">
      <label style="display:flex;align-items:flex-start;gap:8px;cursor:pointer">
        <input type="checkbox" data-ra="${ra.id}" class="ut-ra-chk" ${checked?'checked':''}
          onchange="_toggleRaSection('${ra.id}',this.checked)"
          style="margin-top:3px;accent-color:var(--accent);width:14px;height:14px;flex-shrink:0"/>
        <span style="font-weight:700;color:var(--accent2);font-size:12.5px;white-space:nowrap">${ra.id}</span>
        <span style="font-size:12px;color:var(--text);line-height:1.4">${esc(ra.nombre)}</span>
      </label>
      <div id="ces-block-${ra.id}" style="display:${checked?'grid':'none'};grid-template-columns:1fr 1fr;gap:2px 16px;padding:8px 0 2px 22px">
        ${raCEs.map(ce=>`
        <label style="display:flex;align-items:flex-start;gap:5px;cursor:pointer;padding:2px 0">
          <input type="checkbox" data-ra="${ra.id}" data-ce="${ce.id}" class="ut-ce-chk"
            ${checked&&(selCEs.length===0||selCEs.includes(ce.id))?'checked':''}
            style="margin-top:2px;accent-color:var(--accent);flex-shrink:0"/>
          <span style="font-size:11px;color:var(--text2);line-height:1.35">
            <b style="color:var(--accent)">${ce.id}</b> ${esc(ce.texto)}
          </span>
        </label>`).join('')}
      </div>
    </div>`
  }

  document.getElementById('ut-ras-body').innerHTML = html ||
    '<p style="color:var(--text2);font-size:13px">Este módulo no tiene RAs definidos.</p>'
  document.getElementById('modal-ut-ras').classList.add('open')
}

function _refreshUtHoras(inp, modHoras) {
  const table  = inp.closest('table')
  if (!table) return
  const suma   = Array.from(table.querySelectorAll('.ut-horas-inp')).reduce((s,i) => s+(parseInt(i.value)||0), 0)
  const badge  = document.getElementById('ut-horas-badge')
  if (!badge) return
  const ok = suma === modHoras
  badge.textContent  = `Σ ${suma}h / ${modHoras}h${ok?' ✓':' ⚠'}`
  badge.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(245,158,11,.15)'
  badge.style.color      = ok ? 'var(--green)'         : 'var(--amber)'
}

function _toggleRaSection(raId, checked) {
  const block = document.getElementById(`ces-block-${raId}`)
  if (!block) return
  block.style.display = checked ? 'grid' : 'none'
  if (checked) block.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true)
}

async function saveUtRas() {
  if (!_utRasState) return
  const {mid, data, utId} = _utRasState
  data.asignaciones = (data.asignaciones||[]).filter(a => a.ut !== utId)
  document.querySelectorAll('.ut-ra-chk:checked').forEach(raChk => {
    const raId = raChk.dataset.ra
    const ces  = Array.from(document.querySelectorAll(`.ut-ce-chk[data-ra="${raId}"]:checked`)).map(cb=>cb.dataset.ce)
    data.asignaciones.push({ut: utId, ra: raId, ces})
  })
  await _saveModData(mid, data, true)
  closeUtRasModal()
}

function closeUtRasModal() {
  document.getElementById('modal-ut-ras').classList.remove('open')
  _utRasState = null
}

async function applyModuloPesos() {
  const mid = parseInt(
    document.getElementById('prog-mod-sel')?.value ||
    document.getElementById('eval-mod-sel')?.value || 0
  )
  if (!mid) return
  const pesoPrac = parseFloat(document.getElementById('mod-peso-prac')?.value) || 30
  const pesoExam = parseFloat(document.getElementById('mod-peso-exam')?.value) || 70
  const acts = await window.api.getActividades(mid)
  const evs  = [...new Set(acts.map(a => a.eval))].sort()
  for (const ev of evs) {
    const evActs   = acts.filter(a => a.eval === ev)
    const practicas = evActs.filter(a => a.tipo === 'practica')
    const examenes  = evActs.filter(a => a.tipo === 'examen')
    for (const a of practicas) {
      a.peso = practicas.length ? Math.round(pesoPrac / practicas.length * 10) / 10 : 0
      await window.api.saveActividad(a)
    }
    for (const a of examenes) {
      a.peso = examenes.length  ? Math.round(pesoExam  / examenes.length  * 10) / 10 : 0
      await window.api.saveActividad(a)
    }
  }
  showSaved()
  loadProgramacion()
}

// ═══════════════════════════════════════════════════════════════
// EDICIÓN INLINE — comportamiento tipo Excel
// ═══════════════════════════════════════════════════════════════

// ── Toast "Guardado ✓" ──────────────────────────────────────────
const _toastEl = document.createElement('div')
_toastEl.id = 'toast-saved'
_toastEl.innerHTML = '✓ Guardado'
document.body.appendChild(_toastEl)
let _toastTimer = null
function showSaved() {
  clearTimeout(_toastTimer)
  _toastEl.classList.add('show')
  _toastTimer = setTimeout(() => _toastEl.classList.remove('show'), 1400)
}

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

// ── Navegación con teclado en el grid de notas ─────────────────
// Igual que Excel: flechas, Enter baja, Tab avanza
document.addEventListener('keydown', function(e) {
  const el = e.target
  if (!el.classList.contains('nota-cell')) return

  const tbl   = el.closest('table')
  if (!tbl) return
  const cells = Array.from(tbl.querySelectorAll('.nota-cell'))
  const idx   = cells.indexOf(el)
  if (idx < 0) return

  // Contar columnas de notas por fila para navegar en 2D
  const row      = el.closest('tr')
  const rowCells = Array.from(row.querySelectorAll('.nota-cell'))
  const colIdx   = rowCells.indexOf(el)
  const rows     = Array.from(tbl.querySelectorAll('tbody tr'))
  const rowIdx   = rows.indexOf(row)

  let target = null

  if (e.key === 'ArrowRight' || (e.key === 'Tab' && !e.shiftKey)) {
    target = cells[idx + 1]
    if (e.key === 'Tab') e.preventDefault()
  } else if (e.key === 'ArrowLeft' || (e.key === 'Tab' && e.shiftKey)) {
    target = cells[idx - 1]
    if (e.key === 'Tab') e.preventDefault()
  } else if (e.key === 'ArrowDown' || e.key === 'Enter') {
    // misma columna, fila siguiente
    const nextRow = rows[rowIdx + 1]
    if (nextRow) {
      const nextCells = Array.from(nextRow.querySelectorAll('.nota-cell'))
      target = nextCells[colIdx] || null
    }
    if (e.key === 'Enter') e.preventDefault()
  } else if (e.key === 'ArrowUp') {
    const prevRow = rows[rowIdx - 1]
    if (prevRow) {
      const prevCells = Array.from(prevRow.querySelectorAll('.nota-cell'))
      target = prevCells[colIdx] || null
    }
  } else if (e.key === 'Escape') {
    el.blur()
    return
  }

  if (target) {
    target.focus()
    target.select()
  }
})

// ── Enter en tabla de alumnos mueve al siguiente campo ──────────
document.addEventListener('keydown', function(e) {
  const el = e.target
  if (e.key !== 'Enter') return
  const td = el.closest('td')
  if (!td || td.closest('#alumnos-tbody') === null) return
  // Tab al siguiente input de la misma fila
  const row = el.closest('tr')
  const inputs = Array.from(row.querySelectorAll('input,select'))
  const i = inputs.indexOf(el)
  if (i >= 0 && i < inputs.length - 1) {
    inputs[i + 1].focus()
    if (inputs[i + 1].select) inputs[i + 1].select()
    e.preventDefault()
  }
})
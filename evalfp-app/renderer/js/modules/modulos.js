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

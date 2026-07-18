// MÓDULOS
// ═══════════════════════════════════════════════════════════════
async function renderModulos() {
  _modulos = await window.api.getModulos()
  const el = document.getElementById('mod-cards-list')
  if (!_modulos.length) {
    el.innerHTML = '<div style="color:var(--text2);padding:28px 20px;grid-column:1/-1;text-align:center"><p style="margin-bottom:14px">No hay módulos. Añade uno para empezar.</p><button class="btn btn-primary" onclick="openAddModulo()">+ Añadir primer módulo</button></div>'
    updateModBadge()
    return
  }
  el.innerHTML = _modulos.map(m => `
    <div class="mod-card ${_curMod?.id===m.id?'active-mod':''}" onclick="selectMod(${m.id})">
      <button class="mod-card-del" onclick="event.stopPropagation();delModulo(${m.id})" title="Eliminar" aria-label="Eliminar módulo">✕</button>
      <div class="mod-card-abrev">${esc(m.abrev)}</div>
      <div class="mod-card-nombre">${esc(m.nombre)}</div>
      <div class="mod-card-meta">
        ${esc(m.ciclo||'')} · ${esc(m.curso||'')} · ${esc(m.anno||'')}<br>
        Grupo: <b>${esc(m.grupo)}</b>
        ${m.decreto ? `<br><span style="color:var(--accent2)">${esc(m.decreto)}</span>` : ''}
      </div>
    </div>
  `).join('')
  updateModBadge()
}

function selectMod(id) {
  _curMod = _modulos.find(m => m.id === id)
  updateModBadge()
  closeModDropdown()
  // Recargar la sección activa con el nuevo módulo
  const activeNav = document.querySelector('.nav-item.active')
  const sec = activeNav?.dataset?.sec
  if (sec) goSection(sec)
  else { renderModulos(); renderModRasPanel(_curMod) }
}

// ── Dropdown sidebar ────────────────────────────────────────────
function updateModBadge() {
  const nameEl = document.getElementById('mod-badge-name')
  const subEl  = document.getElementById('mod-badge-sub')
  if (_curMod) {
    if (nameEl) nameEl.textContent = _curMod.abrev
    if (subEl) {
      const parts = [_curMod.nombre, _curMod.curso, _curMod.grupo].filter(Boolean)
      subEl.textContent = parts.join(' · ')
    }
  } else {
    if (nameEl) nameEl.textContent = 'Sin módulo'
    if (subEl) subEl.textContent = 'Toca para añadir'
  }
}

function renderModDropdown() {
   const dd = document.getElementById('mod-dropdown')
   if (!dd) return
   dd.innerHTML = _modulos.map(m => `
     <div class="mod-dd-item ${m.id === _curMod?.id ? 'sel' : ''}"
          onclick="event.stopPropagation();selectMod(${m.id})">
       <span class="mod-dd-abrev">${esc(m.abrev)}</span>
       <div class="mod-dd-info">
         <div class="mod-dd-nombre">${esc(m.nombre)}</div>
         <div class="mod-dd-meta">${[esc(m.curso), esc(m.grupo)].filter(Boolean).join(' · ')}</div>
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
       RAs y Criterios de Evaluación — ${esc(mod.abrev)}
     </div>
     <div style="display:flex;flex-direction:column;gap:8px">`
   for (const ra of ras) {
     const raCes = ces[ra.id] || []
     html += `
       <div class="card" style="border-left:3px solid var(--accent2);padding:12px 16px">
         <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:${raCes.length?'8px':'0'}">
           <span style="font-size:12px;font-weight:700;color:var(--accent2);min-width:34px">${esc(ra.id)}</span>
           <span style="font-size:12px;font-weight:600;flex:1">${esc(ra.nombre)}</span>
           ${ra.pond ? `<span style="font-size:11px;background:var(--navy3);padding:2px 7px;border-radius:10px;color:var(--accent)">${esc(String(ra.pond))}%</span>` : ''}
         </div>
         ${raCes.length ? `<div style="margin-left:44px">${raCes.map(ce => `
           <div style="display:flex;gap:8px;padding:3px 0;border-top:1px solid var(--border);font-size:11px;color:var(--text2)">
             <span style="color:var(--accent);font-weight:600;min-width:26px">${esc(ce.id)}</span>
             <span>${esc(ce.texto)}</span>
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

// ── Catálogo de módulos ──────────────────────────────────────────

const CAT_CICLO_LABELS = {
  'CFGB':      'CFGB — Informática de Oficina',
  'SMR':       'CFGM — Sistemas Microinformáticos y Redes',
  'ASIR':      'CFGS — Administración de Sistemas Informáticos en Red',
  'DAM':       'CFGS — Desarrollo de Aplicaciones Multiplataforma',
  'DAW':       'CFGS — Desarrollo de Aplicaciones Web',
  'CE_CIBER':  'CE — Ciberseguridad en Entornos de las TI',
  'CE_IABD':   'CE — Inteligencia Artificial y Big Data',
  'CE_PYTHON': 'CE — Desarrollo de Aplicaciones en Python',
  'SA':        'CFGB — Servicios Administrativos',
  'GA':        'CFGM — Gestión Administrativa',
  'AF':        'CFGS — Administración y Finanzas',
  'AD':        'CFGS — Asistencia a la Dirección',
}

let _catCicloActual = 'CFGB'
let _catSearch = ''
let _catSelectedKey = null

async function openAddModulo() {
  _modsDisponibles = await window.api.listModulosDisponibles()
  _modData = null
  _catSelectedKey = null
  document.getElementById('add-mod-grupo').value = ''
  document.getElementById('cat-footer').style.display = 'none'
  document.getElementById('cat-count').textContent = _modsDisponibles.length
  document.getElementById('cat-search').value = ''
  _catSearch = ''
  // Activar primer ciclo con módulos disponibles
  selectCatCiclo(document.querySelector('.cat-ciclo-item.active') ||
                 document.querySelector('.cat-ciclo-item'))
  document.getElementById('modal-add-mod').showModal()
}

function selectCatCiclo(el) {
  document.querySelectorAll('.cat-ciclo-item').forEach(i => i.classList.remove('active'))
  if (!el) return
  el.classList.add('active')
  _catCicloActual = el.dataset.clave
  _catSearch = ''
  document.getElementById('cat-search').value = ''
  renderCatCards()
}

function filterCatalogo() {
  _catSearch = document.getElementById('cat-search').value.toLowerCase().trim()
  renderCatCards()
}

function renderCatCards() {
  const addedKeys = new Set(_modulos.map(m => m.key))
  let lista = _modsDisponibles

  if (_catSearch) {
    // Búsqueda global: ignorar ciclo seleccionado
    lista = lista.filter(m =>
      m.nombre.toLowerCase().includes(_catSearch) ||
      m.abrev.toLowerCase().includes(_catSearch) ||
      (m.ciclo||'').toLowerCase().includes(_catSearch))
  } else {
    lista = lista.filter(m => m.ciclo_clave === _catCicloActual)
  }

  const label = _catSearch
    ? `Resultados para "${_catSearch}"`
    : (CAT_CICLO_LABELS[_catCicloActual] || _catCicloActual)
  document.getElementById('cat-ciclo-title').textContent = label

  const cards = document.getElementById('cat-cards')
  if (!lista.length) {
    cards.innerHTML = '<div style="color:var(--text2);font-size:13px;padding:20px 0">No hay módulos.</div>'
    return
  }

  cards.innerHTML = lista.map(m => {
    const added = addedKeys.has(m.key)
    const sel   = _catSelectedKey === m.key
    const horas = m.total_horas || m.horas || ''
    const nRas  = m.n_ras || ''
    return `
    <div class="cat-card ${added?'already-added':''} ${sel?'selected':''}"
         onclick="${added?'':` selectCatCard('${m.key}')`}">
      <div class="cat-card-abrev">${esc(m.abrev)}</div>
      <div class="cat-card-nombre">${esc(m.nombre)}</div>
      <div class="cat-card-meta">
        ${horas ? `<span class="cat-card-pill">${esc(String(horas))}h</span>` : ''}
        ${nRas  ? `<span class="cat-card-pill">${esc(String(nRas))} RA</span>` : ''}
        ${m.curso ? `<span class="cat-card-pill">${esc(m.curso)}</span>` : ''}
      </div>
    </div>`
  }).join('')
}

async function selectCatCard(key) {
  const m_idx = _modsDisponibles.find(m => m.key === key)
  if (!m_idx) return
  try {
    _catSelectedKey = key
    _modData = await window.api.getModuloData(key)
    const m = _modData.modulo
    const horas = m.total_horas || m.horas || '?'
    const info = document.getElementById('cat-sel-info')
    info.innerHTML = `
      <b>${esc(m.abrev)}</b> — ${esc(m.nombre)}
      <span style="color:var(--text2);margin-left:10px">${esc(m.ciclo||'')} · ${esc(String(horas))}h · ${_modData.ras.length} RAs</span>`
    document.getElementById('cat-footer').style.display = 'flex'
    renderCatCards()   // re-render to show selected state
  } catch(e) {
    alert('Error cargando módulo: ' + e.message)
    _modData = null
  }
}

async function confirmAddModulo() {
  if (!_modData || !_catSelectedKey) return alert('Selecciona un módulo primero.')
  const key = _catSelectedKey
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
  const dlg = document.getElementById('modal-add-mod')
  if (dlg.open) dlg.close()
}

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

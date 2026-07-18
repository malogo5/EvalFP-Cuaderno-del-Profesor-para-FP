// NOTAS
// ═══════════════════════════════════════════════════════════════

// H6 — Modo recuperación: las notas de recuperación se guardan en una columna
// aparte (nota_rec) sin sobrescribir la original, para conservar trazabilidad.
let _recMode  = false
let _notasRec = {}   // { alumnoId: { actividadId: nota_rec } }

function toggleRecMode() {
  _recMode = !_recMode
  renderNotasGrid()
}

/** Mapa de notas EFECTIVAS de un alumno (rec ?? original) — para medias. */
function _notasEf(aid) {
  const base = _notasGrid[aid] || {}
  const rec  = _notasRec[aid] || {}
  const out = { ...base }
  for (const [actId, n] of Object.entries(rec)) if (n != null) out[actId] = n
  return out
}

/**
 * Calcula la nota ponderada de un alumno para las actividades dadas.
 * Agrupa las actividades por tipo (practica / examen / otros),
 * promedia las notas calificadas dentro de cada grupo y pondera cada
 * grupo por su peso total, NORMALIZANDO por la suma de pesos de los
 * grupos calificados: media = Σ(media_grupo × peso_grupo) / Σ(peso_grupo).
 * Así el resultado está siempre en la escala 0-10 aunque los pesos de la
 * evaluación no sumen 100 (p. ej. ISO EV1: 2 prácticas×30 + examen 70 = 130).
 * Los grupos sin ninguna nota no entran en la media (reponderación).
 * Devuelve '—' si no hay ninguna actividad calificada.
 *
 * @param {Array}  acts        - Actividades con .tipo, .peso e .id
 * @param {Object} notasAl    - { actividad_id: nota } para este alumno
 * @param {number} [decimals] - Decimales del resultado (default 2)
 * @returns {string}
 */
function _calcMediaPonderada(acts, notasAl, decimals = 2) {
  const byTipo = {}
  acts.forEach(act => {
    if (!byTipo[act.tipo]) byTipo[act.tipo] = []
    byTipo[act.tipo].push(act)
  })
  let sumNota = 0, sumPeso = 0
  const todas = []   // fallback: media simple si ningún grupo tiene peso
  Object.values(byTipo).forEach(tipoActs => {
    // Peso total del grupo (incluye actividades sin calificar)
    const grupoPeso = tipoActs.reduce((s, a) => s + (a.peso || 0), 0)
    // Promedio simple de las calificadas en este grupo
    const graded = tipoActs.map(a => notasAl?.[a.id]).filter(n => n != null && n !== '')
    if (!graded.length) return
    todas.push(...graded)
    if (grupoPeso > 0) {
      const avg = graded.reduce((s, n) => s + n, 0) / graded.length
      sumNota += avg * grupoPeso
      sumPeso += grupoPeso
    }
  })
  if (sumPeso > 0) return (sumNota / sumPeso).toFixed(decimals)
  if (todas.length) return (todas.reduce((s, n) => s + n, 0) / todas.length).toFixed(decimals)
  return '—'
}

async function exportNotasPDF() {
  const mid = document.getElementById('notas-mod-sel').value
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  const mod = _modulos.find(m => m.id == mid)
  const ev = parseInt(document.getElementById('notas-ev-sel').value)
  const acts = ev ? _actividades.filter(a => a.eval === ev) : _actividades
  const alumnos = _alumnos.filter(a => a.estado === 'Activo')
  if (!acts.length || !alumnos.length) { alert('Sin datos que exportar.'); return }

  const titulo = `${mod?.abrev || 'Módulo'} — Registro de Notas${ev ? ' · Evaluación '+ev : ''}`
  const thead = `<tr><th>Alumno/a</th>${acts.map(a=>`<th>${esc(a.instrumento)}<br/><small>${esc(a.ut_id||'EV'+a.eval)}</small></th>`).join('')}<th>Media</th></tr>`
  const tbody = alumnos.map(al => {
    // H6: exportar la nota efectiva; las recuperadas se marcan con *
    const efMap = _notasEf(al.id)
    const vals = acts.map(act => efMap[act.id])
    const notas = acts.map(act => {
      const n = efMap[act.id]
      const esRec = _notasRec[al.id]?.[act.id] != null
      return `<td style="text-align:center">${n != null ? n + (esRec ? '*' : '') : ''}</td>`
    }).join('')
    // Media ponderada por tipo cuando hay EV concreta; simple en vista "Todas"
    const media = ev
      ? _calcMediaPonderada(acts, efMap)
      : (() => { const nums = vals.filter(n => n != null); return nums.length ? (nums.reduce((a,b)=>a+b,0)/nums.length).toFixed(2) : '—' })()
    return `<tr><td>${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}</td>${notas}<td style="text-align:center;font-weight:700">${media}</td></tr>`
  }).join('')

  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"/>
    <style>
      body{font-family:Arial,sans-serif;padding:30px;font-size:12px}
      h2{color:#0f1b2d;margin-bottom:12px}
      table{width:100%;border-collapse:collapse;font-size:11px}
      th{background:#162236;color:#fff;padding:6px 8px;text-align:center}
      th:first-child{text-align:left}
      td{padding:5px 8px;border-bottom:1px solid #e5e7eb}
      tr:nth-child(even){background:#f9fafb}
      small{font-weight:400;opacity:.7}
    </style></head>
    <body>
    <h2>${esc(titulo)}</h2>
    <p style="color:#6b7280;font-size:11px">Generado: ${new Date().toLocaleDateString('es-ES')} · ${alumnos.length} alumnos/as · ${acts.length} actividades</p>
    <table><thead>${thead}</thead><tbody>${tbody}</tbody></table>
    </body></html>`

  const nombre = `notas_${mod?.abrev||'modulo'}${ev?'_ev'+ev:''}`
  try {
    await window.api.exportBoletin(html, nombre)
  } catch(e) {
    alert('Error al exportar: ' + e.message)
  }
}
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
  _notasRec  = {}
  notasArr.forEach(n => {
    if (!_notasGrid[n.alumno_id]) { _notasGrid[n.alumno_id] = {}; _notasRec[n.alumno_id] = {} }
    _notasGrid[n.alumno_id][n.actividad_id] = n.nota
    if (n.nota_rec != null) _notasRec[n.alumno_id][n.actividad_id] = n.nota_rec
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
    ${acts.map(a => `<th title="${esc(a.descripcion)}" style="text-align:center;min-width:58px">
      <div style="font-size:10px;max-width:56px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(a.instrumento)}</div>
      <div style="font-size:9px;color:var(--text2)">${esc(a.ut_id||'EV'+a.eval)}</div>
    </th>`).join('')}
    <th style="min-width:58px;text-align:center">Media</th>
  </tr>`

  const tbody = alumnos.map(al => {
    const efMap = _notasEf(al.id)
    const notas = acts.map(act => {
      if (_recMode) {
        // H6: en modo recuperación se edita nota_rec; la original queda visible
        const orig = _notasGrid[al.id]?.[act.id]
        const rec  = _notasRec[al.id]?.[act.id] ?? ''
        const cls = rec==='' ? '' : rec>=5 ? 'nota-apto' : rec>=4 ? 'nota-riesgo' : 'nota-noapto'
        return `<td style="text-align:center">
          <input class="nota-cell ${cls}" type="number" min="0" max="10" step="0.1"
            value="${rec}" data-aid="${al.id}" data-actid="${act.id}" data-rec="1"
            placeholder="${orig != null ? orig : ''}" title="Recuperación (original: ${orig != null ? orig : '—'})"
            style="border-color:var(--accent)"
            onchange="onNotaChange(this)" oninput="colorNota(this)"/>
          <div style="font-size:8px;color:var(--text3)">orig: ${orig != null ? orig : '—'}</div>
        </td>`
      }
      const nota = _notasGrid[al.id]?.[act.id] ?? ''
      const rec  = _notasRec[al.id]?.[act.id]
      const cls = nota==='' ? '' : nota>=5 ? 'nota-apto' : nota>=4 ? 'nota-riesgo' : 'nota-noapto'
      return `<td style="text-align:center">
        <input class="nota-cell ${cls}" type="number" min="0" max="10" step="0.1"
          value="${nota}" data-aid="${al.id}" data-actid="${act.id}"
          onchange="onNotaChange(this)" oninput="colorNota(this)"/>
        ${rec != null ? `<div style="font-size:8px;color:var(--accent);font-weight:700" title="Nota de recuperación (efectiva)">rec: ${rec}</div>` : ''}
      </td>`
    }).join('')
    // Media ponderada por tipo cuando hay EV concreta; simple en vista "Todas"
    // Siempre sobre la nota EFECTIVA (rec ?? original)
    const media = ev
      ? _calcMediaPonderada(acts, efMap)
      : (() => { const vals = acts.map(act => efMap[act.id]).filter(n => n != null && n !== ''); return vals.length ? (vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(2) : '—' })()
    const mediaCls = media === '—' ? '' : media >= 5 ? 'nota-apto' : media >= 4 ? 'nota-riesgo' : 'nota-noapto'
    return `<tr>
      <td class="sticky-col">${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}</td>
      ${notas}
      <td style="text-align:center;font-weight:700" class="${mediaCls}">${media}</td>
    </tr>`
  }).join('')

  const recBar = `<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
    <button onclick="toggleRecMode()"
      style="font-size:11px;padding:4px 12px;border-radius:7px;cursor:pointer;white-space:nowrap;
             border:1px solid ${_recMode ? 'var(--accent)' : 'var(--border2)'};
             background:${_recMode ? 'rgba(201,104,45,.12)' : 'var(--bg3)'};
             color:${_recMode ? 'var(--accent)' : 'var(--text2)'};font-weight:${_recMode ? '700' : '400'}">
      ${_recMode ? '✎ Modo recuperación ACTIVO' : '✎ Modo recuperación'}
    </button>
    <span style="font-size:10.5px;color:var(--text3)">
      ${_recMode
        ? 'Introduce la nota de recuperación sin perder la original (vacío = sin recuperación). La nota efectiva es la de recuperación.'
        : 'Las celdas con "rec:" tienen recuperación registrada; esa es la nota efectiva.'}
    </span>
  </div>`

  wrap.innerHTML = recBar + `<div class="notas-grid"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div>`
}

function onNotaChange(el) {
  colorNota(el)
  function updateMediaFila(aid) {
  const ev = parseInt(document.getElementById('notas-ev-sel').value)
  const acts = ev ? _actividades.filter(a => a.eval === ev) : _actividades

  // Media ponderada por tipo cuando hay EV concreta; simple en vista "Todas"
  // H6: siempre sobre la nota efectiva (rec ?? original)
  const efMap = _notasEf(aid)
  const media = ev
    ? _calcMediaPonderada(acts, efMap)
    : (() => { const vals = acts.map(act => efMap[act.id]).filter(n => n != null && n !== ''); return vals.length ? (vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(2) : '—' })()

  const fila = document.querySelector(`input[data-aid="${aid}"]`)?.closest('tr')
  if (!fila) return

  const td = fila.lastElementChild
  td.textContent = media

  td.classList.remove('nota-apto','nota-riesgo','nota-noapto')

  if (media !== '—') {
    const n = parseFloat(media)
    td.classList.add(
      n >= 5
        ? 'nota-apto'
        : n >= 4
          ? 'nota-riesgo'
          : 'nota-noapto'
    )
  }
}
  const aid = parseInt(el.dataset.aid)
  const actId = parseInt(el.dataset.actid)
  const val = el.value.trim()

  // Validate nota (0-10)
  if (val !== '') {
    const notaVal = parseFloat(val)
    if (!validators.nota(notaVal)) {
      alert('Nota inválida. Debe estar entre 0 y 10.')
      el.value = ''
      return
    }
  }

  try {
    const esRec = el.dataset.rec === '1'   // H6: modo recuperación
    if (esRec) {
      window.api.saveNotaRec(aid, actId, val === '' ? null : parseFloat(val))
      if (!_notasRec[aid]) _notasRec[aid] = {}
      if (val === '') delete _notasRec[aid][actId]
      else _notasRec[aid][actId] = parseFloat(val)
    } else {
      window.api.saveNota(aid, actId, val === '' ? null : parseFloat(val))
      if (!_notasGrid[aid]) _notasGrid[aid] = {}
      _notasGrid[aid][actId] = val === '' ? null : parseFloat(val)
    }
    updateMediaFila(aid)
  } catch(e) {
    alert('Error al guardar nota: ' + validators.sanitizeErrorMessage(e, 'onNotaChange'))
    console.error(e)
  }
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

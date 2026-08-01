// NOTAS
// ═══════════════════════════════════════════════════════════════

// H6 — Recuperar una ACTIVIDAD dentro de la evaluación continua: la nota nueva
// se guarda en una columna aparte (nota_rec) sin borrar la original.
//
// Ojo con no confundir los dos caminos, que antes se llamaban igual:
//   · aquí se recupera una ACTIVIDAD y afecta a la 1ª convocatoria;
//   · en Evaluaciones → 2ª Ordinaria se recupera por CRITERIO y afecta a la
//     segunda convocatoria, que es la que decide titulación.
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
 * Media de las actividades calificadas de un alumno, con el motor único
 * (js/core/calificacion.js): pondera por el peso de cada actividad y respeta la
 * escala de cada instrumento (`nota_max`). Es una media de actividades, no la
 * nota del módulo: esa se calcula por resultados de aprendizaje en Evaluaciones.
 */
function _calcMediaPonderada(acts, notasAl, decimals = 2) {
  const { PRAC, EXAM } = pesosPorTipo(acts)
  const m = mediaActividades(acts, notasAl, PRAC, EXAM)
  return m === null ? '—' : m.toFixed(decimals)
}

/**
 * Qué se está viendo en la parrilla: la evaluación elegida y sus actividades.
 *
 * A-5 · «Todas» y cada trimestre enseñan solo la 1ª convocatoria; la prueba de
 * la 2ª tiene su propia opción. Mezclarlas metería la nota de junio en la media
 * de un trimestre que ya está en el boletín.
 */
/**
 * Etiqueta de la columna: su unidad de trabajo, o el trimestre. Una prueba de
 * recuperación no pertenece a ningún trimestre —se guarda con eval 1 por dentro—
 * y ponerle «EV1» hacía pensar que era de la primera evaluación.
 */
function _etiquetaColumna(a) {
  if (Number(a.convocatoria) === 2) return '2ª conv.'
  return a.ut_id || 'EV' + a.eval
}

function _vistaNotas() {
  const evRaw = document.getElementById('notas-ev-sel')?.value ?? '0'
  const esRecuperacion = evRaw === 'R'
  const ev = esRecuperacion ? 0 : parseInt(evRaw)
  const deLa2a = a => Number(a.convocatoria) === 2
  const acts = esRecuperacion
    ? _actividades.filter(deLa2a)
    : _actividades.filter(a => !deLa2a(a) && (!ev || a.eval === ev))
  return { ev, acts, esRecuperacion }
}

async function exportNotasPDF() {
  const mid = document.getElementById('notas-mod-sel').value
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  const mod = _modulos.find(m => m.id == mid)
  const { ev, acts, esRecuperacion } = _vistaNotas()
  const alumnos = _alumnos.filter(a => a.estado === 'Activo')
  if (!acts.length || !alumnos.length) { alert('Sin datos que exportar.'); return }

  const titulo = `${mod?.abrev || 'Módulo'} — Registro de Notas` +
    (esRecuperacion ? ' · Recuperación (2ª convocatoria)' : ev ? ' · Evaluación ' + ev : '')
  const thead = `<tr><th>Alumno/a</th>${acts.map(a=>`<th>${esc(a.instrumento)}<br/><small>${esc(_etiquetaColumna(a))}</small></th>`).join('')}<th>Media act.</th></tr>`
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
    <p style="color:#6b7280;font-size:10px">La columna «Media act.» es la media ponderada de las actividades calificadas. La calificación del módulo se obtiene por resultados de aprendizaje y figura en el acta.</p>
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
    ).join('') +
    // A-5: las actividades de la 2ª convocatoria se califican aquí, pero aparte:
    // no pertenecen a ningún trimestre y no cuentan en la nota de la 1ª.
    `<option value="R"${prevEv === 'R' ? ' selected' : ''}>Recuperación · 2ª conv.</option>`
  if (evSel.value !== 'R' && parseInt(evSel.value) > evalCount) evSel.value = '0'

  _alumnos = await window.api.getAlumnos(mid)
  _actividades = await window.api.getActividades(mid)
  // Evidencias: los archivos que respaldan una nota (correcciones desde foto).
  // Se guardaban desde el asistente y no las leía nadie, así que la nota no
  // llevaba a su prueba. El art. 2.4 de la Orden 201/2024 reconoce el derecho a
  // acceder a los documentos de la evaluación: hay que poder enseñarlos.
  _evidencias = {}
  try {
    const evs = await window.api.getEvidencias(parseInt(mid))
    evs.forEach(e => {
      if (e.actividad_id == null) return
      const k = `${e.alumno_id}|${e.actividad_id}`
      if (!_evidencias[k]) _evidencias[k] = e   // la más reciente: vienen ordenadas por fecha
    })
  } catch { /* base antigua sin la tabla evidencias */ }
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
  const { ev, acts, esRecuperacion } = _vistaNotas()
  const alumnos = _alumnos.filter(a => a.estado === 'Activo')
  const wrap = document.getElementById('notas-grid-wrap')
  if (!acts.length || !alumnos.length) {
    const hasModule = !!document.getElementById('notas-mod-sel').value
    wrap.innerHTML = hasModule
      ? `<div class="empty-state">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Aún no hay datos para mostrar</div>
          <div>Cuando cargues alumnado y actividades, aquí verás el registro de notas listo para editar.</div>
        </div>`
      : `<div class="empty-state">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Selecciona un módulo para empezar</div>
          <div>El registro de notas se construye sobre alumnado y actividades del módulo activo.</div>
        </div>`
    return
  }
  const thead = `<tr>
    <th class="sticky-col">Alumno/a</th>
    ${acts.map(a => `<th title="${esc(a.descripcion)}" style="text-align:center;min-width:58px">
      <div style="font-size:10px;max-width:56px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(a.instrumento)}</div>
      <div style="font-size:9px;color:var(--text2)">${esc(_etiquetaColumna(a))}</div>
    </th>`).join('')}
    <th style="min-width:74px;text-align:center"
        title="Media de las actividades calificadas, ponderada por su peso. NO es la nota del módulo: esa se calcula por resultados de aprendizaje y está en Evaluaciones.">Media act.</th>
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
          <input class="nota-cell ${cls}" type="number" min="0" max="${act.nota_max ?? 10}" step="0.1"
            value="${rec}" data-aid="${al.id}" data-actid="${act.id}" data-rec="1"
            data-max="${act.nota_max ?? 10}"
            placeholder="${orig != null ? orig : ''}" title="Recuperación (original: ${orig != null ? orig : '—'})"
            style="border-color:var(--accent)"
            onchange="onNotaChange(this)" oninput="colorNota(this)"/>
          <div style="font-size:8px;color:var(--text3)">orig: ${orig != null ? orig : '—'}</div>
        </td>`
      }
      const nota = _notasGrid[al.id]?.[act.id] ?? ''
      const rec  = _notasRec[al.id]?.[act.id]
      const cls = nota==='' ? '' : nota>=5 ? 'nota-apto' : nota>=4 ? 'nota-riesgo' : 'nota-noapto'
      const evid = _evidencias[`${al.id}|${act.id}`]
      const clip = evid
        ? `<span onclick="abrirEvidencia('${String(evid.ruta).replace(/'/g, "\\'")}')"
                 title="Ver la evidencia de esta nota (${esc(evid.descripcion || evid.tipo || 'archivo')})"
                 style="cursor:pointer;font-size:9px;margin-left:2px">📎</span>`
        : ''
      return `<td style="text-align:center">
        <input class="nota-cell ${cls}" type="number" min="0" max="${act.nota_max ?? 10}" step="0.1"
          value="${nota}" data-aid="${al.id}" data-actid="${act.id}" data-max="${act.nota_max ?? 10}"
          onchange="onNotaChange(this)" oninput="colorNota(this)"/>
        ${rec != null ? `<div style="font-size:8px;color:var(--accent);font-weight:700" title="Nota de recuperación (efectiva)">rec: ${rec}</div>` : ''}${clip}
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

  // En la vista de 2ª convocatoria no cabe el modo «recuperar actividad»: aquí no
  // se vuelve a calificar nada del curso, se califican pruebas nuevas.
  if (esRecuperacion) {
    const avisoRec = `<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;padding:8px 14px;
        background:rgba(224,160,58,.10);border:1px solid rgba(224,160,58,.35);border-radius:9px">
      <span style="font-size:11.5px;font-weight:700;color:var(--amber);white-space:nowrap">🔁 2ª convocatoria</span>
      <span style="font-size:10.5px;color:var(--text2)">
        Pruebas de recuperación, con los criterios que les marcaste en Programación. Su nota no toca
        la 1ª convocatoria: en la 2ª, cada criterio vale la mejor de las dos notas.</span>
    </div>`
    wrap.innerHTML = avisoRec + `<div class="notas-grid"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div>`
    return
  }

  const recBar = `<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
    <button onclick="toggleRecMode()"
      style="font-size:11px;padding:4px 12px;border-radius:7px;cursor:pointer;white-space:nowrap;
             border:1px solid ${_recMode ? 'var(--accent)' : 'var(--border2)'};
             background:${_recMode ? 'rgba(201,104,45,.12)' : 'var(--bg3)'};
             color:${_recMode ? 'var(--accent)' : 'var(--text2)'};font-weight:${_recMode ? '700' : '400'}">
      ${_recMode ? '✎ Recuperar actividad · ACTIVO' : '✎ Recuperar actividad'}
    </button>
    <span style="font-size:10.5px;color:var(--text3)">
      ${_recMode
        ? 'Vuelves a calificar una actividad concreta dentro de la evaluación continua: la nota nueva sustituye a la anterior en la 1ª convocatoria y la original se conserva. Vacío = sin recuperación.'
        : 'Las celdas con «rec:» se han vuelto a calificar; esa es la nota que cuenta. Esto recupera ACTIVIDADES dentro de la 1ª convocatoria — la 2ª convocatoria se hace por criterios, en Evaluaciones.'}
    </span>
  </div>`

  wrap.innerHTML = recBar + `<div class="notas-grid"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div>`
}

/** Abrir el archivo que respalda una nota. */
async function abrirEvidencia(ruta) {
  try {
    await window.api.abrirEvidencia(ruta)
  } catch (e) {
    alert('No se ha podido abrir la evidencia: ' + (e && e.message ? e.message : e))
  }
}

async function onNotaChange(el) {
  function updateMediaFila(aid) {
  const { ev, acts } = _vistaNotas()

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
  const esRec = el.dataset.rec === '1'
  const previous = esRec
    ? _notasRec[aid]?.[actId] ?? null
    : _notasGrid[aid]?.[actId] ?? null

  // La nota se valida contra la escala de SU actividad: una práctica sobre 5 no
  // admite un 7, y un instrumento sobre 20 no se corta en 10.
  const notaMax = parseFloat(el.dataset.max) || 10
  if (val !== '') {
    const notaVal = parseFloat(val)
    if (isNaN(notaVal) || notaVal < 0 || notaVal > notaMax) {
      alert(`Nota inválida. Esta actividad se califica sobre ${notaMax}.`)
      el.value = previous ?? ''
      return
    }
  }

  try {
    if (esRec) {
      await window.api.saveNotaRec(aid, actId, val === '' ? null : parseFloat(val))
      if (!_notasRec[aid]) _notasRec[aid] = {}
      if (val === '') delete _notasRec[aid][actId]
      else _notasRec[aid][actId] = parseFloat(val)
    } else {
      await window.api.saveNota(aid, actId, val === '' ? null : parseFloat(val))
      if (!_notasGrid[aid]) _notasGrid[aid] = {}
      _notasGrid[aid][actId] = val === '' ? null : parseFloat(val)
    }
    colorNota(el)
    updateMediaFila(aid)
  } catch(e) {
    el.value = previous ?? ''
    colorNota(el)
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

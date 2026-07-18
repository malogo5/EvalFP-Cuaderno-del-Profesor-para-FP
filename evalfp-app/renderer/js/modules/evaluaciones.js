// EVALUACIONES
// ═══════════════════════════════════════════════════════════════
// 2026-07 — Correcciones de la auditoría de simulación ISO:
//  H1 Regla de oro: APTO exige TODOS los RA ≥5 (no basta media ≥5)
//  H2 Claves compuestas "RA|CE" en recuperaciones/pardones de 2ª Ord.
//  H3 Mínimo de examen configurable por módulo (config minexam_{mid})
//  H4 Media ponderada por peso de actividad dentro del RA/CE
//  H5 Boletín parcial reponderado + RA pendientes en Ev1-Ev3
//  H6 Nota efectiva = nota_rec ?? nota (recuperación con trazabilidad)
//  H7 Alumnado de baja visible (atenuado, fuera de KPIs)
//  H8 Columna Acta: entero (≥0,5 al alza), 1-4 si no superado
// ═══════════════════════════════════════════════════════════════

let _evalTab = 'ord1'
let _ord2ShowAll = false

function toggleOrd2ShowAll() {
  _ord2ShowAll = !_ord2ShowAll
  loadEvaluaciones()
}

/**
 * Media ponderada de un conjunto de actividades calificadas (H4).
 * Pesa cada actividad por su `peso`. Si ninguna actividad calificada tiene
 * peso > 0, cae al comportamiento anterior: media por tipo × ratio global
 * práctica/examen (pesoPrac/pesoExam).
 */
function _mediaActs(acts, notasAl, pesoPrac, pesoExam) {
  const graded = acts.map(a => ({ a, n: notasAl?.[a.id] })).filter(x => x.n != null)
  if (!graded.length) return null
  const totW = graded.reduce((s, x) => s + (x.a.peso || 0), 0)
  if (totW > 0) return graded.reduce((s, x) => s + x.n * (x.a.peso || 0), 0) / totW
  const gP = graded.filter(x => x.a.tipo === 'practica').map(x => x.n)
  const gE = graded.filter(x => x.a.tipo === 'examen').map(x => x.n)
  const avgP = gP.length ? gP.reduce((s, n) => s + n, 0) / gP.length : null
  const avgE = gE.length ? gE.reduce((s, n) => s + n, 0) / gE.length : null
  if (avgP !== null && avgE !== null) return avgP * pesoPrac + avgE * pesoExam
  return avgP !== null ? avgP : avgE
}

/** Nota de un RA desde sus CEs / actividades. */
function _calcNotaRA(raId, raCeList, acts, notasAl, pesoPrac, pesoExam) {
  if (raCeList?.length) {
    // Solo entra en CE-path si hay actividades vinculadas a CEs de ESTE RA concreto
    const ceIdSet = new Set(raCeList.map(c => c.id))
    const anyHasCEs = acts.some(a => {
      try { return JSON.parse(a.ces || '[]').some(id => ceIdSet.has(id)) } catch { return false }
    })
    if (anyHasCEs) {
      const ceGrades = []
      for (const ce of raCeList) {
        const ceActs = acts.filter(a => {
          try { return JSON.parse(a.ces || '[]').includes(ce.id) } catch { return false }
        })
        if (!ceActs.length) continue
        const g = _mediaActs(ceActs, notasAl, pesoPrac, pesoExam)
        if (g !== null) ceGrades.push(g)
      }
      if (ceGrades.length) return ceGrades.reduce((s, g) => s + g, 0) / ceGrades.length
      return null
    }
  }
  const raActs = acts.filter(a => String(a.ra_id) === String(raId))
  if (!raActs.length) return null
  return _mediaActs(raActs, notasAl, pesoPrac, pesoExam)
}

/** Nota de un CE concreto. */
function _calcNotaCE(ceId, acts, notasAl, pesoPrac, pesoExam) {
  const ceActs = acts.filter(a => {
    try { return JSON.parse(a.ces || '[]').includes(ceId) } catch { return false }
  })
  if (!ceActs.length) return null
  return _mediaActs(ceActs, notasAl, pesoPrac, pesoExam)
}

/**
 * H3 — true si algún examen calificado del RA queda por debajo del mínimo
 * exigido en la programación (minExam null = sin mínimo).
 */
function _raMinExamKO(raId, raCeList, acts, notasAl, minExam) {
  if (minExam == null) return false
  const ceIdSet = new Set((raCeList || []).map(c => c.id))
  const raActs = acts.filter(a => {
    if (String(a.ra_id) === String(raId)) return true
    try { return JSON.parse(a.ces || '[]').some(id => ceIdSet.has(id)) } catch { return false }
  })
  return raActs.some(a => a.tipo === 'examen' && notasAl?.[a.id] != null && notasAl[a.id] < minExam)
}

/** H8 — Nota de acta: entero, ≥0,5 al alza; módulo no superado → 1-4. */
function _actaEntera(media, superado) {
  if (media === null) return null
  const r = Math.floor(media + 0.5)
  return superado ? Math.min(10, Math.max(5, r)) : Math.max(1, Math.min(4, r))
}

/** H3 — guardar mínimo de examen del módulo y recargar. */
async function saveMinExam(mid, val) {
  const v = String(val).trim()
  if (v !== '' && (isNaN(parseFloat(v)) || parseFloat(v) < 0 || parseFloat(v) > 10)) {
    alert('Mínimo inválido (0-10, vacío = sin mínimo).')
    return
  }
  await window.api.setConfig(`minexam_${mid}`, v)
  loadEvaluaciones()
}

function setEvalTab(tab) {
  _evalTab = tab
  document.querySelectorAll('.eval-tab').forEach(t => t.classList.toggle('on', t.dataset.etab === tab))
  document.querySelectorAll('.epanel').forEach(p => p.classList.toggle('on', p.id === `epanel-${tab}`))
}

/** Expandir/contraer fila de detalle en 1ª Ordinaria. */
function toggleEvalCard(alumnoId) {
  const body = document.getElementById(`eval-detail-${alumnoId}`)
  const chev = document.getElementById(`eval-chev-${alumnoId}`)
  if (!body) return
  const open = body.style.display !== 'none'
  body.style.display = open ? 'none' : 'table-row'
  if (chev) chev.textContent = open ? '▶' : '▼'
}

/** Expandir/contraer fila de detalle en 2ª Ordinaria (IDs distintos). */
function toggleEvalCard2(alumnoId) {
  const body = document.getElementById(`eval2-detail-${alumnoId}`)
  const chev = document.getElementById(`eval2-chev-${alumnoId}`)
  if (!body) return
  const open = body.style.display !== 'none'
  body.style.display = open ? 'none' : 'table-row'
  if (chev) chev.textContent = open ? '▶' : '▼'
}

async function loadEvaluaciones() {
  const mid = document.getElementById('eval-mod-sel').value
  if (!mid) return

  // ── Cargar datos ──────────────────────────────────────────────
  const alumnosTodos = await window.api.getAlumnos(mid)
  const alumnos      = alumnosTodos.filter(a => a.estado === 'Activo')
  const alumnosBaja  = alumnosTodos.filter(a => a.estado !== 'Activo')   // H7
  const actividades  = await window.api.getActividades(mid)
  const notasArr     = await window.api.getNotasGrid(mid)

  // H6 — nota efectiva = nota_rec ?? nota; ngRec para mostrar trazabilidad
  const ng = {}, ngRec = {}
  notasArr.forEach(n => {
    if (!ng[n.alumno_id]) { ng[n.alumno_id] = {}; ngRec[n.alumno_id] = {} }
    ng[n.alumno_id][n.actividad_id] = n.nota_rec ?? n.nota
    if (n.nota_rec != null) ngRec[n.alumno_id][n.actividad_id] = { orig: n.nota, rec: n.nota_rec }
  })

  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || [...new Set(actividades.map(a => a.eval))].length || 3
  const evals     = Array.from({ length: evalCount }, (_, i) => i + 1)
  const rasBase   = modData?.ras          || []
  const cesByRa   = modData?.ces          || {}
  const asigsMod  = modData?.asignaciones || []
  const evalRas   = modData?.eval_ras     || {}   // {1:[raId,...], 2:[...], 3:[...]}

  // H2 — migrar claves legacy de recuperaciones/pardones al formato RA|CE
  {
    const sPP = actividades.filter(a => a.tipo === 'practica').reduce((s, a) => s + (a.peso || 0), 0)
    const sPE = actividades.filter(a => a.tipo === 'examen').reduce((s, a) => s + (a.peso || 0), 0)
    const tP = sPP + sPE
    await _migrateLegacyRecKeys(mid, rasBase, cesByRa, actividades, ng,
      tP > 0 ? sPP / tP : 0.30, tP > 0 ? sPE / tP : 0.70, alumnosTodos)
  }

  // Estado compartido con dashboard
  await _loadPardones(mid)
  await _loadRec2Notas(mid)

  // H3 — mínimo de examen configurado para este módulo
  const cfgAll  = await window.api.getAllConfig()
  const minRaw  = cfgAll[`minexam_${mid}`]
  const minExam = minRaw != null && String(minRaw).trim() !== '' ? parseFloat(minRaw) : null

  // ── Pesos globales (fallback si las actividades no tienen peso) ──
  const sumPP = actividades.filter(a => a.tipo === 'practica').reduce((s, a) => s + (a.peso || 0), 0)
  const sumPE = actividades.filter(a => a.tipo === 'examen').reduce((s, a) => s + (a.peso || 0), 0)
  const totP  = sumPP + sumPE
  const PRAC  = totP > 0 ? sumPP / totP : 0.30
  const EXAM  = totP > 0 ? sumPE / totP : 0.70

  // ── RAs con ponderaciones guardadas ──────────────────────────
  let raPondOverrides = {}
  try {
    const rows = await window.api.getRaPonderaciones(parseInt(mid))
    rows.forEach(r => { raPondOverrides[r.ra_id] = r.pond })
  } catch { /* sin overrides */ }

  const ras = rasBase.map(ra => ({
    ...ra,
    pond: raPondOverrides[ra.id] !== undefined ? raPondOverrides[ra.id] : (ra.pond || 0)
  }))
  const rasActivos = ras.filter(ra => actividades.some(a => String(a.ra_id) === String(ra.id)))

  // Evaluación a la que pertenece cada RA (eval_ras > actividades)
  const raEvalMap = {}
  rasActivos.forEach(ra => {
    let evRa = null
    for (const [k, ids] of Object.entries(evalRas)) if ((ids || []).includes(ra.id)) evRa = parseInt(k)
    if (evRa === null) {
      const evs = actividades.filter(a => String(a.ra_id) === String(ra.id)).map(a => a.eval)
      evRa = evs.length ? Math.min(...evs) : 99
    }
    raEvalMap[ra.id] = evRa
  })

  // ── Helpers ───────────────────────────────────────────────────
  const notaRAde = (ra, alumnoId) =>
    _calcNotaRA(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], PRAC, EXAM)

  /**
   * H1/H3 — Estado completo de un alumno:
   * media ponderada, RAs pendientes (<5 o mínimo de examen KO), RAs sin nota,
   * y veredicto normativo: superado ⇔ todos los RA con nota ≥5 y sin mínimos KO.
   * H10 — Los RA SIN nota no computan en la media: su peso se reparte
   * proporcionalmente entre los RA evaluados (media = Σ n·pond / Σ pond de
   * los calificados). Antes contaban como 0 y arrastraban la media.
   */
  function estadoAlumno(alumnoId) {
    const porRA = {}
    const conNota = []              // { nota, pond } de los RA calificados
    const pendientes = [], sinNota = []
    rasActivos.forEach(ra => {
      const n = notaRAde(ra, alumnoId)
      const minKO = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], minExam)
      porRA[ra.id] = { nota: n, minKO }
      if (n === null) { sinNota.push(ra.id); return }
      conNota.push({ nota: n, pond: ra.pond || 0 })
      if (n < 5 || minKO) pendientes.push(ra.id)
    })
    const pondSum = conNota.reduce((s, x) => s + x.pond, 0)
    const media = !conNota.length ? null
      : pondSum > 0 ? conNota.reduce((s, x) => s + x.nota * x.pond, 0) / pondSum
      : conNota.reduce((s, x) => s + x.nota, 0) / conNota.length   // sin ponderaciones: media simple
    const completo = sinNota.length === 0
    const superado = completo && !pendientes.length && media !== null && media >= 5
    return { porRA, media, pendientes, sinNota, completo, superado }
  }

  function nombreAl(al) {
    return `${al.apellidos || ''}${al.apellidos && al.nombre ? ', ' : ''}${al.nombre || ''}`
  }

  const bajaBadge = `<span style="background:var(--bg3);color:var(--text3);padding:1px 7px;border-radius:8px;font-size:10px;font-weight:700;border:1px solid var(--border2)">BAJA</span>`

  // Marca de recuperación sobre una celda de RA (H6)
  function recMark(alumnoId, raId) {
    const raActIds = actividades.filter(a => String(a.ra_id) === String(raId)).map(a => a.id)
    const recs = raActIds.map(id => ngRec[alumnoId]?.[id]).filter(Boolean)
    if (!recs.length) return ''
    const det = recs.map(r => `${r.orig ?? '—'}→${r.rec}`).join(' · ')
    return `<span title="Recuperación: ${det}" style="font-size:9px;color:var(--accent);font-weight:700"> R</span>`
  }

  // ── CSS ───────────────────────────────────────────────────────
  const css = `<style>
    .eval-tab{padding:6px 12px;border-radius:8px;cursor:pointer;font-size:12px;font-weight:500;
              color:var(--text2);transition:all .15s;white-space:nowrap;-webkit-app-region:no-drag}
    .eval-tab:hover{background:var(--bg2);color:var(--text)}
    .eval-tab.on{background:var(--bg2);color:var(--text);font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,.08)}
    .epanel{display:none}
    .epanel.on{display:block}
    .ev-tbl th{font-size:10.5px;font-weight:700;color:var(--text2);text-transform:uppercase;
               letter-spacing:.05em;padding:7px 10px;border-bottom:2px solid var(--border2);text-align:left}
    .ev-tbl td{padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:middle}
    .ev-tbl tr:last-child td{border-bottom:none}
    .ev-tbl .nc{text-align:center}
    .fila-baja td{opacity:.5}
  </style>`

  // ── Tab bar + configuración de mínimo de examen (H3) ─────────
  const minExamCtl = `<div style="display:flex;align-items:center;gap:6px;margin-left:auto;padding:0 6px">
    <span style="font-size:11px;color:var(--text3)" title="Nota mínima de examen para superar un RA (programación didáctica). Vacío = sin mínimo.">Mín. examen</span>
    <input type="number" min="0" max="10" step="0.5" value="${minExam ?? ''}" placeholder="—"
      onchange="saveMinExam(${mid}, this.value)"
      style="width:52px;font-size:11px;padding:3px 5px;border-radius:6px;border:1px solid var(--border2);
             background:var(--bg);color:var(--text);text-align:center"/>
  </div>`

  const tabBar = `<div style="display:flex;gap:2px;flex-wrap:wrap;align-items:center;background:var(--bg3);border-radius:10px;
                              padding:3px;margin-bottom:16px;border:1px solid var(--border)">
    ${evals.map(ev => {
      const lbl = ev === 1 ? '1ª Evaluación' : ev === 2 ? '2ª Evaluación' : '3ª Evaluación'
      return `<div class="eval-tab${_evalTab === `ev${ev}` ? ' on' : ''}" data-etab="ev${ev}" onclick="setEvalTab('ev${ev}')">${lbl}</div>`
    }).join('')}
    <div class="eval-tab${_evalTab === 'ord1' ? ' on' : ''}" data-etab="ord1" onclick="setEvalTab('ord1')">1ª Ordinaria</div>
    <div class="eval-tab${_evalTab === 'ord2' ? ' on' : ''}" data-etab="ord2" onclick="setEvalTab('ord2')">2ª Ordinaria</div>
    ${minExamCtl}
  </div>`

  // ════════════════════════════════════════════════════════════
  // PANEL: EVALUACIÓN PARCIAL
  // ════════════════════════════════════════════════════════════
  function renderEvalPanel(ev) {
    // Actividades de esta evaluación (para la barra de actividades)
    const acts = actividades.filter(a => a.eval === ev)

    // Qué RAs pertenecen a esta eval: eval_ras tiene prioridad sobre a.eval de actividades
    const raIdsConf = evalRas[String(ev)] || evalRas[ev] || []
    const rasCov = raIdsConf.length
      ? rasActivos.filter(ra => raIdsConf.includes(ra.id))
      : rasActivos.filter(ra => acts.some(a => String(a.ra_id) === String(ra.id)))

    if (!acts.length && !rasCov.length) return `<div class="card"><p style="color:var(--text2);font-size:13px;padding:6px 0">Sin actividades configuradas para esta evaluación.</p></div>`

    const pracs = acts.filter(a => a.tipo === 'practica')
    const exams = acts.filter(a => a.tipo === 'examen')
    const actsBar = `<div class="card" style="padding:11px 16px;margin-bottom:12px">
      <div style="display:flex;gap:7px;flex-wrap:wrap;align-items:center">
        <span style="font-size:11px;color:var(--text3)">Actividades:</span>
        ${pracs.map(a => `<span style="padding:2px 8px;border-radius:6px;background:rgba(74,144,217,.1);border:1px solid rgba(74,144,217,.2);font-size:11px;color:var(--text2)">📝 ${esc(a.desc || a.descripcion || 'Práctica')} <span style="color:var(--text3)">${a.peso || 0}%</span></span>`).join('')}
        ${exams.map(a => `<span style="padding:2px 8px;border-radius:6px;background:rgba(201,154,61,.12);border:1px solid rgba(201,154,61,.2);font-size:11px;color:var(--text2)">📋 ${esc(a.desc || a.descripcion || 'Examen')} <span style="color:var(--text3)">${a.peso || 0}%</span></span>`).join('')}
      </div>
    </div>`

    if (!rasCov.length) return actsBar + `<div class="card"><p style="color:var(--text2);font-size:13px;padding:6px 0">Sin RAs vinculados a esta evaluación.</p></div>`

    // ── H5: Boletín de la evaluación (media reponderada acumulada + pendientes) ──
    const rasVistos = rasActivos.filter(ra => raEvalMap[ra.id] <= ev)
    const bolRows = [...alumnos, ...alumnosBaja].map(al => {
      const esBaja = al.estado !== 'Activo'
      let sum = 0, pond = 0
      const pend = [], sinN = []
      rasVistos.forEach(ra => {
        const n = notaRAde(ra, al.id)
        const minKO = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[al.id], minExam)
        if (n !== null) { sum += n * ra.pond; pond += ra.pond }
        if (n === null) sinN.push(ra.id)
        else if (n < 5 || minKO) pend.push(ra.id + (minKO && n >= 5 ? ' ⚠mín' : ''))
      })
      const bol = pond > 0 ? sum / pond : null
      const bolTxt = bol !== null ? bol.toFixed(1) : '—'
      const bolCls = bol === null ? '' : bol >= 5 ? 'nota-apto' : bol >= 4 ? 'nota-riesgo' : 'nota-noapto'
      const pendTxt = pend.length
        ? `<span style="color:var(--red);font-weight:600">${pend.join(', ')}</span>`
        : sinN.length === rasVistos.length ? '<span style="color:var(--text3)">sin notas</span>'
        : '<span style="color:var(--green)">—</span>'
      return `<tr${esBaja ? ' class="fila-baja"' : ''}>
        <td>${esc(nombreAl(al))} ${esBaja ? bajaBadge : ''}</td>
        <td class="nc" style="font-weight:700"><span class="${bolCls}">${bolTxt}</span></td>
        <td style="font-size:11px">${pendTxt}</td>
      </tr>`
    }).join('')

    const boletinCard = `<div style="border:1px solid var(--border2);border-radius:10px;overflow:hidden;margin-bottom:12px">
      <div style="padding:9px 14px;background:var(--bg3);border-bottom:1px solid var(--border);display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <span style="font-weight:700;font-size:13px">Boletín ${ev}ª evaluación</span>
        <span style="font-size:11px;color:var(--text3)">media reponderada de los RA trabajados hasta ahora (${rasVistos.map(r => r.id).join(', ')}) · el boletín NO sustituye al registro de RA pendientes</span>
      </div>
      <div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
        <thead><tr><th>Alumno/a</th><th class="nc" style="min-width:70px">Boletín</th><th>RA pendientes (acumulado)</th></tr></thead>
        <tbody>${bolRows}</tbody>
      </table></div>
    </div>`

    const raSecs = rasCov.map(ra => {
      const ceLst = cesByRa[ra.id] || []
      // Actividades para calificación de este RA: todas las suyas (eval_ras es fuente de verdad)
      const actsRA = raIdsConf.length
        ? actividades.filter(a => String(a.ra_id) === String(ra.id))
        : acts
      const ceCov = new Set()
      actsRA.forEach(a => { try { JSON.parse(a.ces || '[]').forEach(id => ceCov.add(id)) } catch { /* ces inválido */ } })
      const ceLstEv = ceLst.filter(ce => ceCov.has(ce.id))

      const belowFive = alumnos.filter(al => {
        const n = _calcNotaRA(ra.id, ceLst, actsRA, ng[al.id], PRAC, EXAM)
        const minKO = _raMinExamKO(ra.id, ceLst, actsRA, ng[al.id], minExam)
        return n !== null && (n < 5 || minKO)
      }).length
      const alertBadge = belowFive > 0
        ? `<span style="background:rgba(178,59,59,.1);color:var(--red);padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700">${belowFive} pendiente${belowFive > 1 ? 's' : ''}</span>`
        : `<span style="background:rgba(79,121,66,.1);color:var(--green);padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700">Todos ≥5</span>`

      const rows = [...alumnos, ...alumnosBaja].map(al => {
        const esBaja = al.estado !== 'Activo'
        const notaRA = _calcNotaRA(ra.id, ceLst, actsRA, ng[al.id], PRAC, EXAM)
        const minKO  = _raMinExamKO(ra.id, ceLst, actsRA, ng[al.id], minExam)
        const naTxt  = notaRA !== null ? notaRA.toFixed(1) : '—'
        const naCls  = notaRA === null ? '' : (notaRA >= 5 && !minKO) ? 'nota-apto' : notaRA >= 4 ? 'nota-riesgo' : 'nota-noapto'
        const minBadge = minKO && notaRA !== null && notaRA >= 5
          ? ` <span title="Examen por debajo del mínimo (${minExam}): RA no superado aunque la media sea ≥5" style="color:var(--red);font-weight:700;font-size:10px">⚠mín</span>` : ''
        const ceCells = ceLstEv.map(ce => {
          const n   = _calcNotaCE(ce.id, actsRA, ng[al.id], PRAC, EXAM)
          const txt = n !== null ? n.toFixed(1) : '—'
          const cls = n === null ? '' : n >= 5 ? 'nota-apto' : n >= 4 ? 'nota-riesgo' : 'nota-noapto'
          return `<td class="nc"><span class="${cls}" style="font-size:12px;font-weight:600">${txt}</span></td>`
        }).join('')
        return `<tr${esBaja ? ' class="fila-baja"' : ''}>
          <td>${esc(nombreAl(al))} ${esBaja ? bajaBadge : ''}</td>
          ${ceCells}
          <td class="nc" style="font-weight:700;font-size:13px"><span class="${naCls}">${naTxt}</span>${recMark(al.id, ra.id)}${minBadge}</td>
        </tr>`
      }).join('')

      return `<div style="border:1px solid var(--border2);border-radius:10px;overflow:hidden;margin-bottom:10px">
        <div style="padding:9px 14px;background:var(--bg3);display:flex;align-items:center;gap:8px;
                    border-bottom:1px solid var(--border);flex-wrap:wrap">
          <span style="font-weight:700;font-size:13px;color:var(--accent)">${esc(ra.id)}</span>
          <span style="flex:1;font-size:11.5px;color:var(--text2)">${esc(ra.nombre || '')}</span>
          <span style="background:rgba(201,104,45,.1);color:var(--accent);padding:1px 6px;border-radius:4px;font-size:10px;font-weight:700">${ra.pond}%</span>
          ${alertBadge}
        </div>
        ${ceLstEv.length
          ? `<div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
              <thead><tr>
                <th>Alumno/a</th>
                ${ceLstEv.map(ce => `<th class="nc" style="min-width:58px;font-size:10px">${esc(ce.id)}</th>`).join('')}
                <th class="nc" style="min-width:70px">Nota RA</th>
              </tr></thead>
              <tbody>${rows}</tbody>
             </table></div>`
          : `<div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
              <thead><tr><th>Alumno/a</th><th class="nc" style="min-width:70px">Nota RA</th></tr></thead>
              <tbody>${rows}</tbody>
             </table></div>`
        }
      </div>`
    }).join('')

    return actsBar + boletinCard + raSecs
  }

  // ════════════════════════════════════════════════════════════
  // PANEL: 1ª ORDINARIA  (nota final calculada — solo lectura)
  // H1: APTO exige todos los RA superados. H8: columna Acta.
  // ════════════════════════════════════════════════════════════
  function renderOrd1Panel() {
    if (!rasActivos.length) return `<div class="card"><p style="color:var(--text2);font-size:13px;padding:6px 0">Sin RAs con actividades calificables.</p></div>`

    const estados = {}
    alumnos.forEach(al => { estados[al.id] = estadoAlumno(al.id) })

    const aptos    = alumnos.filter(al => estados[al.id].superado).length
    const noAptos  = alumnos.filter(al => estados[al.id].completo && !estados[al.id].superado).length
    const pendEval = alumnos.filter(al => !estados[al.id].completo && estados[al.id].media !== null).length
    const medias   = alumnos.map(al => estados[al.id].media).filter(n => n !== null)
    const media    = medias.length ? (medias.reduce((s, n) => s + n, 0) / medias.length).toFixed(1) : '—'

    const kpis = `<div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${alumnos.length}</div><div style="font-size:10px;color:var(--text2)">Activos</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--green)">${aptos}</div><div style="font-size:10px;color:var(--text2)">Superan (todos los RA ≥5)</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--red)">${noAptos}</div><div style="font-size:10px;color:var(--text2)">No superan</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--amber, #c99a3d)">${pendEval}</div><div style="font-size:10px;color:var(--text2)">Sin evaluar del todo</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${media}</div><div style="font-size:10px;color:var(--text2)">Media</div></div>
    </div>`

    const raHeaders = rasActivos.map(ra =>
      `<th class="nc" style="min-width:70px;font-size:10px;white-space:nowrap" title="${esc(ra.nombre)}">
        ${esc(ra.id)}<br><span style="font-size:9px;opacity:.65">${ra.pond}%</span></th>`
    ).join('')

    const filaAlumno = (al, esBaja) => {
      const st = esBaja ? estadoAlumno(al.id) : estados[al.id]
      const nFinal = st.media
      const nFTxt  = nFinal !== null ? nFinal.toFixed(1) : '—'
      const nFCls  = nFinal === null ? '' : st.superado ? 'nota-apto' : nFinal >= 4 ? 'nota-riesgo' : 'nota-noapto'

      // H1 — veredicto normativo
      let apto, aptoSty, motivo = ''
      if (esBaja)               { apto = '—';          aptoSty = 'color:var(--text3)' }
      else if (nFinal === null) { apto = '—';          aptoSty = 'color:var(--text3)' }
      else if (!st.completo)    { apto = 'PENDIENTE';  aptoSty = 'color:var(--amber, #c99a3d)'; motivo = `Sin nota: ${st.sinNota.join(', ')}` }
      else if (st.superado)     { apto = 'APTO/A';     aptoSty = 'color:var(--green)' }
      else                      { apto = 'NO APTO/A';  aptoSty = 'color:var(--red)'; motivo = st.pendientes.length ? `RA pendientes: ${st.pendientes.join(', ')}` : '' }

      // H8 — acta
      const acta = (esBaja || nFinal === null || !st.completo) ? '—' : _actaEntera(nFinal, st.superado)
      const actaCls = acta === '—' ? '' : acta >= 5 ? 'nota-apto' : 'nota-noapto'

      const raCells = rasActivos.map(ra => {
        const { nota: n, minKO } = st.porRA[ra.id]
        const txt = n !== null ? n.toFixed(1) : '—'
        const cls = n === null ? '' : (n >= 5 && !minKO) ? 'nota-apto' : n >= 4 ? 'nota-riesgo' : 'nota-noapto'
        const warn = minKO && n !== null && n >= 5 ? `<span title="Examen bajo mínimo (${minExam})" style="color:var(--red);font-size:9px;font-weight:700">⚠</span>` : ''
        return `<td class="nc" style="font-size:12px;font-weight:600"><span class="${cls}">${txt}</span>${recMark(al.id, ra.id)}${warn}</td>`
      }).join('')

      const raBlocks = rasActivos.map(ra => {
        const { nota: nRa, minKO } = st.porRA[ra.id]
        const ceLst = cesByRa[ra.id] || []
        const okRA = nRa !== null && nRa >= 5 && !minKO
        const border = nRa === null ? 'var(--border2)' : okRA ? 'var(--green)' : 'var(--red)'
        const raCls  = nRa === null ? '' : okRA ? 'nota-apto' : nRa >= 4 ? 'nota-riesgo' : 'nota-noapto'

        const ceChips = ceLst.map(ce => {
          const n   = _calcNotaCE(ce.id, actividades, ng[al.id], PRAC, EXAM)
          const bg  = n === null ? 'var(--bg3)' : n >= 5 ? 'rgba(79,121,66,.1)' : 'rgba(178,59,59,.07)'
          const brd = n === null ? 'var(--border)' : n >= 5 ? 'rgba(79,121,66,.3)' : 'rgba(178,59,59,.25)'
          const clr = n === null ? 'var(--text2)' : n >= 5 ? 'var(--green)' : 'var(--red)'
          return `<span style="display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:6px;
              background:${bg};border:1px solid ${brd};font-size:11px;margin:0 4px 4px 0">
            <span style="font-weight:700;color:var(--accent);font-size:10px">${esc(ce.id)}</span>
            <span style="font-weight:600;color:${clr}">${n !== null ? n.toFixed(1) : '—'}</span>
          </span>`
        }).join('')

        return `<div style="margin-bottom:6px;padding:8px 10px;background:var(--bg);border-radius:6px;border-left:3px solid ${border}">
          <div style="display:flex;align-items:center;gap:8px;${ceLst.length ? 'margin-bottom:5px' : ''}">
            <span style="font-weight:700;font-size:11px;color:var(--accent)">${esc(ra.id)}</span>
            <span style="font-size:10.5px;color:var(--text2);flex:1">${esc(ra.nombre || '')}</span>
            ${minKO ? `<span style="color:var(--red);font-size:10px;font-weight:700">⚠ examen &lt; mín. ${minExam}</span>` : ''}
            <span class="${raCls}" style="font-weight:700;font-size:13px">${nRa !== null ? nRa.toFixed(1) : '—'}</span>
          </div>
          ${ceChips || '<span style="font-size:10.5px;color:var(--text3)">Sin CEs asignados</span>'}
        </div>`
      }).join('')

      return `
        <tr onclick="toggleEvalCard(${al.id})" style="cursor:pointer" ${esBaja ? 'class="fila-baja"' : ''}
            onmouseover="this.style.background='var(--bg3)'" onmouseout="this.style.background=''">
          <td>
            <span id="eval-chev-${al.id}" style="font-size:10px;color:var(--text3);margin-right:8px;display:inline-block">▶</span>
            ${esc(nombreAl(al))} ${esBaja ? bajaBadge : ''}
          </td>
          ${raCells}
          <td class="nc" style="font-weight:700;font-size:14px"><span class="${nFCls}">${nFTxt}</span></td>
          <td class="nc" style="font-weight:700;font-size:14px"><span class="${actaCls}">${acta}</span></td>
          <td style="text-align:center;font-weight:700;font-size:11px;${aptoSty}" ${motivo ? `title="${esc(motivo)}"` : ''}>${apto}${motivo ? ' *' : ''}</td>
          <td style="text-align:center">
            <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();genBoletin(${al.id})">📄 Boletín</button>
          </td>
        </tr>
        <tr id="eval-detail-${al.id}" style="display:none">
          <td colspan="${rasActivos.length + 5}" style="padding:0">
            <div style="padding:10px 14px 12px;background:var(--bg3)">${raBlocks}</div>
          </td>
        </tr>`
    }

    const rows = alumnos.map(al => filaAlumno(al, false)).join('')
      + alumnosBaja.map(al => filaAlumno(al, true)).join('')

    return `<div style="font-size:11px;color:var(--text2);margin-bottom:12px;display:flex;gap:14px;flex-wrap:wrap">
        <span>Nota RA = media de actividades ponderada por peso · Nota Final = media RAs ponderada, reponderada sobre los RA evaluados (los RA sin nota no computan)</span>
        <span style="color:var(--text3)"><b>Regla de oro:</b> APTO/A exige TODOS los RA ≥5${minExam != null ? ` y exámenes ≥${minExam}` : ''}; la media no compensa un RA suspenso</span>
      </div>
      ${kpis}
      <div class="card" style="padding:0;overflow:hidden">
        <div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
          <thead><tr>
            <th>Alumno/a</th>
            ${raHeaders}
            <th class="nc" style="min-width:70px">Nota Final</th>
            <th class="nc" style="min-width:52px" title="Calificación de acta: entero (≥0,5 al alza); 1-4 si el módulo no está superado">Acta</th>
            <th class="nc" style="min-width:90px">Resultado</th>
            <th style="width:110px"></th>
          </tr></thead>
          <tbody>${rows}</tbody>
        </table></div>
      </div>`
  }

  // ════════════════════════════════════════════════════════════
  // PANEL: 2ª ORDINARIA
  // H2: claves compuestas "RA|CE" en rec/pardones (sin colisiones).
  // H1: veredicto por regla de oro. H8: columna Acta.
  // RAs/CEs aprobados en 1ª Ordinaria: nota bloqueada (solo lectura).
  // ════════════════════════════════════════════════════════════
  function renderOrd2Panel() {
    if (!rasActivos.length) return `<div class="card"><p style="color:var(--text2);font-size:13px;padding:6px 0">Sin RAs con actividades calificables.</p></div>`

    const ceKey = (raId, ceId) => `${raId}|${ceId}`   // H2

    // ── Nota efectiva de un CE en 2ª ordinaria ─────────────────
    // Prioridad: perdón → nota recuperación → nota original si >=5 → pendiente
    function ceNotaOrd2(alumnoId, raId, ceId) {
      const k = ceKey(raId, ceId)
      if (_pardones[alumnoId]?.has(k)) return { nota: 5, fuente: 'pardon' }
      const rec = _rec2Notas[alumnoId]?.[k]
      if (rec != null) return { nota: rec, fuente: 'rec' }
      const orig = _calcNotaCE(ceId, actividades, ng[alumnoId], PRAC, EXAM)
      if (orig !== null && orig >= 5) return { nota: orig, fuente: 'orig_ok' }
      return { nota: orig, fuente: 'pendiente' }
    }

    // ── Nota de un RA en 2ª ordinaria ─────────────────────────
    // Si RA superado en 1ª (≥5 y sin mínimo KO): se mantiene bloqueado.
    // Si no: recalcular desde CEs con ceNotaOrd2.
    function raNotaOrd2(alumnoId, ra) {
      const orig  = notaRAde(ra, alumnoId)
      const minKO = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], minExam)
      if (orig === null || (orig >= 5 && !minKO)) return { nota: orig, fuente: 'orig_ok', orig }

      const ceLst = cesByRa[ra.id] || []
      let ceIds = ceLst.map(c => c.id)

      if (!ceIds.length) {
        // Fallback a asigsMod
        const seen = new Set()
        asigsMod.filter(a => a.ra === ra.id).forEach(asig =>
          (asig.ces || []).forEach(id => { if (!seen.has(id)) { seen.add(id); ceIds.push(id) } })
        )
      }

      if (!ceIds.length) return { nota: orig, fuente: 'orig_fail', orig }

      const grades = ceIds.map(id => ceNotaOrd2(alumnoId, ra.id, id).nota).filter(n => n != null)
      if (!grades.length) return { nota: orig, fuente: 'pendiente', orig }
      return { nota: grades.reduce((s, n) => s + n, 0) / grades.length, fuente: 'rec', orig }
    }

    // ── Estado 2ª ordinaria (H1: regla de oro · H10: reponderación) ──
    function estadoOrd2(alumnoId) {
      const porRA = {}
      const conNota = []
      const pendientes = [], sinNota = []
      rasActivos.forEach(ra => {
        const r = raNotaOrd2(alumnoId, ra)
        porRA[ra.id] = r
        if (r.nota === null) { sinNota.push(ra.id); return }
        conNota.push({ nota: r.nota, pond: ra.pond || 0 })
        if (r.nota < 5) pendientes.push(ra.id)
      })
      const pondSum = conNota.reduce((s, x) => s + x.pond, 0)
      const media = !conNota.length ? null
        : pondSum > 0 ? conNota.reduce((s, x) => s + x.nota * x.pond, 0) / pondSum
        : conNota.reduce((s, x) => s + x.nota, 0) / conNota.length
      const completo = sinNota.length === 0
      const superado = completo && !pendientes.length && media !== null && media >= 5
      return { porRA, media, pendientes, sinNota, completo, superado }
    }

    // ── KPIs ──────────────────────────────────────────────────
    const conRec = alumnos.filter(al => {
      const st = estadoAlumno(al.id)
      return st.pendientes.length > 0
    })
    const estados2 = {}
    alumnos.forEach(al => { estados2[al.id] = estadoOrd2(al.id) })
    const aptosRec   = alumnos.filter(al => estados2[al.id].superado).length
    const noAptosRec = alumnos.filter(al => estados2[al.id].completo && !estados2[al.id].superado).length
    const notasRec   = alumnos.map(al => estados2[al.id].media).filter(n => n !== null)
    const mediaRec   = notasRec.length ? (notasRec.reduce((s, n) => s + n, 0) / notasRec.length).toFixed(1) : '—'

    const kpis = `<div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${alumnos.length}</div><div style="font-size:10px;color:var(--text2)">Alumnos</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--red)">${conRec.length}</div><div style="font-size:10px;color:var(--text2)">Con recuperación</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--green)">${aptosRec}</div><div style="font-size:10px;color:var(--text2)">Superan 2ª (todos RA ≥5)</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--red)">${noAptosRec}</div><div style="font-size:10px;color:var(--text2)">No superan 2ª</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${mediaRec}</div><div style="font-size:10px;color:var(--text2)">Media 2ª</div></div>
    </div>`

    const raHeaders = rasActivos.map(ra =>
      `<th class="nc" style="min-width:70px;font-size:10px;white-space:nowrap" title="${esc(ra.nombre)}">
        ${esc(ra.id)}<br><span style="font-size:9px;opacity:.65">${ra.pond}%</span></th>`
    ).join('')

    const listaAlumnos = _ord2ShowAll ? alumnos : conRec

    const rows = listaAlumnos.map(al => {
      const st1 = estadoAlumno(al.id)
      const st2 = estados2[al.id]
      const nFOrig = st1.media
      const nF2    = st2.media
      const nF2Txt = nF2 !== null ? nF2.toFixed(1) : '—'
      const nF2Cls = nF2 === null ? '' : st2.superado ? 'nota-apto' : nF2 >= 4 ? 'nota-riesgo' : 'nota-noapto'

      // H1 — veredicto por regla de oro
      let apto, aptoSty, motivo = ''
      if (nF2 === null)        { apto = '—';         aptoSty = 'color:var(--text3)' }
      else if (!st2.completo)  { apto = 'PENDIENTE'; aptoSty = 'color:var(--amber, #c99a3d)'; motivo = `Sin nota: ${st2.sinNota.join(', ')}` }
      else if (st2.superado)   { apto = 'APTO/A';    aptoSty = 'color:var(--green)' }
      else                     { apto = 'NO APTO/A'; aptoSty = 'color:var(--red)'; motivo = st2.pendientes.length ? `RA pendientes: ${st2.pendientes.join(', ')}` : '' }

      const acta = (nF2 === null || !st2.completo) ? '—' : _actaEntera(nF2, st2.superado)
      const actaCls = acta === '—' ? '' : acta >= 5 ? 'nota-apto' : 'nota-noapto'

      const changed = nFOrig !== null && nF2 !== null && Math.abs(nF2 - nFOrig) > 0.05
      const changeEl = changed ? `<div style="font-size:9px;color:var(--text3)">1ª: ${nFOrig.toFixed(1)}</div>` : ''

      const raCells = rasActivos.map(ra => {
        const { nota, fuente, orig } = st2.porRA[ra.id]
        const txt    = nota !== null ? nota.toFixed(1) : '—'
        const cls    = nota === null ? '' : nota >= 5 ? 'nota-apto' : nota >= 4 ? 'nota-riesgo' : 'nota-noapto'
        const locked = fuente === 'orig_ok'
        return `<td class="nc" style="font-size:12px;font-weight:600">
          <span class="${cls}">${txt}${locked ? ' 🔒' : ''}</span>
          ${!locked && orig !== null ? `<div style="font-size:9px;color:var(--text3)">(1ª:${orig.toFixed(1)})</div>` : ''}
        </td>`
      }).join('')

      // ── Detalle expandible: bloque por RA ─────────────────────
      const raBlocks = rasActivos.map(ra => {
        const { nota: raRec, fuente: raFuente, orig: raOrig } = st2.porRA[ra.id]
        const ceLst     = cesByRa[ra.id] || []
        const raAprobado = raFuente === 'orig_ok'
        const borderColor = raRec === null ? 'var(--border2)' : raRec >= 5 ? 'var(--green)' : 'var(--red)'
        const raCls = raRec === null ? '' : raRec >= 5 ? 'nota-apto' : raRec >= 4 ? 'nota-riesgo' : 'nota-noapto'

        const ceRows = ceLst.map(ce => {
          const k          = ceKey(ra.id, ce.id)
          const raIdSafe   = ra.id.replace(/'/g, "\\'")
          const ceIdSafe   = ce.id.replace(/'/g, "\\'")
          const { nota: ceNota } = ceNotaOrd2(al.id, ra.id, ce.id)
          const ceOrigNota = _calcNotaCE(ce.id, actividades, ng[al.id], PRAC, EXAM)
          const pardoned   = _pardones[al.id]?.has(k)
          const rec2n      = _rec2Notas[al.id]?.[k]

          // CE sin nota original ni recuperación ni perdón → no visto aún, omitir
          if (ceOrigNota === null && rec2n == null && !pardoned) return ''

          // CE bloqueado sólo si su propia nota original es >= 5 (sin nota rec ni perdón)
          const ceLocked   = ceOrigNota !== null && ceOrigNota >= 5 && rec2n == null && !pardoned

          // CE bloqueado (ya aprobado individualmente)
          if (ceLocked) {
            const n   = ceOrigNota !== null ? ceOrigNota.toFixed(1) : '—'
            const cls = ceOrigNota !== null && ceOrigNota >= 5 ? 'nota-apto' : ''
            return `<div style="display:flex;align-items:center;gap:8px;padding:4px 0;
                                 border-top:1px solid var(--border);font-size:11px;opacity:.7">
              <span style="width:16px;flex-shrink:0">✅</span>
              <span style="color:var(--accent);font-weight:700;min-width:36px;flex-shrink:0">${esc(ce.id)}</span>
              <span style="flex:1;color:var(--text2);font-size:10.5px">${esc(ce.texto.length > 90 ? ce.texto.slice(0, 89) + '…' : ce.texto)}</span>
              <span class="${cls}" style="font-weight:600;font-size:13px;min-width:36px;text-align:center">${n} 🔒</span>
            </div>`
          }

          // CE suspendido: campo de nota de recuperación + botón Aprobado
          const icon = pardoned ? '✅' : (ceNota !== null && ceNota >= 5) ? '✅' : (rec2n != null && rec2n < 5) ? '❌' : '⬜'
          const inputBorder = (rec2n != null && rec2n >= 5) || pardoned ? 'var(--green)' : rec2n != null ? 'var(--red)' : 'var(--border2)'
          const inputBg     = (rec2n != null && rec2n >= 5) || pardoned ? 'rgba(16,185,129,.08)' : rec2n != null ? 'rgba(239,68,68,.06)' : 'var(--bg)'
          const origLabel   = ceOrigNota !== null
            ? `<span style="font-size:9px;color:var(--text3)">(1ª:${ceOrigNota.toFixed(1)})</span>` : ''

          const notaInput = `<input type="number" min="0" max="10" step="0.1"
            value="${rec2n != null ? rec2n : ''}" placeholder="Rec."
            onchange="event.stopPropagation();saveRec2Nota(${mid},${al.id},'${raIdSafe}','${ceIdSafe}',this.value)"
            onclick="event.stopPropagation()"
            style="width:68px;font-size:10px;padding:2px 4px;border-radius:4px;
                   border:1px solid ${inputBorder};background:${inputBg};
                   color:var(--text);text-align:center"/>`

          const pardonBtn = pardoned
            ? `<button onclick="event.stopPropagation();togglePardonCe(${mid},${al.id},'${raIdSafe}','${ceIdSafe}')"
                  style="font-size:10px;padding:1px 7px;border-radius:5px;border:1px solid var(--border2);
                         background:rgba(16,185,129,.1);color:var(--green);cursor:pointer;white-space:nowrap">↩ Quitar</button>`
            : `<button onclick="event.stopPropagation();togglePardonCe(${mid},${al.id},'${raIdSafe}','${ceIdSafe}')"
                  style="font-size:10px;padding:1px 7px;border-radius:5px;border:1px solid var(--border2);
                         background:var(--bg3);color:var(--text2);cursor:pointer;white-space:nowrap">Aprobado</button>`

          return `<div style="display:flex;align-items:center;gap:8px;padding:4px 0;
                               border-top:1px solid var(--border);font-size:11px;flex-wrap:wrap">
            <span style="flex-shrink:0;width:16px">${icon}</span>
            <span style="color:var(--accent);font-weight:700;min-width:36px;flex-shrink:0">${esc(ce.id)}</span>
            <span style="flex:1;color:var(--text2);font-size:10.5px;min-width:60px">${esc(ce.texto.length > 90 ? ce.texto.slice(0, 89) + '…' : ce.texto)}</span>
            ${origLabel}
            ${notaInput}
            ${pardonBtn}
          </div>`
        }).join('')

        return `<div style="margin-bottom:6px;padding:8px 10px;background:var(--bg);border-radius:6px;border-left:3px solid ${borderColor}">
          <div style="display:flex;align-items:center;gap:8px;${ceLst.length ? 'margin-bottom:5px' : ''}">
            <span style="font-weight:700;font-size:11px;color:var(--accent)">${esc(ra.id)}</span>
            <span style="font-size:10.5px;color:var(--text2);flex:1">${esc(ra.nombre || '')}</span>
            ${raAprobado
              ? `<span class="nota-apto" style="font-weight:700;font-size:13px">${raOrig !== null ? raOrig.toFixed(1) : '—'} 🔒</span>`
              : `<span class="${raCls}" style="font-weight:700;font-size:13px">${raRec !== null ? raRec.toFixed(1) : '—'}</span>`
            }
          </div>
          ${ceRows || '<span style="font-size:10.5px;color:var(--text3)">Sin CEs asignados</span>'}
        </div>`
      }).join('')

      return `
        <tr onclick="toggleEvalCard2(${al.id})" style="cursor:pointer"
            onmouseover="this.style.background='var(--bg3)'" onmouseout="this.style.background=''">
          <td>
            <span id="eval2-chev-${al.id}" style="font-size:10px;color:var(--text3);margin-right:8px;display:inline-block">▶</span>
            ${esc(nombreAl(al))}
          </td>
          ${raCells}
          <td class="nc" style="font-weight:700;font-size:14px">
            <span class="${nF2Cls}">${nF2Txt}</span>
            ${changeEl}
          </td>
          <td class="nc" style="font-weight:700;font-size:14px"><span class="${actaCls}">${acta}</span></td>
          <td style="text-align:center;font-weight:700;font-size:11px;${aptoSty}" ${motivo ? `title="${esc(motivo)}"` : ''}>${apto}${motivo ? ' *' : ''}</td>
        </tr>
        <tr id="eval2-detail-${al.id}" style="display:none">
          <td colspan="${rasActivos.length + 4}" style="padding:0">
            <div style="padding:10px 14px 12px;background:var(--bg3)">${raBlocks}</div>
          </td>
        </tr>`
    }).join('')

    return `<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap">
      <p style="font-size:11px;color:var(--text2);flex:1;margin:0">
        RAs y CEs aprobados en 1ª Ordinaria aparecen bloqueados 🔒.
        Para los suspendidos, introduce la nota de recuperación o usa <b>Aprobado</b> para excusar el CE.
        <b>Regla de oro:</b> APTO/A exige todos los RA ≥5.
      </p>
      <button onclick="toggleOrd2ShowAll()"
        style="font-size:11px;padding:4px 12px;border-radius:7px;cursor:pointer;white-space:nowrap;
               border:1px solid var(--border2);background:${_ord2ShowAll ? 'var(--bg2)' : 'var(--bg3)'};color:var(--text2)">
        ${_ord2ShowAll ? '👁 Ocultar aprobados' : '👁 Mostrar todos'}
      </button>
    </div>
    ${kpis}
    <div class="card" style="padding:0;overflow:hidden">
      <div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
        <thead><tr>
          <th>Alumno/a</th>
          ${raHeaders}
          <th class="nc" style="min-width:90px">Nota Final 2ª</th>
          <th class="nc" style="min-width:52px" title="Calificación de acta: entero (≥0,5 al alza); 1-4 si el módulo no está superado">Acta</th>
          <th class="nc" style="min-width:90px">Resultado</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table></div>
    </div>`
  }

  // ── Ensamblar todo ────────────────────────────────────────────
  const evalPanels = evals.map(ev =>
    `<div id="epanel-ev${ev}" class="epanel${_evalTab === `ev${ev}` ? ' on' : ''}">${renderEvalPanel(ev)}</div>`
  ).join('')

  const content = css + tabBar + evalPanels
    + `<div id="epanel-ord1" class="epanel${_evalTab === 'ord1' ? ' on' : ''}">${renderOrd1Panel()}</div>`
    + `<div id="epanel-ord2" class="epanel${_evalTab === 'ord2' ? ' on' : ''}">${renderOrd2Panel()}</div>`

  document.getElementById('eval-content').innerHTML = content
    || '<div style="color:var(--text2);padding:20px">Sin datos de notas aún.</div>'
}

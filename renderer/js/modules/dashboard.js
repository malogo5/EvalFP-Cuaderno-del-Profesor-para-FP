// DASHBOARD
// ═══════════════════════════════════════════════════════════════

// ── Perdones: CEs que el profesor ha excusado por alumno ────────
// H2: las claves de CE son COMPUESTAS "RA|CE" (p.ej. "RA3|CR1") porque los
// IDs de CE se repiten entre RAs y una clave simple provoca colisiones.
let _pardones  = {}          // { alumnoId(number): Set<"RA|CE"> }
let _recSort   = 'pendientes' // 'pendientes' | 'nombre' | 'aprobados'
const _recOpenSet  = new Set() // alumnoIds con tarjeta expandida (2ª Ordinaria)
let _ord1Sort    = 'nombre'  // 'nombre' | 'aptos' | 'noAptos'
const _ord1OpenSet = new Set() // alumnoIds con tarjeta expandida (1ª Ordinaria)
let _rec2Notas  = {}         // { alumnoId: { "RA|CE": nota } } — calificaciones 2ª Ordinaria por CE
let _rec2Timer  = null

/**
 * Carga de la tabla `calificaciones_ce` los criterios dados por alcanzados y las
 * notas de la 2ª convocatoria. Antes vivían como JSON en la configuración y no
 * los veía nadie más que esta pantalla.
 */
async function _loadCalificacionesCE(mid) {
  _pardones = {}
  _rec2Notas = {}
  try {
    const filas = await window.api.getCalificacionesCE(parseInt(mid))
    for (const f of filas) {
      const aid = Number(f.alumno_id)
      const k = `${f.ra_id}|${f.ce_id}`
      if (f.perdonado) {
        if (!_pardones[aid]) _pardones[aid] = new Set()
        _pardones[aid].add(k)
      }
      if (f.nota != null) {
        if (!_rec2Notas[aid]) _rec2Notas[aid] = {}
        _rec2Notas[aid][k] = Number(f.nota)
      }
    }
  } catch (e) { console.error('No se pudieron leer las calificaciones por criterio:', e) }
}

async function _loadPardones(mid) { await _loadCalificacionesCE(mid) }

function _reloadEvalSec() {
  const activeNav = document.querySelector('.nav-item.active')
  const sec = activeNav?.dataset?.sec
  if (sec === 'evaluaciones') loadEvaluaciones()
  else loadDashboard()
}

/**
 * Da por alcanzado un criterio en la 2ª convocatoria, o retira esa decisión.
 * Pide un motivo: es una decisión de evaluación y tiene que quedar justificada y
 * fechada, que es lo que se mira en una reclamación.
 */
async function togglePardonCe(mid, alumnoId, raId, ceId) {
  const k = `${raId}|${ceId}`
  const yaEstaba = _pardones[alumnoId]?.has(k)
  let motivo = null
  if (!yaEstaba) {
    motivo = prompt(
      `Vas a dar por alcanzado el criterio ${ceId} de ${raId}.\n\n` +
      '¿Con qué evidencia? (prueba de recuperación, trabajo entregado, observación en el taller…)\n' +
      'Queda registrado con la fecha.', '')
    if (motivo === null) return              // cancelado
    motivo = motivo.trim()
    if (!motivo) { alert('Hace falta indicar la evidencia para dar un criterio por alcanzado.'); return }
  }
  try {
    await window.api.setCalificacionCE({
      alumnoId, raId, ceId, convocatoria: 2,
      nota: _rec2Notas[alumnoId]?.[k] ?? null,
      perdonado: yaEstaba ? 0 : 1,
      motivo: yaEstaba ? null : motivo,
    })
  } catch (e) {
    alert('No se ha podido guardar: ' + (e && e.message ? e.message : e)); return
  }
  if (!_pardones[alumnoId]) _pardones[alumnoId] = new Set()
  if (yaEstaba) _pardones[alumnoId].delete(k); else _pardones[alumnoId].add(k)
  _reloadEvalSec()
}

function setRecSort(mode) {
  _recSort = mode
  loadDashboard()
}

// Colapsar/expandir sin re-render completo
function toggleRecCard(alumnoId) {
  const body  = document.getElementById(`rec-body-${alumnoId}`)
  const chev  = document.getElementById(`rec-chev-${alumnoId}`)
  if (!body) return
  const open = body.style.display !== 'none'
  body.style.display = open ? 'none' : 'block'
  if (chev) chev.textContent = open ? '▶' : '▼'
  if (open) _recOpenSet.delete(alumnoId)
  else      _recOpenSet.add(alumnoId)
}

function setOrd1Sort(mode) {
  _ord1Sort = mode
  loadDashboard()
}

function toggleOrd1Card(alumnoId) {
  const body = document.getElementById(`ord1-body-${alumnoId}`)
  const chev = document.getElementById(`ord1-chev-${alumnoId}`)
  if (!body) return
  const open = body.style.display !== 'none'
  body.style.display = open ? 'none' : 'block'
  if (chev) chev.textContent = open ? '▶' : '▼'
  if (open) _ord1OpenSet.delete(alumnoId)
  else      _ord1OpenSet.add(alumnoId)
}

// Ya viene cargado junto con los criterios alcanzados (una sola consulta).
async function _loadRec2Notas(_mid) { /* _loadCalificacionesCE lo ha hecho */ }

async function saveRec2Nota(mid, alumnoId, raId, ceId, notaStr) {
  clearTimeout(_rec2Timer)
  const k = `${raId}|${ceId}`
  if (!_rec2Notas[alumnoId]) _rec2Notas[alumnoId] = {}
  const nota = parseFloat(notaStr)
  const vacia = notaStr === '' || isNaN(nota)
  const valor = vacia ? null : Math.min(10, Math.max(0, nota))
  if (vacia) delete _rec2Notas[alumnoId][k]
  else _rec2Notas[alumnoId][k] = valor
  try {
    await window.api.setCalificacionCE({
      alumnoId, raId, ceId, convocatoria: 2,
      nota: valor,
      perdonado: _pardones[alumnoId]?.has(k) ? 1 : 0,
    })
  } catch (e) {
    alert('No se ha podido guardar la nota de recuperación: ' + (e && e.message ? e.message : e))
  }
  _rec2Timer = setTimeout(() => _reloadEvalSec(), 50)
}

async function loadDashboard() {
  const mid = document.getElementById('dash-mod-sel').value
  if (!mid) return
  _alumnos = await window.api.getAlumnos(mid)           // poblar global para genBoletin
  const alumnos = _alumnos.filter(a => a.estado === 'Activo')
  const allActividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  const ng = {}
  // H6: nota efectiva = nota_rec (recuperación) si existe, si no la original
  notasArr.forEach(n => { if(!ng[n.alumno_id])ng[n.alumno_id]={}; ng[n.alumno_id][n.actividad_id]=n.nota_rec ?? n.nota })

  // Datos del módulo
  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)
  const actividades = allActividades.filter(a => evals.includes(a.eval))
  const ras     = modData?.ras          || []
  const cesDict = modData?.ces          || {}
  const asigs   = modData?.asignaciones || []

  if (!alumnos.length || !actividades.length) {
    const why = !alumnos.length
      ? 'No hay alumnado activo en este módulo.'
      : 'No hay actividades configuradas todavía.'
    document.getElementById('dash-content').innerHTML = `
      <div class="empty-state">
        <div style="font-weight:700;color:var(--text);margin-bottom:6px">Dashboard sin datos suficientes</div>
        <div style="margin-bottom:10px">${esc(why)} Cuando añadas alumnado y actividades, aquí aparecerán KPIs, 1ª ordinaria y 2ª ordinaria.</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn btn-ghost btn-sm" onclick="goSection('alumnos')">👥 Ir a alumnos</button>
          <button class="btn btn-ghost btn-sm" onclick="goSection('programacion')">📋 Ir a programación</button>
          <button class="btn btn-ghost btn-sm" onclick="goSection('notas')">📝 Ir a notas</button>
        </div>
      </div>`
    return
  }

  // Cargar perdones y notas de recuperación
  await _loadPardones(mid)
  await _loadRec2Notas(mid)

  // Mínimo de examen del módulo: lo aplica el motor, igual que en Evaluaciones
  const cfgDash = await window.api.getAllConfig()
  const minRawD = cfgDash[`minexam_${mid}`]
  const minExam = minRawD != null && String(minRawD).trim() !== '' ? parseFloat(minRawD) : null

  // ── Motor único de calificación (js/core/calificacion.js) ──────
  // Esta pantalla tenía su propio cálculo: la nota de RA salía de la media
  // ponderada de las actividades, ignorando los criterios, y la nota final era la
  // media simple de todas las notas. Daba 7,25 donde Evaluaciones daba 6,25.
  // Fase de formación en empresa por alumno (Orden 201/2024, art. 12)
  const fasesDash = {}
  try {
    const filas = await window.api.getFaseEmpresa(parseInt(mid))
    filas.forEach(f => { fasesDash[Number(f.alumno_id)] = f.estado })
  } catch { /* base antigua sin la tabla */ }

  const ctxCalculo = contextoModulo({
    ras, cesByRa: cesDict, asignaciones: asigs, actividades, minExam,
    tieneFaseEmpresa: moduloConFaseEmpresa(modData?.modulo),
  })
  const estadoDe = alumnoId =>
    estadoModulo(ctxCalculo, ng[alumnoId], { faseEmpresa: fasesDash[alumnoId] })

  function computeRaNotas(alumnoId) {
    const st = estadoDe(alumnoId)
    const raNotas = {}
    ras.forEach(ra => { raNotas[ra.id] = st.porRA[ra.id] ? st.porRA[ra.id].nota : null })
    return raNotas
  }

  // ── Helper: CEs suspendidos de un alumno (de RAs < 5) ──────────
  function computeFailingCes(alumnoId) {
    const raNotas = computeRaNotas(alumnoId)
    const seen = new Set()
    const result = []
    ras.forEach(ra => {
      const nota = raNotas[ra.id]
      if (nota == null || nota >= 5) return
      // Usar TODOS los CEs del RA (no solo los ligados a UTs en asigs)
      const ceLst = cesDict[ra.id] || []
      if (ceLst.length) {
        ceLst.forEach(ce => {
          if (seen.has(ce.id)) return
          seen.add(ce.id)
          result.push({
            ceId: ce.id,
            ceText: ce.texto || '',
            raId: ra.id,
            raNota: nota,
            pardoned: !!_pardones[alumnoId]?.has(`${ra.id}|${ce.id}`),   // H2
          })
        })
      } else {
        // Fallback: CEs desde asignaciones si cesDict no tiene datos para este RA
        asigs.filter(a => a.ra === ra.id).forEach(asig => {
          ;(asig.ces || []).forEach(ceId => {
            if (seen.has(ceId)) return
            seen.add(ceId)
            result.push({
              ceId,
              ceText: '',
              raId: ra.id,
              raNota: nota,
              pardoned: !!_pardones[alumnoId]?.has(`${ra.id}|${ceId}`),   // H2
            })
          })
        })
      }
    })
    return result
  }

  // ── Helper: nota final recalculada con calificaciones de 2ª Ordinaria ──
  function computeRec2FinalGrade(alumnoId) {
    const raNotasOrig = computeRaNotas(alumnoId)
    const recRaNotas  = {}
    ras.forEach(ra => {
      const origNota = raNotasOrig[ra.id]
      if (origNota === null || origNota >= 5) { recRaNotas[ra.id] = origNota; return }
      // RA suspenso: recalcular con notas de recuperación por CE
      const ceIds = []
      const seen  = new Set()
      const ceLstRec = cesDict[ra.id] || []
      if (ceLstRec.length) {
        ceLstRec.forEach(ce => { if (!seen.has(ce.id)) { seen.add(ce.id); ceIds.push(ce.id) } })
      } else {
        asigs.filter(a => a.ra === ra.id).forEach(asig =>
          (asig.ces || []).forEach(ceId => { if (!seen.has(ceId)) { seen.add(ceId); ceIds.push(ceId) } })
        )
      }
      if (!ceIds.length) { recRaNotas[ra.id] = origNota; return }
      const ceGrades = []
      ceIds.forEach(ceId => {
        const k = ceKey(ra.id, ceId)   // H2: clave compuesta
        const recNota = _rec2Notas[alumnoId]?.[k]
        if (recNota != null) { ceGrades.push(recNota); return }
        if (_pardones[alumnoId]?.has(k)) { ceGrades.push(5); return }
        // Nota original del CE: media de las actividades que cubren ESE criterio
        // de ESE RA (el id suelto se repite entre RAs)
        const ceActs = actividades.filter(a => actCubreCe(a, ra.id, ceId))
        const ceActGrades = ceActs.map(a => ng[alumnoId]?.[a.id]).filter(n => n != null)
        if (ceActGrades.length) ceGrades.push(ceActGrades.reduce((s, n) => s + n, 0) / ceActGrades.length)
      })
      recRaNotas[ra.id] = ceGrades.length ? ceGrades.reduce((s, g) => s + g, 0) / ceGrades.length : origNota
    })
    const ns = Object.values(recRaNotas).filter(n => n !== null)
    return ns.length ? ns.reduce((s, n) => s + n, 0) / ns.length : null
  }

  // Calcular media global por alumno
  // H1 — regla de oro: superar el módulo exige TODOS los RA calificados ≥5,
  // no basta con que la media sea ≥5.
  const resumen = alumnos.map(al => {
    const st = estadoDe(al.id)
    return { ...al, media: st.media, rasPend: st.pendientes, superado: st.superado,
             acta: st.acta, resultado: st.resultado }
  })

  const conNota = resumen.filter(a => a.media !== null)
  const aptos   = conNota.filter(a => a.superado).length
  const noAptos = conNota.filter(a => !a.superado).length
  const enRiesgo= conNota.filter(a => a.media >= 4 && a.media < 5).length
  const mediaGlobal = conNota.length ? (conNota.reduce((s,a)=>s+(a.media||0),0)/conNota.length).toFixed(1) : '—'

  const kpis = `<div class="kpi-grid">
    <div class="kpi"><div class="kpi-val">${alumnos.length}</div><div class="kpi-label">Activos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--green)">${aptos}</div><div class="kpi-label">Aptos (≥5)</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--red)">${noAptos}</div><div class="kpi-label">No Aptos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--amber)">${enRiesgo}</div><div class="kpi-label">En Riesgo</div></div>
    <div class="kpi"><div class="kpi-val">${mediaGlobal}</div><div class="kpi-label">Media Grupo</div></div>
  </div>`

  // ── Ordenar resumen para 1ª Ordinaria ─────────────────────────
  const resumenSorted = resumen.slice()
  if (_ord1Sort === 'noAptos') {
    resumenSorted.sort((a, b) => {
      const va = a.media === null ? 1 : !a.superado ? 0 : 2
      const vb = b.media === null ? 1 : !b.superado ? 0 : 2
      return va - vb || (a.apellidos||'').localeCompare(b.apellidos||'', 'es')
    })
  } else if (_ord1Sort === 'aptos') {
    resumenSorted.sort((a, b) => {
      const va = a.media === null ? 1 : a.superado ? 0 : 2
      const vb = b.media === null ? 1 : b.superado ? 0 : 2
      return va - vb || (a.apellidos||'').localeCompare(b.apellidos||'', 'es')
    })
  } else {
    resumenSorted.sort((a, b) => (a.apellidos||'').localeCompare(b.apellidos||'', 'es'))
  }

  const filas = resumenSorted.map(a => {
    const m = a.media
    const cls = m===null?'':a.superado?'sem-green':m>=4?'sem-amber':'sem-red'
    const nota = m===null ? '—' : m.toFixed(1)
    const notaCls = m===null?'':a.superado?'nota-apto':m>=4?'nota-riesgo':'nota-noapto'
    const apto = m===null ? '—' : etiquetaResultado(a.resultado)
    const aptoCls = m===null ? 'color:var(--text3)'
      : a.resultado === 'SUPERADO' ? 'color:var(--green)'
      : a.resultado === 'SUPERADO_PARCIAL' ? 'color:var(--accent2)' : 'color:var(--red)'
    const motivo = m!==null && !a.superado && m>=5 && a.rasPend.length
      ? ` title="Media ≥5 pero RA pendientes: ${esc(a.rasPend.join(', '))} (la media no compensa un RA suspenso)"` : ''
    return `<tr${motivo}>
      <td><span class="semaforo ${cls}"></span>${esc(a.apellidos||'')}${a.apellidos&&a.nombre?', ':''}${esc(a.nombre||'')}${m!==null && !a.superado && m>=5 && a.rasPend.length ? ' <span style="color:var(--red);font-size:10px;font-weight:700">⚠ RA pend.</span>' : ''}</td>
      <td style="text-align:center;font-weight:700;font-size:15px" class="${notaCls}">${nota}</td>
      <td style="text-align:center;font-weight:700;font-size:11px;${aptoCls}">${apto}</td>
      <td style="text-align:center">
        <button class="btn btn-ghost btn-sm" onclick="genBoletin(${a.id})">📄 Boletín PDF</button>
      </td>
    </tr>`
  }).join('')

  // ── Sort bar para 1ª Ordinaria ─────────────────────────────────
  const ord1SortBtn = (mode, label) => {
    const active = _ord1Sort === mode
    return `<button onclick="setOrd1Sort('${mode}')"
      style="font-size:11px;padding:3px 10px;border-radius:7px;cursor:pointer;white-space:nowrap;
             border:1px solid ${active?'var(--accent)':'var(--border2)'};
             background:${active?'rgba(74,144,217,.15)':'var(--bg3)'};
             color:${active?'var(--accent)':'var(--text2)'};font-weight:${active?'700':'400'}">
      ${label}</button>`
  }
  const ord1SortBar = `<div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;flex-wrap:wrap">
    <span style="font-size:11px;color:var(--text3)">Ordenar:</span>
    ${ord1SortBtn('nombre','A–Z')}
    ${ord1SortBtn('aptos','✓ Aptos primero')}
    ${ord1SortBtn('noAptos','✗ No Aptos primero')}
  </div>`

  // ── Tarjetas colapsables por alumno (1ª Ordinaria) ─────────────
  const ord1AlumCards = resumenSorted.map(al => {
    const raNotas = computeRaNotas(al.id)
    const m = al.media
    const nota = m === null ? '—' : m.toFixed(1)
    const notaCls = m === null ? '' : al.superado ? 'nota-apto' : m >= 4 ? 'nota-riesgo' : 'nota-noapto'
    const isApto = al.superado   // H1: regla de oro
    const isOpen = _ord1OpenSet.has(al.id)
    const nombreAl = `${al.apellidos||''}${al.apellidos&&al.nombre?', ':''}${al.nombre||''}`

    const aptoBadge = m === null
      ? `<span style="background:var(--bg3);color:var(--text3);padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700">—</span>`
      : isApto
      ? `<span style="background:rgba(16,185,129,.15);color:var(--green);padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700">✓ APTO/A</span>`
      : `<span style="background:rgba(239,68,68,.1);color:var(--red);padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700">✗ NO APTO/A</span>`

    // Bloques de RA con CEs
    const raBlocks = ras.map(ra => {
      const raNota = raNotas[ra.id]
      const ceIds = []
      const seen = new Set()
      asigs.filter(a => a.ra === ra.id).forEach(asig => {
        ;(asig.ces || []).forEach(ceId => { if (!seen.has(ceId)) { seen.add(ceId); ceIds.push(ceId) } })
      })
      // Solo mostrar RAs con actividades
      const hasActs = actividades.some(a => {
        if (a.ra_id && String(a.ra_id) === String(ra.id)) return true
        if (a.ut_id) {
          return String(a.ut_id).split(',').filter(Boolean)
            .some(utId => asigs.find(as => as.ut === utId && as.ra === ra.id))
        }
        return false
      })
      if (!hasActs && raNota === null) return ''

      const raCls = raNota === null ? '' : raNota >= 5 ? 'nota-apto' : raNota >= 4 ? 'nota-riesgo' : 'nota-noapto'
      const raNotaTxt = raNota === null ? '—' : raNota.toFixed(1)
      const ceLst = cesDict[ra.id] || []
      const borderClr = raNota === null ? 'var(--border2)' : raNota >= 5 ? 'var(--green)' : 'var(--red)'

      const ceItems = ceIds.map(ceId => {
        const ce = ceLst.find(c => c.id === ceId)
        const icon = raNota === null ? '○' : raNota >= 5 ? '✅' : '❌'
        const ceText = ce ? (ce.texto.length > 110 ? ce.texto.slice(0,109)+'…' : ce.texto) : ''
        return `<div style="display:flex;align-items:baseline;gap:6px;padding:2px 0;font-size:11px">
          <span style="flex-shrink:0;width:16px">${icon}</span>
          <span style="font-weight:700;color:var(--accent);min-width:36px;flex-shrink:0">${esc(ceId)}</span>
          <span style="color:var(--text2);flex:1;font-size:10.5px">${esc(ceText)}</span>
        </div>`
      }).join('')

      return `<div style="margin-bottom:6px;padding:8px 10px;background:var(--bg3);border-radius:6px;border-left:3px solid ${borderClr}">
        <div style="display:flex;align-items:center;gap:8px;${ceIds.length?'margin-bottom:6px':''}">
          <span style="font-weight:700;font-size:11px;color:var(--accent)">${esc(ra.id)}</span>
          <span style="font-size:10px;color:var(--text2);flex:1">${esc(ra.nombre||'')}</span>
          <span class="${raCls}" style="font-weight:700;font-size:13px">${raNotaTxt}</span>
        </div>
        ${ceItems}
      </div>`
    }).filter(Boolean).join('')

    return `<div style="border:1px solid var(--border2);border-radius:10px;margin-bottom:6px;overflow:hidden">
      <div onclick="toggleOrd1Card(${al.id})"
           style="display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;
                  background:${isOpen?'var(--bg3)':'var(--bg)'};user-select:none;flex-wrap:wrap">
        <span id="ord1-chev-${al.id}" style="font-size:10px;color:var(--text3);width:12px;flex-shrink:0">${isOpen?'▼':'▶'}</span>
        <span style="font-size:13px;font-weight:700;flex:1">${esc(nombreAl)}</span>
        <span class="${notaCls}" style="font-weight:700;font-size:14px;margin-right:4px">${nota}</span>
        ${aptoBadge}
        <button onclick="event.stopPropagation();genBoletin(${al.id})"
          class="btn btn-ghost btn-sm" style="margin-left:4px">📄 Boletín</button>
      </div>
      <div id="ord1-body-${al.id}" style="display:${isOpen?'block':'none'};padding:10px 14px 12px">
        ${raBlocks || '<span style="font-size:11px;color:var(--text3)">Sin actividades calificadas.</span>'}
      </div>
    </div>`
  }).join('')

  const ord1Html = `<div class="card" style="margin-top:16px">
    <div class="card-title">1ª Ordinaria</div>
    <div class="tbl-wrap"><table>
      <thead><tr>
        <th>Alumno/a</th>
        <th style="text-align:center;width:80px">Nota final</th>
        <th style="text-align:center;width:110px">Resultado</th>
        <th style="width:130px"></th>
      </tr></thead>
      <tbody>${filas}</tbody>
    </table></div>
    <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--border)">
      <div style="font-size:12px;font-weight:600;color:var(--text2);margin-bottom:10px">
        Detalle por alumno/a <span style="font-weight:400">· haz clic para expandir</span>
      </div>
      ${ord1SortBar}
      ${ord1AlumCards}
    </div>
  </div>`

  // ── 2ª Ordinaria: alumnos con CEs suspendidos ──────────────────
  const conRecuperacion = alumnos
    .map(al => {
      const failingCes = computeFailingCes(al.id)
      if (!failingCes.length) return null
      // CE "pendiente" = no aprobado manualmente Y sin nota rec2 ≥ 5
      const pendientes = failingCes.filter(c => {
        const rec2Nota = _rec2Notas[al.id]?.[`${c.raId}|${c.ceId}`]   // H2
        return !c.pardoned && (rec2Nota == null || rec2Nota < 5)
      })
      const rec2FinalGrade = computeRec2FinalGrade(al.id)
      return { ...al, failingCes, pendientes, rec2FinalGrade }
    })
    .filter(Boolean)

  // Ordenar
  if (_recSort === 'nombre') {
    conRecuperacion.sort((a, b) => (a.apellidos||'').localeCompare(b.apellidos||'', 'es'))
  } else if (_recSort === 'aprobados') {
    conRecuperacion.sort((a, b) => a.pendientes.length - b.pendientes.length)
  } else { // 'pendientes' — más pendientes primero
    conRecuperacion.sort((a, b) => b.pendientes.length - a.pendientes.length
      || (a.apellidos||'').localeCompare(b.apellidos||'', 'es'))
  }

  let rec2Html = ''
  if (ras.length) {
    if (!conRecuperacion.length) {
      rec2Html = `<div class="card" style="margin-top:16px">
        <div class="card-title">2ª Ordinaria</div>
        <p style="font-size:13px;color:var(--text2);padding:8px 0">
          ✅ Ningún alumno/a tiene CEs suspendidos — no hay recuperación pendiente.
        </p>
      </div>`
    } else {
      const sortBtn = (mode, label) => {
        const active = _recSort === mode
        return `<button onclick="setRecSort('${mode}')"
          style="font-size:11px;padding:3px 10px;border-radius:7px;cursor:pointer;white-space:nowrap;
                 border:1px solid ${active?'var(--accent)':'var(--border2)'};
                 background:${active?'rgba(74,144,217,.15)':'var(--bg3)'};
                 color:${active?'var(--accent)':'var(--text2)'};font-weight:${active?'700':'400'}">
          ${label}</button>`
      }
      const sortBar = `<div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;flex-wrap:wrap">
        <span style="font-size:11px;color:var(--text3)">Ordenar:</span>
        ${sortBtn('pendientes','⬆ Más pendientes')}
        ${sortBtn('nombre','A–Z')}
        ${sortBtn('aprobados','✓ Aprobados primero')}
      </div>`

      const alumCards = conRecuperacion.map(al => {
        const todoPerdonado = al.pendientes.length === 0
        const nombreAl = `${al.apellidos || ''}${al.apellidos && al.nombre ? ', ' : ''}${al.nombre || ''}`
        const isOpen = _recOpenSet.has(al.id)

        const rec2Grade    = al.rec2FinalGrade
        const rec2GradeTxt = rec2Grade !== null ? rec2Grade.toFixed(1) : null
        const rec2IsApto   = rec2Grade !== null && rec2Grade >= 5

        const estadoBadge = todoPerdonado
          ? `<span style="background:rgba(16,185,129,.15);color:var(--green);padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700">✓ Aprobado/a</span>`
          : `<span style="background:rgba(239,68,68,.1);color:var(--red);padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700">${al.pendientes.length} CE${al.pendientes.length>1?'s':''} pendiente${al.pendientes.length>1?'s':''}</span>`

        const rec2Badge = rec2GradeTxt !== null
          ? `<span style="background:${rec2IsApto?'rgba(16,185,129,.15)':'rgba(239,68,68,.1)'};color:${rec2IsApto?'var(--green)':'var(--red)'};padding:2px 8px;border-radius:10px;font-size:12px;font-weight:800;margin-left:2px">${rec2GradeTxt} — ${rec2IsApto?'APTO/A':'NO APTO/A'}</span>`
          : ''

        const ceRows = al.failingCes.map(c => {
          const raIdSafe   = c.raId.replace(/'/g, "\\'")
          const ceIdSafe   = c.ceId.replace(/'/g, "\\'")
          const rec2Nota   = _rec2Notas[al.id]?.[`${c.raId}|${c.ceId}`]   // H2
          const passedRec2 = rec2Nota != null && rec2Nota >= 5
          const icon = passedRec2 || c.pardoned ? '✅' : rec2Nota != null ? '❌' : '⬜'

          const pardonBtn = c.pardoned
            ? `<button onclick="event.stopPropagation();togglePardonCe(${mid},${al.id},'${raIdSafe}','${ceIdSafe}')"
                style="font-size:10px;padding:1px 7px;border-radius:5px;border:1px solid var(--border2);background:rgba(16,185,129,.1);color:var(--green);cursor:pointer;white-space:nowrap">
                ↩ Quitar aprobado</button>`
            : `<button onclick="event.stopPropagation();togglePardonCe(${mid},${al.id},'${raIdSafe}','${ceIdSafe}')"
                style="font-size:10px;padding:1px 7px;border-radius:5px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);cursor:pointer;white-space:nowrap">
                Aprobado</button>`

          const notaInput = `<input type="number" min="0" max="10" step="0.1"
            value="${rec2Nota != null ? rec2Nota : ''}"
            placeholder="Nota 2ª"
            onchange="event.stopPropagation();saveRec2Nota(${mid},${al.id},'${raIdSafe}','${ceIdSafe}',this.value)"
            onclick="event.stopPropagation()"
            style="width:68px;font-size:10px;padding:2px 4px;border-radius:4px;
                   border:1px solid ${passedRec2?'var(--green)':rec2Nota!=null?'var(--red)':'var(--border2)'};
                   background:${passedRec2?'rgba(16,185,129,.08)':rec2Nota!=null?'rgba(239,68,68,.06)':'var(--bg)'};
                   color:var(--text);text-align:center"/>`

          return `<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-top:1px solid var(--border);font-size:11px;flex-wrap:wrap">
            <span style="flex-shrink:0;width:16px">${icon}</span>
            <span style="font-weight:700;color:var(--accent);min-width:36px;flex-shrink:0">${esc(c.ceId)}</span>
            <span style="color:var(--text2);flex:1;font-size:10.5px;min-width:60px">${esc(c.raId)} · ${esc(c.ceText.length>90?c.ceText.slice(0,89)+'…':c.ceText)}</span>
            ${notaInput}
            ${pardonBtn}
          </div>`
        }).join('')

        return `<div style="border:1px solid var(--border2);border-radius:10px;margin-bottom:6px;overflow:hidden;${todoPerdonado?'opacity:.7':''}">
          <div onclick="toggleRecCard(${al.id})"
               style="display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;
                      background:${isOpen?'var(--bg3)':'var(--bg)'};user-select:none;flex-wrap:wrap">
            <span id="rec-chev-${al.id}" style="font-size:10px;color:var(--text3);width:12px;flex-shrink:0">${isOpen?'▼':'▶'}</span>
            <span style="font-size:13px;font-weight:700;flex:1">${esc(nombreAl)}</span>
            ${estadoBadge}
            ${rec2Badge}
          </div>
          <div id="rec-body-${al.id}" style="display:${isOpen?'block':'none'};padding:10px 14px 12px">
            ${ceRows}
          </div>
        </div>`
      }).join('')

      rec2Html = `<div class="card" style="margin-top:16px">
        <div class="card-title" style="display:flex;align-items:center;gap:10px">
          2ª Ordinaria
          <span style="font-size:11px;font-weight:400;color:var(--text2)">${conRecuperacion.length} alumno${conRecuperacion.length>1?'s':''} · haz clic para expandir</span>
        </div>
        <p style="font-size:11px;color:var(--text3);margin-bottom:10px">
          CEs de RAs suspendidos (nota &lt; 5). Introduce la <b>nota del examen de recuperación</b> para recalcular la nota final. <b>Aprobado</b> excusa el CE sin nota.
        </p>
        ${sortBar}
        ${alumCards}
      </div>`
    }
  }

  document.getElementById('dash-content').innerHTML = kpis + ord1Html + rec2Html
}

async function genBoletin(alumnoId) {
  // El botón Boletín existe en Dashboard Y en Evaluaciones: usar el selector activo
  const mid = document.getElementById('dash-mod-sel')?.value ||
              document.getElementById('eval-mod-sel')?.value
  if (!mid) { alert('Selecciona un módulo primero.'); return }

  // Cargar alumnos frescos de la BD (la caché _alumnos puede ser de otro módulo)
  const alumnosMod = await window.api.getAlumnos(parseInt(mid))
  const alumno = alumnosMod.find(x => x.id === alumnoId)
  if (!alumno) { alert('Alumno/a no encontrado en este módulo.'); return }

  // ── Cargar datos ──────────────────────────────────────────────────────
  const actividades = await window.api.getActividades(mid)
  const notasArr    = await window.api.getNotasGrid(mid)

  // Mapa de notas de este alumno
  const miNotas = {}
  // H6: nota efectiva = nota_rec si existe
  notasArr.filter(n => n.alumno_id === alumnoId)
          .forEach(n => { miNotas[n.actividad_id] = n.nota_rec ?? n.nota })

  // Metadatos del módulo
  const modData   = _getModData(mid) || {}
  const ras       = modData.ras          || []
  const uts       = modData.uts          || []
  const cesDict   = modData.ces          || {}   // { "RA1": [{id,texto},...], ... }
  const asigs     = modData.asignaciones || []   // [{ut, ra, ces:[...]}, ...]
  const evalCount = modData.modulo?.eval_count || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)
  const mod       = _modulos.find(m => m.id == mid) || {}

  // Aplicar overrides de ponderación de RA editados por el profesor
  try {
    const rows = await window.api.getRaPonderaciones(parseInt(mid))
    rows.forEach(r => {
      const ra = ras.find(x => x.id === r.ra_id)
      if (ra) ra.pond = r.pond
    })
  } catch { /* sin overrides */ }

  // ── Media ponderada por evaluación ────────────────────────────────────
  const evalMedias = evals.map(ev => {
    const actsEv = actividades.filter(a => a.eval === ev)
    let sumP = 0, sumPN = 0
    actsEv.forEach(a => {
      const nota = miNotas[a.id]
      if (nota != null) { const p = a.peso || 1; sumPN += nota * p; sumP += p }
    })
    const media = sumP > 0 ? sumPN / sumP : null
    return {
      ev,
      media,
      numActs:  actsEv.length,
      numNotas: actsEv.filter(a => miNotas[a.id] != null).length,
    }
  })

  const evalConMedia = evalMedias.filter(e => e.media != null)
  const mediaGlobal  = evalConMedia.length
    ? evalConMedia.reduce((s, e) => s + e.media, 0) / evalConMedia.length
    : null

  // ── Nota por UT (promedio ponderado de sus actividades) ───────────────
  // Los exámenes pueden tener ut_id como lista "UT1,UT2" → contribuyen a cada UT
  const actsByUT = {}
  actividades.forEach(a => {
    if (!a.ut_id) return
    const utIds = String(a.ut_id).split(',').filter(Boolean)
    utIds.forEach(utId => {
      if (!actsByUT[utId]) actsByUT[utId] = []
      actsByUT[utId].push(a)
    })
  })
  const utNotas = {}
  Object.entries(actsByUT).forEach(([utId, acts]) => {
    let sumP = 0, sumPN = 0
    acts.forEach(a => {
      const nota = miNotas[a.id]
      if (nota != null) { const p = a.peso || 1; sumPN += nota * p; sumP += p }
    })
    utNotas[utId] = sumP > 0 ? sumPN / sumP : null
  })

  // ── Contribuciones por RA (para cálculo raNotas) ──────────────────────
  // Cada actividad contribuye a su RA vía ra_id (directo) o via ut_id→asigs→ra
  // Si cubre varias UTs con distintos RAs, el peso se reparte proporcionalmente
  const raContribs = {}  // raId → [{nota, peso}]
  ras.forEach(ra => { raContribs[ra.id] = [] })
  actividades.forEach(a => {
    const nota = miNotas[a.id]
    if (nota == null) return
    const p = a.peso || 1
    if (a.ra_id && raContribs[a.ra_id]) {
      // Asignación directa de RA
      raContribs[a.ra_id].push({ nota, peso: p })
    } else if (a.ut_id) {
      // Derivar RAs desde las UTs (examen multi-UT o práctica sin ra_id explícito).
      // Una UT puede trabajar varios RA: entran todos.
      const raIds = rasDeActividad(a, asigs)
      if (raIds.length) {
        const pesoPerRa = p / raIds.length  // peso repartido entre RAs implicados
        raIds.forEach(raId => {
          if (raContribs[raId]) raContribs[raId].push({ nota, peso: pesoPerRa })
        })
      }
    }
  })

  // ── Asignaciones agrupadas por UT ─────────────────────────────────────
  const asigsByUT = {}
  asigs.forEach(a => { if (!asigsByUT[a.ut]) asigsByUT[a.ut] = []; asigsByUT[a.ut].push(a) })

  // ── Helpers ───────────────────────────────────────────────────────────
  const fmt   = n  => n != null ? n.toFixed(2) : '—'
  const e     = s  => (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')
  const trunc = (s, n) => s && s.length > n ? s.substring(0, n - 1) + '…' : (s || '')
  const aptoLabel = n => n == null ? '–' : n >= 5 ? 'APTO/A' : 'NO APTO/A'
  const aptoCls   = n => n == null ? 'sin'  : n >= 5 ? 'ok'  : 'ko'

  // ── CSS ───────────────────────────────────────────────────────────────
  const css = `
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;color:#1a1a2e;padding:28px 36px;line-height:1.45;background:#fff}
    .hdr{border-bottom:3px solid #1a3a6e;padding-bottom:12px;margin-bottom:18px}
    .hdr h1{font-size:17px;font-weight:700;color:#1a3a6e;letter-spacing:-.3px}
    .hdr .mod-name{font-size:13px;font-weight:600;color:#223;margin:3px 0}
    .hdr .meta{font-size:9.5px;color:#666}
    .hdr .al{font-size:14px;font-weight:700;margin:8px 0 2px}
    .sec{font-size:11px;font-weight:700;color:#1a3a6e;text-transform:uppercase;letter-spacing:.5px;margin:18px 0 8px;border-left:3px solid #4a7fd4;padding-left:8px}
    table{width:100%;border-collapse:collapse;margin-bottom:6px}
    th{background:#1a3a6e;color:#fff;padding:5px 8px;text-align:left;font-size:9.5px;font-weight:600;text-transform:uppercase;letter-spacing:.3px}
    td{padding:5px 8px;border-bottom:1px solid #e8edf4;vertical-align:middle}
    tr:last-child td{border-bottom:none}
    .nc{text-align:center;font-weight:700;font-size:12px}
    .ok{color:#1a7a3a}.ko{color:#b52}.sin{color:#888}
    .b-ok{display:inline-block;padding:1px 7px;border-radius:9px;background:#d4edda;color:#155724;font-size:9px;font-weight:700}
    .b-ko{display:inline-block;padding:1px 7px;border-radius:9px;background:#f8d7da;color:#721c24;font-size:9px;font-weight:700}
    .b-sin{display:inline-block;padding:1px 7px;border-radius:9px;background:#e9ecef;color:#6c757d;font-size:9px;font-weight:700}
    .ev-blk{margin-bottom:16px;border:1px solid #c5d0e8;border-radius:5px;overflow:hidden}
    .ev-blk .ut{border:none;border-radius:0;border-bottom:1px solid #d0d8e8;margin-bottom:0}
    .ev-blk .ut:last-child{border-bottom:none}
    .ev-hdr{background:#1a3a6e;color:#fff;padding:7px 12px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
    .ev-num{font-weight:700;font-size:12px;white-space:nowrap;margin-right:4px}
    .ev-empty{padding:8px 10px;font-size:9.5px;color:#888}
    .ut{margin-bottom:12px;border:1px solid #d0d8e8;border-radius:4px;overflow:hidden}
    .uth{background:#eef2fb;padding:5px 10px;display:flex;align-items:center;gap:8px;flex-wrap:nowrap}
    .uth .uid{font-weight:700;color:#1a3a6e;font-size:11px;white-space:nowrap}
    .uth .unm{flex:1;color:#333;font-size:10px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .uth .hh{font-size:9px;color:#888;white-space:nowrap}
    .utn{padding:4px 10px;font-size:10px;border-bottom:1px solid #d8dfe8;background:#fff}
    .rar{padding:5px 10px;background:#fff}
    .rar+.rar{border-top:1px solid #f0f0f0}
    .ral{font-weight:600;font-size:10px;color:#2d5090}
    .cel{margin-top:3px;font-size:9.5px;line-height:1.7;color:#444}
    .ci{display:inline-flex;align-items:baseline;gap:3px;margin-right:8px;margin-bottom:2px}
    .ci .cid{font-weight:700;font-size:9px}
    .ci .ctx{font-size:9px;color:#555}
    .ftr{margin-top:20px;padding-top:8px;border-top:1px solid #dee;font-size:8.5px;color:#999;text-align:right}
    .global{background:#f0f4fb!important;font-size:12px}
    .conv{margin-bottom:14px;border:2px solid #1a3a6e;border-radius:5px;overflow:hidden}
    .conv-hdr{padding:8px 12px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
    .conv-hdr.ord1{background:#1a3a6e;color:#fff}
    .conv-hdr.ord2{background:#b52;color:#fff}
    .conv-num{font-weight:700;font-size:13px;white-space:nowrap}
    .conv-nota{font-size:22px;font-weight:900;margin-left:auto;white-space:nowrap}
    .conv-nota.ok{color:#a8f0b8}
    .conv-nota.ko{color:#ffd0c0}
    .conv-body{padding:10px 12px;background:#fff}
    .conv-ra-ko{margin-bottom:10px;padding:8px 10px;border-left:3px solid #b52;background:#fff5f5;border-radius:0 3px 3px 0}
    .conv-ra-title{font-weight:700;font-size:10.5px;color:#8b1a1a;margin-bottom:4px}
    .conv-ut-list{font-size:9.5px;color:#555;margin-bottom:4px}
    .conv-ce-list{font-size:9px;color:#666;line-height:1.8}
  `

  // ── Tabla medias por evaluación ───────────────────────────────────────
  const evalRows = evalMedias.map(({ ev, media, numActs, numNotas }) => {
    const cl = aptoCls(media)
    return `<tr>
      <td><b>${evalLabel(ev)}</b></td>
      <td class="nc ${cl}">${fmt(media)}</td>
      <td><span class="${cl==='ok'?'b-ok':cl==='ko'?'b-ko':'b-sin'}">${aptoLabel(media)}</span></td>
      <td class="sin" style="font-size:9px">${numNotas}/${numActs} act. calificadas</td>
    </tr>`
  }).join('')

  const cl = aptoCls(mediaGlobal)
  const globalRow = `<tr class="global">
    <td><b>Media global</b></td>
    <td class="nc ${cl}" style="font-size:14px"><b>${fmt(mediaGlobal)}</b></td>
    <td><span class="${cl==='ok'?'b-ok':cl==='ko'?'b-ko':'b-sin'}" style="font-size:10px">${aptoLabel(mediaGlobal)}</span></td>
    <td></td>
  </tr>`

  // ── Helper: bloque de una UT con sus RAs y CEs ───────────────────────
  function utBlock(ut) {
    const nota   = utNotas[ut.id]
    const isApto = nota != null && nota >= 5
    const uCl    = aptoCls(nota)

    const raBlocks = (asigsByUT[ut.id] || []).map(asig => {
      const ra    = ras.find(r => r.id === asig.ra)
      if (!ra) return ''
      const ceLst = cesDict[asig.ra] || []
      const ceIds = asig.ces || []

      const ceItems = ceIds.map(ceId => {
        const ce   = ceLst.find(c => c.id === ceId)
        const icon = nota == null ? '○' : isApto ? '✅' : '❌'
        const ico  = nota == null ? '' : isApto ? 'ok' : 'ko'
        const txt  = ce ? trunc(ce.texto, 90) : ''
        return `<span class="ci">
          <span class="${ico}">${icon}</span>
          <span class="cid">${e(ceId)}</span>
          ${txt ? `<span class="ctx">— ${e(txt)}</span>` : ''}
        </span>`
      }).join('')

      return `<div class="rar">
        <div class="ral">${e(ra.id)} (${ra.pond}%) · ${e(trunc(ra.nombre, 100))}</div>
        ${ceIds.length ? `<div class="cel">${ceItems}</div>` : ''}
      </div>`
    }).join('')

    const notaHtml = nota != null
      ? `Nota práctica: <b class="${uCl}">${fmt(nota)}</b> &nbsp; <span class="${uCl==='ok'?'b-ok':uCl==='ko'?'b-ko':'b-sin'}">${aptoLabel(nota)}</span>`
      : `<span class="sin">Sin calificar</span>`

    return `<div class="ut">
      <div class="uth">
        <span class="uid">${e(ut.id)}</span>
        <span class="unm">${e(ut.nombre || '')}</span>
        ${ut.horas ? `<span class="hh">${ut.horas}h</span>` : ''}
      </div>
      <div class="utn">${notaHtml}</div>
      ${raBlocks}
    </div>`
  }

  // ── Bloques por Evaluación (UTs + RAs + CEs agrupados) ───────────────
  const evalBlocks = evals.map(ev => {
    const evData  = evalMedias.find(x => x.ev === ev) || {}
    const { media, numActs, numNotas } = evData
    const cl      = aptoCls(media)
    const utsEv   = uts.filter(ut => (ut.eval || 1) === ev)

    const evMediaHtml = media != null
      ? `<span class="${cl==='ok'?'b-ok':cl==='ko'?'b-ko':'b-sin'}" style="font-size:10px">${fmt(media)} — ${aptoLabel(media)}</span>` +
        `<span style="font-size:9px;color:#acd;margin-left:6px">(${numNotas}/${numActs} act.)</span>`
      : `<span class="b-sin" style="font-size:10px">Sin calificar</span>`

    const utsHtml = utsEv.length
      ? utsEv.map(ut => utBlock(ut)).join('')
      : `<p class="ev-empty">Sin UTs asignadas a esta evaluación.</p>`

    return `<div class="ev-blk">
      <div class="ev-hdr">
        <span class="ev-num">${evalLabel(ev)}</span>
        ${evMediaHtml}
      </div>
      ${utsHtml}
    </div>`
  }).join('')

  // ── Nota por RA y nota final: motor único (js/core/calificacion.js) ──
  // El boletín es el documento que se lleva a casa: tiene que decir exactamente
  // lo mismo que el acta. Antes calculaba la nota como media de las medias de
  // cada evaluación y salía 6,75 donde Evaluaciones decía 6,25.
  const cfgBol   = await window.api.getAllConfig()
  const minRawB  = cfgBol[`minexam_${mid}`]
  const minExamB = minRawB != null && String(minRawB).trim() !== '' ? parseFloat(minRawB) : null
  let faseAlumnoBol = null
  try {
    const filas = await window.api.getFaseEmpresa(parseInt(mid))
    faseAlumnoBol = filas.find(f => Number(f.alumno_id) === alumnoId)?.estado || null
  } catch { /* base antigua sin la tabla */ }
  const ctxBol   = contextoModulo({
    ras, cesByRa: cesDict, asignaciones: asigs, actividades, minExam: minExamB,
    tieneFaseEmpresa: moduloConFaseEmpresa(modData?.modulo),
  })
  const stBol = estadoModulo(ctxBol, miNotas, { faseEmpresa: faseAlumnoBol })

  // 2ª convocatoria: el boletín tiene que reflejarla. Antes se quedaba en la 1ª y
  // a quien había superado el módulo en la segunda le seguía diciendo que estaba
  // suspenso, porque estas calificaciones vivían solo en la pantalla de la 2ª.
  const { PRAC: pB, EXAM: eB } = pesosPorTipo(actividades)
  const notaCEOrd2 = (raId, ceId) => {
    const k = `${raId}|${ceId}`
    if (_pardones[alumnoId]?.has(k)) return 5
    const rec = _rec2Notas[alumnoId]?.[k]
    if (rec != null) return rec
    return notaCE(raId, ceId, actividades, miNotas, pB, eB)
  }
  const hayOrd2 = Object.keys(_rec2Notas[alumnoId] || {}).length > 0 ||
                  (_pardones[alumnoId] ? _pardones[alumnoId].size > 0 : false)
  const stBol2 = !hayOrd2 ? null : estadoModulo(ctxBol, miNotas, {
    notaRAOverride: (ra, n) => {
      const minKO = raMinExamKO(ra.id, cesDict[ra.id] || [], actividades, miNotas, minExamB, asigs)
      if (n === null || (n >= 5 && !minKO)) return n
      const lst = cesEvaluadosDeRa(ra.id, cesDict[ra.id] || [], actividades)
      const g = lst.map(ce => notaCEOrd2(ra.id, ce.id)).filter(x => x != null)
      return g.length ? g.reduce((s, x) => s + x, 0) / g.length : n
    },
    minKOOverride: (ra, ko) => {
      if (!ko) return false
      const lst = cesEvaluadosDeRa(ra.id, cesDict[ra.id] || [], actividades)
      if (!lst.length) return true
      return !lst.every(ce => { const n = notaCEOrd2(ra.id, ce.id); return n != null && n >= 5 })
    },
  })

  const raNotas = {}
  ras.forEach(ra => { raNotas[ra.id] = stBol.porRA[ra.id] ? stBol.porRA[ra.id].nota : null })

  const notaFinal = stBol.media
  const actaBol   = stBol.acta

  // H1 — regla de oro: superar el módulo exige todos los RA calificados ≥5
  const rasPendBol  = ras.filter(ra => stBol.pendientes.includes(ra.id))
  const superadoBol = stBol.superado
  const clFinal = notaFinal == null ? 'sin'
    : (stBol.resultado === 'SUPERADO' || stBol.resultado === 'SUPERADO_PARCIAL') ? 'ok' : 'ko'
  const lblFinal = notaFinal == null ? '–' : etiquetaResultado(stBol.resultado)
  const avisoRegla = notaFinal != null && !superadoBol && notaFinal >= 5 && rasPendBol.length
    ? `<div style="font-size:9px;color:#721c24;padding:4px 12px">Media ≥5 pero con RA pendientes (${e(rasPendBol.map(r => r.id).join(', '))}): la media no compensa un RA suspenso.</div>`
    : ''

  // Bloque 1ª Ord — con la calificación de acta, que es la que consta oficialmente
  const ord1Block = `<div class="conv">
    <div class="conv-hdr ord1">
      <span class="conv-num">1ª Ordinaria</span>
      <span class="conv-nota ${clFinal}">${notaFinal != null ? notaFinal.toFixed(2) : '—'}</span>
      ${actaBol != null ? `<span style="font-size:10px;color:#555">acta: <b>${actaBol}${stBol.resultado === 'SUPERADO_PARCIAL' ? ' SP' : ''}</b></span>` : ''}
      <span class="${clFinal==='ok'?'b-ok':clFinal==='ko'?'b-ko':'b-sin'}" style="font-size:11px">${lblFinal}</span>
    </div>
    ${avisoRegla}
  </div>`

  // Resultado de la 2ª convocatoria, cuando la hay
  const ord2Resultado = stBol2 && stBol2.media != null ? `<div class="conv">
    <div class="conv-hdr ord2">
      <span class="conv-num">2ª Ordinaria · resultado</span>
      <span class="conv-nota ${stBol2.superado ? 'ok' : 'ko'}">${stBol2.media.toFixed(2)}</span>
      ${stBol2.acta != null ? `<span style="font-size:10px;color:#555">acta: <b>${stBol2.acta}</b></span>` : ''}
      <span class="${stBol2.superado ? 'b-ok' : 'b-ko'}" style="font-size:11px">${stBol2.superado ? 'APTO/A' : 'NO APTO/A'}</span>
    </div>
    ${stBol2.pendientes.length
      ? `<div style="font-size:9px;color:#721c24;padding:4px 12px">RA pendientes tras la 2ª convocatoria: ${e(stBol2.pendientes.join(', '))}</div>`
      : '<div style="font-size:9px;color:#155724;padding:4px 12px">Todos los resultados de aprendizaje alcanzados.</div>'}
  </div>` : ''

  // Bloque 2ª Ord (solo si no supera — por media o por RA pendiente)
  let ord2Block = ''
  if (notaFinal != null && !superadoBol) {
    const rasKo = ras.filter(ra => {
      const n = raNotas[ra.id]
      return n == null || n < 5
    })

    if (rasKo.length === 0) {
      // No hay RAs suspendidos pero la nota global es < 5 (caso raro por ponderación)
      ord2Block = `<div class="conv">
        <div class="conv-hdr ord2">
          <span class="conv-num">2ª Ordinaria</span>
        </div>
        <div class="conv-body"><p style="font-size:10px;color:#555">Todos los RAs tienen nota ≥ 5. Revisar ponderación global.</p></div>
      </div>`
    } else {
      const raKoBlocks = rasKo.map(ra => {
        const nRa = raNotas[ra.id]
        // UTs que trabajan este RA
        const utsDelRA = asigs
          .filter(a => a.ra === ra.id)
          .map(a => uts.find(u => u.id === a.ut))
          .filter(Boolean)
        // CEs no superados de este RA (todos los CEs de las asignaciones de este RA)
        const cesKo = []
        asigs.filter(a => a.ra === ra.id).forEach(asig => {
          const ceLst = cesDict[asig.ra] || []
          ;(asig.ces || []).forEach(ceId => {
            const ce = ceLst.find(c => c.id === ceId)
            if (ce && !cesKo.find(c => c.id === ceId)) cesKo.push(ce)
          })
        })

        const utListHtml = utsDelRA.length
          ? `<div class="conv-ut-list">UTs relacionadas: ${utsDelRA.map(u => `<b>${e(u.id)}</b> ${e(u.nombre||'')} (EV${u.eval||1})`).join(' · ')}</div>`
          : ''

        const ceListHtml = cesKo.length
          ? `<div class="conv-ce-list">${cesKo.map(ce =>
              `❌ <b>${e(ce.id)}</b> — ${e(trunc(ce.texto, 120))}`
            ).join('<br>')}</div>`
          : ''

        return `<div class="conv-ra-ko">
          <div class="conv-ra-title">❌ ${e(ra.id)} (${ra.pond}%) · ${e(trunc(ra.nombre, 100))} &nbsp; Nota: ${nRa != null ? nRa.toFixed(2) : '—'}</div>
          ${utListHtml}
          ${ceListHtml}
        </div>`
      }).join('')

      ord2Block = `<div class="conv">
        <div class="conv-hdr ord2">
          <span class="conv-num">2ª Ordinaria — RAs y CEs a recuperar</span>
        </div>
        <div class="conv-body">${raKoBlocks}</div>
      </div>`
    }
  }

  const convBlocks = ord1Block + ord2Resultado + ord2Block

  // ── Ensamblar HTML ────────────────────────────────────────────────────
  const nombre = `${alumno.apellidos || ''}, ${alumno.nombre || ''}`
  const fecha  = new Date().toLocaleDateString('es-ES', {day:'2-digit', month:'long', year:'numeric'})
  const modMeta = [mod.ciclo || '', mod.curso || '', mod.grupo || ''].filter(Boolean).join(' · ')

  const html = `<!DOCTYPE html>
<html lang="es"><head>
<meta charset="UTF-8"/>
<title>Boletín — ${e(nombre)}</title>
<style>${css}</style>
</head><body>

<div class="hdr">
  <h1>Boletín de Evaluación</h1>
  <div class="mod-name">${e(mod.nombre || mod.abrev || '')}</div>
  ${modMeta ? `<div class="meta">${e(modMeta)}</div>` : ''}
  <div class="al">📋 ${e(nombre)}</div>
  <div class="meta">Generado: ${fecha}</div>
</div>

<div class="sec">Nota media por evaluación</div>
<table>
  <thead><tr>
    <th>Período</th>
    <th style="width:70px;text-align:center">Nota</th>
    <th style="width:110px">Resultado</th>
    <th>Actividades calificadas</th>
  </tr></thead>
  <tbody>${evalRows}${globalRow}</tbody>
</table>

<div class="sec">Detalle por Evaluación</div>
${evalBlocks}

<div class="sec">Resultado Final</div>
${convBlocks}

<div class="ftr">EvalFP · ${fecha} · ${e(mod.abrev || '')} — ${e(nombre)}</div>

</body></html>`

  await window.api.exportBoletin(html, nombre)
}

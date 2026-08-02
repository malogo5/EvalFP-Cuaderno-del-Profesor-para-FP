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

// El motor de cálculo vive en js/core/calificacion.js y lo comparten esta
// pantalla, el Dashboard, el boletín y el asistente de IA. Estos alias se
// conservan porque el resto del archivo los usa por su nombre antiguo.
const _mediaActs   = mediaActividades
const _calcNotaRA  = notaRA
const _calcNotaCE  = notaCE
const _raMinExamKO = raMinExamKO
const _actaEntera  = actaEntera

/**
 * Cierra una sesión de evaluación parcial: registra qué RA ha alcanzado cada
 * alumno para que no puedan volver a bajar. Es la traducción del art. 4.3.f de
 * la Orden 201/2024 («un resultado de aprendizaje superado no se puede volver a
 * evaluar»), y de paso deja fecha de cuándo se acordó.
 */
async function cerrarSesionEvaluacion(mid, ev) {
  const filas = window._evalCierrePendiente?.[ev] || []
  if (!filas.length) {
    alert('No hay ningún resultado de aprendizaje alcanzado que fijar en esta evaluación.')
    return
  }
  const alumnosAfectados = new Set(filas.map(f => f.alumnoId)).size
  if (!confirm(
    `Se van a fijar ${filas.length} resultado(s) de aprendizaje alcanzados por ${alumnosAfectados} alumno(s).\n\n` +
    'A partir de ahora, una actividad posterior no podrá bajarlos.\n' +
    'Puedes seguir subiéndolos, y reabrir uno concreto si te equivocas.\n\n¿Cerrar la evaluación?')) return
  try {
    const n = await window.api.cerrarEvaluacionRAs({ mid: parseInt(mid), evaluacion: ev, filas })
    showToast(`${n} resultados de aprendizaje fijados`)
    loadEvaluaciones()
  } catch (e) {
    alert('No se ha podido cerrar la evaluación: ' + validators.sanitizeErrorMessage(e, 'cerrarEvaluacion'))
  }
}

/**
 * Reabrir un RA que se fijó al cerrar una evaluación. El art. 4.3.f impide que un
 * RA superado vuelva a evaluarse, pero eso protege al alumnado de perder lo ya
 * alcanzado, no consagra un error de quien lo cerró: si la nota se fijó por
 * equivocación hay que poder deshacerlo, y que el motor vuelva a calcular.
 */
async function reabrirRa(mid, alumnoId, raId) {
  if (!confirm(
    `Se va a reabrir ${raId} para este alumno o alumna.\n\n` +
    'Dejará de estar fijado y volverá a calcularse con las notas que haya en cada momento, ' +
    'así que puede bajar.\n\n¿Reabrirlo?')) return
  try {
    await window.api.reabrirRaSuperado({ alumnoId: parseInt(alumnoId), raId: String(raId) })
    showToast(`${raId} reabierto`)
    loadEvaluaciones()
  } catch (e) {
    alert('No se ha podido reabrir: ' + validators.sanitizeErrorMessage(e, 'reabrirRa'))
  }
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
  // Evaluación de cada RA deducida de sus UT (misma fuente que Programación:
  // si el profesor mueve una UT de trimestre, aquí se refleja igual).
  const evalRas   = rasPorEvaluacion(modData, evalCount)   // {1:[raId,...], 2:[...]}

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
  const raPondOverrides = {}
  try {
    const rows = await window.api.getRaPonderaciones(parseInt(mid))
    rows.forEach(r => { raPondOverrides[r.ra_id] = r.pond })
  } catch { /* sin overrides */ }

  const ras = rasBase.map(ra => ({
    ...ra,
    pond: raPondOverrides[ra.id] !== undefined ? raPondOverrides[ra.id] : (ra.pond || 0)
  }))
  // Fase de formación en empresa por alumno (Orden 201/2024, art. 12)
  const fasesAlumno = {}
  try {
    const filas = await window.api.getFaseEmpresa(parseInt(mid))
    filas.forEach(f => { fasesAlumno[Number(f.alumno_id)] = f.estado })
  } catch { /* base antigua sin la tabla */ }
  const tieneFaseEmpresa = moduloConFaseEmpresa(modData?.modulo)
  // Los ámbitos de grado básico se califican IN/SU/BI/NT/SB (art. 25.2)
  const esAmbito = moduloEsAmbito(modData?.modulo)
  const actaTexto = st => {
    if (st.acta == null) return '—'
    if (!esAmbito) return `${st.acta}${st.resultado === 'SUPERADO_PARCIAL' ? ' SP' : ''}`
    const c = calificacionCualitativa(st.media)
    return c ? `${c.sigla}${st.resultado === 'SUPERADO_PARCIAL' ? ' SP' : ''}` : '—'
  }

  // RA ya cerrados como superados en una sesión de evaluación anterior: no
  // pueden volver a bajar (Orden 201/2024, art. 4.3.f).
  const rasCerrados = {}   // { alumnoId: { raId: nota } }
  try {
    const filas = await window.api.getRasSuperados(parseInt(mid))
    filas.forEach(f => {
      const aid = Number(f.alumno_id)
      if (!rasCerrados[aid]) rasCerrados[aid] = {}
      rasCerrados[aid][f.ra_id] = Number(f.nota)
    })
  } catch { /* base antigua sin la tabla */ }

  // Contexto del motor único de calificación (js/core/calificacion.js). Todas las
  // notas de esta pantalla, del Dashboard y del boletín salen de ahí.
  const ctxBase = { ras, cesByRa, asignaciones: asigsMod, actividades, minExam, tieneFaseEmpresa }
  const ctxCalculo = contextoModulo(ctxBase)
  const ctxDe = alumnoId => contextoModulo({ ...ctxBase, rasSuperados: rasCerrados[alumnoId] || null })
  // Un RA está en juego si alguna actividad lo califica: por ra_id, por criterios
  // marcados o por sus UT. Mirando solo ra_id, un RA evaluado con un examen de dos
  // unidades desaparecía de esta pantalla y se escapaba de la regla de oro.
  const rasActivos = ctxCalculo.rasActivos

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
  // Nota de un RA respetando el cierre de evaluación: un RA fijado no baja
  // aunque una actividad posterior sea peor (art. 4.3.f). El aviso de «Cerrar
  // evaluación» promete exactamente eso, y las tablas por evaluación y por RA lo
  // ignoraban: bastaba con bajar una nota para ver caer un RA ya fijado.
  const notaRAcruda = (ra, alumnoId) =>
    _calcNotaRA(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], PRAC, EXAM, asigsMod)

  const notaRAde = (ra, alumnoId) => {
    const n = notaRAcruda(ra, alumnoId)
    const cierre = rasCerrados[alumnoId] ? rasCerrados[alumnoId][ra.id] : null
    if (cierre == null) return n
    return n === null || n < cierre ? cierre : n
  }

  /**
   * H1/H3 — Estado completo de un alumno:
   * media ponderada, RAs pendientes (<5 o mínimo de examen KO), RAs sin nota,
   * y veredicto normativo: superado ⇔ todos los RA con nota ≥5 y sin mínimos KO.
   * H10 — Los RA SIN nota no computan en la media: su peso se reparte
   * proporcionalmente entre los RA evaluados (media = Σ n·pond / Σ pond de
   * los calificados). Antes contaban como 0 y arrastraban la media.
   */
  function estadoAlumno(alumnoId) {
    return estadoModulo(ctxDe(alumnoId), ng[alumnoId], { faseEmpresa: fasesAlumno[alumnoId] })
  }

  function nombreAl(al) {
    return `${al.apellidos || ''}${al.apellidos && al.nombre ? ', ' : ''}${al.nombre || ''}`
  }

  const badgeEstado = est => `<span style="background:var(--bg3);color:var(--text3);padding:1px 7px;border-radius:8px;font-size:10px;font-weight:700;border:1px solid var(--border2)">${est === 'Renuncia' ? 'RC' : 'BAJA'}</span>`
  // La etiqueta tiene que decir el estado REAL de cada persona: una etiqueta fija
  // de «Baja» presentaba como baja a quien había renunciado a la convocatoria,
  // que es otra cosa —y en el acta figura como RC (art. 25.9)—.
  const badgeDe = al => badgeEstado(al.estado || 'Baja')

  // Marca de recuperación sobre una celda de RA (H6)
  function recMark(alumnoId, raId) {
    // Por ra_id, por criterios o por UT: un examen de dos unidades no lleva ra_id
    // y su recuperación se quedaba sin señalizar.
    const raActIds = actividades
      .filter(a => actividadDeRa(a, raId, cesByRa[raId] || [], asigsMod)).map(a => a.id)
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
    ${evals.map(ev =>
      // evalLabel() en vez de la lista escrita a mano: esa etiquetaba como «3ª»
      // cualquier evaluación a partir de la tercera.
      `<div class="eval-tab${_evalTab === `ev${ev}` ? ' on' : ''}" data-etab="ev${ev}" onclick="setEvalTab('ev${ev}')">${evalLabel(ev)}</div>`
    ).join('')}
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
      : rasActivos.filter(ra => acts.some(a => actividadDeRa(a, ra.id, cesByRa[ra.id] || [], asigsMod)))

    if (!acts.length && !rasCov.length) return `
      <div class="card" style="padding:0">
        <div class="empty-state" style="margin:0">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Sin actividades para esta evaluación</div>
          <div>Ve a <b>Programación</b> para añadir prácticas o exámenes y asignarlos a UT/RA.</div>
        </div>
      </div>`

    const pracs = acts.filter(a => a.tipo === 'practica')
    const exams = acts.filter(a => a.tipo === 'examen')
    const actsBar = `<div class="card" style="padding:11px 16px;margin-bottom:12px">
      <div style="display:flex;gap:7px;flex-wrap:wrap;align-items:center">
        <span style="font-size:11px;color:var(--text3)">Actividades:</span>
        ${pracs.map(a => `<span style="padding:2px 8px;border-radius:6px;background:rgba(74,144,217,.1);border:1px solid rgba(74,144,217,.2);font-size:11px;color:var(--text2)">📝 ${esc(a.desc || a.descripcion || 'Práctica')} <span style="color:var(--text3)">${a.peso || 0}%</span></span>`).join('')}
        ${exams.map(a => `<span style="padding:2px 8px;border-radius:6px;background:rgba(201,154,61,.12);border:1px solid rgba(201,154,61,.2);font-size:11px;color:var(--text2)">📋 ${esc(a.desc || a.descripcion || 'Examen')} <span style="color:var(--text3)">${a.peso || 0}%</span></span>`).join('')}
      </div>
    </div>`

    if (!rasCov.length) return actsBar + `
      <div class="card" style="padding:0">
        <div class="empty-state" style="margin:0">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Sin RAs vinculados a esta evaluación</div>
          <div>Asigna RAs a las actividades (o a las UTs) desde <b>Programación</b> para que aquí se calcule el progreso.</div>
        </div>
      </div>`

    // ── H5: Boletín de la evaluación (media reponderada acumulada + pendientes) ──
    const rasVistos = rasActivos.filter(ra => raEvalMap[ra.id] <= ev)
    const bolRows = [...alumnos, ...alumnosBaja].map(al => {
      const esBaja = al.estado !== 'Activo'
      let sum = 0, pond = 0
      const pend = [], sinN = []
      rasVistos.forEach(ra => {
        const n = notaRAde(ra, al.id)
        const minKO = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[al.id], minExam, asigsMod)
        if (n !== null) { sum += n * ra.pond; pond += ra.pond }
        if (n === null) sinN.push(ra.id)
        else if (n < 5 || minKO) pend.push(ra.id + (minKO && n >= 5 ? ' ⚠mín' : ''))
      })
      const bol = pond > 0 ? sum / pond : null
      const bolTxt = bol !== null ? bol.toFixed(1) : '—'
      // Verde solo si además no arrastra ningún RA pendiente: una media de 6 con
      // un RA suspenso no es un aprobado, y pintarla en verde en el boletín que
      // ve la familia contradice la regla de oro que aplica el acta.
      const bolCls = bol === null ? ''
        : (bol >= 5 && !pend.length) ? 'nota-apto'
        : bol >= 4 ? 'nota-riesgo' : 'nota-noapto'
      const pendTxt = pend.length
        ? `<span style="color:var(--red);font-weight:600">${pend.join(', ')}</span>`
        : sinN.length === rasVistos.length ? '<span style="color:var(--text3)">sin notas</span>'
        : '<span style="color:var(--green)">—</span>'
      return `<tr${esBaja ? ' class="fila-baja"' : ''}>
        <td>${esc(nombreAl(al))} ${esBaja ? badgeDe(al) : ''}</td>
        <td class="nc" style="font-weight:700"><span class="${bolCls}">${bolTxt}</span></td>
        <td style="font-size:11px">${pendTxt}</td>
        <td style="text-align:center">
          <button class="btn btn-ghost btn-sm" onclick="genBoletin(${al.id},${ev})"
            title="Boletín de esta evaluación, con la situación acumulada del módulo">📄 PDF</button>
        </td>
      </tr>`
    }).join('')

    // Qué habría que fijar si se cierra esta sesión: los RA que cada alumno ya
    // tiene alcanzados (≥5 y sin mínimo de examen pendiente).
    if (!window._evalCierrePendiente) window._evalCierrePendiente = {}
    window._evalCierrePendiente[ev] = alumnos.flatMap(al => {
      const st = estadoAlumno(al.id)
      return rasVistos
        .filter(ra => {
          const r = st.porRA[ra.id]
          return r && r.nota !== null && r.nota >= 5 && !r.minKO &&
                 !(rasCerrados[al.id] && rasCerrados[al.id][ra.id] != null)
        })
        .map(ra => ({ alumnoId: al.id, raId: ra.id, nota: st.porRA[ra.id].nota }))
    })

    // Cierre de la sesión de evaluación: deja constancia de los RA alcanzados
    // para que no puedan volver a bajar con actividades posteriores.
    const yaCerrados = rasVistos.filter(ra =>
      alumnos.some(al => rasCerrados[al.id] && rasCerrados[al.id][ra.id] != null)).length
    const cierreCard = `<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;
        padding:9px 14px;margin-bottom:12px;background:var(--bg3);border:1px solid var(--border);border-radius:10px">
      <span style="font-size:11.5px;color:var(--text2)">
        Al cerrar la sesión, los RA alcanzados quedan fijados: una actividad posterior ya no los baja.
      </span>
      ${yaCerrados ? `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700">🔒 ${yaCerrados} RA fijados</span>` : ''}
      <button onclick="cerrarSesionEvaluacion(${mid},${ev})"
        title="Registra los RA con nota ≥5 y sin mínimo pendiente como superados en esta sesión (Orden 201/2024, art. 4.3.f)"
        style="margin-left:auto;background:var(--accent);color:#fff;border:none;border-radius:8px;
               padding:5px 14px;font-size:11.5px;font-weight:700;cursor:pointer">
        Cerrar ${evalLabel(ev).toLowerCase()}
      </button>
    </div>`

    const boletinCard = cierreCard + `<div style="border:1px solid var(--border2);border-radius:10px;overflow:hidden;margin-bottom:12px">
      <div style="padding:9px 14px;background:var(--bg3);border-bottom:1px solid var(--border);display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <span style="font-weight:700;font-size:13px">Boletín ${ev}ª evaluación</span>
        <span style="font-size:11px;color:var(--text3)">media reponderada de los RA trabajados hasta ahora (${rasVistos.map(r => r.id).join(', ')}) · el boletín NO sustituye al registro de RA pendientes</span>
      </div>
      <div style="overflow-x:auto"><table class="ev-tbl" style="width:100%">
        <thead><tr><th>Alumno/a</th><th class="nc" style="min-width:70px">Boletín</th><th>RA pendientes (acumulado)</th><th style="width:80px"></th></tr></thead>
        <tbody>${bolRows}</tbody>
      </table></div>
    </div>`

    const raSecs = rasCov.map(ra => {
      const ceLst = cesByRa[ra.id] || []
      // Actividades para calificación de este RA: todas las suyas —por ra_id, por
      // criterios o por UT— aunque estén repartidas en varias evaluaciones.
      const actsRA = raIdsConf.length
        ? actividades.filter(a => actividadDeRa(a, ra.id, ceLst, asigsMod))
        : acts
      const ceLstEv = ceLst.filter(ce => actsRA.some(a => actCubreCe(a, ra.id, ce.id)))

      // Con el RA ya fijado manda la nota del cierre, también aquí.
      const notaRAev = (raObj, alumnoId, ceList, acts) => {
        const n = _calcNotaRA(raObj.id, ceList, acts, ng[alumnoId], PRAC, EXAM, asigsMod)
        const cierre = rasCerrados[alumnoId] ? rasCerrados[alumnoId][raObj.id] : null
        if (cierre == null) return n
        return n === null || n < cierre ? cierre : n
      }
      const belowFive = alumnos.filter(al => {
        const n = notaRAev(ra, al.id, ceLst, actsRA)
        const minKO = rasCerrados[al.id]?.[ra.id] != null
          ? false
          : _raMinExamKO(ra.id, ceLst, actsRA, ng[al.id], minExam, asigsMod)
        return n !== null && (n < 5 || minKO)
      }).length
      const alertBadge = belowFive > 0
        ? `<span style="background:rgba(178,59,59,.1);color:var(--red);padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700">${belowFive} pendiente${belowFive > 1 ? 's' : ''}</span>`
        : `<span style="background:rgba(79,121,66,.1);color:var(--green);padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700">Todos ≥5</span>`

      const rows = [...alumnos, ...alumnosBaja].map(al => {
        const esBaja = al.estado !== 'Activo'
        const congelado = rasCerrados[al.id]?.[ra.id] != null
        const notaRA = notaRAev(ra, al.id, ceLst, actsRA)
        const minKO  = congelado ? false : _raMinExamKO(ra.id, ceLst, actsRA, ng[al.id], minExam, asigsMod)
        const naTxt  = (notaRA !== null ? notaRA.toFixed(1) : '—') + (congelado ? ' 🔒' : '')
        const naCls  = notaRA === null ? '' : (notaRA >= 5 && !minKO) ? 'nota-apto' : notaRA >= 4 ? 'nota-riesgo' : 'nota-noapto'
        const minBadge = minKO && notaRA !== null && notaRA >= 5
          ? ` <span title="Examen por debajo del mínimo (${minExam}): RA no superado aunque la media sea ≥5" style="color:var(--red);font-weight:700;font-size:10px">⚠mín</span>` : ''
        const ceCells = ceLstEv.map(ce => {
          const n   = _calcNotaCE(ra.id, ce.id, actsRA, ng[al.id], PRAC, EXAM)
          const txt = n !== null ? n.toFixed(1) : '—'
          const cls = n === null ? '' : n >= 5 ? 'nota-apto' : n >= 4 ? 'nota-riesgo' : 'nota-noapto'
          return `<td class="nc"><span class="${cls}" style="font-size:12px;font-weight:600">${txt}</span></td>`
        }).join('')
        return `<tr${esBaja ? ' class="fila-baja"' : ''}>
          <td>${esc(nombreAl(al))} ${esBaja ? badgeDe(al) : ''}</td>
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
    if (!rasActivos.length) return `
      <div class="card" style="padding:0">
        <div class="empty-state" style="margin:0">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Aún no hay RAs calificables</div>
          <div>Primero añade alumnado y actividades, y asigna RA/CE en <b>Programación</b>. Luego verás aquí la 1ª ordinaria.</div>
        </div>
      </div>`

    const estados = {}
    alumnos.forEach(al => { estados[al.id] = estadoAlumno(al.id) })

    // «Superado parcial» cuenta como superado (art. 18.4): quien ha alcanzado
    // todos los RA y solo le falta la fase en empresa no puede figurar entre
    // los que no superan, cuando su propia fila dice APTO/A · SP.
    const aptos    = alumnos.filter(al => estados[al.id].superadoParaPromocion).length
    const noAptos  = alumnos.filter(al => estados[al.id].completo && !estados[al.id].superadoParaPromocion).length
    const pendEval = alumnos.filter(al => !estados[al.id].completo && estados[al.id].media !== null).length
    // Con 5 activos se leía «0 superan · 0 no superan · 2 sin evaluar del todo»:
    // faltaban tres por explicar, los que no tienen ninguna nota todavía. Un
    // recuento que no suma hace dudar del resto de la pantalla.
    const sinNada  = alumnos.filter(al => estados[al.id].media === null).length
    const medias   = alumnos.map(al => estados[al.id].media).filter(n => n !== null)
    const media    = medias.length ? (medias.reduce((s, n) => s + n, 0) / medias.length).toFixed(1) : '—'

    const kpis = `<div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${alumnos.length}</div><div style="font-size:10px;color:var(--text2)">Activos</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--green)">${aptos}</div><div style="font-size:10px;color:var(--text2)">Superan (incluye SP)</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--red)">${noAptos}</div><div style="font-size:10px;color:var(--text2)">No superan</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--amber, #c99a3d)">${pendEval}</div><div style="font-size:10px;color:var(--text2)">A medio evaluar</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--text3)">${sinNada}</div><div style="font-size:10px;color:var(--text2)">Sin ninguna nota</div></div>
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
      const nFCls  = nFinal === null ? '' : st.superadoParaPromocion ? 'nota-apto' : nFinal >= 4 ? 'nota-riesgo' : 'nota-noapto'

      // H1 — veredicto normativo
      // Los tres estados del art. 12: superado, superado parcial y no superado
      let apto, aptoSty, motivo = ''
      if (esBaja)               { apto = '—';          aptoSty = 'color:var(--text3)' }
      else {
        apto = etiquetaResultado(st.resultado)
        aptoSty = st.resultado === 'SUPERADO' ? 'color:var(--green)'
          : st.resultado === 'SUPERADO_PARCIAL' ? 'color:var(--accent2)'
          : st.resultado === 'NO_SUPERADO' ? 'color:var(--red)'
          : st.resultado === 'PENDIENTE' ? 'color:var(--amber, #c99a3d)' : 'color:var(--text3)'
        if (st.resultado === 'PENDIENTE') motivo = `Sin nota: ${st.sinNota.join(', ')}`
        else if (st.resultado === 'SUPERADO_PARCIAL') {
          motivo = 'Superado parcial: alcanzado todo lo del centro, falta la fase de formación en empresa ' +
                   '(Orden 201/2024, art. 12). A efectos de promoción cuenta como superado.'
        } else if (st.resultado === 'NO_SUPERADO' && st.pendientes.length) {
          motivo = `RA pendientes: ${st.pendientes.join(', ')}`
        } else if (st.resultado === 'NO_SUPERADO' && st.centroOk) {
          motivo = 'La fase de formación en empresa consta como no superada.'
        }
      }

      // H8 — acta, con las siglas SP cuando falta la fase de empresa (art. 25.4)
      const acta = (esBaja || nFinal === null || !st.completo) ? '—' : actaTexto(st)
      const actaCls = acta === '—' ? '' : (st.acta >= 5 ? 'nota-apto' : 'nota-noapto')

      const raCells = rasActivos.map(ra => {
        const { nota: n, minKO, congelado } = st.porRA[ra.id]
        const txt = n !== null ? n.toFixed(1) : '—'
        const cls = n === null ? '' : (n >= 5 && !minKO) ? 'nota-apto' : n >= 4 ? 'nota-riesgo' : 'nota-noapto'
        const warn = minKO && n !== null && n >= 5 ? `<span title="Examen bajo mínimo (${minExam})" style="color:var(--red);font-size:9px;font-weight:700">⚠</span>` : ''
        // Un RA fijado al cerrar la evaluación (art. 4.3.f) se marca con el candado
        // y se puede reabrir desde aquí: el aviso de cierre lo promete y hasta ahora
        // no había ninguna manera de deshacerlo.
        const lock = congelado && !esBaja
          ? `<span onclick="event.stopPropagation();reabrirRa(${mid},${al.id},'${String(ra.id).replace(/'/g, "\\'")}')"
                   title="RA fijado al cerrar una evaluación. Pulsa para reabrirlo."
                   style="cursor:pointer;font-size:10px;margin-left:2px">🔒</span>`
          : ''
        return `<td class="nc" style="font-size:12px;font-weight:600"><span class="${cls}">${txt}</span>${lock}${recMark(al.id, ra.id)}${warn}</td>`
      }).join('')

      const raBlocks = rasActivos.map(ra => {
        const { nota: nRa, minKO } = st.porRA[ra.id]
        const ceLst = cesByRa[ra.id] || []
        const okRA = nRa !== null && nRa >= 5 && !minKO
        const border = nRa === null ? 'var(--border2)' : okRA ? 'var(--green)' : 'var(--red)'
        const raCls  = nRa === null ? '' : okRA ? 'nota-apto' : nRa >= 4 ? 'nota-riesgo' : 'nota-noapto'

        const ceChips = ceLst.map(ce => {
          const n   = _calcNotaCE(ra.id, ce.id, actividades, ng[al.id], PRAC, EXAM)
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

      // Anulada la matrícula no hay evaluación en ninguna convocatoria (Orden
      // 201/2024, art. 7.1): se ve la fila, con sus notas de trabajo, pero sin
      // calificación final, sin acta y sin veredicto.
      const esRenuncia = al.estado === 'Renuncia'
      const celdasFinales = esBaja
        ? (esRenuncia
          ? `<td class="nc" colspan="3" style="font-size:11px;color:var(--text3);font-style:italic"
                 title="Orden 201/2024, art. 11 y 25.9: la renuncia a convocatoria se refleja en actas como «RC» y no consume convocatoria">
               RC · renuncia a convocatoria
             </td>`
          : `<td class="nc" colspan="3" style="font-size:11px;color:var(--text3);font-style:italic"
                 title="Orden 201/2024, art. 7.1: la anulación de matrícula supone no ser evaluado en ninguna convocatoria del curso">
               Matrícula anulada · sin evaluación
             </td>`)
        : `<td class="nc" style="font-weight:700;font-size:14px"><span class="${nFCls}">${nFTxt}</span></td>
           <td class="nc" style="font-weight:700;font-size:14px"><span class="${actaCls}">${acta}</span></td>
           <td style="text-align:center;font-weight:700;font-size:11px;${aptoSty}" ${motivo ? `title="${esc(motivo)}"` : ''}>${apto}${motivo ? ' *' : ''}</td>`

      return `
        <tr onclick="toggleEvalCard(${al.id})" style="cursor:pointer" ${esBaja ? 'class="fila-baja"' : ''}
            onmouseover="this.style.background='var(--bg3)'" onmouseout="this.style.background=''">
          <td>
            <span id="eval-chev-${al.id}" style="font-size:10px;color:var(--text3);margin-right:8px;display:inline-block">▶</span>
            ${esc(nombreAl(al))} ${esBaja ? badgeEstado(al.estado) : ''}
          </td>
          ${raCells}
          ${celdasFinales}
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
            <th class="nc" style="min-width:52px" title="Calificación de acta. En los módulos, número entero de 1 a 10 (art. 25.4), con tope de 4 si no se alcanzan todos los RA (art. 25.5). En los ámbitos de grado básico, IN/SU/BI/NT/SB (art. 25.2).">Acta</th>
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
    if (!rasActivos.length) return `
      <div class="card" style="padding:0">
        <div class="empty-state" style="margin:0">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Aún no hay RAs calificables</div>
          <div>La 2ª ordinaria se activa cuando hay notas y RAs evaluables en el módulo.</div>
        </div>
      </div>`

    // ceKey() vive en js/utils/ce-keys.js: la clave es RA+CE porque el id del
    // criterio (CR1, CR2…) se repite en todos los RA del módulo.

    // ── Nota efectiva de un CE en 2ª ordinaria ─────────────────
    //
    // A-5: hay tres formas de acreditar un criterio en la segunda convocatoria y
    // ninguna puede empeorar a las otras, así que vale la mejor de las tres:
    //   · la actividad de recuperación (el «instrumento diferente» del art. 21.5),
    //     que el motor ya mezcla con la nota del curso en `_calcNotaCE(…, 2)`;
    //   · la nota suelta por criterio que se teclea en este panel;
    //   · el criterio que el equipo docente da por alcanzado, que vale un 5.
    function ceNotaOrd2(alumnoId, raId, ceId) {
      const k = ceKey(raId, ceId)
      // Nota del curso combinada con la de la actividad de recuperación
      const conRec = _calcNotaCE(raId, ceId, actividades, ng[alumnoId], PRAC, EXAM, 2)
      const soloOrd = _calcNotaCE(raId, ceId, actividades, ng[alumnoId], PRAC, EXAM, 1)

      const candidatos = []
      if (conRec !== null) candidatos.push({ nota: conRec, fuente: conRec === soloOrd ? 'orig' : 'actividad' })
      const rec = _rec2Notas[alumnoId]?.[k]
      if (rec != null) candidatos.push({ nota: rec, fuente: 'rec' })
      if (_pardones[alumnoId]?.has(k)) candidatos.push({ nota: 5, fuente: 'pardon' })

      if (!candidatos.length) return { nota: null, fuente: 'pendiente' }
      const mejor = candidatos.reduce((a, b) => (b.nota > a.nota ? b : a))
      if (mejor.fuente === 'orig') {
        return mejor.nota >= 5
          ? { nota: mejor.nota, fuente: 'orig_ok' }
          : { nota: mejor.nota, fuente: 'pendiente' }
      }
      return mejor
    }

    // ── Criterios que se promedian, iguales en las dos convocatorias ──
    // Solo los que alguna actividad evalúa. Un criterio sin instrumento no entra
    // en la media ni aunque se marque como aprobado: en junio no entraba, y la
    // nota del mismo RA no puede calcularse sobre bases distintas según el mes.
    const cesDeRa = ra => cesEvaluadosDeRa(ra.id, cesByRa[ra.id] || [], actividades)

    // ── Nota de un RA en 2ª ordinaria ─────────────────────────
    // Si RA superado en 1ª (≥5 y sin mínimo KO): se mantiene bloqueado.
    // Si no: recalcular desde CEs con ceNotaOrd2.
    function raNotaOrd2(alumnoId, ra) {
      const orig  = notaRAde(ra, alumnoId)
      const minKO = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], minExam, asigsMod)
      // Un RA sin ninguna nota NO está superado: es un RA sin evaluar. Tratarlo
      // como «orig_ok» lo pintaba con el candado 🔒 de aprobado y lo dejaba fuera
      // de la recuperación, de modo que a quien no se presentó a nada en junio no
      // se le podía recuperar nada en la segunda convocatoria.
      if (orig === null) return { nota: null, fuente: 'sin_evaluar', orig: null }
      if (orig >= 5 && !minKO) return { nota: orig, fuente: 'orig_ok', orig }

      const ceLst = cesDeRa(ra)
      if (!ceLst.length) return { nota: orig, fuente: 'orig_fail', orig }

      // A-5: la nota del RA en la segunda convocatoria la calcula el MISMO motor
      // que la de la primera, con las mismas ponderaciones por criterio. Antes se
      // promediaba aquí a mano y a peso igual: dos convocatorias, dos fórmulas.
      const nota = _calcNotaRA(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId],
        PRAC, EXAM, asigsMod, 2, (raId, ceId) => ceNotaOrd2(alumnoId, raId, ceId).nota)
      if (nota === null) return { nota: orig, fuente: 'pendiente', orig }
      return { nota, fuente: 'rec', orig }
    }

    /**
     * ¿Sigue bloqueando el mínimo de examen en la 2ª convocatoria?
     * El mínimo señala que ciertos criterios no están acreditados; deja de
     * bloquear cuando el alumno los acredita todos en la recuperación, no antes.
     * (Sin esto, un RA suspenso en junio por examen bajo mínimo aparecía superado
     * en la segunda convocatoria sin haber recuperado nada.)
     */
    function raMinKOOrd2(alumnoId, ra) {
      if (minExam == null) return false
      const koEn1 = _raMinExamKO(ra.id, cesByRa[ra.id] || [], actividades, ng[alumnoId], minExam, asigsMod)
      if (!koEn1) return false
      const ceLst = cesDeRa(ra)
      if (!ceLst.length) return true
      return !ceLst.every(ce => {
        const n = ceNotaOrd2(alumnoId, ra.id, ce.id).nota
        return n !== null && n >= 5
      })
    }

    // ── Estado 2ª ordinaria (H1: regla de oro · H10: reponderación) ──
    // Mismo motor que la 1ª convocatoria: solo cambia de dónde sale la nota de
    // cada RA y si el mínimo de examen sigue bloqueando. Así las dos convocatorias
    // no pueden divergir en la media, la regla de oro ni la nota de acta.
    function estadoOrd2(alumnoId) {
      const detalle = {}
      const st = estadoModulo(ctxDe(alumnoId), ng[alumnoId], {
        faseEmpresa: fasesAlumno[alumnoId],
        notaRAOverride: ra => {
          const r = raNotaOrd2(alumnoId, ra)
          detalle[ra.id] = r
          return r.nota
        },
        minKOOverride: ra => raMinKOOrd2(alumnoId, ra),
      })
      for (const id of Object.keys(detalle)) st.porRA[id] = { ...st.porRA[id], ...detalle[id] }
      return st
    }

    // ── KPIs ──────────────────────────────────────────────────
    // Concurre a la 2ª convocatoria quien no superó el módulo en la 1ª: tanto por
    // llevar RA suspensos como por tenerlos SIN NOTA (no presentado), que antes
    // se quedaba fuera de la lista siendo justo quien más la necesita.
    const conRec = alumnos.filter(al => {
      const st = estadoAlumno(al.id)
      return st.pendientes.length > 0 || st.sinNota.length > 0
    })
    const estados2 = {}
    alumnos.forEach(al => { estados2[al.id] = estadoOrd2(al.id) })
    // Todos los indicadores se refieren al MISMO grupo: quien concurre a la 2ª.
    const aptosRec   = conRec.filter(al => estados2[al.id].superadoParaPromocion).length
    const noAptosRec = conRec.filter(al => estados2[al.id].completo && !estados2[al.id].superadoParaPromocion).length
    const notasRec   = conRec.map(al => estados2[al.id].media).filter(n => n !== null)
    const mediaRec   = notasRec.length ? (notasRec.reduce((s, n) => s + n, 0) / notasRec.length).toFixed(1) : '—'

    const kpis = `<div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700">${alumnos.length}</div><div style="font-size:10px;color:var(--text2)">Alumnos</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--red)">${conRec.length}</div><div style="font-size:10px;color:var(--text2)">Con recuperación</div></div>
      <div style="flex:1;min-width:75px;background:var(--bg3);border-radius:10px;padding:10px 14px;border:1px solid var(--border)"><div style="font-size:20px;font-weight:700;color:var(--green)">${aptosRec}</div><div style="font-size:10px;color:var(--text2)">Superan 2ª (incluye SP)</div></div>
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
      else if (st2.resultado === 'SUPERADO_PARCIAL') {
        apto = etiquetaResultado(st2.resultado); aptoSty = 'color:var(--accent2)'
        motivo = 'Superado parcial: falta la fase de formación en empresa (art. 12).'
      }
      else if (st2.superado)   { apto = 'APTO/A';    aptoSty = 'color:var(--green)' }
      else                     { apto = 'NO APTO/A'; aptoSty = 'color:var(--red)'; motivo = st2.pendientes.length ? `RA pendientes: ${st2.pendientes.join(', ')}` : '' }

      const acta = (nF2 === null || !st2.completo) ? '—' : actaTexto(st2)
      const actaCls = acta === '—' ? '' : (st2.acta >= 5 ? 'nota-apto' : 'nota-noapto')

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
          const ceOrigNota = _calcNotaCE(ra.id, ce.id, actividades, ng[al.id], PRAC, EXAM)
          const pardoned   = _pardones[al.id]?.has(k)
          const rec2n      = _rec2Notas[al.id]?.[k]

          // Criterio que ninguna actividad evalúa: se ve, para saber que está ahí,
          // pero no se puede calificar ni dar por aprobado — y no entra en la media.
          const tieneActividad = actividades.some(a => actCubreCe(a, ra.id, ce.id))
          if (!tieneActividad) {
            return `<div style="display:flex;align-items:center;gap:8px;padding:4px 0;
                                 border-top:1px solid var(--border);font-size:11px;opacity:.55">
              <span style="width:16px;flex-shrink:0">○</span>
              <span style="color:var(--accent);font-weight:700;min-width:36px;flex-shrink:0">${esc(ce.id)}</span>
              <span style="flex:1;color:var(--text2);font-size:10.5px">${esc(ce.texto.length > 90 ? ce.texto.slice(0, 89) + '…' : ce.texto)}</span>
              <span title="Ninguna práctica ni examen evalúa este criterio. Asígnale un instrumento en Programación; hasta entonces no puede recuperarse ni contar en la nota."
                    style="font-size:9.5px;color:var(--amber);font-weight:700;white-space:nowrap">sin instrumento</span>
              ${pardoned ? `<button onclick="event.stopPropagation();togglePardonCe(${mid},${al.id},'${raIdSafe}','${ceIdSafe}')"
                  style="font-size:10px;padding:1px 7px;border-radius:5px;border:1px solid var(--border2);
                         background:rgba(16,185,129,.1);color:var(--green);cursor:pointer;white-space:nowrap">↩ Quitar</button>` : ''}
            </div>`
          }

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
          <th class="nc" style="min-width:52px" title="Calificación de acta. En los módulos, número entero de 1 a 10 (art. 25.4), con tope de 4 si no se alcanzan todos los RA (art. 25.5). En los ámbitos de grado básico, IN/SU/BI/NT/SB (art. 25.2).">Acta</th>
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
    || `<div class="empty-state">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Sin datos de notas todavía</div>
          <div>Añade alumnado y registra alguna calificación en <b>Notas</b> para ver el cálculo por RA y las ordinarias.</div>
        </div>`
}

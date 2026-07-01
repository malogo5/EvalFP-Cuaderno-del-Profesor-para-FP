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

// PONDERACIONES DE RAs
// ═══════════════════════════════════════════════════════════════
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

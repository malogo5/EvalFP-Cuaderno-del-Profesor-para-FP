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
    panel.innerHTML = `
      <div class="empty-state">
        <div style="font-weight:700;color:var(--text);margin-bottom:6px">Este módulo aún no tiene programación cargada</div>
        <div style="margin-bottom:12px">Cuando añadas los RAs y CE en el catálogo del módulo, aquí verás el plan de actividades, la distribución por evaluaciones y el mapa UT → RA.</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn btn-primary btn-sm" onclick="openAddModulo()">＋ Añadir módulo</button>
          <button class="btn btn-ghost btn-sm" onclick="goSection('modulos')">📚 Ver catálogo</button>
        </div>
      </div>`
    return
  }

  const ras        = data.ras        || []
  const ces        = data.ces        || {}
  const uts        = data.uts        || []
  const asigs      = data.asignaciones || []  // [{ut,ra,ces:[CRx...]}]
  const raInstr    = data.ra_instrumentos || {}
  // Cargar actividades desde BD (tienen los pesos reales editados por el profesor)
  const actividades = (await window.api.getActividades(parseInt(mid))) || data.actividades || []

  // Cargar overrides de ponderación de RAs y mezclar con los defaults del JSON
  const raPondOverrides = {}
  try {
    const rows = await window.api.getRaPonderaciones(parseInt(mid))
    rows.forEach(r => { raPondOverrides[r.ra_id] = r.pond })
  } catch { /* sin overrides — usar ponderaciones por defecto del JSON */ }
  // Aplicar overrides al raMap
  ras.forEach(ra => {
    if (raPondOverrides[ra.id] !== undefined) ra.pond = raPondOverrides[ra.id]
  })

  // índices rápidos
  const utMap  = Object.fromEntries(uts.map(u => [u.id, u]))
  const raMap  = Object.fromEntries(ras.map(r => [r.id, r]))
  const evalCount = data.modulo?.eval_count || [...new Set(uts.map(u => u.eval||1))].length || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)

  // Qué RAs caen en cada evaluación. Fuente única: la evaluación de las UT que los
  // trabajan, que es lo que el profesor mueve en la tabla de unidades. Así el plan
  // de actividades, la distribución y la ficha de cada RA dicen siempre lo mismo.
  const evalRasMap = rasPorEvaluacion(data, evalCount)
  const evalDeRa   = {}
  for (const [ev, lista] of Object.entries(evalRasMap)) for (const raId of lista) evalDeRa[raId] = ev
  // Dejarlo escrito en el módulo: es lo que leen los informes y los scripts de IA
  await _sincronizarEvalRas(mid, evalCount)

  // Trazabilidad al revés: para cada criterio, qué actividades lo evalúan. Es la
  // pregunta que hay que poder contestar en una reclamación.
  const coberturaCe = {}
  for (const act of actividades) {
    for (const g of cesDisponiblesActividad(act, asigs, ces)) {
      for (const ce of g.ces) {
        if (!actCubreCe(act, g.raId, ce.id)) continue
        const k = ceKey(g.raId, ce.id)
        ;(coberturaCe[k] = coberturaCe[k] || []).push(act.descripcion || act.instrumento || 'actividad')
      }
    }
  }
  const totalCes = ras.reduce((s, ra) => s + (ces[ra.id] || []).length, 0)
  const cesCubiertos = Object.keys(coberturaCe).length

  // ── cabecera ──────────────────────────────────────────────────
  let h = `
  <div class="card" style="margin-bottom:16px;padding:16px 20px;border-left:4px solid var(--accent)">
    <div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap">
      <span style="font-size:24px;font-weight:800;color:var(--accent2)">${esc(mod.abrev)}</span>
      <span style="font-size:15px;font-weight:600">${esc(mod.nombre)}</span>
      <span style="font-size:12px;background:var(--navy3);padding:2px 10px;border-radius:10px;color:var(--text2)">${esc(String(mod.horas||'?'))} h</span>
      <span style="font-size:12px;background:var(--navy3);padding:2px 10px;border-radius:10px;color:var(--text2)">${ras.length} RAs · ${uts.length} UTs</span>
    </div>
    <div style="margin-top:10px;font-size:11.5px;color:var(--text2);line-height:1.55">
      Edita aquí la estructura del módulo: ponderaciones de evaluación, distribución de RAs, unidades de trabajo y asignaciones.
      Todo el resto de pantallas se alimenta de esta base.
    </div>
    ${mod.decreto ? `<div style="font-size:11px;color:var(--accent2);margin-top:6px">📜 ${esc(mod.decreto)}</div>` : ''}
  </div>`

  // ── 1. PLAN DE ACTIVIDADES POR EVALUACIÓN ────────────────────
  {
    const _e0acts = actividades.filter(a => a.eval === evals[0])
    const _initPrac = Math.round(_e0acts.filter(a => a.tipo==='practica').reduce((s,a)=>s+(a.peso||0),0)) || 30
    const _initExam = Math.round(_e0acts.filter(a => a.tipo==='examen'  ).reduce((s,a)=>s+(a.peso||0),0)) || 70
    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
        📝 Plan de Actividades y Evaluación
        <button onclick="rellenarCesDesdeUts(${mid})"
          title="Marca en cada actividad los criterios que su unidad de trabajo tiene asignados en el decreto. No toca las actividades que ya tengan criterios marcados."
          style="background:transparent;color:var(--accent);border:1.5px solid var(--accent);border-radius:8px;padding:3px 12px;font-size:11.5px;font-weight:700;cursor:pointer">
          Rellenar criterios desde las UT
        </button>
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

    // A-5 · Las actividades de recuperación de la 2ª convocatoria van en su propia
    // sección: si se mezclaran con las del trimestre falsearían la suma del 100 %
    // y entrarían en la nota de la 1ª convocatoria, que ya está en acta.
    const actsRecuperacion = actividades.filter(a => Number(a.convocatoria) === 2)

    for (const ev of evals) {
      const acts = actividades.filter(a => a.eval === ev && Number(a.convocatoria) !== 2).sort((a,b) => {
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
      h += `<div style="margin-bottom:14px" id="eval-section-${ev}"
        ondragover="actDragOver(event)" ondragleave="actDragLeave(event)" ondrop="actDrop(event,${ev})">
        <div style="font-size:12px;font-weight:700;color:var(--ice);background:var(--navy3);padding:7px 14px;border-radius:6px;margin-bottom:6px;display:flex;gap:12px;align-items:center">
          <span>${evalLabel(ev)}</span>
          ${rasEvalStr ? `<span style="font-size:11px;font-weight:400;color:var(--text2)">${rasEvalStr}</span>` : ''}
          ${pesoWarn}
        </div>`
      if (acts.length) {
        h += `<table class="prog-table">
          <thead><tr>
            <th style="width:24px"></th>
            <th>Actividad</th>
            <th style="width:88px;text-align:center">Instrumento</th>
            <th style="width:55px;text-align:center">Tipo</th>
            <th class="th-editable" style="width:72px;text-align:center">Peso %</th>
            <th class="th-editable" style="width:72px;text-align:center">Nota máx</th>
            <th class="th-editable" style="width:78px;text-align:center">UT</th>
            <th style="width:56px;text-align:center" title="Resultado de aprendizaje que califica esta actividad, según sus unidades de trabajo">RA</th>
            <th style="width:62px;text-align:center" title="Criterios de evaluación asignados">CEs</th>
            <th style="width:30px"></th>
          </tr></thead>
          <tbody>`
        for (const act of acts) {
          const badge = act.tipo==='examen'
            ? 'background:rgba(224,160,58,.2);color:var(--amber)'
            : 'background:rgba(74,144,217,.15);color:var(--accent2)'
          const actId = act.id || ''
          h += `<tr draggable="${actId?'true':'false'}" data-actid="${actId}" data-fromeval="${ev}"
            ondragstart="actDragStart(event)" ondragend="actDragEnd()"
            style="cursor:${actId?'grab':'default'}">
            <td style="text-align:center;color:var(--text2);font-size:16px;padding:0 4px;line-height:1" title="Arrastrar a otra evaluación">⠿</td>
            <td>${actId
              ? `<input class="nota-cell" type="text" value="${esc(act.descripcion)}"
                  data-actid="${actId}" data-field="descripcion"
                  style="width:100%;text-align:left;font-size:12px"
                  onchange="updateActividadDesc(this)"/>`
              : `<span style="font-size:12px">${esc(act.descripcion)}</span>`}
            </td>
            <td style="text-align:center"><span style="font-size:11px;padding:2px 7px;border-radius:8px;${badge}">${esc(act.instrumento)}</span></td>
            <td style="text-align:center;font-size:11px;color:var(--text2)">${act.tipo||''}</td>
            <td style="text-align:center">
              ${actId ? `<input class="peso-cell" type="number" min="0" max="100" step="1"
                value="${act.peso}" data-actid="${actId}"
                oninput="_refreshPesoTotal(this)"
                onchange="updateActividadPeso(this)"
                title="Peso (%)"/>` : `<span style="font-weight:700;color:var(--accent)">${act.peso}%</span>`}
            </td>
            <td style="text-align:center">
              ${actId ? `<input class="peso-cell" type="number" min="0" max="10" step="0.5"
                value="${act.nota_max}" data-actid="${actId}" data-field="nota_max"
                onchange="updateActividadPeso(this)"
                title="Nota máxima"/>` : `<span style="color:var(--text2)">${act.nota_max}</span>`}
            </td>
            <td style="text-align:center">
              ${actId ? (() => {
                const utIds = (act.ut_id||'').split(',').filter(Boolean)
                if (act.tipo === 'examen') {
                  const chips = utIds.map(id =>
                    `<span style="font-size:10px;font-weight:700;color:var(--accent2);background:rgba(74,144,217,.12);padding:1px 5px;border-radius:4px;white-space:nowrap">${esc(id)}</span>`
                  ).join('')
                  return `<div style="display:flex;flex-direction:column;align-items:center;gap:3px">
                    <div style="display:flex;flex-wrap:wrap;gap:2px;justify-content:center">${chips||'<span style="font-size:11px;color:var(--text3)">—</span>'}</div>
                    <button onclick="openActUtsModal(${actId},${mid},'${(act.ut_id||'').replace(/'/g,"\\'")}')"
                      style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:2px 8px;font-size:10px;font-weight:700;cursor:pointer;margin-top:1px">UT</button>
                  </div>`
                }
                return `<select class="nota-cell" data-actid="${actId}"
                  style="width:68px;font-size:11px;padding:2px 2px;text-align:center"
                  onchange="updateActividadUT(this)">
                  <option value="">—</option>
                  ${uts.map(ut => `<option value="${ut.id}"${act.ut_id===ut.id?' selected':''}>${esc(ut.id)}</option>`).join('')}
                </select>`
              })() : `<span style="font-size:11px;color:var(--text2)">${act.ut_id||'—'}</span>`}
            </td>
            <td style="text-align:center">${(() => {
              // El RA sale de las UT de la actividad: es el eslabón que faltaba para
              // seguir la cadena actividad → UT → RA → criterios sin salir de aquí.
              const rasAct = rasDeActividad(act, asigs)
              if (!rasAct.length) {
                return `<span title="Esta actividad no tiene unidad ni RA asignados, así que no califica nada"
                  style="font-size:10px;font-weight:700;color:var(--amber);white-space:nowrap">sin RA</span>`
              }
              return rasAct.map(id =>
                `<span style="font-size:10px;font-weight:700;color:var(--accent2);background:rgba(74,144,217,.12);padding:1px 5px;border-radius:4px;white-space:nowrap;display:inline-block;margin:1px">${esc(id)}</span>`
              ).join('')
            })()}</td>
            <td style="text-align:center">${(() => {
              if (!actId) return '<span style="font-size:11px;color:var(--text3)">—</span>'
              // Los criterios disponibles se agrupan por RA (un examen puede cubrir
              // varias UT y varios RA) y se cuentan por su clave RA|CE, que es la
              // única que identifica un criterio dentro del módulo.
              const grupos = cesDisponiblesActividad(act, asigs, ces)
              const total  = grupos.reduce((s, g) => s + g.ces.length, 0)
              const validas = []
              for (const g of grupos) {
                for (const ce of g.ces) {
                  if (actCubreCe(act, g.raId, ce.id)) validas.push(ceKey(g.raId, ce.id))
                }
              }
              const count = validas.length
              if (!total) return '<span style="font-size:11px;color:var(--text3)">—</span>'
              const btnColor = count > 0 ? 'var(--green)' : 'var(--text3)'
              const currentCesStr = JSON.stringify(validas).replace(/"/g,'&quot;')
              const utIdSafe = (act.ut_id || '').replace(/'/g,"\\'")
              const raIdSafe = (act.ra_id || '').replace(/'/g,"\\'")
              return `<button onclick="openActCesModal(${actId},${mid},'${utIdSafe}','${raIdSafe}',this.dataset.ces)"
                data-ces="${currentCesStr}"
                title="${count}/${total} CEs asignados"
                style="background:transparent;color:${btnColor};border:1px solid ${btnColor};border-radius:6px;padding:2px 7px;font-size:10px;font-weight:700;cursor:pointer;white-space:nowrap">
                ${count}/${total}
              </button>`
            })()}</td>
            <td style="text-align:center">${actId
              ? `<button onclick="deleteActividadRow(${actId})" title="Eliminar" aria-label="Eliminar actividad"
                  style="background:transparent;color:#ef4444;border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:2px 6px;font-size:11px;cursor:pointer;line-height:1">✕</button>`
              : ''}</td>
          </tr>`
        }
        h += `</tbody></table>`
      } else {
        h += `<div class="empty-state" style="margin:0 0 8px">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">No hay actividades en esta evaluación</div>
          <div style="margin-bottom:10px">Puedes empezar añadiendo una práctica o un examen; luego asigna UT, RA, peso y criterios.</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button onclick="addActividad(${mid},${ev},'practica')"
              style="background:rgba(74,144,217,.12);color:var(--accent2);border:none;border-radius:8px;padding:5px 14px;font-size:12px;font-weight:700;cursor:pointer">+ Práctica</button>
            <button onclick="addActividad(${mid},${ev},'examen')"
              style="background:rgba(224,160,58,.12);color:var(--amber);border:none;border-radius:8px;padding:5px 14px;font-size:12px;font-weight:700;cursor:pointer">+ Examen</button>
          </div>
        </div>`
      }
      h += `<div style="display:flex;gap:8px;padding:8px 2px 2px">
          <button onclick="addActividad(${mid},${ev},'practica')"
            style="${btnSt}background:rgba(74,144,217,.12);color:var(--accent2)">+ Práctica</button>
          <button onclick="addActividad(${mid},${ev},'examen')"
            style="${btnSt}background:rgba(224,160,58,.12);color:var(--amber)">+ Examen</button>
        </div>
      </div>`
    }

    // ── Recuperación · 2ª convocatoria ──────────────────────────
    // El art. 21.5 pide evaluar los RA no superados «utilizando otros instrumentos
    // de evaluación diferentes»: aquí se dan de alta esos instrumentos. Se
    // califican en Notas y la nota entra sola en la 2ª convocatoria, por los
    // criterios que se les marquen.
    const btnRec = 'border:none;border-radius:7px;padding:4px 12px;font-size:11.5px;font-weight:700;cursor:pointer'
    h += `<div style="margin-top:18px" id="eval-section-rec">
      <div style="font-size:12px;font-weight:700;color:var(--ice);background:var(--navy3);padding:7px 14px;border-radius:6px;margin-bottom:6px;display:flex;gap:12px;align-items:center">
        <span>🔁 Recuperación · 2ª convocatoria</span>
        <span style="font-size:11px;font-weight:400;color:var(--text2)">
          No cuenta en la 1ª convocatoria ni en las evaluaciones parciales</span>
      </div>`
    if (actsRecuperacion.length) {
      h += `<table class="prog-table">
        <thead><tr>
          <th>Actividad de recuperación</th>
          <th style="width:88px;text-align:center">Instrumento</th>
          <th class="th-editable" style="width:72px;text-align:center">Nota máx</th>
          <th style="width:62px;text-align:center" title="Criterios que recupera">CEs</th>
          <th style="width:30px"></th>
        </tr></thead><tbody>`
      for (const act of actsRecuperacion) {
        const badge = act.tipo === 'examen'
          ? 'background:rgba(224,160,58,.2);color:var(--amber)'
          : 'background:rgba(74,144,217,.15);color:var(--accent2)'
        const cesAct = actCesLista(act)
        const utIdSafe = (act.ut_id || '').replace(/'/g, "\\'")
        const raIdSafe = (act.ra_id || '').replace(/'/g, "\\'")
        // actCesLista() devuelve las claves ya como cadenas "RA1|CR1": tratarlas
        // como objetos dejaba el modal sin marcar ningún criterio y guardarlo
        // borraba los que ya tenía.
        const cesStr = JSON.stringify(cesAct).replace(/"/g, '&quot;')
        h += `<tr>
          <td><input class="nota-cell" type="text" value="${esc(act.descripcion)}"
                data-actid="${act.id}" data-field="descripcion"
                style="width:100%;text-align:left;font-size:12px"
                onchange="updateActividadDesc(this)"/></td>
          <td style="text-align:center"><span style="font-size:11px;padding:2px 7px;border-radius:8px;${badge}">${esc(act.instrumento)}</span></td>
          <td style="text-align:center"><input class="peso-cell" type="number" min="0" max="10" step="0.5"
                value="${act.nota_max}" data-actid="${act.id}" data-field="nota_max"
                onchange="updateActividadPeso(this)" title="Nota máxima"/></td>
          <td style="text-align:center">
            <button onclick="openActCesModal(${act.id},${mid},'${utIdSafe}','${raIdSafe}',this.dataset.ces,2)"
              data-ces="${cesStr}" title="Criterios que recupera esta actividad"
              style="background:transparent;color:${cesAct.length ? 'var(--green)' : 'var(--amber)'};border:1px solid ${cesAct.length ? 'var(--green)' : 'var(--amber)'};border-radius:6px;padding:2px 7px;font-size:10px;font-weight:700;cursor:pointer;white-space:nowrap">
              ${cesAct.length || '⚠ 0'}
            </button></td>
          <td style="text-align:center">
            <button onclick="deleteActividadRow(${act.id})" title="Eliminar" aria-label="Eliminar actividad de recuperación"
              style="background:transparent;color:#ef4444;border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:2px 6px;font-size:11px;cursor:pointer;line-height:1">✕</button></td>
        </tr>`
      }
      h += `</tbody></table>`
    } else {
      h += `<div class="empty-state" style="margin:0 0 8px">
        <div style="font-weight:700;color:var(--text);margin-bottom:6px">Sin actividades de recuperación</div>
        <div style="margin-bottom:10px">Cuando prepares la prueba de la 2ª convocatoria, dala de alta aquí
          y márcale los criterios que recupera. Su nota entra sola en la 2ª convocatoria.</div>
      </div>`
    }
    h += `<div style="display:flex;gap:8px;padding:8px 2px 2px">
        <button onclick="addActividadRecuperacion(${mid},'examen')"
          style="${btnRec}background:rgba(224,160,58,.12);color:var(--amber)">+ Prueba de recuperación</button>
        <button onclick="addActividadRecuperacion(${mid},'practica')"
          style="${btnRec}background:rgba(74,144,217,.12);color:var(--accent2)">+ Trabajo de recuperación</button>
      </div>
    </div>`
    h += `</div>`
  }

  // ── 2. DISTRIBUCIÓN EVALUACIÓN (RAs por eval) ─────────────────
  // Mismo mapa que el plan de actividades: un RA aparece en una sola evaluación,
  // así las ponderaciones de las tres columnas suman el 100 % del módulo.
  const distRasMap = {}
  for (let e = 1; e <= evalCount; e++) distRasMap[e] = evalRasMap[String(e)] || []

  if (evals.length) {
    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title">📊 Distribución de RAs por Evaluación</div>
      <div style="display:flex;gap:12px;flex-wrap:wrap">`
    for (const ev of evals) {
      const raList = distRasMap[ev] || []
      const totalPond = raList.reduce((s, raId) => s + (raMap[raId]?.pond||0), 0)
      h += `<div style="flex:1;min-width:180px;background:var(--navy3);border-radius:8px;padding:12px 16px">
        <div style="font-size:12px;font-weight:700;color:var(--ice);margin-bottom:8px">${evalLabel(ev)}
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
         // El instrumento se calculaba pero no se pintaba: sin él la tarjeta no
         // decía CON QUÉ se evalúa cada RA, que es justo lo que hay que revisar
         // al programar (un RA sin instrumento no se puede calificar).
         h += `<div style="display:flex;gap:8px;padding:4px 0;border-top:1px solid var(--border);align-items:baseline">
           <span style="font-weight:700;color:var(--accent2);min-width:34px">${esc(raId)}</span>
           <span style="font-size:11px;color:var(--text2);flex:1;line-height:1.3">${esc(ra.nombre||'')}</span>
           <span style="font-size:10px;color:${instrStr ? 'var(--text2)' : 'var(--warn)'}" title="${instrStr ? 'Instrumentos de evaluación' : 'Ningún instrumento evalúa este RA'}">${esc(instrStr || 'sin instrumento')}</span>
           <span class="badge badge-accent">${ra.pond||0}%</span>
         </div>`
      }
      h += `</div>`
    }
    h += `</div></div>`
  }

  // ── 3. TABLA DE UNIDADES DE TRABAJO ──────────────────────────
  // Las UT reparten las horas de AULA. En los ciclos con fase en empresa
  // (Grado Básico) la duración oficial incluye esas horas de empresa, que no
  // se programan en UT: comparar contra ella dejaba el aviso siempre en ámbar.
  const _horasAula = parseInt(data.modulo?.horas_aula, 10) || 0
  const _horasOfi  = parseInt(data.modulo?.total_horas, 10) || mod.horas || 0
  const _sumUtH = uts.reduce((s, u) => s + (parseInt(u.horas, 10) || 0), 0)
  const _modH    = _horasAula || _horasOfi || 0
  const _hOk     = _sumUtH === _modH
  const _hNota   = _horasAula && _horasAula !== _horasOfi ? ' de aula' : ''
  const _hBadgeSt = _hOk
    ? 'background:rgba(16,185,129,.12);color:var(--green)'
    : 'background:rgba(245,158,11,.15);color:var(--amber)'
  h += `<div class="card" style="margin-bottom:16px">
    <div class="prog-section-title" style="display:flex;align-items:center;gap:10px">
      📚 Unidades de Trabajo
      <span id="ut-horas-badge" style="font-size:10.5px;padding:2px 10px;border-radius:8px;font-weight:700;${_hBadgeSt}"
        title="${_hNota ? `${_horasOfi} h de duración oficial, de las que ${_horasAula} son de aula y el resto formación en empresa` : 'Duración del módulo'}">
        Σ ${_sumUtH}h / ${_modH}h${esc(_hNota)}${_hOk?' ✓':' ⚠'}
      </span>
    </div>
    <div style="overflow-x:auto">
    <table class="prog-table">
      <thead><tr>
        <th style="width:56px">UT</th>
        <th style="min-width:180px">Nombre</th>
        <th style="width:82px;text-align:center">Horas</th>
        <th style="width:58px;text-align:center">Eval</th>
        <th style="width:60px;text-align:center">RA</th>
        <th style="min-width:160px">Contenidos clave</th>
        <th style="width:106px;text-align:center">Acciones</th>
      </tr></thead>
      <tbody>`
  for (const ut of uts) {
    const utAsigs = asigs.filter(a => a.ut === ut.id)
    const raIds   = utAsigs.map(a => a.ra)
    const raCellContent = raIds.length
      ? raIds.map(id => `<span style="font-weight:700;color:var(--accent2);display:inline-block">${esc(id)}</span>`).join('<br>')
      : '<span style="color:var(--text2)">—</span>'
    h += `<tr>
      <td style="font-weight:700;color:var(--accent2);white-space:nowrap">${ut.id}</td>
      <td><input class="nota-cell" type="text" value="${esc(ut.nombre)}"
        style="width:100%;min-width:160px;text-align:left;font-weight:500"
        onchange="saveUtField(${mid},'${ut.id}','nombre',this.value)"/></td>
      <td style="text-align:center">
        <input class="peso-cell ut-horas-inp" type="number" min="0" max="999" value="${ut.horas||0}"
          style="width:70px"
          oninput="_refreshUtHoras(this,${_modH},'${_hNota}')"
          onchange="saveUtField(${mid},'${ut.id}','horas',this.value)"/></td>
      <td style="text-align:center">
        <select class="nota-cell" style="width:52px;padding:3px 4px;text-align:center;font-weight:600"
          onchange="saveUtField(${mid},'${ut.id}','eval',this.value)">
          ${evals.map(e=>`<option value="${e}"${ut.eval==e?' selected':''}>${e}</option>`).join('')}
        </select></td>
      <td style="text-align:center;line-height:1.6">${raCellContent}</td>
      <td><input class="nota-cell" type="text" value="${esc(ut.tags||'')}"
        style="width:100%;text-align:left;font-size:11px;color:var(--text2)"
        onchange="saveUtField(${mid},'${ut.id}','tags',this.value)"/></td>
      <td style="text-align:center;white-space:nowrap">
        <button onclick="openUtRasModal(${mid},'${ut.id}')" title="Asignar RAs y CEs"
          style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:3px 9px;font-size:11px;font-weight:700;cursor:pointer;margin-right:4px">RA/CE</button>
        <button onclick="deleteUt(${mid},'${ut.id}')" title="Eliminar UT" aria-label="Eliminar UT"
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

  // ── 4. RESULTADOS DE APRENDIZAJE Y CRITERIOS DE EVALUACIÓN ───
  const totalRaPond = ras.reduce((s, r) => s + (r.pond || 0), 0)
  const raPondOk    = ras.every(r => r.pond) && Math.abs(totalRaPond - 100) < 0.1
  const raSumBadge  = ras.some(r => r.pond)
    ? (raPondOk
        ? `<span data-rapond-total style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700;margin-left:auto">✓ 100%</span>`
        : `<span data-rapond-total style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700;margin-left:auto">⚠ suma ${totalRaPond}%</span>`)
    : ''

  // Cuántos criterios evalúa de verdad alguna actividad. Sin esto, la programación
  // puede tener criterios que nadie califica y no enterarte hasta la reclamación.
  const cobBadge = totalCes
    ? (cesCubiertos === totalCes
        ? `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700"
             title="Cada criterio del decreto está marcado en alguna actividad">✓ los ${totalCes} criterios se evalúan</span>`
        : `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700"
             title="Los criterios sin actividad salen marcados abajo con ○. Asígnalos a una práctica o examen desde la columna CEs del plan.">⚠ ${totalCes - cesCubiertos} criterio${totalCes - cesCubiertos > 1 ? 's' : ''} sin actividad que los evalúe</span>`)
    : ''

  h += `<div class="card" style="margin-bottom:16px">
    <div class="prog-section-title" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">🎯 Resultados de Aprendizaje y Criterios de Evaluación
      ${cobBadge}
      ${raSumBadge}
    </div>
    <div style="display:flex;flex-direction:column;gap:10px">`

  for (const ra of ras) {
    const raCes = ces[ra.id] || []
    // En qué evaluación cae este RA (mismo mapa que las secciones de arriba)
    const raEval = evalDeRa[ra.id] ? `Eval ${evalDeRa[ra.id]}` : 'Sin evaluación'
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

    // RA que hay que tener alcanzado para incorporarse a la fase de empresa
    // (Orden 201/2024, art. 4.3.a). La programación debe especificarlos.
    const llaveChk = `<label title="Marca los RA que el alumnado debe tener alcanzados para incorporarse a la fase de formación en empresa (Orden 201/2024, art. 4.3.a)"
        style="display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--text2);cursor:pointer;white-space:nowrap">
      <input type="checkbox" ${ra.llave ? 'checked' : ''}
        onchange="updateRaLlave(${mid},'${esc(ra.id)}',this.checked)"
        style="accent-color:var(--accent);width:13px;height:13px"/>
      🔑 para empresa
    </label>`

    h += `<div style="border:1px solid var(--border);border-left:4px solid var(--accent2);border-radius:8px;overflow:hidden">
      <div style="background:var(--bg3);padding:10px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
         <span style="font-size:13px;font-weight:800;color:var(--accent2);min-width:38px">${esc(ra.id)}</span>
         <span style="font-size:13px;font-weight:600;flex:1">${esc(ra.nombre)}</span>
         ${llaveChk}
         ${pondInput}
         <span class="badge">${raEval}</span>
         ${utAsigs.length ? `<span class="badge">${esc(utAsigs.join(', '))}</span>` : ''}
         ${instrStr ? `<span class="badge badge-green">${esc(instrStr)}</span>` : ''}
       </div>`

     if (raCes.length) {
       h += `<div style="padding:8px 16px 10px 16px">
         <table style="width:100%;border-collapse:collapse">`
       for (const ce of raCes) {
         // Dónde se evalúa este criterio: verde con el listado, o hueco si nadie lo evalúa
         const donde = coberturaCe[ceKey(ra.id, ce.id)] || []
         const marca = donde.length
           ? `<span title="Se evalúa en: ${esc(donde.join(' · '))}" style="color:var(--green);font-size:11px">●</span>`
           : `<span title="Ningún examen ni práctica evalúa este criterio todavía" style="color:var(--amber);font-size:11px">○</span>`
         // Ponderación del criterio dentro del RA (Orden 201/2024, art. 4.3.a).
         // En blanco = todos los criterios del RA valen lo mismo.
         const pesoCe = `<input class="peso-cell" type="number" min="0" max="100" step="1"
             value="${ce.peso != null && ce.peso !== '' ? ce.peso : ''}" placeholder="—"
             data-mid="${mid}" data-raid="${esc(ra.id)}" data-ceid="${esc(ce.id)}"
             onchange="updateCePeso(this)"
             title="Peso de este criterio dentro del RA. En blanco, todos los criterios pesan igual."
             style="width:52px;font-size:11px"/>`
         h += `<tr style="border-top:1px solid var(--border)">
           <td style="padding:4px 6px 4px 0;text-align:center;vertical-align:top;width:16px">${marca}</td>
           <td style="padding:4px 10px 4px 0;font-size:12px;font-weight:700;color:var(--accent);white-space:nowrap;vertical-align:top">${esc(ce.id)}</td>
           <td style="padding:4px 0;font-size:12px;color:var(--text2);line-height:1.5">${esc(ce.texto)}</td>
           <td style="padding:4px 0 4px 8px;text-align:right;vertical-align:top;white-space:nowrap">${pesoCe}<span style="font-size:10px;color:var(--text3)">%</span></td>
         </tr>`
       }
       h += `</table></div>`
     }
     h += `</div>`
  }
  h += `</div></div>`

  // ── 5. MAPA DE ASIGNACIONES UT → RA → CEs ────────────────────
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
    const asigsSorted = asigs.slice().sort((x, y) => {
      const nx = parseInt(x.ut.replace(/\D/g, ''), 10) || 0
      const ny = parseInt(y.ut.replace(/\D/g, ''), 10) || 0
      return nx - ny
    })
    for (const a of asigsSorted) {
      const ut = utMap[a.ut] || {}
      const ceList = (ces[a.ra] || []).filter(ce => a.ces.includes(ce.id))
       h += `<tr>
         <td style="font-weight:700;color:var(--accent2);vertical-align:top;padding-top:8px">${esc(a.ut)}</td>
         <td style="font-size:11px;color:var(--text2);vertical-align:top;padding-top:8px;line-height:1.4">${esc(ut.nombre||'')}</td>
         <td style="text-align:center;font-weight:700;color:var(--accent2);vertical-align:top;padding-top:8px">${esc(a.ra)}</td>
         <td style="padding:4px 0">${ceList.map(ce =>
           `<div style="display:flex;gap:6px;padding:3px 0;border-top:1px solid var(--border);font-size:11px">
             <span style="color:var(--accent);font-weight:700;white-space:nowrap">${esc(ce.id)}</span>
             <span style="color:var(--text2)">${esc(ce.texto)}</span>
           </div>`
         ).join('')}</td>
       </tr>`
    }
    h += `</tbody></table></div></div>`
  }

  panel.innerHTML = h
}

// PONDERACIONES DE RAs
// ═══════════════════════════════════════════════════════════════
async function updateRaPond(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  if (!mid || !raId) return

  // Vaciar la casilla es legítimo: significa «este RA aún no está ponderado».
  const vacio = String(el.value).trim() === ''
  const pond  = vacio ? 0 : parseFloat(el.value)

  if (!vacio && !validators.ponderacion(pond)) {
    alert('Ponderación inválida. Debe estar entre 0 y 100.')
    el.value = ''
    _refreshRaPondTotal(el)
    return
  }

  clearTimeout(_raPondTimers[mid + raId])
  _raPondTimers[mid + raId] = setTimeout(async () => {
    try {
      await window.api.setRaPonderacion(mid, raId, pond)
      showSaved()
    } catch(e) {
      alert('Error guardando ponderación: ' + validators.sanitizeErrorMessage(e, 'updateRaPond'))
      console.error(e)
    }
  }, 350)
}

/**
 * Peso de un criterio dentro de su RA (Orden 201/2024, art. 4.3.a: la
 * programación debe recoger los RA y sus criterios «con la ponderación
 * establecida para cada uno de ellos»).
 * Vacío = reparto a partes iguales, que es lo que hacía la aplicación antes.
 */
async function updateCePeso(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const ceId = el.dataset.ceid
  if (!mid || !raId || !ceId) return
  const vacio = String(el.value).trim() === ''
  const peso  = vacio ? null : parseFloat(el.value)
  if (!vacio && (isNaN(peso) || peso < 0 || peso > 100)) {
    alert('Peso inválido. Debe estar entre 0 y 100.')
    el.value = ''
    return
  }
  const data = _getModData(mid)
  if (!data) return
  const ce = (data.ces?.[raId] || []).find(c => c.id === ceId)
  if (!ce) return
  if (vacio) delete ce.peso
  else ce.peso = peso
  await _saveModData(mid, data, false)

  // Aviso si los criterios de ese RA no suman 100: se sigue guardando, pero
  // mientras no cuadren el motor reparte a partes iguales.
  const lista = data.ces[raId] || []
  const conPeso = lista.filter(c => c.peso != null && c.peso !== '')
  if (conPeso.length && conPeso.length === lista.length) {
    const suma = conPeso.reduce((s, c) => s + Number(c.peso), 0)
    if (Math.abs(suma - 100) > 0.1) {
      showToast(`Los criterios de ${raId} suman ${Math.round(suma * 10) / 10}%: hasta que sumen 100 pesan todos igual`)
    }
  } else if (conPeso.length) {
    showToast(`${raId}: faltan ${lista.length - conPeso.length} criterios por ponderar`)
  }
}

/**
 * Marca un RA como necesario para incorporarse a la fase de formación en
 * empresa (Orden 201/2024, art. 4.3.a). El asistente de IA ya sabía usarlo, pero
 * no había ninguna pantalla donde indicarlo.
 */
async function updateRaLlave(mid, raId, esLlave) {
  const data = _getModData(mid)
  if (!data) return
  const ra = (data.ras || []).find(r => r.id === raId)
  if (!ra) return
  if (esLlave) ra.llave = true
  else delete ra.llave
  await _saveModData(mid, data, false)
  showToast(esLlave
    ? `${raId} marcado como necesario para la fase de empresa`
    : `${raId} ya no condiciona la fase de empresa`)
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

  if (isNaN(val)) return

  // Validate peso (0-100%)
  if (!validators.numberRange(val, 0, 100)) {
    alert('Peso inválido. Debe estar entre 0 y 100.')
    el.value = ''
    return
  }

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

      // Validate complete actividad object
      act[field] = val
      if (!validators.actividad(act)) {
        alert('Datos de actividad inválidos.')
        return
      }

      await window.api.saveActividad(act)
      showSaved()
      _refreshPesoTotal(el)
    } catch(e) {
      alert('Error guardando actividad: ' + validators.sanitizeErrorMessage(e, 'updateActividadPeso'))
      console.error(e)
    }
  }, 350)
}

async function updateActividadDesc(el) {
  const actId = parseInt(el.dataset.actid)
  if (!actId) return

  // Validate description
  if (!validators.description(el.value)) {
    alert('Descripción inválida. Máximo 500 caracteres.')
    el.value = ''
    return
  }

  const mid = parseInt(document.getElementById('prog-mod-sel')?.value || document.getElementById('eval-mod-sel')?.value || 0)
  if (!mid) return
  clearTimeout(_pesoTimers['desc' + actId])
  _pesoTimers['desc' + actId] = setTimeout(async () => {
    try {
      const acts = await window.api.getActividades(mid)
      const act  = acts.find(a => a.id === actId)
      if (!act) return
      act.descripcion = el.value

      // Validate complete actividad object
      if (!validators.actividad(act)) {
        alert('Datos de actividad inválidos.')
        return
      }

       await window.api.saveActividad(act)
       showSaved()
     } catch(e) {
       alert('Error guardando descripción: ' + validators.sanitizeErrorMessage(e, 'updateActividadDesc'))
       console.error(e)
     }
  }, 400)
}

/**
 * Reasigna las UT de una actividad dejándola coherente:
 *  · ra_id pasa a ser el RA de esas UT (o se vacía si son varios, porque entonces
 *    quien manda son los criterios marcados);
 *  · los criterios que ya no pertenecen a ninguna de las UT nuevas se caen, en vez
 *    de quedarse ahí calificando un RA que la actividad ya no toca.
 * Devuelve cuántos criterios se han descartado.
 */
function _reasignarUtsActividad(act, utIds, data) {
  act.ut_id = utIds.join(',')
  const asigs = data?.asignaciones || []
  const ras   = rasDeActividad({ ut_id: act.ut_id }, asigs)
  act.ra_id   = ras.length === 1 ? ras[0] : null

  const grupos    = cesDisponiblesActividad(act, asigs, data?.ces || {})
  const validas   = new Set()
  grupos.forEach(g => g.ces.forEach(ce => validas.add(ceKey(g.raId, ce.id))))
  const antes     = actCesLista(act)
  const migradas  = migrarCesActividad({ ...act, ces: antes }, asigs, data?.ces || {}) || antes
  const conservar = migradas.filter(k => validas.has(k))
  act.ces = conservar
  return migradas.length - conservar.length
}

async function updateActividadUT(el) {
  const actId = parseInt(el.dataset.actid)
  if (!actId) return
  // Vale tanto para el desplegable simple (práctica) como para varias UT (examen)
  const selected = Array.from(el.selectedOptions).map(o => o.value).filter(Boolean)
  const mid = parseInt(document.getElementById('prog-mod-sel')?.value || document.getElementById('eval-mod-sel')?.value || 0)
  if (!mid) return
  try {
    const acts = await window.api.getActividades(mid)
    const act = acts.find(a => a.id === actId)
    if (!act) return
    const perdidos = _reasignarUtsActividad(act, selected, _getModData(mid))
    await window.api.saveActividad(act)
    showSaved()
    if (perdidos) loadProgramacion()   // el contador de criterios ha cambiado
  } catch(e) { console.error('updateActividadUT:', e) }
}

function actDragStart(event) {
  const tr = event.currentTarget
  if (!tr.dataset.actid) { event.preventDefault(); return }
  event.dataTransfer.setData('text/plain', JSON.stringify({
    actId: tr.dataset.actid,
    fromEval: tr.dataset.fromeval
  }))
  event.dataTransfer.effectAllowed = 'move'
  tr.classList.add('drag-ghost')
  setTimeout(() => tr.classList.remove('drag-ghost'), 0)
}

function actDragOver(event) {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
  event.currentTarget.style.outline = '2px dashed var(--accent2)'
  event.currentTarget.style.borderRadius = '8px'
}

function actDragLeave(event) {
  // Solo quitar el borde cuando el ratón sale del div entero, no de elementos hijo
  if (event.currentTarget.contains(event.relatedTarget)) return
  event.currentTarget.style.outline = ''
}

function actDragEnd() {
  // Limpiar todos los bordes si el drag termina fuera de cualquier zona
  document.querySelectorAll('[id^="eval-section-"]').forEach(el => {
    el.style.outline = ''
  })
}

async function actDrop(event, toEval) {
  event.preventDefault()
  const div = event.currentTarget
  div.style.outline = ''
  let payload
  try { payload = JSON.parse(event.dataTransfer.getData('text/plain')) } catch { return }
  const { actId, fromEval } = payload
  if (parseInt(fromEval) === toEval) return
  const mid = parseInt(document.getElementById('prog-mod-sel')?.value || document.getElementById('eval-mod-sel')?.value || 0)
  if (!mid) return
  try {
    const acts = await window.api.getActividades(mid)
    const act = acts.find(a => a.id === parseInt(actId))
    if (!act) return
    act.eval = toEval
    await window.api.saveActividad(act)
    loadProgramacion()
  } catch(e) { console.error('actDrop:', e) }
}

/**
 * Cambia el número de evaluaciones del módulo y reparte unidades, RA y
 * actividades. Antes lo hacía sin preguntar: con el curso empezado, mover una
 * actividad de trimestre cambia el boletín de la evaluación, así que ahora se
 * enseña primero el reparto que va a quedar.
 */
async function setEvalCount(mid, count) {
  const newCount  = parseInt(count)
  const data      = _getModData(mid)
  if (!data) return

  const actsPrev = await window.api.getActividades(parseInt(mid))
  const utsPrev  = data.uts || []
  const anterior = data.modulo?.eval_count || [...new Set(utsPrev.map(u => u.eval || 1))].length || 3
  if (newCount === anterior) return

  // Simular el reparto para poder contarlo antes de tocar nada
  const simulaUt = (() => {
    const orden = utsPrev.slice().sort((a, b) => (a.eval||1)-(b.eval||1) || (a.orden||0)-(b.orden||0))
    const porEval = Math.ceil(orden.length / newCount) || 1
    return orden.filter((u, i) => (u.eval || 1) !== Math.min(Math.floor(i / porEval) + 1, newCount)).length
  })()
  const simulaAct = (() => {
    const orden = actsPrev.slice().sort((a, b) => (a.eval||1)-(b.eval||1) || (a.orden||0)-(b.orden||0))
    const porEval = Math.ceil(orden.length / newCount) || 1
    return orden.filter((a, i) => (a.eval || 1) !== Math.min(Math.floor(i / porEval) + 1, newCount)).length
  })()

  const conNotas = (() => {
    try { return actsPrev.filter(a => a.peso > 0).length } catch { return 0 }
  })()
  if (!confirm(
    `Vas a pasar de ${anterior} a ${newCount} evaluaciones.\n\n` +
    `Se repartirán de nuevo, por orden:\n` +
    `  · ${simulaUt} unidad(es) de trabajo cambian de evaluación\n` +
    `  · ${simulaAct} actividad(es) cambian de evaluación\n` +
    `  · los RA siguen a sus unidades\n\n` +
    (conNotas ? 'Si ya has puesto notas, sus actividades pueden acabar en otro trimestre y los boletines por evaluación cambiarán.\n\n' : '') +
    '¿Continuar?')) {
    loadProgramacion()   // devolver el desplegable a su valor
    return
  }
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

  // ── Recalcular eval_ras ───────────────────────────────────────
  // Los RA siguen a sus UT: se recalcula desde el reparto que se acaba de hacer,
  // en vez de repartirlos por su cuenta y acabar diciendo dos cosas distintas.
  data.eval_ras = rasPorEvaluacion(data, newCount)

  // ── Redistribuir Actividades (en BD) ─────────────────────────
  // Siempre redistribuye proporcionalmente por eval+orden: ninguna actividad se pierde
  const acts = actsPrev
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
    ? `${instrumento} ${sameType.length + 1} — ${evalLabel(ev)}`
    : `${instrumento} — ${evalLabel(ev)}`
  await window.api.saveActividad({
    modulo_id: parseInt(mid), ut_id: null, ra_id: null,
    descripcion: desc, instrumento, tipo,
    peso: 0, nota_max: 10, eval: ev, orden: maxOrden + 1
  })
  showSaved()
  loadProgramacion()
}

/**
 * Alta de una actividad de la 2ª convocatoria (art. 21.5).
 *
 * Peso 0 a propósito: no compite con las actividades del curso por el 100 % de
 * una evaluación. En la 2ª convocatoria lo que hace es acreditar criterios, y la
 * nota de cada criterio es la mejor entre la del curso y la de la recuperación.
 */
async function addActividadRecuperacion(mid, tipo) {
  const instrumento = tipo === 'examen' ? 'Examen' : 'Práctica'
  const allActs = await window.api.getActividades(parseInt(mid))
  const recs = allActs.filter(a => Number(a.convocatoria) === 2)
  const maxOrden = allActs.reduce((m, a) => Math.max(m, a.orden || 0), 0)
  const desc = recs.length
    ? `${instrumento} de recuperación ${recs.length + 1}`
    : `${instrumento} de recuperación — 2ª convocatoria`
  await window.api.saveActividad({
    modulo_id: parseInt(mid), ut_id: null, ra_id: null,
    descripcion: desc, instrumento, tipo,
    peso: 0, nota_max: 10, eval: 1, orden: maxOrden + 1, convocatoria: 2,
  })
  showSaved()
  loadProgramacion()
}

async function deleteActividadRow(actId) {
  // Borrar una actividad se lleva por delante sus calificaciones (cascada en la
  // base de datos). Hay que decirlo ANTES, no después: es irreversible salvo
  // restaurando una copia de seguridad.
  const mid = parseInt(document.getElementById('prog-mod-sel')?.value || 0)
  let conNota = 0
  try {
    const notas = await window.api.getNotasGrid(mid)
    conNota = notas.filter(n => n.actividad_id === actId &&
                                (n.nota != null || n.nota_rec != null)).length
  } catch { /* si no se puede contar, se avisa igual en genérico */ }
  const aviso = conNota
    ? `\n\nTiene ${conNota} calificación${conNota > 1 ? 'es' : ''} puesta${conNota > 1 ? 's' : ''}, que se perderá${conNota > 1 ? 'n' : ''}.`
    : ''
  if (!confirm(`¿Eliminar esta actividad?${aviso}`)) return
  await window.api.deleteActividad(actId)
  showToast(conNota ? `Actividad eliminada · ${conNota} calificaciones borradas` : 'Actividad eliminada')
  loadProgramacion()
}

function _refreshPesoTotal(changedInput) {
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

/** ¿Dos repartos de RA por evaluación dicen lo mismo? */
function _mismoEvalRas(a, b, evalCount) {
  for (let e = 1; e <= evalCount; e++) {
    const x = [...(a?.[String(e)] || [])].sort()
    const y = [...(b?.[String(e)] || b?.[e] || [])].sort()
    if (x.length !== y.length || x.some((v, i) => v !== y[i])) return false
  }
  for (const k of Object.keys(b || {})) {
    if ((parseInt(k, 10) || 0) > evalCount && (b[k] || []).length) return false
  }
  return true
}

/**
 * Deja escrito en el módulo el reparto de RA por evaluación que sale de las UT.
 * Evaluaciones, Dashboard y los informes de IA leen `eval_ras`; si el profesor
 * mueve una UT de trimestre y no se actualiza, cada pantalla cuenta una cosa.
 */
async function _sincronizarEvalRas(mid, evalCount) {
  const data = _getModData(mid)
  if (!data) return false
  const nuevo = rasPorEvaluacion(data, evalCount)
  if (_mismoEvalRas(nuevo, data.eval_ras, evalCount)) return false
  data.eval_ras = nuevo
  await window.api.setModuloDataJson(parseInt(mid), data)
  _modulos = await window.api.getModulos()
  return true
}

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
  // Siguiente número LIBRE: evita IDs duplicados si se borró una UT intermedia
  const usados = new Set((data.uts||[]).map(u => u.id))
  let n = (data.uts?.length || 0) + 1
  while (usados.has(`UT${n}`)) n++
  data.uts = [...(data.uts||[]), {id:`UT${n}`, nombre:'Nueva unidad de trabajo', horas:0, eval:1, tags:''}]
  await _saveModData(mid, data, true)
}

async function deleteUt(mid, utId) {
  const acts = await window.api.getActividades(parseInt(mid))
  const afectadas = acts.filter(a =>
    String(a.ut_id||'').split(',').map(s => s.trim()).includes(utId))
  const aviso = afectadas.length
    ? `\n\n${afectadas.length} actividad${afectadas.length > 1 ? 'es la tienen' : ' la tiene'} asignada y se ` +
      `quedará${afectadas.length > 1 ? 'n' : ''} sin esa unidad y sin sus criterios.`
    : ''
  if (!confirm(`¿Eliminar ${utId} del módulo?${aviso}`)) return
  const data = _getModData(mid)
  if (!data) return
  data.uts          = (data.uts||[]).filter(u => u.id !== utId)
  data.asignaciones = (data.asignaciones||[]).filter(a => a.ut !== utId)
  await _revisarActividadesDeUts(mid, data, [utId])
  await _saveModData(mid, data, true)
}

/**
 * Repasa las actividades que usan estas UT después de tocar sus RA/CE: quita los
 * criterios que ya no les corresponden y recoloca el RA. Si no, una actividad se
 * queda calificando criterios que su unidad ya no trabaja.
 */
async function _revisarActividadesDeUts(mid, data, utIds) {
  const acts = await window.api.getActividades(parseInt(mid))
  let perdidos = 0
  for (const act of acts) {
    const suyas = String(act.ut_id||'').split(',').map(s => s.trim()).filter(Boolean)
    if (!suyas.some(u => utIds.includes(u))) continue
    const quedan = suyas.filter(u => (data.uts||[]).some(x => x.id === u))
    perdidos += _reasignarUtsActividad(act, quedan, data)
    await window.api.saveActividad(act)
  }
  return perdidos
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
    // Se muestra EXACTAMENTE lo guardado: si el RA está asignado sin criterios,
    // las casillas salen vacías. (Antes se marcaban todas y al volver a guardar
    // la UT se quedaba con criterios que nadie había elegido.)
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
            ${checked && selCEs.includes(ce.id) ? 'checked' : ''}
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
  document.getElementById('modal-ut-ras').showModal()
}

function _refreshUtHoras(inp, modHoras, nota) {
  const table  = inp.closest('table')
  if (!table) return
  const suma   = Array.from(table.querySelectorAll('.ut-horas-inp')).reduce((s,i) => s+(parseInt(i.value)||0), 0)
  const badge  = document.getElementById('ut-horas-badge')
  if (!badge) return
  const ok = suma === modHoras
  badge.textContent  = `Σ ${suma}h / ${modHoras}h${nota||''}${ok?' ✓':' ⚠'}`
  badge.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(245,158,11,.15)'
  badge.style.color      = ok ? 'var(--green)'         : 'var(--amber)'
}

function _toggleRaSection(raId, checked) {
  const block = document.getElementById(`ces-block-${raId}`)
  if (!block) return
  block.style.display = checked ? 'grid' : 'none'
  const cajas = Array.from(block.querySelectorAll('input[type="checkbox"]'))
  // Al marcar un RA se proponen todos sus criterios, pero solo si no había
  // ninguno elegido: así desmarcar y volver a marcar no borra tu selección.
  if (checked && !cajas.some(cb => cb.checked)) cajas.forEach(cb => { cb.checked = true })
}

async function saveUtRas() {
  if (!_utRasState) return
  const {mid, data, utId} = _utRasState
  const nuevas = []
  const sinCriterios = []
  document.querySelectorAll('.ut-ra-chk:checked').forEach(raChk => {
    const raId = raChk.dataset.ra
    const ces  = Array.from(document.querySelectorAll(`.ut-ce-chk[data-ra="${raId}"]:checked`)).map(cb=>cb.dataset.ce)
    if (!ces.length) sinCriterios.push(raId)
    nuevas.push({ut: utId, ra: raId, ces})
  })
  // Un RA marcado sin ningún criterio no evalúa nada: se avisa antes de guardar.
  if (sinCriterios.length && !confirm(
    `${sinCriterios.join(', ')} ${sinCriterios.length > 1 ? 'quedan' : 'queda'} en ${utId} sin ningún criterio marcado, ` +
    'así que esa unidad no evaluará nada de ese resultado de aprendizaje.\n\n¿Guardar de todos modos?')) return

  data.asignaciones = (data.asignaciones||[]).filter(a => a.ut !== utId).concat(nuevas)
  const perdidos = await _revisarActividadesDeUts(mid, data, [utId])
  await _saveModData(mid, data, true)
  closeUtRasModal()
  if (perdidos) {
    showToast(`Se ${perdidos > 1 ? 'han quitado' : 'ha quitado'} ${perdidos} criterio${perdidos > 1 ? 's' : ''} de actividades de ${utId}`)
  }
}

function closeUtRasModal() {
  const dlg = document.getElementById('modal-ut-ras')
  if (dlg.open) dlg.close()
  _utRasState = null
}

// ── Modal UT para actividades de examen ──────────────────────────
let _actUtsState = null

function openActUtsModal(actId, mid, currentUtId) {
  const data = _getModData(mid)
  if (!data) return
  _actUtsState = { actId, mid }

  // Título: descripción de la actividad si está disponible
  document.getElementById('act-uts-title').textContent = `Examen · UTs relacionadas`

  const selIds = (currentUtId||'').split(',').filter(Boolean)
  const uts = data.uts || []
  const evals = [...new Set(uts.map(u => u.eval||1))].sort((a,b)=>a-b)

  let html = ''
  for (const ev of evals) {
    const evUts = uts.filter(u => (u.eval||1) === ev)
    if (!evUts.length) continue
    html += `<div style="margin-bottom:14px">
      <div style="font-size:10.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.6px;margin-bottom:6px">${evalLabel(ev)}</div>`
    for (const ut of evUts) {
      const checked = selIds.includes(ut.id)
      // Todos los RA que trabaja la UT, no solo el primero
      const raIds = (data.asignaciones||[]).filter(a => a.ut === ut.id).map(a => a.ra)
      const raLabel = raIds.map(raId =>
        `<span style="font-size:10px;font-weight:700;color:var(--accent2);background:rgba(74,144,217,.1);padding:1px 5px;border-radius:4px;margin-left:4px">${esc(raId)}</span>`
      ).join('')
      html += `<label style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:8px 12px;background:var(--bg3);border-radius:8px;border:1px solid var(--border);margin-bottom:5px">
        <input type="checkbox" data-utid="${ut.id}" class="act-ut-chk" ${checked?'checked':''}
          style="accent-color:var(--accent);width:14px;height:14px;flex-shrink:0"/>
        <span style="font-weight:700;color:var(--accent2);min-width:36px;font-size:12px">${esc(ut.id)}</span>
        <span style="font-size:12px;color:var(--text);flex:1">${esc(ut.nombre||'')}</span>
        ${raLabel}
        <span style="font-size:11px;color:var(--text3);white-space:nowrap">${ut.horas||0}h</span>
      </label>`
    }
    html += `</div>`
  }

  document.getElementById('act-uts-body').innerHTML = html ||
    '<p style="color:var(--text2);font-size:13px">Este módulo no tiene UTs definidas.</p>'
  document.getElementById('modal-act-uts').showModal()
}

async function saveActUts() {
  if (!_actUtsState) return
  const { actId, mid } = _actUtsState
  const selected = Array.from(document.querySelectorAll('.act-ut-chk:checked')).map(cb => cb.dataset.utid)
  try {
    const acts = await window.api.getActividades(mid)
    const act = acts.find(a => a.id === actId)
    if (!act) return
    const perdidos = _reasignarUtsActividad(act, selected, _getModData(mid))
    await window.api.saveActividad(act)
    closeActUtsModal()
    if (perdidos) {
      showToast(`Se han quitado ${perdidos} criterio${perdidos > 1 ? 's' : ''} que ya no pertenecen a estas UT`)
    }
    loadProgramacion()
  } catch(e) { console.error('saveActUts:', e) }
}

function closeActUtsModal() {
  const dlg = document.getElementById('modal-act-uts')
  if (dlg.open) dlg.close()
  _actUtsState = null
}

// ═══════════════════════════════════════════════════════════════
// CRITERIOS DE EVALUACIÓN POR ACTIVIDAD
// ═══════════════════════════════════════════════════════════════
let _actCesState = null

function openActCesModal(actId, mid, utId, raId, currentCesEncoded, convocatoria) {
  const data = _getModData(mid)
  if (!data) return
  _actCesState = { actId, mid }

  let selCes = []
  try { selCes = JSON.parse(currentCesEncoded || '[]') } catch { /* ces inválido */ }

  const esRecuperacion = Number(convocatoria) === 2
  document.getElementById('act-ces-title').textContent = esRecuperacion
    ? 'Recuperación — criterios que acredita'
    : `${utId || raId} — Criterios de evaluación`

  // CEs disponibles: los que cubren las UT de esta actividad (una o varias, caso
  // examen), agrupados por RA. Sin UT, los del RA de la actividad.
  //
  // Una prueba de recuperación no cuelga de ninguna unidad de trabajo: recupera
  // lo que haga falta, así que se ofrece el módulo entero.
  const grupos = esRecuperacion
    ? (data.ras || [])
        .map(ra => ({ raId: ra.id, ces: (data.ces || {})[ra.id] || [] }))
        .filter(g => g.ces.length)
    : cesDisponiblesActividad(
        { ut_id: utId, ra_id: raId }, data.asignaciones || [], data.ces || {}
      )

  if (!grupos.length) {
    document.getElementById('act-ces-body').innerHTML =
      '<p style="color:var(--text2);font-size:13px">No hay CEs disponibles para esta actividad. Asigna la UT y los CEs en la programación primero.</p>'
    document.getElementById('modal-act-ces').showModal()
    return
  }

  let html = `<div style="font-size:11px;color:var(--text3);margin-bottom:10px">
    Marca los criterios que evalúa esta actividad. La nota de cada RA se calcula como media de sus CEs cubiertos.
  </div>`

  // Ojo: CR1 existe en todos los RA. Cada casilla guarda la clave RA|CE, de forma
  // que marcar el CR1 de RA4 no marca de rebote el CR1 de RA5.
  for (const grupo of grupos) {
    const raNombre = (data.ras || []).find(r => r.id === grupo.raId)?.nombre || ''
    // Marcar 27 criterios de uno en uno es la tarea más repetitiva de la
    // programación, y dejarla a medias es lo que hace que una actividad no
    // evalúe nada. Un atajo por RA evita justamente eso.
    html += `<div style="display:flex;align-items:baseline;gap:8px;margin:10px 0 5px;flex-wrap:wrap">
      <span style="font-size:10.5px;font-weight:700;color:var(--accent2);text-transform:uppercase;letter-spacing:.5px">
        ${esc(grupo.raId)}${raNombre ? ` <span style="font-weight:400;text-transform:none;letter-spacing:0;color:var(--text3)">· ${esc(raNombre)}</span>` : ''}
      </span>
      <button type="button" onclick="_marcarCesDeRa('${String(grupo.raId).replace(/'/g, "\\'")}', true)"
        style="background:transparent;border:1px solid var(--border2);border-radius:6px;padding:1px 8px;font-size:10px;color:var(--accent);cursor:pointer">todos</button>
      <button type="button" onclick="_marcarCesDeRa('${String(grupo.raId).replace(/'/g, "\\'")}', false)"
        style="background:transparent;border:1px solid var(--border2);border-radius:6px;padding:1px 8px;font-size:10px;color:var(--text3);cursor:pointer">ninguno</button>
    </div>`
    for (const ce of grupo.ces) {
      const clave = ceKey(grupo.raId, ce.id)
      const checked = selCes.includes(clave) ||
        (selCes.includes(ce.id) && grupos.length === 1)   // selección antigua, sin RA
      html += `<label style="display:flex;align-items:flex-start;gap:8px;cursor:pointer;padding:8px 12px;background:var(--bg3);border-radius:8px;border:1px solid var(--border);margin-bottom:5px">
        <input type="checkbox" data-cekey="${esc(clave)}" class="act-ce-chk" ${checked ? 'checked' : ''}
          style="accent-color:var(--accent);width:14px;height:14px;flex-shrink:0;margin-top:2px"/>
        <span style="font-size:11.5px;font-weight:700;color:var(--accent);white-space:nowrap;min-width:28px">${esc(ce.id)}</span>
        <span style="font-size:11.5px;color:var(--text);line-height:1.5">${esc(ce.texto)}</span>
      </label>`
    }
  }

  document.getElementById('act-ces-body').innerHTML = html
  document.getElementById('modal-act-ces').showModal()
}

/** Marca o desmarca de golpe los criterios de un RA en el modal abierto. */
function _marcarCesDeRa(raId, marcar) {
  document.querySelectorAll('.act-ce-chk').forEach(chk => {
    if (String(chk.dataset.cekey || '').split('|')[0] === String(raId)) chk.checked = !!marcar
  })
}

async function saveActCes() {
  if (!_actCesState) return
  const { actId, mid } = _actCesState
  const selected = Array.from(document.querySelectorAll('.act-ce-chk:checked')).map(cb => cb.dataset.cekey)
  try {
    const acts = await window.api.getActividades(mid)
    const act = acts.find(a => a.id === actId)
    if (!act) return
    act.ces = selected
    await window.api.saveActividad(act)
    closeActCesModal()
    loadProgramacion()
  } catch(e) { console.error('saveActCes:', e) }
}

function closeActCesModal() {
  const dlg = document.getElementById('modal-act-ces')
  if (dlg?.open) dlg.close()
  _actCesState = null
}

/**
 * Marca en cada actividad los criterios que su unidad de trabajo tiene asignados
 * en el decreto. Es el atajo para no ir criterio a criterio en un módulo recién
 * dado de alta; después se quitan los que ese instrumento no evalúe.
 * No toca las actividades que ya tengan criterios: la decisión del profesor manda.
 */
async function rellenarCesDesdeUts(mid) {
  const data = _getModData(mid)
  if (!data) return
  const asigs    = data.asignaciones || []
  const cesPorRa = data.ces || {}
  const acts = await window.api.getActividades(parseInt(mid))

  // Un examen sin UT no cubre ningún criterio, así que su nota no entra en
  // ningún RA por mucho que se califique. Antes se quedaba fuera de este arreglo
  // («no tiene UT asignada y se queda igual») justo cuando era el que más falta
  // hacía: se le asignan las unidades de su propia evaluación.
  const utsPorEval = {}
  for (const ut of (data.uts || [])) {
    const ev = Number(ut.eval || 1)
    if (!utsPorEval[ev]) utsPorEval[ev] = []
    utsPorEval[ev].push(ut.id)
  }
  const utAsignada = []

  const candidatas = [], yaTenian = [], sinUt = []
  for (let act of acts) {
    // Las pruebas de recuperación no cuelgan de ninguna UT: sus criterios los
    // elige el profesorado a mano, según lo que cada alumno tenga pendiente.
    if (Number(act.convocatoria) === 2) continue
    if (!String(act.ut_id || '').trim() && !String(act.ra_id || '').trim()) {
      const utsEv = utsPorEval[Number(act.eval || 1)] || []
      if (utsEv.length) {
        act = { ...act, ut_id: utsEv.join(',') }
        utAsignada.push(act)
      }
    }
    const grupos = cesDisponiblesActividad(act, asigs, cesPorRa)
    if (!grupos.length) { sinUt.push(act); continue }
    const tiene = grupos.some(g => g.ces.some(ce => actCubreCe(act, g.raId, ce.id)))
    if (tiene) { yaTenian.push(act); continue }
    candidatas.push({ act, claves: grupos.flatMap(g => g.ces.map(ce => ceKey(g.raId, ce.id))) })
  }

  if (!candidatas.length) {
    alert(yaTenian.length && !sinUt.length
      ? 'Todas las actividades tienen ya sus criterios marcados.'
      : `No hay ninguna actividad a la que rellenar:\n\n` +
        `${yaTenian.length} ya tienen criterios.\n` +
        `${sinUt.length} no tienen unidad de trabajo asignada — ponles la UT primero y vuelve a intentarlo.`)
    return
  }

  const detalle = candidatas
    .map(c => `  · ${c.act.descripcion || c.act.instrumento}  →  ${c.claves.length} criterios`)
    .join('\n')
  const avisos = [
    utAsignada.length ? `A ${utAsignada.length} actividad(es) sin unidad se les asignan las de su evaluación.` : '',
    yaTenian.length ? `${yaTenian.length} actividad(es) ya tienen criterios y no se tocan.` : '',
    sinUt.length ? `${sinUt.length} no tienen UT asignada y se quedan igual.` : '',
  ].filter(Boolean).join('\n')

  if (!confirm(
    `Se marcarán los criterios de su unidad en ${candidatas.length} actividad(es):\n\n${detalle}\n\n` +
    (avisos ? avisos + '\n\n' : '') +
    'Después puedes quitar en cada una los que ese instrumento no evalúe.\n\n¿Continuar?')) return

  let hechas = 0
  for (const c of candidatas) {
    try {
      // c.act ya lleva la ut_id que se le haya asignado arriba
      await window.api.saveActividad({ ...c.act, ces: c.claves })
      hechas++
    } catch (e) {
      console.error('rellenarCesDesdeUts:', c.act.id, e)
    }
  }
  showToast(`Criterios marcados en ${hechas} actividad${hechas > 1 ? 'es' : ''}`)
  loadProgramacion()
}

/**
 * Reparte el peso de prácticas y exámenes en TODAS las evaluaciones del módulo.
 * Es la acción más destructiva de la pantalla —pisa cualquier peso afinado a
 * mano y no hay deshacer—, así que dice antes exactamente qué va a cambiar.
 */
async function applyModuloPesos() {
  const mid = parseInt(
    document.getElementById('prog-mod-sel')?.value ||
    document.getElementById('eval-mod-sel')?.value || 0
  )
  if (!mid) return
  const pesoPrac = parseFloat(document.getElementById('mod-peso-prac')?.value) || 30
  const pesoExam = parseFloat(document.getElementById('mod-peso-exam')?.value) || 70
  if (Math.abs(pesoPrac + pesoExam - 100) > 0.1) {
    alert(`Prácticas y exámenes suman ${pesoPrac + pesoExam} %, no 100. Ajústalo antes de aplicar.`)
    return
  }
  const acts = await window.api.getActividades(mid)
  if (!acts.length) { alert('Este módulo no tiene actividades.'); return }

  // Qué pesos cambian de verdad, para poder enseñarlo antes de tocar nada
  const evsPrev = [...new Set(acts.map(a => a.eval))].sort()
  const cambios = []
  for (const ev of evsPrev) {
    const evActs = acts.filter(a => a.eval === ev)
    const nP = evActs.filter(a => a.tipo === 'practica').length
    const nE = evActs.filter(a => a.tipo === 'examen').length
    for (const a of evActs) {
      const nuevo = a.tipo === 'practica'
        ? (nP ? Math.round(pesoPrac / nP * 10) / 10 : 0)
        : (nE ? Math.round(pesoExam / nE * 10) / 10 : 0)
      if (Math.abs((a.peso || 0) - nuevo) > 0.05) {
        cambios.push(`  · ${evalLabel(ev)} · ${a.descripcion || a.instrumento}: ${a.peso || 0}% → ${nuevo}%`)
      }
    }
  }
  if (!cambios.length) { showToast('Los pesos ya son esos, no hay nada que cambiar'); return }
  const muestra = cambios.slice(0, 12).join('\n') +
    (cambios.length > 12 ? `\n  … y ${cambios.length - 12} más` : '')
  if (!confirm(
    `Se van a reescribir ${cambios.length} peso(s) en las ${evsPrev.length} evaluaciones ` +
    `del módulo, repartiendo ${pesoPrac} % entre las prácticas y ${pesoExam} % entre los exámenes:\n\n` +
    `${muestra}\n\nEsto pisa cualquier peso que hayas ajustado a mano y no se puede deshacer.\n\n¿Aplicar?`)) return
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
  showToast(`${cambios.length} peso${cambios.length > 1 ? 's' : ''} actualizado${cambios.length > 1 ? 's' : ''}`)
  loadProgramacion()
}

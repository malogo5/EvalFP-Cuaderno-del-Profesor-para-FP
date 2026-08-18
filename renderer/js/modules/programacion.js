// PROGRAMACIÓN — Vista completa tipo Excel
// ═══════════════════════════════════════════════════════════════
// _cargarCatalogoNormalizado() vive en js/utils/catalogo-normalizado.js:
// la usan también Dashboard y Evaluaciones, así que es un punto único
// compartido, no propio de este archivo.

async function loadProgramacion() {
  const mid = document.getElementById('prog-mod-sel').value
  if (!mid) return
  const mod = _modulos.find(m => m.id == mid)
  if (!mod) return
  // `data_json` solo se lee ya para modulo.eval_count (nº de evaluaciones del
  // módulo, ajeno a RF-02) y como último recurso si getActividades fallara.
  // RA, CE, UT y asignaciones vienen siempre de las tablas normalizadas.
  const data = mod.data_json ? JSON.parse(mod.data_json) : null
  const panel = document.getElementById('prog-panel')

  const cat = await _cargarCatalogoNormalizado(mid)
  if (!cat.raCatalogo.length) {
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
    } else {
      panel.innerHTML = `
        <div class="empty-state">
          <div style="font-weight:700;color:var(--text);margin-bottom:6px">Este módulo todavía no está migrado a la programación normalizada</div>
          <div style="margin-bottom:12px">Desde RF-02, toda la pestaña de Programación lee de tablas con clave foránea
            (<code>ra_catalogo</code>, <code>ce_catalogo</code>, <code>unidades_trabajo</code>, <code>ut_ce</code>), no del
            JSON antiguo del módulo. Migra este módulo desde Ajustes — hace una copia de seguridad antes de tocar nada —
            y vuelve aquí.</div>
          <button class="btn btn-primary btn-sm" onclick="goSection('ajustes')">⚙ Ir a Ajustes</button>
        </div>`
    }
    return
  }
  const {
    raCatalogo, ceCatalogoRows, unidadesTrabajoRows, utCeModuloRows, ceInstrRows, actividadCeModuloRows,
    ras, ces, uts, asigs, raInstr,
  } = cat

  // Cargar actividades desde BD, con `.ces` resuelto contra actividad_ce cuando
  // exista una fila (fuente nueva). Si una actividad no tiene ninguna fila ahí
  // todavía se usa su columna JSON legada — así una actividad editada antes de
  // esta migración no pierde de golpe sus criterios.
  const actividadCePorAct = {}
  for (const f of actividadCeModuloRows) {
    (actividadCePorAct[f.actividad_id] = actividadCePorAct[f.actividad_id] || []).push(ceKey(f.ra_id, f.ce_id))
  }
  const actividades = ((await window.api.getActividades(parseInt(mid))) || data?.actividades || [])
    .map(a => actividadCePorAct[a.id] ? { ...a, ces: actividadCePorAct[a.id] } : a)

  // índices rápidos
  const utMap  = Object.fromEntries(uts.map(u => [u.id, u]))
  const raMap  = Object.fromEntries(ras.map(r => [r.id, r]))
  const evalCount = data?.modulo?.eval_count || [...new Set(uts.map(u => u.eval||1))].length || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)

  // Qué RAs caen en cada evaluación. Fuente única: la evaluación de las UT que los
  // trabajan (unidades_trabajo.eval / ut_ce), que es lo que el profesor mueve en
  // el asistente de UT. rasPorEvaluacion() no distingue de dónde vienen uts y
  // asignaciones, así que se reutiliza tal cual sobre la forma normalizada.
  const evalRasMap = rasPorEvaluacion({ ras, uts, asignaciones: asigs, eval_ras: {} }, evalCount)
  const evalDeRa   = {}
  for (const [ev, lista] of Object.entries(evalRasMap)) for (const raId of lista) evalDeRa[raId] = ev
  // Dejarlo escrito en el módulo: es lo que leen (todavía, fuera de Programación)
  // Evaluaciones, Dashboard y los scripts de IA — ver 00-CONTEXTO.md, deuda RF-02.
  await _sincronizarEvalRas(mid, evalCount, evalRasMap)

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
                      style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:2px 8px;font-size:10px;font-weight:700;cursor:pointer;margin-top:1px"
                      title="Elegir las unidades de trabajo que entran en este examen">Cambiar</button>
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
    // ── Pérdida del derecho a la evaluación continua (art. 3.6) ──────────
    h += `<div style="margin-top:14px">
      <div style="font-size:12px;font-weight:700;color:var(--ice);background:var(--navy3);padding:7px 14px;border-radius:6px;margin-bottom:6px;display:flex;gap:12px;align-items:center;flex-wrap:wrap">
        <span>📕 Pérdida de la evaluación continua</span>
        <span style="font-size:11px;font-weight:400;color:var(--text2)">
          Quien la pierde se evalúa solo con esta prueba, sin conservar nada de lo anterior (art. 3.6)</span>
      </div>
      <div style="padding:2px 2px 2px">
        <button onclick="addPruebaObjetiva(${mid})"
          style="${btnRec}background:rgba(239,68,68,.12);color:#ef4444">+ Prueba objetiva del módulo completo</button>
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
           ${Number(ra.dual) ? `<span style="font-size:10px;color:var(--accent2);font-weight:700" title="Parte que se acredita en la fase de formación en empresa">🏭 ${Number(ra.dual)}%</span>` : ''}
           <span class="badge badge-accent">${ra.pond||0}%</span>
         </div>`
      }
      h += `</div>`
    }
    h += `</div></div>`
  }

  // ── 3. UNIDADES DE TRABAJO — programación normalizada ────────
  // RF-02: lee y escribe unidades_trabajo, ut_ce y actividad_ce
  // (docs/rediseno/04-REDISENO-PANTALLAS.md §1.2-§1.4). El módulo ya está
  // migrado (se comprobó arriba), así que unidadesTrabajoRows/ceCatalogoRows/
  // utCeModuloRows vienen del catálogo cargado al principio de la función.
  {
    // Indicador de cobertura curricular (04-REDISENO-PANTALLAS.md §1.2): cuántos
    // CE del catálogo están asignados a ALGUNA UT. No es lo mismo que "tiene una
    // actividad que lo evalúe" — esa pregunta la contesta la sección de RA.
    const cubiertosSet = new Set(utCeModuloRows.map(f => `${f.ra_id}|${f.ce_id}`))
    const faltantesCe  = ceCatalogoRows.filter(c => !cubiertosSet.has(`${c.ra_id}|${c.ce_id}`))
    const totalCeNorm   = ceCatalogoRows.length
    const cobBadge = !totalCeNorm ? '' : (faltantesCe.length === 0
      ? `<span class="badge badge-green">✓ los ${totalCeNorm} criterios asignados a alguna UT</span>`
      : `<button type="button" onclick="_toggleFaltantesUt(this)" data-abierto="0"
           style="background:rgba(245,158,11,.15);color:var(--amber);border:none;border-radius:8px;padding:2px 10px;font-size:10.5px;font-weight:700;cursor:pointer">
           ⚠ ${totalCeNorm - faltantesCe.length} de ${totalCeNorm} criterios asignados a alguna UT — ver los que faltan
         </button>`)

    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
        📚 Unidades de Trabajo ${cobBadge}
      </div>
      ${faltantesCe.length ? `<div id="ut-faltantes" style="display:none;margin:6px 0 4px;padding:8px 10px;background:var(--bg3);border-radius:8px;font-size:11px;color:var(--text2);max-height:160px;overflow-y:auto">
        ${faltantesCe.map(c => `<div style="padding:2px 0"><b style="color:var(--accent)">${esc(c.ra_id)}|${esc(c.ce_id)}</b> ${esc(c.texto)}</div>`).join('')}
      </div>` : ''}
      <div style="overflow-x:auto">
      <table class="prog-table">
        <thead><tr>
          <th style="width:56px">UT</th>
          <th style="min-width:180px">Nombre</th>
          <th style="width:82px;text-align:center">Horas</th>
          <th style="width:88px;text-align:center">Eval</th>
          <th style="width:110px;text-align:center">Criterios</th>
          <th style="width:150px;text-align:center">Acciones</th>
        </tr></thead>
        <tbody>`
    for (const ut of unidadesTrabajoRows) {
      const misCe = utCeModuloRows.filter(f => f.ut_id === ut.ut_id).length
      h += `<tr>
        <td style="font-weight:700;color:var(--accent2);white-space:nowrap">${esc(ut.ut_id)}</td>
        <td><a href="#" onclick="abrirAsistenteUt(${mid},'${esc(ut.ut_id)}',1);return false" style="font-weight:500">${esc(ut.nombre)}</a></td>
        <td style="text-align:center">${ut.horas||0} h${ut.horas_empresa ? ` <span title="De ellas, en empresa" style="color:var(--accent2)">(🏭${ut.horas_empresa})</span>` : ''}</td>
        <td style="text-align:center"><a href="#" onclick="abrirAsistenteUt(${mid},'${esc(ut.ut_id)}',1);return false" class="badge badge-accent">${evalLabel(ut.eval)}</a></td>
        <td style="text-align:center"><a href="#" onclick="abrirAsistenteUt(${mid},'${esc(ut.ut_id)}',3);return false">${misCe} criterio${misCe===1?'':'s'}</a></td>
        <td style="text-align:center;white-space:nowrap">
          <button onclick="abrirNuevaActividadUt(${mid},'${esc(ut.ut_id)}')" title="Crear actividad desde esta UT"
            style="background:var(--accent);color:#fff;border:none;border-radius:6px;padding:3px 9px;font-size:11px;font-weight:700;cursor:pointer;margin-right:4px">+ Actividad</button>
          <button onclick="eliminarUnidadTrabajo(${mid},'${esc(ut.ut_id)}')" title="Eliminar UT" aria-label="Eliminar UT"
            style="background:transparent;color:#ef4444;border:1px solid rgba(239,68,68,.35);border-radius:6px;padding:3px 8px;font-size:11px;cursor:pointer">✕</button>
        </td>
      </tr>`
    }
    if (!unidadesTrabajoRows.length) {
      h += `<tr><td colspan="6" style="text-align:center;color:var(--text2);padding:16px">Este módulo todavía no tiene ninguna unidad de trabajo.</td></tr>`
    }
    h += `</tbody></table></div>
      <div style="padding:10px 2px 2px">
        <button onclick="abrirAsistenteUt(${mid},null,1)"
          style="background:transparent;color:var(--accent);border:1.5px solid var(--accent);border-radius:8px;padding:5px 16px;font-size:12px;font-weight:700;cursor:pointer">+ Nueva unidad de trabajo</button>
      </div>
    </div>`
  }

  // ── FAMILIA DE REPARTO POR TIPO DE ACTIVIDAD (RF-17) ──────────
  // Cada tipo de actividad tiene una familia de reparto por defecto
  // (examen|práctica: lo único que calificacion.js entiende). Aquí se puede
  // cambiar por módulo, sin tocar el motor — ver renderer/js/utils/tipos-actividad.js.
  {
    const familiaOverridesRows = await window.api.getTipoFamilia(parseInt(mid))
    const familiaOverrides = Object.fromEntries(familiaOverridesRows.map(r => [r.tipo, r.familia]))
    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title">⚖️ Familia de reparto por tipo de actividad</div>
      <div style="font-size:11.5px;color:var(--text2);margin-bottom:10px;line-height:1.5">
        El motor de cálculo solo distingue dos familias de reparto, examen y práctica. Cada tipo de
        actividad tiene una familia por defecto; cámbiala aquí si en este módulo debe repartir de otra forma
        — por ejemplo, que un proyecto pese como examen.
      </div>
      <div style="overflow-x:auto">
      <table class="prog-table" style="max-width:460px">
        <thead><tr><th>Tipo de actividad</th><th style="width:160px;text-align:center">Familia de reparto</th></tr></thead>
        <tbody>
          ${TIPOS_ACTIVIDAD.map(t => {
            const actual = familiaOverrides[t.id] || t.familiaDefecto
            return `<tr>
              <td>${esc(t.label)}</td>
              <td style="text-align:center">
                <select onchange="actualizarFamiliaTipo(${mid},'${t.id}',this.value)" style="font-size:11.5px">
                  <option value="examen"${actual==='examen'?' selected':''}>Examen</option>
                  <option value="practica"${actual==='practica'?' selected':''}>Práctica</option>
                </select>
                ${familiaOverrides[t.id] ? '' : `<span style="font-size:9.5px;color:var(--text3)"> (defecto)</span>`}
              </td>
            </tr>`
          }).join('')}
        </tbody>
      </table>
      </div>
    </div>`
  }

  // ── 4. RESULTADOS DE APRENDIZAJE Y CRITERIOS DE EVALUACIÓN ───
  // RF-02: lee y escribe ra_catalogo, ce_catalogo y ce_instrumentos_previstos
  // (docs/rediseno/05-PLAN-MIGRACION.md). El módulo ya está migrado (se
  // comprobó arriba); ceCatalogoRows/ceInstrRows vienen del catálogo cargado
  // al principio de la función, igual que en el resto de secciones.
  {
    let raEstadosDb = {}
    try {
      raEstadosDb = await window.api.getRaEstados(parseInt(mid)) || {}
    } catch { /* base antigua sin la tabla */ }

    const instrByCeNorm = {}
    for (const row of ceInstrRows) {
      const k = `${row.ra_id}|${row.ce_id}`
      ;(instrByCeNorm[k] = instrByCeNorm[k] || []).push(row.instrumento)
    }

    // RF-01, sobre la fuente normalizada: el motor único no cambia, solo de
    // dónde sacamos ras/cesByRa.
    // RF-17: el motor necesita el tipo ya resuelto a familia, no el real que
    // usa el resto de esta pantalla (plan de actividades, UT…) — por eso se
    // vuelve a pedir aquí en vez de reutilizar `actividades` tal cual.
    const rasParaCtx = raCatalogo.map(r => ({ id: r.ra_id, nombre: r.nombre, pond: r.pond }))
    const { actividades: actividadesParaCtx } = await getActividadesParaMotor(parseInt(mid))
    const ctxRA = contextoModulo({
      ras: rasParaCtx, cesByRa: ces, asignaciones: asigs, actividades: actividadesParaCtx,
      raEstados: raEstadosDb,
    })
    const algunRaNoImpartido = Object.values(ctxRA.ponderaciones).some(p => p.estado === 'no_impartido')

    const nTotalRaPond = raCatalogo.reduce((s, r) => s + (r.pond || 0), 0)
    const nRaPondOk    = raCatalogo.every(r => r.pond) && Math.abs(nTotalRaPond - 100) < 0.1
    const raSumBadge   = raCatalogo.some(r => r.pond)
      ? (nRaPondOk
          ? `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700;margin-left:auto">✓ 100%</span>`
          : `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700;margin-left:auto">⚠ suma ${nTotalRaPond}%</span>`)
      : ''

    // Mismo razonamiento de cobertura que antes, ahora contra el catálogo
    // normalizado. `coberturaCe` sigue siendo válido: solo mira existencia de
    // claves RA|CE, que no cambian entre el JSON viejo y las tablas nuevas.
    const nTotalCes = raCatalogo.reduce((s, r) => s + (ces[r.ra_id] || []).length, 0)
    const nCesCubiertos = Object.keys(coberturaCe)
      .filter(k => raCatalogo.some(r => k.startsWith(r.ra_id + '|'))).length
    const nRaDual = Object.fromEntries(raCatalogo.map(r => [r.ra_id, Number(r.dual_pct) || 0]))
    let nCesEnEmpresa = 0
    for (const ra of raCatalogo) {
      if (!nRaDual[ra.ra_id]) continue
      for (const ce of (ces[ra.ra_id] || [])) {
        if (!coberturaCe[ceKey(ra.ra_id, ce.id)]) nCesEnEmpresa++
      }
    }
    const nCesPendientes = nTotalCes - nCesCubiertos - nCesEnEmpresa
    const nEmpresaTxt = nCesEnEmpresa
      ? ` <span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(74,144,217,.14);color:var(--accent2);font-weight:700"
           title="Criterios de resultados dualizados que se acreditan en la fase de formación en empresa">🏭 ${nCesEnEmpresa} en empresa</span>`
      : ''
    const nPesoDual = raCatalogo.reduce((acc, r) => acc + (Number(r.pond) || 0) * (Number(r.dual_pct) || 0) / 100, 0)
    const nPesoDualTxt = Math.round(nPesoDual * 10) / 10
    const nDualEnRango = nPesoDual >= 10 && nPesoDual <= 20
    const dualBadge = nPesoDual
      ? `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;font-weight:700;${nDualEnRango
          ? 'background:rgba(16,185,129,.12);color:var(--green)'
          : 'background:rgba(245,158,11,.15);color:var(--amber)'}"
          title="Peso de los resultados de aprendizaje que se acreditan en la fase de formación en empresa, ponderado por la ponderación de cada RA. El periodo de formación en empresa del grado D debe cubrir entre el 10 % y el 20 % de los RA de los módulos asociados a estándares de competencia.">
          🏭 ${nPesoDualTxt}% del módulo se acredita en empresa${nDualEnRango ? ' ✓' : ' ⚠ fuera del 10-20 %'}</span>`
      : ''
    const cobBadge = nTotalCes
      ? (nCesPendientes <= 0
          ? `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(16,185,129,.12);color:var(--green);font-weight:700"
               title="Cada criterio del decreto está cubierto: por una actividad del aula o por la fase de formación en empresa">✓ los ${nTotalCes} criterios se evalúan</span>${nEmpresaTxt}`
          : `<span style="font-size:10.5px;padding:2px 9px;border-radius:8px;background:rgba(245,158,11,.15);color:var(--amber);font-weight:700"
               title="Los criterios sin actividad salen marcados en el desplegable con ○. Asígnalos a una práctica o examen, o marca su RA como dualizado si se acreditan en la empresa.">⚠ ${nCesPendientes} criterio${nCesPendientes > 1 ? 's' : ''} sin actividad que los evalúe</span>${nEmpresaTxt}`)
      : ''

    // RF-17: misma lista que el tipo de actividad (renderer/js/utils/tipos-
    // actividad.js) — el instrumento previsto de RF-02 y el tipo de actividad
    // son la misma fuente, no dos listas que puedan desincronizarse. 'empresa'
    // ya no está: no es un tipo de actividad, es la dualización que vive en
    // ra_catalogo.dual_pct (ver 00-CONTEXTO.md, tareas abiertas, sobre el
    // hueco de instrumento en fase_empresa para los CE dualizados).
    const INSTRUMENTOS = TIPOS_ACTIVIDAD.map(t => [t.id, t.label])
    // Instrumentos "del RA": los que comparten TODOS sus CE. Si divergen, no se
    // inventa un valor común — se avisa y se resuelve en el desplegable.
    const instrumentosDeRa = (raId, cesDelRa) => {
      if (!cesDelRa.length) return { lista: [], divergen: false }
      const sets = cesDelRa.map(ce => (instrByCeNorm[`${raId}|${ce.id}`] || []).slice().sort())
      const ref = JSON.stringify(sets[0])
      return { lista: sets[0] || [], divergen: sets.some(s => JSON.stringify(s) !== ref) }
    }
    const chip = (mid_, raId, ceId, val, label, activo) => {
      const attrCe = ceId ? ` data-ceid="${esc(ceId)}"` : ''
      const handler = ceId ? 'toggleCeInstrumento(this)' : 'toggleRaInstrumento(this)'
      return `<button type="button" class="instr-chip" data-mid="${mid_}" data-raid="${esc(raId)}"${attrCe}
          data-val="${val}" data-activo="${activo ? 1 : 0}" onclick="${handler}" title="${label}"
          style="font-size:9.5px;padding:2px 7px;border-radius:9px;cursor:pointer;font-weight:${activo ? 700 : 400};
                 border:1.5px solid ${activo ? 'var(--accent)' : 'var(--border2)'};
                 background:${activo ? 'rgba(201,104,45,.15)' : 'transparent'};
                 color:${activo ? 'var(--accent)' : 'var(--text2)'}">${label}</button>`
    }

    h += `<div class="card" style="margin-bottom:16px">
      <div class="prog-section-title" style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">🎯 Resultados de Aprendizaje y Criterios de Evaluación
        ${cobBadge}
        ${dualBadge}
        ${raSumBadge}
      </div>
      <div style="overflow-x:auto">
      <table class="prog-table" style="width:100%">
        <thead><tr>
          <th style="width:24px"></th>
          <th style="width:48px">RA</th>
          <th style="min-width:160px">Nombre</th>
          <th style="width:96px;text-align:center">Ponderación</th>
          <th style="width:180px;text-align:center">Estado de impartición</th>
          <th style="min-width:220px">Instrumento previsto</th>
          <th style="width:90px;text-align:center">% Empresa</th>
          <th style="width:34px;text-align:center" title="Necesario para incorporarse a la fase de empresa (art. 4.3.a)">🔑</th>
        </tr></thead>
        <tbody>`

    for (const ra of raCatalogo) {
      const raId = ra.ra_id
      const raCes = ces[raId] || []

      const raEstadoActual = ctxRA.raEstados[raId]
      const raEstadoMotivo = raEstadosDb[raId]?.motivo || ''
      const raEstadoColores = {
        previsto:     'background:rgba(106,96,80,.12);color:var(--text2)',
        impartido:    'background:rgba(16,185,129,.12);color:var(--green)',
        no_impartido: 'background:rgba(239,68,68,.12);color:#ef4444',
      }
      const raEstadoTitulo = raEstadoActual === 'no_impartido' && raEstadoMotivo
        ? `No impartido: ${raEstadoMotivo}`
        : 'Estado de impartición de este RA (Orden 201/2024, art. 2.3). "No impartido" excluye el RA del cómputo y reparte su ponderación.'
      const estadoSelect = `<span style="display:inline-flex;align-items:center;gap:3px">
        <select class="ra-estado-sel" data-mid="${mid}" data-raid="${esc(raId)}"
          data-current="${raEstadoActual}" data-motivo="${esc(raEstadoMotivo)}"
          onchange="updateRaEstado(this)" title="${esc(raEstadoTitulo)}"
          style="border:1.5px solid var(--border2);border-radius:8px;padding:2px 4px;font-size:10.5px;font-weight:700;cursor:pointer;font-family:inherit;${raEstadoColores[raEstadoActual] || ''}">
          <option value="previsto"${raEstadoActual === 'previsto' ? ' selected' : ''}>Previsto</option>
          <option value="impartido"${raEstadoActual === 'impartido' ? ' selected' : ''}>Impartido</option>
          <option value="no_impartido"${raEstadoActual === 'no_impartido' ? ' selected' : ''}>No impartido</option>
        </select>
        ${raEstadoActual === 'no_impartido' ? `<button type="button" onclick="openRaNoImpartidoModal(${mid},'${esc(raId)}')"
          title="Ver o editar el motivo" aria-label="Ver o editar el motivo"
          style="background:transparent;border:none;color:var(--text2);cursor:pointer;font-size:12px;padding:0 2px">✎</button>` : ''}
      </span>`

      const raPondCtx = ctxRA.ponderaciones[raId] || {}
      const repartoBadge = algunRaNoImpartido && Math.abs((raPondCtx.original || 0) - (raPondCtx.efectiva || 0)) > 0.05
        ? `<div><span class="badge" title="Ponderación original → efectiva tras repartir la de los RA no impartidos"
            style="background:rgba(245,158,11,.15);color:var(--amber);font-weight:700;font-size:9.5px">${_fmtPct(raPondCtx.original)}% → ${_fmtPct(raPondCtx.efectiva)}%</span></div>`
        : ''

      const { lista: instrRaLista, divergen: instrDivergen } = instrumentosDeRa(raId, raCes)
      const instrCell = `<div style="display:flex;gap:4px;flex-wrap:wrap;align-items:center">
        ${INSTRUMENTOS.map(([val, label]) => chip(mid, raId, null, val, label, instrRaLista.includes(val))).join('')}
        ${instrDivergen ? `<span title="Los CE de este RA no llevan todos los mismos instrumentos: revísalo en el desplegable" style="color:var(--amber);font-size:12px;cursor:help">⚠</span>` : ''}
      </div>`

      const abierto = _raExpandidas.has(raId)
      h += `<tr style="border-top:1px solid var(--border)">
        <td style="text-align:center">
          <button type="button" id="ra-tog-${esc(raId)}" onclick="_toggleRaDetalle('${esc(raId)}')"
            title="${abierto ? 'Ocultar' : 'Ver'} criterios de evaluación"
            style="background:transparent;border:none;color:var(--text2);cursor:pointer;font-size:12px">${abierto ? '▾' : '▸'}</button>
        </td>
        <td style="font-weight:800;color:var(--accent2);white-space:nowrap;vertical-align:top;padding-top:8px">${esc(raId)}</td>
        <td style="font-weight:600;vertical-align:top;padding-top:8px">${esc(ra.nombre)}${repartoBadge}</td>
        <td style="text-align:center;vertical-align:top;padding-top:6px">
          <input class="ra-pond-cell" type="number" min="0" max="100" step="1"
            value="${ra.pond || ''}" placeholder="—"
            data-mid="${mid}" data-raid="${esc(raId)}"
            onchange="updateRaCatalogoPond(this)" title="Ponderación de este RA en la nota final (%)"
            style="width:52px;text-align:center"/>%
        </td>
        <td style="text-align:center;vertical-align:top;padding-top:6px">${estadoSelect}</td>
        <td style="vertical-align:top;padding-top:8px">${instrCell}</td>
        <td style="text-align:center;vertical-align:top;padding-top:6px">
          <input class="ra-dual-cell peso-cell" type="number" min="0" max="100" step="5"
            value="${ra.dual_pct != null && ra.dual_pct !== '' ? ra.dual_pct : ''}" placeholder="0"
            data-mid="${mid}" data-raid="${esc(raId)}"
            onchange="updateRaCatalogoDual(this)"
            title="Parte de este RA que se adquiere y acredita en la fase de formación en empresa (Decreto 80/2024, art. 5.bis)"
            style="width:44px;text-align:center"/>%
        </td>
        <td style="text-align:center;vertical-align:top;padding-top:8px">
          <input type="checkbox" ${ra.llave ? 'checked' : ''}
            onchange="updateRaCatalogoLlave(${mid},'${esc(raId)}',this.checked)"
            title="Necesario para incorporarse a la fase de formación en empresa (Orden 201/2024, art. 4.3.a)"
            style="accent-color:var(--accent);width:14px;height:14px;cursor:pointer"/>
        </td>
      </tr>
      <tr id="ra-det-${esc(raId)}" style="display:${abierto ? '' : 'none'}">
        <td></td>
        <td colspan="7" style="padding:0 0 14px 0">`

      if (raCes.length) {
        const algunPesoExplicito = raCes.some(c => c.peso != null && c.peso !== '')
        h += `<table style="width:100%;border-collapse:collapse;background:var(--bg3);border-radius:8px">
          <thead><tr style="font-size:9.5px;color:var(--text3);text-transform:uppercase;letter-spacing:.04em">
            <th style="width:16px"></th>
            <th style="width:52px;text-align:left;padding:5px 6px">CE</th>
            <th style="text-align:left;padding:5px 6px">Criterio</th>
            <th style="min-width:200px;text-align:left;padding:5px 6px">Instrumento</th>
            <th class="th-ce-pond" style="width:110px;text-align:right;padding:5px 6px;cursor:pointer;user-select:none"
                onclick="_toggleCePesoColumna(this)"
                title="El reparto automático distribuye a partes iguales la ponderación del RA entre sus criterios. Que la casilla esté en blanco no significa que falte un dato.">
              ${algunPesoExplicito ? 'Ponderación ▾' : '▸ reparto automático'}
            </th>
          </tr></thead>
          <tbody>`
        for (const ce of raCes) {
          const donde = coberturaCe[ceKey(raId, ce.id)] || []
          const marca = donde.length
            ? `<span title="Se evalúa en: ${esc(donde.join(' · '))}" style="color:var(--green);font-size:11px">●</span>`
            : (nRaDual[raId]
              ? `<span title="Se acredita en la fase de formación en empresa (${nRaDual[raId]}% de este resultado)" style="font-size:10px">🏭</span>`
              : `<span title="Ningún examen ni práctica evalúa este criterio todavía" style="color:var(--amber);font-size:11px">○</span>`)
          const instrCe = instrByCeNorm[`${raId}|${ce.id}`] || []
          const chipsCe = INSTRUMENTOS.map(([val, label]) =>
            chip(mid, raId, ce.id, val, label, instrCe.includes(val))).join('')
          const pesoCe = `<input class="peso-cell" type="number" min="0" max="100" step="1"
              value="${ce.peso != null && ce.peso !== '' ? ce.peso : ''}" placeholder="—"
              data-mid="${mid}" data-raid="${esc(raId)}" data-ceid="${esc(ce.id)}"
              onchange="updateCeCatalogoPeso(this)"
              title="Peso de este criterio dentro del RA. En blanco, todos los criterios pesan igual."
              style="width:52px;font-size:11px"/>`
          h += `<tr style="border-top:1px solid var(--border)">
            <td style="padding:4px 6px 4px 6px;text-align:center;vertical-align:top">${marca}</td>
            <td style="padding:4px 6px;font-size:12px;font-weight:700;color:var(--accent);white-space:nowrap;vertical-align:top">${esc(ce.id)}</td>
            <td style="padding:4px 6px;font-size:12px;color:var(--text2);line-height:1.5">${esc(ce.texto)}</td>
            <td style="padding:4px 6px;vertical-align:top"><div style="display:flex;gap:3px;flex-wrap:wrap">${chipsCe}</div></td>
            <td class="ce-peso-celda" style="padding:4px 6px;text-align:right;vertical-align:top;white-space:nowrap;display:${algunPesoExplicito ? '' : 'none'}">${pesoCe}<span style="font-size:10px;color:var(--text3)">%</span></td>
          </tr>`
        }
        h += `</tbody></table>`
      } else {
        h += `<div style="padding:6px 0;font-size:11px;color:var(--text2);font-style:italic">Este RA no tiene criterios en el catálogo.</div>`
      }

      h += `</td></tr>`
    }

    h += `</tbody></table></div></div>`
  }

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

// RF-02 · RESULTADOS DE APRENDIZAJE Y CRITERIOS — programación normalizada
// ═══════════════════════════════════════════════════════════════
// Todo esto lee y escribe ra_catalogo / ce_catalogo / ce_instrumentos_previstos
// (docs/rediseno/05-PLAN-MIGRACION.md), no data_json ni ra_ponderaciones.

async function updateRaCatalogoPond(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const vacio = String(el.value).trim() === ''
  const pond  = vacio ? 0 : parseFloat(el.value)
  if (!vacio && !validators.ponderacion(pond)) {
    alert('Ponderación inválida. Debe estar entre 0 y 100.')
    return loadProgramacion()
  }
  try {
    await window.api.setRaCatalogoPond(mid, raId, pond)
    showSaved()
    await loadProgramacion()
  } catch (e) {
    alert('Error guardando ponderación: ' + validators.sanitizeErrorMessage(e, 'updateRaCatalogoPond'))
  }
}

/**
 * Marca un RA como necesario para incorporarse a la fase de formación en
 * empresa (Orden 201/2024, art. 4.3.a).
 */
async function updateRaCatalogoLlave(mid, raId, llave) {
  try {
    await window.api.setRaCatalogoLlave(mid, raId, llave)
    showToast(llave
      ? `${raId} marcado como necesario para la fase de empresa`
      : `${raId} ya no condiciona la fase de empresa`)
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'updateRaCatalogoLlave'))
    await loadProgramacion()
  }
}

/**
 * Porcentaje de un RA que se adquiere y acredita en la fase de formación en
 * empresa (Decreto 80/2024, art. 5.bis). 0 o vacío = íntegramente en el aula.
 */
async function updateRaCatalogoDual(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const vacio = String(el.value).trim() === ''
  const pct   = vacio ? null : parseFloat(el.value)
  if (!vacio && (isNaN(pct) || pct < 0 || pct > 100)) {
    alert('Porcentaje inválido. Debe estar entre 0 y 100.')
    return loadProgramacion()
  }
  try {
    await window.api.setRaCatalogoDual(mid, raId, pct)
    await loadProgramacion()
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'updateRaCatalogoDual'))
  }
}

/**
 * Peso de un criterio dentro de su RA (Orden 201/2024, art. 4.3.a). En blanco,
 * reparto automático entre los CE del RA.
 */
async function updateCeCatalogoPeso(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const ceId = el.dataset.ceid
  const vacio = String(el.value).trim() === ''
  const peso  = vacio ? null : parseFloat(el.value)
  if (!vacio && (isNaN(peso) || peso < 0 || peso > 100)) {
    alert('Peso inválido. Debe estar entre 0 y 100.')
    return loadProgramacion()
  }
  try {
    await window.api.setCeCatalogoPeso(mid, raId, ceId, peso)
    showSaved()
    await loadProgramacion()
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'updateCeCatalogoPeso'))
  }
}

/**
 * Instrumento previsto, declarado por RA: lo heredan TODOS los CE de ese RA
 * (RF-02). Sustituye cualquier excepción puntual que hubiera por CE — es
 * literalmente volver a declararlo por RA.
 */
async function toggleRaInstrumento(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const val  = el.dataset.val
  const grupo = el.closest('div')
  const activos = grupo
    ? Array.from(grupo.querySelectorAll('.instr-chip'))
        .filter(b => b.dataset.activo === '1')
        .map(b => b.dataset.val)
    : []
  const set = new Set(activos)
  if (set.has(val)) set.delete(val); else set.add(val)
  try {
    await window.api.setRaInstrumentos(mid, raId, [...set])
    await loadProgramacion()
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'toggleRaInstrumento'))
  }
}

/** Excepción puntual de instrumento previsto para UN CE (RF-02). */
async function toggleCeInstrumento(el) {
  const mid  = parseInt(el.dataset.mid)
  const raId = el.dataset.raid
  const ceId = el.dataset.ceid
  const val  = el.dataset.val
  const grupo = el.closest('div')
  const activos = grupo
    ? Array.from(grupo.querySelectorAll('.instr-chip'))
        .filter(b => b.dataset.activo === '1')
        .map(b => b.dataset.val)
    : []
  const set = new Set(activos)
  if (set.has(val)) set.delete(val); else set.add(val)
  try {
    await window.api.setCeInstrumentos(mid, raId, ceId, [...set])
    await loadProgramacion()
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'toggleCeInstrumento'))
  }
}

/** Despliega o repliega los criterios de un RA. Se recuerda entre recargas. */
function _toggleRaDetalle(raId) {
  if (_raExpandidas.has(raId)) _raExpandidas.delete(raId)
  else _raExpandidas.add(raId)
  const fila = document.getElementById('ra-det-' + raId)
  const btn  = document.getElementById('ra-tog-' + raId)
  const abierto = _raExpandidas.has(raId)
  if (fila) fila.style.display = abierto ? '' : 'none'
  if (btn)  btn.textContent    = abierto ? '▾' : '▸'
}

/**
 * Columna de ponderación por CE, plegada por defecto (04-REDISENO-PANTALLAS.md
 * §1.1): una casilla en blanco parece un dato que falta y no lo es, así que
 * mientras nadie haya puesto ningún peso se oculta entera tras la cabecera
 * «reparto automático».
 */
function _toggleCePesoColumna(th) {
  const tabla = th.closest('table')
  if (!tabla) return
  const celdas = tabla.querySelectorAll('.ce-peso-celda')
  const oculto = celdas.length > 0 && celdas[0].style.display === 'none'
  celdas.forEach(td => { td.style.display = oculto ? '' : 'none' })
  th.textContent = oculto ? 'Ponderación ▾' : '▸ reparto automático'
}

// RF-01 · ESTADO DE IMPARTICIÓN DEL RA
// ═══════════════════════════════════════════════════════════════
let _raEstadoModalState = null

// RF-02: qué filas de la tabla de RA están desplegadas, para que no se
// vuelvan a cerrar todas cada vez que loadProgramacion() recarga tras guardar.
const _raExpandidas = new Set()

/** Redondea a 1 decimal y quita el ".0" sobrante, para las cifras del badge de reparto. */
function _fmtPct(n) {
  const r = Math.round((Number(n) || 0) * 10) / 10
  return Number.isInteger(r) ? String(r) : String(r.toFixed(1))
}

/**
 * Cambia el estado de impartición de un RA. "Previsto" e "impartido" se
 * guardan al vuelo; "no impartido" exige motivo (RF-01, Orden 201/2024 art.
 * 2.3), así que abre el modal en vez de guardar directamente.
 */
async function updateRaEstado(el) {
  const mid   = parseInt(el.dataset.mid)
  const raId  = el.dataset.raid
  const valor = el.value
  if (!mid || !raId) return

  if (valor === 'no_impartido') {
    openRaNoImpartidoModal(mid, raId, el)
    return
  }
  try {
    await window.api.setRaEstado(mid, raId, valor, null)
    el.dataset.current = valor
    showToast(`${raId}: ${valor === 'impartido' ? 'impartido' : 'previsto'}`)
    await loadProgramacion()
  } catch (e) {
    alert('Error guardando el estado del RA: ' + validators.sanitizeErrorMessage(e, 'updateRaEstado'))
    el.value = el.dataset.current
  }
}

/** Abre el modal de motivo para marcar (o revisar) un RA como no impartido. */
function openRaNoImpartidoModal(mid, raId, el) {
  const selEl = el || document.querySelector(`.ra-estado-sel[data-mid="${mid}"][data-raid="${CSS.escape(raId)}"]`)
  _raEstadoModalState = { mid, raId, el: selEl }
  document.getElementById('ra-estado-title').textContent = `${raId} — marcar como no impartido`
  document.getElementById('ra-estado-motivo').value = selEl?.dataset.motivo || ''
  document.getElementById('modal-ra-estado').showModal()
}

async function saveRaNoImpartido() {
  if (!_raEstadoModalState) return
  const { mid, raId } = _raEstadoModalState
  const motivo = document.getElementById('ra-estado-motivo').value.trim()
  if (!motivo) {
    alert('El motivo es obligatorio para marcar un RA como no impartido.')
    return
  }
  try {
    await window.api.setRaEstado(mid, raId, 'no_impartido', motivo)
    closeRaEstadoModal()
    showToast(`${raId} marcado como no impartido`)
    await loadProgramacion()
  } catch (e) {
    alert('Error guardando el motivo: ' + validators.sanitizeErrorMessage(e, 'setRaEstado'))
  }
}

/** Cierra el modal. Si no se ha guardado, el select vuelve a su valor previo. */
function closeRaEstadoModal() {
  const dlg = document.getElementById('modal-ra-estado')
  if (dlg.open) dlg.close()
  if (_raEstadoModalState?.el) _raEstadoModalState.el.value = _raEstadoModalState.el.dataset.current
  _raEstadoModalState = null
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
 * Traduce una lista de claves "RA|CE" a pares {ra_id,ce_id} y las guarda en
 * actividad_ce (fuente nueva, RF-02). Escritura doble TEMPORAL: actividades.ces
 * (columna JSON) se sigue escribiendo también en cada punto que llama a esto,
 * porque Dashboard, Evaluaciones e IA todavía la leen para construir su
 * contextoModulo — ver 00-CONTEXTO.md, deuda fechada de esta tarea. Se retira
 * cuando esas pantallas pasen a leer las tablas normalizadas.
 */
async function _sincronizarActividadCe(actId, mid, cesKeys) {
  const pares = (cesKeys || []).map(k => ({ ra_id: ceKeyRa(k), ce_id: ceKeyCe(k) }))
  await window.api.setActividadCe(actId, parseInt(mid), pares)
}

/**
 * Reasigna las UT de una actividad dejándola coherente:
 *  · ra_id pasa a ser el RA de esas UT (o se vacía si son varios, porque entonces
 *    quien manda son los criterios marcados);
 *  · los criterios que ya no pertenecen a ninguna de las UT nuevas se caen, en vez
 *    de quedarse ahí calificando un RA que la actividad ya no toca.
 * Devuelve cuántos criterios se han descartado.
 * `asigs`/`cesPorRa` vienen ya adaptados de las tablas normalizadas
 * (_cargarCatalogoNormalizado), con la misma forma que antes tenían
 * data.asignaciones/data.ces.
 */
function _reasignarUtsActividad(act, utIds, asigs, cesPorRa) {
  act.ut_id = utIds.join(',')
  asigs = asigs || []
  const ras = rasDeActividad({ ut_id: act.ut_id }, asigs)
  act.ra_id = ras.length === 1 ? ras[0] : null

  const grupos    = cesDisponiblesActividad(act, asigs, cesPorRa || {})
  const validas   = new Set()
  grupos.forEach(g => g.ces.forEach(ce => validas.add(ceKey(g.raId, ce.id))))
  const antes     = actCesLista(act)
  const migradas  = migrarCesActividad({ ...act, ces: antes }, asigs, cesPorRa || {}) || antes
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
    const { asigs, ces } = await _cargarCatalogoNormalizado(mid)
    const perdidos = _reasignarUtsActividad(act, selected, asigs, ces)
    await window.api.saveActividad(act)
    await _sincronizarActividadCe(actId, mid, act.ces)
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
  const newCount = parseInt(count)
  const data = _getModData(mid)   // solo para modulo.eval_count, no es RF-02
  if (!data) return

  const [actsPrev, cat] = await Promise.all([
    window.api.getActividades(parseInt(mid)),
    _cargarCatalogoNormalizado(mid),
  ])
  const utsPrev  = cat.unidadesTrabajoRows   // {ut_id, nombre, horas, horas_empresa, eval, tags}
  const anterior = data.modulo?.eval_count || [...new Set(utsPrev.map(u => u.eval || 1))].length || 3
  if (newCount === anterior) return

  // Simular el reparto para poder contarlo antes de tocar nada
  const simulaUt = (() => {
    const orden = utsPrev.slice().sort((a, b) => (a.eval||1)-(b.eval||1))
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
  data.modulo = data.modulo || {}
  data.modulo.eval_count = newCount
  // _saveModData (no _sincronizarActividadCe: no toca actividades) porque
  // sigue escribiendo el blob entero de data_json, ras incluido — si esos ras
  // están desactualizados respecto a ra_catalogo, el aviso de cierres/huérfanas
  // de setModuloDataJson es la red de seguridad que lo dice en vez de callarlo.
  await _saveModData(mid, data, false)

  // ── Redistribuir UTs (unidades_trabajo.eval) ──────────────────
  // Siempre redistribuye proporcionalmente: ninguna UT se pierde. eval_ras ya
  // no se calcula ni se guarda aquí: loadProgramacion() lo deriva de las UT
  // recién redistribuidas y lo sincroniza al recargar, más abajo.
  if (utsPrev.length) {
    const sorted = utsPrev.slice().sort((a,b) => (a.eval||1)-(b.eval||1))
    const perEval = Math.ceil(sorted.length / newCount)
    for (const [i, ut] of sorted.entries()) {
      const nuevoEval = Math.min(Math.floor(i / perEval) + 1, newCount)
      if (nuevoEval !== (ut.eval || 1)) {
        await window.api.setUnidadTrabajo(mid, ut.ut_id, {
          nombre: ut.nombre, horas: ut.horas, horasEmpresa: ut.horas_empresa, eval: nuevoEval, tags: ut.tags,
        })
      }
    }
  }

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

  loadProgramacion()
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
 * Alta de la prueba objetiva de evaluación completa del módulo (art. 3.6).
 *
 * Es la prueba de quien ha perdido el derecho a la evaluación continua. La Orden
 * 201/2024, en la redacción de la Orden 55/2026, exige que «incluirá la totalidad
 * de los resultados de aprendizaje a través de sus criterios de evaluación», así
 * que se crea ya con TODOS los criterios del módulo marcados: si se dejara al
 * profesorado marcarlos a mano, lo fácil sería olvidar alguno y el módulo se
 * daría por superado sin haber evaluado todo.
 *
 * Peso 0 y sin evaluación parcial asignada: no compite con las actividades del
 * curso. Para quien conserva la evaluación continua es una actividad más; para
 * quien la ha perdido es la única que cuenta.
 */
async function addPruebaObjetiva(mid) {
  const data = _getModData(mid)   // solo para modulo.eval_count, no es RF-02
  const { ces } = await _cargarCatalogoNormalizado(mid)
  const todos = todosLosCe(ces)
  if (!todos.length) {
    alert('Este módulo no tiene criterios de evaluación cargados.')
    return
  }
  const allActs  = await window.api.getActividades(parseInt(mid))
  const maxOrden = allActs.reduce((m, a) => Math.max(m, a.orden || 0), 0)
  const evalCount = Number(data?.modulo?.eval_count) || 3
  const actId = await window.api.saveActividad({
    modulo_id: parseInt(mid), ut_id: null, ra_id: null,
    descripcion: 'Prueba objetiva de evaluación completa (art. 3.6)',
    instrumento: 'Examen', tipo: 'examen',
    peso: 0, nota_max: 10, eval: evalCount, orden: maxOrden + 1,
    ces: todos, convocatoria: 1, prueba_objetiva: 1,
  })
  await _sincronizarActividadCe(actId, mid, todos)
  showToast(`Prueba objetiva creada con los ${todos.length} criterios del módulo`)
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
 * Deja escrito en el módulo el reparto de RA por evaluación que ya se calculó
 * en loadProgramacion() a partir de las tablas normalizadas. Evaluaciones,
 * Dashboard y los informes de IA leen `eval_ras` desde data_json — no están
 * migrados todavía (00-CONTEXTO.md, deuda RF-02) — así que este es el único
 * punto que les mantiene ese dato al día sin tocar esas pantallas.
 */
async function _sincronizarEvalRas(mid, evalCount, evalRasMap) {
  const data = _getModData(mid)
  if (!data) return false
  if (_mismoEvalRas(evalRasMap, data.eval_ras, evalCount)) return false
  data.eval_ras = evalRasMap
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
  let r
  try {
    r = await window.api.setModuloDataJson(parseInt(mid), data)
  } catch (e) {
    // db.js aborta si el data.ras que se escribe no coincide con ra_catalogo:
    // es la red de seguridad contra un cierre de RA (art. 4.3.f) borrado por un
    // snapshot desactualizado. No debe pasar en el uso normal, pero si pasa hay
    // que decirlo, no perderlo en un rechazo de promesa que nadie ve.
    alert('No se ha podido guardar: ' + validators.sanitizeErrorMessage(e, '_saveModData'))
    if (reload) loadProgramacion()
    return
  }
  _modulos = await window.api.getModulos()
  showSaved()
  // Quitar un RA de la programación deja sin dueño a las actividades que lo
  // calificaban. Siguen en la parrilla con sus notas puestas, pero ya no cuentan
  // para nada: quien las metió da por hecho que sí. No se pueden borrar solas
  // —son notas—, así que al menos hay que decirlo.
  if (r && r.cierresRetirados) {
    // Un cierre de evaluación es un acto formal: si desaparece, hay que decirlo.
    alert(
      `Se ${r.cierresRetirados === 1 ? 'ha retirado 1 cierre de evaluación' : `han retirado ${r.cierresRetirados} cierres de evaluación`} ` +
      `de resultados de aprendizaje que ya no están en la programación. Si vuelves a añadir ` +
      `ese resultado, habrá que cerrarlo otra vez en la próxima sesión de evaluación.`)
  }
  if (r && r.huerfanas && r.huerfanas.length) {
    const lista = r.huerfanas.slice(0, 8).map(a => `· ${a.descripcion || '(sin descripción)'} (${a.ra_id})`).join('\n')
    const mas = r.huerfanas.length > 8 ? `\n… y ${r.huerfanas.length - 8} más.` : ''
    alert(
      `Has quitado de la programación un resultado de aprendizaje que todavía califican ` +
      `${r.huerfanas.length === 1 ? 'esta actividad' : 'estas ' + r.huerfanas.length + ' actividades'}:\n\n` +
      lista + mas +
      `\n\nSus notas siguen guardadas, pero ya no cuentan para ningún resultado de aprendizaje. ` +
      `Asígnalas a otro o bórralas desde la pestaña de Programación.`)
  }
  if (reload) loadProgramacion()
}

// RF-02, segunda parte · UNIDADES DE TRABAJO — programación normalizada
// ═══════════════════════════════════════════════════════════════
// Todo esto lee y escribe unidades_trabajo / ut_ce / actividad_ce
// (docs/rediseno/04-REDISENO-PANTALLAS.md §1.2-§1.4), no data_json.

function _toggleFaltantesUt(btn) {
  const panel = document.getElementById('ut-faltantes')
  if (!panel) return
  const abierto = btn.dataset.abierto === '1'
  panel.style.display = abierto ? 'none' : ''
  btn.dataset.abierto = abierto ? '0' : '1'
}

async function eliminarUnidadTrabajo(mid, utId) {
  if (!confirm(`¿Eliminar ${utId}?\n\nLas actividades que la tengan asignada no se borran: conservan su fecha, ` +
    'su nota y sus evidencias, pero quedan apuntando a una unidad de trabajo que ya no existe en el catálogo.')) return
  try {
    await window.api.deleteUnidadTrabajo(mid, utId)
    showToast(`${utId} eliminada`)
    await loadProgramacion()
  } catch (e) {
    alert('Error eliminando la unidad de trabajo: ' + validators.sanitizeErrorMessage(e, 'eliminarUnidadTrabajo'))
  }
}

async function actualizarFamiliaTipo(mid, tipo, familia) {
  try {
    await window.api.setTipoFamilia(mid, tipo, familia)
    showToast(`${tipo}: ahora reparte como ${familia === 'examen' ? 'examen' : 'práctica'}`)
  } catch (e) {
    alert('Error: ' + validators.sanitizeErrorMessage(e, 'actualizarFamiliaTipo'))
  }
}

// ── Asistente de tres pasos para crear/editar una UT ──────────────────────
// (04-REDISENO-PANTALLAS.md §1.2-§1.4). El mismo asistente sirve para crear
// y para editar: editar solo cambia el paso inicial y precarga el estado.
let _utAsistente = null

async function abrirAsistenteUt(mid, utId, pasoInicial) {
  mid = parseInt(mid)
  const [raCatalogo, ceCatalogoRows, utCeModulo, utsExistentes] = await Promise.all([
    window.api.getRaCatalogo(mid),
    window.api.getCeCatalogo(mid),
    window.api.getUtCeModulo(mid),
    window.api.getUnidadesTrabajo(mid),
  ])
  const cesByRa = {}
  for (const row of ceCatalogoRows) {
    (cesByRa[row.ra_id] = cesByRa[row.ra_id] || []).push({ id: row.ce_id, texto: row.texto })
  }

  const modData = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || 3

  let nombre = '', horas = 0, horasEmpresa = 0, evalNum = 1, tags = ''
  const rasSel = new Set()
  const cesPorRa = {}
  if (utId) {
    const ut = utsExistentes.find(u => u.ut_id === utId)
    if (ut) { nombre = ut.nombre; horas = ut.horas || 0; horasEmpresa = ut.horas_empresa || 0; evalNum = ut.eval || 1; tags = ut.tags || '' }
    for (const f of utCeModulo) {
      if (f.ut_id !== utId) continue
      rasSel.add(f.ra_id)
      ;(cesPorRa[f.ra_id] = cesPorRa[f.ra_id] || new Set()).add(f.ce_id)
    }
  }

  _utAsistente = {
    mid, utId, paso: pasoInicial || 1, evalCount,
    nombre, horas, horasEmpresa, evalNum, tags,
    rasSel, cesPorRa, raCatalogo, cesByRa, utCeModulo, soloSinCubrir: false,
  }
  document.getElementById('ut-asis-title').textContent = utId ? `Editar ${utId}` : 'Nueva unidad de trabajo'
  _renderAsistenteUt()
  document.getElementById('modal-ut-asistente').showModal()
}

function cerrarAsistenteUt() {
  const dlg = document.getElementById('modal-ut-asistente')
  if (dlg.open) dlg.close()
  _utAsistente = null
}

function _pasoAsistenteValido() {
  const st = _utAsistente
  if (!st) return false
  if (st.paso === 1) return st.nombre.trim().length > 0
  if (st.paso === 2) return st.rasSel.size > 0
  if (st.paso === 3) return [...st.rasSel].some(raId => (st.cesPorRa[raId]?.size || 0) > 0)
  return false
}

function _renderAsistenteUt() {
  const st = _utAsistente
  if (!st) return
  for (let p = 1; p <= 3; p++) {
    const seg = document.getElementById(`ut-asis-bar-${p}`)
    if (!seg) continue
    seg.classList.remove('hecho', 'actual')
    if (p < st.paso) seg.classList.add('hecho')
    else if (p === st.paso) seg.classList.add('actual')
  }
  const atras = document.getElementById('ut-asis-atras')
  if (atras) atras.style.visibility = st.paso === 1 ? 'hidden' : 'visible'

  const body = document.getElementById('ut-asis-body')
  if (body) body.innerHTML = st.paso === 1 ? _pasoAsistente1() : st.paso === 2 ? _pasoAsistente2() : _pasoAsistente3()

  const btn = document.getElementById('ut-asis-continuar')
  if (btn) {
    btn.textContent = st.paso === 3 ? (st.utId ? 'Guardar cambios' : 'Crear unidad de trabajo') : 'Continuar'
    btn.disabled = !_pasoAsistenteValido()
  }
}

function _pasoAsistente1() {
  const st = _utAsistente
  const evals = Array.from({length: st.evalCount || 3}, (_, i) => i + 1)
  return `
    <div class="field" style="margin-bottom:14px">
      <label for="ut-asis-nombre">Nombre de la unidad de trabajo</label>
      <input id="ut-asis-nombre" type="text" value="${esc(st.nombre)}" placeholder="Ej. Instalación de software libre y propietario"
        oninput="_utAsistenteCampo('nombre',this.value)" style="width:100%"/>
    </div>
    <div class="field" style="margin-bottom:14px">
      <label>Evaluación prevista</label>
      <div style="display:flex;gap:8px">
        ${evals.map(e => `<button type="button" onclick="_utAsistenteCampo('evalNum',${e})"
          style="flex:1;padding:8px;border-radius:8px;cursor:pointer;font-weight:700;
            border:1.5px solid ${st.evalNum===e?'var(--accent)':'var(--border2)'};
            background:${st.evalNum===e?'rgba(201,104,45,.12)':'transparent'};
            color:${st.evalNum===e?'var(--accent)':'var(--text2)'}">${evalLabel(e)}</button>`).join('')}
      </div>
    </div>
    <div style="display:flex;gap:14px">
      <div class="field" style="flex:1">
        <label for="ut-asis-horas">Horas</label>
        <input id="ut-asis-horas" type="number" min="0" value="${st.horas||''}" oninput="_utAsistenteCampo('horas',this.value)"/>
      </div>
      <div class="field" style="flex:1">
        <label for="ut-asis-horas-emp">Horas en empresa</label>
        <input id="ut-asis-horas-emp" type="number" min="0" value="${st.horasEmpresa||''}" oninput="_utAsistenteCampo('horasEmpresa',this.value)"/>
      </div>
    </div>
    <div class="field" style="margin-top:14px">
      <label for="ut-asis-tags">Contenidos clave (opcional)</label>
      <input id="ut-asis-tags" type="text" value="${esc(st.tags)}" oninput="_utAsistenteCampo('tags',this.value)"/>
    </div>`
}

function _utAsistenteCampo(campo, valor) {
  const st = _utAsistente
  if (!st) return
  if (campo === 'horas' || campo === 'horasEmpresa') valor = parseInt(valor) || 0
  if (campo === 'evalNum') valor = Number(valor)
  st[campo] = valor
  const btn = document.getElementById('ut-asis-continuar')
  if (btn) btn.disabled = !_pasoAsistenteValido()
  // Solo el botón de evaluación necesita repintar (para marcar el activo);
  // el texto se escribe sin volver a montar el HTML, o se perdería el cursor.
  if (campo === 'evalNum') _renderAsistenteUt()
}

function _pasoAsistente2() {
  const st = _utAsistente
  const cubiertosPorRa = {}
  for (const f of st.utCeModulo) {
    if (f.ut_id === st.utId) continue
    (cubiertosPorRa[f.ra_id] = cubiertosPorRa[f.ra_id] || new Set()).add(f.ce_id)
  }
  return `<div style="display:flex;flex-direction:column;gap:8px">
    ${st.raCatalogo.map(ra => {
      const total = (st.cesByRa[ra.ra_id] || []).length
      const cubiertos = cubiertosPorRa[ra.ra_id]?.size || 0
      const checked = st.rasSel.has(ra.ra_id)
      return `<label style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1.5px solid ${checked?'var(--accent)':'var(--border2)'};border-radius:10px;cursor:pointer;background:${checked?'rgba(201,104,45,.06)':'transparent'}">
        <input type="checkbox" ${checked?'checked':''} onchange="_utAsistenteToggleRa('${esc(ra.ra_id)}',this.checked)"
          style="accent-color:var(--accent);width:16px;height:16px"/>
        <span style="font-weight:800;color:var(--accent2);min-width:36px">${esc(ra.ra_id)}</span>
        <span style="flex:1;font-size:12.5px">${esc(ra.nombre)}</span>
        <span style="font-size:11px;color:var(--text3)">${cubiertos}/${total} criterios ya cubiertos por otras UT</span>
      </label>`
    }).join('')}
    ${!st.raCatalogo.length ? '<p style="color:var(--text2);font-size:13px">Este módulo no tiene RA en el catálogo.</p>' : ''}
  </div>`
}

function _utAsistenteToggleRa(raId, checked) {
  const st = _utAsistente
  if (!st) return
  if (checked) st.rasSel.add(raId); else st.rasSel.delete(raId)
  const btn = document.getElementById('ut-asis-continuar')
  if (btn) btn.disabled = !_pasoAsistenteValido()
}

function _pasoAsistente3() {
  const st = _utAsistente
  const otrasUtPorCe = {}
  for (const f of st.utCeModulo) {
    if (f.ut_id === st.utId) continue
    otrasUtPorCe[`${f.ra_id}|${f.ce_id}`] = f.ut_id
  }
  const rasSeleccionados = st.raCatalogo.filter(r => st.rasSel.has(r.ra_id))
  return `
    <label style="display:flex;align-items:center;gap:8px;margin-bottom:14px;font-size:12px;color:var(--text2);cursor:pointer">
      <input type="checkbox" id="ut-asis-solo-sin-cubrir" ${st.soloSinCubrir?'checked':''}
        onchange="_utAsistenteToggleSoloSinCubrir(this.checked)" style="accent-color:var(--accent)"/>
      Mostrar solo los que siguen sin cubrir
    </label>
    ${rasSeleccionados.map(ra => {
      const ces = st.cesByRa[ra.ra_id] || []
      const seleccionados = st.cesPorRa[ra.ra_id] || new Set()
      const visibles = ces.filter(ce => !st.soloSinCubrir || !otrasUtPorCe[`${ra.ra_id}|${ce.id}`])
      if (st.soloSinCubrir && !visibles.length) return ''
      return `<div style="margin-bottom:16px">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
          <span style="font-weight:800;color:var(--accent2)">${esc(ra.ra_id)}</span>
          <span style="font-size:11px;color:var(--text2);flex:1">${esc(ra.nombre)}</span>
          <button type="button" onclick="_utAsistenteMarcarSinCubrir('${esc(ra.ra_id)}')"
            style="font-size:10.5px;padding:2px 9px;border-radius:8px;border:1.5px solid var(--accent);background:transparent;color:var(--accent);font-weight:700;cursor:pointer">
            Marcar los sin cubrir
          </button>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2px 16px">
          ${visibles.map(ce => {
            const checked = seleccionados.has(ce.id)
            const otraUt = otrasUtPorCe[`${ra.ra_id}|${ce.id}`]
            return `<label style="display:flex;align-items:flex-start;gap:6px;padding:3px 0;cursor:pointer">
              <input type="checkbox" ${checked?'checked':''}
                onchange="_utAsistenteToggleCe('${esc(ra.ra_id)}','${esc(ce.id)}',this.checked)"
                style="margin-top:2px;accent-color:var(--accent)"/>
              <span style="font-size:11px;color:var(--text2);line-height:1.35">
                <b style="color:var(--accent)">${esc(ce.id)}</b> ${esc(ce.texto)}
                ${otraUt ? `<span style="color:var(--amber)"> · ya en ${esc(otraUt)}</span>` : ''}
              </span>
            </label>`
          }).join('')}
        </div>
      </div>`
    }).join('')}
    ${!rasSeleccionados.length ? '<p style="color:var(--text2);font-size:13px">Vuelve al paso 2 y elige al menos un RA.</p>' : ''}`
}

function _utAsistenteToggleCe(raId, ceId, checked) {
  const st = _utAsistente
  if (!st) return
  const set = (st.cesPorRa[raId] = st.cesPorRa[raId] || new Set())
  if (checked) set.add(ceId); else set.delete(ceId)
  const btn = document.getElementById('ut-asis-continuar')
  if (btn) btn.disabled = !_pasoAsistenteValido()
}

function _utAsistenteMarcarSinCubrir(raId) {
  const st = _utAsistente
  if (!st) return
  const otrasUtPorCe = {}
  for (const f of st.utCeModulo) { if (f.ut_id !== st.utId) otrasUtPorCe[`${f.ra_id}|${f.ce_id}`] = f.ut_id }
  const ces = st.cesByRa[raId] || []
  const set = (st.cesPorRa[raId] = st.cesPorRa[raId] || new Set())
  for (const ce of ces) if (!otrasUtPorCe[`${raId}|${ce.id}`]) set.add(ce.id)
  _renderAsistenteUt()
}

function _utAsistenteToggleSoloSinCubrir(checked) {
  const st = _utAsistente
  if (!st) return
  st.soloSinCubrir = checked
  _renderAsistenteUt()
}

function asistenteUtAtras() {
  const st = _utAsistente
  if (!st || st.paso <= 1) return
  st.paso--
  _renderAsistenteUt()
}

async function asistenteUtContinuar() {
  const st = _utAsistente
  if (!st || !_pasoAsistenteValido()) return
  if (st.paso < 3) { st.paso++; _renderAsistenteUt(); return }
  await _guardarAsistenteUt()
}

async function _guardarAsistenteUt() {
  const st = _utAsistente
  if (!st) return
  const pares = []
  for (const raId of st.rasSel) {
    for (const ceId of (st.cesPorRa[raId] || [])) pares.push({ ra_id: raId, ce_id: ceId })
  }
  try {
    const utId = await window.api.setUnidadTrabajo(st.mid, st.utId, {
      nombre: st.nombre.trim(), horas: st.horas, horasEmpresa: st.horasEmpresa, eval: st.evalNum, tags: st.tags,
    })
    await window.api.setUtCe(st.mid, utId, pares)
    cerrarAsistenteUt()
    showToast(st.utId ? `${utId} actualizada` : `${utId} creada`)
    await loadProgramacion()
  } catch (e) {
    alert('Error guardando la unidad de trabajo: ' + validators.sanitizeErrorMessage(e, 'guardarAsistenteUt'))
  }
}

// ── Crear una actividad desde una UT ──────────────────────────────────────
// El tipo ofrece los siete de tipos-actividad.js; los CE marcados (subconjunto
// de los que trabaja la UT) alimentan actividad_ce.
let _utActividadState = null

async function abrirNuevaActividadUt(mid, utId) {
  mid = parseInt(mid)
  const [misCe, ceCatalogoRows, utsExistentes] = await Promise.all([
    window.api.getUtCe(mid, utId),
    window.api.getCeCatalogo(mid),
    window.api.getUnidadesTrabajo(mid),
  ])
  const ut = utsExistentes.find(u => u.ut_id === utId)
  const textoPorCe = Object.fromEntries(ceCatalogoRows.map(c => [`${c.ra_id}|${c.ce_id}`, c.texto]))
  _utActividadState = {
    mid, utId, evalUt: ut?.eval || 1,
    ces: misCe.map(f => ({ ra_id: f.ra_id, ce_id: f.ce_id, texto: textoPorCe[`${f.ra_id}|${f.ce_id}`] || f.ce_id })),
    marcados: new Set(misCe.map(f => `${f.ra_id}|${f.ce_id}`)),
  }
  document.getElementById('ut-act-title').textContent = `Nueva actividad en ${utId}`
  _renderActividadUt()
  document.getElementById('modal-ut-actividad').showModal()
}

function _renderActividadUt() {
  const st = _utActividadState
  if (!st) return
  const tiposHtml = TIPOS_ACTIVIDAD.map(t => `<option value="${t.id}">${esc(t.label)}</option>`).join('')
  const cesHtml = st.ces.length
    ? st.ces.map(ce => {
        const key = `${ce.ra_id}|${ce.ce_id}`
        const checked = st.marcados.has(key)
        return `<label style="display:flex;align-items:flex-start;gap:6px;padding:3px 0;cursor:pointer">
          <input type="checkbox" ${checked?'checked':''} onchange="_utActividadToggleCe('${esc(key)}',this.checked)"
            style="margin-top:2px;accent-color:var(--accent)"/>
          <span style="font-size:11px;color:var(--text2);line-height:1.35">
            <b style="color:var(--accent)">${esc(ce.ra_id)}|${esc(ce.ce_id)}</b> ${esc(ce.texto)}
          </span>
        </label>`
      }).join('')
    : `<p style="font-size:12px;color:var(--amber)">Esta UT no tiene ningún criterio asignado todavía: asígnaselos desde el asistente antes de crear actividades.</p>`

  document.getElementById('ut-act-body').innerHTML = `
    <div class="field" style="margin-bottom:12px">
      <label for="ut-act-desc">Descripción</label>
      <input id="ut-act-desc" type="text" placeholder="Ej. Práctica de instalación en máquina virtual" style="width:100%"/>
    </div>
    <div style="display:flex;gap:14px;margin-bottom:14px">
      <div class="field" style="flex:1">
        <label for="ut-act-tipo">Tipo</label>
        <select id="ut-act-tipo" style="width:100%">${tiposHtml}</select>
      </div>
      <div class="field" style="width:100px">
        <label for="ut-act-peso">Peso %</label>
        <input id="ut-act-peso" type="number" min="0" max="100" value="0"/>
      </div>
      <div class="field" style="width:100px">
        <label for="ut-act-notamax">Nota máx</label>
        <input id="ut-act-notamax" type="number" min="1" value="10"/>
      </div>
    </div>
    <div style="font-size:11px;color:var(--text2);margin-bottom:6px">¿Qué criterios de ${esc(st.utId)} evalúa esta actividad?</div>
    ${cesHtml}
  `
}

function _utActividadToggleCe(key, checked) {
  const st = _utActividadState
  if (!st) return
  if (checked) st.marcados.add(key); else st.marcados.delete(key)
}

async function guardarActividadUt() {
  const st = _utActividadState
  if (!st) return
  const descripcion = document.getElementById('ut-act-desc').value.trim()
  if (!descripcion) { alert('Ponle una descripción a la actividad.'); return }
  const tipo = document.getElementById('ut-act-tipo').value
  const peso = parseFloat(document.getElementById('ut-act-peso').value) || 0
  const notaMax = parseFloat(document.getElementById('ut-act-notamax').value) || 10
  if (!st.marcados.size && !confirm('No has marcado ningún criterio: la actividad no evaluará nada. ¿Crearla igual?')) return
  try {
    const raIds = [...new Set([...st.marcados].map(k => k.split('|')[0]))]
    const actId = await window.api.saveActividad({
      modulo_id: st.mid, ut_id: st.utId, ra_id: raIds.length === 1 ? raIds[0] : null,
      descripcion, instrumento: TIPOS_ACTIVIDAD.find(t => t.id === tipo)?.label || tipo,
      tipo, peso, nota_max: notaMax, eval: st.evalUt, orden: 0, ces: [],
    })
    const pares = [...st.marcados].map(k => { const [ra_id, ce_id] = k.split('|'); return { ra_id, ce_id } })
    await window.api.setActividadCe(actId, st.mid, pares)
    cerrarActividadUtModal()
    showToast('Actividad creada')
    await loadProgramacion()
  } catch (e) {
    alert('Error creando la actividad: ' + validators.sanitizeErrorMessage(e, 'guardarActividadUt'))
  }
}

function cerrarActividadUtModal() {
  const dlg = document.getElementById('modal-ut-actividad')
  if (dlg.open) dlg.close()
  _utActividadState = null
}

// ── Modal UT para actividades de examen ──────────────────────────
let _actUtsState = null

async function openActUtsModal(actId, mid, currentUtId) {
  const { uts, asigs, ces } = await _cargarCatalogoNormalizado(mid)
  _actUtsState = { actId, mid, asigs, ces }

  // Título: descripción de la actividad si está disponible
  document.getElementById('act-uts-title').textContent = `Examen · UTs relacionadas`

  const selIds = (currentUtId||'').split(',').filter(Boolean)
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
      const raIds = asigs.filter(a => a.ut === ut.id).map(a => a.ra)
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
  const { actId, mid, asigs, ces } = _actUtsState
  const selected = Array.from(document.querySelectorAll('.act-ut-chk:checked')).map(cb => cb.dataset.utid)
  try {
    const acts = await window.api.getActividades(mid)
    const act = acts.find(a => a.id === actId)
    if (!act) return
    const perdidos = _reasignarUtsActividad(act, selected, asigs, ces)
    await window.api.saveActividad(act)
    await _sincronizarActividadCe(actId, mid, act.ces)
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

async function openActCesModal(actId, mid, utId, raId, currentCesEncoded, convocatoria) {
  const { ras, ces, asigs } = await _cargarCatalogoNormalizado(mid)
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
    ? ras
        .map(ra => ({ raId: ra.id, ces: ces[ra.id] || [] }))
        .filter(g => g.ces.length)
    : cesDisponiblesActividad({ ut_id: utId, ra_id: raId }, asigs, ces)

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
    const raNombre = ras.find(r => r.id === grupo.raId)?.nombre || ''
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
    await _sincronizarActividadCe(actId, mid, selected)
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
  const { uts, asigs, ces: cesPorRa } = await _cargarCatalogoNormalizado(mid)
  const acts = await window.api.getActividades(parseInt(mid))

  // Un examen sin UT no cubre ningún criterio, así que su nota no entra en
  // ningún RA por mucho que se califique. Antes se quedaba fuera de este arreglo
  // («no tiene UT asignada y se queda igual») justo cuando era el que más falta
  // hacía: se le asignan las unidades de su propia evaluación.
  const utsPorEval = {}
  for (const ut of uts) {
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
      await _sincronizarActividadCe(c.act.id, mid, c.claves)
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

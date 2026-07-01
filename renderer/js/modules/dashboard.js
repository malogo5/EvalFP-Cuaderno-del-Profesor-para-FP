// DASHBOARD
// ═══════════════════════════════════════════════════════════════
async function loadDashboard() {
  const mid = document.getElementById('dash-mod-sel').value
  if (!mid) return
  const alumnos = (await window.api.getAlumnos(mid)).filter(a => a.estado === 'Activo')
  const allActividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  const ng = {}
  notasArr.forEach(n => { if(!ng[n.alumno_id])ng[n.alumno_id]={}; ng[n.alumno_id][n.actividad_id]=n.nota })

  // Solo incluir actividades de las evaluaciones activas
  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)
  const actividades = allActividades.filter(a => evals.includes(a.eval))

  // Calcular media global por alumno
  const resumen = alumnos.map(al => {
    const ns = actividades.map(a => ng[al.id]?.[a.id]).filter(n => n!=null)
    const media = ns.length ? ns.reduce((a,b)=>a+b,0)/ns.length : null
    return { ...al, media }
  })

  const conNota = resumen.filter(a => a.media !== null)
  const aptos   = conNota.filter(a => a.media >= 5).length
  const noAptos = conNota.filter(a => a.media < 5).length
  const enRiesgo= conNota.filter(a => a.media >= 4 && a.media < 5).length
  const mediaGlobal = conNota.length ? (conNota.reduce((s,a)=>s+(a.media||0),0)/conNota.length).toFixed(1) : '—'

  const kpis = `<div class="kpi-grid">
    <div class="kpi"><div class="kpi-val">${alumnos.length}</div><div class="kpi-label">Activos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--green)">${aptos}</div><div class="kpi-label">Aptos (≥5)</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--red)">${noAptos}</div><div class="kpi-label">No Aptos</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--amber)">${enRiesgo}</div><div class="kpi-label">En Riesgo</div></div>
    <div class="kpi"><div class="kpi-val">${mediaGlobal}</div><div class="kpi-label">Media Grupo</div></div>
  </div>`

  const filas = resumen.map(a => {
    const m = a.media
    const cls = m===null?'':m>=5?'sem-green':m>=4?'sem-amber':'sem-red'
    const nota = m===null ? '—' : m.toFixed(1)
    const notaCls = m===null?'':m>=5?'nota-apto':m>=4?'nota-riesgo':'nota-noapto'
    return `<tr>
      <td><span class="semaforo ${cls}"></span>${esc(a.apellidos||'')}${a.apellidos&&a.nombre?', ':''}${esc(a.nombre||'')}</td>
      <td style="text-align:center;font-weight:700" class="${notaCls}">${nota}</td>
      <td style="text-align:center">
        <button class="btn btn-ghost btn-sm" onclick="genBoletin(${a.id})">📄 Boletín PDF</button>
      </td>
    </tr>`
  }).join('')

  document.getElementById('dash-content').innerHTML = kpis + `
    <div class="card">
      <div class="card-title">Seguimiento individual</div>
      <div class="tbl-wrap"><table>
        <thead><tr><th>Alumno/a</th><th style="text-align:center;width:80px">Media</th><th style="width:130px"></th></tr></thead>
        <tbody>${filas}</tbody>
      </table></div>
    </div>`
}

async function genBoletin(alumnoId) {
  const a = _alumnos.find(x => x.id === alumnoId) || { apellidos:'', nombre:'' }
  const nombre = `${a.apellidos}, ${a.nombre}`
  // HTML básico del boletín
  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"/>
    <style>body{font-family:Arial,sans-serif;padding:40px;color:#222}
    h1{color:#0f1b2d;border-bottom:2px solid #4a90d9;padding-bottom:8px}
    table{width:100%;border-collapse:collapse;margin-top:20px}
    th{background:#162236;color:#fff;padding:8px;text-align:left}
    td{padding:8px;border-bottom:1px solid #eee}</style></head>
    <body><h1>Boletín de Evaluación</h1>
    <p><b>Alumno/a:</b> ${nombre}</p>
    <p><i>Generado: ${new Date().toLocaleDateString('es-ES')}</i></p>
    </body></html>`
  await window.api.exportBoletin(html, nombre)
}

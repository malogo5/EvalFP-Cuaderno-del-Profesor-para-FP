// EVALUACIONES
// ═══════════════════════════════════════════════════════════════
async function loadEvaluaciones() {
  const mid = document.getElementById('eval-mod-sel').value
  if (!mid) return
  const alumnos = (await window.api.getAlumnos(mid)).filter(a => a.estado === 'Activo')
  const actividades = await window.api.getActividades(mid)
  const notasArr = await window.api.getNotasGrid(mid)
  const ng = {}
  notasArr.forEach(n => { if(!ng[n.alumno_id])ng[n.alumno_id]={}; ng[n.alumno_id][n.actividad_id]=n.nota })

  const modData   = _getModData(mid)
  const evalCount = modData?.modulo?.eval_count || [...new Set(actividades.map(a=>a.eval))].length || 3
  const evals     = Array.from({length: evalCount}, (_, i) => i + 1)

  const html = evals.map(ev => {
    const acts = actividades.filter(a => a.eval === ev)
    const rows = alumnos.map(al => {
      // Media ponderada de actividades de esta evaluación
      let sumPeso = 0, sumNota = 0
      acts.forEach(act => {
        const n = ng[al.id]?.[act.id]
        if (n != null) { sumNota += n * act.peso; sumPeso += act.peso }
      })
      const media = sumPeso > 0 ? (sumNota / sumPeso).toFixed(2) : '—'
      const cls = media==='—' ? '' : media>=5?'nota-apto':media>=4?'nota-riesgo':'nota-noapto'
      return `<tr>
        <td>${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}</td>
        <td style="text-align:center;font-weight:700" class="${cls}">${media}</td>
      </tr>`
    }).join('')

    return `<div class="card">
      <div class="card-title">Evaluación ${ev}</div>
      <div class="tbl-wrap"><table>
        <thead><tr><th>Alumno/a</th><th style="text-align:center;width:100px">Nota EV${ev}</th></tr></thead>
        <tbody>${rows}</tbody>
      </table></div>
    </div>`
  }).join('')

  document.getElementById('eval-content').innerHTML = html || '<div style="color:var(--text2);padding:20px">Sin datos de notas aún.</div>'
}

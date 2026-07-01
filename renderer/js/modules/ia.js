// ASISTENTE IA
// ═══════════════════════════════════════════════════════════════
function iaTab(el, id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'))
  el.classList.add('active')
  IA_TABS.forEach(t => document.getElementById('ia-'+t).style.display = t===id?'':'none')
}

function termAppend(id, d) {
  const el = document.getElementById(id)
  if (el.querySelector('.placeholder')) el.innerHTML = ''
  const line = document.createElement('div')
  if      (d.type==='stdout') { line.className='line-out';  line.textContent=d.text.trimEnd() }
  else if (d.type==='stderr') { line.className='line-err';  line.textContent=d.text.trimEnd() }
  else if (d.type==='done')   { line.className=d.code===0?'line-done':'line-fail'; line.textContent=d.code===0?'✅ Completado':'❌ Error (código '+d.code+')' }
  else                        { line.className='line-err';  line.textContent='⚠️ '+d.text }
  el.appendChild(line)
  el.scrollTop = el.scrollHeight
}

function runIA(cmd) {
  const termId = 'ia-'+cmd+'-term'
  document.getElementById(termId).innerHTML = ''
  const opts = { comando: cmd }
  if (cmd==='rubrica')   { opts.modulo=v('ia-r-mod'); opts.ra=v('ia-r-ra'); opts.proveedor=v('ia-r-prov') }
  if (cmd==='actividad') { opts.modulo=v('ia-a-mod'); opts.ra=v('ia-a-ra'); opts.n=v('ia-a-n'); opts.proveedor=v('ia-a-prov') }
  if (cmd==='informe')   { opts.alumno=v('ia-i-alumno'); opts.notas=v('ia-i-notas'); opts.proveedor=v('ia-i-prov') }
  if (cmd==='todo')      { opts.modulo=v('ia-t-mod'); opts.proveedor=v('ia-t-prov') }
  window.api.genIA(opts)
}
window.api.onIA(d => {
  const active = document.querySelector('#sec-ia .tab.active')?.textContent || ''
  const map = {'📋 Rúbrica':'ia-rubrica-term','🔧 Actividades':'ia-actividad-term','📝 Informe':'ia-informe-term','📄 Apuntes HTML':'ia-apuntes-term','🚀 Todo el módulo':'ia-todo-term'}
  const termId = Object.entries(map).find(([k]) => active.includes(k.slice(3)))?.[1] || 'ia-todo-term'
  termAppend(termId, d)
})

function runApuntes() {
  document.getElementById('ia-apuntes-term').innerHTML = ''
  window.api.genApuntes({ modulo:v('ia-ap-mod'), ut:v('ia-ap-ut').trim()||null, proveedor:v('ia-ap-prov') })
}
window.api.onApuntes(d => termAppend('ia-apuntes-term', d))

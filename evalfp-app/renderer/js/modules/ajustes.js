// AJUSTES
// ═══════════════════════════════════════════════════════════════
async function loadAjustes() {
  const cfg = await window.api.getAllConfig()
  if (cfg.openaiKey)    document.getElementById('cfg-openai').value    = cfg.openaiKey
  if (cfg.anthropicKey) document.getElementById('cfg-anthropic').value = cfg.anthropicKey
  if (cfg.proveedor)    document.getElementById('cfg-prov').value      = cfg.proveedor
}

async function saveAjustes() {
  const keys = { openaiKey:'cfg-openai', anthropicKey:'cfg-anthropic', proveedor:'cfg-prov' }
  for (const [k, id] of Object.entries(keys))
    await window.api.setConfig(k, document.getElementById(id).value)
  const st = document.getElementById('ajustes-ok')
  st.textContent = '✅ Guardado'
  setTimeout(() => st.textContent = '', 2500)
}

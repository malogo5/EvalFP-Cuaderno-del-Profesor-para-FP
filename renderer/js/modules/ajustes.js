// AJUSTES
// ═══════════════════════════════════════════════════════════════
async function loadAjustes() {
  const cfg = await window.api.getAllConfig()
  // Note: API keys are not loaded here for security reasons
  // They are stored in OS keychain and cannot be retrieved
  if (cfg.proveedor) document.getElementById('cfg-prov').value = cfg.proveedor
  document.getElementById('cfg-openai').value = ''
  document.getElementById('cfg-anthropic').value = ''
}

async function saveAjustes() {
  const openai = document.getElementById('cfg-openai').value.trim()
  const anthropic = document.getElementById('cfg-anthropic').value.trim()
  const proveedor = document.getElementById('cfg-prov').value
  
  // Save provider to DB
  await window.api.setConfig('proveedor', proveedor)
  
  // Save API keys securely using keytar
  if (openai || anthropic) {
    try {
      const result = await window.api.saveApiKeys({ openai, anthropic })
      if (result.success) {
        showToast('🔐 API keys guardadas de forma segura', 'success')
      } else {
        showToast('Error: ' + result.error, 'error')
      }
    } catch (e) {
      showToast('Error al guardar keys: ' + e.message, 'error')
    }
  } else {
    showToast('Ingresa al menos una API key', 'warning')
  }
}

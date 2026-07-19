// SPDX-License-Identifier: GPL-3.0-or-later
// AJUSTES
// ═══════════════════════════════════════════════════════════════

function setTheme(name) {
  if (name) {
    document.documentElement.dataset.theme = name
  } else {
    delete document.documentElement.dataset.theme
  }
  document.querySelectorAll('.sb-swatch').forEach(btn => {
    btn.classList.toggle('active', (btn.dataset.themeId || '') === (name || ''))
  })
  window.api.setConfig('theme', name || '').catch(() => {})
}

function _setKeyStatus(elId, hasKey) {
  const el = document.getElementById(elId)
  if (!el) return
  el.textContent  = hasKey ? '✓ configurada' : '✗ no configurada'
  el.style.color  = hasKey ? 'var(--green)' : 'var(--text3)'
}

async function loadAjustes() {
  const cfg = await window.api.getAllConfig()
  if (cfg.proveedor) document.getElementById('cfg-prov').value = cfg.proveedor
  // Mostrar estado de keys (existencia en config, sin revelar el valor)
  _setKeyStatus('cfg-openai-status',    !!(cfg.openaiKey    || cfg.hasOpenAI))
  _setKeyStatus('cfg-anthropic-status', !!(cfg.anthropicKey || cfg.hasAnthropic))
  // Campos siempre vacíos por seguridad — el profesor escribe solo si quiere cambiar
  document.getElementById('cfg-openai').value    = ''
  document.getElementById('cfg-anthropic').value = ''
  // Sincronizar selector de tema con el tema activo
  const activeTheme = cfg.theme || ''
  document.querySelectorAll('.sb-swatch').forEach(btn => {
    btn.classList.toggle('active', (btn.dataset.themeId || '') === activeTheme)
  })
}

async function saveAjustes() {
  const openai    = document.getElementById('cfg-openai').value.trim()
  const anthropic = document.getElementById('cfg-anthropic').value.trim()
  const proveedor = document.getElementById('cfg-prov').value

  // Rate limiting
  if (!rateLimiters.apiKeys.check('saveApiKeys')) {
    alert('Demasiados intentos. Espera un momento.')
    return
  }

  // Validar proveedor
  if (!validators.provider(proveedor)) {
    alert('Proveedor inválido.')
    return
  }

  // Validar formato de claves (solo si se proporcionó una)
  if (openai && !validators.apiKey(openai)) {
    alert('Clave OpenAI inválida (mínimo 10 caracteres).')
    return
  }
  if (anthropic && !validators.apiKey(anthropic)) {
    alert('Clave Anthropic inválida (mínimo 10 caracteres).')
    return
  }

  try {
    // Guardar proveedor en config (no sensible)
    await window.api.setConfig('proveedor', proveedor)

    // Guardar API keys via canal seguro (keytar → fallback DB cifrado)
    // Solo se envían las que el profesor ha escrito en esta sesión
    if (openai || anthropic) {
      const result = await window.api.saveApiKeys({
        openai:    openai    || undefined,
        anthropic: anthropic || undefined,
      })
      if (!result.success) {
        alert('Error guardando las claves: ' + (result.message || 'error desconocido'))
        return
      }
    }

    // Actualizar indicadores de estado
    if (openai)    _setKeyStatus('cfg-openai-status',    true)
    if (anthropic) _setKeyStatus('cfg-anthropic-status', true)

    showSaved()
    document.getElementById('cfg-openai').value    = ''
    document.getElementById('cfg-anthropic').value = ''
  } catch(e) {
    alert('Error guardando ajustes: ' + validators.sanitizeErrorMessage(e, 'saveAjustes'))
    console.error(e)
  }
}

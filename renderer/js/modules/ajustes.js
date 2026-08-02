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
  pintarCopiasSeguridad()
  pintarModulosArchivados()
}

/** Módulos archivados, con su botón para devolverlos al cuaderno. */
async function pintarModulosArchivados() {
  const caja = document.getElementById('archivados-info')
  if (!caja) return
  try {
    const mods = await window.api.getModulosArchivados()
    if (!mods.length) { caja.textContent = 'No hay ningún módulo archivado.'; return }
    caja.innerHTML = mods.map(m => `
      <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-top:1px solid var(--border)">
        <b style="color:var(--accent2)">${esc(m.abrev)}</b>
        <span style="flex:1">${esc(m.nombre)}</span>
        <span style="color:var(--text3);font-size:11px">${esc([m.curso, m.grupo, m.anno].filter(Boolean).join(' · '))}</span>
        <button class="btn btn-ghost btn-sm" onclick="restaurarModulo(${m.id})">↩ Recuperar</button>
      </div>`).join('')
  } catch (e) {
    caja.textContent = 'No se ha podido leer la lista: ' + (e && e.message ? e.message : e)
  }
}

async function restaurarModulo(id) {
  try {
    await window.api.restaurarModulo(id)
    _modulos = await window.api.getModulos()
    showToast('Módulo recuperado')
    pintarModulosArchivados()
  } catch (e) {
    alert('No se ha podido recuperar: ' + (e && e.message ? e.message : e))
  }
}

/** Muestra cuántas copias de seguridad hay y de cuándo es la última. */
async function pintarCopiasSeguridad() {
  const caja = document.getElementById('backups-info')
  if (!caja) return
  try {
    const { carpeta, copias, actual } = await window.api.listBackups()
    if (!copias.length) {
      caja.innerHTML = `Todavía no hay ninguna copia. Se creará al cerrar la aplicación.<br>
        <span style="color:var(--text3)">Carpeta: <code>${carpeta}</code></span>`
      return
    }

    // Qué lleva dentro cada copia. Una base vacía pesa lo mismo que una con un
    // curso entero, así que por el tamaño no se sabe si una copia sirve: se ve
    // al restaurarla, que es el peor momento para enterarse.
    const resumen = c => {
      if (!c.contenido) return '<span style="color:var(--red)">ilegible</span>'
      const { modulos, alumnos, notas } = c.contenido
      if (!modulos && !alumnos && !notas) return '<span style="color:var(--red)">vacía</span>'
      return `${modulos} módulo${modulos === 1 ? '' : 's'} · ${alumnos} alumno/a${alumnos === 1 ? '' : 's'} · ${notas} nota${notas === 1 ? '' : 's'}`
    }
    const filas = copias.slice(0, 6).map(c =>
      `<div style="display:flex;gap:8px;justify-content:space-between;font-size:11px;padding:1px 0">
         <span>${new Date(c.fecha).toLocaleString('es-ES')}</span>
         <span style="color:var(--text3)">${resumen(c)}</span>
       </div>`).join('')

    // Aviso gordo: el cuaderno está vacío pero hay copias con datos dentro.
    const conDatos = copias.find(c => c.contenido && c.contenido.modulos > 0)
    const alarma = (actual && actual.modulos === 0 && conDatos)
      ? `<div style="margin:6px 0;padding:6px 8px;border:1px solid var(--red);border-radius:6px;color:var(--red)">
           ⚠ Ahora mismo no tienes ningún módulo, pero la copia del
           ${new Date(conDatos.fecha).toLocaleString('es-ES')} sí los tiene.
           Cierra EvalFP y sustituye <code>evalfp.db</code> por esa copia si te falta algo.
         </div>`
      : ''

    caja.innerHTML = `<b>${copias.length}</b> copia${copias.length > 1 ? 's' : ''} guardada${copias.length > 1 ? 's' : ''} ·
      la última, del <b>${new Date(copias[0].fecha).toLocaleString('es-ES')}</b><br>
      ${alarma}
      <div style="margin:4px 0 6px">${filas}</div>
      <span style="color:var(--text3)">Carpeta: <code>${carpeta}</code></span>`
  } catch (e) {
    caja.textContent = 'No he podido leer la carpeta de copias: ' + e.message
  }
}

/** Copia de seguridad a demanda, para antes de tocar algo delicado. */
async function crearCopiaSeguridad() {
  const caja = document.getElementById('backups-info')
  if (caja) caja.textContent = 'Creando copia…'
  try {
    await window.api.createBackup()
    await pintarCopiasSeguridad()
    const ok = document.getElementById('ajustes-ok')
    if (ok) { ok.textContent = '✓ Copia creada'; setTimeout(() => { ok.textContent = '' }, 4000) }
  } catch (e) {
    if (caja) caja.textContent = 'No se ha podido crear la copia: ' + e.message
  }
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

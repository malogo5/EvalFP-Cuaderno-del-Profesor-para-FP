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

/**
 * Aviso cuando el llavero del sistema no está disponible.
 *
 * Sin él, la aplicación se niega a guardar las claves de IA —en texto plano no
 * van a ninguna parte—, pero eso no se decía hasta que alguien escribía su clave
 * y pulsaba Guardar. Mejor saberlo al entrar, y con la manera de arreglarlo.
 */
async function pintarLlavero() {
  const caja = document.getElementById('cfg-llavero-aviso')
  if (!caja) return
  try {
    const { available } = await window.api.getKeychainStatus()
    if (available) { caja.style.display = 'none'; return }
    caja.style.display = ''
    caja.innerHTML = `<div style="margin:8px 0;padding:8px 10px;border:1px solid var(--amber);border-radius:8px;font-size:12px;color:var(--text2)">
      <b>El llavero del sistema no está disponible ahora mismo.</b><br>
      Las claves no se pueden guardar: EvalFP no las escribe nunca en texto plano. El asistente
      seguirá funcionando en modo demo. Si esto pasa tras actualizar o reinstalar, suele
      arreglarse recompilando el módulo del llavero:
      <code style="display:block;margin-top:4px">npx electron-rebuild -f -w keytar</code>
    </div>`
  } catch {
    caja.style.display = 'none'
  }
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
  pintarLlavero()
  pintarCopiasSeguridad()
  pintarModulosArchivados()
  pintarFaseEmpresaPython()
  pintarProgramacionNormalizada()
}

/**
 * Fase de empresa del CE de Python (Decreto 79/2025, art. 5.3).
 *
 * El decreto fija la franja —86 a 150 horas en régimen general— y deja el número
 * al centro. Aquí se elige y se reparte entre los cuatro módulos en proporción a
 * su duración; el motor lo lee después como `horas_aula`.
 */
async function pintarFaseEmpresaPython() {
  const inp = document.getElementById('cfg-python-empresa')
  const info = document.getElementById('cfg-python-empresa-info')
  if (!inp) return
  try {
    const cfg = await window.api.getFaseEmpresaPython()
    inp.value = cfg.horas || 0
    info.textContent = cfg.horas
      ? `${cfg.horas} h en empresa · ${cfg.total - cfg.horas} h en el centro`
      : 'No se oferta: las 430 h se imparten en el centro'
  } catch { info.textContent = '' }
}

async function guardarFaseEmpresaPython() {
  const inp = document.getElementById('cfg-python-empresa')
  const info = document.getElementById('cfg-python-empresa-info')
  const h = Number(inp.value) || 0
  try {
    const r = await window.api.setFaseEmpresaPython(h)
    info.textContent = r.horas
      ? `Aplicado a ${r.modulos} módulo(s): ${r.horas} h en empresa`
      : `Aplicado a ${r.modulos} módulo(s): sin fase de empresa`
    info.style.color = 'var(--green)'
  } catch (e) {
    info.textContent = validators.sanitizeErrorMessage(e, 'guardarAjustes')
    info.style.color = 'var(--red)'
  }
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

/**
 * RF-02 · Programación normalizada (docs/rediseno/05-PLAN-MIGRACION.md).
 *
 * Estado de cada módulo: migrado si tiene filas en ra_catalogo, sin migrar si
 * no. Se comprueba módulo a módulo porque la migración en sí no distingue —
 * es una única transacción para toda la base, todo o nada— pero un módulo
 * creado después de migrar la base también aparecería sin migrar, y conviene
 * que se vea aquí en vez de descubrirlo en Programación.
 */
async function pintarProgramacionNormalizada() {
  const caja = document.getElementById('rf02-info')
  if (!caja) return
  caja.textContent = 'Comprobando…'
  try {
    const mods = await window.api.getModulos()
    if (!mods.length) { caja.textContent = 'Todavía no hay ningún módulo.'; return }
    const estados = await Promise.all(mods.map(async m => {
      try { return { m, migrado: (await window.api.getRaCatalogo(m.id)).length > 0 } }
      catch { return { m, migrado: false } }
    }))
    const sinMigrar = estados.filter(e => !e.migrado)
    const filas = estados.map(({ m, migrado }) =>
      `<div style="display:flex;align-items:center;gap:8px;padding:2px 0;font-size:12px">
        <span style="${migrado ? 'color:var(--green)' : 'color:var(--amber)'}">${migrado ? '✓' : '○'}</span>
        <b style="color:var(--accent2)">${esc(m.abrev)}</b>
        <span style="color:var(--text2)">${esc(m.nombre)}</span>
        <span style="color:var(--text3);margin-left:auto">${migrado ? 'migrado' : 'sin migrar'}</span>
      </div>`).join('')
    caja.innerHTML = filas +
      (sinMigrar.length
        ? `<div style="margin-top:8px;font-size:12px;color:var(--amber)">
             ${sinMigrar.length} módulo${sinMigrar.length > 1 ? 's' : ''} sin migrar: en Programación,
             la vista de Resultados de Aprendizaje de ese módulo pedirá migrar antes de poder editarla.
           </div>`
        : `<div style="margin-top:8px;font-size:12px;color:var(--green)">Todos los módulos están migrados.</div>`)
  } catch (e) {
    caja.textContent = 'No se ha podido comprobar: ' + (e && e.message ? e.message : e)
  }
}

/**
 * Dispara la migración a las tablas normalizadas de RF-02. Manual, con
 * confirmación explícita y copia de seguridad previa — nunca automática al
 * abrir la aplicación (la copia la hace main.js, antes de tocar la base:
 * ver db:migrarProgramacionNormalizada). Fail-closed: si cualquier módulo
 * tiene una inconsistencia, no se confirma nada y el mensaje dice cuál y por
 * qué, para poder corregirla y reintentar.
 */
async function migrarProgramacionNormalizadaUI() {
  const caja = document.getElementById('rf02-info')
  if (!confirm(
    'Esto va a migrar la programación de todos los módulos a las tablas normalizadas de RF-02 ' +
    '(ra_catalogo, ce_catalogo, ce_instrumentos_previstos…).\n\n' +
    'Antes se hace una copia de seguridad completa de la base. Si algún módulo tiene una ' +
    'inconsistencia (un criterio o una unidad que ya no existe en su catálogo), la migración ' +
    'no se aplica a ninguno y el mensaje dirá cuál es y por qué.\n\n¿Migrar ahora?')) return

  if (caja) caja.textContent = 'Haciendo copia de seguridad y migrando…'
  try {
    const resumen = await window.api.migrarProgramacionNormalizada()
    showToast('✓ Programación migrada')
    await pintarProgramacionNormalizada()
    // pintarProgramacionNormalizada() acaba de reescribir la caja con el estado
    // por módulo; el recuento de esta migración concreta se antepone, no se
    // pierde debajo de ese refresco.
    if (caja) {
      caja.insertAdjacentHTML('afterbegin', `<div style="font-size:12px;color:var(--green);margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid var(--border)">
        Migrados ${resumen.modulos} módulo${resumen.modulos === 1 ? '' : 's'} ·
        ${resumen.ra_catalogo} RA · ${resumen.ce_catalogo} CE · ${resumen.unidades_trabajo} UT ·
        ${resumen.ut_ce} asignaciones UT→CE · ${resumen.ce_instrumentos_previstos} instrumentos ·
        ${resumen.actividad_ce} relaciones actividad→CE.<br>
        Copia de seguridad previa: <code>${esc(resumen.backup || '')}</code>
      </div>`)
    }
  } catch (e) {
    // El motivo (qué módulo, qué referencia) va en el propio mensaje del
    // error — ver migrarProgramacionNormalizada() en db.js — así que se
    // muestra tal cual, no se sustituye por un genérico.
    if (caja) caja.innerHTML = `<div style="color:var(--red);font-size:12px">La migración no se ha aplicado: ${esc(e.message || String(e))}</div>`
    alert('La migración no se ha aplicado. Detalle:\n\n' + (e.message || e))
  }
}

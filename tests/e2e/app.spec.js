/**
 * Tests E2E — EvalFP App (Electron + Playwright)
 *
 * Flujos cubiertos:
 *   1. Arranque y navegación básica
 *   2. Flujo completo: módulo → alumno → notas → evaluación → PDF
 *
 * Ejecutar:
 *   npm run test:e2e
 *   npx playwright test --headed   (con ventana visible para debug)
 */

'use strict'

const { test, expect, _electron: electron } = require('@playwright/test')
const path = require('path')

// ── Helpers ────────────────────────────────────────────────────────────────
const ALUMNO_APELLIDOS = 'E2E'
const ALUMNO_NOMBRE    = 'Test'

/**
 * Lanza la app y devuelve { electronApp, page }.
 * EVALFP_TEST=1 hace que main.js use un userData temporal por proceso:
 * la BD real del profesor nunca se toca y cada lanzamiento parte de cero.
 */
async function launchApp() {
  const electronApp = await electron.launch({
    args: [path.join(__dirname, '../../main.js')],
    env: { ...process.env, NODE_ENV: 'test', EVALFP_TEST: '1' },
  })
  const page = await electronApp.firstWindow()
  await page.waitForSelector('.nav-item', { timeout: 15_000 })
  await page.waitForFunction(() => typeof window.updateModBadge === 'function')
  // Los alert() nativos bloquean Electron bajo Playwright — neutralizarlos
  await page.evaluate(() => { window.alert = () => {} })
  return { electronApp, page }
}

/**
 * Cierra Electron sin dejar que un proceso atascado bloquee el worker de
 * Playwright. Si el cierre elegante no termina, se fuerza la terminación.
 */
async function closeApp(electronApp) {
  if (!electronApp) return

  let timer
  const closed = await Promise.race([
    electronApp.close().then(() => true).catch(() => true),
    new Promise(resolve => { timer = setTimeout(() => resolve(false), 8_000) }),
  ])
  clearTimeout(timer)

  if (!closed) {
    try { electronApp.process()?.kill('SIGKILL') } catch { /* ya cerrado */ }
  }
}

/**
 * Selecciona el módulo ISO en un <select> dado su id.
 * Los selectores de módulo están ocultos por diseño (la selección se hace en
 * el sidebar), así que se fija el valor por JS y se dispara su onchange.
 */
async function selectIsoModule(page, selId) {
  await page.locator(`#${selId}`).waitFor({ state: 'attached', timeout: 5_000 })
  await page.evaluate((id) => {
    const sel = document.getElementById(id)
    const opts = [...sel.options]
    const iso = opts.find(o => (o.textContent || '').includes('ISO')) || opts[0]
    if (iso && iso.value) {
      sel.value = iso.value
      if (typeof sel.onchange === 'function') sel.onchange()
    }
  }, selId)
  await page.waitForTimeout(300)
}

/** Crea el módulo ISO desde el catálogo prebaked usando la API del preload. */
async function ensureIsoModule(page) {
  const diag = await page.evaluate(async () => {
    const existentes = await window.api.getModulos()
    const previo = existentes.find(m => m.key === 'iso_data')
    if (previo) {
      const acts = await window.api.getActividades(previo.id)
      return { creado: false, mid: previo.id, nActs: acts.length, nActsPayload: null }
    }
    const data = await window.api.getModuloData('iso_data')
    const m = data.modulo
    const mid = await window.api.addModulo({
      key: 'iso_data', abrev: m.abrev, nombre: m.nombre, ciclo: m.ciclo,
      curso: m.curso, anno: m.anno, grupo: 'Grupo E2E',
      horas: m.total_horas || m.horas || 0, decreto: m.decreto || null,
      actividades: data.actividades, data,
    })
    // Refrescar estado global del renderer
    _modulos = await window.api.getModulos()
    _curMod  = _modulos.find(x => x.key === 'iso_data') || _modulos[0]
    updateModBadge()
    const acts = await window.api.getActividades(_curMod.id)
    return { creado: true, mid, midReal: _curMod.id,
             nActsPayload: Array.isArray(data.actividades) ? data.actividades.length : String(typeof data.actividades),
             nActs: acts.length }
  })
  console.log('[e2e setup] módulo ISO:', JSON.stringify(diag))
  if (!diag.nActs) {
    throw new Error(`El módulo ISO se creó SIN actividades (payload=${diag.nActsPayload}, en BD=${diag.nActs}). ` +
      'Las secciones Notas/Evaluaciones no pueden funcionar sin actividades.')
  }
  await page.waitForTimeout(300)
}

// ── Grupo 1: Arranque y navegación ─────────────────────────────────────────
test.describe('Arranque y navegación', () => {
  let electronApp, page

  test.beforeEach(async () => {
    ;({ electronApp, page } = await launchApp())
  })
  test.afterEach(async () => {
    await closeApp(electronApp)
  })

  test('muestra el título EvalFP en el sidebar', async () => {
    const logoText = await page.locator('.logo-mark').textContent()
    expect(logoText).toBe('EvalFP')
  })

  test('arranca en Inicio con la BD de test vacía', async () => {
    // init(): sin módulos → sección "inicio"; con módulos → "inicio".
    // La BD de test (EVALFP_TEST) siempre parte vacía.
    const activeItem = page.locator('.nav-item.active')
    await expect(activeItem).toHaveCount(1)
    await expect(activeItem).toHaveAttribute('data-sec', 'inicio')
    await expect(page.locator('#home-guide')).toContainText('Primeros pasos')
  })

  test('navega a Módulos', async () => {
    await page.click('[data-sec="modulos"]')
    await expect(page.locator('.nav-item.active')).toHaveAttribute('data-sec', 'modulos')
  })

  test('navega a Alumnos', async () => {
    await page.click('[data-sec="alumnos"]')
    await expect(page.locator('.nav-item.active')).toHaveAttribute('data-sec', 'alumnos')
  })

  test('navega a Ajustes', async () => {
    await page.click('[data-sec="ajustes"]')
    await expect(page.locator('.nav-item.active')).toHaveAttribute('data-sec', 'ajustes')
  })

  test('la sección IA se abre sin errores JS en consola', async () => {
    const consoleErrors = []
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text())
    })
    await page.click('[data-sec="ia"]')
    await page.waitForTimeout(1000)
    expect(consoleErrors).toHaveLength(0)
  })
})

// ── Grupo 2: Flujo completo módulo → alumno → notas → PDF ─────────────────
test.describe('Flujo completo', () => {
  let electronApp, page
  let alumnoId = null   // guardamos el id para limpiar al final

  test.beforeAll(async () => {
    ;({ electronApp, page } = await launchApp())
    // Setup: crear el módulo ISO en la BD de test (temporal y vacía)
    await ensureIsoModule(page)
  })

  test.afterAll(async () => {
    // La BD es temporal (EVALFP_TEST) — no hace falta limpiar datos
    await closeApp(electronApp)
  })

  // ── 2a. El módulo ISO existe ─────────────────────────────────────────────
  test('el módulo ISO aparece en el selector de Alumnos', async () => {
    await page.click('[data-sec="alumnos"]')
    const sel = page.locator('#alumnos-mod-sel')
    await sel.waitFor({ state: 'attached', timeout: 5_000 })   // oculto por diseño
    const opts = await sel.locator('option').allTextContents()
    const hasISO = opts.some(t => t.includes('ISO'))
    expect(hasISO, `Opciones disponibles: ${opts.join(', ')}`).toBe(true)
  })

  // ── 2b. Añadir alumno de prueba ──────────────────────────────────────────
  test('añade un alumno de prueba E2E', async () => {
    await page.click('[data-sec="alumnos"]')
    await selectIsoModule(page, 'alumnos-mod-sel')
    await page.waitForTimeout(400)

    // Solo filas reales (con inputs) — la tabla vacía muestra una fila-placeholder
    const filasReales = () => page.locator('#alumnos-table tbody tr').filter({ has: page.locator('input') })
    const countBefore = await filasReales().count()

    await page.click('button:has-text("Añadir alumno")')
    await page.waitForTimeout(400)

    // La nueva fila aparece al final — rellenar apellidos y nombre
    const rows   = page.locator('#alumnos-table tbody tr')
    const newRow = rows.last()

    const apellidosInput = newRow.locator('td:nth-child(2) input')
    const nombreInput    = newRow.locator('td:nth-child(3) input')

    await apellidosInput.fill(ALUMNO_APELLIDOS)
    await apellidosInput.blur()
    await page.waitForTimeout(300)

    await nombreInput.fill(ALUMNO_NOMBRE)
    await nombreInput.blur()
    await page.waitForTimeout(300)

    // Guardar el id para la limpieza posterior
    const onclickAttr = await newRow.locator('button[onclick*="removeAlumno"]').getAttribute('onclick')
    const match = onclickAttr?.match(/removeAlumno\((\d+)/)
    if (match) alumnoId = parseInt(match[1])

    // Verificar que hay una fila real más
    const countAfter = await filasReales().count()
    expect(countAfter).toBe(countBefore + 1)
  })

  // ── 2c. Introducir notas para EV1 ────────────────────────────────────────
  test('introduce notas en EV1 para el alumno de prueba', async () => {
    await page.click('[data-sec="notas"]')
    await selectIsoModule(page, 'notas-mod-sel')

    // Seleccionar EV1 y esperar a que el grid renderice celdas
    await page.locator('#notas-ev-sel').selectOption('1')
    await page.waitForSelector('#notas-grid-wrap input.nota-cell', { timeout: 5_000 })

    // Buscar celdas del alumno de prueba
    // Si tenemos el id lo usamos; si no, buscamos por fila de nombre
    let cells
    if (alumnoId !== null) {
      cells = page.locator(`input.nota-cell[data-aid="${alumnoId}"]`)
    } else {
      // Buscar la fila que contiene el nombre E2E
      const row = page.locator('#notas-grid-wrap tbody tr').filter({ hasText: ALUMNO_APELLIDOS })
      cells = row.locator('input.nota-cell')
    }

    const count = await cells.count()
    expect(count, 'Debe haber al menos 1 celda de nota').toBeGreaterThan(0)

    // Entrar 8 en todas las celdas (valor válido 0-10, independiente del peso)
    for (let i = 0; i < count; i++) {
      const cell = cells.nth(i)
      await cell.fill('8')
      await cell.press('Tab')
      await page.waitForTimeout(150)
    }

    // Verificar que las celdas tienen el valor guardado
    for (let i = 0; i < count; i++) {
      await expect(cells.nth(i)).toHaveValue('8')
    }

    // Regresión: con todas las notas a 8, la media ponderada debe ser
    // exactamente 8.00 — y NUNCA mayor que 10 aunque los pesos de la
    // evaluación no sumen 100 (bug histórico: EV1 de ISO suma 130 → daba 10.40)
    const filaAlumno = page.locator('#notas-grid-wrap tbody tr').filter({ hasText: ALUMNO_APELLIDOS })
    const mediaTxt = await filaAlumno.locator('td').last().textContent()
    const media = parseFloat(mediaTxt)
    expect(media, `Media fuera de escala: ${mediaTxt}`).toBeLessThanOrEqual(10)
    expect(media).toBeCloseTo(8, 2)
  })

  // ── 2d. La evaluación muestra nota calculada ─────────────────────────────
  test('la sección Evaluaciones muestra nota para el alumno de prueba', async () => {
    await page.click('[data-sec="evaluaciones"]')
    await selectIsoModule(page, 'eval-mod-sel')
    await page.waitForTimeout(600)

    // La fila del alumno debe aparecer en 1ª Ordinaria
    const fila = page.locator('#epanel-ord1 tbody tr').filter({ hasText: ALUMNO_APELLIDOS }).first()
    await fila.waitFor({ timeout: 5_000 })
    const contenido = await fila.textContent()

    // H10 — reponderación: con solo la EV1 calificada (todo 8), la nota final
    // debe ser 8.0 (los RA sin nota no computan ni arrastran su peso)…
    expect(contenido).toContain('8.0')
    // …y el resultado debe ser PENDIENTE (quedan RA sin evaluar), nunca NO APTO
    expect(contenido).toContain('PENDIENTE')
    expect(contenido).not.toContain('NO APTO')
  })

  // ── 2e. Exportar PDF de notas ────────────────────────────────────────────
  test('el botón Exportar PDF no lanza error', async () => {
    await page.click('[data-sec="notas"]')
    await selectIsoModule(page, 'notas-mod-sel')
    await page.waitForTimeout(400)

    const consoleErrors = []
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text())
    })

    await page.click('button:has-text("Exportar PDF")')
    await page.waitForTimeout(1500)   // dar tiempo al proceso de generación

    // No debe haber errores JS al pulsar exportar
    expect(consoleErrors).toHaveLength(0)
  })

  // ── 2f. Multi-módulo: el desplegable del sidebar manda ───────────────────
  test('cambiar de módulo en el sidebar actualiza todas las secciones', async () => {
    // Crear un 2º módulo (E2E2) y activarlo como haría el desplegable lateral.
    // Nota: esto solo existe en la BD temporal de tests (EVALFP_TEST), no en la app real.
    const ids = await page.evaluate(async () => {
      const KEY = 'par_data' // clave de datos existente, pero se muestra como "E2E2"
      if (!(await window.api.getModulos()).some(m => m.key === KEY)) {
        const data = await window.api.getModuloData(KEY)
        const m = { ...data.modulo, abrev: 'E2E2', nombre: 'Módulo E2E2 (solo tests)' }
        await window.api.addModulo({
          key: KEY, abrev: m.abrev, nombre: m.nombre, ciclo: m.ciclo,
          curso: m.curso, anno: m.anno, grupo: 'Grupo E2E',
          horas: m.total_horas || m.horas || 0, decreto: m.decreto || null,
          actividades: data.actividades, data,
        })
      }
      _modulos = await window.api.getModulos()
      const iso = _modulos.find(x => x.key === 'iso_data')
      const e2e2 = _modulos.find(x => x.key === KEY)
      selectMod(e2e2.id)   // ← equivale al clic en el desplegable del sidebar
      return { iso: iso.id, e2e2: e2e2.id }
    })
    await page.waitForTimeout(400)

    // Regresión: todas las secciones deben seguir al módulo activo del sidebar
    await page.click('[data-sec="alumnos"]')
    await expect(page.locator('#alumnos-mod-sel')).toHaveValue(String(ids.e2e2))
    // El alumno de ISO no debe aparecer en E2E2 (los nombres van en <input value>,
    // no en texto, así que se comprueba el placeholder de tabla vacía)
    await expect(page.locator('#alumnos-tbody')).toContainText(/Todavía no hay alumnado|Sin alumnos/i)

    await page.click('[data-sec="notas"]')
    await expect(page.locator('#notas-mod-sel')).toHaveValue(String(ids.e2e2))

    await page.click('[data-sec="evaluaciones"]')
    await expect(page.locator('#eval-mod-sel')).toHaveValue(String(ids.e2e2))

    // Volver a ISO: las secciones vuelven a mostrar sus datos
    await page.evaluate(id => selectMod(id), ids.iso)
    await expect(page.locator('#mod-badge-name')).toHaveText('ISO')
    await page.click('[data-sec="alumnos"]')
    await expect(page.locator('#alumnos-mod-sel')).toHaveValue(String(ids.iso))
    // La presencia y el uso del alumno ISO ya se validan en las pruebas previas.
    // Aquí comprobamos únicamente la regresión que motivó este caso: que el
    // cambio del sidebar se propaga a los selectores de todas las secciones.
  })
})

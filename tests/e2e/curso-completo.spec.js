/**
 * Auditoría de usuario — un curso completo en EvalFP
 *
 * No es un test unitario: es el recorrido que hace una profesora desde
 * septiembre hasta la 2ª ordinaria, pinchando la aplicación de verdad.
 *
 *   npx playwright test tests/e2e/curso-completo.spec.js
 *   npx playwright test tests/e2e/curso-completo.spec.js --headed   (para verlo)
 *
 * Deja:
 *   tests/e2e/AUDITORIA_CURSO.md   informe con todo lo que ha encontrado
 *   tests/e2e/capturas/*.png       una captura por fase
 *
 * Trabaja sobre una base de datos temporal (EVALFP_TEST=1): la del profesorado
 * NO se toca en ningún momento.
 *
 * Filosofía: casi nada aborta la ejecución. Cada comprobación anota un hallazgo
 * (ok / aviso / fallo) y el recorrido sigue, para que el informe salga completo.
 * Al final el test falla solo si hay hallazgos de nivel «fallo».
 */

'use strict'

const { test, expect, _electron: electron } = require('@playwright/test')
const path = require('path')
const fs = require('fs')

const CAPTURAS = path.join(__dirname, 'capturas')
const INFORME = path.join(__dirname, 'AUDITORIA_CURSO.md')

const GRUPO_ISO = '1º ASIR A'
const GRUPO_OACE = '2º IO A'

// 12 alumnos con perfiles distintos: la última se dará de baja
const ALUMNADO = [
  'Alarcón Vega, Lucía', 'Bermúdez Soto, Iván', 'Carrasco Nieto, Marta',
  'Delgado Pinto, Hugo', 'Escobar Ramos, Nerea', 'Fuentes Gil, Adrián',
  'Gallardo Mora, Claudia', 'Herrera Pardo, Diego', 'Iglesias Vargas, Sofía',
  'Jiménez Bravo, Mateo', 'Lorenzo Castro, Alba', 'Molina Cid, Rubén',
]

const hallazgos = []
let capN = 0

function anota(nivel, zona, texto, detalle) {
  hallazgos.push({ nivel, zona, texto, detalle: detalle || '' })
  const icono = nivel === 'fallo' ? '✗' : nivel === 'aviso' ? '!' : '·'
  console.log(`  ${icono} [${zona}] ${texto}${detalle ? ' — ' + detalle : ''}`)
}

function comprueba(cond, zona, textoOk, textoMal, detalle) {
  if (cond) anota('ok', zona, textoOk)
  else anota('fallo', zona, textoMal, detalle)
  return !!cond
}

async function captura(page, nombre) {
  fs.mkdirSync(CAPTURAS, { recursive: true })
  capN += 1
  const ruta = path.join(CAPTURAS, `${String(capN).padStart(2, '0')}-${nombre}.png`)
  await page.screenshot({ path: ruta, fullPage: false })
  return path.basename(ruta)
}

test.describe.configure({ mode: 'serial', timeout: 240_000 })

/**
 * Una fase del curso. Si algo se rompe, queda anotado como fallo y el recorrido
 * continúa: interesa más el informe completo que parar en el primer tropiezo.
 */
function fase(titulo, fn) {
  test(titulo, async () => {
    try {
      await fn()
    } catch (e) {
      const msg = String((e && e.message) || e).split('\n')[0].slice(0, 220)
      anota('fallo', 'recorrido', `la fase «${titulo}» se cortó`, msg)
    }
  })
}

test.describe('Un curso completo con EvalFP', () => {
  let electronApp, page
  const erroresConsola = []
  const ctx = {}   // ids que se van necesitando entre fases

  test.beforeAll(async () => {
    electronApp = await electron.launch({
      args: [path.join(__dirname, '../../main.js')],
      env: { ...process.env, NODE_ENV: 'test', EVALFP_TEST: '1' },
    })
    page = await electronApp.firstWindow()
    await page.waitForSelector('.nav-item', { timeout: 20_000 })
    await page.waitForFunction(() => typeof window.updateModBadge === 'function')
    page.setDefaultTimeout(12_000)   // fallar rápido y seguir, en vez de 30 s por clic
    page.on('console', m => {
      if (m.type() === 'error') erroresConsola.push(m.text())
    })
    page.on('pageerror', e => erroresConsola.push('pageerror: ' + e.message))
    // los alert() nativos bloquean Electron bajo Playwright
    await page.evaluate(() => {
      window.__avisos = []
      window.alert = (t) => { window.__avisos.push(String(t)) }
      window.confirm = () => true
    })
  })

  test.afterAll(async () => {
    escribeInforme()
    if (electronApp) {
      let timer
      const ok = await Promise.race([
        electronApp.close().then(() => true).catch(() => true),
        new Promise(r => { timer = setTimeout(() => r(false), 8_000) }),
      ])
      clearTimeout(timer)
      if (!ok) { try { electronApp.process()?.kill('SIGKILL') } catch { /* ya cerrado */ } }
    }
  })

  // ───────────────────────────────────────────────────────────── SEPTIEMBRE ──
  fase('Septiembre · doy de alta mis dos módulos desde el catálogo', async () => {
    await page.click('[data-sec="modulos"]')
    await page.waitForTimeout(400)
    await captura(page, 'inicio-sin-modulos')

    // ── OACE, 2º de Grado Básico: interesa por las horas de aula ──
    await page.locator('button[onclick="openAddModulo()"]:visible').first().click()
    await page.waitForSelector('#modal-add-mod', { state: 'visible', timeout: 5_000 })
    await page.fill('#cat-search', 'OACE')
    await page.waitForTimeout(500)

    const tarjetas = page.locator('#cat-cards .cat-card')
    const nTarjetas = await tarjetas.count()
    comprueba(nTarjetas > 0, 'catálogo', `la búsqueda «OACE» encuentra ${nTarjetas} módulo(s)`,
      'la búsqueda del catálogo no encuentra OACE')

    if (nTarjetas > 0) {
      const textoTarjeta = await tarjetas.first().textContent()
      comprueba(/338h/.test(textoTarjeta), 'catálogo',
        'la tarjeta muestra la duración oficial (338h)',
        'la tarjeta no muestra la duración oficial', textoTarjeta.trim())
      comprueba(/200h aula/.test(textoTarjeta), 'catálogo',
        'la tarjeta distingue las horas de aula (200h aula)',
        'no se ven las horas de aula, que son las que reparten las UT', textoTarjeta.trim())
      await tarjetas.first().click()
      await page.waitForTimeout(400)
      const info = await page.locator('#cat-sel-info').textContent()
      comprueba(/empresa/i.test(info), 'catálogo',
        'al seleccionarlo explica el reparto aula/empresa',
        'la ficha no aclara de dónde salen las horas', info.trim().slice(0, 120))
      await captura(page, 'catalogo-oace')

      await page.fill('#add-mod-grupo', GRUPO_OACE)
      await page.locator('#cat-footer button[onclick="confirmAddModulo()"]:visible').first().click()
      await page.waitForTimeout(1200)
    }

    // ── ISO, 1º ASIR: el módulo real ──
    await page.locator('button[onclick="openAddModulo()"]:visible').first().click()
    await page.waitForSelector('#modal-add-mod', { state: 'visible', timeout: 5_000 })
    await page.fill('#cat-search', 'Implantación de sistemas')
    await page.waitForTimeout(500)
    const tarjetasIso = page.locator('#cat-cards .cat-card')
    if (await tarjetasIso.count() > 0) {
      await tarjetasIso.first().click()
      await page.waitForTimeout(400)
      const info = await page.locator('#cat-sel-info').textContent()
      comprueba(/8 RAs?/.test(info), 'catálogo', 'ISO llega con sus 8 RA del decreto',
        'ISO no muestra los 8 RA esperados', info.trim().slice(0, 120))
      await page.fill('#add-mod-grupo', GRUPO_ISO)
      await page.locator('#cat-footer button[onclick="confirmAddModulo()"]:visible').first().click()
      await page.waitForTimeout(1200)
    }

    const modulos = await page.evaluate(() => window.api.getModulos())
    comprueba(modulos.length === 2, 'módulos', 'los dos módulos quedan dados de alta',
      `esperaba 2 módulos y hay ${modulos.length}`)
    ctx.oace = modulos.find(m => (m.abrev || '').includes('OACE'))
    ctx.iso = modulos.find(m => (m.abrev || '').includes('ISO'))

    // El módulo trae actividades de partida y ningún RA se queda sin ellas
    for (const m of [ctx.iso, ctx.oace].filter(Boolean)) {
      const info = await page.evaluate(async (mid) => {
        const acts = await window.api.getActividades(mid)
        const mods = await window.api.getModulos()
        const mm = mods.find(x => x.id === mid)
        const data = typeof mm.data_json === 'string' ? JSON.parse(mm.data_json) : mm.data_json
        const conAct = new Set(acts.filter(a => a.ra_id).map(a => a.ra_id))
        return {
          nActs: acts.length,
          ras: (data.ras || []).map(r => r.id),
          sinAct: (data.ras || []).map(r => r.id).filter(r => !conAct.has(r)),
          sumaPond: (data.ras || []).reduce((s, r) => s + (r.pond || 0), 0),
          horasUt: (data.uts || []).reduce((s, u) => s + (u.horas || 0), 0),
          horasAula: data.modulo.horas_aula || data.modulo.total_horas,
        }
      }, m.id)
      comprueba(info.nActs > 0, 'alta de módulo', `${m.abrev} llega con ${info.nActs} actividades`,
        `${m.abrev} se ha creado sin actividades`)
      comprueba(info.sinAct.length === 0, 'alta de módulo',
        `${m.abrev}: los ${info.ras.length} RA tienen actividad con la que calificarse`,
        `${m.abrev}: RA sin ninguna actividad`, info.sinAct.join(', '))
      comprueba(info.sumaPond === 100, 'alta de módulo', `${m.abrev}: las ponderaciones suman 100 %`,
        `${m.abrev}: las ponderaciones suman ${info.sumaPond} %`)
      comprueba(info.horasUt === info.horasAula, 'alta de módulo',
        `${m.abrev}: las UT suman las ${info.horasAula} h de aula`,
        `${m.abrev}: las UT suman ${info.horasUt} h y el aula son ${info.horasAula} h`)
    }
    await captura(page, 'modulos-dados-de-alta')
  })

  // ─────────────────────────────────────────────────────────────── ALUMNADO ──
  fase('Septiembre · paso la lista de clase de una vez', async () => {
    await page.click('[data-sec="alumnos"]')
    await page.waitForTimeout(400)
    await page.evaluate(id => window.selectMod(id), ctx.iso.id)
    await page.waitForTimeout(500)

    await page.locator('button[onclick="importAlumnos()"]:visible').first().click()
    await page.waitForSelector('#dlg-import-alumnos', { state: 'visible', timeout: 5_000 })
    await page.fill('#import-alumnos-txt', ALUMNADO.join('\n'))
    await captura(page, 'importar-lista')
    await page.locator('button[onclick="confirmImportAlumnos()"]:visible').first().click()
    await page.waitForTimeout(1500)

    const alumnos = await page.evaluate(id => window.api.getAlumnos(id), ctx.iso.id)
    comprueba(alumnos.length === ALUMNADO.length, 'alumnado',
      `la importación pegando la lista crea ${alumnos.length} alumnos de una vez`,
      `esperaba ${ALUMNADO.length} alumnos y hay ${alumnos.length}`)
    const primera = alumnos[0] || {}
    comprueba(!!(primera.apellidos && primera.nombre), 'alumnado',
      'separa bien apellidos y nombre',
      'la importación no separa apellidos y nombre',
      JSON.stringify(primera).slice(0, 120))
    ctx.alumnos = alumnos

    // La última se traslada de centro en noviembre
    if (alumnos.length) {
      const baja = alumnos[alumnos.length - 1]
      const okBaja = await page.evaluate(async (a) => {
        try { await window.api.saveAlumno({ ...a, estado: 'Baja' }); return true } catch { return false }
      }, baja)
      if (okBaja) {
        ctx.baja = baja
        anota('ok', 'alumnado', `${baja.apellidos} se marca de baja en noviembre`)
      } else {
        anota('aviso', 'alumnado', 'no he podido marcar la baja desde la API de la app')
      }
    }

    // Alumnado también en el módulo de Grado Básico
    await page.evaluate(async (args) => {
      for (const linea of args.lista) {
        const [ape, nom] = linea.split(',').map(s => s.trim())
        await window.api.saveAlumno({ modulo_id: args.mid, apellidos: ape, nombre: nom, estado: 'Activo' })
      }
    }, { mid: ctx.oace.id, lista: ALUMNADO.slice(0, 8) })
    const alumnosOace = await page.evaluate(id => window.api.getAlumnos(id), ctx.oace.id)
    comprueba(alumnosOace.length === 8, 'alumnado',
      'el alumnado de cada módulo va por separado',
      `OACE debería tener 8 alumnos y tiene ${alumnosOace.length}`)
    await captura(page, 'alumnado-iso')
  })

  // ────────────────────────────────────────────────── LAS TRES EVALUACIONES ──
  for (const ev of [1, 2, 3]) {
    fase(`Evaluación ${ev} · pongo las notas y miro cómo va la clase`, async () => {
      await page.click('[data-sec="notas"]')
      await page.waitForTimeout(300)
      await page.evaluate(id => window.selectMod(id), ctx.iso.id)
      await page.waitForTimeout(500)
      await page.locator('#notas-ev-sel').selectOption(String(ev))
      await page.waitForTimeout(800)

      const celdas = page.locator('#notas-grid-wrap input.nota-cell')
      const n = await celdas.count()
      comprueba(n > 0, `evaluación ${ev}`, `la parrilla muestra ${n} celdas de nota`,
        `la parrilla de la evaluación ${ev} sale vacía`)
      if (!n) return

      // La primera celda se rellena pinchando, como en clase; el resto por API
      // para no tardar veinte minutos en 12 alumnos × varias actividades.
      await celdas.first().fill('7')
      await celdas.first().press('Tab')
      await page.waitForTimeout(400)
      await expect(celdas.first()).toHaveValue('7')
      anota('ok', `evaluación ${ev}`, 'escribir una nota en la parrilla la guarda al salir de la celda')

      // Reparto de notas por perfiles. El alumno 2 es la prueba de fuego de la
      // regla de oro: va bien en todo menos en un RA, así que su media aprueba
      // pero no puede salir APTO.
      const resumen = await page.evaluate(async (args) => {
        const acts = await window.api.getActividades(args.mid)
        const raDeAct = Object.fromEntries(acts.map(a => [a.id, a.ra_id]))
        const cells = [...document.querySelectorAll('#notas-grid-wrap input.nota-cell')]
        const base = [9, 7, 8, 5, 6, 7, 10, 6, 7, 3, 8, 7]
        let i = 0
        for (const c of cells) {
          const aid = Number(c.dataset.aid)
          const idx = args.orden.indexOf(aid)
          const ra = raDeAct[Number(c.dataset.actid)]
          let v = base[(idx < 0 ? i : idx) % base.length]
          if (idx === 2 && ra === args.raLlave) v = 3   // regla de oro: un RA a pique
          if (idx === 9) v = 3                          // suspende todo, recuperará
          if (idx === 5 && args.ev === 2) v = 4         // pincha en la 2ª evaluación
          c.value = String(v)
          c.dispatchEvent(new Event('change', { bubbles: true }))
          i++
        }
        await new Promise(r => setTimeout(r, 1200))
        return { puestas: cells.length }
      }, { orden: ctx.alumnos.map(a => a.id), ev, mid: ctx.iso.id, raLlave: 'RA2' })
      anota('ok', `evaluación ${ev}`, `${resumen.puestas} notas registradas`)
      await page.waitForTimeout(1200)

      // La media de la parrilla nunca puede pasar de 10
      const medias = await page.evaluate(() =>
        [...document.querySelectorAll('#notas-grid-wrap tbody tr')]
          .map(tr => parseFloat(tr.querySelector('td:last-child')?.textContent))
          .filter(x => !isNaN(x)))
      const fuera = medias.filter(m => m > 10 || m < 0)
      comprueba(fuera.length === 0, `evaluación ${ev}`,
        `todas las medias están dentro de 0-10 (${medias.length} alumnos)`,
        'hay medias fuera de escala', fuera.join(', '))
      await captura(page, `notas-ev${ev}`)

      // Vista de evaluación: estado de la clase
      await page.click('[data-sec="evaluaciones"]')
      await page.waitForTimeout(800)
      await page.evaluate(e => window.setEvalTab(`ev${e}`), ev)
      await page.waitForTimeout(600)
      const panel = await page.locator(`#epanel-ev${ev}`).textContent().catch(() => '')
      comprueba(panel && panel.length > 50, `evaluación ${ev}`,
        'la pestaña de la evaluación muestra el resumen de la clase',
        `la pestaña de la evaluación ${ev} aparece vacía`)
      if (ev < 3) {
        comprueba(/pendiente/i.test(panel), `evaluación ${ev}`,
          'avisa de los RA que aún están sin evaluar',
          'no distingue lo pendiente en una evaluación intermedia')
      }
      await captura(page, `evaluacion-ev${ev}`)
    })
  }

  // ─────────────────────────────────────────────────────── RECUPERACIONES ──
  fase('Marzo · recupero al alumnado que lleva RA suspensos', async () => {
    await page.click('[data-sec="notas"]')
    await page.waitForTimeout(300)
    await page.locator('#notas-ev-sel').selectOption('1')
    await page.waitForTimeout(600)

    const antes = await page.evaluate(() => {
      const c = document.querySelector('#notas-grid-wrap input.nota-cell')
      return c ? { aid: c.dataset.aid, k: c.dataset.k || c.dataset.act, v: c.value } : null
    })

    const hayModo = await page.evaluate(() => typeof toggleRecMode === 'function')
    if (!hayModo) {
      anota('fallo', 'recuperación', 'no existe el modo recuperación en la parrilla')
      return
    }
    await page.evaluate(() => window.toggleRecMode())
    await page.waitForTimeout(800)
    await captura(page, 'modo-recuperacion')

    const enModoRec = await page.evaluate(() => {
      const w = document.getElementById('notas-grid-wrap')
      return /recuperaci/i.test(w ? w.textContent : '')
    })
    comprueba(enModoRec, 'recuperación', 'la parrilla avisa de que estoy en modo recuperación',
      'nada indica que la parrilla está en modo recuperación (riesgo de pisar notas)')

    // Subo la nota del alumno flojo
    const res = await page.evaluate(async (aid) => {
      const cells = [...document.querySelectorAll('#notas-grid-wrap input.nota-cell')]
        .filter(c => Number(c.dataset.aid) === aid)
      for (const c of cells.slice(0, 3)) {
        c.value = '5'
        c.dispatchEvent(new Event('change', { bubbles: true }))
      }
      await new Promise(r => setTimeout(r, 1200))
      return cells.length
    }, ctx.alumnos[9].id)
    anota('ok', 'recuperación', `${res} celdas del alumno con RA suspensos disponibles para recuperar`)

    await page.evaluate(() => window.toggleRecMode())
    await page.waitForTimeout(800)
    const despues = await page.evaluate(() => {
      const c = document.querySelector('#notas-grid-wrap input.nota-cell')
      return c ? { aid: c.dataset.aid, v: c.value } : null
    })
    if (antes && despues && antes.aid === despues.aid) {
      comprueba(antes.v === despues.v, 'recuperación',
        'la nota original se conserva al recuperar (queda el rastro de las dos)',
        'la recuperación ha sobrescrito la nota original',
        `antes ${antes.v} → después ${despues.v}`)
    }
  })

  // ─────────────────────────────────────────────────────────── 1ª ORDINARIA ──
  fase('Junio · cierro la 1ª ordinaria y miro las actas', async () => {
    await page.click('[data-sec="evaluaciones"]')
    await page.waitForTimeout(500)
    await page.evaluate(() => window.setEvalTab('ord1'))
    await page.waitForTimeout(1000)
    await captura(page, 'ordinaria-1')

    const filas = await page.evaluate(() =>
      [...document.querySelectorAll('#epanel-ord1 tbody tr')].map(tr => ({
        texto: tr.innerText.replace(/\s+/g, ' ').trim(),
        celdas: [...tr.querySelectorAll('td')].map(td => td.innerText.trim()),
      })).filter(f => f.texto))

    comprueba(filas.length > 0, '1ª ordinaria', `el acta lista ${filas.length} filas de alumnado`,
      'la 1ª ordinaria no muestra alumnado')

    // Regla de oro: nadie con un RA suspenso puede salir APTO
    const contradicciones = filas.filter(f => /APTO/.test(f.texto) && !/NO APTO/.test(f.texto)
      && /pendiente|suspens/i.test(f.texto))
    comprueba(contradicciones.length === 0, '1ª ordinaria',
      'nadie aparece como APTO teniendo RA sin superar (regla de oro)',
      'hay alumnado APTO con algún RA suspenso',
      contradicciones.map(c => c.texto.slice(0, 80)).join(' | '))

    // La prueba de fuego: media aprobada pero un RA suspenso ⇒ NO APTO
    const golden = ctx.alumnos[2]
    const filaG = filas.find(f => f.texto.includes(golden.apellidos))
    if (!filaG) {
      anota('fallo', '1ª ordinaria', 'no encuentro en el acta al alumno de la prueba de la regla de oro',
        golden.apellidos)
    } else {
      const nums = filaG.celdas.map(c => parseFloat(c.replace(',', '.'))).filter(x => !isNaN(x))
      const notaFinal = nums.length >= 2 ? nums[nums.length - 2] : null
      comprueba(notaFinal !== null && notaFinal >= 5, '1ª ordinaria',
        `${golden.apellidos} tiene la media aprobada (${notaFinal})`,
        'el caso de prueba no ha quedado con la media aprobada', filaG.texto.slice(0, 100))
      comprueba(/NO APTO/.test(filaG.texto), '1ª ordinaria',
        'con la media aprobada pero un RA suspenso, el resultado es NO APTO (la media no compensa)',
        'REGLA DE ORO INCUMPLIDA: aprueba con un RA suspenso', filaG.texto.slice(0, 120))
    }

    // La columna Acta debe ser un entero
    const actas = filas.map(f => f.celdas[f.celdas.length - 1]).filter(Boolean)
    const noEnteras = actas.filter(a => /^\d+([.,]\d+)$/.test(a))
    comprueba(noEnteras.length === 0, '1ª ordinaria',
      'la calificación de acta sale como número entero',
      'hay calificaciones de acta con decimales', noEnteras.join(', '))

    // El alumnado de baja no debe contaminar el acta sin avisar
    if (ctx.baja) {
      const filaBaja = filas.find(f => f.texto.includes(ctx.baja.apellidos))
      if (!filaBaja) {
        anota('aviso', '1ª ordinaria',
          'el alumnado de baja no aparece en el acta',
          'correcto si tu centro no los lista; revisa que sea lo que quieres')
      } else {
        comprueba(/baja/i.test(filaBaja.texto), '1ª ordinaria',
          'el alumnado de baja aparece marcado como tal',
          'el alumnado de baja se mezcla con el resto sin distintivo',
          filaBaja.texto.slice(0, 90))
      }
    }
  })

  // ─────────────────────────────────────────────────────────── 2ª ORDINARIA ──
  fase('Junio · preparo la 2ª ordinaria solo con lo pendiente', async () => {
    await page.evaluate(() => window.setEvalTab('ord2'))
    await page.waitForTimeout(1000)
    const panel = await page.locator('#epanel-ord2').textContent().catch(() => '')
    comprueba(panel && panel.length > 40, '2ª ordinaria',
      'la 2ª ordinaria muestra a quién le queda algo',
      'la pestaña de 2ª ordinaria aparece vacía')
    const soloPendientes = !/APTO(?!.*NO APTO)/.test(panel) || /pendiente|recuper/i.test(panel)
    comprueba(soloPendientes, '2ª ordinaria',
      'se centra en el alumnado con RA pendientes',
      'la 2ª ordinaria no distingue lo que queda por recuperar')
    await captura(page, 'ordinaria-2')
  })

  // ──────────────────────────────────────────────────────────── DOCUMENTOS ──
  fase('Junio · saco los papeles: boletines y PDF de notas', async () => {
    erroresConsola.length = 0

    await page.click('[data-sec="notas"]')
    await page.waitForTimeout(400)
    await page.locator('button[onclick="exportNotasPDF()"]:visible').first().click()
    await page.waitForTimeout(2500)
    comprueba(erroresConsola.length === 0, 'documentos',
      'exportar el PDF de notas no da error',
      'exportar el PDF de notas lanza errores', erroresConsola.slice(0, 2).join(' | '))

    erroresConsola.length = 0
    await page.click('[data-sec="dashboard"]')
    await page.waitForTimeout(1200)
    const hayBoletin = await page.locator('button:has-text("Boletín"):visible').count()
    comprueba(hayBoletin > 0, 'documentos', 'desde el panel puedo sacar el boletín de cada alumno',
      'no encuentro el botón de boletín en el panel')
    if (hayBoletin > 0) {
      await page.locator('button:has-text("Boletín"):visible').first().click()
      await page.waitForTimeout(2500)
      comprueba(erroresConsola.length === 0, 'documentos',
        'el boletín individual se genera sin errores',
        'el boletín individual lanza errores', erroresConsola.slice(0, 2).join(' | '))
    }
    await captura(page, 'dashboard-boletines')
  })

  // ────────────────────────────────────────────────────────── MULTI-MÓDULO ──
  fase('Todo el curso · cambio de módulo en el lateral y nada se mezcla', async () => {
    await page.click('#mod-badge')
    await page.waitForTimeout(500)
    const opciones = await page.locator('#mod-dropdown').innerText().catch(() => '')
    comprueba(/OACE/.test(opciones) && /ISO/.test(opciones), 'multi-módulo',
      'el desplegable del lateral lista mis dos módulos',
      'el desplegable no muestra los dos módulos', opciones.replace(/\s+/g, ' ').slice(0, 90))

    await page.evaluate(id => window.selectMod(id), ctx.oace.id)
    await page.waitForTimeout(800)

    for (const [sec, sel] of [['alumnos', '#alumnos-mod-sel'], ['notas', '#notas-mod-sel'],
      ['evaluaciones', '#eval-mod-sel'], ['dashboard', '#dash-mod-sel'],
      ['programacion', '#prog-mod-sel']]) {
      await page.click(`[data-sec="${sec}"]`)
      await page.waitForTimeout(700)
      const v = await page.locator(sel).inputValue().catch(() => null)
      comprueba(String(v) === String(ctx.oace.id), 'multi-módulo',
        `${sec} sigue al módulo elegido en el lateral`,
        `${sec} se queda en otro módulo`, `esperaba ${ctx.oace.id} y hay ${v}`)
    }

    // Las notas de ISO no pueden verse desde OACE
    await page.click('[data-sec="notas"]')
    await page.waitForTimeout(700)
    const alumnosVisibles = await page.evaluate(() =>
      [...document.querySelectorAll('#notas-grid-wrap tbody tr')].length)
    comprueba(alumnosVisibles <= 8, 'multi-módulo',
      `en OACE solo veo su alumnado (${alumnosVisibles} filas)`,
      `se están mezclando alumnos entre módulos (${alumnosVisibles} filas)`)
    await captura(page, 'cambio-de-modulo')
  })

  // ──────────────────────────────────────────────────── PROGRAMACIÓN Y RA ──
  fase('Todo el curso · reviso la programación y los criterios del decreto', async () => {
    await page.click('[data-sec="programacion"]')
    await page.waitForTimeout(1000)
    const prog = await page.locator('#prog-panel').textContent().catch(() => '')
    comprueba(prog && prog.length > 100, 'programación',
      'la programación muestra las UT del módulo',
      'la programación aparece vacía')
    await captura(page, 'programacion')

    // ── Coherencia de la elección de RA y CE ──────────────────────────────
    // El plan de actividades, la distribución por evaluaciones y la ficha de
    // cada RA salen del mismo sitio: tienen que decir lo mismo.
    const coherencia = await page.evaluate(() => {
      const texto = el => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '')
      const secciones = Array.from(document.querySelectorAll('#prog-panel .prog-section-title'))
      const distCard = secciones.find(s => /Distribución de RAs/.test(s.textContent))?.closest('.card')
      const raCard = secciones.find(s => /Resultados de Aprendizaje/.test(s.textContent))?.closest('.card')
      // RA por evaluación según la tarjeta de distribución
      const dist = {}
      distCard?.querySelectorAll('div[style*="min-width:180px"]').forEach(col => {
        const ev = (texto(col.querySelector('div')).match(/(\d)ª/) || [])[1]
        if (!ev) return
        dist[ev] = Array.from(col.querySelectorAll('span[style*="min-width:34px"]')).map(s => s.textContent.trim())
      })
      // Evaluación que declara la ficha de cada RA
      const fichas = {}
      raCard?.querySelectorAll('div[style*="border-left:4px solid var(--accent2)"]').forEach(b => {
        const raId = b.querySelector('span')?.textContent.trim()
        const ev = (texto(b).match(/Eval (\d)/) || [])[1]
        if (raId) fichas[raId] = ev || null
      })
      // Contadores de criterios de las actividades: n/total, nunca n > total
      const contadores = Array.from(document.querySelectorAll('#prog-panel button[data-ces]'))
        .map(b => b.textContent.trim())
      const badgeHoras = document.getElementById('ut-horas-badge')?.textContent.trim() || ''
      return { dist, fichas, contadores, badgeHoras }
    })

    const desajustes = Object.entries(coherencia.dist).flatMap(([ev, ras]) =>
      ras.filter(ra => coherencia.fichas[ra] && coherencia.fichas[ra] !== ev)
        .map(ra => `${ra}: distribución dice ${ev}ª y su ficha ${coherencia.fichas[ra]}ª`))
    comprueba(desajustes.length === 0, 'programación',
      'la evaluación de cada RA es la misma en la distribución y en su ficha',
      'un RA aparece en una evaluación distinta según dónde lo mires', desajustes.join(' · '))

    const contadoresMal = coherencia.contadores.filter(t => {
      const m = t.match(/^(\d+)\s*\/\s*(\d+)$/)
      return m && Number(m[1]) > Number(m[2])
    })
    comprueba(contadoresMal.length === 0, 'programación',
      'los criterios marcados en cada actividad nunca superan los disponibles',
      'alguna actividad dice tener más criterios de los que existen', contadoresMal.join(', '))

    comprueba(/✓/.test(coherencia.badgeHoras), 'programación',
      `las horas de las UT cuadran con las del módulo (${coherencia.badgeHoras})`,
      'la suma de horas de las UT no cuadra con la duración del módulo', coherencia.badgeHoras)

    await page.click('[data-sec="modulos"]')
    await page.waitForTimeout(900)
    const ras = await page.locator('#mod-ras-panel').textContent().catch(() => '')
    comprueba(/RA1/.test(ras), 'módulos', 'veo los RA del módulo con sus ponderaciones',
      'el panel de RA no muestra nada')
    const decreto = await page.evaluate(async (mid) => {
      const mods = await window.api.getModulos()
      return (mods.find(m => m.id === mid) || {}).decreto || ''
    }, ctx.oace.id)
    comprueba(/Decreto \d+\/\d{4}/.test(decreto) && !/^RD/.test(decreto), 'módulos',
      'el módulo cita el decreto de Castilla-La Mancha',
      'el módulo no cita el decreto autonómico', decreto.slice(0, 90))
    await captura(page, 'modulos-ra')
  })

  // ──────────────────────────────────────────────────────────────── AJUSTES ──
  fase('Todo el curso · ajustes y copia de seguridad', async () => {
    await page.click('[data-sec="ajustes"]')
    await page.waitForTimeout(800)
    const texto = await page.locator('#sec-ajustes').innerText().catch(() => '')
    comprueba(/copias de seguridad/i.test(texto), 'ajustes',
      'las copias de seguridad están a la vista, con su carpeta',
      'no encuentro nada sobre copias de seguridad')
    const hayBoton = await page.locator('button[onclick="crearCopiaSeguridad()"]:visible').count()
    if (hayBoton) {
      await page.locator('button[onclick="crearCopiaSeguridad()"]').first().click()
      await page.waitForTimeout(2000)
      const info = await page.locator('#backups-info').innerText().catch(() => '')
      comprueba(/copia/i.test(info) && /\d/.test(info), 'ajustes',
        'puedo crear una copia a demanda y me dice cuántas hay y de cuándo',
        'crear la copia no da información de vuelta', info.slice(0, 120))
    } else {
      anota('fallo', 'ajustes', 'no hay botón para crear una copia de seguridad')
    }
    comprueba(/tema|claro|oscuro/i.test(texto), 'ajustes', 'puedo cambiar el tema',
      'no encuentro el cambio de tema')
    await captura(page, 'ajustes')

    erroresConsola.length = 0
    await page.click('[data-sec="ia"]')
    await page.waitForTimeout(1200)
    const ia = await page.locator('#sec-ia').innerText().catch(() => '')
    comprueba(ia.length > 50, 'IA', 'la sección de IA abre sin romperse',
      'la sección de IA aparece vacía')

    // Las pestañas nuevas tienen que abrir y traer el módulo activo
    for (const [tab, sel] of [['plan', '#ia-p-mod'], ['grupo', '#ia-g-mod'], ['examen', '#ia-e-mod'],
      ['corregir', '#ia-c-mod']]) {
      await page.evaluate(t2 => {
        const el = [...document.querySelectorAll('.tab')].find(x => x.getAttribute('onclick')?.includes(`'${t2}'`))
        if (el) el.click()
      }, tab)
      await page.waitForTimeout(400)
      const visible = await page.locator(`#ia-${tab}`).isVisible().catch(() => false)
      const conModulo = await page.locator(sel).locator('option').count().catch(() => 0)
      comprueba(visible && conModulo > 0, 'IA',
        `la pestaña «${tab}» abre con mis módulos cargados`,
        `la pestaña «${tab}» no abre o no tiene módulos`, `visible=${visible} opciones=${conModulo}`)
    }
    // El RA de la prueba escrita se rellena solo desde el módulo
    const nRas = await page.locator('#ia-e-ra option').count().catch(() => 0)
    comprueba(nRas > 0, 'IA', `la prueba escrita ofrece los ${nRas} RA del módulo`,
      'el selector de RA de la prueba escrita sale vacío')
    // Corregir desde foto: sin fotos elegidas no debe dejar lanzar nada
    const alumnosCorr = await page.locator('#ia-c-alumno option').count().catch(() => 0)
    comprueba(alumnosCorr > 1, 'IA', 'la corrección desde foto trae el alumnado del módulo',
      'el selector de alumnado de la corrección sale vacío')
    // El lote tiene dos barreras contra mezclar alumnos: los botones ni siquiera
    // aparecen hasta verificar el reparto, y la función se niega si la llaman igual.
    const botonesLoteVisibles = await page.locator('#ia-c-lote-acciones').isVisible().catch(() => true)
    comprueba(!botonesLoteVisibles, 'IA',
      'los botones del lote no aparecen hasta verificar el reparto de fotos',
      'los botones del lote están disponibles sin haber comprobado qué foto es de quién')
    await page.evaluate(() => { window.__avisos = [] })
    await page.evaluate(() => { try { window.iaCorregirPrimero() } catch { /* da igual */ } })
    await page.waitForTimeout(300)
    const avisosLote = await page.evaluate(() => window.__avisos || [])
    comprueba(avisosLote.some(a => /reparto|fotos/i.test(a)), 'IA',
      'aunque se fuerce, el lote se niega a corregir sin el reparto verificado',
      'el lote arranca sin comprobar qué foto es de quién', avisosLote.join(' | ').slice(0, 90))
    await page.evaluate(() => { window.__avisos = [] })
    await page.locator('button[onclick="runCorreccion()"]').click().catch(() => {})
    await page.waitForTimeout(500)
    const avisos = await page.evaluate(() => window.__avisos || [])
    comprueba(avisos.some(a => /foto/i.test(a)), 'IA',
      'sin fotos seleccionadas avisa en lugar de intentar corregir',
      'deja lanzar la corrección sin fotos', avisos.join(' | ').slice(0, 90))
    await captura(page, 'ia-pestanas-nuevas')

    // Un payload inválido tiene que volver como error visible, no dejar el
    // indicador de «generando…» girando para siempre.
    const respuesta = await page.evaluate(() => new Promise(resolve => {
      const recibido = []
      const tope = setTimeout(() => resolve({ timeout: true, recibido }), 8000)
      window.api.onIA(d => {
        recibido.push(d && d.type)
        if (d && d.type === 'done') { clearTimeout(tope); resolve({ timeout: false, recibido }) }
      })
      try {
        window.api.genIA({ comando: 'rubrica', modulo: 'modulo_que_no_existe', proveedor: 'demo' })
      } catch (e) {
        clearTimeout(tope); resolve({ timeout: false, recibido: ['excepcion'], mensaje: e.message })
      }
    }))
    comprueba(!respuesta.timeout, 'IA',
      'un fallo del proceso principal vuelve como error y libera el indicador',
      'un payload inválido deja el «generando…» girando sin decir nada',
      JSON.stringify(respuesta).slice(0, 120))
    comprueba(erroresConsola.length === 0, 'IA',
      'abrir IA sin clave configurada no lanza errores',
      'abrir la sección de IA lanza errores en consola', erroresConsola.slice(0, 2).join(' | '))
    await captura(page, 'ia')
  })

  // ────────────────────────────────────────────────────────────── VEREDICTO ──
  test('Veredicto de la auditoría', async () => {
    const fallos = hallazgos.filter(h => h.nivel === 'fallo')
    console.log(`\n  Hallazgos: ${hallazgos.filter(h => h.nivel === 'ok').length} correctos · ` +
      `${hallazgos.filter(h => h.nivel === 'aviso').length} avisos · ${fallos.length} fallos`)
    console.log(`  Informe: ${INFORME}`)
    expect(fallos.map(f => `[${f.zona}] ${f.texto}${f.detalle ? ' — ' + f.detalle : ''}`)).toEqual([])
  })

  function escribeInforme() {
    const cuenta = n => hallazgos.filter(h => h.nivel === n).length
    const bloque = (nivel, titulo, icono) => {
      const lista = hallazgos.filter(h => h.nivel === nivel)
      if (!lista.length) return ''
      return `\n## ${titulo}\n\n` + lista.map(h =>
        `- ${icono} **${h.zona}** — ${h.texto}${h.detalle ? `\n  \`${h.detalle}\`` : ''}`).join('\n') + '\n'
    }
    const md = `# Auditoría de usuario · un curso completo en EvalFP

Recorrido automático por la interfaz real de la aplicación, de septiembre a la 2ª ordinaria,
sobre una base de datos temporal. Módulos usados: **ISO** (1º ASIR) y **OACE** (2º de Grado
Básico), con 12 alumnos, una baja a mitad de curso y alumnado que suspende RA.

Ejecutado: ${new Date().toLocaleString('es-ES')}

| | |
|---|---|
| Comprobaciones correctas | ${cuenta('ok')} |
| Avisos | ${cuenta('aviso')} |
| Fallos | ${cuenta('fallo')} |
${bloque('fallo', 'Fallos', '✗')}${bloque('aviso', 'Avisos', '!')}${bloque('ok', 'Lo que funciona', '✓')}
## Capturas

Las ${capN} capturas del recorrido están en \`tests/e2e/capturas/\`.

## Errores de consola durante todo el recorrido

${erroresConsola.length ? erroresConsola.slice(0, 20).map(e => `- \`${e.slice(0, 200)}\``).join('\n') : 'Ninguno.'}
`
    fs.writeFileSync(INFORME, md, 'utf8')
  }
})

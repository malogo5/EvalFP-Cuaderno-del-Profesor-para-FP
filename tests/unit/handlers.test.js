import { describe, expect, it } from 'vitest'
import fs from 'fs'
import path from 'path'

/**
 * El renderer es multi-script: index.html llama a las funciones por su nombre
 * desde onclick/onchange. ESLint no ve el HTML, así que no puede decir si una
 * función sobra o si un botón apunta a algo que no existe — y los dos fallos
 * han pasado ya: un botón que no respondía (los ciclos de Administración) y una
 * función que no llamaba nadie (_iaAlertTypeForCode) escondida entre 111 avisos
 * falsos de no-unused-vars.
 *
 * Este test cierra las tres direcciones:
 *   HTML → JS      : todo manejador apunta a una función que existe.
 *   JS  → HTML     : toda función global la usa alguien.
 *   renderer → API : todo window.api.x() está expuesto en preload.js.
 */

const RAIZ = path.resolve('.')
const leer = rel => fs.readFileSync(path.join(RAIZ, rel), 'utf8')

const html = leer('renderer/index.html')

const ARCHIVOS_JS = [
  'renderer/js/app.js',
  ...fs.readdirSync(path.join(RAIZ, 'renderer/js/modules'))
    .filter(f => f.endsWith('.js'))
    .map(f => `renderer/js/modules/${f}`),
]

const fuentes = Object.fromEntries(ARCHIVOS_JS.map(f => [f, leer(f)]))

/** Funciones declaradas en el nivel superior de cada archivo. */
function funcionesDe(src) {
  const nombres = []
  const re = /^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/gm
  let m
  while ((m = re.exec(src)) !== null) nombres.push(m[1])
  return nombres
}

/**
 * Nombres invocados desde atributos on*= del HTML. Solo llamadas sueltas:
 * `window.api.openOutput()` o `this.close()` son métodos de otro objeto y no
 * tienen que existir como función global.
 */
function manejadoresDelHtml() {
  const nombres = new Set()
  const re = /\son[a-z]+\s*=\s*"([^"]*)"/g
  let m
  while ((m = re.exec(html)) !== null) {
    for (const c of m[1].matchAll(/(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(/g)) nombres.add(c[1])
  }
  return nombres
}

// Globals del navegador y helpers definidos fuera de estos archivos.
const EXTERNOS = new Set([
  'alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'String', 'Number',
  'JSON', 'Boolean', 'Array', 'Object', 'Math', 'Date', 'console', 'event',
  'setTimeout', 'clearTimeout', 'encodeURIComponent', 'decodeURIComponent',
  'esc', 'if', 'return', 'typeof',
])

describe('Manejadores del HTML', () => {
  const declaradas = new Set(Object.values(fuentes).flatMap(funcionesDe))

  it('todo onclick/onchange apunta a una función que existe', () => {
    const rotos = [...manejadoresDelHtml()].filter(n => !EXTERNOS.has(n) && !declaradas.has(n))
    expect(rotos, `botones que llaman a funciones inexistentes: ${rotos.join(', ')}`).toEqual([])
  })
})

describe('Código muerto en el renderer', () => {
  const delHtml = manejadoresDelHtml()

  it('ninguna función global se queda sin que la llame nadie', () => {
    const muertas = []
    for (const [archivo, src] of Object.entries(fuentes)) {
      for (const fn of funcionesDe(src)) {
        if (delHtml.has(fn)) continue
        const escapado = fn.replace(/\$/g, '\\$')
        const patron = new RegExp(`\\b${escapado}\\b`, 'g')
        let usos = 0
        for (const otro of Object.values(fuentes)) usos += (otro.match(patron) || []).length
        // También cuenta si el HTML la nombra fuera de un atributo on*
        usos += (html.match(patron) || []).length
        const declaraciones = (src.match(new RegExp(`function\\s+${escapado}\\s*\\(`, 'g')) || []).length
        if (usos - declaraciones <= 0) muertas.push(`${archivo} → ${fn}()`)
      }
    }
    expect(muertas, `funciones que no usa nadie:\n  ${muertas.join('\n  ')}`).toEqual([])
  })
})

describe('Estado compartido entre scripts', () => {
  it('ninguna variable declarada const se reasigna desde otro archivo', () => {
    // `npx eslint --fix` convirtió una vez `let _alumnos` en `const` porque en
    // app.js nadie la reasigna… pero alumnos.js sí. Con const, la app arranca y
    // se queda en blanco al entrar en Alumnos. ESLint no puede verlo: solo mira
    // un archivo cada vez.
    const rotas = []
    for (const [archivo, src] of Object.entries(fuentes)) {
      for (const m of src.matchAll(/^const\s+([A-Za-z_$][\w$]*)\s*=/gm)) {
        const nombre = m[1].replace(/\$/g, '\\$')
        const asignacion = new RegExp(`(?<![.\\w$])${nombre}\\s*=(?!=)`, 'g')
        for (const [otro, texto] of Object.entries(fuentes)) {
          for (const uso of texto.matchAll(asignacion)) {
            const antes = texto.slice(Math.max(0, uso.index - 6), uso.index)
            if (/(?:const|let|var)\s+$/.test(antes)) continue
            rotas.push(`${m[1]}: const en ${archivo}, reasignada en ${otro}`)
            break
          }
        }
      }
    }
    expect([...new Set(rotas)], `const reasignadas desde otro script:\n  ${rotas.join('\n  ')}`).toEqual([])
  })
})

describe('Puente con el proceso principal', () => {
  it('todo window.api.x() que usa el renderer está expuesto en preload.js', () => {
    const preload = leer('preload.js')
    const expuestos = new Set()
    for (const m of preload.matchAll(/^\s{2}([A-Za-z_$][\w$]*)\s*:/gm)) expuestos.add(m[1])

    const usados = new Set()
    for (const src of [html, ...Object.values(fuentes)]) {
      for (const m of src.matchAll(/window\.api\.([A-Za-z_$][\w$]*)/g)) usados.add(m[1])
    }

    const ausentes = [...usados].filter(n => !expuestos.has(n))
    expect(ausentes, `el renderer llama a window.api.${ausentes.join('/')} y preload.js no lo expone`).toEqual([])
  })
})

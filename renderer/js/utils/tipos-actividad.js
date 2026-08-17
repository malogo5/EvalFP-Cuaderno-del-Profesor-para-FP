// SPDX-License-Identifier: GPL-3.0-or-later
// ═══════════════════════════════════════════════════════════════
// RF-17 · Tipos de actividad y familia de reparto
// ═══════════════════════════════════════════════════════════════
// Fuente única para dos cosas que antes eran listas distintas y podían
// desincronizarse: el TIPO de actividad (lo que elige la docente al crearla,
// y lo que declara como instrumento previsto de un CE en RF-02) y el
// INSTRUMENTO PREVISTO. Son la misma lista.
//
// `calificacion.js` no conoce estos siete valores: solo sabe repartir entre
// dos FAMILIAS, "examen" y "practica" (`pesosPorTipo`, `mediaActividades`,
// `examenesQueDeciden`, todas comparan `a.tipo === 'practica'|'examen'`
// literalmente). Por eso el tipo real nunca llega al motor: antes de
// pasarle una actividad, su `tipo` se sustituye por la familia que le
// corresponde — ver `resolverFamilia` más abajo, que es el único sitio del
// proyecto donde ocurre esa sustitución.

const TIPOS_ACTIVIDAD = [
  { id: 'examen',       label: 'Examen',       familiaDefecto: 'examen' },
  { id: 'practica',     label: 'Práctica',     familiaDefecto: 'practica' },
  { id: 'proyecto',     label: 'Proyecto',     familiaDefecto: 'practica' },
  { id: 'observacion',  label: 'Observación',  familiaDefecto: 'practica' },
  { id: 'exposicion',   label: 'Exposición',   familiaDefecto: 'practica' },
  { id: 'trabajo',      label: 'Trabajo',      familiaDefecto: 'practica' },
  { id: 'cuestionario', label: 'Cuestionario', familiaDefecto: 'examen' },
]

const DEFECTO_FAMILIA = Object.fromEntries(TIPOS_ACTIVIDAD.map(t => [t.id, t.familiaDefecto]))

/**
 * Familia de reparto de un tipo, para un módulo concreto.
 *
 * Jerarquía: override del módulo (`overrides`, de `tipo_familia`) → defecto
 * del tipo (`DEFECTO_FAMILIA`, fijo en código) → 'practica' de cierre.
 *
 * El tercer nivel no debería alcanzarse nunca — el <select> de tipo de
 * actividad solo ofrece los siete valores de TIPOS_ACTIVIDAD —, pero si llega
 * un tipo que ninguna de las dos listas conoce (dato heredado, edición manual
 * de la base), `disparoDeCierre` en `true` es la señal de que se ha
 * clasificado a ciegas, para que quien llame pueda avisar en vez de callarlo.
 *
 * @returns {{familia: 'examen'|'practica', disparoDeCierre: boolean}}
 */
function familiaDeTipo(tipo, overrides) {
  const ov = overrides || {}
  if (Object.prototype.hasOwnProperty.call(ov, tipo)) {
    return { familia: ov[tipo], disparoDeCierre: false }
  }
  if (Object.prototype.hasOwnProperty.call(DEFECTO_FAMILIA, tipo)) {
    return { familia: DEFECTO_FAMILIA[tipo], disparoDeCierre: false }
  }
  return { familia: 'practica', disparoDeCierre: true }
}

/**
 * Copia de `actividades` lista para el motor: `tipo` pasa a ser la FAMILIA
 * (examen|practica) de cada actividad, nunca el tipo real. Cada actividad se
 * clona superficialmente — el array de entrada no se toca, así que quien lo
 * necesite para mostrar el tipo real (Programación) sigue pudiendo.
 *
 * Con una base sin ningún override (`overrides` vacío u omitido) y
 * actividades cuyo tipo ya sea 'practica' o 'examen' —el único caso posible
 * antes de RF-17—, esto es una identidad: el tipo sale igual que entra. Es lo
 * que garantiza que migrar a este camino no cambia ninguna nota ya calculada
 * (ver tests/unit/tipos-actividad.test.js).
 *
 * @returns {{actividades: Array, tiposSinClasificar: string[]}}
 */
function resolverFamilia(actividades, overrides) {
  const sinClasificar = new Set()
  const salida = (actividades || []).map(act => {
    const { familia, disparoDeCierre } = familiaDeTipo(act?.tipo, overrides)
    if (disparoDeCierre) sinClasificar.add(act?.tipo)
    return { ...act, tipo: familia }
  })
  return { actividades: salida, tiposSinClasificar: [...sinClasificar] }
}

/**
 * ÚNICO punto de obtención de actividades listas para el motor. Cualquier
 * pantalla que vaya a pasarle actividades a `contextoModulo`, `pesosPorTipo`
 * o `mediaActividades` llama aquí — no a `window.api.getActividades()` para
 * ese fin —, así no hay un sitio más que se pueda olvidar de resolver la
 * familia. Es el mismo fallo que tuvo `notas.nota_rec ?? nota` repartido en
 * cuatro pantallas distintas, con reglas que acababan divergiendo.
 *
 * Si algún tipo se clasifica por el cierre de 'practica' (ver
 * `familiaDeTipo`), avisa por consola siempre y con un toast si la pantalla
 * tiene uno disponible: no se clasifica en silencio.
 *
 * @returns {Promise<{actividades: Array, actividadesReales: Array}>}
 *   `actividades` lleva el tipo sustituido por familia, lista para el motor.
 *   `actividadesReales` es exactamente lo que devuelve la API, con el tipo
 *   real — para lo que la pantalla necesite mostrarlo (hoy, Programación).
 */
async function getActividadesParaMotor(moduloId) {
  const [actividadesReales, overridesRows] = await Promise.all([
    window.api.getActividades(moduloId),
    window.api.getTipoFamilia(moduloId).catch(() => []),
  ])
  const overrides = Object.fromEntries((overridesRows || []).map(r => [r.tipo, r.familia]))
  const { actividades, tiposSinClasificar } = resolverFamilia(actividadesReales, overrides)
  if (tiposSinClasificar.length) {
    const msg = `Tipo de actividad sin familia configurada, tratado como práctica: ${tiposSinClasificar.join(', ')}`
    console.warn('[RF-17]', msg)
    if (typeof showToast === 'function') showToast('⚠ ' + msg, 6000)
  }
  return { actividades, actividadesReales }
}

// Exportado también para los tests y para db.js (en el navegador `module` no
// existe). `getActividadesParaMotor` se incluye por completitud — solo tiene
// sentido llamarla desde el renderer (usa `window.api`), pero declararla no
// tiene ningún coste en Node mientras nadie la invoque desde ahí.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    TIPOS_ACTIVIDAD, DEFECTO_FAMILIA, familiaDeTipo, resolverFamilia, getActividadesParaMotor,
  }
}

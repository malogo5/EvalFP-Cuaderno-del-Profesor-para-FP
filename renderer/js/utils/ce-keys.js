// SPDX-License-Identifier: GPL-3.0-or-later
// ═══════════════════════════════════════════════════════════════
// Identidad de los criterios de evaluación
// ═══════════════════════════════════════════════════════════════
// Los decretos numeran los criterios DENTRO de cada resultado de aprendizaje:
// RA1 tiene CR1…CR10 y RA2 vuelve a empezar por CR1. Es decir, "CR1" a secas no
// señala a ningún criterio concreto del módulo: hace falta el par RA + CE.
//
// Por eso todo lo que guarde criterios (los de una actividad, los perdones, las
// notas de 2ª ordinaria) usa la clave compuesta "RA1|CR1".

/** Clave canónica de un criterio dentro de su RA. */
function ceKey(raId, ceId) {
  return `${raId}|${ceId}`
}

/** Parte RA de una clave compuesta (null si la clave es antigua, sin RA). */
function ceKeyRa(clave) {
  const i = String(clave).indexOf('|')
  return i < 0 ? null : String(clave).slice(0, i)
}

/** Parte CE de una clave compuesta (o la clave entera si es antigua). */
function ceKeyCe(clave) {
  const s = String(clave)
  const i = s.indexOf('|')
  return i < 0 ? s : s.slice(i + 1)
}

/** Criterios de una actividad, ya parseados. Nunca lanza. */
function actCesLista(act) {
  if (!act) return []
  const bruto = act.ces
  if (Array.isArray(bruto)) return bruto
  try {
    const l = JSON.parse(bruto || '[]')
    return Array.isArray(l) ? l : []
  } catch { return [] }
}

/**
 * RAs que evalúa una actividad: los de sus UTs (una actividad de examen puede
 * cubrir varias) y, si no tiene UT, el ra_id que lleve asignado.
 */
function rasDeActividad(act, asignaciones) {
  const utIds = String(act?.ut_id || '').split(',').map(s => s.trim()).filter(Boolean)
  if (utIds.length) {
    const ras = []
    for (const a of (asignaciones || [])) {
      if (utIds.includes(a.ut) && !ras.includes(a.ra)) ras.push(a.ra)
    }
    if (ras.length) return ras
  }
  return act?.ra_id ? [String(act.ra_id)] : []
}

/**
 * ¿Esta actividad evalúa ese criterio de ese RA?
 * Acepta claves antiguas sin RA, pero solo cuando la actividad pertenece sin
 * ambigüedad a ese RA: así una clave "CR1" heredada nunca contamina a otro RA.
 */
function actCubreCe(act, raId, ceId) {
  const lista = actCesLista(act)
  if (!lista.length) return false
  if (lista.includes(ceKey(raId, ceId))) return true
  if (lista.includes(ceId)) return String(act?.ra_id || '') === String(raId)
  return false
}

/**
 * ¿Esta actividad califica ese RA? Tres caminos, y valen los tres:
 *  · lleva el RA asignado directamente (ra_id),
 *  · tiene marcados criterios de ese RA,
 *  · o sus UT trabajan ese RA (caso del examen que cubre varias unidades, que se
 *    queda sin ra_id justo porque no es de uno solo).
 */
function actividadDeRa(act, raId, raCeList, asignaciones) {
  if (String(act?.ra_id || '') === String(raId)) return true
  if ((raCeList || []).some(ce => actCubreCe(act, raId, ce.id))) return true
  return rasDeActividad(act, asignaciones).includes(raId)
}

/** Criterios que una actividad evalúa de un RA concreto (ids sin el prefijo). */
function actCesDeRa(act, raId) {
  const lista = actCesLista(act)
  const salida = []
  for (const clave of lista) {
    const ra = ceKeyRa(clave)
    if (ra === raId) salida.push(ceKeyCe(clave))
    else if (ra === null && String(act?.ra_id || '') === String(raId)) salida.push(ceKeyCe(clave))
  }
  return salida
}

/**
 * Traduce los criterios antiguos de una actividad a claves compuestas.
 * Devuelve la lista nueva, o null si no hacía falta tocar nada.
 *
 * Un id suelto se resuelve contra los RAs que la actividad evalúa de verdad:
 *  · un solo RA candidato  → clave inequívoca
 *  · varios (examen que cubre dos UTs) → se conserva en todos los que tengan
 *    ese criterio, que es exactamente lo que la pantalla venía mostrando
 *  · ninguno → se descarta, porque apuntaba a una UT que ya no está asignada
 */
function migrarCesActividad(act, asignaciones, cesPorRa) {
  const lista = actCesLista(act)
  if (!lista.length) return null
  if (lista.every(k => String(k).includes('|'))) return null

  const candidatos = rasDeActividad(act, asignaciones)
  if (!candidatos.length) return null          // sin RA ni UT no hay nada que resolver

  const salida = []
  const push = k => { if (!salida.includes(k)) salida.push(k) }
  for (const bruto of lista) {
    const s = String(bruto)
    if (s.includes('|')) { push(s); continue }
    for (const raId of candidatos) {
      if ((cesPorRa[raId] || []).some(c => c.id === s)) push(ceKey(raId, s))
    }
  }
  return salida
}

/** Criterios disponibles para una actividad: [{raId, ces:[{id,texto}]}]. */
function cesDisponiblesActividad(act, asignaciones, cesPorRa) {
  const utIds = String(act?.ut_id || '').split(',').map(s => s.trim()).filter(Boolean)
  const grupos = []
  if (utIds.length) {
    // Una UT puede trabajar varios RA: se agrupan todos, sin perder ninguno.
    for (const asig of (asignaciones || [])) {
      if (!utIds.includes(asig.ut)) continue
      const todos = cesPorRa[asig.ra] || []
      const ces = todos.filter(ce => (asig.ces || []).includes(ce.id))
      if (!ces.length) continue
      const ya = grupos.find(g => g.raId === asig.ra)
      if (ya) ces.forEach(ce => { if (!ya.ces.some(c => c.id === ce.id)) ya.ces.push(ce) })
      else grupos.push({ raId: asig.ra, ces: ces.slice() })
    }
  }
  if (!grupos.length && act?.ra_id) {
    const ces = cesPorRa[act.ra_id] || []
    if (ces.length) grupos.push({ raId: String(act.ra_id), ces: ces.slice() })
  }
  return grupos
}

/**
 * Criterios de un RA que alguna actividad evalúa de verdad.
 *
 * Es la BASE de la media del resultado de aprendizaje, y tiene que ser la misma
 * en todas las convocatorias: si en junio se promedian los criterios evaluados y
 * en la segunda convocatoria todos los del decreto, la misma nota sale distinta y
 * un criterio sin instrumento puede subirla sin haberse evaluado nunca.
 */
function cesEvaluadosDeRa(raId, raCeList, acts) {
  return (raCeList || []).filter(ce => (acts || []).some(a => actCubreCe(a, raId, ce.id)))
}

/**
 * RAs de cada evaluación deducidos de las UT, que son lo que el profesor mueve.
 * Devuelve { "1": [raId, …], … }; un RA repartido entre varias evaluaciones se
 * queda en la primera en la que se trabaja.
 */
function rasPorEvaluacion(data, evalCount) {
  const uts = data?.uts || []
  const asigs = data?.asignaciones || []
  const total = evalCount || data?.modulo?.eval_count ||
    [...new Set(uts.map(u => u.eval || 1))].length || 3
  const mapa = {}
  for (let e = 1; e <= total; e++) mapa[String(e)] = []
  const evalDe = {}
  const utEval = Object.fromEntries(uts.map(u => [u.id, Math.min(Math.max(u.eval || 1, 1), total)]))
  for (const a of asigs) {
    const ev = utEval[a.ut]
    if (!ev) continue
    if (evalDe[a.ra] === undefined || ev < evalDe[a.ra]) evalDe[a.ra] = ev
  }
  // Los RA sin UT asignada conservan la evaluación que dijera el catálogo.
  for (const [ev, lista] of Object.entries(data?.eval_ras || {})) {
    const e = Math.min(Math.max(parseInt(ev, 10) || 1, 1), total)
    for (const raId of (lista || [])) if (evalDe[raId] === undefined) evalDe[raId] = e
  }
  for (const ra of (data?.ras || [])) {
    const ev = evalDe[ra.id]
    if (ev) mapa[String(ev)].push(ra.id)
  }
  return mapa
}

// Exportado también para los tests unitarios (en el navegador `module` no existe)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ceKey, ceKeyRa, ceKeyCe, actCesLista, rasDeActividad, actCubreCe, actCesDeRa,
    actividadDeRa, migrarCesActividad, cesDisponiblesActividad, cesEvaluadosDeRa,
    rasPorEvaluacion,
  }
}

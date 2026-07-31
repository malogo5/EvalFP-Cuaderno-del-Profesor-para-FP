// SPDX-License-Identifier: GPL-3.0-or-later
// ═══════════════════════════════════════════════════════════════
// MOTOR ÚNICO DE CALIFICACIÓN
// ═══════════════════════════════════════════════════════════════
// Todas las pantallas que muestren una nota —Evaluaciones, Dashboard, el boletín
// en PDF y el asistente de IA— tienen que salir de aquí. Antes cada una hacía su
// propio cálculo y el mismo alumno tenía cuatro notas distintas: 6,25 en
// Evaluaciones, 7,25 en el Dashboard y 6,75 en el boletín que se llevaba a casa.
//
// El criterio que implementa este módulo es el de la Orden 201/2024 de
// Castilla-La Mancha:
//   · art. 2.2 — se verifica la adquisición de los RA conforme a sus criterios;
//   · art. 2.3 — el módulo está superado cuando se alcanzan TODOS los RA;
//   · art. 25.4 — la calificación es numérica, de 1 a 10, sin decimales;
//   · art. 25.5 — si no se superan todos los RA, la calificación máxima es 4.

/**
 * Nota efectiva de una actividad en escala 0-10.
 * Una práctica calificada sobre 5 vale 8 si el alumno saca 4, no 4: `nota_max`
 * es la escala del instrumento, no un adorno.
 */
function notaEnEscala10(nota, notaMax) {
  if (nota == null) return null
  const max = Number(notaMax)
  if (!isFinite(max) || max <= 0 || max === 10) return nota
  return (nota / max) * 10
}

/**
 * Media ponderada de un conjunto de actividades calificadas.
 * Pesa cada actividad por su `peso`. Si ninguna calificada tiene peso, cae a la
 * media por tipo (práctica/examen) con el reparto global del módulo.
 */
function mediaActividades(acts, notasAl, pesoPrac, pesoExam) {
  const graded = acts
    .map(a => ({ a, n: notaEnEscala10(notasAl?.[a.id], a.nota_max) }))
    .filter(x => x.n != null)
  if (!graded.length) return null
  const totW = graded.reduce((s, x) => s + (x.a.peso || 0), 0)
  if (totW > 0) return graded.reduce((s, x) => s + x.n * (x.a.peso || 0), 0) / totW
  const gP = graded.filter(x => x.a.tipo === 'practica').map(x => x.n)
  const gE = graded.filter(x => x.a.tipo === 'examen').map(x => x.n)
  const avgP = gP.length ? gP.reduce((s, n) => s + n, 0) / gP.length : null
  const avgE = gE.length ? gE.reduce((s, n) => s + n, 0) / gE.length : null
  if (avgP !== null && avgE !== null) return avgP * pesoPrac + avgE * pesoExam
  return avgP !== null ? avgP : avgE
}

/** Reparto global práctica/examen del módulo, para cuando no hay pesos por actividad. */
function pesosPorTipo(actividades) {
  const sP = actividades.filter(a => a.tipo === 'practica').reduce((s, a) => s + (a.peso || 0), 0)
  const sE = actividades.filter(a => a.tipo === 'examen').reduce((s, a) => s + (a.peso || 0), 0)
  const t = sP + sE
  return t > 0 ? { PRAC: sP / t, EXAM: sE / t } : { PRAC: 0.30, EXAM: 0.70 }
}

/**
 * Peso total declarado en una lista de criterios; 0 si alguno no lo tiene.
 * Mezclar criterios con peso y sin peso daría una media que no significa nada,
 * así que en ese caso se usa el reparto a partes iguales.
 */
function _pesoTotal(ces) {
  let total = 0
  for (const ce of ces) {
    const p = Number(ce.peso)
    if (!isFinite(p) || p <= 0) return 0
    total += p
  }
  return total
}

/** Nota de un criterio de evaluación dentro de su RA. */
function notaCE(raId, ceId, acts, notasAl, pesoPrac, pesoExam) {
  const ceActs = acts.filter(a => actCubreCe(a, raId, ceId))
  if (!ceActs.length) return null
  return mediaActividades(ceActs, notasAl, pesoPrac, pesoExam)
}

/**
 * Nota de un resultado de aprendizaje.
 * Si hay criterios evaluados, es la media de sus notas —esa es la evaluación por
 * criterios que pide la norma—. Si no hay ninguno, caen las actividades del RA.
 */
function notaRA(raId, raCeList, acts, notasAl, pesoPrac, pesoExam, asigs) {
  const evaluados = cesEvaluadosDeRa(raId, raCeList, acts)
  if (evaluados.length) {
    // Cada criterio puede llevar su propio peso dentro del RA, como exige el
    // art. 4.3.a de la Orden 201/2024. Sin peso declarado, todos valen igual.
    let sumaN = 0, sumaP = 0, cuenta = 0, simple = 0
    for (const ce of evaluados) {
      const g = notaCE(raId, ce.id, acts, notasAl, pesoPrac, pesoExam)
      if (g === null) continue
      const p = Number(ce.peso)
      if (isFinite(p) && p > 0) { sumaN += g * p; sumaP += p }
      simple += g; cuenta++
    }
    if (!cuenta) return null
    return sumaP > 0 && sumaP === _pesoTotal(evaluados) ? sumaN / sumaP : simple / cuenta
  }
  const raActs = acts.filter(a => actividadDeRa(a, raId, raCeList, asigs))
  if (!raActs.length) return null
  return mediaActividades(raActs, notasAl, pesoPrac, pesoExam)
}

/** ¿Algún examen del RA por debajo del mínimo exigido en la programación? */
function raMinExamKO(raId, raCeList, acts, notasAl, minExam, asigs) {
  if (minExam == null) return false
  const raActs = acts.filter(a => actividadDeRa(a, raId, raCeList, asigs))
  return raActs.some(a =>
    a.tipo === 'examen' &&
    notasAl?.[a.id] != null &&
    notaEnEscala10(notasAl[a.id], a.nota_max) < minExam)
}

/**
 * Calificación de acta: entero, ≥0,5 al alza (art. 25.4).
 * Si el módulo no está superado, el tope es 4 (art. 25.5).
 */
function actaEntera(media, superado) {
  if (media === null || media === undefined) return null
  const r = Math.floor(media + 0.5)
  return superado ? Math.min(10, Math.max(5, r)) : Math.max(1, Math.min(4, r))
}

/**
 * Contexto de cálculo de un módulo. Se construye una vez por pantalla y se pasa
 * a `estadoModulo` para cada alumno.
 *
 * @param {Object}   d
 * @param {Array}    d.ras          RAs con su ponderación ya resuelta
 * @param {Object}   d.cesByRa      { RA1: [{id,texto}, …] }
 * @param {Array}    d.asignaciones [{ut, ra, ces:[…]}]
 * @param {Array}    d.actividades  actividades del módulo
 * @param {?number}  d.minExam      mínimo de examen (null = sin mínimo)
 * @param {?Object}  d.rasSuperados { raId: nota } de los RA cerrados como
 *                                  superados en una sesión anterior
 */
function contextoModulo({ ras, cesByRa, asignaciones, actividades, minExam, rasSuperados }) {
  const acts = actividades || []
  const { PRAC, EXAM } = pesosPorTipo(acts)
  const rasBase = ras || []
  return {
    ras: rasBase,
    cesByRa: cesByRa || {},
    asigs: asignaciones || [],
    actividades: acts,
    minExam: minExam == null ? null : minExam,
    rasSuperados: rasSuperados || null,
    PRAC, EXAM,
    // Un RA está en juego si alguna actividad lo califica, por ra_id, por
    // criterios marcados o por sus unidades de trabajo.
    rasActivos: rasBase.filter(ra =>
      acts.some(a => actividadDeRa(a, ra.id, (cesByRa || {})[ra.id] || [], asignaciones || []))),
  }
}

/**
 * Estado completo de un alumno en el módulo: nota por RA, nota final, RA
 * pendientes, RA sin calificar y veredicto.
 *
 * · La nota final es la media de los RA ponderada por su peso, reponderada sobre
 *   los RA ya evaluados: un RA que aún no se ha trabajado no cuenta como cero.
 * · El veredicto aplica el art. 2.3: hacen falta TODOS los RA alcanzados. La
 *   media no compensa un RA suspenso.
 *
 * @param {Object} ctx        el de `contextoModulo`
 * @param {Object} notasAl    { actividad_id: nota } del alumno
 * @param {Object} [opts]
 * @param {Function} [opts.notaRAOverride]  (ra, notaOriginal) → nota  (2ª convocatoria)
 * @param {Function} [opts.minKOOverride]   (ra, minKOOriginal) → bool (2ª convocatoria)
 */
function estadoModulo(ctx, notasAl, opts) {
  const o = opts || {}
  const porRA = {}, conNota = [], pendientes = [], sinNota = []

  ctx.rasActivos.forEach(ra => {
    const ceLst = ctx.cesByRa[ra.id] || []
    let n = notaRA(ra.id, ceLst, ctx.actividades, notasAl, ctx.PRAC, ctx.EXAM, ctx.asigs)
    let minKO = raMinExamKO(ra.id, ceLst, ctx.actividades, notasAl, ctx.minExam, ctx.asigs)
    if (o.notaRAOverride) n = o.notaRAOverride(ra, n)
    if (o.minKOOverride)  minKO = o.minKOOverride(ra, minKO)

    // «Un resultado de aprendizaje superado no se puede volver a evaluar»
    // (Orden 201/2024, art. 4.3.f). Si el RA quedó superado en una sesión de
    // evaluación anterior, una actividad posterior no puede tumbarlo: la nota se
    // mantiene en la del cierre y se avisa de que está congelada.
    // Puede subir —la evaluación continua juega a favor— pero nunca bajar.
    const cierre = ctx.rasSuperados ? ctx.rasSuperados[ra.id] : null
    let congelado = false
    if (cierre != null) {
      if (n === null || n < cierre) { n = cierre; congelado = true }
      if (minKO) { minKO = false; congelado = true }
    }

    porRA[ra.id] = { nota: n, minKO, congelado }
    if (n === null) { sinNota.push(ra.id); return }
    conNota.push({ nota: n, pond: ra.pond || 0 })
    if (n < 5 || minKO) pendientes.push(ra.id)
  })

  const pondSum = conNota.reduce((s, x) => s + x.pond, 0)
  const media = !conNota.length ? null
    : pondSum > 0 ? conNota.reduce((s, x) => s + x.nota * x.pond, 0) / pondSum
    : conNota.reduce((s, x) => s + x.nota, 0) / conNota.length

  const completo = sinNota.length === 0
  const superado = completo && !pendientes.length && media !== null && media >= 5
  return { porRA, media, pendientes, sinNota, completo, superado, acta: actaEntera(media, superado) }
}

// Exportado también para los tests (en el navegador `module` no existe)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    notaEnEscala10, mediaActividades, pesosPorTipo, notaCE, notaRA,
    raMinExamKO, actaEntera, contextoModulo, estadoModulo,
  }
}

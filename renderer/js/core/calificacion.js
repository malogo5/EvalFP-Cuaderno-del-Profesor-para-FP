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

/**
 * Convocatoria de una actividad. Todo lo anterior a la columna `convocatoria`
 * —y cualquier actividad que no la traiga— es de la primera.
 */
function convocatoriaDe(act) {
  const c = Number(act?.convocatoria)
  return isFinite(c) && c >= 2 ? 2 : 1
}

/**
 * ¿Es una prueba objetiva de evaluación completa del módulo?
 *
 * Es la prueba del art. 3.6 de la Orden 201/2024 (redacción de la Orden
 * 55/2026): la que se hace a quien ha perdido el derecho a la evaluación
 * continua y que «incluirá la totalidad de los resultados de aprendizaje a
 * través de sus criterios de evaluación».
 *
 * Se marca en la actividad con `prueba_objetiva`. No basta con que sea un examen:
 * un examen de la 2ª evaluación no evalúa el módulo entero.
 */
function esPruebaObjetiva(act) {
  const v = act?.prueba_objetiva
  return v === 1 || v === true || v === '1'
}

/** Actividades que cuentan en una convocatoria: la 2ª ve también las de la 1ª. */
function actividadesDeConvocatoria(acts, conv) {
  const c = Number(conv) >= 2 ? 2 : 1
  return (acts || []).filter(a => convocatoriaDe(a) <= c)
}

/**
 * Nota de un criterio de evaluación dentro de su RA.
 *
 * En segunda convocatoria el criterio puede tener dos notas: la del curso y la
 * de la actividad de recuperación, que el art. 21.5 exige que sea un instrumento
 * distinto. Vale la mejor de las dos: recuperar no puede empeorar lo que ya se
 * había alcanzado (art. 4.3.f).
 */
function notaCE(raId, ceId, acts, notasAl, pesoPrac, pesoExam, conv) {
  const ceActs = (acts || []).filter(a => actCubreCe(a, raId, ceId))
  if (!ceActs.length) return null
  const ordinaria = ceActs.filter(a => convocatoriaDe(a) === 1)
  const nOrd = ordinaria.length ? mediaActividades(ordinaria, notasAl, pesoPrac, pesoExam) : null
  if (Number(conv) < 2 || !conv) return nOrd

  const recuperacion = ceActs.filter(a => convocatoriaDe(a) === 2)
  const nRec = recuperacion.length ? mediaActividades(recuperacion, notasAl, pesoPrac, pesoExam) : null
  if (nRec === null) return nOrd
  if (nOrd === null) return nRec
  return Math.max(nOrd, nRec)
}

/**
 * Nota de un resultado de aprendizaje.
 * Si hay criterios evaluados, es la media de sus notas —esa es la evaluación por
 * criterios que pide la norma—. Si no hay ninguno, caen las actividades del RA.
 */
function notaRA(raId, raCeList, acts, notasAl, pesoPrac, pesoExam, asigs, conv, notaCEFn) {
  const evaluados = cesEvaluadosDeRa(raId, raCeList, acts)
  if (evaluados.length) {
    // Cada criterio puede llevar su propio peso dentro del RA, como exige el
    // art. 4.3.a de la Orden 201/2024. Sin peso declarado, todos valen igual.
    let sumaN = 0, sumaP = 0, cuenta = 0, simple = 0
    for (const ce of evaluados) {
      const calculada = notaCE(raId, ce.id, acts, notasAl, pesoPrac, pesoExam, conv)
      // La 2ª convocatoria puede aportar por criterio algo que no es una
      // actividad: el criterio que el equipo docente da por alcanzado. Entra por
      // aquí, no por una media aparte, para que las dos convocatorias usen el
      // mismo cálculo y respeten igual la ponderación de cada criterio.
      const g = notaCEFn ? notaCEFn(raId, ce.id, calculada) : calculada
      if (g === null || g === undefined) continue
      const p = Number(ce.peso)
      if (isFinite(p) && p > 0) { sumaN += g * p; sumaP += p }
      simple += g; cuenta++
    }
    if (!cuenta) return null
    return sumaP > 0 && sumaP === _pesoTotal(evaluados) ? sumaN / sumaP : simple / cuenta
  }
  const raActs = (acts || []).filter(a => actividadDeRa(a, raId, raCeList, asigs))
  if (!raActs.length) return null
  const ordinaria = raActs.filter(a => convocatoriaDe(a) === 1)
  const nOrd = ordinaria.length ? mediaActividades(ordinaria, notasAl, pesoPrac, pesoExam) : null
  if (Number(conv) < 2 || !conv) return nOrd
  const recuperacion = raActs.filter(a => convocatoriaDe(a) === 2)
  const nRec = recuperacion.length ? mediaActividades(recuperacion, notasAl, pesoPrac, pesoExam) : null
  if (nRec === null) return nOrd
  if (nOrd === null) return nRec
  return Math.max(nOrd, nRec)
}

/**
 * ¿Algún examen del RA por debajo del mínimo exigido en la programación?
 *
 * En segunda convocatoria manda el examen de recuperación: es el «instrumento de
 * evaluación diferente» del art. 21.5, y si con él se llega al mínimo, el mínimo
 * está alcanzado. Solo si no hay prueba de recuperación se mira la del curso.
 */
function examenesQueDeciden(raId, raCeList, acts, notasAl, asigs, conv) {
  const raActs = (acts || []).filter(a => actividadDeRa(a, raId, raCeList, asigs))
  const examenes = raActs.filter(a => a.tipo === 'examen' && notasAl?.[a.id] != null)
  const ordinarios = examenes.filter(a => convocatoriaDe(a) === 1)
  if (Number(conv) < 2 || !conv) return ordinarios
  const recuperacion = examenes.filter(a => convocatoriaDe(a) === 2)
  return recuperacion.length ? recuperacion : ordinarios
}

/**
 * La peor nota de examen que cuenta para el mínimo, en escala 0-10.
 * `null` si el RA no tiene ningún examen calificado.
 */
function notaExamenDecisiva(raId, raCeList, acts, notasAl, asigs, conv) {
  const exs = examenesQueDeciden(raId, raCeList, acts, notasAl, asigs, conv)
  if (!exs.length) return null
  return Math.min(...exs.map(a => notaEnEscala10(notasAl[a.id], a.nota_max)))
}

function raMinExamKO(raId, raCeList, acts, notasAl, minExam, asigs, conv) {
  if (minExam == null) return false
  const peor = notaExamenDecisiva(raId, raCeList, acts, notasAl, asigs, conv)
  return peor !== null && peor < minExam
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
function contextoModulo({ ras, cesByRa, asignaciones, actividades, minExam, rasSuperados,
                          tieneFaseEmpresa, convocatoria }) {
  const conv = Number(convocatoria) >= 2 ? 2 : 1
  // En la 1ª convocatoria las actividades de recuperación de junio no existen
  // todavía: no pueden entrar en la nota que va al acta de la 1ª.
  const acts = actividadesDeConvocatoria(actividades, conv)
  const { PRAC, EXAM } = pesosPorTipo(acts.filter(a => convocatoriaDe(a) === 1))
  const rasBase = ras || []
  return {
    ras: rasBase,
    cesByRa: cesByRa || {},
    asigs: asignaciones || [],
    actividades: acts,
    convocatoria: conv,
    minExam: minExam == null ? null : minExam,
    rasSuperados: rasSuperados || null,
    tieneFaseEmpresa: !!tieneFaseEmpresa,
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
 * @param {Function} [opts.notaCEOverride]  (raId, ceId, notaCalculada) → nota
 *                                          (criterios dados por alcanzados)
 */
function estadoModulo(ctx, notasAl, opts) {
  const o = opts || {}
  const porRA = {}, conNota = [], pendientes = [], sinNota = []

  // ── Pérdida del derecho a la evaluación continua (art. 3.6) ──────────────
  //
  // «Estas pruebas de evaluación completa del módulo o módulos profesionales
  //  incluirán la totalidad de los resultados de aprendizaje a través de sus
  //  criterios de evaluación, SIN QUE PUEDA CONSIDERARSE LA CONSERVACIÓN DE
  //  CALIFICACIONES PARCIALES obtenidas con anterioridad a la pérdida del
  //  derecho a la evaluación continua.»
  //
  // Es lo contrario de lo que hace un cuaderno de notas por defecto, así que
  // aquí se corta por tres sitios a la vez:
  //   1. solo cuentan las actividades marcadas como prueba objetiva;
  //   2. no se aplican los RA cerrados como superados en sesiones anteriores;
  //   3. no se aplican los criterios dados por alcanzados a mano.
  // Y se exigen TODOS los RA, no solo los que tengan actividad: si la prueba no
  // cubre alguno, el módulo se queda en PENDIENTE en vez de darse por superado.
  const perdidaEC = !!o.evalContinuaPerdida
  const acts = perdidaEC ? ctx.actividades.filter(esPruebaObjetiva) : ctx.actividades
  const cierres = perdidaEC ? null : ctx.rasSuperados
  const ceOverride = perdidaEC ? null : o.notaCEOverride
  const raEnJuego = perdidaEC ? (ctx.ras || []) : ctx.rasActivos

  raEnJuego.forEach(ra => {
    const ceLst = ctx.cesByRa[ra.id] || []
    let n = notaRA(ra.id, ceLst, acts, notasAl, ctx.PRAC, ctx.EXAM, ctx.asigs,
                   ctx.convocatoria, ceOverride)
    let minKO = raMinExamKO(ra.id, ceLst, acts, notasAl, ctx.minExam, ctx.asigs, ctx.convocatoria)

    // «Presentarse a la recuperación no puede salir caro» (art. 4.3.f, que
    // prohíbe volver a evaluar un RA superado). El cálculo por criterio ya se
    // queda con la mejor nota de cada uno, pero se le escapaba un caso: si la
    // prueba de junio evalúa un criterio que durante el curso no llegó a
    // calificarse, ese criterio nuevo entra en la media del RA y podía hundir
    // uno que estaba en 9. Pasaba con solo marcar «todos» los criterios al crear
    // la prueba, que es lo más cómodo de hacer. Así que la nota de la 2ª
    // convocatoria nunca puede quedar por debajo de la que ya había.
    if (ctx.convocatoria >= 2) {
      const n1 = notaRA(ra.id, ceLst, acts, notasAl, ctx.PRAC, ctx.EXAM, ctx.asigs, 1)
      // El «igual» importa: si las dos convocatorias dan la misma nota, la que
      // vale es la del curso. Con un 8 en el examen de mayo y un 2 en el de
      // junio, la nota se quedaba en 8 —bien— pero el mínimo de examen miraba
      // el de junio y dejaba el RA sin alcanzar. Un 8 y un RA suspenso a la vez.
      if (n1 !== null && (n === null || n1 >= n)) {
        n = n1
        minKO = raMinExamKO(ra.id, ceLst, acts, notasAl, ctx.minExam, ctx.asigs, 1)
      }
    }

    if (o.notaRAOverride) n = o.notaRAOverride(ra, n)
    if (o.minKOOverride)  minKO = o.minKOOverride(ra, minKO)

    // «Un resultado de aprendizaje superado no se puede volver a evaluar»
    // (Orden 201/2024, art. 4.3.f). Si el RA quedó superado en una sesión de
    // evaluación anterior, una actividad posterior no puede tumbarlo: la nota se
    // mantiene en la del cierre y se avisa de que está congelada.
    // Puede subir —la evaluación continua juega a favor— pero nunca bajar.
    const cierre = cierres ? cierres[ra.id] : null
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
  // Lo que se ha alcanzado en el centro educativo
  const centroOk = completo && !pendientes.length && media !== null && media >= 5

  // Tres estados, los del art. 12 de la Orden 201/2024. «Superado parcial» es el
  // del alumnado que ha alcanzado todo lo del centro y le falta la fase de
  // formación en empresa; cuenta como superado a efectos de promoción (art. 18.4)
  // y conserva su calificación cuando complete la fase (art. 25.6).
  const fase = o.faseEmpresa || 'pendiente'
  const faseOk = !ctx.tieneFaseEmpresa || fase === 'superada' || fase === 'exenta'
  let resultado
  if (media === null)       resultado = 'SIN_EVALUAR'
  else if (!completo)       resultado = 'PENDIENTE'
  else if (!centroOk)       resultado = 'NO_SUPERADO'
  else if (!faseOk)         resultado = fase === 'no_superada' ? 'NO_SUPERADO' : 'SUPERADO_PARCIAL'
  else                      resultado = 'SUPERADO'

  const superado = resultado === 'SUPERADO'
  // El «superado parcial» ya tiene su calificación: es la que conservará cuando
  // supere la fase de empresa, así que el tope de 4 del art. 25.5 no le aplica.
  const acta = actaEntera(media, superado || resultado === 'SUPERADO_PARCIAL')

  return {
    porRA, media, pendientes, sinNota, completo, superado, acta,
    resultado,
    centroOk,
    // A efectos de promoción, SP cuenta como superado (art. 18.4)
    superadoParaPromocion: resultado === 'SUPERADO' || resultado === 'SUPERADO_PARCIAL',
  }
}

/**
 * Calificación cualitativa de los ámbitos de grado básico.
 *
 * Orden 201/2024, art. 25.2: los ámbitos de Comunicación y Ciencias Sociales y
 * de Ciencias Aplicadas **no se califican con números**, sino con Insuficiente,
 * Suficiente, Bien, Notable o Sobresaliente. El art. 25.3 fija la equivalencia
 * al pasar de cualitativo a cuantitativo: IN 3 · SU 5 · BI 6 · NT 7,5 · SB 9,
 * y este reparto es su lectura inversa.
 */
function calificacionCualitativa(nota) {
  if (nota === null || nota === undefined) return null
  if (nota < 5)   return { sigla: 'IN', texto: 'Insuficiente', equivalente: 3 }
  if (nota < 6)   return { sigla: 'SU', texto: 'Suficiente',   equivalente: 5 }
  if (nota < 7.5) return { sigla: 'BI', texto: 'Bien',         equivalente: 6 }
  if (nota < 9)   return { sigla: 'NT', texto: 'Notable',      equivalente: 7.5 }
  return { sigla: 'SB', texto: 'Sobresaliente', equivalente: 9 }
}

/**
 * ¿Este módulo es un ámbito de grado básico? Se marca en la programación; si no,
 * se deduce del nombre, que en los decretos es siempre «Ámbito de …».
 */
// Nota: el catálogo de EvalFP no incluye los ámbitos de Grado Básico —Comunicación
// y Sociedad, Ciencias Aplicadas—, porque los imparte profesorado de otras
// especialidades y no de FP. Esta función y `calificacionCualitativa` se quedan
// implementadas para cumplir el art. 25.2 si alguna vez hacen falta: se activan
// poniendo `ambito: true` en el módulo.
function moduloEsAmbito(modulo) {
  if (!modulo) return false
  if (modulo.ambito === true || modulo.ambito === false) return modulo.ambito
  const nivel = String(modulo.ciclo_nivel || '').toUpperCase()
  if (nivel !== 'CFGB') return false
  const nombre = String(modulo.nombre || '').toLowerCase()
  return nombre.startsWith('ámbito') || nombre.startsWith('ambito') ||
         /ciencias aplicadas|comunicación y ciencias sociales|comunicacion y ciencias sociales/.test(nombre)
}

/**
 * ¿Este módulo tiene fase de formación en empresa?
 * Se deduce del catálogo: si la duración oficial es mayor que las horas de aula,
 * la diferencia son horas de empresa. El profesorado puede forzarlo en la
 * programación con `modulo.fase_empresa`.
 */
function moduloConFaseEmpresa(modulo) {
  if (!modulo) return false
  if (modulo.fase_empresa === true || modulo.fase_empresa === false) return modulo.fase_empresa
  const total = parseInt(modulo.total_horas, 10) || 0
  const aula  = parseInt(modulo.horas_aula, 10) || 0
  return aula > 0 && total > aula
}

/** Etiqueta corta de acta para cada estado (art. 12 y 25.4). */
function etiquetaResultado(resultado) {
  switch (resultado) {
    case 'SUPERADO':          return 'APTO/A'
    case 'SUPERADO_PARCIAL':  return 'APTO/A · SP'
    case 'NO_SUPERADO':       return 'NO APTO/A'
    case 'PENDIENTE':         return 'PENDIENTE'
    default:                  return '—'
  }
}

/* ==========================================================================
 * Calificaciones finales de ciclo · Orden 201/2024 en la redacción dada por la
 * Orden 55/2026, de 17 de abril (DOCM núm. 78, de 27/04/2026)
 *
 * Cuidado con la numeración: la Orden 55/2026 suprimió el apartado 8 del
 * artículo 25 y renumeró los siguientes. Aquí se cita SIEMPRE la numeración
 * vigente, indicando entre paréntesis la anterior cuando ayuda.
 * ========================================================================== */

/**
 * ¿Computa este módulo en la calificación final del ciclo?
 *
 * Art. 25.11 (antes 25.12): «Los módulos profesionales convalidados sin nota no
 * podrán ser computados a efectos del cálculo de la calificación final».
 *
 * La Orden 55/2026 eliminó de este apartado la mención «o exentos», en
 * coherencia con la supresión del apartado que creaba el estado «EXEN».
 *
 * @param {Object} m  { nota, convalidado }
 */
function computaEnNotaFinal(m) {
  if (!m) return false
  if (m.convalidado && (m.nota === null || m.nota === undefined || m.nota === '')) return false
  return m.nota !== null && m.nota !== undefined && m.nota !== ''
}

/**
 * Calificación final del ciclo formativo o curso de especialización.
 *
 * Art. 25.9 y 25.10 (antes 25.10 y 25.11): «será la media aritmética entre 1 y
 * 10 con dos decimales […] **con independencia de la carga lectiva de los
 * mismos**». Es media aritmética simple: NO se pondera por horas. Es el error
 * fácil de cometer, porque dentro de un módulo sí se pondera.
 *
 * Para el título de Técnico Básico el art. 25.9 acota el conjunto a «todos los
 * módulos del ámbito profesional y proyecto intermodular»: los ámbitos de
 * Comunicación y Ciencias Sociales y de Ciencias Aplicadas quedan fuera.
 *
 * @param {Array}  modulos  [{ nota, convalidado, esAmbito }]
 * @param {Object} [opts]
 * @param {boolean} [opts.soloAmbitoProfesional]  true para el título de Técnico Básico
 * @returns {?number} media con dos decimales, o null si no computa ninguno
 */
function notaFinalCiclo(modulos, opts) {
  const o = opts || {}
  let lista = (modulos || []).filter(computaEnNotaFinal)
  if (o.soloAmbitoProfesional) lista = lista.filter(m => !m.esAmbito)
  if (!lista.length) return null
  const suma = lista.reduce((s, m) => s + Number(m.nota), 0)
  return Math.round((suma / lista.length) * 100) / 100
}

/**
 * Nota que se presenta como requisito de acceso a grado medio tras un grado
 * básico (art. 25.9, párrafo tercero): aquí sí entran los ámbitos.
 *
 * Ojo: el título de Graduado en ESO obtenido por superar un ciclo de grado
 * básico «se expedirá sin calificación» (art. 25.9, párrafo segundo). Esta
 * media es sólo para el procedimiento de admisión, no va en el título.
 */
function notaAccesoGradoMedio(modulos) {
  return notaFinalCiclo(modulos, { soloAmbitoProfesional: false })
}

/**
 * Cupo de Matrícula de Honor de un centro.
 *
 * Art. 25.12 (antes 25.13): «Se podrá conceder una Matrícula de Honor por cada
 * veinte alumnos y alumnas o fracción, computando la totalidad del alumnado de
 * último curso en el centro, diferenciado por ciclo formativo o curso de
 * especialización y modalidad».
 *
 * La Orden 55/2026 cambió el criterio de reparto: antes era «por modalidades»,
 * ahora por ciclo o curso de especialización **y** modalidad.
 */
function cupoMatriculaHonor(totalAlumnadoUltimoCurso) {
  const n = Number(totalAlumnadoUltimoCurso) || 0
  return n <= 0 ? 0 : Math.ceil(n / 20)
}

/**
 * Quién puede optar a Matrícula de Honor: calificación final ≥ 9 (art. 25.12).
 *
 * Devuelve las candidaturas ordenadas por nota, junto al cupo disponible. La
 * concesión no es automática: «será otorgada por acuerdo del equipo docente»,
 * valorando además el esfuerzo y la evolución. Por eso esto propone, no decide.
 *
 * @param {Array} alumnado  [{ id, nombre, notaFinal }]
 * @param {number} totalUltimoCurso  alumnado de último curso del ciclo y modalidad
 */
function candidatosMatriculaHonor(alumnado, totalUltimoCurso) {
  const cupo = cupoMatriculaHonor(totalUltimoCurso)
  const candidatos = (alumnado || [])
    .filter(a => a.notaFinal !== null && a.notaFinal !== undefined && Number(a.notaFinal) >= 9)
    .sort((a, b) => Number(b.notaFinal) - Number(a.notaFinal))
  return { cupo, candidatos, excedeCupo: candidatos.length > cupo }
}

/**
 * Art. 18.5 (añadido por la Orden 55/2026): en el último curso de un grado D,
 * el equipo docente puede decidir que el alumnado no vuelva a cursar hasta tres
 * materias no superadas si su carga horaria conjunta es inferior al 30 % de la
 * duración total del curso. Se evalúan al año siguiente como pendientes.
 *
 * Devuelve si se cumplen las condiciones objetivas. La decisión sigue siendo
 * del equipo docente, que además debe emitir el informe del anexo VIII.
 *
 * @param {Array}  pendientes    [{ nombre, horas }] materias no superadas
 * @param {number} horasCurso    duración total del curso
 */
function puedeContinuarConPendientes(pendientes, horasCurso) {
  const lista = pendientes || []
  const total = Number(horasCurso) || 0
  const horas = lista.reduce((s, m) => s + (Number(m.horas) || 0), 0)
  const porcentaje = total > 0 ? (horas / total) * 100 : null
  const cumple = lista.length > 0 && lista.length <= 3 && total > 0 && porcentaje < 30
  return {
    cumple,
    materias: lista.length,
    horas,
    porcentaje: porcentaje === null ? null : Math.round(porcentaje * 100) / 100,
    // Motivo de por qué no cumple, para poder explicarlo en pantalla
    motivo: !lista.length ? 'sin materias pendientes'
      : lista.length > 3 ? `${lista.length} materias pendientes, el máximo son 3`
      : total <= 0 ? 'falta la duración del curso'
      : porcentaje >= 30 ? `la carga pendiente es el ${Math.round(porcentaje * 100) / 100} %, y el tope es el 30 %`
      : null,
  }
}

/**
 * Franja legal de la fase de formación en empresa de un curso de especialización.
 *
 * Decreto 79/2025, de 14 de octubre, artículo 5.3 (el del CE de Desarrollo de
 * aplicaciones en lenguaje Python, DOCM núm. 205 de 23/10/2025):
 *
 *   · Régimen general: duración «entre el 20 y 35 %» de la duración total del
 *     currículo, y «entre el 10 y el 20 % de los resultados de aprendizaje».
 *   · Régimen intensivo: «entre el 35 y 50 %» de la duración y «al menos, el
 *     30 % de los resultados de aprendizaje».
 *
 * Los porcentajes de RA se aplican «a la totalidad de los mismos y no por módulo
 * profesional»: son del curso entero, no de cada módulo por separado.
 *
 * Es una oferta potestativa, «a propuesta del centro educativo». Esta función no
 * decide nada: devuelve los límites entre los que la decisión del centro es legal.
 */
function franjaFaseEmpresaCE(horasTotales, regimen) {
  const t = Number(horasTotales) || 0
  const intensivo = regimen === 'intensivo'
  const pHoras = intensivo ? [0.35, 0.50] : [0.20, 0.35]
  const pRa    = intensivo ? [0.30, 1] : [0.10, 0.20]
  return {
    regimen: intensivo ? 'intensivo' : 'general',
    horasMin: Math.ceil(t * pHoras[0]),
    horasMax: Math.floor(t * pHoras[1]),
    porcentajeHoras: pHoras.map(p => p * 100),
    porcentajeRa: pRa.map(p => p * 100),
  }
}

/**
 * ¿Encaja en la norma la fase de empresa que propone el centro?
 *
 * @param {Object} p
 * @param {number} p.horasEmpresa   horas que se van a la empresa
 * @param {number} p.horasTotales   duración total del curso de especialización
 * @param {number} p.raEnEmpresa    RA que se trabajan en la empresa
 * @param {number} p.raTotales      RA del curso completo
 * @param {string} [p.regimen]      'general' (por defecto) o 'intensivo'
 */
function validaFaseEmpresaCE({ horasEmpresa, horasTotales, raEnEmpresa, raTotales, regimen }) {
  const f = franjaFaseEmpresaCE(horasTotales, regimen)
  const h = Number(horasEmpresa) || 0
  const pctRa = Number(raTotales) > 0 ? (Number(raEnEmpresa) / Number(raTotales)) * 100 : null
  const horasOk = h >= f.horasMin && h <= f.horasMax
  const raOk = pctRa !== null && pctRa >= f.porcentajeRa[0] && pctRa <= f.porcentajeRa[1]
  const avisos = []
  if (!horasOk) {
    avisos.push(`las horas de empresa (${h}) tienen que estar entre ${f.horasMin} y ` +
                `${f.horasMax} en régimen ${f.regimen}`)
  }
  if (!raOk) {
    avisos.push(`los RA en empresa (${pctRa === null ? '?' : Math.round(pctRa * 10) / 10} %) ` +
                `tienen que estar entre el ${f.porcentajeRa[0]} y el ${f.porcentajeRa[1]} %`)
  }
  return { valida: horasOk && raOk, franja: f, porcentajeRa: pctRa, avisos }
}

// Exportado también para los tests (en el navegador `module` no existe)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    notaEnEscala10, mediaActividades, pesosPorTipo, notaCE, notaRA,
    raMinExamKO, actaEntera, contextoModulo, estadoModulo, etiquetaResultado,
    moduloConFaseEmpresa, calificacionCualitativa, moduloEsAmbito,
    convocatoriaDe, actividadesDeConvocatoria, notaExamenDecisiva, esPruebaObjetiva,
    computaEnNotaFinal, notaFinalCiclo, notaAccesoGradoMedio,
    cupoMatriculaHonor, candidatosMatriculaHonor, puedeContinuarConPendientes,
    franjaFaseEmpresaCE, validaFaseEmpresaCE,
  }
}

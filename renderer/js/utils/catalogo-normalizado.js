// SPDX-License-Identifier: GPL-3.0-or-later
// ═══════════════════════════════════════════════════════════════
// RF-02, cierre · Catálogo normalizado — punto único de lectura
// ═══════════════════════════════════════════════════════════════
// Adapta ra_catalogo/ce_catalogo/unidades_trabajo/ut_ce/ce_instrumentos_previstos
// a las formas {ras, ces, uts, asigs, raInstr} que ya entendían los helpers de
// ce-keys.js (rasDeActividad, actCubreCe, cesDisponiblesActividad,
// rasPorEvaluacion…), para no reescribirlos.
//
// Toda pantalla que necesite RA/CE/UT/asignaciones de un módulo pasa por aquí
// — Programación, Dashboard y Evaluaciones, de momento (docs/rediseno/
// 05-PLAN-MIGRACION.md) — en vez de leer modulos.data_json cada una a su
// manera. `raCatalogo.length === 0` es la señal de "módulo sin migrar": cada
// pantalla decide cómo avisarlo, esta función solo informa.

/**
 * @param {number|string} mid
 * @returns {Promise<{
 *   raCatalogo: object[], ceCatalogoRows: object[], unidadesTrabajoRows: object[],
 *   utCeModuloRows: object[], ceInstrRows: object[], actividadCeModuloRows: object[],
 *   ras: object[], ces: object, uts: object[], asigs: object[], raInstr: object,
 * }>}
 */
async function _cargarCatalogoNormalizado(mid) {
  mid = parseInt(mid)
  const [raCatalogo, ceCatalogoRows, unidadesTrabajoRows, utCeModuloRows, ceInstrRows, actividadCeModuloRows] =
    await Promise.all([
      window.api.getRaCatalogo(mid),
      window.api.getCeCatalogo(mid),
      window.api.getUnidadesTrabajo(mid),
      window.api.getUtCeModulo(mid),
      window.api.getCeInstrumentosPrevistos(mid),
      window.api.getActividadCeModulo(mid),
    ])
  const ras = raCatalogo.map(r => ({ id: r.ra_id, nombre: r.nombre, pond: r.pond, dual: r.dual_pct, llave: r.llave }))
  const ces = {}
  for (const c of ceCatalogoRows) (ces[c.ra_id] = ces[c.ra_id] || []).push({ id: c.ce_id, texto: c.texto, peso: c.peso })
  const uts = unidadesTrabajoRows.map(u => ({
    id: u.ut_id, nombre: u.nombre, horas: u.horas, horas_empresa: u.horas_empresa, eval: u.eval, tags: u.tags,
  }))
  const asigMap = {}
  for (const f of utCeModuloRows) {
    const k = `${f.ut_id}|${f.ra_id}`
    ;(asigMap[k] = asigMap[k] || { ut: f.ut_id, ra: f.ra_id, ces: [] }).ces.push(f.ce_id)
  }
  const asigs = Object.values(asigMap)
  const raInstr = {}
  for (const row of ceInstrRows) (raInstr[row.ra_id] = raInstr[row.ra_id] || new Set()).add(row.instrumento)
  for (const k of Object.keys(raInstr)) raInstr[k] = [...raInstr[k]]
  return {
    raCatalogo, ceCatalogoRows, unidadesTrabajoRows, utCeModuloRows, ceInstrRows, actividadCeModuloRows,
    ras, ces, uts, asigs, raInstr,
  }
}

// Exportado también para los tests (en el navegador `module` no existe). Usa
// window.api, así que en Node solo sirve para que ESLint vea el uso — los
// tests que necesiten datos normalizados llaman a db.js directamente.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { _cargarCatalogoNormalizado }
}

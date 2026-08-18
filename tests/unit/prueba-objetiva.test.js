/**
 * RF-02, cierre · Prueba objetiva de evaluación completa (art. 3.6).
 *
 * addPruebaObjetiva() (programacion.js) dejó de leer data_json.ces y pasó a leer
 * ce_catalogo (docs/rediseno/05-PLAN-MIGRACION.md). La ley exige que esa prueba
 * cubra «la totalidad de los resultados de aprendizaje a través de sus criterios
 * de evaluación» — así que el cambio de fuente no puede perder ni un criterio.
 *
 * addPruebaObjetiva() vive en el renderer (usa document/window.api) y no es
 * testable en Node directamente. La parte que de verdad importa aquí — barrer
 * TODO el catálogo sin dejarse ninguno — se extrajo a todosLosCe() (ce-keys.js),
 * una función pura sin DOM que addPruebaObjetiva() llama tal cual. Este test
 * prueba esa función contra un catálogo migrado de verdad, con el mismo tamaño
 * que el módulo real inspeccionado en el plan de migración: 8 RA, 79 CE en total.
 */
import { describe, it, expect, afterEach } from 'vitest'
import os   from 'os'
import path from 'path'
import fs   from 'fs'

const sqliteDisponible = await import('node:sqlite').then(() => true, () => false)
if (!sqliteDisponible) {
  console.warn(
    `\n⚠️  tests/unit/prueba-objetiva.test.js omitido: este Node (${process.version}) ` +
    'no expone node:sqlite. Para ejecutarlos, usa Node >= 22.5.\n'
  )
}
const db = sqliteDisponible ? await import('../../db.js') : null
const { todosLosCe } = await import('../../renderer/js/utils/ce-keys.js')

afterEach(() => {
  try {
    db.closeDb()
    const dbDir  = path.join(os.tmpdir(), `evalfp-test-${process.pid}`)
    const dbFile = path.join(dbDir, 'evalfp.db')
    if (fs.existsSync(dbFile)) fs.unlinkSync(dbFile)
  } catch {
    // Limpieza best-effort.
  }
})

// 8 RA con conteos de CE que suman 79, como el módulo real inspeccionado en
// docs/rediseno/05-PLAN-MIGRACION.md §0 (8 RA, 79 CE en total).
const CE_POR_RA = [10, 10, 10, 10, 10, 10, 10, 9]
const TOTAL_CE  = CE_POR_RA.reduce((s, n) => s + n, 0)   // 79

function datosFixture() {
  const ras = CE_POR_RA.map((_, i) => ({ id: `RA${i + 1}`, nombre: `Resultado ${i + 1}`, pond: 100 / 8 }))
  const ces = {}
  CE_POR_RA.forEach((n, i) => {
    ces[`RA${i + 1}`] = Array.from({ length: n }, (_, j) => ({ id: `CR${j + 1}`, texto: `Criterio ${j + 1} de RA${i + 1}` }))
  })
  return {
    modulo: { eval_count: 3 }, ras, ces,
    uts: [], asignaciones: [], eval_ras: {}, ra_instrumentos: {}, actividades: [],
  }
}

function crearModuloMigrado() {
  const mid = db.addModulo({
    key: 'MOD_PRUEBA_OBJ', abrev: 'PO', nombre: 'Módulo prueba objetiva', ciclo: 'CFGS Test',
    curso: '1', anno: '2026-2027', grupo: 'Grupo A', horas: 200, decreto: null, actividades: [],
    data: datosFixture(),
  })
  db.migrarProgramacionNormalizada()
  return mid
}

/** Agrupa ce_catalogo por RA, igual que _cargarCatalogoNormalizado() en programacion.js. */
function agruparPorRa(ceCatalogoRows) {
  const ces = {}
  for (const c of ceCatalogoRows) (ces[c.ra_id] = ces[c.ra_id] || []).push({ id: c.ce_id, texto: c.texto, peso: c.peso })
  return ces
}

describe.skipIf(!sqliteDisponible)('RF-02 · addPruebaObjetiva() sigue cubriendo todos los criterios', () => {
  it('ce_catalogo conserva los 79 criterios del módulo tras la migración', () => {
    const mid = crearModuloMigrado()
    expect(db.getCeCatalogo(mid)).toHaveLength(TOTAL_CE)
  })

  it('todosLosCe() sobre el catálogo migrado da exactamente los 79 "RA|CE", sin duplicados ni huecos', () => {
    const mid = crearModuloMigrado()
    const ceCatalogo = db.getCeCatalogo(mid)
    const ces = agruparPorRa(ceCatalogo)

    const claves = todosLosCe(ces)

    expect(claves).toHaveLength(TOTAL_CE)
    expect(new Set(claves).size).toBe(TOTAL_CE)   // sin duplicados

    const esperadas = new Set(ceCatalogo.map(c => `${c.ra_id}|${c.ce_id}`))
    expect(new Set(claves)).toEqual(esperadas)     // ni uno de más, ni uno de menos

    // Los 8 RA están representados: no basta con el número total, un fallo que
    // se salte un RA entero pero rellene con duplicados de otro no se vería
    // solo con la longitud.
    const rasEnClaves = new Set(claves.map(k => k.split('|')[0]))
    expect(rasEnClaves).toEqual(new Set(CE_POR_RA.map((_, i) => `RA${i + 1}`)))
  })

  it('la actividad creada con esas claves persiste los 79 criterios en actividad_ce (addPruebaObjetiva de extremo a extremo)', () => {
    const mid = crearModuloMigrado()
    const ces = agruparPorRa(db.getCeCatalogo(mid))
    const claves = todosLosCe(ces)

    // Mismos pasos que addPruebaObjetiva(): crear la actividad con `ces` (JSON,
    // compatibilidad con pantallas no migradas) y sincronizar actividad_ce.
    const actId = db.saveActividad({
      modulo_id: mid, ut_id: null, ra_id: null,
      descripcion: 'Prueba objetiva de evaluación completa (art. 3.6)',
      instrumento: 'Examen', tipo: 'examen', peso: 0, nota_max: 10, eval: 3, orden: 1,
      ces: claves, convocatoria: 1, prueba_objetiva: 1,
    })
    const pares = claves.map(k => { const [ra_id, ce_id] = k.split('|'); return { ra_id, ce_id } })
    db.setActividadCe(actId, mid, pares)

    expect(db.getActividadCe(actId)).toHaveLength(TOTAL_CE)
    const actividad = db.getActividades(mid).find(a => a.id === actId)
    expect(JSON.parse(actividad.ces)).toHaveLength(TOTAL_CE)   // doble escritura, ver 00-CONTEXTO.md
  })

  it('un módulo con un RA sin ningún CE cargado no revienta y no lo cuenta', () => {
    const mid = db.addModulo({
      key: 'MOD_PRUEBA_OBJ_VACIO', abrev: 'POV', nombre: 'Módulo con RA vacío', ciclo: 'CFGS Test',
      curso: '1', anno: '2026-2027', grupo: 'Grupo A', horas: 50, decreto: null, actividades: [],
      data: {
        modulo: { eval_count: 3 },
        ras: [{ id: 'RA1', nombre: 'Con criterios', pond: 100 }],
        ces: { RA1: [{ id: 'CR1', texto: 'Único criterio' }] },
        uts: [], asignaciones: [], eval_ras: {}, ra_instrumentos: {}, actividades: [],
      },
    })
    db.migrarProgramacionNormalizada()
    const ces = agruparPorRa(db.getCeCatalogo(mid))
    expect(todosLosCe(ces)).toEqual(['RA1|CR1'])
  })
})

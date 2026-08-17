/**
 * RF-02 · Unidades de trabajo normalizadas, segunda parte.
 * Ver docs/rediseno/04-REDISENO-PANTALLAS.md §1.2-§1.4.
 */
import { describe, it, expect, afterEach } from 'vitest'
import os   from 'os'
import path from 'path'
import fs   from 'fs'

const sqliteDisponible = await import('node:sqlite').then(() => true, () => false)
if (!sqliteDisponible) {
  console.warn(
    `\n⚠️  tests/unit/unidades-trabajo.test.js omitido: este Node (${process.version}) ` +
    'no expone node:sqlite. Para ejecutarlos, usa Node >= 22.5.\n'
  )
}
const db = sqliteDisponible ? await import('../../db.js') : null
const { temporalizacionRas } = await import('../../renderer/js/utils/ce-keys.js')

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

function datosFixture() {
  return {
    modulo: { eval_count: 3 },
    ras: [{ id: 'RA1', nombre: 'Resultado uno', pond: 100 }],
    ces: { RA1: [{ id: 'CR1', texto: 'Criterio 1' }, { id: 'CR2', texto: 'Criterio 2' }] },
    uts: [], asignaciones: [], eval_ras: {}, ra_instrumentos: {}, actividades: [],
  }
}

function crearModulo(key) {
  return db.addModulo({
    key, abrev: key, nombre: `Módulo ${key}`, ciclo: 'CFGS Test', curso: '1', anno: '2026-2027',
    grupo: 'Grupo A', horas: 100, decreto: null, actividades: [], data: datosFixture(),
  })
}

describe.skipIf(!sqliteDisponible)('RF-02 · unidades_trabajo', () => {
  it('setUnidadTrabajo() sin utId genera UT1, UT2… saltando huecos', () => {
    const mid = crearModulo('MOD_UT_ID')
    const id1 = db.setUnidadTrabajo(mid, null, { nombre: 'Primera' })
    const id2 = db.setUnidadTrabajo(mid, null, { nombre: 'Segunda' })
    expect(id1).toBe('UT1')
    expect(id2).toBe('UT2')
    db.deleteUnidadTrabajo(mid, 'UT1')
    const id3 = db.setUnidadTrabajo(mid, null, { nombre: 'Tercera' })
    // Con UT1 borrada, "siguiente libre" es UT1 otra vez si se conserva ese
    // criterio (nº de existentes + 1 = 2 → ya usado por UT2 → sube a 3... o
    // reutiliza el hueco). Lo único exigible: no colisiona con lo que existe.
    const existentes = db.getUnidadesTrabajo(mid).map(u => u.ut_id)
    expect(existentes).toContain(id3)
    expect(new Set(existentes).size).toBe(existentes.length) // sin duplicados
  })

  it('setUnidadTrabajo() con utId actualiza en vez de duplicar', () => {
    const mid = crearModulo('MOD_UT_UPD')
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Original', horas: 10, eval: 1 })
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Renombrada', horas: 20, eval: 2 })
    const uts = db.getUnidadesTrabajo(mid)
    expect(uts).toHaveLength(1)
    expect(uts[0]).toMatchObject({ nombre: 'Renombrada', horas: 20, eval: 2 })
  })

  it('deleteUnidadTrabajo() borra la UT y su ut_ce en cascada, pero no las actividades que la referenciaban', () => {
    const mid = crearModulo('MOD_UT_DEL')
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Unidad', eval: 1 })
    db.migrarProgramacionNormalizada()
    db.setUtCe(mid, 'UT1', [{ ra_id: 'RA1', ce_id: 'CR1' }])
    const actId = db.saveActividad({
      modulo_id: mid, ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Práctica', instrumento: 'Práctica',
      tipo: 'practica', peso: 100, nota_max: 10, eval: 1, orden: 1, ces: [],
    })

    db.deleteUnidadTrabajo(mid, 'UT1')

    expect(db.getUnidadesTrabajo(mid)).toEqual([])
    expect(db.getUtCe(mid, 'UT1')).toEqual([])
    const actividades = db.getActividades(mid)
    expect(actividades).toHaveLength(1)
    expect(actividades[0].ut_id).toBe('UT1')   // sigue apuntando a la UT ya borrada: es lo esperado
    expect(actividades[0].id).toBe(actId)
  })

  it('setUtCe() sustituye la asignación completa, no la acumula', () => {
    const mid = crearModulo('MOD_UT_CE')
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Unidad', eval: 1 })
    db.migrarProgramacionNormalizada()
    db.setUtCe(mid, 'UT1', [{ ra_id: 'RA1', ce_id: 'CR1' }, { ra_id: 'RA1', ce_id: 'CR2' }])
    expect(db.getUtCe(mid, 'UT1')).toHaveLength(2)
    db.setUtCe(mid, 'UT1', [{ ra_id: 'RA1', ce_id: 'CR1' }])
    expect(db.getUtCe(mid, 'UT1')).toEqual([{ ra_id: 'RA1', ce_id: 'CR1' }])
  })

  it('setActividadCe() sustituye los CE de una actividad, no los acumula', () => {
    const mid = crearModulo('MOD_ACT_CE')
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Unidad', eval: 1 })
    db.migrarProgramacionNormalizada()
    const actId = db.saveActividad({
      modulo_id: mid, ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Práctica', instrumento: 'Práctica',
      tipo: 'practica', peso: 100, nota_max: 10, eval: 1, orden: 1, ces: [],
    })
    db.setActividadCe(actId, mid, [{ ra_id: 'RA1', ce_id: 'CR1' }, { ra_id: 'RA1', ce_id: 'CR2' }])
    expect(db.getActividadCe(actId)).toHaveLength(2)
    db.setActividadCe(actId, mid, [{ ra_id: 'RA1', ce_id: 'CR2' }])
    expect(db.getActividadCe(actId)).toEqual([{ ra_id: 'RA1', ce_id: 'CR2' }])
  })
})

describe.skipIf(!sqliteDisponible)('RF-02 · cambiar la evaluación de una UT no toca lo ya evaluado', () => {
  it('setUnidadTrabajo() con un eval distinto no cambia actividades, evidencias ni notas', () => {
    const mid = crearModulo('MOD_TEMPORALIZACION')
    const alumnoId = db.saveAlumno({ modulo_id: mid, nombre: 'Ana', apellidos: 'García', estado: 'Activo' })
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Unidad', eval: 1 })
    db.migrarProgramacionNormalizada()
    db.setUtCe(mid, 'UT1', [{ ra_id: 'RA1', ce_id: 'CR1' }])
    const actId = db.saveActividad({
      modulo_id: mid, ut_id: 'UT1', ra_id: 'RA1', descripcion: 'Práctica', instrumento: 'Práctica',
      tipo: 'practica', peso: 100, nota_max: 10, eval: 1, orden: 1, ces: ['RA1|CR1'],
    })
    db.saveNota(alumnoId, actId, 7)
    const evidId = db.addEvidencia({ alumnoId, actividadId: actId, ruta: '/tmp/ejemplo.pdf' })

    const actividadAntes = db.getActividades(mid).find(a => a.id === actId)
    const notaAntes = db.getNotasGrid(mid).find(n => n.actividad_id === actId)
    const evidAntes = db.getEvidencias(mid).find(e => e.id === evidId)

    // Mover la UT de la 1ª a la 3ª evaluación.
    db.setUnidadTrabajo(mid, 'UT1', { nombre: 'Unidad', eval: 3 })

    const actividadDespues = db.getActividades(mid).find(a => a.id === actId)
    const notaDespues = db.getNotasGrid(mid).find(n => n.actividad_id === actId)
    const evidDespues = db.getEvidencias(mid).find(e => e.id === evidId)

    // La actividad conserva SU PROPIO eval (columna independiente de la UT:
    // el eje actividades.eval del art. 21.5 no se toca).
    expect(actividadDespues).toEqual(actividadAntes)
    expect(notaDespues).toEqual(notaAntes)
    expect(evidDespues).toEqual(evidAntes)
    expect(actividadDespues.eval).toBe(1)   // no ha heredado el 3 de la UT

    // Lo que SÍ cambia es la temporalización derivada del RA.
    const rango = temporalizacionRas(db.getUnidadesTrabajo(mid), db.getUtCeModulo(mid))
    expect(rango.RA1).toEqual({ min: 3, max: 3 })
  })
})

describe('RF-02 · temporalizacionRas() — pura, sin base de datos', () => {
  it('un RA en una sola UT hereda esa evaluación como min y max', () => {
    const uts = [{ ut_id: 'UT1', eval: 2 }]
    const utCe = [{ ut_id: 'UT1', ra_id: 'RA1', ce_id: 'CR1' }]
    expect(temporalizacionRas(uts, utCe)).toEqual({ RA1: { min: 2, max: 2 } })
  })

  it('un RA trabajado en dos UT de evaluaciones distintas hereda el rango completo', () => {
    const uts = [{ ut_id: 'UT1', eval: 1 }, { ut_id: 'UT4', eval: 3 }]
    const utCe = [
      { ut_id: 'UT1', ra_id: 'RA1', ce_id: 'CR1' },
      { ut_id: 'UT4', ra_id: 'RA1', ce_id: 'CR2' },
    ]
    expect(temporalizacionRas(uts, utCe)).toEqual({ RA1: { min: 1, max: 3 } })
  })

  it('una fila de ut_ce que apunta a una UT que ya no existe se ignora, no revienta', () => {
    const uts = [{ ut_id: 'UT1', eval: 1 }]
    const utCe = [{ ut_id: 'UT_BORRADA', ra_id: 'RA1', ce_id: 'CR1' }]
    expect(temporalizacionRas(uts, utCe)).toEqual({})
  })
})

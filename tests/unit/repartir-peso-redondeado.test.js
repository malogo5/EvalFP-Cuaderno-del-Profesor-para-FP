/**
 * repartirPesoRedondeado() (ce-keys.js) — usado por applyModuloPesos().
 *
 * Bug real (2026-08-19, módulo ISO): redondear el peso de cada actividad por
 * separado (Math.round(total/n*10)/10) no garantiza que la suma vuelva a dar
 * el total. Con 30 % entre 7 prácticas salía 30,1 %; con 40 % entre 6 salía
 * 40,2 %. El profesorado lo veía como "⚠ suma 100,x %" en evaluaciones que sí
 * estaban bien programadas.
 */
import { describe, it, expect } from 'vitest'

const { repartirPesoRedondeado } = await import('../../renderer/js/utils/ce-keys.js')

describe('repartirPesoRedondeado() — la suma de lo repartido es siempre exacta', () => {
  it('caso real: 30 % entre 7 prácticas ya no da 30,1 %', () => {
    const partes = repartirPesoRedondeado(30, 7)
    expect(partes).toHaveLength(7)
    expect(partes.reduce((s, p) => s + p, 0)).toBeCloseTo(30, 5)
    // 6 actividades a 4,3 % y 1 a 4,2 % (el resto mayor decide cuáles suben)
    expect(partes.filter(p => p === 4.3)).toHaveLength(6)
    expect(partes.filter(p => p === 4.2)).toHaveLength(1)
  })

  it('caso real: 40 % entre 6 actividades ya no da 40,2 %', () => {
    const partes = repartirPesoRedondeado(40, 6)
    expect(partes.reduce((s, p) => s + p, 0)).toBeCloseTo(40, 5)
    expect(partes.filter(p => p === 6.7)).toHaveLength(4)
    expect(partes.filter(p => p === 6.6)).toHaveLength(2)
  })

  it('60 % entre 1 examen: sin redondeo, exacto', () => {
    expect(repartirPesoRedondeado(60, 1)).toEqual([60])
  })

  it('reparto exacto (100 % entre 4) no inventa decimales de más', () => {
    expect(repartirPesoRedondeado(100, 4)).toEqual([25, 25, 25, 25])
  })

  it('0 elementos devuelve un reparto vacío, no revienta', () => {
    expect(repartirPesoRedondeado(30, 0)).toEqual([])
  })

  it('repartir dos veces el mismo total y n da siempre el mismo resultado (determinista)', () => {
    const a = repartirPesoRedondeado(30, 7)
    const b = repartirPesoRedondeado(30, 7)
    expect(b).toEqual(a)
  })

  it('propiedad general: para cualquier total/n razonable, la suma redondeada a 1 decimal coincide con el total redondeado a 1 decimal', () => {
    for (const total of [100, 70, 60, 30, 45.5, 33.3]) {
      for (let n = 1; n <= 12; n++) {
        const partes = repartirPesoRedondeado(total, n)
        const suma = Math.round(partes.reduce((s, p) => s + p, 0) * 10) / 10
        expect(suma, `total=${total} n=${n}`).toBe(Math.round(total * 10) / 10)
      }
    }
  })
})

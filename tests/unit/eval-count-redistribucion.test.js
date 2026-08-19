/**
 * setEvalCount() (programacion.js) — cambiar el nº de evaluaciones del módulo.
 *
 * Bug real (2026-08-18, confirmado en producción): las actividades se
 * redistribuían por posición en una lista plana ordenada por (eval, orden),
 * sin mirar a qué UT pertenecían. Una actividad de una UT de la evaluación 2
 * podía acabar en la 1 solo porque le tocaba ese turno en la lista — mientras
 * su propia UT (redistribuida por SU cuenta, con el mismo problema pero sobre
 * otra lista) se quedaba en la 2. Resultado: la cabecera de una evaluación
 * decía un RA y debajo aparecían actividades de UT de otras evaluaciones, y
 * la suma de pesos por evaluación dejaba de cuadrar (una evaluación se
 * quedaba con las prácticas de un grupo y ningún examen, u otro caso mixto).
 *
 * El arreglo: `_repartoNuevoEvalUt()` sigue repartiendo las UT por bloques
 * (eso no cambia — es el eje real, art. 4.3.f), pero `_nuevoEvalDeActividad()`
 * ya no reparte la actividad por su cuenta: la deriva de su(s) propia(s) UT.
 * Estas dos funciones son las mismas que usa `setEvalCount()`, así que
 * probarlas aquí prueba el comportamiento real, no una reimplementación.
 */
import { describe, it, expect } from 'vitest'

const { _repartoNuevoEvalUt, _nuevoEvalDeActividad } =
  await import('../../renderer/js/utils/ce-keys.js')

describe('_nuevoEvalDeActividad() — una actividad sigue a su UT, no a su posición en una lista', () => {
  it('una actividad de una sola UT hereda el nuevo eval de esa UT', () => {
    const mapa = { UT1: 1, UT2: 2, UT3: 3 }
    expect(_nuevoEvalDeActividad({ ut_id: 'UT2' }, mapa)).toBe(2)
  })

  it('un examen multi-UT va a la evaluación de la UT más temprana', () => {
    const mapa = { UT1: 1, UT2: 2, UT3: 3 }
    expect(_nuevoEvalDeActividad({ ut_id: 'UT2,UT3' }, mapa)).toBe(2)
    expect(_nuevoEvalDeActividad({ ut_id: 'UT3,UT1,UT2' }, mapa)).toBe(1)
  })

  it('una actividad sin UT (recuperación, prueba objetiva del art. 3.6) no se toca: devuelve null', () => {
    const mapa = { UT1: 1 }
    expect(_nuevoEvalDeActividad({ ut_id: null }, mapa)).toBeNull()
    expect(_nuevoEvalDeActividad({ ut_id: '' }, mapa)).toBeNull()
  })

  it('una actividad cuya UT ya no existe en el reparto (borrada) tampoco se toca', () => {
    const mapa = { UT1: 1 }
    expect(_nuevoEvalDeActividad({ ut_id: 'UT_BORRADA' }, mapa)).toBeNull()
  })
})

describe('Caso real: 8 UT repartidas 3/1/4 (módulo ISO), cambiar 3→2 no descoloca ninguna actividad de su UT', () => {
  // Mismas 8 UT y 19 actividades del módulo real que disparó el fallo.
  const uts = [
    { ut_id: 'UT1', eval: 1 }, { ut_id: 'UT2', eval: 1 }, { ut_id: 'UT3', eval: 1 },
    { ut_id: 'UT4', eval: 2 },
    { ut_id: 'UT5', eval: 3 }, { ut_id: 'UT6', eval: 3 }, { ut_id: 'UT7', eval: 3 }, { ut_id: 'UT8', eval: 3 },
  ]
  const actividades = [
    { id: 1,  ut_id: 'UT1', peso: 5,  eval: 1 },
    { id: 2,  ut_id: 'UT1', peso: 5,  eval: 1 },
    { id: 3,  ut_id: 'UT2', peso: 5,  eval: 1 },
    { id: 4,  ut_id: 'UT2', peso: 5,  eval: 1 },
    { id: 5,  ut_id: 'UT3', peso: 5,  eval: 1 },
    { id: 6,  ut_id: 'UT3', peso: 5,  eval: 1 },
    { id: 13, ut_id: 'UT1,UT2,UT3', peso: 60, eval: 1 },   // Examen Evaluación 1
    { id: 16, ut_id: 'UT1', peso: 5, eval: 1 },
    { id: 17, ut_id: 'UT2', peso: 5, eval: 1 },
    { id: 7,  ut_id: 'UT4', peso: 20, eval: 2 },
    { id: 14, ut_id: 'UT4', peso: 60, eval: 2 },           // Examen Evaluación 2
    { id: 18, ut_id: 'UT4', peso: 20, eval: 2 },
    { id: 8,  ut_id: 'UT5', peso: 6.7, eval: 3 },
    { id: 9,  ut_id: 'UT6', peso: 6.7, eval: 3 },
    { id: 10, ut_id: 'UT7', peso: 6.7, eval: 3 },
    { id: 11, ut_id: 'UT7', peso: 6.7, eval: 3 },
    { id: 12, ut_id: 'UT8', peso: 6.7, eval: 3 },
    { id: 15, ut_id: 'UT5,UT6,UT7,UT8', peso: 60, eval: 3 }, // Examen Evaluación 3
    { id: 19, ut_id: 'UT5', peso: 6.7, eval: 3 },
    // Una prueba objetiva del art. 3.6, sin UT: no debe tocarse.
    { id: 20, ut_id: null, peso: 0, eval: 1 },
  ]

  function aplicarRedistribucion(newCount) {
    const mapaUt = _repartoNuevoEvalUt(uts, newCount)
    uts.forEach(u => { u.eval = mapaUt[u.ut_id] })
    actividades.forEach(a => {
      const nuevo = _nuevoEvalDeActividad(a, mapaUt)
      if (nuevo != null) a.eval = nuevo
    })
    return mapaUt
  }

  function comprobarConsistencia(mapaUt) {
    for (const act of actividades) {
      const utIds = String(act.ut_id || '').split(',').map(s => s.trim()).filter(Boolean)
      if (!utIds.length) continue   // sin UT: no se comprueba, no se toca
      const esperado = Math.min(...utIds.map(id => mapaUt[id]))
      expect(act.eval, `actividad ${act.id} (UT ${act.ut_id})`).toBe(esperado)
    }
  }

  it('bajar de 3 a 2 evaluaciones: cada actividad queda en el eval de su UT', () => {
    const mapaUt = aplicarRedistribucion(2)
    comprobarConsistencia(mapaUt)
    // La prueba objetiva del art. 3.6 (sin UT) no se ha movido.
    expect(actividades.find(a => a.id === 20).eval).toBe(1)
  })

  it('subir de 2 a 3 evaluaciones: cada actividad sigue en el eval de su UT (aunque no sea el original)', () => {
    // Encadenado: parte del estado ya redistribuido a 2 del test anterior.
    const mapaUt = aplicarRedistribucion(3)
    comprobarConsistencia(mapaUt)
    expect(actividades.find(a => a.id === 20).eval).toBe(1)
  })

  it('ningún peso se pierde ni se altera al redistribuir: la suma total del módulo no cambia', () => {
    const totalAntes = actividades.reduce((s, a) => s + a.peso, 0)
    aplicarRedistribucion(2)
    aplicarRedistribucion(3)
    const totalDespues = actividades.reduce((s, a) => s + a.peso, 0)
    expect(totalDespues).toBe(totalAntes)
  })
})

describe('Caso con reparto par: 6 UT a 2 por evaluación, el ida-y-vuelta 3→2→3 es exacto', () => {
  // Con un número de UT que divide justo entre 2 y 3, el reparto proporcional
  // no pierde información: ida y vuelta recompone el mismo agrupamiento, y
  // por tanto los pesos —que no se tocan— vuelven a sumar 100 % en cada
  // evaluación. Con reparto impar (caso real de arriba, 3/1/4) esto NO está
  // garantizado — fusionar y volver a partir en bloques distintos pierde el
  // agrupamiento original, igual que ya le pasaba solo a las UT antes de este
  // arreglo. Lo que este arreglo garantiza SIEMPRE es la consistencia
  // actividad↔UT del bloque de arriba, no la reversibilidad exacta del reparto.
  const utsOriginales = [
    { ut_id: 'UT1', eval: 1 }, { ut_id: 'UT2', eval: 1 },
    { ut_id: 'UT3', eval: 2 }, { ut_id: 'UT4', eval: 2 },
    { ut_id: 'UT5', eval: 3 }, { ut_id: 'UT6', eval: 3 },
  ]
  const actividadesOriginales = [
    { id: 1, ut_id: 'UT1', peso: 50, eval: 1 }, { id: 2, ut_id: 'UT2', peso: 50, eval: 1 },
    { id: 3, ut_id: 'UT3', peso: 50, eval: 2 }, { id: 4, ut_id: 'UT4', peso: 50, eval: 2 },
    { id: 5, ut_id: 'UT5', peso: 50, eval: 3 }, { id: 6, ut_id: 'UT6', peso: 50, eval: 3 },
  ]

  it('tras 3→2→3, las UT y las actividades vuelven exactamente a su evaluación original', () => {
    const uts = utsOriginales.map(u => ({ ...u }))
    const actividades = actividadesOriginales.map(a => ({ ...a }))

    let mapaUt = _repartoNuevoEvalUt(uts, 2)
    uts.forEach(u => { u.eval = mapaUt[u.ut_id] })
    actividades.forEach(a => { a.eval = _nuevoEvalDeActividad(a, mapaUt) })

    mapaUt = _repartoNuevoEvalUt(uts, 3)
    uts.forEach(u => { u.eval = mapaUt[u.ut_id] })
    actividades.forEach(a => { a.eval = _nuevoEvalDeActividad(a, mapaUt) })

    expect(uts.map(u => u.eval)).toEqual(utsOriginales.map(u => u.eval))
    expect(actividades.map(a => a.eval)).toEqual(actividadesOriginales.map(a => a.eval))

    // Y, con el agrupamiento restaurado, los pesos vuelven a sumar 100 % en
    // cada evaluación (aquí sí es una garantía real, porque el reparto es par).
    for (const ev of [1, 2, 3]) {
      const suma = actividades.filter(a => a.eval === ev).reduce((s, a) => s + a.peso, 0)
      expect(suma, `evaluación ${ev}`).toBe(100)
    }
  })
})

# Simulación de curso completo — ISO (0369) con EvalFP

> **Actualización 08/07/2026:** los 8 hallazgos (H1-H8) están **corregidos** en EvalFP 3.1.0. La re-simulación con el motor corregido arroja 0 discrepancias con la guía. Ver `CORRECCIONES_EVALFP.md`. Este informe documenta el estado previo (3.0).

**Módulo:** Implantación de Sistemas Operativos · 1º ASIR · 186 h · curso 2026-2027
**Método:** se ejecutó el **motor de cálculo real de la app** (`_calcNotaRA`/`_calcNotaCE` y los pipelines de 1ª/2ª Ordinaria de `evaluaciones.js`) sobre una clase simulada de 12 alumnos, siguiendo paso a paso la *Guía para profesorado novel*. Los resultados del motor se verificaron con un recálculo aritmético independiente: **11/11 notas finales coinciden**.

## 1. Programación simulada (matriz RA → instrumento → peso)

RAs y ponderaciones oficiales del DOCM ya incluidas en la app: RA1 13% · RA2 19% · RA3 9% · RA4 16% · RA5 13% · RA6 12% · RA7 13% · RA8 5% (Σ=100). Distribución: Ev1 = RA1-RA2, Ev2 = RA3-RA5, Ev3 = RA6-RA8.

Por cada RA: **Práctica UTx (peso 30) + Examen RAx (peso 70)**; RA8 solo proyecto (instrumento «empresa»). Mínimo de instrumento fijado en la programación simulada: **examen ≥ 4** para mediar.

> Nota de comportamiento del motor: los pesos por actividad solo alimentan un **ratio global** práctica/examen del módulo (aquí 32,9% / 67,1%, porque RA8 no tiene examen). Dentro de cada RA la app hace media simple por tipo y aplica ese ratio global; el peso individual de una actividad concreta no pondera.

## 2. Evaluaciones parciales (boletín = media reponderada de los RA vistos, según guía)

| # | Alumno/a | Ev1 (RA1-2) | Ev2 acum. (RA1-5) | Ev3 acum. (RA1-8) | RA pendientes al cierre de cada Ev |
|---|---|---|---|---|---|
| 1 | Aguado, Ana | 8,9 | 9,0 | 9,1 | — |
| 2 | Barrios, Bruno | 7,3 | 7,3 | 7,4 | — |
| 3 | Cifuentes, Carla | 6,3 | 6,3 | 6,3 | — |
| 4 | Delgado, David | 5,3 | 5,3 | 5,4 | — |
| 5 | Escudero, Elena | 5,1 | 6,4 | 6,5 | Ev1: RA2 (3,99) → recuperado en Ev2 con 6,0 |
| 6 | Ferrer, Fran | 5,9 | 5,1 | 5,5 | Ev2: RA4, RA5 → RA4 rec. en Ev3 (5,3); RA5 rec. final (5,2) |
| 7 | Gil, Gema | 7,0 | 6,4 | 6,6 | RA3 (3,2 → 3,8 → 4,2): **no recupera** |
| 8 | Herrera, Hugo | 4,1 | 4,5 | 4,4 | Ev1: RA1-2 · Ev2: +RA3, RA5 · Ev3: +RA6-8 |
| 9 | Ibáñez, Irene | 6,3 | 6,3 | 6,2 | Ev3: RA6 = 5,3 con **examen 3,5** (ver hallazgo H3) |
| 10 | Jurado, Jorge | 4,7 | *Baja* | *Baja* | Baja tras Ev1; desaparece de todas las vistas (H7) |
| 11 | Lozano, Lucía | 7,7 | 7,7 | 6,9 | Ev3: RA6 (4,8), RA7 (4,0) → recupera ambos en final |
| 12 | Mena, Marcos | 5,8 | 5,8 | 5,5 | Ev3: RA6 (3,3 → 4,0 tras rec.): **no recupera** |

Observación (guía §4-5): el boletín de Elena en Ev1 sale 5,1 **con RA2 suspenso** — la media reponderada puede aprobar el boletín con un RA pendiente; el registro de pendientes por alumno es imprescindible y la app no lo genera (H5).

## 3. Evaluación final ordinaria (tras recuperación final)

| # | Alumno/a | RAs <5 | Media pond. | **App** | **Guía** (acta) | ¿Coinciden? |
|---|---|---|---|---|---|---|
| 1 | Ana | — | 9,07 | APTO 9,1 | SUPERADO **9** | ✅ |
| 2 | Bruno | — | 7,38 | APTO 7,4 | SUPERADO **7** | ✅ |
| 3 | Carla | — | 6,33 | APTO 6,3 | SUPERADO **6** | ✅ |
| 4 | David | — | 5,37 | APTO 5,4 | SUPERADO **5** | ✅ |
| 5 | Elena | — | 6,49 | APTO 6,5 | SUPERADO **6** | ✅ |
| 6 | Fran | — | 5,61 | APTO 5,6 | SUPERADO **6** | ✅ |
| 7 | **Gema** | **RA3 = 4,2** | 6,61 | **APTO 6,6** | **NO SUPERADO — 4** | ❌ **H1** |
| 9 | Irene | — (examen RA6 recuperado con 5,0) | 6,32 | APTO 6,3 | SUPERADO **6** | ✅ |
| 8 | Hugo | RA3, RA5, RA6, RA7, RA8 | 4,58 | NO APTO 4,6 | NO SUPERADO — 4 | ✅ |
| 11 | Lucía | — | 7,18 | APTO 7,2 | SUPERADO **7** | ✅ |
| 12 | **Marcos** | **RA6 = 4,0** | 5,55 | **APTO 5,6** | **NO SUPERADO — 4** | ❌ **H1** |

## 4. 2ª Ordinaria (recuperación por CE en la app)

| Alumno/a | Rec. introducida | Resultado App | Resultado Guía | ¿Coinciden? |
|---|---|---|---|---|
| Gema | CEs de RA3 = 6,0 | RA3=6,0 🔒resto → APTO 6,8 | SUPERADO 7 | ✅ correcto |
| Marcos | CEs de RA6 = 6,0 | RA6=6,0 🔒resto → APTO 5,8 | SUPERADO 6 | ✅ correcto |
| **Hugo** | **Solo CEs de RA3 = 5,5** | RA3=5,5 pero también **RA5, RA6, RA7 y RA8 pasan a 5,5** → **APTO 5,3** | **NO SUPERADO — 4** (siguen pendientes RA5-RA8) | ❌ **H2** |

## 5. Hallazgos de la auditoría

**H1 — CRÍTICO · La app no aplica la "regla de oro".** En 1ª y 2ª Ordinaria el veredicto APTO/NO APTO se decide solo con `nota final ≥ 5` (media ponderada), sin exigir todos los RA ≥ 5. Gema (RA3=4,2, media 6,6) y Marcos (RA6=4,0, media 5,6) aparecen como APTO/A; según la normativa FP deben ir al acta como NO SUPERADO (1-4). Es exactamente el "error de calificación grave" que la guía advierte. *Corrección sugerida en `renderOrd1Panel`/`renderOrd2Panel`: `apto = nFinal >= 5 && todosLosRA >= 5`.*

**H2 — CRÍTICO · Colisión de IDs de CE en la recuperación de 2ª Ordinaria.** Los CEs de todos los RA de ISO comparten identificadores (CR1, CR2…). `rec2notas` y `pardones` se guardan por `ceId` sin prefijo de RA: al calificar la recuperación de RA3 de Hugo (CR1-CR8 = 5,5), el motor la contabiliza también para RA5, RA6, RA7 y RA8, que pasan de suspensos a 5,5 y el alumno sale APTO. Cualquier alumno con ≥2 RA pendientes contamina resultados. *Corrección: clave compuesta `RA|CE` en `rec2notas_{mid}`/`pardones_{mid}` y en `ceNotaOrd2`.*

**H3 — Sin mínimos por instrumento.** La programación exige examen ≥ 4 para mediar, pero la app siempre media: RA6 de Irene figura 5,3 (aprobado) con examen 3,5, sin aviso. El profesor debe vigilarlo a mano.

**H4 — Pesos de actividad no ponderan individualmente.** Solo determinan el ratio global práctica/examen del módulo (32,9/67,1 en esta configuración, no el 30/70 declarado, porque RA8 carece de examen).

**H5 — Sin nota de boletín parcial ni informe de RA pendientes.** Las pestañas Ev1-Ev3 muestran notas por RA, pero no calculan la media reponderada del trimestre ni generan el registro de pendientes que exige la documentación (guía §7); en esta simulación se calcularon externamente.

**H6 — Recuperar antes de la ordinaria obliga a sobrescribir la nota original.** No hay campo de recuperación en parciales/1ª Ordinaria (solo en 2ª): se pierde la trazabilidad instrumento→nota original→nota rec. que pide la guía ante reclamaciones. Documentar fuera de la app (aquí, en este informe).

**H7 — El estado "Baja" borra al alumno de todas las vistas,** incluidas evaluaciones ya celebradas (Jorge tenía notas de Ev1). El acta histórica queda incompleta en pantalla, aunque las notas siguen en la BD.

**H8 — Sin redondeo de acta.** La app muestra decimales; el acta exige entero (≥0,5 al alza en CLM) y 1-4 para no superados. Calculado externamente en las tablas de este informe.

**Lo que funciona bien:** la cascada actividad→RA→nota final es matemáticamente correcta (verificación independiente 11/11), el bloqueo 🔒 de RAs/CEs aprobados en 2ª Ordinaria funciona (casos Gema y Marcos, limpios), y el flujo Ev1→Ev2→Ev3→Ordinarias reproduce el proceso de la guía.

## 6. Cargar la simulación en la app

La BD `evalfp_simulacion_ISO.db` (en esta carpeta) contiene el curso completo: módulo ISO, 12 alumnos, 15 actividades, 169 notas (estado post-recuperaciones, previo a 1ª Ordinaria) y las recuperaciones de 2ª Ordinaria de Gema, Hugo y Marcos ya introducidas.

1. Cierra EvalFP.
2. Haz copia de tu BD real: `~/Library/Application Support/EvalFP/evalfp.db` (o `.../evalfp/` si arrancas con `npm start`).
3. Sustitúyela por `evalfp_simulacion_ISO.db` renombrada a `evalfp.db`.
4. Abre EvalFP → Evaluaciones → ISO: en **1ª Ordinaria** verás a Gema y Marcos como APTO/A (H1) y en **2ª Ordinaria**, al expandir a Hugo, la contaminación entre RAs (H2).
5. Para volver, restaura tu copia.

---
*Simulación generada el 08/07/2026 ejecutando el código real de EvalFP 3.0.0 (`evaluaciones.js`, `db.js`). Detalle completo por alumno y fase en `sim_resultados.json`.*

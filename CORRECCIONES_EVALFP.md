# Correcciones EvalFP 3.1.0 — cierre de la auditoría de simulación ISO

Los 8 hallazgos del `INFORME_SIMULACION_ISO.md` están corregidos en el código de la app. Tras las correcciones se re-ejecutó la misma simulación (12 alumnos, curso completo) con el motor corregido: **14 comprobaciones app-vs-guía, 0 discrepancias** (detalle en `sim_resultados_v2.json`).

## Qué se ha cambiado y dónde

**H1 · Regla de oro (crítico).** `evaluaciones.js`: nuevo `estadoAlumno()` — APTO/A exige todos los RA ≥5 (y mínimos de examen); si falta algún RA por evaluar el resultado es PENDIENTE. Aplicado también en 2ª Ordinaria (`estadoOrd2`), en el Dashboard (tabla, tarjetas y KPIs de 1ª Ordinaria) y en el Boletín PDF, que ahora avisa: «media ≥5 pero con RA pendientes: la media no compensa».

**H2 · Colisión de CEs (crítico).** `dashboard.js` + `evaluaciones.js`: `rec2notas_{mid}` y `pardones_{mid}` usan clave compuesta `RA|CE` (p. ej. `RA3|CR1`). Calificar la recuperación de RA3 ya no altera RA5-RA8. Las recuperaciones guardadas con el formato antiguo se **migran automáticamente** al abrir Evaluaciones o Dashboard: si el alumno tiene un único RA suspenso que contenga ese CE, la clave se reasigna a ese RA; si hay varios candidatos (intención ambigua), se conserva sin efecto y la app muestra un aviso único con la lista de calificaciones a reintroducir. Verificado con test aislado: migración correcta, ambiguos detectados, claves nuevas intactas, idempotente.

**H3 · Mínimo de examen.** Campo «Mín. examen» en la pestaña Evaluaciones (config `minexam_{mid}`, vacío = sin mínimo). Un RA con examen por debajo del mínimo queda pendiente aunque medie ≥5, con aviso ⚠mín en todas las vistas.

**H4 · Ponderación real de instrumentos.** `_calcNotaRA`/`_calcNotaCE` ponderan cada actividad por su peso dentro del RA (práctica 30 / examen 70 se respeta RA a RA). Si las actividades no tienen peso, se mantiene el comportamiento anterior como fallback.

**H5 · Boletín parcial.** Cada pestaña Ev1-Ev3 abre con la tabla «Boletín»: media reponderada de los RA trabajados hasta esa evaluación y columna de RA pendientes acumulados por alumno (el registro que pide la guía §4-5 y §7).

**H6 · Recuperación con trazabilidad.** Nueva columna `notas.nota_rec` (migración automática al abrir la app). En Reg. Notas, el botón «✎ Modo recuperación» permite calificar recuperaciones sin tocar la nota original; la celda muestra ambas. Todo el motor (evaluaciones, dashboard, boletín, informes IA, export PDF) usa la nota efectiva `rec ?? original`, y las notas de RA recuperadas se marcan con «R».

**H7 · Bajas visibles.** El alumnado de baja aparece atenuado con insignia BAJA en Evaluaciones y boletines parciales (histórico conservado), excluido de KPIs y veredictos.

**H8 · Acta.** Columna «Acta» en 1ª y 2ª Ordinaria: entero con redondeo ≥0,5 al alza si el módulo está superado; 1-4 si no lo está.

## Re-simulación de verificación (motor corregido)

| Caso | Antes (3.0) | Ahora (3.1) |
|---|---|---|
| Gema — media 6,6 con RA3=3,8 | APTO 6,6 ❌ | **NO APTO/A · Acta 4 · pend. RA3** ✅ · recupera en 2ª Ord → Acta 7 |
| Marcos — media 5,5 con RA6=3,3 | APTO 5,6 ❌ | **NO APTO/A · Acta 4 · pend. RA6** ✅ · recupera en 2ª Ord → Acta 6 |
| Hugo — rec. solo de RA3 en 2ª Ord | Contaminaba RA5-RA8 → APTO ❌ | Solo cambia RA3; **NO APTO/A · Acta 4 · pend. RA5-RA8** ✅ |
| Irene — RA6 media 5,2 con examen 3,5 | Aprobado sin aviso ❌ | **⚠mín: RA6 pendiente** hasta recuperar el examen (5,0) ✅ |
| Elena/Fran/Lucía — recuperaciones | Sobrescribían la nota | Original + rec conservadas (`nota_rec`), marca R ✅ |
| Jorge — baja tras Ev1 | Desaparecía | Visible atenuado con sus notas de Ev1 ✅ |
| Boletines Ev1-Ev3 | No existían | Media reponderada + pendientes por alumno ✅ |
| Ponderación 30/70 | Ratio global 32,9/67,1 | 30/70 exacto dentro de cada RA ✅ |

Los aprobados legítimos (Ana 9, Bruno 7, Carla 6, David 5, Elena 6, Fran 6, Lucía 7) no cambian de resultado; solo varían décimas por la ponderación corregida (H4).

## Ficheros modificados

`db.js` (migración `nota_rec`, `saveNotaRec`) · `main.js` y `preload.js` (IPC) · `renderer/js/modules/evaluaciones.js` (reescrito: motor + paneles) · `renderer/js/modules/dashboard.js` (claves compuestas, regla de oro, boletín PDF) · `renderer/js/modules/notas.js` (modo recuperación) · `renderer/js/modules/ia.js` (nota efectiva) · `renderer/js/app.js` (registro de handlers) · `CHANGELOG.md` (v3.1.0). ESLint sin errores.

**Nota:** los tests unitarios (`npm test`) y e2e no se han podido ejecutar en este entorno (better-sqlite3 compilado para macOS); conviene pasarlos en tu máquina: `npm test && npm run test:e2e`.

## BD simulada actualizada

`evalfp_simulacion_ISO.db` regenerada con el nuevo esquema: 10 notas con `nota_rec` separada de la original, recuperaciones de 2ª Ordinaria con claves `RA|CE` y `minexam=4`. Instrucciones de carga en §6 del informe original. Al abrirla verás: Gema y Marcos NO APTO/A en 1ª Ordinaria con Acta 4, Hugo sin contaminación en 2ª Ordinaria, columna Acta y avisos ⚠mín.

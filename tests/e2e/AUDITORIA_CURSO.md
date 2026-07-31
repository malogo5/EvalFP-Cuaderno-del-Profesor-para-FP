# Auditoría de usuario · un curso completo en EvalFP

Recorrido automático por la interfaz real de la aplicación, de septiembre a la 2ª ordinaria,
sobre una base de datos temporal. Módulos usados: **ISO** (1º ASIR) y **OACE** (2º de Grado
Básico), con 12 alumnos, una baja a mitad de curso y alumnado que suspende RA.

Ejecutado: 31/7/2026, 16:45:19

| | |
|---|---|
| Comprobaciones correctas | 74 |
| Avisos | 0 |
| Fallos | 0 |

## Lo que funciona

- ✓ **catálogo** — la búsqueda «OACE» encuentra 1 módulo(s)
- ✓ **catálogo** — la tarjeta muestra la duración oficial (338h)
- ✓ **catálogo** — la tarjeta distingue las horas de aula (200h aula)
- ✓ **catálogo** — al seleccionarlo explica el reparto aula/empresa
- ✓ **catálogo** — ISO llega con sus 8 RA del decreto
- ✓ **módulos** — los dos módulos quedan dados de alta
- ✓ **alta de módulo** — ISO llega con 11 actividades
- ✓ **alta de módulo** — ISO: los 8 RA tienen actividad con la que calificarse
- ✓ **alta de módulo** — ISO: las ponderaciones suman 100 %
- ✓ **alta de módulo** — ISO: las UT suman las 186 h de aula
- ✓ **alta de módulo** — OACE llega con 7 actividades
- ✓ **alta de módulo** — OACE: los 4 RA tienen actividad con la que calificarse
- ✓ **alta de módulo** — OACE: las ponderaciones suman 100 %
- ✓ **alta de módulo** — OACE: las UT suman las 200 h de aula
- ✓ **alumnado** — la importación pegando la lista crea 12 alumnos de una vez
- ✓ **alumnado** — separa bien apellidos y nombre
- ✓ **alumnado** — Molina Cid se marca de baja en noviembre
- ✓ **alumnado** — el alumnado de cada módulo va por separado
- ✓ **evaluación 1** — la parrilla muestra 33 celdas de nota
- ✓ **evaluación 1** — escribir una nota en la parrilla la guarda al salir de la celda
- ✓ **evaluación 1** — 33 notas registradas
- ✓ **evaluación 1** — todas las medias están dentro de 0-10 (11 alumnos)
- ✓ **evaluación 1** — la pestaña de la evaluación muestra el resumen de la clase
- ✓ **evaluación 1** — avisa de los RA que aún están sin evaluar
- ✓ **evaluación 2** — la parrilla muestra 44 celdas de nota
- ✓ **evaluación 2** — escribir una nota en la parrilla la guarda al salir de la celda
- ✓ **evaluación 2** — 44 notas registradas
- ✓ **evaluación 2** — todas las medias están dentro de 0-10 (11 alumnos)
- ✓ **evaluación 2** — la pestaña de la evaluación muestra el resumen de la clase
- ✓ **evaluación 2** — avisa de los RA que aún están sin evaluar
- ✓ **evaluación 3** — la parrilla muestra 44 celdas de nota
- ✓ **evaluación 3** — escribir una nota en la parrilla la guarda al salir de la celda
- ✓ **evaluación 3** — 44 notas registradas
- ✓ **evaluación 3** — todas las medias están dentro de 0-10 (11 alumnos)
- ✓ **evaluación 3** — la pestaña de la evaluación muestra el resumen de la clase
- ✓ **recuperación** — la parrilla avisa de que estoy en modo recuperación
- ✓ **recuperación** — 3 celdas del alumno con RA suspensos disponibles para recuperar
- ✓ **recuperación** — la nota original se conserva al recuperar (queda el rastro de las dos)
- ✓ **1ª ordinaria** — el acta lista 24 filas de alumnado
- ✓ **1ª ordinaria** — nadie aparece como APTO teniendo RA sin superar (regla de oro)
- ✓ **1ª ordinaria** — Carrasco Nieto tiene la media aprobada (6.8)
- ✓ **1ª ordinaria** — con la media aprobada pero un RA suspenso, el resultado es NO APTO (la media no compensa)
- ✓ **1ª ordinaria** — la calificación de acta sale como número entero
- ✓ **1ª ordinaria** — el alumnado de baja aparece marcado como tal
- ✓ **2ª ordinaria** — la 2ª ordinaria muestra a quién le queda algo
- ✓ **2ª ordinaria** — se centra en el alumnado con RA pendientes
- ✓ **documentos** — exportar el PDF de notas no da error
- ✓ **documentos** — desde el panel puedo sacar el boletín de cada alumno
- ✓ **documentos** — el boletín individual se genera sin errores
- ✓ **multi-módulo** — el desplegable del lateral lista mis dos módulos
- ✓ **multi-módulo** — alumnos sigue al módulo elegido en el lateral
- ✓ **multi-módulo** — notas sigue al módulo elegido en el lateral
- ✓ **multi-módulo** — evaluaciones sigue al módulo elegido en el lateral
- ✓ **multi-módulo** — dashboard sigue al módulo elegido en el lateral
- ✓ **multi-módulo** — programacion sigue al módulo elegido en el lateral
- ✓ **multi-módulo** — en OACE solo veo su alumnado (8 filas)
- ✓ **programación** — la programación muestra las UT del módulo
- ✓ **módulos** — veo los RA del módulo con sus ponderaciones
- ✓ **módulos** — el módulo cita el decreto de Castilla-La Mancha
- ✓ **ajustes** — las copias de seguridad están a la vista, con su carpeta
- ✓ **ajustes** — puedo crear una copia a demanda y me dice cuántas hay y de cuándo
- ✓ **ajustes** — puedo cambiar el tema
- ✓ **IA** — la sección de IA abre sin romperse
- ✓ **IA** — la pestaña «plan» abre con mis módulos cargados
- ✓ **IA** — la pestaña «grupo» abre con mis módulos cargados
- ✓ **IA** — la pestaña «examen» abre con mis módulos cargados
- ✓ **IA** — la pestaña «corregir» abre con mis módulos cargados
- ✓ **IA** — la prueba escrita ofrece los 4 RA del módulo
- ✓ **IA** — la corrección desde foto trae el alumnado del módulo
- ✓ **IA** — los botones del lote no aparecen hasta verificar el reparto de fotos
- ✓ **IA** — aunque se fuerce, el lote se niega a corregir sin el reparto verificado
- ✓ **IA** — sin fotos seleccionadas avisa en lugar de intentar corregir
- ✓ **IA** — un fallo del proceso principal vuelve como error y libera el indicador
- ✓ **IA** — abrir IA sin clave configurada no lanza errores

## Capturas

Las 21 capturas del recorrido están en `tests/e2e/capturas/`.

## Errores de consola durante todo el recorrido

Ninguno.

# Registro de Cambios (Changelog) - EvalFP

Todos los cambios notables realizados en el proyecto EvalFP se documentarán en este archivo.

## [3.0.0] - 2026-07-01
### Seguridad y estabilidad
*   **XSS:** Escapado de entradas de usuario en `innerHTML` para prevenir inyección de scripts.
*   **API keys:** Cifrado de claves de API mediante almacenamiento a nivel de sistema operativo con `keytar`, con fallback opcional para evitar fallos de compilación nativa en macOS.
*   **Backups:** Copias de seguridad automáticas diarias de la base de datos, con limpieza de backups antiguos.
*   **Logging:** Logger centralizado (Winston) para sustituir los `console.log` dispersos.
*   **Compatibilidad macOS:** Wrapper seguro para `keytar` que evita errores de módulo nativo en macOS.
*   **Calidad:** 24/24 tests superados en el módulo de dashboard (QA).

## [2.0.1] - 2026-06-29
### Corrección: diálogo de reparación de Excel eliminado
*   **Problema:** Excel 365 para Mac mostraba el diálogo "Hemos encontrado un problema con el contenido de EvalFP.xlsx" en cada apertura, causado por múltiples violaciones OOXML que openpyxl 3.1.x genera de forma incorrecta.
*   **Diagnóstico:** Metodología ZIP diff (EvalFP.xlsx vs versión reparada por Excel) en 6 rondas iterativas. Se identificaron 7 causas raíz.
*   **Fix 1 — workbook.xml:** Eliminado elemento `<workbookProtection/>` vacío que openpyxl inserta por defecto.
*   **Fix 2 — styles.xml:** `<patternFill/>` sin atributo `patternType` → `patternType="none"` (requerido por esquema OOXML).
*   **Fix 3 — styles.xml:** Colores ARGB con alpha `00` (transparente) → `FF` (opaco). Afectaba a ~190 colores en borders, fills y fonts.
*   **Fix 4 — workbook.xml.rels:** Rutas `Target="/xl/..."` absolutas → relativas (e.g. `worksheets/sheet1.xml`).
*   **Fix 5 — styles.xml:** Atributos redundantes `pivotButton="0"` y `quotePrefix="0"` en los 352 elementos `cellXf` → eliminados.
*   **Fix 6 — styles.xml:** Orden de elementos hijos de `<font>` incorrecto (`<name><family><color><sz>`) → orden canónico de Excel (`<b?><i?><sz><color><name><family><scheme?>`).
*   **Fix 7 — workbook.xml:** `calcPr fullCalcOnLoad="1"` → atributo eliminado.
*   **Resultado:** EvalFP.xlsx abre sin ningún diálogo de reparación en Excel 365 para Mac. ✅
*   **Implementación:** Bloque post-save en `main()` de `build_template.py` (líneas ~3592–3645). El parche se aplica en cada generación del xlsx reescribiendo los ZIP entries afectados.

## [2.0.0] - 2026-06-29
### EvalFP 2.0 — Versión estable (Sprints 2.6 + 2.7)
*   **Sprint 2.7 (Limpieza técnica y lanzamiento):** Hardcode residual `"1º ASIR"` en tabla `_Grupos` sustituido por `MODULO['curso']`. Docstring de `build_template.py` actualizado a v2.0. `requirements.txt` creado con dependencias obligatorias (`openpyxl`) y opcionales (`anthropic`/`openai`). README completamente reescrito con estructura real v2.0, guías de uso y tabla de docs técnica. ROADMAP y CHANGELOG cerrados con todos los sprints ✅.
*   **Sprint 2.6 (Asistente IA):** Nuevo script `scripts/ai_asistente.py` con clase `IAAsistente`. Genera descriptores de rúbricas (4 niveles × CE), propuestas de actividades y borradores de informes individuales via API Claude o OpenAI. Modo DEMO automático si no hay API key. CLI con 4 comandos: `rubrica` · `actividad` · `informe` · `todo`. Flag `--ia` en `build_template.py` para generación masiva tras crear el xlsx. Nueva hoja oculta `_IA_Config` con instrucciones y comandos de ejemplo.
*   **Estructura final:** 35 hojas visibles + 19 ocultas. 7 globales + 14 hojas por módulo × 2 (ISO + PAR) + `_IA_Config`.

## [2.0.0-alpha.5] - 2026-06-29
### Añadido
*   **Sprint 2.5 (Dashboard Global):** Nueva hoja `Dashboard Global` con KPIs consolidados por módulo (Activos, Aptos, No Aptos, En Riesgo, Media, % Aprobados), fila TOTAL CURSO y accesos rápidos hipervínculo a Dashboard/Programación/Informe de cada módulo. Indicadores referenciados desde `1ªORD` y `Alumnos` de cada módulo.
*   **Sprint 2.4 (Panel Diario `Hoy`):** Hoja con fecha dinámica `=TODAY()`, tabla de módulos activos, bloque KPIs en riesgo por módulo y bloc de notas rápidas del día.
*   **Sprint 2.3 (Calendario):** Hoja global con 60 filas de eventos configurables (Examen/Entrega/Recuperación/Tutoría/Otro), dropdowns de validación para módulo, evaluación, grupo, tipo y estado.
*   **Sprint 2.2 (Biblioteca):** Hoja global con índice de todas las actividades y exámenes de todos los módulos, incluyendo instrucciones para buscar, duplicar y crear recursos.
*   **Estructura final v2.0-alpha:** 7 hojas globales + 14 hojas por módulo. Con ISO + PAR: 35 hojas visibles + 18 ocultas.

## [2.0.0-alpha.1] - 2026-06-29
### Añadido
*   **Sprint 2.1 (Multi-módulo):** `_sn()`/`_sr()` como helpers de prefijo y referencia cruzada. `_set_module_context(mod, prefix)` recarga todos los globales de módulo. Todas las referencias cruzadas en fórmulas Excel actualizadas para respetar el prefijo activo.
*   **Sprint 2.1 (`teacher_config.py`):** Nuevo fichero de configuración de carga docente — el profesor declara su lista de `(módulo, grupo)` y el generador produce un libro con todos ellos.
*   **Sprint 2.1 (`par_data.py`):** Segundo módulo de ejemplo: PAR — Planificación y Administración de Redes (6 RAs, 7 UTs, 3 evaluaciones, RA6 dual).
*   **Sprint 2.1 (Hoja `Mis Módulos`):** Portal de navegación con tabla de módulos activos, hipervínculos a Programación y Dashboard de cada módulo, y nota de uso.
*   **Sprint 2.1 (Nav global):** `GLOBAL_NAV_ITEMS` y `apply_global_header()` para hojas sin prefijo (Inicio, Config, Mis Módulos). Nav de módulo generada en `_set_module_context` con `_MODULE_NAV_ITEMS`.
*   **Sprint 2.1 (`main()`):** Nuevo flujo: hojas globales una vez → bucle por módulos con `_set_module_context` + `_build_module_sheets`. Con ISO + PAR genera 31 hojas visibles + 18 ocultas.

## [2.0.0-planning] - 2026-06-29
### Añadido
*   **Visión EvalFP 2.0:** Definición del alcance de la versión 2.0 — un único archivo para gestionar toda la carga docente del profesor (varios módulos, varios grupos, un curso académico). Documentado en `docs/version_2.md`.
*   **Casos de uso:** Catálogo de 15 casos de uso (CU01–CU15) organizados en tres áreas: Gestión académica, Evaluación y Administración. Documentado en `docs/casos_uso.md`.
*   **Architecture Decision Records:** 7 ADRs aceptadas (ADR-001 a ADR-007), incluyendo ADR-007 "Arquitectura preparada para múltiples módulos". Documentado en `docs/decisiones_arquitectura.md`.
*   **Guía de desarrollo:** Filosofía de sprints, reglas de codificación y flujo de trabajo formalizado en `docs/guia_desarrollo.md`.
*   **Reorganización docs:** Los cuatro documentos de planificación movidos a `docs/`. README actualizado con estructura real del proyecto y enlace a v2.0.

## [1.0.0-alpha.9] - 2026-06-29
### Añadido
*   **Sprint 9 (Dashboard — hoja nueva):** Nueva hoja `Dashboard` como cuadro de mando del grupo. Tres secciones: 6 KPIs globales (Activos, Aptos, No Aptos, Media, Máxima, En Riesgo <4), tabla de seguimiento individual de 30 alumnos con semáforo dinámico (🟢 NOTABLE ≥7 · 🟡 APTO 5-6.9 · 🔴 NO APTO <5) y % de evaluaciones completadas, y panel de medias del grupo por RA (desde Reg. Notas). Todas las celdas son fórmulas: el Dashboard se actualiza solo al introducir notas.
*   **Sprint 9 (Navegación):** Enlace `📊 Dashboard` añadido a la barra de navegación. El libro tiene ahora 16 hojas visibles.

## [1.0.0-alpha.8] - 2026-06-29
### Añadido
*   **Sprint 8 (Boletín — dinámico):** `build_boletin` reescrito sin ningún hardcode de columnas. Las secciones de evaluación se generan en bucle desde `EVAL_RAS` y `ACTIVIDADES`: columnas de examen, actividades y RAs se calculan desde `_RN_EX_START`, `_RN_ACT_START` y `RN_RA_COL`. Las notas de evaluación usan `_EV_NOTA_COL`/`_EV_RES_COL`; la nota final usa `_ORD1_FINAL_COL_L`. El Boletín funciona correctamente con cualquier módulo sin cambiar una sola línea.
*   **Sprint 8 (Informe Grupo — hoja nueva):** Nueva hoja `Informe Grupo` con: bloque KPIs (activos, aprobados, suspensos, media, máx., mín., en riesgo) desde `1ªORD`; medias del grupo por RA; listado completo de 30 alumnos con nota por RA, nota final y resultado. Área de impresión configurada (landscape, fit-to-page).
*   **Sprint 8 (constantes módulo-nivel):** Nuevas constantes `_EV_NOTA_COL`, `_EV_RES_COL`, `_ORD1_FINAL_COL_L`, `_ORD1_RES_COL_L` calculadas dinámicamente, compartidas por `build_boletin`, `build_informe_grupo` y `build_data_sheets`.
*   **Sprint 8 (Navegación):** Enlace `📊 Inf.Grupo` añadido a la barra de navegación. El libro tiene ahora 15 hojas visibles.

## [1.0.0-alpha.7] - 2026-06-29
### Añadido
*   **Sprint 7 (Rúbricas — hoja nueva):** Nueva hoja `Rúbricas` con una rúbrica por cada RA del módulo. Cada rúbrica muestra todos los CEs del RA como indicadores de logro (filas) × 4 niveles de desempeño (columnas): No Alcanzado (0-4), En Proceso (5-6), Alcanzado (7-8), Sobresaliente (9-10). Descriptores auto-generados desde los datos del módulo, editables por el profesor.
*   **Sprint 7 (Rúbricas — datos):** Cabecera de cada RA incluye badge EV1/EV2/EV3, ponderación y marca DUAL. Fila resumen muestra el total de indicadores y la escala de conversión nivel→nota.
*   **Sprint 7 (Navegación):** Enlace `🎯 Rúbricas` añadido a la barra de navegación de todas las hojas.
*   **Sprint 7 (_Actividades):** Nueva tabla oculta `_Actividades` con todas las actividades prácticas y exámenes generados desde `ACTIVIDADES` (id, UT, RA, eval, CEs, descripción, tipo).

## [1.0.0-alpha.6] - 2026-06-29
### Añadido
*   **Sprint 6 (Motor — cascada completa):** La hoja `1ªORD` ya no usa entrada manual para las notas RA. Cada celda RA usa `=IFERROR('Reg. Notas'!XX{fila},"")` — la cadena completa es ahora: **Actividades → Reg.Notas → Evaluación 1/2/3 → 1ªORD → Nota Final** sin intervención manual.
*   **Sprint 6 (1ªORD — badge EV):** Fila 8 añade badge de evaluación (EV1/EV2/EV3) sobre cada columna RA con código de color, y fila 9 muestra la ponderación. Subtítulo dinámico desde `MODULO`.
*   **Sprint 6 (2ªORD — auto-referencia):** El profesor introduce el número de alumno/a (1-30) en columna B. El nombre se auto-rellena desde `Alumnos` y la Nota 1ªORD se auto-rellena desde `1ªORD` via `INDEX`. Solo queda introducir manualmente la Nota Extraordinaria.
*   **Sprint 6 (_Evaluaciones — fórmulas):** La tabla oculta `_Evaluaciones` se puebla con 90 filas reales (30 alumnos × 3 evals) que referencian mediante fórmulas `nota_eval` y `resultado` desde cada hoja `Evaluación N`.
*   **Sprint 6 (títulos dinámicos):** Subtítulos de `Boletín`, `Resumen` y `2ªORD` ahora usan `MODULO`. Eliminados todos los textos hardcodeados "ISO 1º ASIR" del generador.

## [1.0.0-alpha.5] - 2026-06-29
### Añadido
*   **Sprint 5 (Actividades — generación dinámica):** Nueva constante `ACTIVIDADES` calculada automáticamente desde `ASIGNACIONES`: una práctica por asignación primaria (UT y RA en la misma evaluación). Se eliminan las actividades hardcodeadas.
*   **Sprint 5 (Actividades — nuevas columnas):** La hoja `Actividades` incluye ahora: **Eval.** (badge EV1/EV2/EV3 con color), **UT**, **RA** (badge coloreado), **CEs vinculados** (lista de criterios de evaluación de esa actividad), Descripción, Instrumento, Tipo, Peso (%), Nota máx. Título y subtítulo dinámicos desde `MODULO`.
*   **Sprint 5 (Reg. Notas — dinámico):** `build_reg_notas` ya no hardcodea IDs de actividades ni el mapa `ra_act_map`; ambos se calculan desde `ACTIVIDADES`. `RN_RA_COL` (referencia cruzada RA→columna) también es dinámico. El subtítulo incluye módulo y año desde `MODULO`.
*   **Sprint 5 (Arquitectura):** Eliminada la constante `RN_RA_START = 16` hardcodeada. Las variables `_RN_ACT_START`, `_RN_EX_START`, `_RN_RA_START` se calculan en cascada para ser correctas con cualquier módulo.

## [1.0.0-alpha.4] - 2026-06-29
### Añadido
*   **Sprint 4 (Programación — módulo agnóstico):** El título y subtítulo de la hoja `Programación` se generan dinámicamente desde `MODULO` (`abrev`, `curso`, `nombre`, `anno`). Ya no hay texto hardcodeado del módulo ISO.
*   **Sprint 4 (Programación — columna Evaluación):** Nueva columna `Eval.` (EV1/EV2/EV3) con código de color por evaluación (azul/naranja/verde) en el mapa de UTs y en la tabla resumen de RAs.
*   **Sprint 4 (Programación — columna Instrumento):** Nueva columna `Instrumento(s)` que muestra los instrumentos de evaluación de cada RA (📝 Examen, 🔧 Práctica, 🏢 Empresa) leídos desde `RA_INSTRUMENTOS` en `iso_data.py`.
*   **Sprint 4 (Programación — layout extendido):** Layout ampliado de columna K a columna M. Tabla resumen de RAs también incluye columnas Eval. e Instrumento. Paneles congelados actualizados a `D10`.

## [1.0.0-alpha.3] - 2026-06-29
### Añadido
*   **Sprint 3 (Boletín Individual):** Nueva hoja `Boletín` con selector de alumno/a (número 1-30). Muestra automáticamente, mediante fórmulas INDEX, todas las notas de actividades, exámenes, RAs por evaluación y nota final del módulo. Se actualiza instantáneamente al cambiar el número de alumno/a.
*   **Sprint 3 (Alumnos):** Dropdown de estado (Activo / Pendiente / Baja) en columna J con validación de datos. Contadores automáticos de activos, bajas y pendientes en fila 8.
*   **Sprint 3 (Navegación):** Enlace `📄 Boletín` añadido a la barra de navegación de todas las hojas.

## [1.0.0-alpha.2] - 2026-06-29
### Añadido
*   **Sprint 2 (Motor de datos):** Cuatro nuevas tablas relacionales ocultas: `_Alumnos` (espejo relacional de la hoja Alumnos), `_Grupos` (datos del módulo y grupo), `_Notas_Actividades` (esquema tabla larga alumno×actividad×nota), `_Evaluaciones` (esquema resultados por alumno y periodo).
*   **Sprint 2 (Nombres automáticos):** Las columnas de nombre en Reg. Notas, Evaluación 1/2/3, 1ªORD y 2ªORD ahora tiran de la hoja Alumnos mediante fórmulas. Escribe el nombre una sola vez y aparece en todas las hojas.
*   **Reg. Notas (Exámenes):** Nuevas columnas EX1, EX2, EX3 para registrar la nota del examen de cada evaluación. Nota de cada RA = `PESO_EXAMEN × examen + PESO_PRACTICA × media_actividades`.
*   **Configuración (Pesos):** Dos campos editables `Peso examen` y `Peso prácticas` (por defecto 75%/25%) como nombres de rango globales. Cambiarlos actualiza todas las fórmulas de Reg. Notas en cascada.
*   **Evaluación 1/2/3 (Cascada):** Las columnas de nota RA en las hojas de Evaluación ahora referencian directamente Reg. Notas, cerrando el circuito de cascada desde Configuración hasta las notas finales.
*   **Año académico:** Corregido a 2026-2027 en todas las cabeceras.

## [1.0.0-alpha.1] - 2026-06-29
### Añadido
*   **Sprint 1 (Navegación):** Barra de navegación unificada con hipervínculos nativos estilizados (activa/inactiva) en fila 5 de todas las hojas. Compatible con Excel en Mac, Windows y Office 365 sin necesidad de macros.
*   **Sprint 1 (Diseño):** Estructura de filas estandarizada en todas las hojas (fila 1 cortesía, 2-3 encabezado, 4 separador, 5 navegación, 6 separador, 7+ contenido). Paneles congelados a partir de fila 12 en Evaluaciones y Resumen.
*   **Sprint 1 (Configuración):** Pestaña `Configuracion` rediseñada con 3 bloques laterales: *Datos del Curso*, *Motor de Evaluación* y *Preferencias del Sistema*.
*   **Sprint 1 (VBA):** Creación del módulo de macros `src/vba/EvalFP_Macros.bas` con las macros `ExportarBoletinesPDF`, `LimpiarCalificaciones` y `RespaldarLibro`.
*   **Sprint 1 (Motor):** Fórmulas `AVERAGEIFS` relacionales actualizadas para reflejar el nuevo layout (datos de alumnos en fila 12). Cálculo dinámico de columna de Nota Evaluación en función del número real de CEs por evaluación.

## [1.0.0-alpha.0] - 2026-06-29
### Añadido
*   **Sprint 0 (Estructura Base):** Creación del repositorio con carpetas `docs`, `scripts` y `src`.
*   **Sprint 0 (Documentación):** Creación del `README.md`, `ROADMAP.md` y `CHANGELOG.md`.
*   **Sprint 0 (Arquitectura):** Especifiación de reglas de codificación y diseño de datos en `docs/arquitectura.md` y `docs/modelo_datos.md`.
*   **Sprint 1 (Plantilla Base - En progreso):** Preparación del script `scripts/build_template.py` para generar el libro de Excel `src/EvalFP.xlsx`.


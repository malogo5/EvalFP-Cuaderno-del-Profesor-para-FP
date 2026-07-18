# Hoja de Ruta (Roadmap) - EvalFP

> **Estado actual: v3.0.0 — en desarrollo activo** (2 jul 2026)
> EvalFP v3 es una app Electron desktop que reemplaza el flujo basado en Excel.
> v1.0 y v2.0 (Excel) completadas. v3.0 en Semana 2 del plan de securización.

---

## Versión 3.0 — App Electron Desktop (En curso)

### ✅ Completado

**Base de la app**
- Electron + SQLite (`better-sqlite3`), sin dependencia de Excel ni Python para funcionalidad principal
- Módulos prebaked desde DOCM Castilla-La Mancha (JSON estático)
- Sidebar con 9 secciones, redimensionable por arrastre

**Programación**
- Tabla de UTs editable (añadir/borrar, asignar RA/CE)
- Plan de actividades por evaluación (exámenes + prácticas)
- Ponderaciones por RA y módulo
- Selector 2/3 evaluaciones con redistribución proporcional
- Distribución de RAs derivada de UTs (fuente de verdad)

**Alumnos, Notas, Evaluaciones, Dashboard**
- CRUD alumnos con importación bulk
- Grid de notas con navegación Excel (flechas, Enter, Tab)
- Exportación PDF de notas y boletines por alumno
- Dashboard con KPIs y semáforo individual

**Seguridad (Semana 1 — 1 jul 2026)**
- XSS prevention (28 instancias)
- API keys cifradas con keytar + fallback DB
- Backups automáticos diarios (node-schedule)
- Logging centralizado (Winston)

**Seguridad (Semana 2 — 2 jul 2026)**
- Validación en preload.js (SEC-005)
- Rollback en saveAlumno por race condition (SEC-009)
- Sanitización args spawn IA (SEC-010)
- Utilidades: CSRF token, Session Manager, Password Validator, Rate Limiter

**Testing**
- Vitest configurado
- 15 tests unitarios para db.js (módulos, alumnos, notas, config, cascade)

### 🔲 Pendiente

**Semana 2 (8-14 jul 2026)**
- [ ] E2E tests con Playwright (flujo crear módulo → alumno → nota → PDF)
- [ ] QA módulo IA con API key real (validar respuestas Python)

**Semana 3 (15-21 jul 2026)**
- [ ] QA módulo Ajustes completo
- [ ] Actualizar `/docs/refactor/` con estado de seguridad real
- [ ] Crear `/docs/refactor/11_SECURITY.md`

**Semana 4 (22-28 jul 2026)**
- [ ] `npm audit` limpio
- [ ] Build macOS + Windows (DMG + NSIS)
- [ ] Release v3.0.0-rc.1 con release notes de seguridad

**Funcionalidad v3.1 (post-RC1)**
- [ ] Nota final ponderada (media de evaluaciones con peso configurable)
- [ ] 2ª Ordinaria / recuperación por alumno
- [ ] Multigrupo por módulo (actualmente 1 grupo por módulo)
- [ ] Rúbricas por RA con niveles de logro
- [ ] Backup/restauración manual desde UI
- [ ] Calendario académico (exámenes, entregas, recuperaciones)

---

## Versión 2.x — EvalFP Multigrupo / Multimódulo ✅

### Sprint 2.1 – Arquitectura multigrupo ✅
*   `teacher_config.py`: configuración de carga docente (lista de módulos + grupos).
*   `_set_module_context()` y helpers de prefijo `_sn()`/`_sr()`.
*   Segundo módulo de ejemplo: `par_data.py` (PAR).
*   Nueva hoja global `Mis Módulos` con navegación por hipervínculo.

### Sprint 2.2 – Biblioteca de Recursos ✅
*   Hoja global `Biblioteca` con índice consolidado de actividades y exámenes de todos los módulos.

### Sprint 2.3 – Calendario Académico ✅
*   Hoja global `Calendario` con 60 eventos configurables y dropdowns de validación.

### Sprint 2.4 – Panel Diario ✅
*   Hoja `Hoy` con fecha dinámica, KPIs en riesgo y bloc de notas rápidas.

### Sprint 2.5 – Dashboard Global ✅
*   Hoja `Dashboard Global` con KPIs consolidados por módulo y fila TOTAL CURSO.

### Sprint 2.6 – Asistente IA ✅
*   `scripts/ai_asistente.py`: clase `IAAsistente` para descriptores de rúbricas, propuestas de actividades e informes individuales via Claude / OpenAI.
*   Hoja oculta `_IA_Config`. Flag `--ia` en `build_template.py`.

### Sprint 2.7 – Lanzamiento EvalFP 2.0 ✅
*   Limpieza de hardcodes residuales, `requirements.txt`, README v2.0, documentación técnica cerrada.

### v2.0.1 – Corrección OOXML (diálogo de reparación Excel) ✅
*   Eliminado diálogo "Hemos encontrado un problema con el contenido de EvalFP.xlsx".
*   7 violaciones OOXML de openpyxl corregidas mediante bloque post-save en `build_template.py`.
*   Ver CHANGELOG [2.0.1] para detalle completo.

---

## Versión 1.0 — EvalFP Monomódulo ✅

Este bloque contiene la planificación original de EvalFP v1.0, organizada en **14 Sprints**.

---

---

## Sprint 0 – Fundación del proyecto ✅
*   **Objetivo:** Preparar el proyecto para que sea mantenible durante años.
*   **Entregables:**
    *   Repositorio estructurado.
    *   Documento de arquitectura.
    *   Modelo de datos.
    *   Convenciones de nombres.
    *   Changelog y Roadmap.
*   **Estado:** ✅ Completado.

## Sprint 1 – Núcleo del Excel ✅
*   **Objetivo:** Construir el libro de Excel base definitivo.
*   **Entregables:**
    *   Estructura completa de hojas (Visibles: Inicio, Configuración, Alumnos, Actividades, Reg. Notas, Resumen, 3 Evaluaciones).
    *   Tablas maestras cargadas con datos de ejemplo.
    *   Configuración y variables globales en 3 bloques temáticos.
    *   Estilo visual premium (Azul Marino / Ice Blue, Segoe UI) y navegación con hipervínculos.
    *   Módulo VBA exportable (`EvalFP_Macros.bas`) para PDF, limpieza y backups.
*   **Estado:** ✅ Completado.

## Sprint 2 – Motor de datos ✅
*   **Objetivo:** Diseñar la base de datos interna relacional del Excel.
*   **Tablas creadas:** `_Alumnos`, `_Grupos`, `_UTs`, `_RAs`, `_CEs`, `_Asignaciones`, `_Notas_Actividades` (esquema), `_Evaluaciones` (esquema).
*   **Mejora clave:** nombres del alumnado se auto-poblan desde la hoja Alumnos a todas las hojas de notas (Reg. Notas, Evaluación 1/2/3, 1ªORD, 2ªORD).
*   **Estado:** ✅ Completado.

## Sprint 3 – Gestión de alumnos e Informes Básicos ✅
*   **Objetivo:** Módulo de alumnos terminado con informes individuales iniciales.
*   **Entregables:**
    *   Hoja Alumnos mejorada: dropdown de estado (Activo/Pendiente/Baja), contadores automáticos.
    *   Nueva hoja **Boletín Individual**: selector de alumno/a, muestra automáticamente notas de actividades, exámenes, RAs, evaluaciones y nota final.
*   **Estado:** ✅ Completado.

## Sprint 4 – Programaciones ✅
*   **Objetivo:** Carga automática de cualquier módulo mapeando la estructura completa: Módulo → RA → CE → Instrumentos → Ponderaciones.
*   **Entregables:**
    *   Hoja `Programación` con título y subtítulo dinámicos desde `MODULO` (módulo agnóstico).
    *   Nueva columna **Evaluación** (EV1/EV2/EV3) con badge de color en el mapa de UTs y en la tabla resumen.
    *   Nueva columna **Instrumento(s)** (📝 Examen · 🔧 Práctica · 🏢 Empresa) leída desde `RA_INSTRUMENTOS`.
    *   Layout extendido A–M. Tabla resumen de RAs también incluye Eval. e Instrumento.
*   **Estado:** ✅ Completado.

## Sprint 5 – Actividades ✅
*   **Objetivo:** Actividades auto-generadas desde los datos del módulo y vinculadas a sus CEs, con estructura lista para alimentar el motor de evaluación.
*   **Entregables:**
    *   Hoja `Actividades` regenerada dinámicamente desde `ASIGNACIONES` (una práctica por UT + exámenes por evaluación).
    *   Columnas: **Eval** · **UT** · **RA** · **CEs vinculados** · Descripción · Instrumento · Tipo · Peso (%) · Nota máx.
    *   Color coding por evaluación. Título dinámico desde `MODULO`.
    *   Hoja `Reg. Notas` actualizada para ser dinámica: número de actividades y exámenes se calcula desde los datos del módulo.
    *   Subtítulo de `Reg. Notas` dinámico (elimina hardcode "ISO 1º ASIR").
*   **Estado:** ✅ Completado.

## Sprint 6 – Motor de evaluación ✅
*   **Objetivo:** Implementación del motor de cálculo automático: Alumno → Actividad/Evidencia → CEs → RAs → Promedio de Evaluación → Nota Final.
*   **Entregables:**
    *   **Cascada cerrada:** Actividades → Reg. Notas → Evaluación 1/2/3 → 1ªORD → Nota Final, 100% automática sin entrada manual de notas intermedias.
    *   **1ªORD:** RAs con fórmula `=IFERROR('Reg. Notas'!XX{fila},"")`. Badge EV1/EV2/EV3 y ponderaciones en cabecera. Subtítulo dinámico.
    *   **2ªORD:** Nombre y Nota 1ªORD auto-referenciados desde sus hojas origen mediante `INDEX`. Solo se introduce manualmente el número de alumno y la nota extraordinaria.
    *   **_Evaluaciones:** 90 filas reales con fórmulas a Evaluación 1/2/3.
    *   Eliminados todos los textos hardcodeados "ISO 1º ASIR" del generador.
*   **Estado:** ✅ Completado.

## Sprint 7 – Rúbricas ✅
*   **Objetivo:** Editor visual/gráfico de rúbricas con pesos e indicadores reutilizables.
*   **Entregables:**
    *   Nueva hoja `Rúbricas`: una rúbrica por RA con sus CEs como indicadores × 4 niveles de desempeño (No Alcanzado · En Proceso · Alcanzado · Sobresaliente).
    *   Descriptores auto-generados desde los datos del módulo (editables). Peso equitativo por CE (modificable).
    *   Badge EV, ponderación y marca DUAL en la cabecera de cada RA. Fila resumen con escala nivel→nota.
    *   `🎯 Rúbricas` añadido a la barra de navegación. Nueva tabla oculta `_Actividades`.
*   **Estado:** ✅ Completado.

## Sprint 8 – Informes Avanzados ✅
*   **Objetivo:** Generación automatizada de reportes en PDF detallados para alumnos, grupos, tutores e inspección educativa.
*   **Entregables:**
    *   **Boletín dinámico:** Reescrito sin ningún hardcode de columnas — funciona con cualquier módulo. Secciones de evaluación generadas en bucle. Área de impresión configurada (portrait, fit-to-page).
    *   **Informe Grupo:** Nueva hoja con KPIs del grupo (activos, aprobados, suspensos, media, máx/mín, en riesgo), medias por RA y listado completo de 30 alumnos con notas desde `1ªORD`. Área de impresión landscape.
    *   **Constantes de referencia cruzada:** `_EV_NOTA_COL`, `_EV_RES_COL`, `_ORD1_FINAL_COL_L`, `_ORD1_RES_COL_L` — calculadas dinámicamente y reutilizables.
    *   15 hojas visibles en el libro. Enlace `📊 Inf.Grupo` en navegación.
*   **Estado:** ✅ Completado.

## Sprint 9 – Dashboard (Cuadro de Mando) ✅
*   **Objetivo:** Pantalla principal con KPIs globales, semáforos de riesgo por alumno y panel de rendimiento por RA.
*   **Entregables:**
    *   Nueva hoja `Dashboard` con tres secciones: **Indicadores Globales** (6 KPIs: Activos, Aptos, No Aptos, Media, Máxima, En Riesgo), **Seguimiento Individual** (tabla de 30 alumnos con nota por Evaluación, Nota Final y semáforo 🟢/🟡/🔴), **Rendimiento por RA** (media del grupo para cada RA desde Reg. Notas).
    *   Todos los datos con fórmulas referenciadas a `1ªORD`, `Evaluación 1/2/3` y `Reg. Notas` — se actualizan solos al introducir notas.
    *   Semáforo: 🟢 NOTABLE (≥7) · 🟡 APTO (5-6.9) · 🔴 NO APTO (<5). KPI "En Riesgo" = alumnos con nota final < 4.
    *   Enlace `📊 Dashboard` añadido a la barra de navegación. 16 hojas visibles en el libro.
*   **Estado:** ✅ Completado.

## Sprint 10 – Exportación y Automatización (CU09, CU10)
*   **Objetivo:** Copias de seguridad automáticas y exportación masiva a PDF de boletines e informes.
*   **Entregables previstos:** Macro `ExportarBoletinesPDF` (un PDF por alumno), macro `RespaldarLibro` (copia con fecha en nombre), exportación del Informe Grupo a PDF landscape.

## Sprint 11 – Historial y Auditoría (CU11)
*   **Objetivo:** Registro de cambios en calificaciones para transparencia y atención a reclamaciones.
*   **Entregables previstos:** Hoja oculta `_Historial` que registra fecha, celda, valor anterior y valor nuevo mediante evento `Worksheet_Change`. Filtros por alumno y por fecha.

## Sprint 12 – Optimización y Cierre v1.0 (CU15)
*   **Objetivo:** Refactorización, pruebas de campo y empaquetado del producto v1.0.
*   **Entregables previstos:** Revisión completa de fórmulas, guía de uso para el profesorado, instalador simplificado (ejecutar `build_template.py` y abrir el xlsx).

## Sprint 13 – EvalFP 1.0 (Lanzamiento)
*   **Objetivo:** Primera versión estable y distribuible para profesorado de FP.

---

# EvalFP 2.0 — Cuaderno del Profesor (multi-módulo, multi-grupo)

> Visión completa: [docs/version_2.md](docs/version_2.md)  
> Casos de uso: [docs/casos_uso.md](docs/casos_uso.md)  
> Decisiones de arquitectura: [docs/decisiones_arquitectura.md](docs/decisiones_arquitectura.md)

**Objetivo:** Un único archivo gestiona toda la carga docente de un profesor: varios módulos, varios grupos, un curso académico completo. El motor de evaluación de v1.0 se convierte en el núcleo de una plataforma de gestión integral.

## Sprint 2.1 – Multigrupo y Multimódulo (CU01, CU02, CU03, CU04) ✅
*   **Objetivo:** Soporte para varios módulos y grupos dentro del mismo libro.
*   **Entregables:**
    *   Nuevo módulo de ejemplo `par_data.py` (Planificación y Administración de Redes, 6 RAs, 7 UTs).
    *   `teacher_config.py`: el profesor define su carga docente como lista de `(módulo, grupo)` — fácil de ampliar.
    *   `_sn(name)` / `_sr(name)`: helpers para prefijo de hojas y referencias cruzadas en fórmulas Excel.
    *   `_set_module_context(mod, prefix)`: recarga todos los globales de módulo antes de cada generación.
    *   Hojas globales sin prefijo: `Inicio`, `Configuración`, `Mis Módulos` con nav global.
    *   Hojas de módulo con prefijo `{ABREV} · `: 16 hojas por módulo (Programación → Dashboard + hojas ocultas).
    *   `Mis Módulos`: tabla de módulos activos con hipervínculos directos a Programación y Dashboard de cada uno.
    *   `main()` refactorizado: genera hojas globales una vez y luego itera sobre `TEACHER_MODULES`.
    *   Con 2 módulos (ISO + PAR): **31 hojas visibles + 18 ocultas** generadas sin errores.
*   **Estado:** ✅ Completado.

## Sprint 2.2 – Biblioteca de Recursos (CU05, CU12, CU13, CU14) ✅
*   **Objetivo:** Repositorio compartido de actividades, exámenes y rúbricas reutilizables entre módulos.
*   **Entregables:**
    *   Nueva hoja global `Biblioteca` con índice de todas las actividades y exámenes de todos los módulos activos.
    *   Columnas: ID · Módulo · RA · Descripción · Instrumento · Tags · Eval · Peso.
    *   Instrucciones integradas para CU13 (buscar), CU12 (duplicar), CU14 (crear rúbrica) y CU05 (crear actividad).
*   **Estado:** ✅ Completado.

## Sprint 2.3 – Calendario Académico ✅
*   **Objetivo:** Vista de calendario con exámenes, entregas y recuperaciones del curso completo.
*   **Entregables:**
    *   Nueva hoja global `Calendario` con 60 filas de eventos configurables.
    *   Dropdowns de validación: Módulo · Evaluación (EV1/EV2/EV3) · Grupo · Tipo (Examen/Entrega/Recuperación/Tutoría) · Estado.
    *   Campos de fecha con formato DD/MM/YYYY.
*   **Estado:** ✅ Completado.

## Sprint 2.4 – Panel Diario del Profesor ✅
*   **Objetivo:** Vista de lo que el profesor tiene pendiente hoy.
*   **Entregables:**
    *   Nueva hoja global `Hoy` con: fecha de hoy dinámica (`=TODAY()`), módulos activos con acceso directo al Dashboard, KPIs de alumnos en riesgo por módulo (referenciados desde `{ABREV} · Dashboard`), bloque de notas rápidas del día (8 filas libres).
*   **Estado:** ✅ Completado.

## Sprint 2.5 – Dashboard Global del Curso ✅
*   **Objetivo:** KPIs consolidados de toda la carga docente.
*   **Entregables:**
    *   Nueva hoja global `Dashboard Global` con tabla de KPIs por módulo: Activos · Aptos · No Aptos · En Riesgo · Media · % Aprobados.
    *   Fila TOTAL CURSO con sumas y promedios globales.
    *   Accesos rápidos (hipervínculos) al Dashboard, Programación e Informe Grupo de cada módulo.
    *   Todos los indicadores referenciados directamente desde las hojas `1ªORD` y `Alumnos` de cada módulo.
    *   **Estructura final:** 7 hojas globales + 14 hojas por módulo = **35 hojas visibles** (con ISO + PAR).
*   **Estado:** ✅ Completado.

## Sprint 2.6 – Asistencia IA (Generación de Contenido) ✅
*   **Objetivo:** Integración de IA para la generación asistida de actividades, rúbricas y borradores de informes.
*   **Entregables:**
    *   Nuevo script `scripts/ai_asistente.py`: módulo Python standalone con clase `IAAsistente`.
    *   Tres generadores: `descriptores_rubrica()` · `propuesta_actividades()` · `borrador_informe_alumno()` · `generar_todo_modulo()`.
    *   Soporte dual Claude (anthropic SDK) / OpenAI con modo DEMO automático si no hay API key.
    *   CLI completo: comandos `rubrica` · `actividad` · `informe` · `todo` con `--ayuda`.
    *   Flag `--ia` en `build_template.py` para generación masiva tras crear el xlsx.
    *   Hoja oculta `_IA_Config` en el xlsx con instrucciones y comandos de ejemplo.
*   **Estado:** ✅ Completado.

## Sprint 2.7 – EvalFP 2.0 (Lanzamiento) ✅
*   **Objetivo:** Versión estable multi-módulo con todas las funcionalidades del Cuaderno del Profesor.
*   **Entregables:**
    *   `requirements.txt` con dependencias obligatorias y opcionales documentadas.
    *   README reescrito con estructura real v2.0, guías de uso y tabla de documentación.
    *   Último hardcode residual (`"1º ASIR"`) sustituido por `MODULO['curso']` en `_Grupos`.
    *   Docstring de `build_template.py` actualizado a v2.0 con flags de línea de comandos.
    *   Verificación final: xlsx con 35 hojas visibles + 19 ocultas (incluida `_IA_Config`).
*   **Estado:** ✅ Completado.

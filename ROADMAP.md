# Hoja de ruta de EvalFP

> **Estado: 3.7.0** — aplicación de escritorio (Electron + SQLite), catálogo completo de
> Castilla-La Mancha y auditoría integral cerrada. Agosto de 2026.

El detalle de cada versión está en [CHANGELOG.md](CHANGELOG.md); esto es solo el mapa.

## De dónde viene

EvalFP nació como un **libro de Excel** generado con Python (`build_template.py`), con hojas
de evaluación y apuntes en HTML. Llegó a la versión 2.0.1 y se quedó pequeño: un archivo por
módulo, fórmulas frágiles y ninguna forma decente de programar por criterios.

La versión 3 tiró ese enfoque y rehízo el cuaderno como aplicación de escritorio con base de
datos. De la etapa Excel ya no queda código en el repositorio (agosto de 2026): sigue en el
historial de git, en los commits anteriores a la 3.7.0.

## Dónde está ahora

| Área | Estado |
|---|---|
| Catálogo CLM | 91 módulos · 12 ciclos · 4.444 CE literales del DOCM |
| Motor de calificación | Único, en `renderer/js/core/calificacion.js` |
| Normativa | Orden 201/2024, con la modificación de la Orden 55/2026 |
| Auditoría integral | 30 incidencias resueltas · 1 abierta (A-5) |
| Pruebas | Unitarias con Vitest · extremo a extremo con Playwright |
| Distribución | DMG (arm64 + x64) e instalador NSIS para Windows 11 |

## Lo siguiente

1. **A-5 · Unificar el modelo de recuperación.** Hoy conviven tres mecanismos: `nota_rec` en
   las actividades, las notas por criterio de la 2ª convocatoria y los criterios dados por
   alcanzados. El diseño propuesto —una columna `convocatoria` en `actividades`, apoyada en
   el art. 21.5— está descrito en [AUDITORIA_INTEGRAL.md](AUDITORIA_INTEGRAL.md). Es el
   único punto de la auditoría que sigue abierto.
2. **Retirar la migración heredada.** `db.js` todavía convierte al arrancar los datos en JSON
   de la etapa anterior. Cuando se empaquete la 1.0 pública, ese camino sobra.
3. **Firmar los instaladores.** Sin certificado, macOS y Windows siguen avisando de
   desarrollador no identificado en cada equipo nuevo.
4. **Ámbitos de Grado Básico.** La calificación cualitativa ya está (IN/SU/BI/NT/SB); falta
   comprobarla con un ciclo de grado básico completo y real.

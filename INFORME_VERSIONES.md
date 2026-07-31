# Comparativa de versiones de EvalFP · 30/07/2026

## ✅ Limpieza ejecutada (30/07/2026)

- **Conservada:** `~/ProyectosCodex/evalfp` — única copia del proyecto en el disco.
- **A la Papelera** (recuperables hasta que la vacíes): `~/ProyectosCodex/evalfp copia`,
  `~/ProyectosCodex/evalfp_backup`, `~/Desktop/EvalFP para probar glm5.2` y
  `~/Documents/Claude/Projects/cuaderno-profesor-archivo-final.zip`. Espacio liberable: ~4,7 GB.
- **`db.js` restaurado** al de `node:sqlite` del último commit (`git status` limpio).
  El JSON descartado se guardó como copia en la carpeta de salidas de la sesión.
- **Verificado tras los cambios:** 27/27 tests unitarios ✅ · CASCADE correcto
  (borrar un módulo ya no toca las notas de los demás; borrar un alumno borra solo las suyas)
  · `nota_rec` operativa.
- **No se ha tocado** `~/Documents/EvalFP` (boletines, Material IA y backups de la app).

## Veredicto

**Versión a conservar: `~/ProyectosCodex/evalfp`** — repo git sincronizado con
GitHub (`malogo5/EvalFP-Cuaderno-del-Profesor-para-FP`), HEAD `c00f5e2` del 29/07/2026,
al día con `origin/main` (0 commits por delante o por detrás).
**Pero con una acción pendiente crítica: descartar el `db.js` local sin commitear** (ver abajo).

## Copias encontradas

| Copia | Estado | Tamaño | Veredicto |
|---|---|---|---|
| `~/ProyectosCodex/evalfp` | git, HEAD c00f5e2 (29 jul), = origin/main, 1 fichero modificado (`db.js`) | 1,2 GB | **CONSERVAR** |
| `~/ProyectosCodex/evalfp copia` | Idéntica a la anterior: 0 diferencias de código, mismo HEAD y mismo `db.js` modificado | 1,2 GB | Redundante |
| `~/ProyectosCodex/evalfp_backup` | git, HEAD `379e4aa` (20 jul) — commit que **ya no existe** en el repo actual (historia reescrita), 0 ficheros exclusivos | 1,2 GB | Obsoleta (histórico) |
| `~/Desktop/EvalFP para probar glm5.2` | Sin git. Su código es **idéntico al HEAD** de la versión buena (0 diferencias en main.js, db.js, evaluaciones.js, ai_asistente.py, notas.js) y 0 ficheros exclusivos | 480 MB | Redundante |
| `~/Documents/Claude/Projects/cuaderno-profesor-archivo-final.zip` | Archivo comprimido del 18 jul | 1,24 GB | Histórico |
| `~/Documents/EvalFP` | **NO es código**: es la carpeta de salida de la app (boletines PDF, Material IA, backups de BD) | — | **No tocar** |

Nota: la carpeta original `Cuaderno del profesor` ya no existe en el Mac
(búsqueda por nombre en todo el disco: 0 resultados); su contenido está en el zip del 18 jul.

## Calidad de las dos ramas comparadas

| Métrica | `evalfp` (29 jul) | `Escritorio glm5.2` (= HEAD) |
|---|---|---|
| ESLint | 0 errores, 120 avisos | 0 errores, 106 avisos |
| Tests unitarios | 27/27 ✅ | 27/27 ✅ |
| Archivos js/py | 223 | 87 |
| Extras | `tools/ai_toolkit`, `.evalfp-ai`, `docs/dev-notes/AI_TOOLKIT_ARCHITECTURE.md` | — |

Las correcciones de la auditoría anterior (H1-H10: regla de oro, claves `RA|CE`,
`nota_rec`, mínimo de examen, acta, Material IA, `EVALFP_TEST`…) están presentes en
todas las copias recientes.

Commits nuevos de la versión buena respecto al Escritorio: ninguno en código
(el Escritorio es un snapshot del mismo HEAD), pero la versión buena mantiene el
historial git completo y el `origin` de GitHub.

## ⚠️ CRÍTICO: el `db.js` sin commitear destruye datos

En `~/ProyectosCodex/evalfp/db.js` (y en `evalfp copia`) hay un cambio **sin commitear**
que sustituye SQLite por un almacén JSON. Su cabecera dice que «prioriza SQLite si está
disponible», pero **no lo hace**: `_mode` está fijado a `'json'` y no existe ningún
`require('node:sqlite')` en el fichero. Dos fallos verificados empíricamente:

1. **Pérdida total de la base de datos al arrancar.** Con una BD SQLite real (probado:
   1 módulo + 169 notas, 12 288 bytes), `_loadState()` intenta `JSON.parse` del fichero,
   falla, ignora el error y **reescribe `evalfp.db` con un JSON vacío de 248 bytes**.
   La app arranca mostrando 0 módulos y los datos del profesor se pierden sin backup previo.

2. **`deleteModulo` borra las notas de los demás módulos.** La emulación del CASCADE
   invierte el conjunto de IDs: recoge las actividades que *sobreviven* y borra las notas
   de esas. Probado con dos módulos A y B: al borrar A, la nota de **B** desaparece y
   queda huérfana la de A.

**Recomendación:** `git restore db.js` (o `git checkout -- db.js`) en `evalfp` para volver
al `db.js` con `node:sqlite` del HEAD, que es el que está en GitHub y en el snapshot del
Escritorio. Los tests unitarios pasan igual (27/27) con la versión de SQLite.

Mientras ese `db.js` esté activo, **no abrir la app con una base de datos real**.

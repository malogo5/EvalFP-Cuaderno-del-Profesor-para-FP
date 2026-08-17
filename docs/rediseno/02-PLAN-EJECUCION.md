# Plan de ejecución y guía del paquete

## Qué hay en esta carpeta

| Fichero | Para qué sirve |
|---|---|
| `00-CONTEXTO.md` | Memoria del trabajo: normativa verificada, decisiones de diseño, hallazgos de la auditoría y estado actual. **Léelo primero.** |
| `01-PROMPT-MAESTRO.md` | Los trece requisitos. Es lo que se le pasa al agente de código. |
| `02-PLAN-EJECUCION.md` | Este documento. |
| `03-PROGRAMACION-ISO.md` | Los tres apartados para la programación didáctica de ISO. |
| `rf-01-estado-imparticion-ra.patch` | RF-01 ya implementado, listo para aplicar. |

---

## Reparto de modelos

Opus y Sonnet están incluidos en el plan. Fable se paga aparte, así que interviene solo en
tres momentos y siempre en modo lectura. Coste estimado de las tres sesiones: 30-70 €.

---

## Paso 0 — Preparación

1. Cierra EvalFP antes de copiar la base, o copia también los ficheros `-wal` y `-shm`: con
   la aplicación abierta puedes llevarte una base incompleta.
2. Copia tu `.sqlite` real **fuera del repositorio**, a una carpeta tuya (por ejemplo
   `~/evalfp-datos-prueba/`). **El repositorio es público** y el `.gitignore` no cubre
   `tmp/`, `*.sqlite`, `-wal` ni `-shm`.
3. Añade `*.sqlite`, `*-wal` y `*-shm` al `.gitignore`.
4. Sincroniza el repositorio local con GitHub y crea la rama de trabajo.
5. Comprueba en Ajustes si Fable consume créditos prepagados aparte del plan.

## Paso 1 — Fable: diseño de la migración *(paga)*

Lectura, sin escribir código. Plan de migración de RF-02 y RF-08: tablas nuevas,
transformación de las asignaciones de `data_json`, conversión de los `nota_rec` existentes,
orden de pasos, puntos de fallo, reversión, y el contrato que debe seguir emitiendo
`export_modulo_json.py`.

## Paso 2 — Opus: RF-01

Ya está implementado el motor y la persistencia (aplicar el parche). Falta la interfaz en la
pestaña de Programación y que las pantallas pasen `raEstados` a `contextoModulo`.

## Paso 3 — Opus: RF-02

La migración, siguiendo el plan del paso 1, ensayada contra la copia externa de la base. Al
terminar: `PRAGMA foreign_key_check`, tests en verde y un test nuevo que verifique el
contrato de `export_modulo_json.py`.

## Paso 4 — Fable: punto de control *(paga)*

Sobre el `git diff` de RF-02, no sobre el repositorio entero. Una pregunta: ¿la migración
conserva todo y deja el modelo en condiciones de sostener lo que viene encima?

## Paso 5 — Opus: núcleo de evaluación

RF-03, RF-07 y RF-08, en ese orden. El informe de diferencias de la migración de RF-08 se
revisa a mano, alumno por alumno, antes de aplicar nada.

## Paso 6 — Opus: trazabilidad

RF-04, RF-05 y RF-06. RF-05 debe congelar también el **origen** del mínimo, no solo su valor.

## Paso 7 — Opus: el resto

RF-09 y RF-13 primero (protección de datos y la IA calculando por su cuenta). RF-10, RF-11 y
RF-12 son documentos y pueden esperar a septiembre.

## Paso 8 — Prueba de integración

El curso completo de septiembre al cierre de la 2ª Ordinaria, contra la copia de la base, no
contra la real.

## Paso 9 — Fable: auditoría final *(paga)*

Sobre el diff acumulado, en modo lectura, con los criterios de aceptación como contrato.
Veredicto requisito por requisito con evidencia en el código. **No** otro documento de
auditoría: ya hay siete.

## Paso 10 — Puesta en producción

Copia previa, migración de la base real, verificación, y solo entonces trabajar con ella.
Hacerlo en agosto, nunca en periodo de evaluación ni de reclamación.

## Paso 11 — La programación

Insertar los tres apartados de `03-PROGRAMACION-ISO.md` en la programación de ISO 26-27 y
llevarlos a departamento. Sin esto, los criterios que la aplicación aplica no son
defendibles.

---

## Reglas para las sesiones de Fable

- Trabaja solo dentro del repositorio; no busca ni escribe en el directorio de datos de la
  aplicación instalada.
- Si se le da acceso a una copia de la base, no vuelca su contenido en respuestas ni
  informes: recuentos e identificadores internos, nada más.
- Cada sesión de una sentada, para que el caché siga caliente.
- Veredicto, no prosa.
- Para el punto de control y la auditoría: arrancar por `git diff` y los ficheros tocados,
  ampliando solo si se justifica.

---

## Cómo aplicar el parche de RF-01

```bash
git checkout -b rf-01-estado-imparticion
git apply --check rf-01-estado-imparticion-ra.patch   # si no dice nada, aplica limpio
git apply rf-01-estado-imparticion-ra.patch
npm test                                              # deben pasar 186
git diff HEAD                                         # revisar antes de confirmar
git commit -am "RF-01: estado de impartición del RA (art. 2.3)"
```

Si `--check` protesta, la copia local difiere de GitHub: mejor que lo integre el agente de
código en lugar de forzarlo.

**Decisión pendiente**: el parche ajusta una expectativa en
`tests/unit/convocatorias.test.js`. Antes, un RA aún no impartido no figuraba como pendiente
en el boletín de trimestre; ahora sí, y el módulo sale PENDIENTE en diciembre. La media no
cambia (sigue sin contar como cero). Si se prefiere que el boletín parcial no los muestre, se
resuelve en la presentación, no en el motor.

---

## Alternativa en estudio: reescritura de la capa de interfaz

Está sobre la mesa rehacer el renderer desde cero, conservando `calificacion.js`, `db.js`,
los tests y el catálogo de `normativa/`. Motivo: la aplicación ha crecido a parches y la capa
de interfaz ha quedado incómoda (`programacion.js` con 1.741 líneas, `ia.js` con 1.340, la IA
manejada por terminal, la programación dentro de un JSON).

Criterio: **no reescribir el motor**. Los 186 tests y las siete auditorías son la única
garantía existente de que los cálculos son correctos, y reescribirlo la pone a cero justo
antes de empezar el curso. Para aumentar la confianza en los cálculos, el camino es una
batería de casos de referencia validados a mano —el alumno con todo aprobado menos un RA, el
que recupera en febrero y sube, el superado parcial por fase de empresa, el que pierde la
evaluación continua, el que tiene un RA sin dar— convertidos en tests permanentes.

# Auditoría integral de EvalFP

31/07/2026 · versión auditada **3.3.1** (commit `6ee16f9` + cambios de trazabilidad RA/CE en curso)
Alcance: arquitectura, modelo de datos, lógica de negocio, interfaz, persistencia, flujos,
cálculos, validaciones, informes, exportaciones y configuración.

## Cómo leer este informe

Cada incidencia lleva una categoría que **no se mezcla**:

- **Error confirmado** — reproducido sobre el código o ejecutando el motor real.
- **Riesgo potencial** — el diseño lo permite, no se ha observado aún en datos reales.
- **Mejora recomendada** — funciona, se puede hacer mejor.

Lo que **no** se ha podido comprobar y se declara expresamente:

- No se ha auditado el comportamiento con **claves de IA reales de Anthropic** (no configurada).
- No se ha probado la aplicación **empaquetada en Windows** (sin acceso a la máquina virtual).
- No se ha auditado el proceso de **corrección de exámenes con fotos reales** de alumnado.
- La normativa se ha contrastado con el texto vigente de la **Orden 201/2024 de CLM**; su
  modificación por la **Orden 55/2026, de 17 de abril**, no se ha leído íntegra.

## Marco normativo utilizado

- Ley Orgánica 3/2022, de 31 de marzo, de ordenación e integración de la Formación Profesional.
- Real Decreto 659/2023, de 18 de julio, por el que se desarrolla la ordenación del Sistema de FP.
- **Orden 201/2024, de 28 de noviembre**, de la Consejería de Educación, Cultura y Deportes, por la
  que se regula la evaluación, promoción, titulación y certificación académica del alumnado
  matriculado en los grados D y E de FP en Castilla-La Mancha (DOCM 03/12/2024), modificada por la
  Orden 55/2026, de 17 de abril.

Esta Orden es **la norma que rige la evaluación de los módulos que gestiona la aplicación**, y
ahora mismo **no se cita en ninguna parte del proyecto**: ni en el código, ni en la documentación,
ni en la carpeta `normativa/`, que solo contiene los decretos de currículo.

---

## Estado de corrección

Trabajo del 31/07/2026 sobre esta misma auditoría. Las incidencias marcadas
**CORREGIDO** llevan al final de su apartado la comprobación con el motor real.

| Estado | Incidencias |
|---|---|
| ✅ Corregidas | C-1, C-2, C-3, C-4, C-5, A-2, A-3, A-4, A-6, A-7, A-8, M-1, M-2, M-3, M-4, M-6 |
| ⏳ Pendientes | A-1 (superado parcial), A-5 (unificar recuperación), M-5, M-7, M-8, riesgos R-1 a R-5, mejoras de experiencia B-1 a B-5 |

---

# 1. Errores críticos

## C-1 · Cuatro pantallas dan cuatro notas finales distintas — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica** · **Prioridad: 1**
**Módulos:** Evaluaciones, Dashboard, Boletín PDF, Notas

**Descripción.** No existe un motor de cálculo único. Cada pantalla implementa el suyo:

| Pantalla | Cómo calcula la nota del alumno | Archivo |
|---|---|---|
| Evaluaciones · 1ª Ordinaria | Σ(nota_RA × ponderación_RA) / Σponderaciones, con la nota de cada RA obtenida como media de sus criterios | `evaluaciones.js:226-243` |
| Dashboard · 1ª Ordinaria | **Media aritmética simple de todas las notas de actividad** | `dashboard.js:356-358` |
| Boletín PDF | **Media de las medias de cada evaluación** (cada una ponderada por peso de actividad) | `dashboard.js:706-720` |
| Notas · columna Media | Agrupa por tipo, media simple dentro del grupo, ponderada por peso del grupo | `notas.js:42-64` |

**Evidencia.** Ejecutando los cuatro algoritmos tal cual están en el código, sobre un mismo alumno
(RA1 pond. 70 % con práctica 9 / examen 4; RA2 pond. 30 % con práctica 8 / examen 8):

```
Evaluaciones · 1ª Ordinaria : 6,25
Dashboard    · 1ª Ordinaria : 7,25
Boletín PDF                 : 6,75
Notas (columna Media)       : 6,75
```

**Impacto funcional.** La misma persona tiene cuatro calificaciones simultáneas y ninguna es
señalada como «la buena».

**Impacto educativo.** El boletín que se entrega a la familia (6,75) no coincide con el acta que
sale de Evaluaciones (6,25). Un punto de diferencia decide un aprobado.

**Riesgo en inspección.** Máximo. La observación sería inmediata: *«¿cuál de estos documentos
refleja la calificación del alumno y con qué criterio de calificación de la programación se
corresponde?»*. El art. 4.3.c de la Orden 201/2024 exige que la programación fije **los criterios
de calificación**; aquí hay cuatro criterios distintos conviviendo, ninguno documentado.

**Causa raíz.** Crecimiento por pantallas: cada una resolvió su cálculo en local en vez de llamar a
un servicio común. Los cuatro algoritmos son de autoría distinta y ninguno se apoya en el otro.

**Solución propuesta.** Extraer un único módulo `renderer/js/core/calificacion.js` con las
funciones `notaRA`, `notaModulo`, `estadoModulo` y `actaEntera`, y que **las cuatro pantallas y el
boletín consuman exclusivamente ese módulo**. El algoritmo de referencia debe ser el de
Evaluaciones (nota de RA por criterios + ponderación de RA), que es el único alineado con el
art. 2.3 de la Orden. Añadir un test que compare las cuatro salidas y falle si divergen.

**Corrección aplicada.** Creado `renderer/js/core/calificacion.js` con `notaCE`, `notaRA`,
`raMinExamKO`, `actaEntera`, `contextoModulo` y `estadoModulo`. Lo consumen Evaluaciones (1ª y 2ª
convocatoria), el Dashboard, el boletín PDF y el asistente de IA; la columna Media de la parrilla
usa su `mediaActividades` y queda documentada como media de actividades, no como nota del módulo.
Comprobado con el motor real:

```
la nota final es la media de los RA ponderada por su peso     → 6,95 · acta 7
la media no compensa un RA suspenso y el acta se topa en 4    → media 8,00 · acta 4
un RA sin calificar deja el módulo pendiente y no cuenta como cero
```

---

## C-2 · La 2ª Ordinaria no llega a ningún documento — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica** · **Prioridad: 1**
**Módulos:** Evaluaciones (2ª Ordinaria), Boletín, Asistente IA, Dashboard

**Descripción.** Las calificaciones de 2ª convocatoria (por criterio, en `rec2notas_<mid>`) y los
criterios perdonados (`pardones_<mid>`) **solo existen dentro del panel de 2ª Ordinaria**. Nada más
en la aplicación los lee.

**Evidencia.**

- `grep "_rec2Notas\|_pardones" renderer/js/modules/ia.js` → **0 resultados**. El informe de alumno
  que genera la IA se construye con `_calcNotaRA` sobre las notas de 1ª convocatoria
  (`ia.js:697`): a un alumno que ha superado el módulo en 2ª ordinaria le redacta un informe
  diciendo que tiene RA suspensos.
- `genBoletin` (`dashboard.js:665-...`) parte de `notasArr` y `nota_rec`, y **no abre** `rec2notas`
  ni `pardones`. El boletín de junio y el de la 2ª convocatoria son idénticos.
- El Dashboard tiene una función propia, `computeRec2FinalGrade` (`dashboard.js:318-352`), que
  calcula la nota de 2ª ordinaria como **media aritmética simple de los RA, sin ponderaciones**,
  mientras Evaluaciones la calcula ponderada (`evaluaciones.js:645-648`). Dos notas de 2ª
  convocatoria distintas para el mismo alumno.

**Impacto educativo.** Se rompe la cadena en el punto donde más falta hace: la convocatoria que
decide titulación y promoción.

**Riesgo en inspección.** *«Muéstreme el informe individualizado y el boletín del alumnado que
superó el módulo en la segunda convocatoria»* — los documentos dirán que sigue suspenso.

**Causa raíz.** `rec2notas` y `pardones` se guardaron como **JSON dentro de la tabla `config`**, no
como entidades del modelo de datos. Al no ser tablas, ninguna consulta las alcanza y cada pantalla
que las quiera usar tiene que reimplementar su lectura.

**Solución propuesta.** Promoverlas a tablas de primer nivel con clave foránea:

```sql
CREATE TABLE calificaciones_ce (
  alumno_id INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE CASCADE,
  ra_id TEXT NOT NULL, ce_id TEXT NOT NULL,
  convocatoria INTEGER NOT NULL DEFAULT 2,
  nota REAL, perdonado INTEGER DEFAULT 0,
  motivo TEXT, fecha TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (alumno_id, ra_id, ce_id, convocatoria)
);
```

y que el motor único de C-1 reciba la convocatoria como parámetro.

**Corrección aplicada.** Creada la tabla `calificaciones_ce` con clave foránea, fecha y motivo, y
migración automática desde la configuración al abrir la aplicación (las claves antiguas sin RA se
descartan y se registran en el log). El boletín muestra ahora el bloque «2ª Ordinaria · resultado»
con su nota, su acta y los RA que sigan pendientes; el informe de IA recalcula los RA suspensos con
las calificaciones de la segunda convocatoria. Comprobado sobre el esquema real: 2 calificaciones
migradas, 1 descartada por no indicar el RA, y al borrar el módulo no queda ninguna huérfana.

---

## C-3 · `nota_max` no lo respetaba ningún cálculo — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica** · **Prioridad: 1**
**Módulos:** Programación, Notas, Evaluaciones, Dashboard, Boletín, IA

**Descripción.** Cada actividad tiene «Nota máx», editable entre 0 y 20 (`validators.js:133`),
persistida (`actividades.nota_max`) y visible en el plan de actividades. **Ningún motor la usa.**

**Evidencia.** `grep -rn "nota_max" renderer/js scripts/*.py` → solo aparece en la validación, en la
persistencia y en el HTML del plan. Ni `_mediaActs`, ni `computeRaNotas`, ni `_calcMediaPonderada`,
ni el boletín, ni `ai_asistente.py` la leen. Además, la parrilla de notas valida siempre **0-10
fijo** (`notas.js:180` y `:192`, `min="0" max="10"`), con independencia de lo que diga `nota_max`.

**Pasos para reproducir.** Programación → poner «Nota máx» = 5 en una práctica → Notas → intentar
poner 5 (el máximo de esa actividad) → la nota entra como 5 sobre 10, no como un 10.

**Impacto educativo.** Una práctica calificada sobre 5 hunde la nota del RA a la mitad. Y al revés:
si alguien pone 20, la parrilla no deja escribir más de 10.

**Riesgo en inspección.** La calificación no se corresponde con el instrumento declarado. Es un
error de cálculo puro, difícil de defender ante una reclamación.

**Causa raíz.** Campo heredado del diseño en hoja de cálculo que nunca se conectó al motor.

**Solución propuesta.** Dos opciones, ambas válidas, pero hay que elegir una:
1. **Normalizar**: `nota_efectiva = nota / nota_max × 10` en el motor único, y que la parrilla valide
   contra `nota_max`.
2. **Eliminar el campo** de la interfaz y de la base de datos, dejando la escala 0-10 fija.
La opción 1 es la correcta si se quiere calificar con rúbricas por puntos; la 2 evita el problema.

**Corrección aplicada.** Opción 1. `notaEnEscala10()` normaliza en el motor y la parrilla valida
contra la escala de cada actividad (`max` y mensaje propios). Comprobado: práctica sobre 5 con un 4
y práctica sobre 10 con un 6 dan media 7, no 5.

---

## C-4 · El alumnado con la matrícula anulada recibía calificación y acta — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica** · **Prioridad: 1**
**Módulo:** Evaluaciones

**Descripción.** El alumnado marcado como baja se pinta en la tabla de 1ª Ordinaria con **su nota
final, su calificación de acta y su veredicto APTO/NO APTO**, solo que atenuado
(`evaluaciones.js:556`: `alumnosBaja.map(al => filaAlumno(al, true))`).

**Normativa.** Orden 201/2024, **art. 7.1**: «La anulación de la matrícula supondrá causar baja en
todos los módulos profesionales en los que esté matriculado el alumno o la alumna y, por tanto,
**no será evaluado o evaluada en ninguna de las convocatorias** correspondientes al curso».

**Riesgo en inspección.** Un acta con calificación para quien no debe ser evaluado es una
incidencia de expediente, no un detalle estético.

**Solución propuesta.** Distinguir en el modelo el estado real —**Activo / Baja por anulación /
Renuncia a convocatoria**— y que en 1ª y 2ª Ordinaria esas filas muestren la leyenda normativa
(«Anulación de matrícula», «RC») en lugar de nota, acta y veredicto. La sección debe seguir
mostrándolos, pero sin calificación.

**Corrección aplicada.** La fila del alumnado de baja sigue visible con sus notas de trabajo, pero
las columnas de nota final, acta y resultado se sustituyen por «Matrícula anulada · sin evaluación»,
con la cita del art. 7.1 en el título. Queda pendiente el estado «Renuncia a convocatoria» (RC),
anotado como parte de A-1.

---

## C-5 · Los RA suspensos no cuadran entre la 1ª y la 2ª convocatoria — **CORREGIDO 31/07/2026**

**Categoría:** Error confirmado · **Gravedad: Crítica** · **Prioridad: 1**
**Módulo:** Evaluaciones · 2ª Ordinaria

> **Estado: corregido.** Criterio adoptado por la profesora responsable: **el mínimo de examen se
> sigue exigiendo en la segunda convocatoria**. Comprobación tras el arreglo, con el mismo caso:
>
> ```
> mínimo 4 · RA1 práctica 8 / examen 3
>   sin recuperar nada       → RA pendientes: ["RA1"]   (antes: [])
>   recuperando el criterio  → RA pendientes: []
>
> RA con 4 criterios, solo CR1 y CR2 evaluados (3 y 3)
>   sin tocar                              → RA1 = 3,00
>   perdonando CR3 y CR4 (sin instrumento) → RA1 = 3,00   (antes: 4,00)
>   recuperando de verdad CR1 y CR2 a 6    → RA1 = 6,00
> ```

Tres defectos independientes que se acumulan en la misma pantalla.

### C-5.1 · El mínimo de examen deja de aplicarse en la 2ª convocatoria

En 1ª Ordinaria un RA es pendiente si `n < 5 **|| minKO**` (`evaluaciones.js:239`). En 2ª, la
condición pierde el mínimo: `if (r.nota < 5) pendientes.push(ra.id)` (`evaluaciones.js:643`).

**Evidencia** (motor real, mínimo de examen = 4; RA1 con práctica 8 y examen 3):

```
1ª Ordinaria  RA1=5.50 minExamKO=true  → RA pendientes: [RA1]   media 6.25
2ª Ordinaria  RA1=5.50 sin recuperar   → RA pendientes: []      media 6.25
Veredicto 1ª: NO APTO   ·   Veredicto 2ª: APTO
```

**El alumno pasa de NO APTO a APTO sin haber hecho nada.** Y aparece en la lista de recuperación
—porque `conRec` sí mira los pendientes de la 1ª— con todos los RA en verde y ningún criterio que
recuperar: ese es el «no cuadra» que se ve en pantalla.

**Solución.** `estadoOrd2` debe reevaluar el mínimo de examen sobre las notas de la convocatoria, o
bien la programación debe declarar si el mínimo aplica también en la segunda. Ahora mismo no hace
ni una cosa ni otra: simplemente se olvida.

### C-5.2 · La nota del RA se calcula sobre bases distintas en cada convocatoria

- **1ª**: `_calcNotaRA` promedia **solo los criterios que tienen alguna actividad**
  (`if (!ceActs.length) continue`, `evaluaciones.js:52`).
- **2ª**: `raNotaOrd2` recorre **todos los criterios del decreto** (`ceLst.map(c => c.id)`,
  `evaluaciones.js:616`) y conserva los que devuelvan algún valor.

Como `ceNotaOrd2` devuelve **5** para cualquier criterio perdonado, incluido uno que nunca se
evaluó, perdonar criterios sin actividad **cambia el denominador** de la media.

**Evidencia** (RA con 4 criterios en el decreto, programación que solo evalúa CR1 y CR2, ambos con 3):

```
1ª Ordinaria  RA1 = 3.00   (media de los dos criterios evaluados)
2ª sin tocar  RA1 = 3.00
tras «Aprobado» en CR3, que nunca se evaluó → 3.67
tras «Aprobado» también en CR4              → 4.00
```

La nota sube sin haber recuperado ninguno de los criterios realmente suspensos. Con un RA de diez o
doce criterios de los que solo se evalúan tres —situación normal en el catálogo— este camino lleva
al aprobado.

**Riesgo en inspección.** Es el peor de todos: la calificación mejora por criterios **no evaluados**.
Contradice el art. 2.2 de la Orden 201/2024, que exige verificar la adquisición de los RA «conforme
a los criterios de evaluación asociados a los mismos».

**Solución.** Una única función de nota de RA, parametrizada por convocatoria, que use **siempre el
mismo conjunto de criterios**: los que la programación evalúa. Un criterio sin instrumento no puede
entrar en ninguna media, ni siquiera perdonado.

### C-5.3 · Los criterios sin actividad son invisibles pero computan

El detalle por RA omite la fila del criterio cuando no tiene nota original, ni recuperación, ni
perdón (`evaluaciones.js:731`). Consecuencia: un RA suspenso cuyos criterios problemáticos no tienen
instrumento asignado **se muestra sin ninguna fila donde recuperar** —o con menos criterios de los
que tiene el RA— y el profesorado no encuentra dónde actuar. Al mismo tiempo, si alguno de ellos
llegó a perdonarse, sí computa en la media (C-5.2). Visible y computable no coinciden.

**Solución.** Mostrar todos los criterios del RA, marcando explícitamente los que no tienen
instrumento («sin actividad que lo evalúe»), y no permitir perdonarlos hasta que lo tengan. Es la
misma información que ya se pinta en Programación con el punto hueco en ámbar.

### C-5.4 · Los indicadores de la cabecera no se refieren al mismo grupo

`conRec` cuenta el alumnado con pendientes de la 1ª (`evaluaciones.js:655`), mientras que
«Superan 2ª», «No superan 2ª» y «Media 2ª» se calculan sobre **todo** el alumnado activo
(`evaluaciones.js:661-664`). Por eso pueden convivir «Con recuperación: 3» y «Superan 2ª: 11».

---

# 2. Errores importantes

## A-1 · No existe el estado «superado parcial» (SP)

**Categoría:** Error confirmado (omisión funcional) · **Gravedad: Alta** · **Prioridad: 2**
**Módulos:** Evaluaciones, Actas

**Normativa.** Orden 201/2024, **art. 12**: el registro del proceso de evaluación «obedecerá a tres
estados: “superado”, “superado parcial” a falta de la formación en empresa u organismo equiparado y
“no superado”». El **art. 25.4** obliga a reflejarlo en actas con las siglas **SP**, y el **art.
18.4** dice que a efectos de promoción SP cuenta como superado.

**Evidencia.** La aplicación solo produce `APTO/A`, `NO APTO/A` y `PENDIENTE`
(`evaluaciones.js:691-694`). No hay ningún rastro de «superado parcial» ni de la fase de empresa.

**Agravante.** El catálogo **sí distingue** horas de aula y horas de empresa (`horas_aula` frente a
`total_horas` en los diez módulos de Grado Básico), de modo que la aplicación conoce que existe esa
fase pero no la evalúa.

**Riesgo en inspección.** El alumnado que ha superado la formación en el centro y no la de empresa
queda registrado como «NO APTO» cuando normativamente es «SP», con consecuencias directas sobre
promoción y matrícula del curso siguiente.

**Solución.** Añadir a cada módulo el indicador «tiene fase en empresa», y al alumnado el estado de
esa fase (pendiente / superada / no superada / exenta). El veredicto pasa a calcularse con los tres
estados del art. 12.

---

## A-2 · Un RA superado podía volver a suspenderse — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Prioridad: 2**
**Módulo:** Evaluaciones (motor de cálculo)

**Normativa.** Orden 201/2024, **art. 4.3.f**: «un resultado de aprendizaje superado **no se puede
volver a evaluar**».

**Descripción.** La nota de un RA se recalcula íntegramente cada vez que se abre la pantalla, como
media de sus criterios sobre **todas** las actividades del módulo (`_calcNotaRA`). Si un RA se
trabaja en dos evaluaciones y el alumno lo tenía superado en diciembre con 6, una actividad de mayo
con un 2 lo devuelve a suspenso.

**Pasos para reproducir.** RA1 con CR1 (examen de la 1ª evaluación, nota 8) y CR2 (práctica de la 3ª
evaluación, nota 2) → RA1 pasa de 8,0 en diciembre a 5,0 en junio; con un 1 en la práctica, a 4,5 y
el módulo entero cae por la regla de oro.

**Riesgo en inspección.** El alumno puede acreditar que se le comunicó el RA como superado y que
después se le retiró. Es motivo de reclamación con recorrido.

**Solución.** Registrar el **hito de superación de cada RA** (fecha, convocatoria y nota con la que
se superó) y, una vez superado, congelarlo: las actividades posteriores no pueden bajarlo.

**Corrección aplicada.** Nueva tabla `ra_superados` y botón **«Cerrar 1ª/2ª/3ª evaluación»** en cada
pestaña de evaluación parcial: registra qué RA ha alcanzado cada alumno, con su nota y la fecha. A
partir de ahí el RA puede subir pero no bajar, y se marca como fijado. Comprobado:

```
RA1 con el examen de diciembre = 8
  mayo, práctica con un 2                → 5,00   (comportamiento anterior)
  con la 1ª evaluación cerrada           → 8,00 🔒 fijado · sin RA pendientes
```

---

## A-3 · Ponderación por criterio de evaluación — **CORREGIDO**

**Categoría:** Error confirmado (omisión funcional) · **Gravedad: Alta** · **Prioridad: 2**
**Módulos:** Programación, motor de cálculo

**Normativa.** Orden 201/2024, **art. 4.3.a**: en la programación deben constar «los resultados de
aprendizaje y sus correspondientes criterios de evaluación **con la ponderación establecida para
cada uno de ellos**».

**Evidencia.** La aplicación pondera los RA (tabla `ra_ponderaciones`) pero dentro de cada RA
promedia sus criterios **a peso igual**: `ceGrades.reduce(...) / ceGrades.length`
(`evaluaciones.js:56`). No hay ningún sitio donde asignar peso a un criterio.

**Impacto educativo.** Un criterio menor pesa lo mismo que uno esencial. Y en los módulos del
catálogo hay RA con 19 criterios: cada uno vale un 5 % del RA, se quiera o no.

**Riesgo en inspección.** La programación didáctica que exige el art. 4.3.a no se puede generar
completa desde la aplicación.

**Solución.** Añadir `peso` al criterio dentro de `data_json.ces[ra][i]`, editable en Programación,
con reparto por defecto a partes iguales y aviso si no suma 100. El motor pasa de media simple a
media ponderada de criterios.

**Corrección aplicada.** Cada criterio tiene su casilla de ponderación en la ficha del RA. Mientras
no estén todos ponderados y no sumen 100 se reparte a partes iguales, y se avisa de lo que falta.
Comprobado con CR1 = 10 y CR2 = 0:

```
sin ponderar → 5,00 · CR1 80 % → 8,00 · CR1 20 % → 2,00 · a medio ponderar → 5,00
```

---

## A-4 · Reglas normativas sin datos que las alimentaran — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Prioridad: 2**
**Módulos:** Asistente IA (Python), Programación

**Descripción.** `ai_asistente.py` aplica dos reglas que cambian el veredicto del alumno:

- **Pérdida de evaluación continua por absentismo**, a partir de `faltas_<mid>` (`ia.js:299-308`).
- **RA llave suspendido ⇒ módulo NO APTO**, a partir de `ras_llave` (`ia.js:292-296`), con código de
  alerta `RA_LLAVE_SUSPENDIDO` (`ia.js:133`).

**Evidencia.** `grep -rn "faltas_\|ras_llave" renderer/index.html renderer/js/modules/ajustes.js
renderer/js/modules/programacion.js` → **0 resultados**. Ninguna pantalla permite introducir esos
datos, y ningún módulo del catálogo los define.

**Doble problema.** (a) Las reglas están muertas: el informe nunca las aplicará. (b) Si algún día se
escriben esas claves a mano en `config`, el veredicto de un alumno cambiará sin que quede rastro
visible de por qué.

**Normativa afectada.** Ambas reglas son reales y necesarias: art. 3.3 (75 % de asistencia para
conservar la evaluación continua; art. 3.4: no aplicable en Grado Básico) y art. 4.3.a (RA que hay
que tener superados para incorporarse a la fase de empresa — el concepto de «RA llave»).

**Solución.** Implementarlas de verdad: registro de faltas por alumno y módulo, con el cálculo del
75 % y el aviso del anexo I de la Orden; y una marca «RA necesario para la fase de empresa» en la
pantalla de Programación. O retirarlas del script mientras no existan.

**Corrección aplicada.** En **Alumnos**, columna «Faltas (h)» con el porcentaje sobre las horas del
módulo y aviso en rojo al pasar del 25 %; en grado básico se indica que no aplica (art. 3.4). En
**Programación**, casilla «🔑 para empresa» en cada RA. El asistente de IA lee ya ambas cosas de
donde el profesorado las escribe, no de una clave de configuración invisible.

---

## A-5 · Dos mecanismos distintos llamados «recuperación»

**Categoría:** Error confirmado (incoherencia funcional) · **Gravedad: Alta** · **Prioridad: 3**
**Módulos:** Notas, Evaluaciones, Dashboard

**Descripción.** Conviven dos sistemas con el mismo nombre y distinto alcance:

1. **Recuperación por actividad** — `notas.nota_rec`, se activa con el botón «modo recuperación» de
   la parrilla. Sustituye la nota efectiva y **sí** afecta a la 1ª Ordinaria.
2. **Recuperación por criterio** — `rec2notas_<mid>` en `config`, se introduce en el panel de 2ª
   Ordinaria. **Solo** afecta a ese panel (ver C-2).

**Impacto.** Nada indica al profesorado cuál usar ni qué consecuencias tiene cada una. Una nota de
recuperación puesta en la parrilla en mayo modifica la calificación de la **primera** convocatoria,
que ya está en acta.

**Solución.** Un solo modelo: la calificación se asocia siempre a (alumno, criterio, convocatoria).
La parrilla de notas registra evidencias; la convocatoria decide qué se computa.

---

## A-6 · Borrar una actividad borraba sus calificaciones sin decirlo — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Prioridad: 3**
**Módulos:** Programación, base de datos

**Evidencia.** `deleteActividadRow` pregunta solo «¿Eliminar esta actividad?»
(`programacion.js:800`). La clave foránea `notas.actividad_id ... ON DELETE CASCADE`
(`db.js:197`) borra en silencio todas las notas de esa actividad. Verificado sobre el esquema real:

```
notas antes de borrar la actividad: 1
notas después                     : 0   ← cascada silenciosa
```

**Riesgo.** Pérdida irreversible de calificaciones con un clic y un «Aceptar». Solo la copia de
seguridad diaria las recupera.

**Solución.** Contar las notas asociadas antes de borrar y decirlo en el aviso («esta actividad
tiene 12 calificaciones, se perderán»); mejor aún, **archivar en vez de borrar** (`activo=0`), que
es lo que espera cualquier documento de evaluación.

**Corrección aplicada.** El aviso cuenta las calificaciones antes de preguntar: «¿Eliminar esta
actividad? Tiene 12 calificaciones puestas, que se perderán». El archivado en vez del borrado queda
como mejora (M-5).

---

## A-7 · Borrar un módulo dejaba huérfanas las calificaciones — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Prioridad: 3**
**Módulo:** Base de datos

**Evidencia.** Prueba sobre el esquema real: al borrar el módulo, `alumnos`, `actividades`, `notas`
y `ra_ponderaciones` se limpian por cascada, pero quedan **5 filas de `config` huérfanas**:

```
rec2notas_1 = {"1":{"RA1|CR1":6}}      ← calificaciones de 2ª convocatoria
pardones_1  = {"1":["RA1|CR2"]}        ← criterios perdonados
minexam_1   = 4 · faltas_1 = 35 · recmigra_avisado_1 = 1
```

**Causa raíz.** La misma que C-2: datos de evaluación guardados fuera del modelo relacional.

**Solución.** La de C-2. Mientras tanto, borrar por prefijo en `deleteModulo`.

**Corrección aplicada.** Las calificaciones por criterio se van por cascada al ser ya una tabla con
clave foránea, y `deleteModulo` limpia además las claves de configuración del módulo (mínimo de
examen, faltas y avisos). Comprobado sobre el esquema real: 0 filas huérfanas.

---

## A-8 · La numeración del alumnado se duplicaba al importar — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Prioridad: 3**
**Módulo:** Alumnos

**Evidencia.** Dos caminos calculan el número de lista de forma distinta:

- Alta manual: `Math.max(...nums) + 1` (`alumnos.js:118`) — correcto.
- Importación: `_alumnos.length + imported + 1` (`alumnos.js:176`) — **usa el recuento, no el
  máximo**.

**Pasos para reproducir.** Importar 5 alumnos (1-5) → borrar el nº 3 → importar uno más → recibe el
número **5**, duplicado con el que ya lo tenía.

**Impacto.** El número de lista es la clave con la que se anonimiza al alumnado en la corrección de
exámenes (`Alumno_03`). Dos alumnos con el mismo número es un error de identificación.

**Solución.** Usar `Math.max` también en la importación y añadir un índice único
`(modulo_id, num)`.

**Corrección aplicada.** La importación numera con `Math.max(...num) + 1`, igual que el alta
manual.

---

# 3. Errores menores

## M-1 · La base de datos aceptaba notas fuera de rango — **CORREGIDO**

**Categoría:** Riesgo potencial · **Gravedad: Media** · **Prioridad: 4**

La validación 0-10 vive solo en el renderer (`notas.js:271`). La comprobación directa sobre el
esquema inserta un `99` sin problema. Cualquier ruta que no pase por la parrilla —una importación
futura, un script, un fallo de la interfaz— puede meter notas imposibles.
**Solución:** `CHECK (nota IS NULL OR (nota >= 0 AND nota <= 10))` en la tabla.

**Corrección aplicada.** `saveNota` y `saveNotaRec` rechazan valores fuera de 0-20 (el margen cubre
los instrumentos con `nota_max` mayor que 10), y al abrir la base se avisa por consola si quedan
notas fuera de escala de versiones anteriores, sin borrarlas.

## M-2 · El alumnado sin calificar no aparecía en la 2ª Ordinaria — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Media** · **Prioridad: 3**

`conRec` selecciona a quien tiene RA con nota inferior a 5 (`evaluaciones.js:655-658`), pero **no** a
quien tiene RA **sin nota**, que es precisamente el alumnado que no se presentó. Hay que marcar «ver
todos» para encontrarlo. **Solución:** incluir también `st.sinNota.length > 0`.

**Corrección aplicada.** Concurren a la 2ª convocatoria los que tienen RA suspensos **o sin nota**, y
los indicadores de la cabecera se calculan sobre ese mismo grupo.

## M-3 · La marca de recuperación se perdía en exámenes multiunidad — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Media** · **Prioridad: 4**

`recMark` busca las actividades del RA solo por `ra_id` (`evaluaciones.js:254`). Un examen que cubre
dos unidades no tiene `ra_id`, así que su recuperación no se señaliza con la «R» de trazabilidad.
**Solución:** usar `actividadDeRa`, como ya hace el resto del motor.

**Corrección aplicada.**

## M-4 · `saveActividad` no actualizaba instrumento ni tipo — **CORREGIDO**

**Categoría:** Riesgo potencial · **Gravedad: Media** · **Prioridad: 4**

El `UPDATE` de `db.js:285` no incluía `instrumento` ni `tipo`. Hoy no hay interfaz para cambiarlos,
pero el día que la haya, los cambios se habrían perdido en silencio.

**Corrección aplicada.** El `UPDATE` los incluye con `COALESCE`, de modo que solo se tocan si vienen
en la llamada.

## M-5 · El indicador `activo` de los módulos no se usa

**Categoría:** Mejora recomendada · **Gravedad: Baja** · **Prioridad: 5**

`modulos.activo` existe y `getModulos` filtra por él, pero `deleteModulo` hace un `DELETE` real. El
borrado lógico está a medio construir: usarlo daría papelera y trazabilidad.

## M-6 · Dar un criterio por alcanzado no guardaba por qué — **CORREGIDO**

**Categoría:** Riesgo potencial · **Gravedad: Media** · **Prioridad: 3**

`togglePardonCe` marca un criterio como superado con un 5 y no registra motivo, fecha ni autoría
(`dashboard.js:35-47`). Es una decisión de evaluación sin justificación documental. En una
reclamación, «aparece un 5 y no consta por qué» es indefendible.
**Solución:** exigir un motivo breve y guardar fecha, junto con la tabla propuesta en C-2.

**Corrección aplicada.** Dar un criterio por alcanzado pide ahora la evidencia («prueba de
recuperación, trabajo entregado, observación en el taller…»), no deja continuar sin ella y guarda
motivo y fecha en `calificaciones_ce`.

## M-7 · Las evidencias de la corrección desde foto no se vinculan al alumnado

**Categoría:** Riesgo potencial · **Gravedad: Media** · **Prioridad: 4**

Las correcciones se escriben en `Documentos/EvalFP/correcciones/...` sin referencia en la base de
datos. El art. 2.4 de la Orden reconoce al alumnado el derecho de acceso a «las pruebas y documentos
de las evaluaciones que se le realicen»; conviene poder llegar al documento desde la calificación.

## M-8 · La migración de criterios reescribe la base de datos al abrir una pantalla

**Categoría:** Riesgo potencial · **Gravedad: Media** · **Prioridad: 4**

`_migrarCesActividades` (`programacion.js`) se ejecuta al cargar Programación, Evaluaciones,
Dashboard e IA, y escribe si encuentra claves antiguas. Es idempotente y necesaria, pero una
migración de datos disparada por una pantalla debería ejecutarse **una vez al arrancar**, con
registro de lo migrado.

---

# 4. Riesgos futuros

## R-1 · Los ámbitos de Grado Básico se calificarían con números

**Categoría:** Riesgo potencial · **Gravedad: Alta si se materializa**

Orden 201/2024, **art. 25.2**: los ámbitos de Comunicación y Ciencias Sociales y de Ciencias
Aplicadas se califican como **IN / SU / BI / NT / SB**, no numéricamente. La aplicación calcula
siempre en escala 1-10. Hoy el catálogo no incluye ámbitos, así que no se ha materializado; el día
que se añadan, las actas saldrán mal.

## R-2 · No hay módulos pendientes de cursos anteriores

**Categoría:** Riesgo potencial · **Gravedad: Alta si se materializa**

Los arts. 18 y 19 regulan la promoción con módulos pendientes y su evaluación en el curso
siguiente. El modelo de datos ata el alumnado a un módulo de un año concreto (`modulos.anno`), sin
concepto de matrícula ni de arrastre. Un alumno con el módulo pendiente hay que darlo de alta como
si fuera nuevo, perdiendo su historial.

## R-3 · No hay control de convocatorias consumidas

**Categoría:** Riesgo potencial · **Gravedad: Media**

Art. 8.2: máximo **cuatro convocatorias ordinarias** en grado D y **dos** en grado E; art. 9,
extraordinarias; art. 11, renuncia que no consume convocatoria. La aplicación no cuenta
convocatorias. Para un cuaderno de aula es asumible —lo lleva la secretaría del centro— pero
conviene decirlo en la documentación para que nadie lo dé por hecho.

## R-4 · Datos personales de alumnado enviados a un proveedor de IA

**Categoría:** Riesgo potencial · **Gravedad: Alta**

La aplicación pide consentimiento y ofrece anonimizar por número de lista, que es lo correcto. Pero:
las fotos de exámenes manuscritos **contienen el nombre escrito por el alumno**, y se envían
completas al proveedor. La anonimización del identificador no anonimiza la imagen.
**Solución:** avisarlo expresamente en la pantalla de corrección y recomendar tapar la cabecera, o
recortarla automáticamente.

## R-5 · Cobertura de pruebas asimétrica

**Categoría:** Mejora recomendada · **Gravedad: Media**

Hay tests unitarios del motor de Evaluaciones y de las claves RA|CE, pero **ninguno** del Dashboard,
del boletín ni de la columna Media de Notas — que son justo los tres motores divergentes de C-1. Lo
que no se prueba, se rompe.

---

# 5. Coherencia funcional: resumen de contradicciones

| # | Concepto | Implementación A | Implementación B | Coinciden |
|---|---|---|---|---|
| 1 | Nota final del alumno | Evaluaciones, ponderada por RA | Dashboard, media simple | **No** |
| 2 | Nota final del alumno | Evaluaciones | Boletín PDF, media de evaluaciones | **No** |
| 3 | Nota de un RA | Por criterios (Evaluaciones) | Por actividades (Dashboard, boletín) | Solo si cada actividad cubre todos los criterios del RA |
| 4 | Nota de 2ª convocatoria | Ponderada (Evaluaciones) | Media simple (Dashboard) | **No** |
| 5 | Número de lista | `max+1` (alta manual) | `length+1` (importación) | **No** |
| 6 | Recuperación | Por actividad (`nota_rec`) | Por criterio (`rec2notas`) | Ámbitos distintos, mismo nombre |

---

# 6. Experiencia de usuario

- **B-1 · «Perdonar» un criterio** es un clic sin confirmación que sube un criterio a 5. Es la acción
  más delicada de la aplicación y la más fácil de pulsar sin querer. Debería pedir motivo.
- **B-2 · «Aplicar a todo el módulo»** (ponderación prácticas/exámenes) reescribe los pesos de
  **todas** las actividades de todas las evaluaciones sin confirmación ni deshacer.
- **B-3 · Cambiar el número de evaluaciones** con el curso empezado redistribuye unidades,
  RA y actividades por índice, sin previsualización de lo que va a pasar.
- **B-4 · Dos botones «Boletín»** —en Dashboard y en Evaluaciones— generan el mismo documento con
  una nota que no coincide con la de la pantalla desde la que se pulsa (consecuencia de C-1).
- **B-5 · La media de la parrilla de Notas** no dice de qué es media; con el selector en «Todas» es
  una media simple de actividades que no significa nada evaluable.

---

# 7. Plan de corrección propuesto

**Fase 1 — antes de volver a usarla para calificar (crítico)**

1. C-1: motor único de calificación y las cuatro pantallas consumiéndolo.
2. C-5: cuadrar la 2ª convocatoria con la 1ª — mismo conjunto de criterios, mismo mínimo de examen,
   criterios sin instrumento visibles y no perdonables.
3. C-3: decidir qué se hace con `nota_max` (normalizar o eliminar).
4. C-4: el alumnado de baja deja de recibir acta.
5. C-2: `rec2notas` y `pardones` a tablas, y boletín e informes leyendo la convocatoria.

**Fase 2 — coherencia normativa**

5. A-1: estado «superado parcial» y fase de empresa.
6. A-2: congelar el RA superado.
7. A-3: ponderación por criterio.
8. A-4: faltas y RA llave con interfaz, o retirar las reglas.

**Fase 3 — integridad y experiencia**

9. A-5, A-6, A-7, A-8 y los menores M-1 a M-8.
10. Tests del motor único que comparen las cuatro salidas (R-5).

---

# 8. Lo que está bien resuelto

Para que el informe sea útil hay que decir también dónde el diseño aguanta una inspección:

- **La regla de oro está bien implementada y bien fundamentada.** Exigir todos los RA ≥ 5 es
  exactamente el art. 2.3 de la Orden 201/2024, y la aplicación no deja que la media compense un RA
  suspenso.
- **El tope de 4 en módulos no superados** (`_actaEntera`) cumple el art. 25.5.
- **La calificación de acta es entera**, como exige el art. 25.4.
- **Los criterios de evaluación son literales del DOCM** en los 87 módulos con decreto autonómico,
  verificados uno a uno. Es el punto más sólido del proyecto.
- **La reponderación sobre los RA evaluados** evita que un RA aún no trabajado cuente como cero.
- **El bloqueo de los RA superados en 2ª convocatoria** cumple el art. 4.3.f (aunque no se aplique
  en la 1ª, ver A-2).
- **Las copias de seguridad automáticas** con limpieza a 30 días.
- **La IA no pone notas**: propone y el profesorado decide, con consentimiento y anonimización.

---

*Auditoría realizada sobre el código del repositorio, el esquema real de la base de datos ejecutado
en SQLite y los motores de cálculo ejecutados con datos de prueba. Las citas normativas proceden del
texto publicado en el DOCM.*

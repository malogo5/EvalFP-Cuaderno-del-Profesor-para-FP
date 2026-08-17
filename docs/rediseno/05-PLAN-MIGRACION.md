# Plan de migración — RF-02 (programación normalizada) y RF-08 (recuperación como actividad)

> Documento de planificación. No se ha escrito ni modificado código para producirlo.
> Se apoya en `00-CONTEXTO.md`, `01-PROMPT-MAESTRO.md`, `04-REDISENO-PANTALLAS.md` y en la
> inspección en solo lectura de una copia real de `evalfp.db`
> (`~/evalfp-datos-prueba/evalfp.db`, copiada a un directorio de trabajo y abierta con
> `sqlite3 -readonly "file:...?immutable=1"` para no requerir ni un byte de escritura sobre
> ella, ni siquiera los ficheros `-wal`/`-shm` que SQLite intenta crear en modo `-readonly`
> normal). El original no se ha tocado.

---

## 0. Qué había de verdad en la base inspeccionada

Antes de diseñar nada, esto es lo que contiene la copia de prueba — un solo módulo, así que
las cifras son pequeñas, pero sirven para fijar la forma real de los datos, no una hipotética:

| Tabla / dato | Cantidad real |
|---|---|
| `modulos` | 1 (ISO, `iso_data`, grupo por defecto, curso 2026-2027) |
| `alumnos` | 1 |
| `actividades` | 19 (17 de convocatoria 1 normales + 2 exámenes multi-UT) |
| `notas` | 1 fila, `nota_rec` **siempre NULL** |
| `calificaciones_ce`, `ra_ponderaciones`, `ra_estado`, `ra_superados` | 0 filas cada una |
| `data_json.ras` | 8 RA (RA1–RA8), con `pond`, y `dual`/`llave` solo en algunos |
| `data_json.ces` | 8 claves (una por RA), 79 CE en total, **ninguno con `peso`** |
| `data_json.uts` | 8 UT |
| `data_json.asignaciones` | 12 objetos `{ut,ra,ces:[...]}`, 79 CE referenciados en total |
| `data_json.ra_instrumentos` | 8 claves, 201 pares RA×instrumento al expandir por CE |
| `actividades.ces` (tabla viva) | 158 claves `RA|CE` en total, ya en formato compuesto |

Hallazgos que cambian el diseño:

1. **`data_json.actividades` es una fotografía muerta.** Es el mismo array que se pasó a
   `addModulo()` al crear el módulo (comprobado campo a campo: coincide con las 19 filas de la
   tabla `actividades` en el mismo orden). Ninguna pantalla lo vuelve a escribir tras la
   creación — `_saveModData` reserializa el mismo objeto sin tocar esa clave, y las pantallas
   leen actividades de la tabla SQL, con `data.actividades` solo como *fallback* si la llamada
   IPC fallara. **No se migra**: la tabla `actividades` ya es la única fuente viva.
2. **`ra_id` es `NULL` de verdad**, no cadena vacía, en las actividades multi-UT
   (`ut_id = "UT1,UT2,UT3"`, dos casos reales: ids 13 y 15). El diseño de abajo no depende de
   `ra_id` para resolver criterios de estas actividades — usa `actividades.ces`, que ya trae la
   clave `RA|CE` completa.
3. **Ningún CE tiene `peso` explícito** en este módulo real. El reparto es automático hoy y lo
   sigue siendo tras la migración (columna `NULL`, no `0`).
4. **`eval_ras` es una caché derivable**, no un dato nuevo: `renderer/js/utils/ce-keys.js` ya
   calcula lo mismo en `rasPorEvaluacion(data, evalCount)` a partir de `uts[].eval` y
   `asignaciones`. Coincide además con la decisión de `04-REDISENO-PANTALLAS.md` §1.3: la
   temporalización se declara en la UT y el RA la hereda, nunca al revés. **No se migra a
   ninguna tabla**: se sigue derivando en consulta.
5. **`ra_ponderaciones` es un *override* sobre el `pond` del JSON**, no una tabla
   independiente — las pantallas hacen `raPondOverrides[ra.id] ?? ra.pond`. El valor a migrar a
   la nueva columna es ese **valor efectivo ya fusionado**, no el del JSON a secas.

---

## 1. Tablas nuevas (RF-02) y sus claves foráneas

Nomenclatura: minúsculas, español, igual que el resto del esquema
(`ra_ponderaciones`, `ra_estado`, `calificaciones_ce`…). Todas cuelgan de `modulo_id` con
`ON DELETE CASCADE`, igual que `alumnos` o `actividades` hoy.

```sql
-- Catálogo de RA del módulo. Sustituye a data_json.ras[] como fuente viva.
-- `pond` es el valor EFECTIVO (fusión de data_json.ras[].pond y el override que
-- hoy vive en ra_ponderaciones — ver §2.1).
CREATE TABLE ra_catalogo (
  modulo_id INTEGER NOT NULL,
  ra_id     TEXT    NOT NULL,
  nombre    TEXT    NOT NULL,
  pond      REAL    NOT NULL DEFAULT 0,
  llave     INTEGER NOT NULL DEFAULT 0,   -- necesario para la fase de empresa (art. 4.3.a)
  dual_pct  REAL,                          -- % del RA que se acredita en empresa; NULL = nada
  PRIMARY KEY (modulo_id, ra_id),
  FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
);

-- Catálogo de CE del módulo. Sustituye a data_json.ces{RA: [...]}.
-- `peso` NULL = reparto automático entre los CE del mismo RA (decisión de
-- 04-REDISENO-PANTALLAS.md §1.1: una casilla en blanco no es un dato que falta).
CREATE TABLE ce_catalogo (
  modulo_id INTEGER NOT NULL,
  ra_id     TEXT    NOT NULL,
  ce_id     TEXT    NOT NULL,
  texto     TEXT    NOT NULL,
  peso      REAL,
  PRIMARY KEY (modulo_id, ra_id, ce_id),
  FOREIGN KEY (modulo_id, ra_id) REFERENCES ra_catalogo(modulo_id, ra_id) ON DELETE CASCADE
);

-- Unidades de trabajo. Sustituye a data_json.uts[].
CREATE TABLE unidades_trabajo (
  modulo_id     INTEGER NOT NULL,
  ut_id         TEXT    NOT NULL,
  nombre        TEXT    NOT NULL,
  horas         INTEGER DEFAULT 0,
  horas_empresa INTEGER DEFAULT 0,
  eval          INTEGER NOT NULL DEFAULT 1,
  tags          TEXT,
  PRIMARY KEY (modulo_id, ut_id),
  FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
);

-- Asignación UT→CE. Sustituye a data_json.asignaciones[{ut,ra,ces:[...]}], EXPLOTADO
-- a una fila por CE (RF-02: "no podrá existir asignación UT–RA independiente que
-- contradiga la relación UT–CE"; el RA de una UT se DERIVA agrupando estas filas).
CREATE TABLE ut_ce (
  modulo_id INTEGER NOT NULL,
  ut_id     TEXT    NOT NULL,
  ra_id     TEXT    NOT NULL,
  ce_id     TEXT    NOT NULL,
  PRIMARY KEY (modulo_id, ut_id, ra_id, ce_id),
  FOREIGN KEY (modulo_id, ut_id) REFERENCES unidades_trabajo(modulo_id, ut_id) ON DELETE CASCADE,
  FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
);

-- Instrumento previsto, resuelto A NIVEL DE CE (art. 4.3.b) aunque hoy se declare
-- por RA en la interfaz. Sustituye a data_json.ra_instrumentos{RA: [...]}, expandido
-- a cada CE de ese RA. Un CE puede tener varios instrumentos (varias filas).
CREATE TABLE ce_instrumentos_previstos (
  modulo_id   INTEGER NOT NULL,
  ra_id       TEXT    NOT NULL,
  ce_id       TEXT    NOT NULL,
  instrumento TEXT    NOT NULL,
  PRIMARY KEY (modulo_id, ra_id, ce_id, instrumento),
  FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
);

-- Relación actividad→CE. Sustituye a la columna actividades.ces (JSON de claves
-- "RA|CE"). modulo_id va redundante (ya está en actividades) solo para poder
-- referenciar la clave compuesta de ce_catalogo sin un JOIN previo.
CREATE TABLE actividad_ce (
  actividad_id INTEGER NOT NULL,
  modulo_id    INTEGER NOT NULL,
  ra_id        TEXT    NOT NULL,
  ce_id        TEXT    NOT NULL,
  PRIMARY KEY (actividad_id, ra_id, ce_id),
  FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE,
  FOREIGN KEY (modulo_id, ra_id, ce_id) REFERENCES ce_catalogo(modulo_id, ra_id, ce_id)
);
```

**No se toca el esquema de `ra_ponderaciones`, `ra_estado` ni `ra_superados`.** Podrían ganar
una FK compuesta a `ra_catalogo(modulo_id, ra_id)` por higiene, pero eso exige recrearlas (SQLite
no añade FK con `ALTER TABLE`) para un beneficio puramente de integridad, sobre tablas que ya
están en producción y probadas por RF-01. Se deja fuera de este plan; si se hace, en un paso
aparte y con sus propios tests.

**`ra_ponderaciones` queda obsoleta pero no se borra en esta migración.** Su valor ya se fusiona
dentro de `ra_catalogo.pond` (§2.1). Borrar la tabla es una decisión de código (el renderer
tiene que dejar de llamar a `getRaPonderaciones`/`setRaPonderacion` y leer/escribir
`ra_catalogo.pond`), no de datos — se deja para cuando esa parte de RF-02 esté implementada.

---

## 2. Transformación de `modulos.data_json` → tablas nuevas

Para cada fila de `modulos`, con `data = JSON.parse(data_json)`:

### 2.1 `ra_catalogo`

```
overrides = SELECT ra_id, pond FROM ra_ponderaciones WHERE modulo_id = ?   -- mapa ra_id→pond

para cada ra en data.ras:
  pond_efectivo = overrides[ra.id] ?? ra.pond ?? 0
  INSERT INTO ra_catalogo (modulo_id, ra_id, nombre, pond, llave, dual_pct)
  VALUES (modulo_id, ra.id, ra.nombre, pond_efectivo, ra.llave ? 1 : 0, ra.dual ?? NULL)
```

Validación: `ra.id` y `ra.nombre` no vacíos (si faltan, se cuenta como fallo del módulo y se
avisa — no se inventa un nombre).

### 2.2 `ce_catalogo`

```
para cada ra_id en data.ces:
  si ra_id no está en data.ras → CONTAR como "RA huérfano en ces", NO insertar sus CE
     (mismo defecto que ya vigila tests/unit/catalogo.test.js sobre el catálogo estático)
  para cada ce en data.ces[ra_id]:
    INSERT INTO ce_catalogo (modulo_id, ra_id, ce_id, texto, peso)
    VALUES (modulo_id, ra_id, ce.id, ce.texto, ce.peso ?? NULL)
```

### 2.3 `unidades_trabajo`

```
para cada ut en data.uts:
  INSERT INTO unidades_trabajo (modulo_id, ut_id, nombre, horas, horas_empresa, eval, tags)
  VALUES (modulo_id, ut.id, ut.nombre, ut.horas ?? 0, ut.horas_empresa ?? 0,
          ut.eval ?? 1, ut.tags ?? NULL)
```

### 2.4 `ut_ce` (explota `asignaciones`)

```
para cada asignación {ut, ra, ces} en data.asignaciones:
  si ut no está en data.uts → CONTAR "asignación con UT huérfana", saltar
  si ra no está en data.ras → CONTAR "asignación con RA huérfano", saltar
  para cada ce_id en asignación.ces:
    si ce_id no está en data.ces[ra] → CONTAR "asignación con CE huérfano", saltar ese CE
    INSERT OR IGNORE INTO ut_ce (modulo_id, ut_id, ra_id, ce_id)
    VALUES (modulo_id, ut, ra, ce_id)
```

`INSERT OR IGNORE` porque el mismo `(ut,ra)` puede aparecer más de una vez en `asignaciones` en
otros módulos del catálogo aunque no ocurra en el inspeccionado (dos entradas para el mismo par
que amplíen la lista de CE) — la tabla normalizada los fusiona sin más.

Este es el paso que hace cumplir la regla de RF-02 "no puede existir asignación UT–RA que
contradiga UT–CE": como `ut_ce` no tiene fila si no hay al menos un CE, un RA sin ningún CE
asignado a una UT sencillamente no aparece ligado a ella — no hace falta una regla aparte.

### 2.5 `ce_instrumentos_previstos` (expande `ra_instrumentos` a nivel de CE)

```
para cada ra_id en data.ra_instrumentos:
  si ra_id no está en data.ras → CONTAR, saltar
  para cada ce en data.ces[ra_id] ?? []:
    para cada instrumento en data.ra_instrumentos[ra_id]:
      INSERT OR IGNORE INTO ce_instrumentos_previstos (modulo_id, ra_id, ce_id, instrumento)
      VALUES (modulo_id, ra_id, ce.id, instrumento)
```

Esto es pura herencia mecánica (lo que hoy ya asume la interfaz): todo CE de un RA hereda todos
los instrumentos declarados para ese RA. La excepción puntual por CE que describe RF-02 no
existe todavía en ningún módulo real — no hay nada que migrar para ella, se implementa como
funcionalidad nueva sobre esta misma tabla.

### 2.6 `actividad_ce` (desde la tabla viva `actividades`, no desde `data_json`)

Fuente: la columna `actividades.ces`, que **ya está en formato `"RA|CE"`** gracias a la
migración existente `_migrarCesDeActividades` (corre en cada arranque, así que para cuando este
paso se ejecute ya no debería quedar ninguna clave suelta sin `|`; aun así se comprueba).

```
para cada actividad en SELECT id, modulo_id, ces FROM actividades:
  lista = JSON.parse(actividad.ces ?? '[]')
  para cada clave en lista:
    si clave no contiene '|' → CONTAR "clave sin migrar todavía", saltar (no debería pasar
        si este paso corre después de _migrarCesDeActividades, pero no se asume)
    [ra_id, ce_id] = clave.split('|', 2)
    si (modulo_id, ra_id, ce_id) no existe en ce_catalogo → CONTAR "actividad con CE que ya
        no está en el catálogo" (pasa si se borró un CE de la programación después de crear
        la actividad — comportamiento ya conocido y avisado por _saveModData con sus
        "huérfanas"), saltar
    INSERT OR IGNORE INTO actividad_ce (actividad_id, modulo_id, ra_id, ce_id)
    VALUES (actividad.id, modulo_id, ra_id, ce_id)
```

Con los datos reales: 158 claves de entrada, y las 158 deberían insertarse limpias porque el
catálogo (79 CE) las cubre todas — se comprueba, no se asume.

### 2.7 Qué NO se toca en este paso

- `modulos.data_json` **se conserva intacto**, no se limpia ni se reescribe. No aporta nada
  borrarlo (el ahorro de espacio es insignificante) y sirve de rastro histórico de cómo estaba
  la programación antes de normalizar, gratis. El código deja de leerlo — eso es un cambio de
  las pantallas, no de esta migración de datos.
- Los metadatos de `data.modulo` (`codigo`, `ciclo_clave`, `ciclo_nivel`, `horas_sem`,
  `total_horas`, `eval_count`, `decreto`…) no se tocan aquí. Varios ya son columnas de `modulos`
  (`abrev`, `nombre`, `ciclo`, `curso`, `anno`, `horas`, `decreto`); los que no lo son
  (`eval_count`, `total_horas`, `horas_sem`, `ciclo_clave`, `ciclo_nivel`) se siguen leyendo del
  JSON como hasta ahora. Normalizarlos también es una ampliación razonable pero no la pide RF-02
  explícitamente (que habla de UT/CE/RA/asignaciones/instrumentos) y no tiene relación con
  `nota_rec`; se deja fuera para no ensanchar el riesgo de esta migración concreta.

---

## 3. RF-08 — `notas.nota_rec` → actividad de recuperación

### 3.1 Qué es hoy `nota_rec`, con precisión

No es lo mismo que la 2ª convocatoria. El propio código lo avisa
(`renderer/js/modules/notas.js:5-9`): `nota_rec` es "recuperar una ACTIVIDAD dentro de la
evaluación continua" — un segundo intento de la MISMA actividad, para el MISMO alumno, dentro de
la 1ª convocatoria. La recuperación por criterio de la 2ª Ordinaria (`calificaciones_ce`,
convocatoria 2) es un camino completamente distinto que **no se toca** en este punto.

En la base inspeccionada no hay ningún caso real (`notas_con_rec = 0`): el algoritmo de abajo no
se ha podido ejercitar contra un caso de verdad y **debe probarse con datos sintéticos antes de
confiar en él** frente a cualquier base que sí tenga `nota_rec` con valores.

### 3.2 Columnas nuevas en `actividades`

```sql
ALTER TABLE actividades ADD COLUMN es_recuperacion INTEGER NOT NULL DEFAULT 0;
ALTER TABLE actividades ADD COLUMN recupera_actividad_id INTEGER
  REFERENCES actividades(id) ON DELETE SET NULL;
```

(SQLite no permite añadir una FK con `ALTER TABLE ... ADD COLUMN` con la misma solidez que una
declarada en la creación de la tabla — la referencia se declara igualmente por claridad, pero
`node:sqlite` no la hará cumplir retroactivamente sin recrear la tabla. Se anota como limitación
conocida, no bloquea la migración: el valor seguirá siendo correcto, solo no está forzado a nivel
de motor si alguien lo corrompe a mano.)

### 3.3 Algoritmo

```
actividades_con_rec = SELECT DISTINCT actividad_id FROM notas WHERE nota_rec IS NOT NULL

para cada actividad_id en actividades_con_rec:
  original = SELECT * FROM actividades WHERE id = actividad_id
  si original no existe (huérfana) → CONTAR, saltar (la nota_rec queda sin poder migrarse:
      ver §4, es una pérdida real, no un caso a inventar)

  nueva_id = INSERT INTO actividades
    (modulo_id, ut_id, ra_id, descripcion, instrumento, tipo, peso, nota_max, eval,
     orden, convocatoria, ces, prueba_objetiva, es_recuperacion, recupera_actividad_id)
    VALUES (
      original.modulo_id, original.ut_id, original.ra_id,
      'Recuperación — ' || original.descripcion,
      NULL,                          -- instrumento: origen desconocido (RF-08 lo exige así)
      original.tipo,
      0,                             -- peso 0: ver razón más abajo, es la clave de seguridad
      original.nota_max,
      original.eval, original.orden,
      original.convocatoria,          -- misma convocatoria que el original (nunca fue la 2ª
                                       -- Ordinaria: ver §3.1)
      original.ces,                   -- recupera los MISMOS CE que la actividad original
      original.prueba_objetiva,
      1,                               -- es_recuperacion
      original.id                     -- recupera_actividad_id
    )

  para cada (alumno_id, nota_rec) en SELECT alumno_id, nota_rec FROM notas
                                     WHERE actividad_id = actividad_id AND nota_rec IS NOT NULL:
    INSERT INTO notas (alumno_id, actividad_id, nota, fecha, observaciones)
    VALUES (alumno_id, nueva_id, nota_rec, NULL,
            'Migrado de notas.nota_rec el <fecha de la migración>')
```

### 3.4 Por qué `peso = 0`

Esta es la decisión más delicada del plan, y hay que decirla en voz alta: **el motor
(`renderer/js/core/calificacion.js`) no sabe todavía qué hacer con `es_recuperacion`.** RF-08
quiere que la nota de recuperación compita por CE con la original y se quede con la mejor
(`00-CONTEXTO.md`, decisión 6), no que sume como una actividad más. Mientras el motor no
implemente esa regla, cualquier actividad nueva con peso > 0 SÍ entraría en el promedio ponderado
de hoy y cambiaría notas ya cerradas — exactamente lo que el art. 4.3.f prohíbe y lo que
`ra_superados`/RF-01 existen para evitar.

Poniendo `peso = 0`, la actividad de recuperación queda **registrada, con su nota, trazable y
enlazada** a la original, pero invisible para el cálculo actual (`pesosPorTipo`/`notaCE`/
`notaRA` ignoran una actividad de peso 0). El día que el motor aprenda a leer
`es_recuperacion`/`recupera_actividad_id` para aplicar "la mejor nota por CE", dejará de mirar
`peso` para esa actividad de todas formas.

**Esta migración de datos no debe ejecutarse en una base con `nota_rec` reales sin que antes (o
en el mismo cambio) el motor sepa ignorar `peso=0` por diseño explícito y sin que exista al menos
un test que compruebe que una actividad `es_recuperacion=1` no mueve la nota de nadie hasta que
se implemente su regla.** Es una dependencia dura con el motor, no con `calificacion.js` en el
sentido de tocarlo hoy — es una condición de entrada para ejecutar §3 en producción.

---

## 4. Qué no se puede migrar sin pérdida

Dicho en claro, sin inventar un sustituto:

1. **Qué CE concretos se acreditan en la fase de empresa dentro de un RA dualizado.**
   `scripts/prebake_modules.py` calcula el `dual` (%) de cada RA a partir de una lista de CE
   concretos (`DUAL_CES = {"RA8": ["CR1", ...]}` en los módulos estáticos de Python), pero **esa
   lista no se guarda en ningún sitio de `modulos.data_json`** — solo sobrevive el porcentaje
   agregado por RA (`ras[].dual`), ya persistido y que sí migra a `ra_catalogo.dual_pct`. La
   granularidad de CE se pierde en el momento en que se crea el módulo desde el catálogo, no en
   esta migración: no hay ninguna fuente en la base de datos de la que recuperarla. Si se
   necesita, hay que volver a declararla a mano por CE (candidato natural: una columna en
   `ce_catalogo`, p.ej. `en_empresa INTEGER`), no reconstruirla.
2. **El instrumento real con el que se hizo cada recuperación histórica de `nota_rec`.** Nunca
   se guardó — solo la nota. Por eso §3.3 lo deja `NULL` y la descripción dice "origen
   desconocido"; no se puede inventar un instrumento que nadie registró.
3. **La fecha exacta de cada recuperación histórica.** Mismo motivo: `notas.fecha` es la fecha de
   la nota ORIGINAL (columna única, la actualiza tanto `saveNota` como `saveNotaRec`), no hay
   una fecha independiente para el intento de recuperación. Queda `NULL`.
4. **Una actividad de `nota_rec` huérfana** (su `actividad_id` ya no existe en `actividades`,
   p. ej. porque se borró la actividad y `ON DELETE CASCADE` se llevó por delante sus filas de
   `notas`, `nota_rec` incluido). Este caso en concreto no puede ocurrir de verdad — si la
   actividad no existe, tampoco existe ya la fila de `notas` que la referenciaba, así que no hay
   nada que migrar ni que perder. Se deja documentado en el algoritmo (§3.3) como guarda
   defensiva, no como pérdida real.

Nada de la parte de RF-02 (§2) implica pérdida: cada tabla nueva es una proyección exacta de un
campo que ya existe en `data_json` o en `actividades.ces`, sin ningún dato que no tenga a dónde
ir. Las únicas bajas son las **inconsistencias** que ya existieran en el JSON de origen
(asignaciones o instrumentos apuntando a un RA/CE que ya no está en el catálogo) — esas no se
"pierden" al migrar, se quedan fuera exactamente porque ya no significan nada hoy tampoco: la
interfaz actual tampoco las muestra.

---

## 5. Orden de ejecución

1. **Copia de seguridad del `.sqlite` fuera del repositorio**, antes de tocar nada — ya está
   anotado como tarea pendiente en `00-CONTEXTO.md` y aquí se convierte en el primer paso
   obligatorio, no en una sugerencia. Verificar que la copia abre y que
   `PRAGMA integrity_check` devuelve `ok` sobre ella, en solo lectura, antes de continuar.
2. **Esquema aditivo** (fuera de transacción explícita, igual que hoy hacen las migraciones de
   columnas en `getDb()`): `CREATE TABLE IF NOT EXISTS` de las seis tablas de §1, y
   `ALTER TABLE actividades ADD COLUMN` de `es_recuperacion`/`recupera_actividad_id` de §3.2,
   cada uno guardado tras comprobar con `PRAGMA table_info`/`sqlite_master` que no existe ya —
   el mismo patrón que sigue el resto de `db.js`. No modifica ni una fila existente.
3. **Transformación RF-02 (§2), en una única transacción** que cubre los seis pasos (2.1 a 2.6)
   para TODOS los módulos de la base. Un único `BEGIN`/`COMMIT`, no uno por módulo: con la
   escala real de esta app (un profesor, un fichero, un puñado de módulos — `AGENTS.md`,
   ADR-001/002) el coste de repetir todo si algo falla es bajo, y mantiene el mismo estilo que
   `_migrarCesDeActividades`/`_migrarCalificacionesCE`, que ya hacen exactamente esto. Dentro de
   la transacción, un módulo con `data_json` ilegible o sin `ras`/`ces` se salta con un
   `try/catch` alrededor de su `JSON.parse` y se cuenta — eso NO aborta la transacción, solo la
   sentencia SQL que fallase de verdad la abortaría.
4. **Verificación antes de confirmar (dentro de la misma transacción del paso 3):**
   - `PRAGMA foreign_key_check` sin filas.
   - Recuento cruzado: nº de filas insertadas en `ut_ce` == nº de pares (asignación, CE) que
     pasaron la validación (no los huérfanos descartados); mismo contraste para
     `ce_instrumentos_previstos` y `actividad_ce`.
   - Ningún RA de `ra_catalogo` con `pond` fuera de 0–100; si los `pond` de un módulo no suman
     100, **no bloquea** (ya pasa hoy, el badge de Programación solo avisa) pero se deja constancia
     en el log de migración.
   - Si cualquiera de estas comprobaciones falla: `ROLLBACK` completo del paso 3 y la migración
     se detiene ahí — no se sigue con el paso 5.
5. **Transformación RF-08 (§3), en su propia transacción, aparte de la del paso 3.** No depende
   de las tablas nuevas de RF-02 (solo de `actividades`/`notas` y de las dos columnas del paso 2),
   así que puede posponerse o repetirse independientemente si el paso 3 tuviera que
   reejecutarse. **No se ejecuta contra una base con `nota_rec` reales hasta que se cumpla la
   condición de §3.4** (el motor ignora con seguridad `peso=0` en actividades de recuperación, y
   hay un test que lo demuestra).
   - Verificación antes de confirmar: nº de `(alumno_id, actividad_id)` con `nota_rec IS NOT
     NULL` al empezar == nº de filas nuevas en `notas` con `observaciones LIKE 'Migrado de
     notas.nota_rec%'`. Si no cuadra, `ROLLBACK`.
6. **Punto de no retorno, aparte, solo si 3, 4 y 5 terminaron limpios:** eliminar la columna
   `notas.nota_rec`. Comprobar primero la versión de SQLite que sirve `node:sqlite` en el
   Electron empaquetado: si soporta `ALTER TABLE notas DROP COLUMN nota_rec` (SQLite ≥ 3.35), se
   usa directo; si no, se recrea la tabla `notas` con el procedimiento ya establecido en
   `_migrarUnicidadModulos` (claves foráneas apagadas, `BEGIN`, `CREATE`+`INSERT SELECT`+`DROP`+
   `RENAME`, `PRAGMA foreign_key_check`, `COMMIT`). Este paso se deja como **acción manual
   explícita y separada**, no automática al arrancar la app: borrar una columna no se deshace
   sin la copia del paso 1, así que no debe disparase sola la primera vez que alguien abra la
   versión nueva.
7. **Verificación final, de lectura, sin escritura:** recorrer un módulo de verdad en la
   interfaz (Programación, Notas, Evaluaciones) y comprobar que las cifras que dependían de
   `data_json` (RA, CE, UT, asignaciones, instrumentos previstos) coinciden con las que devuelven
   las tablas nuevas, antes de dar la migración por buena para ese fichero.

---

## 6. Qué puede fallar, con causa concreta, y cómo se revierte

| Puede fallar | Causa real observable | Cómo se revierte |
|---|---|---|
| `JSON.parse(data_json)` lanza | Módulo con JSON corrupto (no se ha visto en la base inspeccionada, pero `data_json` es un `TEXT` sin validación de esquema en `modulos`) | Se captura por módulo, se cuenta, no aborta el resto de la transacción del paso 3 |
| Asignación con CE que ya no está en el catálogo | Se borró un CE del módulo después de que quedara referenciado en `asignaciones` (mismo defecto que ya vigila `tests/unit/catalogo.test.js` sobre el catálogo estático) | Se descarta esa fila de `ut_ce`, se cuenta, no aborta |
| `ra_instrumentos` con un RA que ya no está en `ras` | Programación editada a mano entre versiones | Se descarta, se cuenta, no aborta |
| `PRAGMA foreign_key_check` devuelve filas al final del paso 3 | Alguna de las validaciones anteriores tiene un hueco no previsto | `ROLLBACK` de toda la transacción del paso 3; la base queda exactamente como estaba, sin ninguna tabla nueva poblada (siguen existiendo, vacías, por el `CREATE TABLE IF NOT EXISTS` del paso 2, que es inocuo) |
| `notas.nota_rec` con `actividad_id` que ya no existe | Solo posible si la fila de `notas` sobrevivió al `ON DELETE CASCADE` de su actividad, lo que no debería pasar nunca con las FK activas — se trata como bug a investigar, no como caso normal, y bloquea el paso 5 hasta explicarlo | `ROLLBACK` del paso 5; no toca el paso 3 |
| El recuento de `notas` migradas no cuadra en el paso 5 | Alguna fila con `nota_rec` fuera de rango 0–10 que el `INSERT` rechazara (la base ya avisa hoy de notas fuera de escala en `getDb()`, línea ~121) | `ROLLBACK` del paso 5; se corrige el dato de origen y se reintenta |
| El fichero `.sqlite` se corrompe a media migración (corte de luz, fallo de disco) | WAL + `journal_mode=WAL` ya protege bastante, pero no es infalible | Restaurar la copia del paso 1; es la única red de seguridad real, por eso es el paso 0 y no una nota a pie de página |
| Paso 6 (`DROP COLUMN`) ejecutado antes de tiempo, con `nota_rec` sin migrar del todo | Error humano: saltarse la verificación del paso 5 | No hay marcha atrás dentro de la base — se restaura la copia del paso 1 y se repite desde el paso 3. Por eso el paso 6 está separado y descrito como manual, no como parte del arranque automático |

---

## 7. Contrato de `scripts/export_modulo_json.py` para `_ModFromJson`

Hallazgo verificado leyendo ambos ficheros: **hoy el contrato ya está roto**, aunque nadie lo
haya notado porque ninguna ruta de código llama a `export_modulo_json.py` seguido de
`build_apuntes.py --datos <json>` — `_ModFromJson`/`_cargar_desde_json` existen en
`scripts/build_apuntes.py` pero no los invoca ni `ia.js` ni `main.js` todavía.

- `_ModFromJson.__init__` (líneas 46-61 de `build_apuntes.py`) lee `nombre`, `abrev`, `ciclo`,
  `curso`, `anno` **en el nivel superior** del dict: `data.get('nombre', ...)`, etc.
- `export_modulo_json.py` (líneas 43-51) genera esos mismos campos **anidados bajo la clave
  `"modulo"`**: `{"modulo": {"nombre": ..., "abrev": ...}, "ras": [...], ...}`.

Con el JSON que produce hoy `export_modulo_json.py`, `_ModFromJson.MODULO` saldría con
`{'nombre': '?', 'abrev': '?', 'ciclo': 'FP', 'curso': '', 'anno': '2026-2027'}` — ninguno de los
campos reales llegaría. `uts`, `ras`, `ces`, `asignaciones` sí coinciden porque esos van sueltos
en el nivel superior en ambos sitios.

**Contrato que debe cumplir la reescritura de `export_modulo_json.py` tras RF-02** (cuando pase a
leer de `ra_catalogo`/`ce_catalogo`/`unidades_trabajo`/`ut_ce` en vez de
`scripts/modules/*_data.py`):

```json
{
  "nombre": "...", "abrev": "...", "ciclo": "...", "curso": "...", "anno": "...",
  "uts":  [ {"id": "UT1", "nombre": "...", "horas": 30, "eval": 1, "tags": ""}, ... ],
  "ras":  [ {"id": "RA1", "nombre": "...", "pond": 13}, ... ],
  "ces":  { "RA1": [ {"id": "CR1", "texto": "..."}, ... ], ... },
  "asignaciones": [ {"ut": "UT1", "ra": "RA1", "ces": ["CR1", "CR2"]}, ... ]
}
```

Es decir: **quitar el anidado bajo `"modulo"`** y dejar esos cinco campos sueltos, o alternativamente
cambiar `_ModFromJson` para que lea `data.get('modulo', data)`. Cualquiera de las dos cierra el
contrato; la primera es la fiel al docstring de `_ModFromJson` ("exportado desde SQLite por
Electron") y no toca `build_apuntes.py`, que RF-13 dice explícitamente que no hay que reescribir.
`ra_instrumentos` y `eval_ras` no forman parte del contrato — `_ModFromJson` no los lee, así que
no hace falta emitirlos para este consumidor (aunque sigan existiendo para el resto de la app).

El test que falta y que RF-13 pide explícitamente ("es el punto de rotura silenciosa de esta
migración"): un test que exporte un módulo con datos no triviales (con `dual`, con `llave`, con
una UT multi-RA) y compruebe que `_ModFromJson(json.loads(salida))` reconstruye `MODULO`, `UTS`,
`RAS`, `CES` y `ASIGNACIONES` con los valores esperados — no solo que el JSON sea válido.

---

## 8. Lo que este plan deja abierto

- **No decide** si `ra_ponderaciones` se borra o se deja como tabla muerta — es una decisión de
  cuándo el código dela de usarla, no de esta migración.
- **No decide** el nombre final de la columna `ce_catalogo.peso` frente a la UI de "reparto
  automático" de `04-REDISENO-PANTALLAS.md` — el nombre de columna aquí es una propuesta, no un
  contrato cerrado con el renderer todavía inexistente.
- **No incluye** normalizar `actividades.ut_id` (hoy texto, a veces con varias UT separadas por
  coma) a una tabla `actividad_ut`. RF-02 no lo pide explícitamente («asignación UT–CE» y
  «relación actividad–CE» sí; la relación propia de una actividad con sus UT, no) y añadirlo
  ensancha el riesgo sin un requisito que lo exija hoy. Se deja anotado como candidato para
  cuando haga falta.
- **No implementa** la regla de "mejor nota por CE" de RF-08 en el motor — ese es trabajo de
  `calificacion.js`, fuera del encargo de este documento y con la condición explícita del §3.4
  antes de poder ejecutar §3 contra datos reales.
- **No se ha podido validar el algoritmo de §3 (nota_rec) contra ningún caso real**, porque no
  existe ninguno en los datos inspeccionados. Antes de confiar en él hace falta un fichero de
  prueba sintético con varios `nota_rec` en distintas combinaciones (una actividad con varios
  alumnos recuperados, una actividad de convocatoria ya cerrada, un `nota_rec` en el límite 0/10)
  y comprobar el resultado a mano.

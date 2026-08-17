# Prompt maestro — Implementación auditada de EvalFP (RF-01 a RF-13)

> Documento de trabajo. Se pasa al agente de código que vaya a implementar los requisitos.

## Contexto

EvalFP es un cuaderno del profesorado en Electron con better-sqlite3 y keytar, monousuario
y local. Repositorio `malogo5/EvalFP-Cuaderno-del-Profesor-para-FP`, versión 3.16.1. Caso de
referencia: CFGS ASIR, 1.º curso, módulo ISO (código 0369), Castilla-La Mancha.

## Qué se espera de ti

Ya se ha auditado el código y las decisiones de modelo están tomadas. No repitas el
diagnóstico ni generes otro documento de auditoría: en el repositorio hay siete. Tu trabajo
es implementar los trece requisitos.

Dicho esto, si al leer el código encuentras un planteamiento mejor —en arquitectura, en
modelo de datos, en diseño funcional o en la experiencia de uso del profesorado— proponlo
antes de implementarlo: explica el problema que resuelve, qué requisitos afecta y qué riesgo
introduce, y espera confirmación. Se te pide criterio también sobre lo funcional: si una
pantalla obliga a trabajo redundante, si un flujo no encaja con cómo se programa y evalúa
realmente un módulo de FP a lo largo de un curso, o si una funcionalidad está resuelta como
herramienta suelta en vez de integrada en el modelo, dilo. Lo que no debes hacer es cambiar
de rumbo por tu cuenta ni sustituir una decisión de modelo ya tomada por otra que te parezca
más elegante. Si detectas un fallo adicional que no está en estos requisitos, señálalo con
su evidencia en el código y sigue adelante con lo tuyo.

## Objetivo

Ninguna aplicación puede blindar jurídicamente una calificación: lo que la sostiene ante una
revisión es que los criterios aplicados figuren en la programación didáctica, porque el
art. 27.4 contrasta lo aplicado con ese documento. Lo que sí debe conseguir EvalFP, y es el
criterio con el que debes decidir cualquier duda de diseño, es capacidad de justificación
suficiente ante una revisión, una reclamación o una actuación inspectora: que se pueda
demostrar qué se programó, qué se informó al alumnado, qué se evaluó, con qué instrumentos,
con qué evidencias, qué criterios se aplicaron, cómo se recuperó, cómo se calculó y qué
resultado se comunicó. Y que lo aplicado sea exactamente lo configurado, sin desviaciones
silenciosas.

## Cómo leer el origen de cada regla

Cada requisito indica su fundamento y no debes elevar una categoría a otra:

- **Normativo verificado**: exigencia de la Orden 201/2024 o del RD 659/2023, comprobada en
  fuente oficial.
- **Derivado del código**: consecuencia de un fallo localizado en el repositorio.
- **Decisión de EvalFP**: criterio profesional de la docente. No es obligación legal. Cuando
  afecte a criterios de calificación, su legitimidad descansa en que figure en la
  programación didáctica; tú la implementas, no la justificas.

## Normativa aplicable, ya verificada en fuente oficial

Orden 201/2024, de 28 de noviembre (DOCM 3-12-2024), en su redacción vigente tras la
Orden 55/2026, de 17 de abril (DOCM 27-4-2026). Real Decreto 659/2023, de 18 de julio.
Artículos utilizados: 2.2, 2.3, 2.4, 3.3, 3.6, 3.7, 4.3.a-f, 8.3, 12, 16, 18.4, 21.5, 25.1,
25.4, 25.5, 27.2, 27.3, 27.4, 27.8.2, 29.2, 29.4, 30.3, 31.2, 31.3. La Orden 55/2026
suprimió el apartado 8 del art. 25 y renumeró los siguientes.

No des por buena ninguna afirmación normativa sin comprobarla en DOCM o BOE. Si no puedes
verificar algo, escribe NO VERIFICADO. Si es interpretable, escribe INTERPRETACIÓN NO
DETERMINADA. No inventes artículos ni citas.

## Lo que ya cumple y no debes tocar

`renderer/js/core/calificacion.js` es el motor único y aplica correctamente el art. 2.3, el
tope de 4 del art. 25.5 en `actaEntera`, el entero del art. 25.4, los tres estados del
art. 12 con el superado parcial y su efecto del art. 18.4, la congelación del RA superado
del art. 4.3.f mediante `ra_superados`, y la pérdida del derecho a evaluación continua del
art. 3.6 en su redacción vigente. Los ejes `actividades.eval` (parcial) y
`actividades.convocatoria` (1ª y 2ª ordinaria) son correctos y se conservan. Las tablas
`calificaciones_ce`, `fase_empresa`, `evaluacion_continua` y `matricula` están bien
planteadas. `PRAGMA foreign_keys = ON`, WAL y `busy_timeout` ya están configurados, y la
recreación de tabla de `_migrarUnicidadModulos` sigue el procedimiento correcto de SQLite:
no es un residuo.

Si una modificación que vayas a hacer entra en conflicto con algo declarado correcto aquí,
detén el cambio, identifica el conflicto y resuélvelo preservando el comportamiento
correcto, salvo evidencia normativa o técnica explícita que justifique modificarlo.

## Estructura real del módulo

Tres evaluaciones parciales en módulos de primer curso, dos en los de segundo (el JSON de
normativa trae el `eval_count`). La recuperación de la primera parcial se realiza al
principio de la segunda; la de la segunda, al principio de la tercera; al final de la
tercera se recupera cualquier RA no superado del curso y se cierra la 1ª Ordinaria; lo que
quede sin superar se recupera para cerrar la 2ª Ordinaria. Las parciales son seguimiento
(art. 16); las ordinarias son las convocatorias (art. 8.3). Tres de las cuatro
recuperaciones ocurren dentro de la convocatoria 1.

---

## RF-01 — Estado de impartición del RA
*Normativo verificado la exigencia; decisión de EvalFP el reparto.*

**Estado: implementado en motor y persistencia. Falta la interfaz.**

Estado de grupo con tres valores: previsto, impartido, no impartido. No se deduce de la
existencia de actividades. "No impartido" exige fecha y motivo y se excluye del cómputo. Hoy
`rasActivos` en `contextoModulo` excluye cualquier RA sin actividad, de modo que un módulo
puede salir SUPERADO sin haberse evaluado un RA: vulnera el art. 2.3 y es el fallo más
grave.

La redistribución proporcional de la ponderación del RA no impartido entre los impartidos es
regla funcional de EvalFP, no exigencia normativa, y debe ser coherente con la programación
didáctica. Se registran ponderación original y efectiva.

Aceptación: un RA en previsto impide SUPERADO; crear o borrar actividades no cambia ningún
estado; el cierre de acta se bloquea con RA en previsto.

**Pendiente**: interfaz en la pestaña de Programación para fijar el estado, y que las
pantallas pasen `raEstados` a `contextoModulo`.

## RF-02 — La programación como modelo de datos
*Normativo verificado (arts. 4.3.a-b, 27.4) y derivado del código.*

La programación deja `modulos.data_json` y pasa a tablas normalizadas con claves foráneas:
unidades de trabajo; catálogo de CE del módulo con su RA, su peso y su instrumento previsto;
asignación UT–CE; y relación actividad–CE.

La interfaz puede mantener el flujo pedagógico RA → CE: es decisión de UX y no implica una
relación independiente UT–RA en el modelo. En persistencia, el RA de una UT o actividad se
deriva de sus CE. No podrá existir asignación UT–RA independiente que contradiga la relación
UT–CE, ni quedar tabla o lógica residual que la mantenga.

Instrumentos previstos: el art. 4.3.b los exige asociados al criterio de evaluación. Para no
obligar a rellenarlos uno a uno, se declaran por RA y los CE los heredan, con excepción
puntual por CE. La herencia es comodidad de introducción: en persistencia y en RF-11 cada CE
debe tener su instrumento previsto resuelto explícitamente, no expresado como referencia al
RA. Un CE puede tener varios. Los instrumentos previstos pertenecen a la programación y no
dependen de que existan actividades.

La actividad conserva aparte el instrumento realmente utilizado. Cuando difiera del previsto
para alguno de los CE que evalúa, la aplicación muestra aviso y conserva ambos datos; nunca
bloquea.

El catálogo de RA y CE se siembra desde `normativa/docm_json/<CICLO>_<código>.json` — para
ISO es `ASIR_0369.json`, que trae `modulo` con su `eval_count` y `ras` con los CE literales,
además de `dual_ra` para los RA de la fase en empresa. `oficial_informatica.json` solo
contiene códigos y horas de módulo y no sirve para esto. Comprueba antes si ya existe lógica
de catálogo, porque hay un `tests/unit/catalogo.test.js`: amplíala en lugar de duplicarla.
Tras esta migración, la base de datos es la única fuente de verdad del currículo: los
ficheros `scripts/modules/*_data.py` dejan de serlo.

Migración con copia previa, dentro de una transacción y con `PRAGMA foreign_key_check`
posterior. Aceptación: "dónde se evaluó el CE 2b", "qué instrumentos están previstos para el
CE 2b" y "qué evidencias justifican el RA3" se responden por consulta; no queda código que
lea asignaciones desde `data_json`.

## RF-03 — Mínimo de superación y criterio dado por alcanzado
*Normativo verificado (arts. 2.2, 4.3.a-b, 25.1, 27.4); los valores concretos son decisión de EvalFP.*

Un RA se considera superado si la media ponderada de sus CE alcanza 5 y ningún CE queda por
debajo del mínimo aplicable.

Jerarquía del mínimo: valor por defecto del módulo, mínimo específico por RA que lo
sobrescribe, y excepción específica por CE que prevalece sobre el de su RA solo para ese CE.
No se obliga a configurar un mínimo por cada CE. El sistema arranca sin mínimo fijado, y debe
distinguir dos estados distintos: "sin mínimo", que es una decisión aplicable y significa que
basta el 5 de media ponderada, y "sin configurar", que es un hueco pendiente. La aplicación
muestra siempre el valor aplicado y su origen: por defecto de módulo, específico de RA o
excepción de CE.

Se eliminan `minExam`, `raMinExamKO`, `notaExamenDecisiva` y `examenesQueDeciden`, y el
control que hoy alimenta el mínimo desde el DOM. Ningún resultado puede depender de un valor
leído del DOM.

El override individual se renombra a "criterio dado por alcanzado", con motivo obligatorio,
fecha, sesión y evidencia opcional. Se permite si el CE tiene nota por debajo del mínimo. Se
permite también si el CE tiene actividad en el grupo pero ese alumno no tiene nota; en ese
caso se identifica explícitamente como "dado por alcanzado por criterio docente" y como
"evidencia no formalizada" en informes y trazabilidad. Se bloquea si el CE no se ha evaluado
a nadie del grupo, remitiendo a RF-01. No añadas ningún bloqueo adicional. Se mantiene la
desactivación de los overrides bajo pérdida de evaluación continua.

Existe además una vista que lista todos los CE dados por alcanzado del módulo, por alumno y
por criterio, y un aviso cuando un RA queda superado únicamente gracias a overrides, sin
impedirlo.

## RF-04 — Histórico posterior al cierre
*Normativo verificado (arts. 27.3, 27.4, 30.3); el alcance limitado al post-cierre es decisión de EvalFP.*

Fecha y hora, elemento, valor anterior, valor nuevo y motivo obligatorio. Antes del cierre no
se registra nada. Los asientos no son editables ni borrables.

## RF-05 — Instantánea de criterios en el cierre
*Normativo verificado (art. 27.4).*

Al cerrar una evaluación se congelan: ponderaciones original y efectiva de cada RA, estado de
impartición de cada RA, convocatoria, y el mínimo aplicable con su valor, su origen (módulo,
RA o CE) y la configuración efectiva resultante de la jerarquía. Los resultados comunicados
se recalculan siempre contra su instantánea, nunca contra la configuración actual. Un mínimo
establecido después de un cierre solo rige hacia adelante.

## RF-06 — Almacén de evidencias y restauración
*Normativo verificado (arts. 2.4, 29.2, 29.4).*

Copia del fichero a un almacén propio junto a la base de datos, con huella de integridad,
tamaño, tipo y ruta original informativa. Vinculación a alumno, actividad y CE. Borrar una
actividad no desvincula sus evidencias.

Existe ya copia de seguridad automática diaria en `userData/backups` (`main.js:209`):
amplíala para que incluya el almacén de evidencias y verifique que el fichero resultante es
legible al crearlo. Falta la restauración: añádela desde la interfaz, con confirmación
explícita y copia previa del estado actual. Este almacén queda reservado a las evidencias de
evaluación; el material didáctico generado por IA no se copia aquí (ver RF-13).

## RF-07 — Estado explícito de la valoración
*Normativo verificado (arts. 2.3, 3.7, 25.1); el carácter manual es decisión de EvalFP.*

Pendiente, calificada, no presentado y excluida, sin NULL interpretables. Pendiente no
computa y marca la nota como provisional en pantalla y en cualquier exportación; no
presentado computa como cero y solo se establece a mano; excluida no computa y redistribuye
peso. El cierre lista los pendientes y obliga a resolverlos uno a uno.

## RF-08 — Recuperación como concepto propio
*Derivado del código el fallo; decisión de EvalFP la regla.*

Marca de recuperación en la actividad, con los CE que recupera, independiente de la parcial y
de la convocatoria. Se elimina `notas.nota_rec` y las fusiones `nota_rec ?? nota` de
`evaluaciones.js:129`, `dashboard.js:148`, `ia.js:711` e `ia.js:793`, que hoy sustituyen la
nota, pueden bajarla y contaminan el `n1` de `estadoModulo`.

La regla de conservar la mejor valoración entre evidencia original y recuperación para los CE
afectados, dentro de la misma convocatoria, es regla de negocio de EvalFP y debe ser
configurable; no la presentes como obligación normativa general.

Migración a actividades de recuperación marcadas como de origen desconocido en fecha e
instrumento, con informe previo de diferencias que exija confirmación antes de aplicar.

## RF-09 — Anonimización total frente al proveedor de IA
*Normativo verificado (arts. 29.2, 29.3) y RGPD.*

No sale nombre, apellidos, NIA, email, teléfono ni fecha de nacimiento, tampoco en el
análisis individual, que hoy envía el nombre en `ia.js:986`; el análisis de grupo ya
seudonimiza en `ia.js:468` y sirve de referencia. Token aleatorio por petición, no el `id` de
la base de datos, para que dos consultas no sean enlazables. Textos libres (observaciones de
alumno y de nota, motivos, descripciones de actividad) depurados o excluidos. Cifrado de la
base de datos en reposo.

Excepción de imágenes: localiza primero en el repositorio y en las skills disponibles la
funcionalidad de corrección de exámenes mediante fotografías; no asumas su nombre interno.
Debe avisar explícitamente antes de enviar, no enviar nunca de forma automática, aplicar
minimización cuando sea técnicamente posible, no reutilizar el `id` interno como token,
registrar que se ha producido un envío externo y quedar aislada del resto del flujo
anonimizado.

## RF-10 — Informe de justificación de la calificación
*Normativo verificado (arts. 27.4, 27.8.2).*

Informe reproducible por alumno, módulo y convocatoria, que permita reconstruir: alumno,
módulo, grupo, convocatoria y evaluación, RA y CE, ponderación original y efectiva, mínimo
aplicado con su origen, instrumentos previstos y utilizados, actividades y evidencias,
valoración y estado de cada CE y de cada RA, recuperaciones, criterios dados por alcanzado
por criterio docente, regla de cálculo aplicada, calificación interna, calificación oficial
comunicada, instantánea utilizada y fecha de generación.

Incluye una sección de contraste con la programación de esa evaluación: RA y CE evaluados
frente a programados, instrumentos utilizados frente a previstos, criterios de calificación
aplicados frente a configurados, recuperaciones realizadas frente a planificadas, y resultado
con sus reglas.

Se reconstruye desde la instantánea de RF-05, nunca recalculando contra el estado actual de
la base de datos.

Antes de implementarlo, localiza el generador de boletín PDF existente en
`renderer/js/modules/evaluaciones.js` y determina la relación: el boletín es información
comunicada de evaluación, el informe RF-10 es justificación de una calificación. No los
fusiones ni construyas un segundo generador en paralelo: factoriza un generador documental
común con documentos distintos.

## RF-11 — Documento informativo al inicio de curso
*Normativo verificado (art. 27.2).*

Documento generable al comienzo del curso con módulo, grupo, RA evaluables, CE asociados,
instrumentos de evaluación, criterios de calificación y criterios de recuperación. Su
contenido procede exclusivamente de la programación normalizada de RF-02, con el instrumento
resuelto a nivel de CE, y no de las actividades creadas después: en septiembre puede no
existir ninguna. Debe identificar la versión de programación de la que procede.

## RF-12 — Aportación del módulo para el informe de traslado
*Normativo verificado (arts. 31.2, 31.3).*

El informe de evaluación individualizado lo consigna el tutor, lo visa la dirección y su
modelo lo genera el programa de gestión del centro. EvalFP no lo sustituye: genera la
aportación de este módulo, con calificaciones de las evaluaciones realizadas y listado de RA
superados, en formato reutilizable por el tutor. El listado se deriva del estado curricular
registrado, nunca de introducción manual.

## RF-13 — La IA como parte del modelo, no como herramienta adjunta
*Derivado del código; el alcance funcional es decisión de EvalFP.*

Ninguna función de IA reimplementa ni transporta reglas de calificación: mínimos,
ponderaciones, faltas y estados se piden al motor único, nunca al DOM ni a un cálculo propio.
Hoy el informe toma `minExam` y `ponderaciones` del `dataset` y `_extractFaltasPorcentaje`
recalcula por su cuenta el 75 % del art. 3.3; ambas cosas desaparecen.

Las funciones que generan material curricular —rúbricas, actividades, exámenes— trabajan
sobre CE, no solo sobre RA como hoy hacen `ia-r-ra` e `ia-a-ra`, y su resultado se propone
como objeto de la aplicación (actividad con sus CE, rúbrica asociada a criterios) que la
docente revisa y acepta o descarta, en lugar de imprimirse en una terminal para teclearla
después.

El generador de apuntes (`scripts/build_apuntes.py`, orquestado por `scripts/ai_asistente.py`)
no se reescribe: se integra. La aplicación pregunta la carpeta destino, la recuerda como
preferencia y la pasa por el parámetro `--salida` que el script ya acepta, en lugar de
escribir en la ruta por defecto `apuntes/04-FP/{MOD}/{CURSO}/...`, que ensucia el sistema de
ficheros. Al terminar, devuelve las rutas producidas y EvalFP guarda únicamente el vínculo
con la UT y sus CE, de modo que el material sea localizable desde la programación; si el
fichero deja de existir, el vínculo se marca como roto y se avisa. No se copia al almacén de
RF-06.

`scripts/export_modulo_json.py` debe seguir emitiendo, después de la normalización de RF-02,
el contrato que espera el adaptador `_ModFromJson` de `build_apuntes.py` (`uts`, `ras`,
`ces`, `asignaciones` como `[{ut, ra, ces}]`), con un test que lo verifique: es el punto de
rotura silenciosa de esta migración.

Las respuestas del proveedor se solicitan y validan con un esquema estructurado, no por
prefijos de texto como `EVALFP_FASE:` ni con validadores frágiles del tipo
`_isValidNotasClientFormat`. La corrección de exámenes devuelve valoración por CE y archiva
la imagen como evidencia según RF-06, respetando la excepción de RF-09. Se revisa la
dependencia de Python que comprueba `_refreshPythonStatus`: o se documenta como requisito de
instalación o se elimina.

Aceptación: ninguna ruta de código de IA lee criterios del DOM ni calcula por su cuenta;
generar material no escribe en ninguna carpeta sin preguntar; el material queda listado desde
la UT a la que pertenece; y una rúbrica generada puede usarse para calificar CE sin
transcripción manual.

---

## Cómo trabajar

Primero lee y no modifiques nada. Rama git separada y commits atómicos por requisito.
Ninguna migración sin copia previa y sin ser reversible. Ejecuta las migraciones de RF-02 y
RF-08 antes de cualquier cierre de evaluación, nunca en periodo de reclamación.

No hay ni un uso de `db.transaction()` en el proyecto: toda operación que escriba en más de
una tabla o en más de una fila —guardar notas de un lote, cerrar una evaluación, cualquier
migración— se envuelve en una transacción, con verificación antes de confirmar.

Los tests corren con `vitest run`; hay unitarios en `tests/unit` (`motor-unico`,
`orden-55-2026`, `evaluation-calculations`, `convocatorias`, `catalogo`, `ce-keys`, `db`,
`handlers`, `ra-imparticion`) y un e2e de curso completo en `tests/e2e/curso-completo.spec.js`
con Playwright. Cada requisito lleva sus tests y no debe romper los existentes. No des por
terminado nada porque compile. Cambio mínimo: no reescribas lo que ya cumple.

Orden sugerido: RF-01 primero por su gravedad (ya implementado en motor y persistencia),
después RF-02 porque casi todo lo demás depende de él, luego RF-03, RF-07 y RF-08, después
RF-04, RF-05 y RF-06, y al final RF-09 a RF-13.

## Prueba de integración obligatoria, de septiembre al cierre de la 2ª Ordinaria

No des por completados los requisitos por haberlos implementado por separado. Ejecuta un
curso completo con varios RA, varios CE, varias UT, alumnado con casuísticas distintas
(incluida pérdida del derecho a evaluación continua), una recuperación en cada momento
previsto y un cambio de programación posterior a un cierre, recorriendo: siembra del catálogo
desde `normativa/docm_json`, programación con ponderaciones, mínimos e instrumentos
previstos, documento informativo inicial, creación de UT y asignación de CE, material
generado por IA vinculado a una UT, actividades con sus CE e instrumento utilizado,
evidencias, valoraciones con sus estados, cierre de cada parcial con su instantánea,
recuperaciones, cierre de 1ª Ordinaria, recuperación de junio, cierre de 2ª Ordinaria,
informe de justificación, aportación de traslado, copia de seguridad y restauración.

Comprueba que no se pierde ninguna relación; que ninguna calificación histórica cambia al
modificar la programación o los mínimos después; que un RA en previsto no aparece nunca como
superado; que un RA superado queda congelado y puede subir pero no bajar; que una
recuperación no sustituye a la baja; que las evidencias siguen vinculadas tras modificar o
borrar una actividad; que el informe de justificación reproduce exactamente lo comunicado en
su día; que la divergencia de instrumentos genera aviso y no bloqueo; y que la trazabilidad
se recorre en ambos sentidos.

## Entrega

Por cada requisito: qué has cambiado, en qué archivos y funciones, qué tests lo cubren y qué
caso límite comprueba cada uno. Y un listado final de lo que hayas dejado sin implementar y
por qué.

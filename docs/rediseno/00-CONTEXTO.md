# EvalFP — Decisiones de diseño y estado del trabajo

Fecha: 17 de agosto de 2026 · Repositorio `malogo5/EvalFP-Cuaderno-del-Profesor-para-FP` v3.16.1

---

## 1. Normativa verificada en fuente oficial

Orden 201/2024, de 28 de noviembre (DOCM 3-12-2024), en su redacción vigente tras la
Orden 55/2026, de 17 de abril (DOCM 27-4-2026). Real Decreto 659/2023, de 18 de julio.
La Orden 55/2026 suprimió el apartado 8 del art. 25 y renumeró los siguientes.

| Artículo | Qué dice |
|---|---|
| 2.2 | La evaluación comprueba la adquisición de los RA conforme a sus CE |
| 2.3 | El módulo se supera cuando se alcanzan **todos** los RA |
| 2.4 | Derecho del alumnado a acceder a pruebas y documentos de evaluación |
| 3.3 | Pérdida de evaluación continua: 75 % de asistencia en presencial |
| 3.6 | (redacción Orden 55/2026) La prueba abarca la totalidad de los RA vía CE, sin conservar calificaciones parciales |
| 4.3.a-f | La programación debe recoger RA y CE con ponderación, instrumentos asociados a los CE, criterios de calificación, planificación de recuperación, instrumentos para alumnado sin evaluación continua y temporalización de RA. Incluye: **un RA superado no se puede volver a evaluar** |
| 8.3 | Dos convocatorias ordinarias por matrícula |
| 12 | Estados: superado / superado parcial (SP) / no superado |
| 16 | Sesiones de evaluación parciales: seguimiento, no calificación final |
| 18.4 | El superado parcial cuenta como superado a efectos de promoción |
| 21.5 | RA no superados de la fase de empresa: instrumentos distintos, en el centro |
| 25.1 | La calificación es consecuencia del seguimiento del profesor responsable |
| 25.4 | Calificación numérica de 1 a 10, **sin decimales** |
| 25.5 | Si no se superan todos los RA, la calificación máxima de esa convocatoria es **4** |
| 27.2 | Informar al alumnado al comienzo del curso de instrumentos y criterios de calificación |
| 27.3 / 27.4 / 27.8.2 | Revisión y reclamación: se contrasta lo aplicado con la programación |
| 29.2 / 29.4 | Autenticidad, integridad y conservación de los documentos de evaluación |
| 30.3 | Cierre provisional y definitivo de actas |
| 31.2 / 31.3 | Informe individualizado de traslado con listado de RA superados; lo consigna el tutor y su modelo lo genera el programa de gestión del centro |

RD 659/2023: arts. 18.6, 18.7 y 163 (valoración de RA por la empresa) y 18.8 (calificación 1-10 sin decimales).

**No localizado en la norma:** el reparto proporcional de la ponderación de un RA no
impartido. Es criterio profesional y debe figurar en la programación didáctica.

---

## 2. Estructura real del módulo

- Tres evaluaciones parciales en módulos de 1.º curso; dos en los de 2.º.
- Recuperación de la 1.ª parcial → al inicio de la 2.ª.
- Recuperación de la 2.ª → al inicio de la 3.ª.
- Final de la 3.ª → se recupera cualquier RA no superado del curso; cierra la **1.ª Ordinaria**.
- Lo no superado en 1.ª Ordinaria → se recupera para cerrar la **2.ª Ordinaria**.
- Tres de las cuatro recuperaciones ocurren **dentro de la convocatoria 1**.

---

## 3. Decisiones de diseño tomadas

1. **RA no impartido**: marca de **grupo**, nunca individual. Exige fecha y motivo. Su
   ponderación se reparte proporcionalmente entre los RA impartidos, conservando
   ponderación original y efectiva. *(Regla funcional de EvalFP, no normativa.)*
2. **Superación del RA**: media ponderada de sus CE ≥ 5 **y** ningún CE por debajo del
   mínimo aplicable.
3. **Jerarquía del mínimo**: valor por defecto del módulo → mínimo por RA → excepción
   puntual por CE (prevalece la más específica). No se configura CE a CE.
4. **El mínimo nace abierto** ("sin mínimo"). Se distingue *sin mínimo* (decisión
   aplicable) de *sin configurar* (hueco). Un mínimo activado después **solo rige hacia
   adelante**.
5. **Criterio dado por alcanzado** (antes "perdonado"): permitido si el CE tiene nota bajo
   el mínimo; permitido y marcado como *evidencia no formalizada* si el CE tiene actividad
   en el grupo pero ese alumno no tiene nota; **bloqueado** si el CE no se ha evaluado a
   nadie del grupo.
6. **Recuperación**: vale la **mejor** de las dos valoraciones por CE, dentro de la misma
   convocatoria (apoyo en art. 4.3.f). Se descartó la alternativa de "nota nueva tal cual".
   Se elimina `notas.nota_rec`; la recuperación pasa a ser una actividad marcada como tal,
   con sus CE, fecha e instrumento, dentro de su propia convocatoria.
7. **Estado de la valoración**: pendiente / calificada / no presentado / excluida. El paso
   de pendiente a no presentado es **siempre manual**.
8. **Histórico**: solo se registran los cambios **posteriores al cierre** de una evaluación,
   con motivo obligatorio.
9. **Instantánea en el cierre** en vez de versionado completo de la programación. Congela
   también el **origen** del mínimo, no solo su valor.
10. **Evidencias**: se copian a un almacén propio con huella de integridad.
11. **Material didáctico generado por IA**: se queda como fichero en la carpeta que elija la
    docente; la app pregunta dónde guardarlo y solo almacena el vínculo con UT y CE.
12. **Instrumento previsto**: se declara por RA, lo heredan sus CE, con excepción puntual
    por CE. En persistencia queda resuelto **a nivel de CE** (art. 4.3.b).
13. **Divergencia instrumento previsto / utilizado**: aviso, nunca bloqueo.
14. **Catálogo de RA y CE**: se siembra desde `normativa/docm_json/<CICLO>_<código>.json`
    (ISO = `ASIR_0369.json`). `oficial_informatica.json` solo tiene códigos y horas.
15. **Anonimización frente al proveedor de IA**: total. Token aleatorio por petición, no el
    `id` interno.
16. **Operativa**: Opus y Sonnet entran en el plan; solo Fable se paga. Fable interviene en
    tres sesiones (diseño de migración, control tras RF-02, auditoría final) y trabaja sobre
    el repositorio, no sobre la app instalada.

---

## 4. Hallazgos de la auditoría sobre el código real

**Ya cumple, no tocar:** `renderer/js/core/calificacion.js` implementa arts. 2.3, 25.4,
25.5, 12, 18.4, 4.3.f y 3.6. Ejes `actividades.eval` y `actividades.convocatoria`
correctos. Tablas `calificaciones_ce`, `fase_empresa`, `evaluacion_continua`, `matricula`
bien planteadas. `PRAGMA foreign_keys = ON`, WAL y `busy_timeout` configurados. La
recreación de tabla de `_migrarUnicidadModulos` es el procedimiento correcto de SQLite.

**Fallos localizados:**

- **Crítico (art. 2.3)**: `rasActivos` en `contextoModulo` excluía del cómputo cualquier RA
  sin actividad → el módulo podía salir SUPERADO sin haberlo evaluado. *(Corregido en RF-01.)*
- **Crítico**: la programación vive como JSON en `modulos.data_json`, sin claves foráneas ni
  consultabilidad. `actividades.ra_id` y `ut_id` son texto único.
- **Alto**: `minExam` se lee del DOM → criterio de calificación fuera de la programación.
  Además es mínimo por *examen*, no por CE, y `notaExamenDecisiva` toma la peor nota.
- **Alto**: no existe tabla de auditoría; `notas` se sobrescribe.
- **Alto**: tres caminos de recuperación (`nota_rec`, `calificaciones_ce` conv. 2,
  actividades conv. 2) con reglas contradictorias. `nota_rec ?? nota` **sustituye** y puede
  bajar la nota, y contamina el `n1` de `estadoModulo`.
- **Medio**: `setRaPonderacion` sobrescribe sin histórico.
- **Medio**: `evidencias.ruta` apunta a fichero externo sin copia ni huella.
- **Medio**: no hay estado explícito de valoración (NULL ambiguo).
- **Medio**: ningún uso de `db.transaction()` en todo el proyecto.
- **Medio**: hay copia de seguridad automática (`main.js:209`) pero **no hay restauración**.
- **Protección de datos**: `ia.js:986` envía nombre y apellidos en el análisis individual
  (el de grupo sí seudonimiza, `ia.js:468`). Base de datos sin cifrar con NIA, fecha de
  nacimiento, email y teléfono.
- **IA**: reglas de negocio duplicadas fuera del motor (`minExam` y `ponderaciones` del
  `dataset`, `_extractFaltasPorcentaje` recalculando el 75 %). Material generado fuera del
  modelo. Acoplamiento por prefijos de texto (`EVALFP_FASE:`).

---

## 5. Estado del trabajo

**RF-01 implementado** (parche `rf-01-estado-imparticion-ra.patch`):

- Tabla `ra_estado` (modulo_id, ra_id, estado, motivo, fecha), de grupo.
- `getRaEstados` / `setRaEstado` en `db.js`, con motivo obligatorio para "no impartido".
- IPC en `main.js` y `preload.js`.
- Motor: `estadoImparticion`, `reparterPonderaciones`, `raPendientesDeDecidir`, `ESTADO_RA`.
  `contextoModulo` expone `raEstados`, `rasExcluidos`, `rasEnJuego`, `ponderaciones`.
  `estadoModulo` recorre los RA en juego, no solo los que tienen actividad.
- 10 tests nuevos en `tests/unit/ra-imparticion.test.js`. Batería completa: 186 en verde.

**Pendiente de RF-01**: la interfaz para fijar el estado (pestaña Programación) y que las
pantallas pasen `raEstados` a `contextoModulo`.

**Decisión pendiente de la docente**: en `tests/unit/convocatorias.test.js` se ajustó la
expectativa del boletín de trimestre. Antes un RA aún no impartido no figuraba como
pendiente; ahora sí, y el módulo sale PENDIENTE en diciembre. La media no cambia (sigue
siendo 7, no cuenta como cero). Si se prefiere que el boletín parcial no los muestre, se
resuelve en la presentación, no en el motor.

---

## 6. Tareas abiertas

- RF-02 a RF-13 sin implementar (ver prompt maestro).
- Insertar los tres apartados en la programación de ISO 26-27 y llevarlos a departamento.
- Copia manual del `.sqlite` **fuera** del repositorio antes de cualquier migración: el
  repositorio es **público** y el `.gitignore` no cubre `tmp/`, `*.sqlite`, `-wal` ni `-shm`.
- Batería de casos de referencia validados a mano para verificar el motor.
- `ai_asistente.py` (`_calc_informe_estado`, línea 1019) cuenta como `sin_nota` cualquier RA sin
  nota, incluidos los no impartidos, así que el informe de IA sale PENDIENTE de forma incorrecta
  en cualquier módulo con un RA excluido. Fallo preexistente; se resuelve en RF-13, cuando la IA
  deje de calcular por su cuenta y pida los estados al motor.

---

## 7. RF-14 — Filtrado de RA en el boletín de evaluación parcial

*Requisito de presentación, no de cálculo. Anotado tras aplicar RF-01.*

Con RF-01, un RA que aún no se ha impartido figura como pendiente y el módulo queda
PENDIENTE en las evaluaciones parciales. Es correcto en el motor: lo exige el art. 2.3.

Pero en el boletín de un trimestre puede resultar confuso listar como pendientes RA que
todavía no tocaba dar. Si molesta, se resuelve **en la presentación**: el boletín de una
evaluación parcial filtra los RA por la evaluación a la que están temporalizados y no lista
los posteriores. El motor no se toca, y el estado del módulo sigue siendo el que es.

No es urgente. Se decide al montar la interfaz de RF-01.

---

## 8. RF-15 — Control de asistencia

*Normativo verificado la necesidad (art. 3.3); los umbrales concretos son criterio de centro.*

EvalFP no registra asistencia, así que hoy la pérdida del derecho a evaluación continua se
introduce a mano en `evaluacion_continua` sin nada que la sustente. El art. 3.3 condiciona ese
derecho a la asistencia, y el art. 4.3.e obliga a que la programación prevea los instrumentos
para ese alumnado.

Registro por alumno, módulo, fecha y tramo horario, con estados presente, falta justificada,
falta injustificada y retraso. A partir de ahí, porcentaje de inasistencia sobre las horas del
módulo y aviso cuando se acerca al límite.

**Cuidado con las cifras.** El límite y la equivalencia entre retrasos y faltas **no** están en
la Orden 201/2024: son criterio de centro y deben ser configurables, no constantes en el
código. Ningún texto de la aplicación debe atribuir esas cifras a la Orden. Lo que sí es
normativo es que la pérdida del derecho se acuerde y se comunique, y sus efectos del art. 3.6
en su redacción vigente, que ya implementa el motor.

Sustituye a `_extractFaltasPorcentaje` de `ia.js`, que hoy recalcula el porcentaje por su
cuenta fuera del motor (ver RF-13).

## 9. RF-16 — Diario de observaciones

*Decisión de EvalFP; se apoya en el art. 2.2 (la observación directa como instrumento).*

Notas breves por alumno y fecha, con categoría, escritas sobre la marcha durante la clase. No
es una calificación: es la evidencia no formalizada que hoy no queda registrada en ninguna
parte.

Su valor está en RF-03: cuando se da un criterio por alcanzado por criterio docente, el motivo
puede apoyarse en una observación concreta y fechada en lugar de en un texto libre escrito
meses después. Y alimenta la vista de pendientes de RF-14 con contexto sobre cada alumno.

Requiere que la observación directa figure como instrumento en la programación (art. 4.3.b) si
va a sustentar la valoración de un criterio.

**Origen de ambos requisitos:** un prototipo alternativo generado con Arena AI a partir de un
prompt de un párrafo. Se descartó como sustituto —sin tests, sin convocatorias, con el mismo
agujero del art. 2.3 y con cifras normativas inventadas— pero tenía estas dos piezas que
EvalFP no cubre.

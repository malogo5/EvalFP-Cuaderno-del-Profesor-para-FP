# La elección de RA y CE en la programación

30/07/2026 · revisión de coherencia entre lo que se elige en Programación y lo que
después calculan Evaluaciones, Dashboard e IA.

## El fallo de fondo: «CR1» no identifica a ningún criterio

Los decretos numeran los criterios **dentro de cada resultado de aprendizaje**: RA1 tiene
CR1…CR10 y RA2 vuelve a empezar por CR1. En los 91 módulos del catálogo, sin excepción, el
identificador de criterio se repite entre RA.

La aplicación guardaba en cada actividad una lista de criterios **con el id suelto**
(`["CR1","CR2"]`) y el motor de notas comparaba solo ese id. Consecuencia: cualquier actividad
con «CR1» contaba en el CR1 de **todos** los RA del módulo.

Reproducido con datos reales (0651 Comunicación y atención al cliente, una práctica por RA):

| | RA1 | RA2 | RA3 | RA4 | RA5 | RA6 | RA7 |
|---|---|---|---|---|---|---|---|
| Notas puestas | 9 | 3 | 8 | 4 | 7 | 2 | 10 |
| Lo que calculaba | 6,10 | 6,10 | 6,09 | 6,09 | 6,14 | 6,10 | 6,10 |
| Lo que calcula ahora | 9,00 | 3,00 | 8,00 | 4,00 | 7,00 | 2,00 | 10,00 |

Siete resultados de aprendizaje distintos se fundían en una misma media. Con eso, la regla de
oro (todos los RA ≥ 5) no separaba nada y ningún RA suspenso salía como tal: exactamente lo
que no aguanta una reclamación.

**Arreglado**: los criterios se guardan como par `RA|CE` (`"RA4|CR1"`), la misma clave compuesta
que ya usaban perdones y notas de 2ª ordinaria. Está en `renderer/js/utils/ce-keys.js`, y todo lo
que lee criterios pasa por ahí. Las actividades ya guardadas **se traducen solas** la primera vez
que se abre Programación, Evaluaciones, Dashboard o el asistente: cada id suelto se resuelve
contra los RA que la actividad evalúa de verdad.

## Lo demás que no cuadraba

**La evaluación de un RA dependía de dónde lo mirases.** El reparto de RA por trimestre estaba
congelado en el catálogo (`eval_ras`) y no se tocaba al mover una UT de evaluación: el Plan de
Actividades decía una cosa, la Distribución de RAs otra y la ficha del RA una tercera. Ahora las
tres salen del mismo sitio —la evaluación de las UT que trabajan ese RA— y el módulo se actualiza
en disco, que es lo que leen los informes.

**Una UT con dos RA perdía el segundo.** En la distribución por evaluaciones, en el reparto de
pesos del dashboard, al asignar una UT a una actividad y en el modal de UT del examen se cogía
solo la primera asignación. Ahora entran todas.

**Un RA evaluado solo con un examen de varias unidades desaparecía.** Evaluaciones daba por
«activo» un RA únicamente si alguna actividad llevaba su `ra_id`, y un examen que cubre dos UT no
puede llevar uno solo. Ese RA no aparecía en pantalla y se escapaba de la regla de oro. Ahora una
actividad cuenta para un RA por tres caminos: `ra_id`, criterios marcados o sus UT.

**El modal de RA/CE marcaba lo que nadie había marcado.** Si un RA estaba asignado a una UT sin
criterios, al abrirlo salían **todos** seleccionados; guardar sin tocar nada le metía los 10
criterios. Ahora se muestra exactamente lo guardado, marcar un RA propone sus criterios solo si no
había ninguno elegido, y guardar un RA sin criterios pide confirmación, porque así no evalúa nada.

**El modal de criterios de una actividad duplicaba casillas.** En un examen sobre dos UT con dos
RA, «CR1» aparecía dos veces y marcar uno marcaba el otro. Cada casilla lleva ahora su clave
`RA|CE` y el grupo se encabeza con el nombre del RA.

**Cambiar la UT de una actividad dejaba criterios huérfanos**, que seguían calificando un RA que la
actividad ya no tocaba; el contador podía enseñar «10/6». Al cambiar de UT —o al editar los RA/CE
de una UT, o al borrarla— se recolocan el RA y los criterios de las actividades afectadas y se
avisa de cuántos se han quitado. El contador cuenta ahora criterios válidos sobre disponibles.

**El aviso de horas estaba siempre en ámbar en Grado Básico.** Las UT reparten las horas de
**aula**, y se comparaban con la duración oficial, que incluye la formación en empresa. Ahora se
compara con las de aula y la etiqueta lo dice: «Σ 200h / 200h de aula ✓».

**Borrar la ponderación de un RA daba error.** Dejar la casilla vacía es legítimo —ese RA aún no
está ponderado— y saltaba «Ponderación inválida».

**Los informes de IA se saltaban los exámenes multiunidad.** Python agrupaba por `ra_id` y los
descartaba; ahora deduce el RA de las claves `RA|CE` y reparte el peso entre los RA implicados.

## Cómo comprobarlo

```
npm test                 # incluye tests/unit/ce-keys.test.js y los del motor de notas
npm run test:auditoria   # la fase de programación verifica ahora las tres coherencias
```

El test unitario del motor usa a propósito ids repetidos (CR1 en RA1 y en RA2): con el código
anterior fallaba.

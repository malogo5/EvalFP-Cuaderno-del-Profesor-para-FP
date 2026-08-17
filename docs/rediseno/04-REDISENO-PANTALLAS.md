# Rediseño de la capa de interfaz — las tres pantallas

> Decisiones tomadas el 17 de agosto de 2026. Afectan solo al renderer: el motor de cálculo
> (`renderer/js/core/calificacion.js`), la base de datos y los tests se conservan.
>
> Este documento se lee **junto a** `01-PROMPT-MAESTRO.md`, no en su lugar. Varios requisitos
> tocan estas mismas pantallas: RF-02 reescribe Programación, RF-03 y RF-07 tocan Notas, y
> RF-05, RF-07 y RF-10 alimentan Evaluación. No son proyectos paralelos: al implementar cada
> requisito hay que darle la forma que describe este documento.

## Por qué

La aplicación ha crecido a parches. Al incorporar toda la normativa de FP y la parte de IA, la
capa de interfaz ha quedado incómoda: `programacion.js` con 1.741 líneas, `ia.js` con 1.340, la
programación viviendo dentro de un JSON y la IA manejada desde una terminal.

El motor, en cambio, está verificado: 186 tests y siete auditorías. **No se reescribe.** Para
aumentar la confianza en los cálculos el camino es una batería de casos de referencia
validados a mano, no rehacerlo.

---

## 1. Programación

**Problema principal: el flujo.** La pantalla presenta el currículo entero de golpe y hay que
ir rellenando huecos sin un orden que guíe. Lo que se busca es lo contrario: partir de los
RA/CE, crear una UT, asignarle RA y CE, y seguir.

Se parte en dos vistas, porque hoy la pantalla hace dos trabajos distintos mezclados.

### 1.1 Vista «Resultados de aprendizaje» — configuración

Tabla compacta, **una fila por RA**, sin tarjetas de media pantalla:

- ponderación del RA
- estado de impartición (RF-01): previsto / impartido / no impartido
- instrumento previsto (RF-02)
- mínimo de superación con su origen (RF-03)
- porcentaje en empresa

Al desplegar una fila aparecen sus CE. La **ponderación por CE existe y es configurable**,
pero la columna va **plegada por defecto**; mientras no se rellene, los CE de un RA pesan
igual. La cabecera de esa columna debe decir «reparto automático» en lugar de mostrar casillas
vacías: una casilla en blanco parece un dato que falta, y no lo es.

Se toca al principio de curso y casi nunca más.

### 1.2 Vista «Unidades de trabajo» — el flujo guiado

Botón **Nueva UT** y, a partir de ahí:

1. nombre y **evaluación prevista**
2. elegir los RA que trabaja
3. dentro de esos RA, marcar los CE concretos, viendo cuáles ya están asignados a otra UT y
   cuáles siguen sin cubrir
4. al guardar, la UT aparece en la lista con sus CE y con un botón para **crear actividades**
   desde ella misma

**Indicador de cobertura curricular permanente**: «38 de 52 criterios asignados a alguna UT»,
con los que faltan a un clic. Es lo que hace el flujo guiado sin imponer un orden rígido: en
todo momento se ve cuál es el siguiente paso. Al final de curso, ese mismo indicador señala lo
que se quedó sin programar, y enlaza con RF-01.

### 1.3 Temporalización

**La temporalización se declara en la UT; el RA hereda la suya de las UT que lo trabajan.**
No al revés.

Sigue cumpliendo el art. 4.3.f: la programación temporaliza los RA, solo que el dato se deriva
en vez de teclearse. En el documento de RF-11 debe salir cada RA con su evaluación.

Dos consecuencias que hay que implementar explícitamente:

- Un RA trabajado en varias UT **hereda un rango**, no un valor: si aparece en la UT1 de la 1.ª
  evaluación y en la UT4 de la 3.ª, su temporalización es «de la 1.ª a la 3.ª». Para saber si
  está completo, manda la última.
- **Mover una UT de evaluación recalcula la temporalización del RA, pero no toca nada de lo ya
  evaluado.** Actividades, evidencias y notas siguen donde estaban, con su fecha y su
  convocatoria. La temporalización es previsión; lo evaluado es hecho.

---

## 2. Notas

**Problema principal: la densidad.** Hoy solo se puede filtrar por evaluación, y cuando una
evaluación tiene muchas actividades meter notas resulta denso.

**Solución: la actividad es la unidad de trabajo.** Se elige una actividad y se abre una
pantalla dedicada a calificarla. Encaja con RF-02: si la actividad ya declara sus CE, es
también donde se califica.

### 2.1 Lista de actividades

Filtrable **por UT además de por evaluación**, con un indicador de progreso por actividad
(«18 de 24») para ver de un vistazo qué está a medias. Avisa de las actividades con notas
pendientes cuando se acerca un cierre.

### 2.2 Pantalla de calificación

Pantalla completa, **una fila por alumno**:

- nombre y casilla de nota grande
- los estados de RF-07 a un clic: pendiente / no presentado / excluida
- navegación con Enter para bajar al siguiente
- guardado automático
- arriba, el contexto de la actividad: UT, CE que evalúa, instrumento, fecha y convocatoria
- **adjuntar la evidencia de cada alumno desde aquí mismo** (RF-06), que hoy queda desconectado

### 2.3 Dos modos de calificación

El modo **se declara en la actividad al crearla**, no en la pantalla de notas: así no hay que
decidirlo cada vez que se entra a calificar.

- **Nota única**: una casilla; esa nota se aplica por igual a todos los CE que evalúa la
  actividad.
- **Desglose por CE**: la fila del alumno se abre en tantas casillas como CE evalúe la
  actividad (un examen por preguntas, una rúbrica). La nota de la actividad se calcula a partir
  de ellas con la ponderación de CE de la vista 1.1.

El desglose es **lo que da sentido al mínimo por CE de RF-03**: con nota única, el mínimo no
puede distinguir entre los CE de una misma actividad — o pasan todos o fallan todos.

**Cambio de modo:**

- De nota única a desglose: la nota simple **se copia a cada CE como punto de partida**, para no
  perder trabajo, avisando de que a partir de ahí son notas independientes.
- De desglose a nota única: se pierde el detalle, así que **pide confirmación**.

---

## 3. Evaluación

**Problema principal: ver quién está pendiente de qué.**

La clave del diseño es que «pendiente» significa hoy tres cosas distintas que no deben
mezclarse:

| Tipo | Qué es | Quién lo resuelve |
|---|---|---|
| Pendiente **tuyo** | Actividades entregadas y sin calificar | La docente, poniendo notas |
| Pendiente **del alumno** | No ha entregado, no se ha presentado, o tiene un RA no superado que recuperar | El alumno; es lo que se comenta en la sesión |
| Pendiente **del calendario** | RA que aún no tocaba dar | Nadie: no es una alarma (RF-14) |

### 3.1 Vista de grupo (la que se abre por defecto)

Tabla de **una fila por alumno** para la evaluación elegida, con columnas cortas y numéricas:

- actividades sin calificar
- actividades sin entregar
- RA no superados
- RA sin ninguna evidencia
- estado del módulo
- nota provisional

Cada número lleva al detalle al pulsarlo. Arriba, contadores del grupo: cuántas notas faltan
por poner, cuántos alumnos tienen algún RA sin superar, cuántos están en riesgo de no superar
el módulo por el tope de 4 del art. 25.5.

**El orden importa**: primero lo tuyo, porque hasta que no se resuelve los datos del alumno no
son fiables. Por eso la nota aparece marcada como **provisional** mientras queden pendientes
propios, que es lo que ya exige RF-07.

### 3.2 Vista por alumno

Se abre pulsando una fila: ficha con todo su detalle y **flechas para pasar al siguiente sin
volver atrás** — el gesto de la sesión de evaluación cuando se va uno por uno.

### 3.3 Exportación

El mismo dato, en papel o PDF, eligiendo entre el resumen del grupo y el detalle de todo el
alumnado. Debe apoyarse en el **generador documental común** de RF-10, no en un generador
nuevo.

---

## Qué NO cambia

- `renderer/js/core/calificacion.js` y sus reglas.
- El esquema de evaluación ya verificado (`calificaciones_ce`, `ra_superados`,
  `evaluacion_continua`, `fase_empresa`, `matricula`).
- Los 186 tests existentes.
- Los ejes `actividades.eval` (parcial) y `actividades.convocatoria` (ordinaria).

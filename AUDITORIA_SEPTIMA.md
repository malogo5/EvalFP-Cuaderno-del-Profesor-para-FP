# Séptima auditoría · usando la aplicación

Esta ronda se hizo con la aplicación abierta y delante: dar de alta un módulo del catálogo,
crear alumnado, importar una lista de clase y recorrer las pantallas mirando lo que sale.

Cuatro hallazgos, y un susto que resultó no ser un fallo.

---

## El susto: el cuaderno estaba vacío

Al abrir Ajustes, la base no tenía ni un módulo y las tres copias de seguridad tampoco —
incluida una anterior a todos los cambios de estos días, así que no lo había provocado
ninguna de las auditorías. No hubo pérdida real (era el alumnado inventado de las pruebas),
pero de ahí salió el hallazgo más útil de la ronda.

### A14-1 · Una copia vacía se leía igual que una llena — **Gravedad: Alta**

En Ajustes ponía «3 copias guardadas · la última del 2/8 (84 KB)». Una base vacía pesa 86 KB
y una con un curso entero, 90: **por el tamaño no se distinguen**. Una copia inservible
parecía tan buena como cualquier otra, y eso solo se descubre al restaurarla, que es el peor
momento posible.

Ahora cada copia dice cuántos módulos, alumnos y notas lleva dentro, y si el cuaderno está
vacío mientras existe una copia con datos, sale un aviso en rojo con la fecha de esa copia.

---

## A15-1 · El «Acerca de» llevaba cinco versiones sin novedades — **Gravedad: Media**

La ventana buscaba en el CHANGELOG un encabezado con corchetes, `## [3.9.0]`, y las versiones
llevan tiempo escribiéndose `## 3.14.0 · Sexta auditoría`. Como no lo encontraba, enseñaba
siempre el texto de reserva: «Consulta CHANGELOG.md para el detalle de esta versión». Ahora
acepta los dos formatos y saca los titulares de cada novedad.

## A15-2 · El catálogo se presentaba como si solo hubiera grado superior — **Gravedad: Baja**

La cabecera de Módulos decía «Ciclo Formativo de Grado Superior» aunque el catálogo trae
también grado básico, grado medio y cursos de especialización.

## A15-3 · El grupo, en una línea suelta — **Gravedad: Baja**

En la tarjeta de cada módulo, «Grupo:» quedaba solo al final de una línea y el nombre del
grupo caía en la siguiente. Y si el módulo no tenía grupo, la palabra salía igual sin nada
detrás.

## A15-4 · «Omitidos por duplicado» cuando no era duplicado — **Gravedad: Baja**

Al importar la lista de clase, el aviso achacaba a los duplicados también las líneas que
venían sin nombre. Ahora dice los dos motivos.

## A15-5 · Los apellidos con tilde salían rotos en el nombre del PDF — **Gravedad: Media**

Esto apareció mirando los boletines que ya había en el ordenador:
`boletin_Alarc_n_Vega__Luc_a_1785516525526.pdf`. Todo lo que no fuera una letra inglesa o un
número se sustituía por un guion bajo, así que **media clase tenía el apellido roto** en un
documento que se entrega a las familias. Las tildes y las eñes valen perfectamente en macOS y
en Windows; lo único que no vale es `/ \ : * ? " < > |`.

Y el nombre llevaba pegada la hora en milisegundos, de modo que cada vez que se generaba el
mismo boletín aparecía otro archivo: en esa carpeta había **cinco copias del mismo alumno de
la misma tarde**. Ahora manda la fecha y regenerarlo el mismo día sustituye al anterior.

---

## Segunda tanda, recorriendo las pantallas con datos

Con un módulo dado de alta, alumnado y notas puestas a mano.

### A15-6 · El boletín y la pantalla de Evaluaciones no decían lo mismo — **Gravedad: Alta**

Mismo alumno, misma evaluación: **Evaluaciones decía 6,3 y el boletín 6,53**. Y el boletín es
el papel que se lleva la familia.

El boletín calculaba la nota del trimestre por su cuenta —una media de las actividades
ponderada por su peso—, sin pasar por los criterios, sin pasar por los resultados de
aprendizaje y sin mirar la escala de cada instrumento. La octava pantalla con su propio motor,
y la que más lejos llega.

Ahora la nota de cada evaluación sale de `contextoModulo` + `estadoModulo`, como en todas las
demás, y la media global del boletín es la del módulo —la de los RA ponderada por su peso, la
que va al acta— en vez del promedio de los tres trimestres. Comprobado en la aplicación: el
boletín pasó a decir 6,29 y Evaluaciones 6,3, que es el mismo número.

### A15-7 · Los contadores de Evaluaciones no sumaban — **Gravedad: Media**

Con cinco alumnos activos se leía «0 superan · 0 no superan · 2 sin evaluar del todo». Los
otros tres no aparecían en ninguna parte: eran los que aún no tenían ninguna nota. Un recuento
que no cuadra hace dudar de toda la pantalla. Ahora son «a medio evaluar» y «sin ninguna nota»,
y la suma da los activos.

### A15-8 · Un botón que parecía una etiqueta — **Gravedad: Baja**

En Programación, el botón para elegir las unidades de un examen se llamaba «UT», igual que los
chips de las unidades que tiene al lado. Ahora dice «Cambiar».

---

## Lo comprobado en la aplicación

- El catálogo abre los 91 módulos y da de alta ISO · 1ºA con sus 8 RA, sus criterios literales
  del decreto y sus ponderaciones.
- La importación de la lista de clase **ya no revienta** cuando hay una fila todavía en blanco
  —el fallo que cerró la cuarta auditoría—, separa por punto y coma además de por comas, e
  ignora las líneas vacías y las de solo espacios.
- Las copias de seguridad muestran su contenido y marcan en rojo las que están vacías.

---

## Estado

| | |
|---|---|
| Hallazgos | 8 corregidos |
| Pruebas | 149 unitarias |
| Total en siete auditorías | 83 incidencias cerradas |

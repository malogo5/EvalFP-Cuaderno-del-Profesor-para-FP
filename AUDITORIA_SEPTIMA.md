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
| Hallazgos | 4 corregidos |
| Pruebas | 144 unitarias |
| Total en siete auditorías | 79 incidencias cerradas |

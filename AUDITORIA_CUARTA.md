# Cuarta auditoría · agosto de 2026

Después de tres pasadas, buscar «leyendo el código otra vez» ya no daba nada. Esta cambia de
método: en vez de mirar, se ataca.

Lo que se ha hecho: lanzar **13.000 combinaciones al azar** contra las reglas de la Orden
201/2024 comprobando que ninguna se rompe; deshacer la programación después de haber
calificado; y teclear lo que se teclea de verdad —comas decimales, listas pegadas de una hoja
de cálculo, valores absurdos—.

Seis hallazgos. Dos de ellos afectan directamente a la nota de un alumno.

---

## A6 · Miles de casos aleatorios contra las reglas de la Orden

Trece mil módulos inventados —con sus RA, sus criterios, sus pesos, sus escalas y sus notas
al azar— comprobando en cada uno que se cumplen las reglas: que superar exige todos los RA
alcanzados, que el acta topa en 4 sin aprobar y no baja de 5 aprobando, que la escala del
instrumento se respeta, que subir una nota nunca baja la media, que un RA que no se ha
trabajado no cuenta, y que dos cálculos iguales dan lo mismo.

Aguantó todo menos una cosa.

### A6-1 · Presentarse a la recuperación podía salir caro — **Gravedad: Alta**

La nota de un RA en 2ª convocatoria podía quedar **por debajo** de la que el alumno ya tenía
en la 1ª. El caso: un criterio que durante el curso no llegó a calificarse, y que la prueba de
junio sí evalúa. Ese criterio nuevo entra en la media del RA y podía hundir uno que estaba en
9. Y bastaba con marcar «todos» los criterios al crear la prueba, que es lo más cómodo de
hacer, y lo que hicimos en la auditoría anterior sin darnos cuenta.

Va contra el art. 4.3.f, que prohíbe volver a evaluar un RA superado. Ahora la 2ª convocatoria
nunca deja un RA peor de como estaba.

### A6-2 · Un 8 y un RA suspenso a la vez — **Gravedad: Media**

Variante del anterior, que apareció al escribir la prueba del arreglo. Con un 8 en el examen
de mayo y un 2 en el de junio, la nota se quedaba —bien— en 8, pero el mínimo de examen miraba
el de junio y dejaba el RA sin alcanzar. Un RA con un 8 y suspenso al mismo tiempo.

---

## A7 · Cambiar la programación con notas ya puestas

### A7-1 · Criterios fantasma — **Gravedad: Media**

Al quitar un criterio de la programación, las actividades seguían apuntando a él. No se veía
en ninguna parte y reaparecía si alguien creaba después otro criterio con el mismo
identificador. Ahora se limpian solos al guardar.

### A7-2 · Actividades que se quedan sin dueño, en silencio — **Gravedad: Alta**

Al quitar un RA, las actividades que lo calificaban se quedaban huérfanas: seguían en la
parrilla, con sus notas puestas, pero ya no contaban para nada. Quien metió esas notas da por
hecho que cuentan.

No se pueden borrar solas —son notas—, así que ahora la aplicación lo dice con nombre y
apellidos: qué actividades han quedado sueltas y qué hacer con ellas.

---

## A8 · Lo que se teclea de verdad

### A8-1 · «7,5» valía 7 — **Gravedad: Alta**

En español la coma es el separador decimal, y es lo que se teclea. Según el idioma del
sistema, el campo devolvía 7 —medio punto perdido, sin un aviso— o directamente vacío,
borrando la nota. Ahora «7,5» son siete y medio, en la pantalla y en la base de datos.

### A8-2 · La base no defendía sus propios límites — **Gravedad: Media**

Las notas sí estaban protegidas, pero no el resto: una ponderación de RA admitía 1000, −20 o
la palabra «mucho»; una actividad admitía peso −50, escala 0 —cualquier nota valdría infinito
al pasarla a base 10— y evaluación 99, que crea una columna que ninguna pantalla enseña, con
notas dentro. La interfaz lo comprobaba; ahora la base también.

---

## A9 · Faltas, convocatorias e importación

Las convocatorias (cuatro en grado D, dos en grado E) y el aviso del 25 % de faltas están
bien, y los 91 módulos tienen horas para calcularlo. La importación, no.

### A9-1 · Importar la lista se rompía si había una fila en blanco — **Gravedad: Media**

Pulsar «añadir alumno» deja una fila sin nombre. Al importar después la lista de clase, la
comprobación de duplicados llamaba a `toLowerCase()` sobre ese hueco y reventaba **la
importación entera**, con un mensaje de error genérico. De paso, ahora la lista se puede pegar
con tabuladores o punto y coma —como sale de una hoja de cálculo— y no solo con comas.

---

## Estado

| | |
|---|---|
| Hallazgos | 6, todos corregidos |
| Pruebas | 131 unitarias, de 114 al empezar |
| Casos aleatorios | 13.000, sin infracciones tras los arreglos |

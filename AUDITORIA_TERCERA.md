# Tercera auditoría · agosto de 2026

Las dos anteriores miraron el código (31 incidencias) y el uso normal de la aplicación
con dos módulos reales (17). Esta va por los ángulos que ninguna de las dos tocó: los datos
personales, el aguante con un curso entero, el catálogo completo, los caminos poco
recorridos y lo que quedaba suelto.

Diez hallazgos, todos corregidos y cubiertos con pruebas.

---

## A1 · Datos personales y seguridad

### A1-1 · «Anonimizar» no anonimizaba — **Gravedad: Alta**

El nombre se sustituía por sus iniciales: `Alumno_ANON_FGS`. En un grupo de veinte personas
eso identifica a casi cualquiera, así que no era anonimizar, era disimular. El informe no
necesita el nombre —lo pone quien lo entrega—, de modo que ahora no sale ninguno.

### A1-2 · La casilla de anonimizar venía desmarcada en el informe — **Gravedad: Alta**

En el plan de recuperación y en la corrección desde foto venía marcada; en el informe
individual, que es el que más datos lleva, no. Ahora las tres vienen marcadas.

### A1-3 · La ventana que imprime el boletín ejecutaba JavaScript — **Gravedad: Media**

El boletín se construye con nombres y observaciones y se carga como `data:` URL, fuera de la
política de seguridad de la ventana principal. Un nombre con etiquetas dentro no llegaba a
ninguna parte porque todo se escapa, pero la ventana no tenía por qué poder ejecutar código:
un documento que se imprime no lo necesita. Ahora va con `javascript: false`.

### A1-4 · La ventana principal podía abrir ventanas y navegar fuera — **Gravedad: Baja**

La aplicación funciona sin conexión y no tiene enlaces externos. Ahora se rechazan las
ventanas nuevas y cualquier navegación que no sea al propio `index.html`.

---

## A2 · Aguante con un curso real

Probado con 6 módulos, 180 matrículas y 8.640 notas: las lecturas son instantáneas y la base
ocupa medio megabyte. Dos cosas sí aparecieron.

### A2-1 · La pantalla de evaluaciones tardaba el doble de lo necesario — **Gravedad: Media**

Los criterios de cada actividad viajan como texto JSON y se preguntaban una vez por alumno,
por RA y por criterio: más de cien mil `JSON.parse` cada vez que se repintaba la pantalla.
Con el resultado recordado junto a la actividad, el cálculo de un grupo de 30 pasa de
**216 ms a 84 ms**, medido tres veces antes y después.

### A2-2 · El disco lleno decía «inténtalo de nuevo» — **Gravedad: Media**

Con el disco lleno, SQLite responde «disk I/O error» y la aplicación lo traducía por «ha
ocurrido un error, inténtalo de nuevo». Lo natural entonces es reintentar, y cada reintento
falla igual mientras se siguen perdiendo las notas que se están poniendo. Ahora se dice lo
que pasa y qué hacer. De paso, los avisos que escribe la propia aplicación —«La evidencia
está fuera de la carpeta de EvalFP»— ya no se tapan con el mensaje genérico.

Comprobado también que un apagón a media escritura no corrompe nada: con el registro de
escritura anticipada, la última nota guardada sobrevive a un cierre a lo bruto.

---

## A3 · El catálogo entero, módulo a módulo

Los 91 módulos se dan de alta sin un solo error, y con todas las actividades a 7 los 91
devuelven un 7. Dos incoherencias de datos.

### A3-1 · Cuatro módulos sin ciclo — **Gravedad: Media**

Los de Informática de Oficina tenían el campo vacío, y el ciclo sale impreso en el boletín
que se entrega a la familia.

### A3-2 · Dos módulos con una evaluación de más — **Gravedad: Media**

Los cursos de especialización se organizan en dos trimestres, pero uno de Ciberseguridad y
otro de IA y Big Data se habían quedado con tres mientras sus compañeros de curso tenían dos.
La aplicación ofrecía una tercera evaluación inexistente y el boletín del mismo alumno no
cuadraba de un módulo a otro. Arreglado en el generador, no a mano: la regla ahora vale para
2º curso y para los cursos de especialización.

---

## A4 · Los caminos poco recorridos

Archivar y recuperar módulos, copias de seguridad, borrados en cascada, dos ventanas a la
vez y los cuatro estados del alumnado: todo correcto. Uno falló.

### A4-1 · No se podía empezar el curso siguiente — **Gravedad: Alta**

Un módulo era único por su clave y su grupo, sin mirar el año. En septiembre, al dar de alta
ISO · 1ºA del curso nuevo, saltaba «UNIQUE constraint failed» mientras existiera el del curso
anterior — y archivarlo no bastaba, porque la restricción mira toda la tabla. La única salida
era borrar el curso pasado para poder empezar el siguiente.

Ahora la unicidad es **módulo, grupo y curso escolar**. La migración se probó sobre una base
con el esquema anterior: conserva los módulos y su alumnado, admite el año nuevo y sigue
rechazando el duplicado exacto.

---

## A5 · Lo que quedaba

### A5-1 · Sesenta campos sin nombre para un lector de pantalla — **Gravedad: Media**

Ni un solo `<select>` o `<input>` tenía etiqueta asociada: quien no ve la pantalla oye «menú
desplegable» y no sabe si elige módulo, evaluación o proveedor. Cuarenta y dos etiquetas ya
existían y solo les faltaba el vínculo; los dieciocho restantes llevan ahora su descripción.

### A5-2 · La documentación no decía qué sale del ordenador — **Gravedad: Media**

Tratándose de datos de menores, ahora hay una tabla de qué se envía y qué no cuando se usa la
IA, dónde viven los datos y cómo borrarlo todo. Y en las instrucciones de compilación, lo que
no estaba escrito y costó descubrir: que PowerShell bloquea `npm` y hay que llamar a
`npm.cmd`, y qué instalar en una máquina virtual con Windows on ARM.

Sin vulnerabilidades en las dependencias (`npm audit`), sin código muerto, sin `TODO`
pendientes y sin jerga técnica en los textos de la interfaz.

---

## Estado

| | |
|---|---|
| Hallazgos | 10, todos corregidos |
| Pruebas | 114 unitarias, de 95 al empezar |
| Ficheros nuevos de prueba | `catalogo.test.js` (los 91 módulos) |
| Comprobado a mano | 6 módulos · 180 matrículas · 8.640 notas · 91 módulos dados de alta |

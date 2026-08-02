# Quinta auditoría · agosto de 2026

Ángulos que seguían sin tocarse: el paso del tiempo dentro de un curso (cerrar, reabrir,
volver a cerrar), dos ventanas abiertas a la vez, y la corrección de exámenes desde foto.

Seis hallazgos.

---

## A10 · Cierres, reaperturas y el paso del tiempo

Lo esencial funciona: el cierre guarda el RA alcanzado, bajar una nota después no lo tumba,
subirla sí lo mejora, un cierre posterior con peor nota no baja el anterior, y reabrir
devuelve el RA a lo que digan las notas. Uno falló.

### A10-1 · Cierres zombis — **Gravedad: Media**

Al quitar un RA de la programación, su cierre de evaluación se quedaba en la base. Si algún
día se crea otro RA con ese mismo identificador —cosa normal: todos se llaman RA1, RA2…—,
nacería **congelado con una nota antigua** que nadie recuerda haber puesto, y ninguna
actividad podría bajarlo. Ahora se retiran al guardar la programación, y se avisa: un cierre
de evaluación es un acto formal y su desaparición hay que contarla.

---

## A11 · Dos ventanas a la vez

### A11-1 · «La base de datos está bloqueada» — **Gravedad: Alta**

Si una ventana estaba escribiendo —un cierre de evaluación, una copia de seguridad—, la otra
fallaba **al instante** con «database is locked» y la nota recién tecleada no se guardaba.
SQLite esperaba cero. Ahora espera cinco segundos y reintenta él solo: en la prueba, una nota
que antes se perdía ahora se guarda tras esperar 913 ms a que la otra ventana terminara. Y si
aun así se agota la espera, el aviso dice qué pasa en vez de «error de base de datos».

### A11-2 · La aplicación se abría dos veces sobre los mismos datos — **Gravedad: Media**

Cada ventana lleva sus datos en memoria: se cambia una nota en una, la otra no se entera y al
guardar escribe encima con lo que tenía de antes. Ahora la segunda no se abre: trae al frente
la que ya estaba. Las pruebas automáticas, que usan su propia carpeta de datos, no se estorban.

---

## A12 · La corrección de exámenes desde foto

Lo de fondo está bien: las fotos se recortan por arriba para no enviar el nombre manuscrito,
las copias que se envían viven en una carpeta temporal que se borra sola, hay límite de
páginas y de tamaño, y la agrupación por alumno se calcula en el ordenador para poder
revisarla antes de gastar un céntimo. Pero al guardar la nota había dos cosas.

### A12-1 · La nota de la IA ignoraba la escala de la actividad — **Gravedad: Alta**

La corrección puntúa siempre sobre 10. Si la actividad se califica sobre 20, ese 8,5 se
guardaba tal cual y valía un 4,25; si se califica sobre 5, un 8 se salía de la escala. Ahora
la escala aparece en el desplegable, la nota se convierte y se pide confirmación antes.

### A12-2 · Las notas que fallaban al guardarse desaparecían — **Gravedad: Media**

En el guardado por lotes, un error se anotaba en la consola —que nadie mira— y el aviso solo
contaba las guardadas. Quien corrige veinte exámenes daba por hechas las veinte notas. Ahora
se dice cuántas han fallado y por qué.

### A12-3 · Otro error crudo en pantalla — **Gravedad: Baja**

Quedaba un `alert` con el mensaje interno tal cual, de los que la tercera auditoría ya había
quitado de las demás pantallas.

---

## Estado

| | |
|---|---|
| Hallazgos | 6, todos corregidos |
| Pruebas | 138 unitarias, de 131 al empezar |
| Total en cinco auditorías | 70 incidencias cerradas |

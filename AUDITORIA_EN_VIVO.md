# Auditoría usando la aplicación · 01/08/2026

Segunda vuelta de la auditoría, esta vez **manejando EvalFP como la maneja una
profesora**: dando de alta módulos, importando alumnado, programando, calificando
y sacando documentos. La primera auditoría se hizo leyendo el código y ejecutando
el motor; esta busca lo que solo aparece al usar la aplicación.

**Entorno.** EvalFP 3.8.0 · macOS · base de datos real, con copia de seguridad
guardada aparte antes de empezar.

**Datos de prueba.** Dos módulos nuevos, identificables por su grupo:

| Módulo | Ciclo | Curso | Grupo | Evaluaciones |
|---|---|---|---|---|
| IMRTD · Instalación y Mantenimiento de Redes para Transmisión de Datos | CFGB Informática de Oficina | 2º | AUD-2A | 2 |
| ISO · Implantación de Sistemas Operativos | CFGS ASIR | 1º | AUD-1A | 3 |

---

## V-1 · Un módulo no se puede dar de alta dos veces, para dos grupos

**Categoría:** Error confirmado · **Gravedad: Alta**
**Pantalla:** Módulos → Catálogo

**Qué pasa.** En el catálogo, OACE aparece **en gris con la etiqueta «✓ Añadido»**
y no responde al clic. Un módulo que ya está en el cuaderno no se puede volver a
añadir.

**Por qué importa.** Dar el mismo módulo a dos grupos es lo más normal del mundo
en FP, y la propia documentación lo promete: *«Ponle el grupo si das el mismo
módulo a dos clases»* (INSTALACION_Y_USO.md). El campo **Grupo / Clase** existe en
el diálogo de alta, se rellena… y no sirve para lo único para lo que hace falta.

**Cómo reproducirlo.** Módulos → ＋ Añadir módulo → cualquier módulo ya dado de
alta. La tarjeta está atenuada y no se selecciona.

---

## V-2 · Un módulo recién creado llega con las ponderaciones sin cuadrar

**Categoría:** Error confirmado · **Gravedad: Alta**
**Pantalla:** Programación

**Qué pasa.** Nada más dar de alta ISO, sin haber tocado un solo campo:

```
Ponderación del módulo:  Prácticas 60 %  /  Exámenes 70 %   →  130 %
1ª Evaluación   ⚠ suma 130 %     (30 + 30 + 70)
2ª Evaluación   ⚠ suma 160 %     (30 + 30 + 30 + 70)
3ª Evaluación   ⚠ suma 160 %     (30 + 30 + 30 + 70)
```

**Por qué importa.** La aplicación se abre avisando de un error que ella misma ha
creado. Quien no sepa interpretarlo se lo encuentra en las tres evaluaciones y no
sabe si el problema es suyo. Y quien lo ignore está calificando sobre una base que
no suma 100.

---

## V-3 · Los exámenes de arranque no evalúan ningún criterio, y pesan el 70 %

**Categoría:** Error confirmado · **Gravedad: Crítica**
**Pantalla:** Programación → columnas UT · RA · CES

**Qué pasa.** Las tres actividades de examen que trae el módulo —«Examen
Evaluación 1», «2» y «3»— llegan con:

```
UT: —      RA: sin RA      CES: —      PESO: 70 %
```

Es decir: **un instrumento con el 70 % del peso que no está ligado a ningún
resultado de aprendizaje ni a ningún criterio**. Las prácticas sí traen su UT y su
RA; los exámenes, no.

**Por qué importa.** El motor calcula la nota de cada RA a partir de sus criterios.
Una actividad que no cubre ningún criterio, no tiene RA y no cuelga de ninguna UT
no entra en el cálculo de ningún RA. La consecuencia es que **se puede calificar
el examen de toda una evaluación y que esa nota no mueva la calificación del
módulo**, mientras sí aparece en la columna «Media act.» de la parrilla. Dos
números distintos, y el que la profesora mira primero es el que no cuenta.

---

## V-4 · El campo de convocatorias es más estrecho que su propio dígito

**Categoría:** Error confirmado (usabilidad) · **Gravedad: Media**
**Pantalla:** Alumnos → columna «Convoc. · pend.»

**Qué pasa.** El número de convocatorias consumidas **no se lee**: el campo recorta
el dígito y solo se ve un trazo. Al pincharlo para escribir, el control de
incremento ocupa prácticamente todo el ancho, así que el clic sube el valor en
lugar de situar el cursor. En la prueba, un triple clic dejó el contador por
encima de 4 y disparó el aviso de convocatorias agotadas del art. 8.2 sin que
hubiera intención de cambiar nada.

**Por qué importa.** Es un dato normativo —cuatro convocatorias en grado D, dos en
grado E— que la aplicación muestra precisamente para que se pueda vigilar. Si no
se lee, no cumple su función; y si se cambia solo, informa mal.

---

## V-5 · Al dar de alta un módulo, el detalle muestra el anterior

**Categoría:** Error confirmado (interfaz) · **Gravedad: Baja**
**Pantalla:** Módulos

**Qué pasa.** Tras añadir IMRTD, su tarjeta queda marcada y el módulo activo pasa a
ser IMRTD, pero la lista de RA y criterios de debajo sigue titulada **«RAS Y
CRITERIOS DE EVALUACIÓN — OACE»**, con el contenido del módulo anterior. Se repitió
igual al añadir ISO, que mostraba los RA de IMRTD. Pinchando la tarjeta se corrige.

---

## V-6 · Quien no tiene ninguna nota aparece con todos los RA bloqueados — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica**
**Pantalla:** Evaluaciones → 2ª Ordinaria

**Qué pasa.** Los cinco alumnos sin ninguna calificación salían con **🔒 en los
ocho RA**, el candado que marca «aprobado en 1ª, no se vuelve a evaluar». Al
desplegar su ficha, ningún criterio era editable.

**Por qué importa.** A quien no se presentó a nada en junio **no se le podía
recuperar nada en la segunda convocatoria**: la aplicación lo trataba como si lo
tuviera todo aprobado. Es justo el alumnado que más necesita esa convocatoria.

**Causa.** `raNotaOrd2` devolvía la fuente `orig_ok` —la que pinta el candado—
tanto para un RA superado como para un RA **sin nota**: `if (orig === null || (orig
>= 5 && !minKO))`. Un RA sin evaluar no está superado.

**Corregido el 01/08/2026** y comprobado en pantalla: ahora solo lleva candado el
RA que de verdad se aprobó.

## V-7 · El boletín desde Evaluaciones buscaba al alumnado en otro módulo — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta**
**Pantalla:** Evaluaciones → cualquier pestaña con botón de boletín

**Qué pasa.** Al pedir el boletín de la 1ª evaluación de una alumna de ISO, la
aplicación respondía **«Alumno/a no encontrado en este módulo.»**

**Causa.** `_genBoletin` resolvía el módulo con
`dash-mod-sel?.value || eval-mod-sel?.value`. El selector del Dashboard existe en
el DOM aunque no se esté viendo esa pantalla, así que ganaba siempre: se buscaba a
la alumna de ISO entre el alumnado de otro módulo. Afectaba también al botón que
ya existía en la 1ª Ordinaria.

**Corregido el 01/08/2026**: manda el selector de la sección visible.

## V-8 · Marcar los criterios de un examen son 27 clics

**Categoría:** Mejora recomendada · **Gravedad: Media**
**Pantalla:** Programación → botón de criterios

Un examen que cubre dos unidades ofrece 27 criterios y hay que marcarlos **uno a
uno**: no hay «marcar todos» ni «todos los de este RA». Es la tarea más repetitiva
de la programación y la que más se abandona a medias — y abandonarla es
exactamente lo que produce el V-3.

---

## Resumen

| | Incidencia | Gravedad | Estado |
|---|---|---|---|
| V-1 | Un módulo no se puede dar de alta para dos grupos | Alta | Corregida |
| V-2 | Ponderaciones sin cuadrar en un módulo recién creado | Alta | Corregida |
| V-3 | Exámenes con el 70 % del peso que no evalúan nada | **Crítica** | Corregida |
| V-4 | Campo de convocatorias ilegible e inmanejable | Media | Corregida |
| V-5 | El detalle de Módulos va un módulo por detrás | Baja | Corregida |
| V-6 | RA sin nota bloqueados en la 2ª convocatoria | **Crítica** | Corregida |
| V-7 | Boletín desde Evaluaciones con el módulo equivocado | Alta | Corregida |
| V-8 | Sin «marcar todos» en los criterios de una actividad | Media | Corregida |
| V-9 | El botón «Acerca de» no respondía al clic | Baja | Corregida |

**Lo que confirma esta segunda vuelta.** La auditoría de código encontró errores de
cálculo; esta encuentra otra familia distinta: **la aplicación calcula bien lo que
se le da, pero deja llegar a la pantalla de notas un módulo que no está listo para
calificar**, y no avisa. V-2 y V-3 juntos significan que alguien puede dar un curso
entero calificando exámenes que no cuentan.

*Auditoría realizada manejando EvalFP 3.8.0 en el equipo, con dos módulos dados de
alta desde cero. Los módulos de prueba llevan los grupos AUD-1A y AUD-2A.*


---

## Correcciones del 01/08/2026

- **V-1.** `modulos.key` era única. Migración a **UNIQUE(key, grupo)**, recreando
  la tabla con el procedimiento de SQLite (claves foráneas apagadas, dentro de
  transacción y con `foreign_key_check` antes de confirmar). La tarjeta del
  catálogo pasa a decir «✓ Ya lo tienes» y se puede seleccionar; al añadir se
  pide el grupo y se rechaza solo el duplicado exacto módulo+grupo. Comprobado
  sobre una base con el esquema antiguo: conserva el alumnado.
- **V-2 y V-3.** `prebake_modules.py` genera ahora cada evaluación sumando 100 %
  —las prácticas se reparten el 30 % y el examen se lleva el 70 %—, el examen
  cuelga de las UT de su evaluación y **ninguna actividad nace sin criterios**.
  Verificado en los 91 módulos: 800 actividades, ninguna sin criterios y ninguna
  evaluación fuera del 100 %. `addModulo` no guardaba la columna `ces`, así que
  además los perdía al dar de alta el módulo.
- **V-4.** El campo de convocatorias pasa a ser un desplegable de 0 al tope, que
  se lee y no se puede desbordar con el ratón.
- **V-5.** El alta repinta también el panel de RA y criterios.
- **V-8.** Botones «todos» y «ninguno» por RA en el modal de criterios.

**Nota.** V-1 necesita **reiniciar EvalFP** una vez: la migración de la base la
hace el proceso principal al abrir, no basta con recargar la ventana.


## V-9 · El botón «Acerca de» no respondía — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Baja**
**Pantalla:** barra lateral, pie

La barra lateral entera lleva `-webkit-app-region: drag` para poder mover la
ventana arrastrándola, y esa zona **se traga los clics** de lo que tenga encima.
Los `.nav-item` lo anulaban uno a uno; el pie de la barra, no, así que el botón
«Acerca de» no hacía nada.

Es exactamente el mismo fallo que dejó sin respuesta los ciclos del catálogo en
la auditoría de julio. Corregido en la raíz: se exime del arrastre **todo lo que
se pulsa** dentro de la barra —botones, campos, enlaces y cualquier elemento con
`onclick`—, en vez de ir anulándolo elemento a elemento, que es como se llega a
este fallo una y otra vez.


---

## Las tres familias, cerradas de raíz

Los fallos de esta auditoría no eran ocho casos sueltos: eran **tres patrones**
repitiéndose. Cerrarlos uno a uno es lo que hizo que volvieran. Ahora cada
patrón tiene su guarda.

**1 · Zonas de arrastre que se tragan los clics.** Ha pasado dos veces —los
ciclos del catálogo y el botón «Acerca de»—. Las tres zonas con
`-webkit-app-region: drag` eximen ya todo lo pulsable que contienen, y
`handlers.test.js` falla si se añade una zona nueva sin eximirlo.

**2 · Veredictos decididos con un booleano.** El art. 12 tiene tres estados y un
ternario solo sabe expresar dos: el «superado parcial» acababa saliendo como NO
APTO. Ninguna pantalla decide ya la etiqueta con un booleano. Y en el boletín de
trimestre, una media de 6 con un RA suspenso deja de pintarse en verde.

**3 · Pantallas que se calculan sus propios números.** Siete sitios distintos
promediaban los criterios de la 2ª convocatoria a peso igual, ignorando la
ponderación del art. 4.3.a, y ninguno veía las actividades de recuperación: el
último era el informe de la IA, que citaba una nota que no coincidía con el acta.
`motor-unico.test.js` falla ahora si alguien vuelve a promediar criterios a mano.


---

## Segunda tanda · lo que salió al probar los estados raros

## V-10 · La renuncia a convocatoria era imposible de registrar — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Alta** · **Pantalla:** Alumnos

Poner a alguien en **Renuncia** devolvía «Error: Ha ocurrido un error. Inténtalo
de nuevo» y el estado volvía atrás. La baja sí funcionaba.

El mismo dato estaba escrito en tres sitios: el desplegable de la interfaz, el
validador del renderer y `preload.js`. Al añadir el estado «Renuncia» se
actualizaron los dos primeros y **no el tercero**, que seguía comprobando contra
`['Activo','Pendiente','Baja']` y cortaba el guardado con «estado inválido». La
renuncia del art. 11 —que en actas figura como RC, art. 25.9— no se podía usar.

Corregido, y con un test que compara las tres listas: si una se queda atrás,
falla. El mensaje real solo se pudo leer gracias al registro en consola que se
añadió esta misma mañana; antes se perdía en un «ha ocurrido un error».

## V-11 · La aplicación pedía tipografías a Google en cada arranque — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Media** · **Pantalla:** todas

La hoja de estilos empezaba con un `@import` a `fonts.googleapis.com`. Dos
problemas a la vez:

1. **No funcionaba.** La propia CSP de la aplicación lo bloqueaba —«violates the
   following Content Security Policy directive: style-src 'self'»— así que las
   tipografías nunca llegaban y se veía la de respaldo, dejando dos errores en la
   consola en cada arranque.
2. **Contradecía lo que el cuaderno promete.** «Sin cuenta, sin nube y sin
   conexión: tus datos no salen del ordenador» — y arrancaba llamando a un
   servidor de Google.

Sustituido por la pila tipográfica del sistema. La consola queda **sin un solo
aviso**.

## V-12 · Las novedades del «Acerca de» se quedaron cinco versiones atrás — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Baja** · **Pantalla:** Acerca de

El modal de la 3.9.0 seguía presumiendo del instalador y del propio modal, que
son novedades de la 3.3.1: la lista estaba escrita a mano en `main.js`. Ahora se
lee del CHANGELOG, que es lo único que se actualiza siempre.

---

### Comprobado y correcto

- **Baja a mitad de curso**: conserva las notas, sale separada del alumnado activo
  y con «Matrícula anulada · sin evaluación», sin acta (art. 7.1).
- **Renuncia**: figura como **RC · renuncia a convocatoria**, sin calificación.
- **Archivar y restaurar un módulo**: ISO volvió con sus seis alumnos y sus notas.
- **Numeración del alumnado importado**: correlativa, 1 a 6.


## V-13 · El cierre de evaluación no protegía en la pestaña del trimestre — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Crítica**
**Pantalla:** Evaluaciones → 1ª / 2ª / 3ª Evaluación

**Qué pasa.** Con la 1ª evaluación cerrada y el aviso «🔒 2 RA fijados» a la
vista, se baja una práctica de un 8 a un 1 y el RA de esa alumna **cae de 7,3 a
2,8**, apareciendo además como pendiente. El botón de cierre promete literalmente
que «una actividad posterior no podrá bajarlos».

**Causa.** La congelación se aplicaba en 1ª y 2ª Ordinaria —que construyen el
contexto con `rasSuperados`— pero las tablas de la evaluación parcial llamaban
directamente a `notaRA` sin ese contexto. Es el error A-2 de la primera
auditoría sobreviviendo en la pantalla donde más se mira durante el curso.

**Corregido**: la nota de un RA fijado no baja en ninguna de las tablas, lleva su
candado y deja de contarse como pendiente. Comprobado en la aplicación: tras
bajar la nota, el RA vuelve a 7,3 🔒 y el boletín del trimestre a 7,1.

## V-14 · La renuncia se etiquetaba como baja en las evaluaciones — **CORREGIDO**

**Categoría:** Error confirmado · **Gravedad: Media**
**Pantalla:** Evaluaciones → pestañas de evaluación parcial

Las tablas usaban una etiqueta fija de «BAJA» para todo el alumnado no activo, así
que quien había renunciado a la convocatoria figuraba como baja. Son dos cosas
distintas y en el acta se reflejan distinto (RC, art. 25.9). Ahora cada fila
muestra su estado real.


## V-15 · La prueba de recuperación se etiquetaba «EV1» en la parrilla — **CORREGIDO**

**Categoría:** Mejora recomendada · **Gravedad: Baja** · **Pantalla:** Notas

Las actividades de recuperación se guardan con `eval = 1` por dentro, así que la
cabecera de su columna decía «EV1» y parecían de la primera evaluación. Ahora
ponen **«2ª conv.»**.

---

## V-16 · El Asistente IA se calculaba sus propias notas — **CORREGIDO**

**Categoría:** Fallo grave · **Gravedad: Alta** · **Pantalla:** Asistente IA

Con una alumna que había recuperado el RA1 en la 2ª convocatoria, Evaluaciones
decía **7,0** y el informe de la IA se autorrellenaba con **2,6** más una entrada
fantasma «RA1_EX:2.0». Eran dos motores paralelos más:

- el informe individual y el plan de recuperación se calculaban las notas por RA
  a mano, sin ver las pruebas de recuperación (art. 21.5) ni los RA cerrados
  (art. 4.3.f);
- la radiografía del grupo y «Todo el módulo» las calculaban en Python con una
  media aritmética de las notas crudas: sin el peso de cada actividad y sin la
  escala del instrumento, así que un 18 sobre 20 valía 18.

Ahora las cuatro usan `contextoModulo` + `estadoModulo`, y la aplicación manda a
Python las notas por RA ya hechas (`--notas-ra-json`). Comprobado: el informe de
la alumna pasó a decir **RA1:7,0 · RA2:4,0**, los mismos números del acta.

---

## V-17 · No dejaba hacer un informe a mitad de curso — **CORREGIDO**

**Categoría:** Fallo grave · **Gravedad: Media** · **Pantalla:** Asistente IA

«Faltan calificaciones en algunos Resultados de Aprendizaje» cortaba la
generación en seco. En diciembre faltan casi todos: el informe de trimestre era
imposible. Ahora es un aviso, el informe se redacta con lo evaluado, la nota se
presenta como parcial y los RA que aún no se han trabajado se citan como tales
para que la IA no los dé por suspensos.

---

## Curso completo, comprobado en la aplicación

- **Cierre de evaluación**: fija los RA alcanzados, los marca con candado y
  aguanta que se baje una nota después (V-13).
- **Boletín de trimestre**: la media acumulada y los RA pendientes cuadran con la
  tabla por RA.
- **2ª convocatoria con actividades (A-5)**: la prueba de recuperación subió a una
  alumna el RA1 de **2,6 a 7,0**, y siguió pendiente por el RA2, que no estaba
  entre los criterios de esa prueba. Es exactamente el comportamiento que exige
  la regla de oro.
- **Alumnado de baja y con renuncia**: separado, sin acta y con su etiqueta.
- **Asistente IA con datos reales**: informe individual y radiografía del grupo
  generados contra la API, con las notas del motor único.

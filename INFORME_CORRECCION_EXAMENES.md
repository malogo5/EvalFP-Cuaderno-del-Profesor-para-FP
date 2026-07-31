# Corregir exámenes desde foto

La pestaña **🖊️ Corregir desde foto** del Asistente IA lee las fotos de un examen
manuscrito, lo corrige contra los criterios de evaluación del decreto y devuelve el
feedback, las fotos marcadas y una **propuesta** de nota.

## De dónde sale

De tu propio material, no de cero:

- El **prompt maestro de corrección de ProfeLibre** (`Prompt_Maestro_Correccion_Y_Guía_De_Uso`),
  cuyos principios innegociables se han traducido a las reglas del sistema del corrector.
- El **skill `corregir-examen`**, del que se han integrado tal cual sus dos herramientas:
  `scripts/corregir/preprocesar_imagen.py` y `scripts/corregir/anotar_examen.py`.

## Los principios, y cómo los cumple la aplicación

| Principio | Cómo se aplica aquí |
|---|---|
| La rúbrica es la única referencia | La rúbrica son los criterios de evaluación **literales del DOCM** del RA que elijas. El modelo tiene prohibido añadir criterios propios. |
| No mezclar alumnos | Una llamada por examen, con las páginas de una sola persona. No hay contexto compartido entre alumnos. |
| No inventar | Lo ilegible va como `[ilegible]`, lo ambiguo como `[dudoso]`, y distingue «en blanco» de «no legible». Lo que no ha podido resolver y afecta a la nota te lo devuelve en «Dudas que debes resolver tú». |
| Anonimización | Por defecto se refiere al alumnado por número de lista (`Alumno_03`). Puedes desactivarlo. |
| Fotos originales en color | El preprocesado en gris y alto contraste se hace en una carpeta temporal **solo para leer**; las marcas se superponen siempre sobre tus fotos originales. |
| Rigor pedagógico | Prohibidas «muy bien», «sigue así», «ánimo». Feedback en los cuatro bloques: puntos fuertes específicos, UN aspecto a mejorar con el ejemplo de su examen, dos a cuatro acciones para esta semana y nota con desglose. |
| Transcripción mínima | Solo se transcribe cuando la cita es la evidencia de un acierto o de un error. |

## Qué te deja

En `Documentos/EvalFP/correcciones/<MÓDULO>_<RA>/`:

- `correccion_Alumno_NN.json` — la corrección estructurada: pregunta a pregunta, con los
  criterios acreditados y los que no.
- `correccion_Alumno_NN.md` — el documento de entrega.
- Las fotos con las marcas: ✓ verde, ✗ roja con la corrección, ~ naranja para lo incompleto
  y comentarios en azul al margen.

## La nota no entra sola

El corrector devuelve una **propuesta**. Aparece en un recuadro con un selector de actividad
y un botón; hasta que no lo pulsas, no se escribe nada en el cuaderno. Es deliberado: una nota
la pone una persona.

## Toda la clase de una vez

En la misma pestaña, debajo, está el bloque de tanda completa. El orden es deliberado:

1. **Eliges todas las fotos** del grupo de una sola vez.
2. **Verificas el reparto.** Se agrupan por el número del nombre del archivo
   (`01_p1.jpg`, `A07_2.png`…) o por número fijo de páginas, y se te muestra la tabla:
   qué fotos son de cada examen y **qué no cuadra** («esperaba 4 páginas y veo 3»).
   Este paso **no envía nada ni cuesta nada**: es la red de seguridad contra el peor
   error posible, mezclar producciones de dos alumnos.
3. **Asignas alumno a cada examen**, a mano o con «asignar por orden de lista».
4. **Corriges el primero** y lo lees. Si el criterio no te encaja, escribes los ajustes
   («más estricto con las unidades», «el feedforward más corto») y se aplican a todos
   los siguientes: es la calibración de tu prompt maestro, sin fases de chat.
5. **Corriges el resto** y revisas la tabla final de notas propuestas, con casillas para
   marcar cuáles aceptas y un solo botón para guardarlas.

Mientras corre la tanda ves el contador («corrigiendo 7 de 25») y puedes **pausar**: el examen
que ya está enviado termina y se guarda, y la cola se queda esperando con las que faltan. Al
reanudar sigue por donde iba. Si prefieres dejarlo ahí, «dejarlo aquí» vacía la cola sin perder
nada de lo ya corregido: sigues pudiendo guardar esas notas.

En lugar de las tandas fijas de cinco del prompt maestro, aquí la tanda es continua y se
corta cuando tú quieras: en una aplicación no hay contexto compartido que administrar —cada
examen es una llamada aislada, que es justo lo que garantiza no mezclar alumnado—, así que
partir en grupos de cinco solo añadiría clics. Lo que sí hacía falta era poder respirar a
mitad, y para eso está la pausa.

## Consejos de uso

- **Pega el enunciado o el solucionario** en su campo: es lo que más mejora la corrección.
- Elige las páginas **de un solo alumno y en orden**. Máximo 12 páginas por examen.
- Empieza corrigiendo **un examen representativo** y mira si el criterio te encaja antes de
  seguir con el resto: es la fase de calibración de tu prompt maestro, aquí a mano.
- Si las fotos vienen de iPhone en HEIC y no se leen bien, conviértelas antes a JPG.
- El preprocesado usa ImageMagick si lo tienes instalado; si no, se lee la foto original.

# Instalación y uso de EvalFP

EvalFP es un cuaderno del profesor para Formación Profesional, con el catálogo de módulos
de Castilla-La Mancha y los criterios de evaluación literales del DOCM. Funciona en macOS
y en Windows, sin cuenta, sin nube y sin conexión: tus datos no salen del ordenador.

Este documento es para **usar** la aplicación. Para construir los instaladores desde el
código, mira `DISTRIBUCIONES.md`.

## Instalar en macOS

1. Abre el archivo `EvalFP-<versión>-arm64.dmg` (Apple Silicon) o `EvalFP-<versión>.dmg` (Intel).
2. Arrastra **EvalFP** a la carpeta **Aplicaciones**. Si ya tenías una versión, sustitúyela.
3. Ábrela desde Aplicaciones o con Spotlight.

La aplicación no está firmada con certificado de Apple, así que la primera vez macOS avisa
de que «no se puede comprobar el desarrollador». Ábrela con **clic derecho → Abrir**, o ve a
**Ajustes del Sistema → Privacidad y seguridad** y pulsa *Abrir de todos modos*. Solo hace
falta la primera vez.

Si la tenías en el Dock, quita el icono antiguo y vuelve a arrastrar la app: el acceso del
Dock sigue apuntando a la copia anterior aunque la hayas sustituido.

## Instalar en Windows 11

1. Ejecuta `EvalFP Setup <versión>.exe`.
2. Windows enseña la pantalla azul de SmartScreen porque el instalador no está firmado:
   pulsa **Más información → Ejecutar de todas formas**.
3. Elige la carpeta de instalación y deja marcados los accesos directos si los quieres.
4. Abre EvalFP desde el menú Inicio.

El mismo `.exe` sirve para cualquier Windows 11: puedes copiarlo a otro equipo sin repetir
nada.

## Python: solo para la IA y el Excel

El cuaderno entero —módulos, alumnado, notas, evaluaciones, actas, boletines— funciona sin
instalar nada más. Pero el **Asistente IA**, la **corrección de exámenes desde foto** y la
exportación a Excel usan scripts de Python que la aplicación llama por debajo, y Python no
viene dentro del instalador.

Si vas a usarlos, instala **Python 3.10 o superior** (en Windows, desde python.org marcando
*Add python.exe to PATH*) y luego, en una terminal:

```
pip install openpyxl anthropic openai
```

`openpyxl` es para el libro de Excel; `anthropic` y `openai` son los dos proveedores de IA
—con instalar el que vayas a usar es suficiente—. La lista completa está en
`requirements.txt`, dentro de la carpeta `resources` de la aplicación instalada.

## Las claves de IA

Se configuran en **Ajustes**, y son tuyas y de pago: se generan en
console.anthropic.com (Claude) o platform.openai.com (GPT), con saldo en la cuenta.

Se guardan en el llavero del sistema —Keychain en macOS, Credential Manager en Windows—,
nunca en el código ni en la base de datos, y los campos aparecen siempre vacíos al volver a
Ajustes: verás «✓ configurada», no la clave.

Sin claves, el asistente responde en **modo demo**: genera textos de ejemplo para que veas
el formato, sin llamar a ningún servicio.

Para leer letra manuscrita en la corrección de exámenes, Claude da bastante mejor resultado.

## Dónde viven tus datos

Todo está en un único archivo de base de datos, fuera de la aplicación:

| Sistema | Carpeta |
|---|---|
| macOS | `~/Library/Application Support/EvalFP/evalfp.db` |
| Windows | `%APPDATA%\EvalFP\evalfp.db` |

Que esté fuera tiene dos consecuencias buenas: **instalar una versión nueva encima no borra
nada**, y para llevarte el cuaderno a otro ordenador basta con copiar ese archivo a la misma
ruta del equipo de destino (con la aplicación cerrada en los dos).

Lo que la aplicación genera —informes, apuntes, boletines, correcciones— va a
`Documentos/EvalFP`, en subcarpetas por tipo (`Material IA`, `boletines`, `apuntes`,
`correcciones`).

## Copias de seguridad

Se hacen solas: **una diaria a las 2:00** y otra **cada vez que cierras la aplicación**. Se
guardan como `evalfp_<fecha>.db` en la subcarpeta `backups` de la carpeta de datos, y las de
más de 30 días se borran para no acumular.

En **Ajustes** ves cuántas hay y de cuándo es la última, puedes abrir la carpeta y puedes
crear una **a demanda** — conviene antes de tocar algo delicado, como rehacer la
programación de un módulo.

Para restaurar: cierra la aplicación, sustituye `evalfp.db` por la copia que quieras
(quitándole la fecha del nombre) y vuelve a abrir.

## Cómo se trabaja un curso

1. **Módulos → ＋ Añadir módulo.** Elige el ciclo en el menú de la izquierda y el módulo en
   las tarjetas. Llega con sus RA, sus criterios literales del decreto, sus unidades de
   trabajo y unas actividades de partida. Ponle el grupo si das el mismo módulo a dos clases.
2. **Alumnos.** Pega la lista de clase entera de una vez, un nombre por línea; separa solo
   apellidos y nombre. Quien cause baja se marca como tal y deja de contar en las medias,
   pero no desaparece.
3. **Programación.** Es la base de la que come todo lo demás: reparte las unidades por
   evaluación, ajusta horas y ponderaciones, y decide **qué criterios evalúa cada actividad**
   con el botón de CE. Los avisos en ámbar (`⚠ suma 130%`) señalan lo que no cuadra.
4. **Notas.** La parrilla de siempre. Se guarda al salir de cada celda.
5. **Evaluaciones.** Resultado por evaluación, 1ª y 2ª ordinaria, y la columna de acta con el
   redondeo normativo. Rige la **regla de oro**: para superar el módulo hacen falta *todos*
   los RA con 5 o más; la media no compensa un RA suspenso.
6. **Dashboard.** Vista de clase y boletines individuales en PDF.
7. **Asistente IA** (opcional). Rúbricas, actividades, informes de alumno, planes de
   recuperación, radiografía del grupo, pruebas escritas con solucionario, apuntes y
   corrección de exámenes desde foto.

## La IA no pone notas

Todo lo que genera el asistente es un **borrador que tú revisas**. La corrección desde foto
devuelve una *propuesta* de nota que no entra en el cuaderno hasta que pulsas el botón, y en
la corrección por lotes se te enseña primero qué fotos son de cada alumno para que lo
verifiques antes de enviar nada. Una nota la pone una persona.

Antes de enviar nada a un proveedor de IA, la aplicación pide consentimiento y ofrece
**anonimizar**: el alumnado viaja como «Alumno_03», no con su nombre.

## Buenas prácticas

- Revisa de vez en cuando en Ajustes que las copias se están haciendo.
- Antes de rehacer la programación de un módulo en marcha, crea una copia a demanda.
- Si compartes capturas o exportaciones, comprueba que no llevan datos identificativos.
- Mantén una sola copia instalada por equipo: dos versiones distintas de la aplicación
  comparten la misma base de datos y es fácil perderse.

## Licencia

EvalFP se distribuye bajo licencia GPLv3 o posterior.

# Changelog

## [3.3.2] - 2026-07-31

### Fixed
- **La 2ª convocatoria vuelve a cuadrar con la 1ª.** Tres fallos encadenados en el mismo panel:
  - **El mínimo de examen dejaba de aplicarse.** Un RA suspenso en junio por tener el examen bajo
    el mínimo aparecía superado en la segunda convocatoria **sin haber recuperado nada**, y el
    alumno pasaba de NO APTO a APTO. Ahora el mínimo se sigue exigiendo y deja de bloquear solo
    cuando se acreditan todos los criterios del RA.
  - **La nota del RA se calculaba sobre bases distintas**: en junio, los criterios evaluados; en la
    segunda, todos los del decreto. Como marcar un criterio como aprobado devuelve un 5, perdonar
    criterios que **nadie evalúa** subía la nota (3,00 → 4,00 en el caso reproducido) sin haber
    recuperado ninguno de los suspensos. Las dos convocatorias usan ya el mismo conjunto:
    `cesEvaluadosDeRa()`.
  - **Los criterios sin instrumento eran invisibles pero computaban.** Ahora se muestran atenuados
    con la marca «sin instrumento» y no se pueden calificar ni dar por aprobados hasta que se les
    asigne una actividad en Programación.
- **A la 2ª convocatoria concurre también quien tiene RA sin nota** (no presentado), que antes se
  quedaba fuera de la lista siendo quien más la necesitaba.
- **Los indicadores de la cabecera de la 2ª ordinaria** se refieren ya al mismo grupo: antes «Con
  recuperación» contaba a unos y «Superan 2ª / Media» a todo el alumnado activo.

### Added
- **`AUDITORIA_INTEGRAL.md`**: auditoría de la aplicación completa contra la Orden 201/2024 de
  Castilla-La Mancha, el RD 659/2023 y la LOFP, con 21 incidencias clasificadas y un plan de
  corrección en tres fases.

## [3.3.1] - 2026-07-31

### Changed
- **La versión del proyecto pasa a 3.3.1** (estaba clavada en la 3.0.0 de julio, que es lo que
  mostraba la app y lo que nombraba los instaladores).
- **`DISTRIBUCIONES.md`**: cómo reconstruir el `.dmg` y el `.exe`, y por qué el instalador de
  Windows sale mejor desde una máquina Windows que desde macOS con Wine.


### Fixed
- **Los modales dejaban de responder al ratón de cierta altura para abajo.** El lateral de la app
  es zona de arrastre de la ventana (`-webkit-app-region: drag`) y sus botones la anulan uno a uno,
  pero el hueco vacío bajo el último botón sigue siendo arrastrable. Cualquier diálogo abierto
  encima perdía los clics de esa franja, que macOS se quedaba para mover la ventana: en el catálogo
  eso dejaba muertos justamente los cuatro ciclos de Administración y Gestión. Los diálogos pasan a
  `no-drag` salvo su cabecera. (No lo cazaban los tests: Playwright inyecta los clics en el
  renderizador y se salta el reparto de zonas de arrastre del sistema.)
- **El catálogo enseña cuántos módulos trae cada ciclo** y avisa, si uno está vacío, de que la copia
  empaquetada de la aplicación es más antigua que el catálogo.
- **Los criterios de evaluación ya no se confunden entre resultados de aprendizaje.** Los decretos
  numeran los criterios dentro de cada RA (RA1 tiene CR1…CR10 y RA2 vuelve a empezar por CR1), pero
  las actividades los guardaban con el id suelto: cualquier actividad con «CR1» contaba en el CR1
  de **todos** los RA del módulo. En una prueba con notas 9, 3, 8, 4, 7, 2 y 10 en siete RA, los
  siete salían ~6,1. Los criterios pasan a la clave compuesta `RA|CE` —la misma que ya usaban
  perdones y notas de 2ª ordinaria— y las actividades guardadas se traducen solas al abrir la app.
- **La evaluación de cada RA es ya la misma en toda la app.** El reparto por trimestres estaba
  congelado en el catálogo y no seguía a las UT: mover una unidad de evaluación dejaba el Plan de
  Actividades, la Distribución de RAs y la ficha del RA diciendo cosas distintas.
- **Una UT con dos RA ya no pierde el segundo** en la distribución, en el reparto de pesos del
  dashboard, al asignar UT a una actividad ni en el modal de UT del examen.
- **Un RA evaluado solo con un examen de varias unidades vuelve a aparecer** en Evaluaciones (antes
  hacía falta un `ra_id`, que un examen multiunidad no puede tener) y por tanto vuelve a entrar en
  la regla de oro.
- **El modal de RA/CE muestra lo guardado.** Un RA asignado sin criterios ya no aparece con todos
  marcados; guardar uno sin ninguno pide confirmación, porque así no evalúa nada.
- **En el modal de criterios de una actividad, cada casilla es la suya**: en un examen sobre dos RA,
  marcar el CR1 de uno ya no marca el del otro.
- **Cambiar o borrar la UT de una actividad recoloca su RA y sus criterios**, en vez de dejarlos
  huérfanos calificando un RA que ya no toca; se avisa de cuántos se han quitado.
- **Las horas de las UT se comparan con las horas de aula** en los módulos con formación en empresa
  (Grado Básico): el aviso estaba siempre en ámbar.
- **Vaciar la ponderación de un RA ya no da error**: significa que aún no está ponderado.
- **Los informes de IA ya no se saltan los exámenes de varias unidades** al agrupar notas por RA.

Detalle y reproducción en `INFORME_COHERENCIA_RA_CE.md`.

## [3.3.0] - 2026-07-30

### Changed
- **Todo el catálogo pasa a los decretos de currículo de Castilla-La Mancha.** Los 42 módulos de
  Informática y los 10 de las especializaciones tenían RA y CE adaptados del Real Decreto estatal:
  solo el 18 % del texto coincidía con el DOCM y 28 de ellos tenían incluso distinto número de RA.
  Regenerados con el texto literal del decreto autonómico; los 4.351 criterios de los 87 módulos
  con decreto están verificados uno a uno contra el PDF oficial (100 %).
- **Grado Básico: se separan la duración oficial y las horas de aula.** El total que publica la
  Consejería incluye la formación en empresa (338 h a 8 h/semana serían 42 semanas). Nuevo campo
  `horas_aula`, que es el que reparten las UT; la app muestra las dos cifras.
- **CE Ciberseguridad**: BRS 180 → 185 h y NC 60 → 55 h (Anexo I del Decreto 77/2022).
- **CE IA y Big Data**: el curso son 600 h, no 720. SAA 120 → 100, PIA 180 → 200, SBD 90 → 100 y
  BDA 120 → 140 (Anexo I del Decreto 69/2022).

### Changed
- **El generador de informes ya sabe de qué habla.** Al prompt solo le llegaban números
  (`RA1: 7.5`), sin el enunciado de los resultados de aprendizaje ni los criterios, así que la IA
  únicamente podía escribir prosa genérica. Ahora recibe el enunciado literal de cada RA, los
  criterios de evaluación del DOCM de los que no ha superado, en qué unidades de trabajo se
  trabajan y las notas actividad a actividad del alumno o alumna. El informe pasa de «sigue
  esforzándote en RA3» a explicar qué se esperaba y cómo recuperarlo.
- **Modelo según la tarea.** Informes y planes —lo que leen las familias y sostiene una
  reclamación— con el modelo capaz; rúbricas y listados con el económico.
- **Timeout de 15 s a 30 s (90 s en textos largos) y un reintento** ante corte de red: una
  generación cuidada no cabía en quince segundos y se perdía el trabajo.

### Added
- **Corrección de exámenes manuscritos desde foto** (pestaña «Corregir desde foto»): lee las
  páginas, corrige contra los criterios literales del decreto, devuelve feedback en cuatro
  bloques, marca las fotos originales en color y **propone** una nota que solo entra en el
  cuaderno si el profesorado pulsa el botón. Construida sobre el prompt maestro de corrección de
  ProfeLibre y las herramientas del skill `corregir-examen`, cuyos principios se respetan:
  rúbrica única, no mezclar alumnado, no inventar (`[ilegible]` / `[dudoso]`), anonimización por
  número de lista, entrega siempre con las fotos originales y feedback sin frases vacías.
  Detalle en `INFORME_CORRECCION_EXAMENES.md`.
- **Corrección por lotes de toda la clase**, con dos salvaguardas: el reparto de fotos por
  alumno se **verifica en pantalla antes de enviar nada** (agrupación por número en el nombre
  del archivo o por páginas fijas, señalando lo que no cuadra), y el criterio se **calibra**
  corrigiendo el primer examen: los ajustes que escribas se aplican a todos los siguientes,
  para que el alumno 1 y el 25 se corrijan con la misma vara de medir. Al final, tabla de notas
  propuestas con casillas y un único botón para guardar las aceptadas. La tanda se puede
  **pausar y reanudar**: el examen en curso termina y se guarda, la cola espera, y al reanudar
  continúa por donde iba.
- **Tres generadores nuevos que usan los datos del cuaderno**, no solo el catálogo:
  - **Plan de recuperación** por alumno o alumna, con SOLO los resultados de aprendizaje que le
    quedan: qué tiene que llegar a hacer, qué repasar y dónde, tareas de práctica, cómo se le
    evaluará y un calendario por semanas.
  - **Radiografía del grupo**: qué RA y qué actividades han ido peor en toda la clase y qué
    reforzar. Los porcentajes y las medias se calculan en el ordenador y la IA solo los
    interpreta, así que las cifras del documento son siempre las de la aplicación.
  - **Prueba escrita con solucionario** a partir de los criterios literales del decreto:
    enunciado con los criterios que evalúa cada pregunta, solucionario con errores frecuentes y
    baremo por criterio que suma 10.
- **Copias de seguridad visibles en Ajustes.** La aplicación ya hacía copia cada día y al
  cerrarse, y conservaba 30 días, pero no había forma de saberlo ni de usarlas: si la base de
  datos se estropeaba, el profesorado no llegaba a enterarse de que existían. Ahora se ve cuántas
  hay, de cuándo es la última y en qué carpeta, con botones para crear una al momento y abrir la
  carpeta, y con las instrucciones para restaurar.
- **Auditoría de usuario de curso completo** (`npm run test:auditoria`): recorre la interfaz real
  como lo haría una profesora de septiembre a la 2ª ordinaria —alta de módulos desde el catálogo,
  lista de clase, tres evaluaciones, recuperaciones, actas, boletines, cambio de módulo, ajustes—
  y deja informe en `tests/e2e/AUDITORIA_CURSO.md` y una captura por fase. 64 comprobaciones.
  Incluye la prueba de fuego de la regla de oro: media aprobada con un RA suspenso ⇒ NO APTO.
- `scripts/regenerar_desde_clm.py`: rehace un módulo con los RA y CE literales de su decreto,
  conservando sigla, código, curso, horas, evaluaciones e instrumentos.
- `scripts/aplicar_horas_aula.py`: calcula las horas de aula de Grado Básico a partir de las
  semanas reales del curso, deducidas de los ámbitos (30 en 1º, 25 en 2º).
- Decretos en `normativa/`: 107/2009 (SMR), 200/2010 (ASIR), 230/2011 (DAW), 252/2011 (DAM),
  80/2014 (CFGB Informática de Oficina), 77/2022 (Ciberseguridad), 69/2022 (IA y Big Data) y
  78/2024 (Grado Básico, del que sale el módulo IPE).

### Fixed
- El parser del DOCM no reconocía los marcadores `ll)` y `ñ)` del alfabeto español ni toleraba
  que un decreto se saltase una letra (el 80/2014 va de `e)` a `g)` en un RA).
- La limpieza de guionado unía palabras separadas por un guion de inciso («consumibles - tintas»).
- El Decreto 69/2022 coloca los marcadores en una columna aparte; se extrae con `pdftotext -raw`
  para no perder 16 criterios.

## [3.2.0] - 2026-07-30

### Added
- **33 módulos nuevos de la familia Administración y Gestión** con RA y CE literales del DOCM:
  Servicios Administrativos (Decreto 83/2014), Gestión Administrativa (Decreto 251/2011),
  Administración y Finanzas (Decreto 43/2013) y Asistencia a la Dirección (Decreto 41/2013).
  El catálogo pasa de 58 a 91 módulos en 12 ciclos.
- `scripts/parse_docm.py`: extractor de RA y CE literales del texto de un decreto del DOCM, con
  soporte de los marcadores `ll)` y `ñ)` del alfabeto español y limpieza del guionado del PDF.
- `scripts/mezclar_meta.py`: une el texto del decreto con la capa didáctica (UT, siglas, horas).
- `scripts/gen_modulo.py`: genera los `*_data.py` con horas de UT y ponderaciones cuadradas.
- `scripts/corregir_catalogo.py`: alinea código, duración, horas semanales y curso con la tabla
  oficial de la Consejería, reescalando las horas de las UT.
- `scripts/validar_catalogo.py`: validación de coherencia de todo el catálogo prebakeado.
- `normativa/`: PDF y texto de los decretos, JSON crudos por ciclo y tabla oficial de Informática.

### Fixed
- **`prebake_modules.py` dejaba RA sin actividad de partida**: cuando una UT trabajaba criterios
  de dos RA, solo generaba práctica para el primero. Afectaba a 11 RA de DAM, DAW, ASIR y CFGB.
  Ahora crea una práctica por cada par UT–RA.
- **Códigos de módulo mal asignados** en DAM (9 módulos), DAW (3) y SMR (4 intercambiados entre
  sí), corregidos según la tabla oficial del ciclo.
- **Duraciones y horas semanales** de 36 módulos de Informática, que venían de los mínimos del
  Real Decreto en lugar de la distribución vigente de CLM (p. ej. OACE 210 → 338 h).
- **Dos módulos de SMR tenían un RA huérfano** sin ninguna UT que lo trabajase: 0226 Seguridad
  informática (RA5) y 0227 Servicios en red (RA4). Añadida la UT que faltaba en cada uno.
- `AO` Aplicaciones ofimáticas pasa a 2º de SMR y `AW` Aplicaciones web a 1º, como marca la
  distribución oficial.
- Los tests unitarios ya no se caen cuando el Node del sistema no expone `node:sqlite`:
  `vitest.config.js` añade `--experimental-sqlite` si esa versión lo admite y `db.test.js`
  se omite con un aviso explicativo si el módulo no está disponible.

## [1.0.0-rc1] - 2026-07-29

Esta versión consolida el cierre funcional y arquitectónico principal de EvalFP. El sistema queda reforzado en evaluación, generación de informes, robustez de IA, privacidad y preparación para empaquetado.

### Added
- Ponderaciones dinámicas de RA integradas desde la base de datos local.
- Informes IA con control normativo de mínimos, regla de oro y mensajes humanizados.
- Validación previa de formato de notas en el cliente.
- Banners visuales de error y advertencia en la interfaz de IA.
- Indicadores de carga por fases durante procesos largos.
- Anonimización del alumnado antes de enviar datos a APIs externas.
- Aviso explícito cuando falla la generación de apuntes HTML.
- Exportación automatizada de informes individuales en el flujo masivo.
- Soporte para absentismo crítico y RAs llave en el diagnóstico.
- Resolución de rutas robusta para desarrollo y producción.

### Changed
- El parser de opciones de Python ahora rechaza flags desconocidos y flags sin valor.
- La lógica de CE→RA fue centralizada en un helper único.
- El motor IA añadió control de errores de red, timeouts y fallos de API.
- El flujo IPC fue unificado entre Electron y Python para el informe IA.
- La resolución de rutas internas de los scripts pasó a depender de la ubicación real del archivo, no del directorio de ejecución.

### Fixed
- Se eliminó la duplicación de lógica en varios puntos del backend.
- Se corrigieron casos de suma cero en ponderaciones.
- Se evitó el uso de texto técnico en crudo en la terminal del profesor.
- Se redujo el riesgo de congelación ante fallos de conexión.
- Se corrigieron silencios peligrosos en flags mal escritos.
- Se estabilizó el flujo de apuntes y materiales ante errores internos.

### Notes
- La base de código ha sido validada con comprobaciones estáticas.
- La validación definitiva de producción debe seguir realizándose sobre el binario empaquetado en macOS y Windows.
- Esta release candidate marca el cierre del bloque principal de hardening funcional y técnico.

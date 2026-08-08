# Informe de discrepancias del catálogo · curso 2026-27

**Fecha:** 7 de agosto de 2026
**Alcance:** alineación del catálogo de módulos de EvalFP con los Decretos 78/2024,
79/2024 y 80/2024 de Castilla-La Mancha.
**Estado:** análisis cerrado. **No se ha modificado ningún dato del catálogo.**

---

## 0. Copia de seguridad

Antes de cualquier lectura se hizo copia de:

| Origen | Copia |
|---|---|
| `renderer/modules_data.json` | `backup_catalogo_20260807_183357/modules_data.json` |
| `scripts/modules/*.py` (92 ficheros) | `backup_catalogo_20260807_183357/modules/` |

Verificado: MD5 idéntico en el JSON y los 92 `.py` byte a byte.

---

## 1. Fuentes utilizadas

| Norma | Publicación | Fichero |
|---|---|---|
| Decreto 78/2024, de 5 de noviembre (grado básico) | DOCM AÑO XLIII **núm. 218, de 11/11/2024**, pág. 37673. NID [2024/8889] | `normativa/Decreto 78:2024.pdf` |
| Decreto 79/2024, de 5 de noviembre (grado medio) | DOCM AÑO XLIII **núm. 218, de 11/11/2024**, pág. 37694. NID [2024/8895] | `normativa/Decreto 79:2024.pdf` |
| Decreto 80/2024, de 5 de noviembre (grado superior) | DOCM AÑO XLIII **núm. 218, de 11/11/2024**, pág. 38018. NID [2024/8907] | `normativa/Decreto 80:2024.pdf` |
| Corrección de errores del Decreto 80/2024 | DOCM AÑO XLIV **núm. 31, de 14/02/2025**, pág. 6099. NID [2025/1026] | `normativa/texto/DOCM_correccion_80_2024_2025-02-14.txt` |

Los tres decretos son de la misma fecha y número de DOCM.

### 1.1 Sobre la corrección de errores: no es de septiembre de 2025

La corrección de errores del Decreto 80/2024 **es del 14 de febrero de 2025**, no de
septiembre de 2025. El «2025-09» que aparece en la URL del PDF alojado por la
Consejería (`.../normativas/2025-09/Correccion de errores DECRETO 80-2024.pdf`) es la
carpeta de subida del gestor de contenidos, no la fecha de publicación. El propio pie
del documento dice: *AÑO XLIV Núm. 31 · 14 de febrero de 2025 · 6099*.

**Su contenido íntegro es una única corrección y no toca ninguna hora:**

> En la página 38043, Disposición adicional segunda. Catálogo de módulos optativos,
> donde dice: «En el anexo III del presente Decreto, …» debe decir: «En el anexo III
> del Decreto 79/2024, de 5 de noviembre, …»

Es una remisión cruzada mal escrita. **No modifica ninguna duración, ninguna
distribución horaria semanal, ningún RA y ningún CE.** Se ha buscado expresamente una
corrección posterior del Decreto 80/2024 y no consta ninguna.

El mismo día se publicó la corrección del Decreto 79/2024 (NID [2025/1027]), que sí
corrige una tabla horaria: la del Anexo IA-4. 4º, ciclo de **Elaboración de Productos
Alimenticios**, ajeno al catálogo de EvalFP.

---

## 2. Método y control de calidad de la extracción

Los anexos se extrajeron de los PDF con `pdftotext -layout` y el script
`scripts/normativa/parse_anexos_2024.py`, que reconstruye cada tabla de «Duración y
distribución horaria semanal».

**Control aplicado a cada tabla:** la suma de las horas de los módulos y la suma de
cada columna semanal se comparan con la fila «Total» de la propia tabla. De 250 tablas
extraídas, **192 cuadran**. Las 58 que no cuadran son, en su mayoría, tablas de oferta
en tres cursos ajenas a este catálogo, salvo el caso de SMR que se detalla en §5.

**Todas las tablas de los ciclos del catálogo cuadran**, con la única excepción de SMR.

Datos crudos reproducibles en `normativa/anexos_2024_horas.json` y
`normativa/comparacion_2026-27.json`.

---

## 3. Resumen: el problema NO está donde se esperaba

Se compararon los 91 módulos del catálogo. Resultado por ciclo:

| Ciclo | Módulos comparados | Coinciden con el decreto | Discrepan |
|---|---|---|---|
| ASIR | 10 | **10** | 0 |
| DAM | 10 | **10** | 0 |
| DAW | 9 | **9** | 0 |
| AD (Asistencia a la Dirección) | 8 | **8** | 0 |
| AF (Administración y Finanzas) | 10 | **10** | 0 |
| SMR | 8 | **8** | 0 |
| SA (Servicios Administrativos) | 7 | **7** | 0 |
| CFGB Informática de Oficina | 5 | **5** | 0 |
| **GA (Gestión Administrativa)** | **9** | **0** | **9** |
| Cursos de especialización (CIBER, IABD, Python) | 15 | fuera de alcance | — |

**El único ciclo con las horas desactualizadas es Gestión Administrativa.**

### 3.1 ASIR ya estaba corregido

ASIR **no** tiene las horas del Decreto 200/2010. Comprobado contra el Anexo I A del
propio 200/2010:

| Código | Módulo | D. 200/2010 | D. 80/2024 | Catálogo hoy |
|---|---|---|---|---|
| 0369 | Implantación de sistemas operativos | 212 h · 7 | 186 h · 6 | **186 h · 6** |
| 0370 | Planificación y administración de redes | 200 h · 6 | 157 h · 5 | **157 h · 5** |
| 0371 | Fundamentos de hardware | 134 h · 4 | 116 h · 3 | **116 h · 3** |
| 0374 | Administración de sistemas operativos | 147 h · 7 | 242 h · 6 | **242 h · 6** |
| 0377 | Admón. de sistemas gestores de BD | 58 h · 3 | 65 h · 2 | **65 h · 2** |

El catálogo coincide al 100 % con el Decreto 80/2024. Lo mismo ocurre en DAM, DAW, AD,
AF, SMR, SA e Informática de Oficina.

### 3.2 Pero la fuente citada sí está mal (riesgo de inspección)

Aunque los números son correctos, el campo `decreto` de los módulos **sigue citando el
decreto original derogado**. Esto es lo que un inspector vería:

| Ciclo | Fuente que cita el catálogo | Fuente que corresponde |
|---|---|---|
| ASIR | Decreto 200/2010, de 03/08/2010 | Decreto 80/2024 (Anexo IA-3. 1º) |
| DAM | Decreto 252/2011, de 12/08/2011 | Decreto 80/2024 (Anexo IA-3. 6º) |
| DAW | Decreto 230/2011, de 28/07/2011 | Decreto 80/2024 (Anexo IA-3. 2º) |
| AD | Decreto 41/2013, de 25/07/2013 | Decreto 80/2024 (Anexo I-C.3º) |
| AF | Decreto 43/2013, de 25/07/2013 | Decreto 80/2024 (Anexo I-C.4º) |
| SMR | Decreto 107/2009, de 04/08/2009 | Decreto 79/2024 (Anexo IA-3 2º) |
| GA | Decreto 251/2011, de 12/08/2011 | Decreto 79/2024 (Anexo IC-1. 1º) |
| CFGB IO / SA | ya citan 78/2024 en parte | Decreto 78/2024 (Anexo I y II) |

**Matiz importante:** los RA y CE de esos módulos técnicos sí proceden legítimamente de
los decretos originales, porque los Decretos 78/79/80 de 2024 no los modifican. Lo que
falta es dejar constancia de que **las horas** vienen del decreto de 2024. La cita debe
ser doble, no sustituirse.

---

## 4. Discrepancias reales: Gestión Administrativa

Fuente: **Decreto 79/2024, Anexo IC-1. 1º** (DOCM núm. 218, de 11/11/2024).
La tabla cuadra: 2.000 h totales, 30 h/semana en 1.º y 30 h/semana en 2.º.

Los valores actuales del catálogo son exactamente los del Anexo I A del Decreto
251/2011 (DOCM núm. 164, de 22/08/2011), es decir, los originales sin actualizar.

### 4.1 Horas

| Código | Abrev. | Módulo | Catálogo | Decreto 79/2024 | Δ horas |
|---|---|---|---|---|---|
| 0437 | CEAC | Comunicación empresarial y atención al cliente | 130 h · 4 | **167 h · 4** | +37 |
| 0438 | OACV | Operaciones administrativas de compra-venta | 135 h · 4 | **133 h · 4** | −2 |
| 0439 | EA | Empresa y administración | 105 h · 3 | **158 h · 4** | +53 |
| 0440 | TII | Tratamiento informático de la información | 315 h · 10 | **233 h · 7** | −82 |
| 0441 | TC | Técnica contable | 165 h · 5 | **167 h · 5** | +2 |
| 0442 | OARH | Operaciones administrativas de recursos humanos | 130 h · 6 | **158 h · 4** | +28 |
| 0443 | TDC | Tratamiento de la documentación contable | 130 h · 6 | **195 h · 5** | +65 |
| 0446 | EAU | Empresa en el aula | 145 h · 7 | **195 h · 5** | +50 |
| 0448 | OAGT | Operaciones auxiliares de gestión de tesorería | 165 h · 7 | **169 h · 5** | +4 |

### 4.2 Cambios de curso (no detectados hasta ahora)

Tres módulos **cambian de curso** en el Decreto 79/2024:

| Código | Abrev. | Catálogo | Decreto 79/2024 |
|---|---|---|---|
| 0437 | CEAC | 1.º GA | **2.º GA** |
| 0439 | EA | 1.º GA | **2.º GA** |
| 0448 | OAGT | 2.º GA | **1.º GA** |

Esto afecta a la planificación, no sólo a las horas.

---

## 5. Aviso: el Decreto 79/2024 no cuadra en SMR

La tabla de SMR (**Anexo IA-3 2º**, pág. 37719) declara un total de 2.000 horas, pero
**la suma de sus propios módulos da 2.001 horas**:

```
0221 Montaje y mantenimiento de equipo            204   0223 Aplicaciones ofimáticas       270
0222 Sistemas operativos monopuesto               169   0224 Sistemas operativos en red    223
0225 Redes locales                                169   0226 Seguridad informática         167
0228 Aplicaciones web                             169   0227 Servicios en red              205
0156 Inglés profesional (GM)                       60   1710 Itinerario personal II          60
1664 Digitalización (GM)                           50   Optatividad                          80
1708 Sostenibilidad                                 40   1713 Proyecto intermodular          55
1709 Itinerario personal I                         80
                                              ---------
                                       SUMA = 2.001 h   ·   TOTAL DECLARADO = 2.000 h
```

Las columnas semanales sí cuadran (30 y 30). **No es un error de extracción:** se
comprobó con dos modos independientes de `pdftotext` (`-layout` y `-raw`) y los dígitos
coinciden. La corrección de errores del Decreto 79/2024 de 14/02/2025 **no** corrige
esta tabla (sólo corrige la de Elaboración de Productos Alimenticios).

**Acción propuesta: no tocar nada en SMR.** Los ocho módulos de SMR del catálogo ya
coinciden uno a uno con el decreto. La inconsistencia está en la norma, no en EvalFP.
Conviene documentarla y, si procede, consultarla a la Administración.

---

## 6. Módulos obligatorios que faltan y de dónde salen sus RA y CE

Faltan los transversales en los siete ciclos de grado medio y superior, y los ámbitos y
el proyecto intermodular en los dos de grado básico. Las **horas** están verificadas en
los decretos de CLM y no plantean problema.

El problema son los **RA y CE**, y afecta a la regla de trabajo del proyecto.

### 6.1 Lo que dicen literalmente los decretos de CLM

**Decreto 80/2024 (grado superior), artículo undécimo:**

> Los resultados de aprendizaje y criterios de evaluación de los módulos profesionales
> de **Itinerario personal para la empleabilidad I y II**, son los establecidos en el
> **anexo V del Real Decreto 659/2023**, de 18 de julio.
> Los resultados de aprendizaje y criterios de evaluación del módulo profesional de
> **Digitalización aplicada a los sectores productivos** son los establecidos en el
> **anexo VII del Real Decreto 659/2023**.
> Los resultados de aprendizaje y criterios de evaluación del módulo profesional de
> **Sostenibilidad aplicada al sistema productivo** son los establecidos en el
> **anexo VIII del Real Decreto 659/2023**.
> Los resultados de aprendizaje y criterios de evaluación del módulo profesional de
> **Inglés profesional**, son los establecidos en el **anexo X del Real Decreto 659/2023**.

**Decreto 79/2024 (grado medio), artículo duodécimo:** idéntico, cambiando Digitalización
al **anexo VI**, Inglés profesional al **anexo IX**, y añadiendo:

> Los resultados de aprendizaje y criterios de evaluación del módulo profesional de
> **proyecto intermodular de grado medio**, son los establecidos en el **anexo II del
> Real Decreto 499/2024**, de 21 de mayo.

**Decreto 78/2024 (grado básico), artículo tercero 2.3:**

> a) **3159. Itinerario personal para la empleabilidad**, cuyos resultados de aprendizaje,
> criterios de evaluación y duración son los establecidos en el **anexo II del presente
> decreto**.
> b) **3160. Proyecto intermodular de aprendizaje colaborativo**, cuyos resultados de
> aprendizaje y criterios de evaluación son los establecidos en el **anexo I del Real
> Decreto 498/2024**, de 21 de mayo y su duración es de 55 horas.

### 6.2 Consecuencia

| Módulo | Grado | ¿Hay texto literal de CLM? |
|---|---|---|
| Itinerario personal para la empleabilidad (3159) | básico | **Sí** — Anexo II del D. 78/2024 |
| Itinerario personal para la empleabilidad I y II (1709/1710) | medio y superior | No — remite al RD 659/2023, anexo V |
| Inglés profesional (0156 / 0179) | medio y superior | No — RD 659/2023, anexos IX y X |
| Digitalización aplicada (1664 / 1665) | medio y superior | No — RD 659/2023, anexos VI y VII |
| Sostenibilidad aplicada (1708) | medio y superior | No — RD 659/2023, anexo VIII |
| Proyecto intermodular (3160) | básico | No — RD 498/2024, anexo I |
| Proyecto intermodular (1713) | medio | No — RD 499/2024, anexo II |
| Proyecto intermodular (0379, 0492, 0616, 0657, 0664) | superior | No aparece con RA/CE en el D. 80/2024 |
| Ámbitos Ciencias aplicadas y Comunicación y CC.SS. (3161-3164) | básico | No — Anexo V del **Decreto 82/2022** de CLM (ESO) |

**Buena noticia:** el módulo 3159 de grado básico, el único con texto literal de CLM,
**ya está en el catálogo** (`cfgb_io_ipe_data.py` y `sa_ipe_data.py`), correctamente
citado al Anexo II del Decreto 78/2024.

### 6.3 Por qué esto choca con la regla del proyecto

La regla es *«los RA y los criterios se copian literalmente del decreto de CLM publicado
en el DOCM, nunca del Real Decreto estatal, porque no coinciden»*.

Esa regla es correcta para los módulos técnicos: ahí CLM amplía los CE respecto de las
enseñanzas mínimas estatales y los textos divergen. **Pero para estos transversales no
hay divergencia posible**, porque CLM no ha redactado texto propio: lo ha asumido por
remisión expresa. Copiar del RD 659/2023 aquí **es** cumplir el decreto de CLM.

Aun así, esto no lo decido yo. **No he añadido ningún módulo.** Los ámbitos 3161-3164
son un caso aparte: su currículo está en el Decreto 82/2022 de CLM (ESO), norma
autonómica que no está en `normativa/` y que habría que descargar.

---

## 7. Fuera de alcance

Los 15 módulos de cursos de especialización (**CE Ciberseguridad**, **CE IA y Big Data**,
**CE Python**) **no** se ven afectados por los Decretos 78/79/80 de 2024, que sólo
modifican currículos de ciclos de grado básico, medio y superior. Se dejan intactos.

---

## 8. Propuesta de actuación

Pendiente de tu decisión. Nada de lo siguiente se ha ejecutado.

1. **Corregir las horas y el curso de los 9 módulos de Gestión Administrativa**
   (`scripts/modules/ga_*_data.py`) según §4. Verificado y sin ambigüedad.
2. **Actualizar la trazabilidad de todos los ciclos** (§3.2): añadir al campo `decreto`
   la referencia al decreto de 2024 del que salen las horas, manteniendo la del decreto
   original del que salen los RA y CE.
3. **Documentar el descuadre de SMR** (§5) sin tocar los datos.
4. **Módulos transversales:** bloqueado a la espera de tu criterio sobre §6.
5. Regenerar con `npm run prebake` y pasar `tests/unit/catalogo.test.js`.

Los tests **no** se han ejecutado todavía: no se ha modificado nada que pudiera
romperlos.

---

## 9. Verificación del encaje normativo de Grado Básico (añadido 07/08/2026)

Se comprobó una propuesta de tabla horaria alternativa para Informática de Oficina y
Servicios Administrativos que reducía los módulos técnicos (3029→320, 3016→190,
3030→210, 3002→320) y daba de alta la formación en empresa como módulo de 400 horas.
**No se ha aplicado.** Estas son las razones, con la norma en la mano.

### 9.1 Las 400 horas salen de dentro del Anexo I, no se restan otra vez

**Decreto 78/2024, artículo cuarto**, que incorpora un artículo 5.bis a los decretos de
grado básico:

> «2. […] La fase de formación en empresa u organismo equiparado, **que carece de
> currículo propio y diferenciado**, contribuye al desarrollo de parte de los resultados
> de aprendizaje contemplados en los módulos profesionales del correspondiente
> currículo […]
> 3. Para la consecución de los resultados de aprendizaje de los diferentes módulos
> profesionales se destinarán 400 horas, **de las totales del ciclo formativo**, a la
> formación en la empresa u organismo equiparado.»

**Orden 204/2024, de 2 de diciembre, artículo 16.1** (DOCM de 05/12/2024):

> «La asignación total de horas de formación en el centro educativo y en la empresa
> **deberá ser la prevista en los anexos de distribución horaria que se incluyen en los
> decretos de currículo** de cada una de las enseñanzas de Castilla-La Mancha.»

**Artículo 16.2** de la misma Orden:

> «Con carácter general, **en los mencionados anexos se establece** que […] para los
> ciclos formativos de grado básico, se destinarán 400 horas en la oferta de régimen
> general, con una distribución de **entre 70 y 120 horas** a desarrollar durante el
> primer curso y el periodo resultante hasta completar el total de las 400 horas,
> durante el segundo curso.»

Conclusión: el Anexo I del Decreto 78/2024 **ya es la tabla definitiva** y ya contiene
las 400 horas. No existe un segundo ajuste a la baja a cargo del centro; al contrario,
el artículo 16.1 obliga a respetar el anexo. Y el reparto de la dualidad es 70-120 h en
primer curso (no 180) y 280-330 h en segundo (no 220).

### 9.2 El catálogo ya distingue duración oficial y horas de aula

La cifra que la propuesta llamaba «horas totales legales» es en realidad la de aula. El
proyecto ya separa ambas desde `scripts/aplicar_horas_aula.py`:

| Cód. | `total_horas` (Anexo I, D78/2024) | `horas_aula` | Regla |
|---|---:|---:|---|
| 3029 | 335 | 300 | 10 h/sem × 30 semanas (1.º) |
| 3031 | 275 | 240 | 8 × 30 |
| 3016 | 338 | 200 | 8 × 25 semanas (2.º) |
| 3030 | 338 | 200 | 8 × 25 |
| 3002 | 387 | 225 | 9 × 25 |

Las semanas lectivas se deducen de los ámbitos, que no tienen fase de empresa:
120 h ÷ 4 h/sem = 30 semanas en 1.º; 152 h ÷ 6 h/sem ≈ 25 en 2.º.

`total_horas` es el dato que ve la Inspección; `horas_aula` es el que reparten las
unidades de trabajo. **No debe sustituirse el primero por el segundo.**

### 9.3 Extremos verificados como correctos

- **Decreto 62/2014, de 24/07/2014**, es el currículo de Informática y Comunicaciones
  (artículo primero, apartado 2.b, del Decreto 78/2024). El módulo 3015 (Equipos
  eléctricos y electrónicos) no figura en la tabla de Informática de Oficina: comprobado,
  cero apariciones en su Anexo I.
- **Orden 204/2024, de 2 de diciembre** (DOCM de 05/12/2024): organización de la FP dual
  en Grados D y E. Correctamente citada.
- **Orden 201/2024, de 28 de noviembre**: evaluación, promoción, titulación y
  certificación en Grados D y E.
- Supresión de «Iniciación a la actividad emprendedora y empresarial» y alta del 3159:
  artículo tercero, apartados 2.1 y 2.3.a, del Decreto 78/2024.

### 9.4 Norma sobrevenida a revisar

La **Orden 201/2024 está modificada por la Orden 55/2026, de 17 de abril** (DOCM de
27/04/2026), en vigor para el curso 2026-27. Afecta, entre otros puntos, al derecho a
pruebas objetivas del alumnado que pierde la evaluación continua.

`tests/unit/catalogo.test.js` apoya varias reglas en artículos de la Orden 201/2024
(art. 3.3 del 25 % de faltas, art. 3.4 de evaluación continua, art. 8.2 de
convocatorias). **Pendiente:** revisar si la Orden 55/2026 altera esos supuestos.

---

## 10. Cursos de especialización (añadido 07/08/2026)

Los Decretos 78, 79 y 80 de 2024 no afectan a los cursos de especialización. Aun así
se auditaron los tres del catálogo.

### 10.1 Ciberseguridad e IA y Big Data: correctos

Las once horas de los once módulos coinciden una a una con el Anexo I de sus decretos,
en la distribución de tres trimestres:

| Ciclo | Decreto | DOCM | Total | h/sem | Resultado |
|---|---|---|---:|---:|---|
| CE Ciberseguridad en Entornos de las TI | 77/2022, de 12/07/2022 | núm. 136, de 18/07/2022 | 720 h | 24 | 6 de 6 correctos |
| CE Inteligencia Artificial y Big Data | 69/2022, de 12/07/2022 | núm. 136, de 18/07/2022 | 600 h | 18 | 5 de 5 correctos |

Se completó la cita de procedencia de los once, que no indicaba número ni fecha de
DOCM ni de qué anexo salía cada dato.

### 10.2 CE de Python: reconstruido por completo

Era el punto más débil del catálogo. Su procedencia decía literalmente
`CE Desarrollo de Aplicaciones en Python (Decreto CLM — Turno Diurno)`, que no es una
cita normativa, y sus códigos de módulo estaban inventados.

Existe decreto desde octubre de 2025: **Decreto 79/2025, de 14 de octubre** (DOCM
núm. 205, de 23/10/2025, pág. 33217, NID [2025/7868]), que complementa el Real Decreto
566/2024. Los cuatro módulos estaban mal en todo:

| Antes | Ahora (Decreto 79/2025) |
|---|---|
| `PYENV` Entornos · 60 h · 3 RA · 17 CE | **5098** Entornos y sintaxis en Python · 50 h · 5 RA · 32 CE |
| `PYCTRL` Control · 60 h · 3 RA · 18 CE | **5099** Estructuras de control en Python · 80 h · 5 RA · 34 CE |
| `PYOOP` POO · 150 h · 5 RA · 29 CE | **5100** Programación orientada a objetos · 150 h · 5 RA · 41 CE |
| `PYDATA` Datos · 150 h · 5 RA · 29 CE | **5101** Análisis de datos con Python · 150 h · 4 RA · 20 CE |
| Total **420 h** | Total **430 h** |

Los 127 criterios de evaluación se han transcrito literalmente del Anexo II. Las
unidades de trabajo, ponderaciones y reparto por evaluación son propuesta didáctica,
no normativa, y así consta en la cabecera de cada fichero.

Detalle documentado en `normativa/texto/DOCM_CE_PYTHON_79_2025.txt`, incluida una
errata del propio decreto (el artículo 5.1 escribe «Phyton»; los anexos, «Python»).

**Pendiente:** el artículo 5.3 permite incorporar una fase de formación en empresa a
propuesta del centro (20-35 % de la duración en régimen general). El catálogo no la
tiene dada de alta. Si el centro la oferta, habría que reflejarla.

---

## 11. Módulos transversales incorporados (07/08/2026)

Se han dado de alta **39 módulos transversales**. El catálogo pasa de 91 a **130**.

### 11.1 Qué se ha añadido

| Módulos | Código | Ciclos | RA y CE |
|---:|---|---|---|
| 7 | 1709 Itinerario personal para la empleabilidad I | ASIR, DAW, DAM, AD, AF, GA, SMR | RD 659/2023, anexo V |
| 7 | 1710 Itinerario personal para la empleabilidad II | los mismos | RD 659/2023, anexo V |
| 7 | 1708 Sostenibilidad aplicada al sistema productivo | los mismos | RD 659/2023, anexo VIII |
| 5 | 1665 Digitalización aplicada (GS) | ASIR, DAW, DAM, AD, AF | RD 659/2023, anexo VII |
| 2 | 1664 Digitalización aplicada (GM) | GA, SMR | RD 659/2023, anexo VI |
| 5 | 0179 Inglés profesional (GS) | ASIR, DAW, DAM, AD, AF | RD 659/2023, anexo X |
| 2 | 0156 Inglés profesional (GM) | GA, SMR | RD 659/2023, anexo IX |
| 2 | 1713 Proyecto intermodular | GA, SMR | RD 499/2024, anexo II |
| 2 | 3160 Proyecto intermodular de aprendizaje colaborativo | IO, SA | RD 498/2024, anexo I |

Las **horas, el curso y las horas semanales** salen siempre del anexo del decreto
autonómico (78, 79 u 80 de 2024). Los **RA y CE** son literales del Real Decreto al
que el decreto de CLM remite expresamente. Cada ficha lleva la cadena completa en su
campo `decreto`, del estilo:

> Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de
> 11/11/2024), Anexo I · RA y CE: Anexo V del RD 659/2023 (por remisión expresa del
> decreto de CLM, Real Decreto 659/2023, de 18 de julio, texto consolidado)

Fuentes literales guardadas en `scripts/normativa/transversales_datos.py`,
`transversales_datos2.py` y `gen_transversales.py`, con las erratas del BOE
transcritas tal cual y señaladas.

### 11.2 Verificación

- 115 módulos comparables contra su decreto: **cero discrepancias de horas**.
- El comparador marca 4 avisos en los proyectos intermodulares (1713 y 3160). No son
  errores: el anexo les asigna 1 h/semana en **cada** curso y el comparador suma las
  dos columnas. Las horas totales (55) coinciden. El catálogo los ancla en 2.º con
  1 h/semana, que es lo correcto por curso.
- `npm run prebake`: 130 módulos. `tests/unit/catalogo.test.js`: 9 de 9.
- El test tenía el 91 fijado; se ha actualizado a 130.

### 11.3 Lo que sigue faltando: 14 módulos

| Nº | Módulos | Ciclos | Situación |
|---:|---|---|---|
| 8 | Ámbitos 3161-3164 (Ciencias aplicadas I-II, Comunicación y CC.SS. I-II) | IO, SA | Su currículo está en el anexo V del **Decreto 82/2022** de CLM (ESO). **Problema de fondo:** ese decreto no usa la estructura RA + CE, sino competencias específicas, criterios de evaluación y saberes básicos. No encaja directamente en el modelo de EvalFP y hay que decidir cómo representarlo. |
| 5 | Proyecto intermodular de grado superior (0379 ASIR, 0492 DAM, 0616 DAW, 0657 AF, 0664 AD) | los 5 CFGS | **Sin fuente localizada.** El Decreto 80/2024 no desarrolla sus RA ni CE, y a diferencia del grado medio y del básico tampoco remite a ningún Real Decreto. Conviene consultarlo a la Administración antes de inventar nada. |
| 1 | 0180 Segunda lengua (Francés), 110 h, 2.º | AD | Fuente disponible (Decreto 41/2013, anexo II, ya en `normativa/`). Pendiente sólo de transcribir. |

---

## 12. Cotejo literal de los criterios de evaluación (07/08/2026)

Afirmar «RA y CE literales del DOCM» solo vale si se puede demostrar. Se ha cotejado
**criterio a criterio** el texto que guarda EvalFP contra el texto del decreto del que
dice proceder.

**Método.** `scripts/normativa/cotejar_ce.py` extrae el texto de cada decreto, lo
normaliza (quita todo lo que no sea letra o número y pasa a minúsculas) y comprueba
que cada criterio del catálogo aparece dentro. La normalización neutraliza los
guiones de partición que mete el PDF («in - formación»), los dobles espacios, las
comillas tipográficas y los saltos de línea; **no** neutraliza una palabra distinta,
una frase cambiada ni un criterio inventado.

### 12.1 Resultado

| Ciclo | Criterios | No casan |
|---|---:|---:|
| ASIR | 627 | 0 |
| DAM | 552 | 0 |
| DAW | 516 | 0 |
| AF | 510 | 0 |
| GA | 507 | 0 |
| SMR | 494 | 0 |
| AD | 425 | 0 |
| SA | 209 | 0 |
| Informática de Oficina | 200 | 0 |
| CE Ciberseguridad | 178 | 0 |
| CE IA y Big Data | 133 | 0 |
| **Total heredado** | **4.351** | **0** |

**4.351 de 4.351 coinciden literalmente. El 100 %.**

Los 43 módulos transcritos en esta sesión se cotejaron contra sus ficheros de datos
literales, con el mismo resultado:

| Origen | Criterios | Diferencias |
|---|---:|---:|
| 39 transversales (RD 659/2023, 498/2024, 499/2024) | 1.486 | 0 |
| 4 del CE de Python (Decreto 79/2025) | 127 | 0 |

**Total verificado: 5.964 criterios de evaluación.**

### 12.2 Un fallo del propio cotejo, y cómo se resolvió

La primera pasada dio 52 criterios sin localizar, los de los dos módulos de
Itinerario personal para la empleabilidad (3159) de Informática de Oficina y
Servicios Administrativos. No era un error del catálogo sino del script: buscaba sus
criterios en los Decretos 80/2014 y 83/2014, cuando el 3159 es el único transversal
cuyos RA y CE redacta Castilla-La Mancha, en el Anexo II del Decreto 78/2024. Con la
fuente correcta, casan los 26 de cada uno.

### 12.3 Cómo repetirlo

    python3 scripts/normativa/cotejar_ce.py            # resumen por ciclo
    python3 scripts/normativa/cotejar_ce.py --detalle  # lista los que no casen

Devuelve código de salida 0 si todo casa y 1 si algo falla, así que sirve para
integrarlo en el control de calidad. Conviene volver a pasarlo cada vez que se toque
un módulo o se publique una modificación de currículo.

---

## 13. Alcance definitivo del catálogo (07/08/2026)

De los 14 módulos que quedaban sin dar de alta, **9 se descartan por alcance**: no los
imparte profesorado de Formación Profesional, así que no pertenecen a un cuaderno del
profesor de FP.

### 13.1 Módulos descartados y por qué

| Nº | Módulos | Motivo |
|---:|---|---|
| 1 | 0180 Segunda lengua (Francés), AD | Módulo de idioma, no lo imparte profesorado de FP. |
| 8 | Ámbitos 3161-3164 (Ciencias aplicadas I-II, Comunicación y Ciencias Sociales I-II) en IO y SA | El propio Decreto 78/2024 los denomina **«ámbitos no profesionales»** y los atribuye a otro profesorado. |

Respaldo normativo del segundo caso, artículo 9 en la redacción dada por el artículo
octavo del Decreto 78/2024:

> «2. Las especialidades del profesorado con atribución docente en los ámbitos no
> profesionales de un ciclo formativo de grado básico serán las establecidas en el
> anexo IV del Real Decreto 286/2023, de 18 de abril […]
>
> 3. La docencia de los Ámbitos de Ciencias Aplicadas y Comunicación y Ciencias
> Sociales será impartida preferentemente por profesorado adscrito a los ámbitos
> lingüístico y social, y científico-tecnológico.»

Esto resuelve además el problema estructural señalado en §11.3: no hacía falta decidir
cómo representar unas competencias específicas y unos saberes básicos en un modelo de
RA y CE, porque esos ámbitos quedan fuera del alcance de la herramienta.

### 13.2 Lo único que queda pendiente

**Los 5 proyectos intermodulares de grado superior**: 0379 (ASIR), 0492 (DAM),
0616 (DAW), 0657 (AF) y 0664 (AD). Sí los imparte profesorado de FP, y el Anexo I del
Decreto 80/2024 les asigna 55 horas, pero **el decreto no desarrolla sus resultados de
aprendizaje ni sus criterios de evaluación, y tampoco remite a ningún Real Decreto**,
a diferencia de lo que sí hacen el Decreto 79/2024 para grado medio (RD 499/2024,
anexo II) y el 78/2024 para grado básico (RD 498/2024, anexo I).

Es una laguna de la norma, no del catálogo. **Recomendación:** consultarlo por escrito
a la Administración educativa y archivar la respuesta. Una consulta documentada
protege mejor ante una inspección que un texto redactado por cuenta propia, que sería
justamente lo que la regla del proyecto prohíbe.

### 13.3 Estado final

| | |
|---|---|
| Módulos en el catálogo | **130** |
| Criterios de evaluación verificados literalmente | **5.964 de 5.964 (100 %)** |
| Discrepancias de horas contra los decretos | **0** |
| Módulos pendientes por laguna normativa | 5 |
| Módulos fuera de alcance (otro profesorado) | 9 |
| Tests | 151 de 151 |

---

## 14. Revisión de la Orden 55/2026 sobre las reglas de evaluación (07/08/2026)

**Orden 55/2026, de 17 de abril** (DOCM AÑO XLV núm. 78, de 27/04/2026, pág. 14105,
NID [2026/3017]), que modifica la Orden 201/2024. En vigor desde el 28/04/2026, es
decir, aplicable al curso 2026-27.

### 14.1 Conclusión

**Ninguna regla implementada en el código queda invalidada.** La Orden confirma tres
comportamientos que EvalFP ya tenía bien, deja obsoleta una cita (corregida) y añade
obligaciones que la aplicación todavía no cubre.

### 14.2 Lo que ya estaba bien y la Orden confirma

| Regla | Dónde | Estado |
|---|---|---|
| «Superado parcial» cuenta como superado a efectos de promoción (art. 18.4) | `calificacion.js`, `superadoParaPromocion` | Correcto |
| Con exención total de la fase de empresa no cabe el «superado parcial» (art. 22.5, nuevo) | `faseOk` incluye `fase === 'exenta'` → SUPERADO | Correcto |
| Módulos dualizados → SP o NS; el resto → S o NS (art. 21.7, párrafo nuevo) | `faseOk = !ctx.tieneFaseEmpresa \|\| …` | Correcto |

### 14.3 Cita corregida: la renumeración del artículo 25

La Orden **suprime el apartado 8 del artículo 25** (el que reflejaba «Exento/EXEN»
para los módulos objeto de correspondencia con la práctica laboral) y **renumera los
siguientes**: 9→8, 10→9, 11→10, 12→11, 13→12, 14→13.

El código cita el artículo 25 en seis puntos. Cinco (25.2, 25.3, 25.4, 25.5 y 25.6)
son anteriores al apartado suprimido: ni su número ni su contenido cambian.

El sexto sí se veía afectado: las siglas **«RC» de renuncia a convocatoria estaban en
el art. 25.9 y pasan a ser el art. 25.8**. La conducta del programa es la correcta;
lo que quedaba obsoleto era la referencia. Corregido en tres ficheros:

- `preload.js`
- `renderer/js/modules/alumnos.js`
- `renderer/js/modules/evaluaciones.js`

El apartado suprimido (EXEN) **no estaba implementado**, así que su desaparición no
deja código muerto.

### 14.4 Obligaciones nuevas que la aplicación no cubre

Ninguna rompe nada; son funcionalidad pendiente.

| Artículo | Qué exige | Situación en EvalFP |
|---|---|---|
| **3.6** (nuevo) | Quien pierde el derecho a evaluación continua tiene derecho a pruebas objetivas sobre **la totalidad de los RA**, «sin que pueda considerarse la conservación de calificaciones parciales obtenidas con anterioridad». | No se modela la pérdida de evaluación continua. **Es el cambio de más calado**: si se implementa, hay que impedir expresamente que se arrastren notas previas. |
| **3.7** (nuevo) | Ese alumnado no podrá realizar prácticas o pruebas que impliquen riesgo. | No se modela. |
| **18.5** (nuevo) | En último curso, hasta 3 materias pendientes con carga conjunta < 30 % de la duración del curso no obligan a repetirlas; el tutor emite informe (anexo VIII). | No se modela. |
| **25.9** (antes 25.10) | Nota final del título de Técnico Básico: media aritmética de los módulos **del ámbito profesional** y el proyecto intermodular, **con independencia de la carga lectiva**. Además, el título de Graduado en ESO por grado básico **se expide sin calificación**. | La aplicación no calcula nota final de ciclo. Si se implementa, **la media es aritmética, no ponderada por horas**. |
| **25.10** (antes 25.11) | Igual para grado medio, superior y cursos de especialización. | Ídem. |
| **25.11** (antes 25.12) | Los módulos convalidados sin nota no computan en la calificación final. Ya no menciona «o exentos», por la supresión del apartado 8. | No se modela la convalidación (art. 25.7, «CONV»). |
| **25.12** (antes 25.13) | Matrícula de Honor con nota ≥ 9, una por cada veinte estudiantes, ahora «diferenciado por ciclo formativo o curso de especialización **y modalidad**». | No se modela. |
| **22.4 y 22.5** | Exención del periodo de empresa: solicitud con 15 días de antelación (anexo X), resolución del director (nuevo anexo X-BIS), posibilidad de exención parcial. | Se modela el estado `exenta`, pero no el circuito documental. |

### 14.5 Verificación

`npx vitest run`: 151 de 151 tests en 7 ficheros, después de la corrección.

---

## 15. Implementación de la Orden 55/2026 (07/08/2026)

### 15.1 Motor de cálculo

Todo en `renderer/js/core/calificacion.js`, con 19 tests nuevos en
`tests/unit/orden-55-2026.test.js`.

| Artículo | Qué se ha implementado |
|---|---|
| **3.6** | `estadoModulo(ctx, notas, { evalContinuaPerdida: true })`. Corta por tres sitios: solo cuentan las actividades marcadas como prueba objetiva, no se aplican los RA cerrados como superados en sesiones anteriores, y no se aplican los criterios dados por alcanzados a mano. Además exige **todos** los RA, no solo los que tengan actividad: si la prueba no cubre alguno, el módulo queda PENDIENTE en vez de darse por superado. |
| **25.9 y 25.10** | `notaFinalCiclo(modulos)` — media **aritmética** con dos decimales, sin ponderar por horas. `notaAccesoGradoMedio(modulos)` para el acceso a grado medio, que sí incluye los ámbitos. |
| **25.11** | `computaEnNotaFinal(m)` — excluye los convalidados sin nota; con nota, computan. |
| **25.12** | `cupoMatriculaHonor(n)` (uno por cada veinte o fracción) y `candidatosMatriculaHonor(alumnado, total)`, que propone pero no decide: la concesión es «por acuerdo del equipo docente». |
| **18.5** | `puedeContinuarConPendientes(pendientes, horasCurso)` — hasta tres materias y por debajo del 30 %, devolviendo el motivo cuando no se cumple. |

El test que más importa es el de la media aritmética: un módulo de 300 h con un 4 y
otro de 50 h con un 10 dan **7**, no 4,86. Ponderar por horas ahí es el error natural,
porque dentro de un módulo sí se pondera.

### 15.2 Persistencia

Migraciones automáticas en `db.js`, con el patrón de las anteriores (no tocan datos
existentes):

- `actividades.prueba_objetiva` — marca la prueba de evaluación completa del art. 3.6.
- `evaluacion_continua` (tabla nueva) — pérdida del derecho por alumno y módulo, con
  fecha y motivo. Se guarda el motivo porque es la decisión que deja a alguien sin la
  nota que ya tenía: hay que poder justificarla.
- `matricula.convalidado` y `matricula.nota_convalidacion` — la distinción que exige
  el art. 25.11.

Quitar la marca de pérdida devuelve al alumnado a la evaluación ordinaria y recupera
lo calificado durante el curso: **no se borra nada**. El art. 3.6 impide *considerar*
esas notas mientras la pérdida está vigente, no eliminarlas.

Accesores `getEvaluacionContinua` / `setEvaluacionContinua` y `getConvalidaciones` /
`setConvalidacion`, expuestos por IPC y `preload.js` como los de la fase de empresa.

### 15.3 Verificación

`npx vitest run`: **170 tests en 8 ficheros**, todos verdes. `npx eslint`: limpio.

### 15.4 Lo que queda: la capa de pantallas

El motor y los datos están; falta la interfaz.

| Pendiente | Nota |
|---|---|
| Casilla «prueba objetiva» al crear una actividad | Mecánico. |
| Marcar en Alumnos la pérdida de evaluación continua y la convalidación | Mecánico, mismo patrón que la fase de empresa. |
| Aviso del art. 3.7 (no realizar pruebas que impliquen riesgo) | Es un aviso en pantalla, no afecta al cálculo. |
| Informe del anexo VIII (art. 18.5) y anexo X-BIS (exención) | Documentos nuevos. |
| **Pantalla de calificación final de ciclo y Matrícula de Honor** | **Tiene enjundia arquitectónica.** Hoy cada módulo y grupo es un cuaderno independiente y el alumnado vive dentro de un módulo. Para la nota final del ciclo hay que cruzar el mismo alumno entre módulos, previsiblemente por NIA. Es una decisión de diseño, no una pantalla más. |

### 15.5 Fase de empresa del CE de Python (Decreto 79/2025, art. 5.3)

Implementadas `franjaFaseEmpresaCE()` y `validaFaseEmpresaCE()`, que devuelven los
límites legales y validan la propuesta del centro. Para las 430 horas del curso:

| Régimen | Horas en empresa | RA en empresa |
|---|---|---|
| General (el ordinario) | **86 a 150 h** (20-35 %) | 10-20 % → 2 o 3 de los 19 RA |
| Intensivo | **151 a 215 h** (35-50 %) | al menos el 30 % → 6 RA o más |

Los porcentajes de RA se aplican «a la totalidad de los mismos y no por módulo
profesional»: son del curso entero.

**No se ha fijado la cifra en el catálogo.** El artículo dice «a propuesta del centro
educativo»: dentro de esa franja, cuántas horas y qué RA van a la empresa es una
decisión del centro, no un dato del decreto. En cuanto esté decidida, se traduce en el
`horas_aula` de los cuatro módulos y la validación confirma que encaja.

---

## 16. Cierre de la implementación (07/08/2026)

### 16.1 Pantallas conectadas

- **Programación** · botón «Prueba objetiva del módulo completo» en su propio bloque.
  Crea la actividad del art. 3.6 **ya marcada con todos los criterios del módulo**:
  dejar que se marcaran a mano invitaba a olvidar alguno, y entonces el módulo se
  daría por superado sin haber evaluado todo.
- **Alumnado** · columna «Ev. continua · conval.» con dos controles. El de pérdida de
  evaluación continua pide confirmación explicando qué implica, muestra el porcentaje
  de faltas acumulado y exige un motivo que queda registrado con la fecha. Se oculta
  en grado básico, donde no aplica (art. 3.4).
- **Ajustes** · fase de empresa del CE de Python, configurable entre 86 y 150 horas,
  con la franja del art. 5.3 validada en el servidor. Se reparte entre los cuatro
  módulos en proporción a su duración.

### 16.2 El cálculo, conectado de verdad

La marca de pérdida se pasa al motor en **Evaluaciones**, **Dashboard** y el
**boletín individual**. Era el paso que faltaba: sin él la casilla existiría y el
cálculo seguiría igual.

### 16.3 Fuera de alcance por decisión de la usuaria

**La calificación final de ciclo y la Matrícula de Honor no se implementan como
pantalla.** Los cuadernos de EvalFP son de cada docente y de un solo módulo; la nota
final del ciclo la calcula la Administración con los datos de todo el equipo docente.
Las funciones puras (`notaFinalCiclo`, `candidatosMatriculaHonor`) quedan en el motor,
probadas y documentadas, por si algún día hicieran falta.

Esto resuelve además el problema arquitectónico de §15.4: ya no hace falta cruzar al
mismo alumno entre módulos.

### 16.4 Verificación

`npx vitest run`: **175 tests en 8 ficheros**. `npx eslint .`: limpio.

Un apunte: el test de accesibilidad detectó que el campo nuevo de Ajustes no tenía
nombre para un lector de pantalla. Corregido con `label for` y `aria-label`. La red
funciona.

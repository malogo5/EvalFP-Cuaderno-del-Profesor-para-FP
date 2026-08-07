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

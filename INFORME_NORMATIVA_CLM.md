# Todo el catálogo con los decretos de Castilla-La Mancha

> **Documento histórico, con las cifras de la fecha en que se escribió.**
> El 07/08/2026 el catálogo se alineó con los Decretos 78, 79 y 80 de 2024 y pasó a
> **130 módulos y 5.964 criterios**. Lo vigente está en
> [INFORME_DISCREPANCIAS_2026-27.md](INFORME_DISCREPANCIAS_2026-27.md).
> Corrección concreta: donde este informe dice que el CE de Desarrollo de Aplicaciones
> en Python es un «curso propio, sin normativa asociada», ya no es cierto. Su currículo
> lo establece el **Decreto 79/2025, de 14 de octubre** (DOCM núm. 205, de 23/10/2025),
> y los cuatro módulos se rehicieron con él.



30/07/2026 · **91 módulos · 552 RA · 552 unidades de trabajo · 4.444 criterios de evaluación**

De los 4.351 criterios de los 87 módulos que tienen decreto autonómico, **el 100 % es texto
literal del DOCM**, verificado por comparación automática contra el PDF oficial de cada decreto.
Los 4 restantes (CE de Python) son un curso propio sin normativa asociada.

## Lo que estaba mal

El campo `decreto` de los módulos de Informática citaba a la vez el Real Decreto estatal y el
decreto de CLM, pero el texto que había dentro **no era el del DOCM**: solo el 18 % de los
criterios coincidía. No era una cuestión de redacción: **28 de los 42 módulos tenían incluso un
número distinto de RA** que su decreto autonómico.

| Ciclo | Ejemplo | Antes | Decreto CLM |
|---|---|---|---|
| SMR | 0227 Servicios en red | 5 RA / 32 CE | **9 RA / 78 CE** |
| SMR | 0223 Aplicaciones ofimáticas | 6 RA / 41 CE | **10 RA / 65 CE** |
| DAM | 0488 Desarrollo de interfaces | 5 RA / 32 CE | **8 RA / 65 CE** |
| DAW | 0613 Desarrollo web en entorno servidor | 6 RA / 40 CE | **9 RA / 68 CE** |
| ASIR | 0369 Implantación de sistemas operativos | 8 RA / 79 CE | **8 RA / 72 CE** |

Evaluar con criterios que no son los del decreto es justo lo que no aguanta una reclamación,
así que se han regenerado los 52 módulos afectados (42 de ciclos + 10 de especializaciones)
con el texto exacto del DOCM.

## Los 12 ciclos y su fuente

| Ciclo | Módulos | RA | CE | Decreto de Castilla-La Mancha |
|---|---|---|---|---|
| CFGB Informática de Oficina | 5 | 29 | 200 | Decreto 80/2014 (NID 2014/10283) · IPE del Decreto 78/2024 |
| CFGB Servicios Administrativos | 7 | 30 | 209 | Decreto 83/2014 (NID 2014/10286) · IPE del Decreto 78/2024 |
| CFGM Sistemas Microinformáticos y Redes | 8 | 59 | 494 | Decreto 107/2009 (NID 2009/11413) |
| CFGM Gestión Administrativa | 9 | 54 | 507 | Decreto 251/2011 (NID 2011/11912) |
| CFGS Administración de Sistemas Informáticos en Red | 10 | 68 | 627 | Decreto 200/2010 (NID 2010/13389) |
| CFGS Desarrollo de Aplicaciones Multiplataforma | 10 | 66 | 552 | Decreto 252/2011 (NID 2011/11916) |
| CFGS Desarrollo de Aplicaciones Web | 9 | 64 | 516 | Decreto 230/2011 (NID 2011/11276) |
| CFGS Administración y Finanzas | 10 | 60 | 510 | Decreto 43/2013 (NID 2013/9487) |
| CFGS Asistencia a la Dirección | 8 | 49 | 425 | Decreto 41/2013 (NID 2013/9482) |
| CE Ciberseguridad | 6 | 32 | 178 | Decreto 77/2022 |
| CE Inteligencia Artificial y Big Data | 5 | 25 | 133 | Decreto 69/2022 (NID 2022/6683) |
| CE Desarrollo de Aplicaciones en Python | 4 | 16 | 93 | curso propio, sin decreto |

Los PDF están en `normativa/` y su texto en `normativa/texto/`.

## Qué se ha conservado de cada módulo

Sigla, código, curso, horas semanales, duración, número de evaluaciones e instrumentos por RA.
El nombre de cada UT se ha mantenido cuando el RA del decreto decía esencialmente lo mismo que
el que había (cuando el parecido era ≥ 0,8); en el resto se ha derivado del propio enunciado del RA, para que
ningún título de UT contradiga a la normativa. **Renómbralas a tu gusto**: son la capa didáctica,
no la normativa.

Las horas de las UT y las ponderaciones de los RA se han recalculado solas (proporcionales al
número de criterios) y vuelven a cuadrar al 100 % y al total del módulo.

**Los módulos que ya tienes dados de alta en el cuaderno no se han tocado**: cada uno guarda su
propia copia en la base de datos (`modulos.data_json`), así que tu ISO en marcha y sus notas
siguen exactamente igual. Los cambios afectan a los módulos que añadas a partir de ahora. Si
quieres pasar ISO al texto literal, hay que darlo de alta de nuevo o migrar sus criterios a mano.

## Horas de Grado Básico: por qué no cuadraban

Había tres cifras distintas para el mismo módulo y ninguna era un error:

| Módulo | Decreto 80/2014 | Tabla LOFP vigente | Lo que tenía el cuaderno |
|---|---|---|---|
| 3031 OAD | 255 | 275 | 208 |
| 3029 MMSCI | 320 | 335 | 288 |
| 3016 IMRTD | 190 | 338 | 210 |
| 3030 OACE | 210 | 338 | 210 |

La clave: **338 h a 8 h/semana serían 42 semanas**, imposible. En cambio los ámbitos del mismo
curso (Ciencias aplicadas II, 152 h a 6 h/semana) dan 25 semanas. Los ámbitos no tienen fase de
empresa y los módulos profesionales sí: el total LOFP **incluye la formación en empresa**.

Solución aplicada: se guardan las dos cifras.

| Módulo | Duración oficial | Horas de aula | En empresa |
|---|---|---|---|
| 3031 OAD | 275 | 240 (8 h/sem × 30 sem) | 35 |
| 3029 MMSCI | 335 | 300 (10 × 30) | 35 |
| 3016 IMRTD | 338 | 200 (8 × 25) | 138 |
| 3030 OACE | 338 | 200 (8 × 25) | 138 |
| 3001 TID | 268 | 240 (8 × 30) | 28 |
| 3003 TAB | 197 | 180 (6 × 30) | 17 |
| 3004 AC | 144 | 120 (4 × 30) | 24 |
| 3002 ABO | 387 | 225 (9 × 25) | 162 |
| 3005 ATC | 117 | 75 (3 × 25) | 42 |
| 3006 PPVP | 173 | 100 (4 × 25) | 73 |

Las semanas (30 en 1º, 25 en 2º) no son inventadas: salen de dividir la duración de los ámbitos
entre sus horas semanales, que es la única parte del ciclo sin formación en empresa.

**Las UT reparten las horas de aula**, que son las que de verdad programas, y la app muestra las
dos cifras en la ficha del módulo («275h» y «240h aula»). La duración oficial sigue guardada para
citarla en la programación.

## Además

- **CE Ciberseguridad**: BRS 180 → **185 h** y NC 60 → **55 h** (Anexo I del Decreto 77/2022;
  el ciclo suma 720 h).
- **CE IA y Big Data**: el curso son **600 h**, no 720. SAA 120 → **100**, PIA 180 → **200**,
  SBD 90 → **100**, BDA 120 → **140** (Anexo I del Decreto 69/2022). Con esto queda resuelta la
  discrepancia de horas que estaba anotada como pendiente, y **PIA verificado** contra el decreto
  autonómico, no contra el RD 279/2021.
- **Dos fallos del parser** que habrían colado texto mal cortado: los decretos usan `ll)` y `ñ)`
  como marcadores, y el Decreto 80/2014 se salta la letra `f)` en un RA de Ofimática y archivo.
- **El decreto de IA y Big Data** trae los marcadores en una columna aparte del texto; hubo que
  extraerlo con `pdftotext -raw` para no perder 16 criterios.

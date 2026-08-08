# Catálogo de módulos · Administración y Gestión + revisión de Informática

> **Documento histórico, con las cifras de la fecha en que se escribió.**
> El 07/08/2026 el catálogo se alineó con los Decretos 78, 79 y 80 de 2024 y pasó a
> **130 módulos y 5.964 criterios**. Lo vigente está en
> [INFORME_DISCREPANCIAS_2026-27.md](INFORME_DISCREPANCIAS_2026-27.md).



30/07/2026 · el catálogo pasa de **58 a 91 módulos** en 12 ciclos.

## 1. Los 33 módulos nuevos de Administración y Gestión

Todos con **RA y CE literales del DOCM** (no del BOE) y con la **duración vigente**
que publica la Consejería de Educación de CLM para cada ciclo.

| Ciclo | Módulos | Decreto (DOCM) |
|---|---|---|
| **SA** — Servicios Administrativos (Grado Básico) | 6 nuevos + IPE ya existente = 7 | Decreto 83/2014, de 01/08/2014 · NID 2014/10286 |
| **GA** — Gestión Administrativa (Grado Medio) | 9 | Decreto 251/2011, de 12/08/2011 · DOCM 22/08/2011 · NID 2011/11912 |
| **AF** — Administración y Finanzas (Grado Superior) | 10 | Decreto 43/2013, de 25/07/2013 · DOCM 01/08/2013 · NID 2013/9487 |
| **AD** — Asistencia a la Dirección (Grado Superior) | 8 | Decreto 41/2013, de 25/07/2013 · DOCM 01/08/2013 · NID 2013/9482 |

### SA · Servicios Administrativos

| Código | Sigla | Módulo | Horas | h/sem | Curso |
|---|---|---|---|---|---|
| 3001 | TID | Tratamiento informático de datos | 268 | 8 | 1º |
| 3003 | TAB | Técnicas administrativas básicas | 197 | 6 | 1º |
| 3004 | AC | Archivo y comunicación | 144 | 4 | 1º |
| 3159 | IPE | Itinerario personal para la empleabilidad | 60 | 2 | 1º |
| 3002 | ABO | Aplicaciones básicas de ofimática | 387 | 9 | 2º |
| 3005 | ATC | Atención al cliente | 117 | 3 | 2º |
| 3006 | PPVP | Preparación de pedidos y venta de productos | 173 | 4 | 2º |

### GA · Gestión Administrativa

| Código | Sigla | Módulo | Horas | h/sem | Curso |
|---|---|---|---|---|---|
| 0437 | CEAC | Comunicación empresarial y atención al cliente | 130 | 4 | 1º |
| 0438 | OACV | Operaciones administrativas de compra-venta | 135 | 4 | 1º |
| 0439 | EA | Empresa y Administración | 105 | 3 | 1º |
| 0440 | TII | Tratamiento informático de la información | 315 | 10 | 1º |
| 0441 | TC | Técnica contable | 165 | 5 | 1º |
| 0442 | OARH | Operaciones administrativas de recursos humanos | 130 | 6 | 2º |
| 0443 | TDC | Tratamiento de la documentación contable | 130 | 6 | 2º |
| 0446 | EAU | Empresa en el aula | 145 | 7 | 2º |
| 0448 | OAGT | Operaciones auxiliares de gestión de tesorería | 165 | 7 | 2º |

### AF · Administración y Finanzas

| Código | Sigla | Módulo | Horas | h/sem | Curso |
|---|---|---|---|---|---|
| 0647 | GDJE | Gestión de la documentación jurídica y empresarial | 67 | 2 | 1º |
| 0648 | RHRSC | Recursos humanos y responsabilidad social corporativa | 68 | 2 | 1º |
| 0649 | OPI | Ofimática y proceso de la información | 223 | 7 | 1º |
| 0650 | PIAC | Proceso integral de la actividad comercial | 205 | 6 | 1º |
| 0651 | CAC | Comunicación y atención al cliente | 148 | 4 | 1º |
| 0652 | GRH | Gestión de recursos humanos | 158 | 4 | 2º |
| 0653 | GF | Gestión financiera | 197 | 5 | 2º |
| 0654 | CF | Contabilidad y fiscalidad | 236 | 6 | 2º |
| 0655 | GLC | Gestión logística y comercial | 117 | 3 | 2º |
| 0656 | SE | Simulación empresarial | 156 | 4 | 2º |

### AD · Asistencia a la Dirección

Comparte con AF los cinco módulos de 1º (mismos códigos y mismos RA/CE, verificado
cotejando los dos decretos), y añade los tres propios de 2º.

| Código | Sigla | Módulo | Horas | h/sem | Curso |
|---|---|---|---|---|---|
| 0647 | GDJE | Gestión de la documentación jurídica y empresarial | 67 | 2 | 1º |
| 0648 | RHRSC | Recursos humanos y responsabilidad social corporativa | 68 | 2 | 1º |
| 0649 | OPI | Ofimática y proceso de la información | 223 | 7 | 1º |
| 0650 | PIAC | Proceso integral de la actividad comercial | 205 | 6 | 1º |
| 0651 | CAC | Comunicación y atención al cliente | 148 | 4 | 1º |
| 0661 | PE | Protocolo empresarial | 157 | 4 | 2º |
| 0662 | OEE | Organización de eventos empresariales | 313 | 7 | 2º |
| 0663 | GAI | Gestión avanzada de la información | 284 | 6 | 2º |

## 2. Cómo se ha hecho (reproducible)

1. **Texto oficial**: PDF del DOCM de cada decreto → `normativa/*.pdf` y su texto en
   `normativa/texto/`.
2. **`scripts/parse_docm.py`** extrae los módulos con sus RA y CE **literales**. Corta por los
   marcadores del alfabeto español —incluidos `ll)` y `ñ)`, que es donde fallan los parsers
   ingenuos—, deshace el guionado de fin de línea del PDF (`«trámi - tes» → «trámites»`) y
   elimina cabeceras y números de página del boletín.
3. **`normativa/docm_json/_meta_*.json`** guarda la capa didáctica que no está en el decreto:
   sigla, curso, horas semanales, nombre de cada UT, palabras clave y evaluación.
4. **`scripts/mezclar_meta.py`** une decreto + metadatos emparejando por código y orden de RA
   (y aborta si el número de RA no coincide, para que nunca se descoloquen los criterios).
5. **`scripts/gen_modulo.py`** genera el `*_data.py`: una UT por RA, horas y ponderaciones
   proporcionales al número de criterios y ajustadas para sumar exactamente el total y el 100 %.
6. **`npm run prebake`** + **`scripts/validar_catalogo.py`**.

Verificado en los 91 módulos: horas de UT = duración del módulo, ponderaciones = 100 %,
ningún RA sin criterios, ningún criterio sin UT, ningún RA fuera de las evaluaciones,
y ni códigos ni siglas repetidos dentro de un ciclo.

## 3. Revisión de Informática: 36 módulos corregidos

Las siglas estaban bien salvo la que ya arreglamos (`OPER` → `OACE`), pero al cotejar con la
tabla oficial de cada ciclo aparecieron **errores más serios**: códigos de módulo mal asignados
y duraciones tomadas de los mínimos del Real Decreto en lugar de la distribución de CLM.

**Códigos corregidos**

| Ciclo | Antes | Ahora |
|---|---|---|
| DAM | LMSGI 0483 · SI 0484 · BD 0485 · PRG 0486 · PSP 0489 · DI 0490 · SGE 0492 · AD 0488 · PMDM 0493 | LMSGI **0373** · SI **0483** · BD **0484** · PRG **0485** · AD **0486** · DI **0488** · PMDM **0489** · PSP **0490** · SGE **0491** |
| DAW | SI 0484 · BD 0485 · PRG 0486 | SI **0483** · BD **0484** · PRG **0485** |
| SMR | RL 0224 · SOR 0225 · SR 0228 · AW 0227 | RL **0225** · SOR **0224** · SR **0227** · AW **0228** |

**Dos módulos estaban en el curso equivocado**: `AO` Aplicaciones ofimáticas pasa de 1º a **2º**
de SMR, y `AW` Aplicaciones web pasa de 2º a **1º**.

**Duraciones**: 36 módulos tenían horas distintas a las de CLM. Al ajustarlas, las horas de sus
UT se han reescalado proporcionalmente para seguir sumando el total. Ejemplos:
`OACE` 210 → **338 h**, `IMRTD` 210 → **338 h**, `OAD` 208 → **275 h**, `MMSCI` 288 → **335 h**
(la discrepancia del CFGB que quedó anotada como pendiente), `DWES` 256 → **326 h**,
`ASGBD` 160 → **65 h**, `SR` 128 → **205 h**.

**Tu módulo ISO no se ha tocado**: 0369, 186 h, 6 h/semana ya coincidía con la tabla oficial.

## 4. Dos fallos de datos encontrados y arreglados

- **`prebake_modules.py` dejaba RA sin actividad.** Cuando una UT trabajaba criterios de dos RA,
  solo generaba práctica para el primero: **11 RA** de DAM, DAW, ASIR y CFGB quedaban sin
  ninguna actividad con la que calificarse. Ahora crea una práctica por cada par UT–RA.
- **Dos módulos de SMR tenían un RA huérfano**: `SI` 0226 (RA5, servidores proxy) y `SR` 0227
  (RA4, mensajería instantánea) no tenían ninguna UT que los trabajase. Se ha añadido la UT que
  faltaba en cada uno y se han reescalado las horas.

## 5. Criterios y decisiones que conviene que revises

- **Qué módulos se han incluido**: los de la especialidad de Administración. Quedan fuera
  Inglés, Segunda lengua, FOL, EIE, FCT/Dual y los proyectos intermodulares, además de los
  ámbitos de Grado Básico (Ciencias aplicadas, Comunicación y Ciencias Sociales). El texto de
  todos ellos está extraído en `normativa/docm_json/_crudo_*.json` si quieres añadir alguno.
- **`CLM0041` Iniciación a la actividad emprendedora y empresarial** existe en el Decreto
  83/2014 pero **ya no aparece** en la distribución horaria vigente de SA (lo sustituyen IPE y
  el proyecto intermodular), así que no lo he metido. Su texto está extraído por si lo necesitas.
- **UT, ponderaciones y evaluaciones son una propuesta de partida**, no normativa: una UT por RA,
  peso proporcional al número de criterios y reparto de RA por evaluación (3 en 1º, 2 en los
  cursos con FCT). Todo editable desde la app.
- **Los RA/CE sí son literales del decreto** y no deberían tocarse: son los que sostienen una
  reclamación.
- **5073 PIA** sigue pendiente de cotejar contra el Decreto CLM 69/2022 (ahora tiene el texto
  del RD 279/2021, idéntico en lo que se ha podido comprobar).

## 6. Qué falta por hacer tú

```bash
npm test          # los tests unitarios y e2e no se pueden lanzar desde mi sandbox Linux
npm run test:e2e
npm start         # y comprobar las 12 pestañas del catálogo
```

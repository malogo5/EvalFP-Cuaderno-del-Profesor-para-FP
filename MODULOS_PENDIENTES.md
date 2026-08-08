# Estado del catálogo de módulos

**07/08/2026 · 130 módulos en 12 ciclos.** Los **5.964 criterios de evaluación** son texto
literal de su norma, **cotejado uno a uno**: 100 % de coincidencia. El cotejo es repetible
con `python3 scripts/normativa/cotejar_ce.py`.

Detalle: [INFORME_NORMATIVA_CLM.md](INFORME_NORMATIVA_CLM.md) (verificación contra los decretos
y horas de Grado Básico) y [INFORME_CATALOGO_ADMINISTRACION.md](INFORME_CATALOGO_ADMINISTRACION.md)
(los 33 módulos de Administración).

| Ciclo | Módulos | Fuente de los RA y CE |
|---|---|---|
| CFGB Informática de Oficina | 5 | Decreto 80/2014 (DOCM) · IPE del Decreto 78/2024 |
| CFGM Sistemas Microinformáticos y Redes | 8 | Decreto 107/2009 (DOCM) |
| CFGS Administración de Sistemas Informáticos en Red | 10 | Decreto 200/2010 (DOCM) |
| CFGS Desarrollo de Aplicaciones Multiplataforma | 10 | Decreto 252/2011 (DOCM) |
| CFGS Desarrollo de Aplicaciones Web | 9 | Decreto 230/2011 (DOCM) |
| CE Ciberseguridad | 6 | Decreto 77/2022 (DOCM), Anexo II |
| CE Inteligencia Artificial y Big Data | 5 | Decreto 69/2022 (DOCM), Anexo II |
| CE Desarrollo de Aplicaciones en Python | 4 | **Decreto 79/2025 (DOCM), Anexo II** |
| **CFGB Servicios Administrativos** | **7** | **Decreto 83/2014 (DOCM) · IPE del Decreto 78/2024** |
| **CFGM Gestión Administrativa** | **9** | **Decreto 251/2011 (DOCM), Anexo I** |
| **CFGS Administración y Finanzas** | **10** | **Decreto 43/2013 (DOCM), Anexo I** |
| **CFGS Asistencia a la Dirección** | **8** | **Decreto 41/2013 (DOCM), Anexo I** |

## Pendiente

No queda ningún módulo pendiente de dar de alta. Estos quedan fuera **por decisión**:

1. **Proyecto intermodular de grado superior** (0379 ASIR, 0492 DAM, 0616 DAW, 0657 AF,
   0664 AD). El Decreto 80/2024 les da 55 horas en su Anexo I pero **no desarrolla sus RA ni
   CE, y tampoco remite a ningún Real Decreto**. Es una laguna de la norma. Se decide no
   darlos de alta antes que redactar un currículo por cuenta propia.
2. **Fuera de alcance por profesorado**: los ámbitos 3161-3164 de Grado Básico y la Segunda
   lengua (0180) de Asistencia a la Dirección. El artículo 9 del Decreto 78/2024 los llama
   «ámbitos no profesionales» y los atribuye a otro profesorado.

Los transversales que antes figuraban aquí como pendientes —Itinerario Personal para la
Empleabilidad I y II, Inglés Profesional, Digitalización, Sostenibilidad y Proyecto
Intermodular de grado medio y básico— **ya están en el catálogo** desde el 07/08/2026.
FOL y EIE desaparecen del currículo con la Ley 3/2022: sus contenidos pasan al Itinerario
Personal para la Empleabilidad.

## Herramientas del pipeline

| Script | Para qué |
|---|---|
| `scripts/parse_docm.py` | extrae módulos, RA y CE literales del texto de un decreto del DOCM |
| `scripts/mezclar_meta.py` | une el texto del decreto con la capa didáctica (UT, siglas, horas) |
| `scripts/gen_modulo.py` | genera el `*_data.py` con horas y ponderaciones cuadradas |
| `scripts/corregir_catalogo.py` | alinea código, duración, horas semanales y curso con la tabla oficial |
| `scripts/regenerar_desde_clm.py` | rehace un módulo existente con los RA y CE literales de su decreto |
| `scripts/aplicar_horas_aula.py` | separa la duración oficial de las horas de aula en Grado Básico |
| `scripts/validar_catalogo.py` | comprueba la coherencia de los módulos ya prebakeados |
| `scripts/normativa/cotejar_ce.py` | coteja cada CE del catálogo con el texto de su decreto |
| `scripts/normativa/parse_anexos_2024.py` | extrae las tablas horarias de los Decretos 78/79/80 de 2024 |
| `scripts/normativa/gen_transversales.py` | genera los módulos transversales desde el texto literal del BOE |

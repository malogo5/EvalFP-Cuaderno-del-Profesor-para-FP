# Estado del catálogo de módulos

**30/07/2026 · 91 módulos en 12 ciclos.** Los 4.351 criterios de evaluación de los 87 módulos
con decreto autonómico son **texto literal del DOCM**, verificado uno a uno contra el PDF oficial.

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
| CE Desarrollo de Aplicaciones en Python | 4 | curso propio, sin normativa asociada |
| **CFGB Servicios Administrativos** | **7** | **Decreto 83/2014 (DOCM) · IPE del Decreto 78/2024** |
| **CFGM Gestión Administrativa** | **9** | **Decreto 251/2011 (DOCM), Anexo I** |
| **CFGS Administración y Finanzas** | **10** | **Decreto 43/2013 (DOCM), Anexo I** |
| **CFGS Asistencia a la Dirección** | **8** | **Decreto 41/2013 (DOCM), Anexo I** |

## Pendiente

1. **Módulos transversales**, si algún día los quieres en el cuaderno: FOL, EIE, Inglés,
   Segunda lengua, proyectos intermodulares, FCT/Dual y los ámbitos de Grado Básico. El texto
   literal de todos ellos ya está extraído en `normativa/docm_json/_crudo_*.json`.
2. **Abrir la app (`npm start`)** y revisar las 12 pestañas del catálogo.
   Tests verificados el 30/07/2026: `npm test` 27/27 y `npm run test:e2e` 12/12.
   (Con Node < 22.5 los 23 tests de base de datos se omiten con un aviso, porque esa versión no
   expone `node:sqlite`; la app no está afectada, Electron sí lo trae.)

## Herramientas del pipeline

| Script | Para qué |
|---|---|
| `scripts/parse_docm.py` | extrae módulos, RA y CE literales del texto de un decreto del DOCM |
| `scripts/mezclar_meta.py` | une el texto del decreto con la capa didáctica (UT, siglas, horas) |
| `scripts/gen_modulo.py` | genera el `*_data.py` con horas y ponderaciones cuadradas |
| `scripts/corregir_catalogo.py` | alinea código, duración, horas semanales y curso con la tabla oficial |
| `scripts/regenerar_desde_clm.py` | rehace un módulo existente con los RA y CE literales de su decreto |
| `scripts/aplicar_horas_aula.py` | separa la duración oficial de las horas de aula en Grado Básico |
| `scripts/validar_catalogo.py` | comprueba la coherencia de los 91 módulos ya prebakeados |

# EvalFP — Cuaderno del Profesor para FP

[![Licencia: GPLv3](https://img.shields.io/badge/Licencia-GPLv3-blue.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/versión-3.0.0-orange.svg)](CHANGELOG.md)

EvalFP automatiza la gestión del cuaderno del profesor de Formación Profesional en España: programación didáctica, registro de notas, cálculo de calificaciones, informes y dashboard, todo dentro de un único libro Excel generado por Python.

**Versión actual:** 3.0.0 · Consulta el [ROADMAP](ROADMAP.md) y el [CHANGELOG](CHANGELOG.md) para el historial completo.

## ¿Por qué existe EvalFP?

El profesorado de FP en España gestiona programación didáctica, evaluación por resultados de aprendizaje (RA) y boletines sin herramientas específicas: la alternativa habitual son hojas de cálculo genéricas o cuadernos en papel. EvalFP nace de la experiencia directa en el aula para cubrir ese hueco con una herramienta abierta, gratuita y adaptada al sistema de evaluación real de la FP española.

## Captura de pantalla

![Panel Diario de EvalFP](Captura%20de%20pantalla%202026-06-29%20a%20las%2011.29.07.png)

---

## Características de EvalFP 2.0

- **Multi-módulo y multi-grupo** — un único `.xlsx` para toda la carga docente del profesor
- **Motor de evaluación** 100% en fórmulas Excel: Actividades → Reg. Notas → Evaluaciones → Nota Final
- **Cascada automática** sin macros: introduce la nota de una actividad y la nota final se recalcula sola
- **Hojas globales** — Inicio · Configuración · Mis Módulos · Biblioteca · Calendario · Panel Diario · Dashboard Global
- **Hojas por módulo** (prefijadas `{ABREV} · `) — Programación · Alumnos · Actividades · Reg. Notas · Evaluación 1/2/3 · 1ªORD · 2ªORD · Rúbricas · Informe Grupo · Boletín · Dashboard
- **Asistente IA** — genera descriptores de rúbricas, propuestas de actividades e informes individuales via API Claude/OpenAI
- **Arquitectura módulo-agnóstica** — añade un nuevo módulo creando un `*_data.py` y añadiendo una línea en `teacher_config.py`

---

## Estructura del proyecto

```text
cuaderno-del-profesor/
├── README.md                         # Este archivo
├── ROADMAP.md                        # Plan de ruta v1.0 y v2.0
├── CHANGELOG.md                      # Historial de versiones
├── requirements.txt                  # Dependencias Python
├── docs/
│   ├── version_2.md                  # Visión EvalFP 2.0
│   ├── casos_uso.md                  # Casos de uso CU01–CU15
│   ├── decisiones_arquitectura.md    # Architecture Decision Records ADR-001–007
│   └── guia_desarrollo.md            # Filosofía y flujo de sprints
├── scripts/
│   ├── build_template.py             # Generador principal del libro Excel
│   ├── ai_asistente.py               # Asistente IA (Sprint 2.6)
│   ├── teacher_config.py             # Carga docente del profesor/a
│   └── modules/
│       ├── iso_data.py               # Módulo ISO (Implantación de Sistemas Operativos)
│       └── par_data.py               # Módulo PAR (Planificación y Administración de Redes)
├── src/
│   └── EvalFP.xlsx                   # Libro Excel generado (artefacto)
└── ia_output/                        # Contenido generado por el Asistente IA (opcional)
    ├── iso/
    └── par/
```

---

## Requisitos

- Python 3.10+
- `openpyxl` (obligatorio): `pip install openpyxl`
- `anthropic` o `openai` (opcional, para el Asistente IA): `pip install anthropic`

O instala todo de una vez:

```bash
pip install -r requirements.txt
```

---

## Generar el libro Excel

```bash
# Genera src/EvalFP.xlsx con todos los módulos configurados en teacher_config.py
python3 scripts/build_template.py

# Genera el xlsx + contenido IA para todos los módulos (requiere API key)
python3 scripts/build_template.py --ia
```

---

## Configurar tu carga docente

Edita `scripts/teacher_config.py`:

```python
import modules.iso_data as iso_data
import modules.par_data as par_data

TEACHER_MODULES = [
    (iso_data, "1º ASIR-A"),
    (par_data, "1º ASIR-A"),
]
```

Añade un nuevo módulo copiando `iso_data.py` o `par_data.py`, adaptando los datos, y añadiendo una línea a la lista.

---

## Asistente IA

El asistente genera contenido pedagógico en lenguaje natural a partir de los datos de tu módulo.

```bash
# Ver ayuda completa
python3 scripts/ai_asistente.py --ayuda

# Generar rúbrica para un RA
python3 scripts/ai_asistente.py rubrica --modulo iso_data --ra RA1

# Proponer actividades
python3 scripts/ai_asistente.py actividad --modulo par_data --ra RA3 --n 3

# Borrador de informe individual
python3 scripts/ai_asistente.py informe --alumno "García López, Marta" --notas "RA1:7,RA2:4,RA3:8"

# Generar todo el contenido de un módulo
python3 scripts/ai_asistente.py todo --modulo iso_data --salida ia_output/iso
```

Configura tu API key en el entorno antes de ejecutar:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # Claude (recomendado)
# o
export OPENAI_API_KEY=sk-...          # OpenAI (alternativa)
```

Sin API key, el asistente funciona en **modo DEMO** con texto de ejemplo.

---

## Documentación técnica

| Documento | Descripción |
|---|---|
| [docs/version_2.md](docs/version_2.md) | Visión y alcance de EvalFP 2.0 |
| [docs/casos_uso.md](docs/casos_uso.md) | Catálogo de casos de uso CU01–CU15 |
| [docs/decisiones_arquitectura.md](docs/decisiones_arquitectura.md) | ADRs y decisiones de diseño |
| [docs/guia_desarrollo.md](docs/guia_desarrollo.md) | Reglas de codificación y flujo de sprints |

---

## Contribuir

Las contribuciones son bienvenidas: nuevos módulos de FP (`*_data.py`), correcciones, traducciones o documentación. Consulta [docs/guia_desarrollo.md](docs/guia_desarrollo.md) para la filosofía del proyecto y abre un issue o pull request.

## Licencia

Publicado bajo licencia [GNU GPL v3.0](LICENSE). Uso, modificación y redistribución libres para el profesorado de FP y cualquier persona interesada, manteniendo la misma licencia en trabajos derivados.

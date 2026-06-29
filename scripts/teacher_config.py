"""
EvalFP — Configuración de carga docente del profesor/a
Edita esta lista para añadir o quitar módulos/grupos de tu cuaderno.

Formato de cada entrada: (módulo_data, nombre_grupo)
  - módulo_data : el módulo importado desde scripts/modules/
  - nombre_grupo: etiqueta libre para identificar el grupo (p.ej. "1ºASIR-A")
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from modules.iso_data import (
    MODULO, UTS, RAS, ASIGNACIONES, EVAL_RAS,
    DUAL_RA, DUAL_PCT_NOTA, DUAL_JUSTIFICACION, RA_INSTRUMENTOS,
)
import modules.iso_data as iso_data
import modules.par_data as par_data

# ─────────────────────────────────────────────────────────────────────────────
# CARGA DOCENTE DEL PROFESOR/A
# Añade una tupla por cada módulo+grupo que impartes.
# El prefijo de hojas se genera automáticamente como "{ABREV} · "
# ─────────────────────────────────────────────────────────────────────────────
TEACHER_MODULES = [
    (iso_data, "1º ASIR-A"),
    (par_data, "1º ASIR-A"),
]

"""EvalFP — Alias DAW de ed_data.py · Mismos RAs/CEs, ciclo DAW."""
from .ed_data import UTS, RAS, ASIGNACIONES, EVAL_RAS, DUAL_RA, RA_INSTRUMENTOS, CES
from .ed_data import MODULO as _BASE

MODULO = {
    **_BASE,
    "ciclo":       "DAW",
    "ciclo_clave": "DAW",
    "ciclo_nivel": "CFGS",
    "curso":       "1º DAW",
}

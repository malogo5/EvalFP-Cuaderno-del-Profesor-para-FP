"""
EvalFP — Datos del módulo PAR (Planificación y Administración de Redes)
Módulo: 0370 · 1º ASIR · Ciclo: ASIR
Curso académico: 2026-2027

Para añadir un nuevo módulo, copia este fichero, renómbralo y adapta las listas.
"""

# ─── MÓDULO ──────────────────────────────────────────────────────────────────
MODULO = {
    "nombre":      "Planificación y Administración de Redes",
    "codigo":      "0370",
    "abrev":       "PAR",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "curso":       "1º ASIR",
    "horas_sem":   5,
    "total_horas": 155,
    "anno":        "2026-2027",
    "eval_count":  3,
}

# ─── UNIDADES DE TRABAJO ─────────────────────────────────────────────────────
UTS = [
    {
        "id":     "UT1",
        "nombre": "Introducción a las redes locales",
        "horas":  20,
        "eval":   1,
        "tags":   "OSI · TCP/IP · Ethernet",
    },
    {
        "id":     "UT2",
        "nombre": "Dispositivos de red y medios de transmisión",
        "horas":  22,
        "eval":   1,
        "tags":   "Switch · Router · Cableado estructurado",
    },
    {
        "id":     "UT3",
        "nombre": "Configuración y administración de conmutadores",
        "horas":  22,
        "eval":   2,
        "tags":   "VLANs · STP · Port-security",
    },
    {
        "id":     "UT4",
        "nombre": "Configuración y administración de routers",
        "horas":  28,
        "eval":   2,
        "tags":   "OSPF · RIP · NAT · ACLs",
    },
    {
        "id":     "UT5",
        "nombre": "Configuración de redes inalámbricas",
        "horas":  20,
        "eval":   2,
        "tags":   "WiFi 6 · WPA3 · RADIUS",
    },
    {
        "id":     "UT6",
        "nombre": "Introducción a las redes WAN y servicios de red",
        "horas":  22,
        "eval":   3,
        "tags":   "DHCP · DNS · VPN · MPLS",
    },
    {
        "id":     "UT7",
        "nombre": "Resolución de incidencias de red",
        "horas":  21,
        "eval":   3,
        "tags":   "Wireshark · ping · traceroute · SNMP",
    },
]

# ─── RESULTADOS DE APRENDIZAJE ───────────────────────────────────────────────
RAS = [
    {
        "id":     "RA1",
        "pond":   15,
        "nombre": "Reconoce la estructura de las redes de datos describiendo sus elementos "
                  "y funcionamiento.",
    },
    {
        "id":     "RA2",
        "pond":   20,
        "nombre": "Integra ordenadores y periféricos en redes cableadas e inalámbricas, "
                  "evaluando su funcionamiento y prestaciones.",
    },
    {
        "id":     "RA3",
        "pond":   20,
        "nombre": "Administra conmutadores estableciendo opciones de configuración para "
                  "su integración en la red.",
    },
    {
        "id":     "RA4",
        "pond":   25,
        "nombre": "Administra las funciones de un router estableciendo opciones de "
                  "configuración para su integración en la red.",
    },
    {
        "id":     "RA5",
        "pond":   10,
        "nombre": "Configura redes inalámbricas en modo infraestructura describiendo sus "
                  "características y relacionándolas con su área de aplicación.",
    },
    {
        "id":     "RA6",
        "pond":   10,
        "nombre": "Soluciona problemas de conectividad en redes locales y en redes con "
                  "salida a Internet identificando las causas y describiendo las soluciones.",
    },
]

# ─── ASIGNACIONES UT → RA → CEs ──────────────────────────────────────────────
ASIGNACIONES = [
    ("UT1", "RA1", ["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2", "RA2", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2", "RA1", ["CR7","CR8"]),
    ("UT3", "RA3", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4", "RA4", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5", "RA5", ["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5", "RA4", ["CR10"]),
    ("UT6", "RA4", ["CR11","CR12"]),
    ("UT7", "RA6", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]

# ─── EVALUACIÓN POR RA ───────────────────────────────────────────────────────
EVAL_RAS = {
    1: ["RA1", "RA2"],         # Eval 1: 15% + 20% = 35%
    2: ["RA3", "RA4", "RA5"],  # Eval 2: 20% + 25% + 10% = 55%
    3: ["RA6"],                # Eval 3: 10%
}

# ─── RA DUAL ─────────────────────────────────────────────────────────────────
DUAL_RA = "RA6"
DUAL_PCT_NOTA = 0.10
DUAL_JUSTIFICACION = (
    "RA6 — Resolución de problemas de red — se evalúa en modalidad DUAL "
    "de acuerdo con el artículo 42 de la Ley Orgánica 3/2022. "
    "El alumno/a resuelve incidencias reales en el entorno laboral bajo "
    "supervisión del tutor/a de empresa. Peso en nota final: 10%."
)

# ─── INSTRUMENTOS DE EVALUACIÓN POR RA ───────────────────────────────────────
RA_INSTRUMENTOS = {
    "RA1": ["examen", "practica"],
    "RA2": ["examen", "practica"],
    "RA3": ["examen", "practica"],
    "RA4": ["examen", "practica"],
    "RA5": ["practica"],
    "RA6": ["empresa"],
}

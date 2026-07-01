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
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
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

# ─── CRITERIOS DE EVALUACIÓN (BOE RD 1629/2009) ──────────────────────────────
CES = {
    "RA1": [
        {"id": "CR1", "texto": "Se han descrito los principios de las comunicaciones entre dispositivos."},
        {"id": "CR2", "texto": "Se han identificado los estándares de comunicaciones en redes de área local."},
        {"id": "CR3", "texto": "Se han descrito las topologías de red y sus características."},
        {"id": "CR4", "texto": "Se han descrito los modelos de referencia OSI y TCP/IP."},
        {"id": "CR5", "texto": "Se han relacionado los modelos OSI y TCP/IP identificando los protocolos de cada capa."},
        {"id": "CR6", "texto": "Se ha descrito el encapsulamiento de la información en los distintos niveles de los modelos de referencia."},
        {"id": "CR7", "texto": "Se han identificado las principales tecnologías Ethernet y sus características."},
        {"id": "CR8", "texto": "Se ha analizado el direccionamiento en redes IPv4 e IPv6."},
    ],
    "RA2": [
        {"id": "CR1", "texto": "Se han instalado y configurado adaptadores de red."},
        {"id": "CR2", "texto": "Se han utilizado aplicaciones para configurar y verificar el direccionamiento en redes."},
        {"id": "CR3", "texto": "Se han conectado equipos y dispositivos de red utilizando distintos medios."},
        {"id": "CR4", "texto": "Se han instalado y configurado conmutadores."},
        {"id": "CR5", "texto": "Se han instalado y configurado puntos de acceso inalámbrico."},
        {"id": "CR6", "texto": "Se han establecido los parámetros de configuración de los dispositivos de red."},
        {"id": "CR7", "texto": "Se ha evaluado la idoneidad de distintos medios de transmisión para cada aplicación."},
    ],
    "RA3": [
        {"id": "CR1", "texto": "Se han descrito las funciones de los conmutadores en la red."},
        {"id": "CR2", "texto": "Se han configurado VLANs en un conmutador."},
        {"id": "CR3", "texto": "Se han configurado enlaces troncales entre conmutadores."},
        {"id": "CR4", "texto": "Se ha analizado y configurado el protocolo Spanning Tree."},
        {"id": "CR5", "texto": "Se han configurado protocolos de agregación de enlaces."},
        {"id": "CR6", "texto": "Se han aplicado medidas de seguridad en el acceso a los conmutadores."},
        {"id": "CR7", "texto": "Se han configurado listas de control de acceso en los puertos del conmutador."},
        {"id": "CR8", "texto": "Se ha verificado el funcionamiento de las VLANs en una red conmutada."},
    ],
    "RA4": [
        {"id": "CR1",  "texto": "Se han descrito las funciones y características de los routers."},
        {"id": "CR2",  "texto": "Se han configurado los parámetros básicos de un router."},
        {"id": "CR3",  "texto": "Se han configurado rutas estáticas."},
        {"id": "CR4",  "texto": "Se han configurado protocolos de enrutamiento dinámico (RIP, OSPF)."},
        {"id": "CR5",  "texto": "Se han configurado listas de control de acceso (ACL)."},
        {"id": "CR6",  "texto": "Se ha configurado el servicio NAT."},
        {"id": "CR7",  "texto": "Se han configurado interfaces WAN."},
        {"id": "CR8",  "texto": "Se han verificado los parámetros de configuración y funcionamiento del router."},
        {"id": "CR9",  "texto": "Se han documentado los procedimientos de configuración y las incidencias."},
        {"id": "CR10", "texto": "Se ha configurado el acceso a Internet desde una red local."},
        {"id": "CR11", "texto": "Se han configurado servicios DHCP en el router."},
        {"id": "CR12", "texto": "Se han configurado servicios DNS en el router."},
    ],
    "RA5": [
        {"id": "CR1", "texto": "Se han descrito los estándares de redes inalámbricas."},
        {"id": "CR2", "texto": "Se han descrito los modos de funcionamiento de las redes inalámbricas."},
        {"id": "CR3", "texto": "Se han configurado redes inalámbricas en modo infraestructura."},
        {"id": "CR4", "texto": "Se han aplicado protocolos de seguridad en redes inalámbricas."},
        {"id": "CR5", "texto": "Se han establecido parámetros de acceso de usuarios a la red inalámbrica."},
        {"id": "CR6", "texto": "Se ha verificado el funcionamiento de la red inalámbrica."},
    ],
    "RA6": [
        {"id": "CR1", "texto": "Se han descrito los procedimientos para el diagnóstico de incidencias."},
        {"id": "CR2", "texto": "Se han utilizado herramientas de diagnóstico de red."},
        {"id": "CR3", "texto": "Se han identificado las causas de problemas de conectividad."},
        {"id": "CR4", "texto": "Se han resuelto problemas de configuración de los dispositivos de red."},
        {"id": "CR5", "texto": "Se han aplicado medidas correctoras a las incidencias detectadas."},
        {"id": "CR6", "texto": "Se han documentado las incidencias y las soluciones aplicadas."},
        {"id": "CR7", "texto": "Se han interpretado los registros de los dispositivos de red."},
    ],
}

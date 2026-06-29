"""
EvalFP — Datos del módulo ISO (Implantación de Sistemas Operativos)
Módulo: 0369 · 1º ASIR · Ciclo: ASIR
Curso académico: 2026-2027

Este fichero contiene ÚNICAMENTE los datos del módulo.
Para añadir un nuevo módulo, copia este fichero, renómbralo y adapta las listas.
El generador (build_template.py) importa de aquí; no contiene datos de módulo.
"""

# ─── MÓDULO ──────────────────────────────────────────────────────────────────
MODULO = {
    "nombre":      "Implantación de Sistemas Operativos",
    "codigo":      "0369",
    "abrev":       "ISO",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "curso":       "1º ASIR",
    "horas_sem":   6,
    "total_horas": 186,
    "anno":        "2026-2027",
    "eval_count":  3,
}

# ─── UNIDADES DE TRABAJO ─────────────────────────────────────────────────────
# eval: evaluación en que se imparte (1, 2 o 3)
# horas: horas presenciales asignadas en la programación
# tags: tecnologías / contenidos clave (texto libre, aparece en Programación)
UTS = [
    {
        "id":     "UT1",
        "nombre": "Instalación de software libre y propietario",
        "horas":  30,
        "eval":   1,
        "tags":   "Linux · Windows Server · Virtualización",
    },
    {
        "id":     "UT2",
        "nombre": "Administración de software base",
        "horas":  25,
        "eval":   1,
        "tags":   "Usuarios · Red TCP/IP · Registro Windows",
    },
    {
        "id":     "UT3",
        "nombre": "Administración y aseguramiento de la información",
        "horas":  22,
        "eval":   2,
        "tags":   "Permisos · Backups · RAID",
    },
    {
        "id":     "UT4",
        "nombre": "Gestión de dominios",
        "horas":  30,
        "eval":   2,
        "tags":   "Active Directory · GPO · Perfiles",
    },
    {
        "id":     "UT5",
        "nombre": "Administración de acceso al dominio",
        "horas":  25,
        "eval":   2,
        "tags":   "Samba · NFS · NTFS / ACLs POSIX",
    },
    {
        "id":     "UT6",
        "nombre": "Supervisión del rendimiento del sistema",
        "horas":  22,
        "eval":   3,
        "tags":   "top/htop · Perfmon · journalctl",
    },
    {
        "id":     "UT7",
        "nombre": "Directivas de seguridad y auditorías",
        "horas":  22,
        "eval":   3,
        "tags":   "secpol.msc · auditd · fail2ban",
    },
    {
        "id":     "UT8",
        "nombre": "Resolución de incidencias y asistencia técnica",
        "horas":  10,
        "eval":   3,
        "tags":   "WDS/MDT · VPN WireGuard · ITIL",
    },
]

# ─── RESULTADOS DE APRENDIZAJE ───────────────────────────────────────────────
# pond: ponderación sobre la nota final del módulo (suma debe ser 100)
RAS = [
    {
        "id":     "RA1",
        "pond":   13,
        "nombre": "Instala sistemas operativos, relacionando sus características con el "
                  "hardware del equipo y el software de aplicación.",
    },
    {
        "id":     "RA2",
        "pond":   19,
        "nombre": "Gestiona el software de base, aplicando criterios de explotación del "
                  "sistema.",
    },
    {
        "id":     "RA3",
        "pond":    9,
        "nombre": "Asegura y recupera el sistema, aplicando procedimientos de "
                  "administración de la información.",
    },
    {
        "id":     "RA4",
        "pond":   16,
        "nombre": "Gestiona dominios, elaborando el modelo lógico de la red en un entorno "
                  "de trabajo.",
    },
    {
        "id":     "RA5",
        "pond":   13,
        "nombre": "Administra el acceso al dominio, gestionando servidores de directorio "
                  "y verificando el acceso de los usuarios.",
    },
    {
        "id":     "RA6",
        "pond":   12,
        "nombre": "Supervisa el rendimiento del sistema, diagnosticando las causas de "
                  "pérdidas de rendimiento.",
    },
    {
        "id":     "RA7",
        "pond":   13,
        "nombre": "Aplica directivas de seguridad y gestiona auditorías, interpretando "
                  "y aplicando la normativa vigente.",
    },
    {
        "id":     "RA8",
        "pond":    5,
        "nombre": "Establece la conexión en red de los sistemas informáticos, "
                  "configurando dispositivos y protocolos.",
    },
]

# ─── ASIGNACIONES UT → RA → CEs ──────────────────────────────────────────────
# Cada tupla: (id_ut, id_ra, [lista de CEs que se trabajan en esa UT para ese RA])
ASIGNACIONES = [
    ("UT1", "RA1", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT1", "RA2", ["CR7","CR8"]),
    ("UT2", "RA2", ["CR1","CR2","CR3","CR4","CR5","CR6","CR10","CR11","CR12",
                    "CR13","CR14","CR16","CR17","CR19"]),
    ("UT2", "RA7", ["CR1"]),
    ("UT3", "RA3", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3", "RA2", ["CR9","CR15","CR18"]),
    ("UT4", "RA4", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5", "RA5", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5", "RA7", ["CR1"]),
    ("UT6", "RA6", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT7", "RA7", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7", "RA5", ["CR8"]),
    ("UT8", "RA8", ["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]

# ─── EVALUACIÓN POR RA ───────────────────────────────────────────────────────
# RAs que se evalúan principalmente en cada evaluación
EVAL_RAS = {
    1: ["RA1", "RA2"],          # Eval 1: 13% + 19% = 32%
    2: ["RA3", "RA4", "RA5"],   # Eval 2:  9% + 16% + 13% = 38%
    3: ["RA6", "RA7", "RA8"],   # Eval 3: 12% + 13% + 5% = 30%
}

# ─── RA DUAL ─────────────────────────────────────────────────────────────────
# RA evaluado en modalidad dual (empresa + centro, LO 3/2022 art. 42)
DUAL_RA = "RA8"
DUAL_PCT_NOTA = 0.05   # Peso del RA dual sobre la nota final (5%)
DUAL_JUSTIFICACION = (
    "RA8 — Resolución de incidencias y asistencia técnica — se evalúa en modalidad DUAL "
    "de acuerdo con el artículo 42 de la Ley Orgánica 3/2022 de ordenación e integración "
    "de la FP, que obliga a dualizar un mínimo del 10% de los Resultados de Aprendizaje. "
    "Se ha seleccionado este RA por ser el de mayor aplicabilidad en entorno laboral real "
    "(gestión de incidencias ITIL, WDS/MDT, VPN, acceso remoto), el de menor peso "
    "ponderado (5% = 0,05 de la nota final) y el que más naturalmente puede ser evaluado "
    "por un tutor de empresa sin necesidad de instrumentos técnicos específicos del centro. "
    "La calificación la otorga el tutor/a de empresa y se incorpora directamente a la "
    "columna RA8 de la hoja 1ªORD.\n\n"
    "NOTA IMPORTANTE: En el caso de que este RA no llegue a impartirse en el centro "
    "educativo por falta de tiempo lectivo, la evaluación recae íntegramente (100%) en el "
    "tutor/a de empresa. Esta circunstancia está prevista y amparada por la modalidad dual: "
    "el alumno/a adquiere y demuestra los contenidos de este RA exclusivamente en el "
    "entorno de trabajo, y la calificación del tutor/a de empresa es la única que computa "
    "para este RA. El peso en la nota final del módulo sigue siendo el mismo: 5% (0,05)."
)

# ─── INSTRUMENTOS DE EVALUACIÓN POR RA ───────────────────────────────────────
# Instrumentos principales con los que se evalúa cada RA.
# "examen": prueba escrita/oral de teoría y práctica guiada
# "practica": actividad práctica, proyecto, entrega
# "empresa": evaluación por tutor/a de empresa (solo RA dual)
RA_INSTRUMENTOS = {
    "RA1": ["examen", "practica"],
    "RA2": ["examen", "practica"],
    "RA3": ["examen", "practica"],
    "RA4": ["examen", "practica"],
    "RA5": ["examen", "practica"],
    "RA6": ["examen", "practica"],
    "RA7": ["examen", "practica"],
    "RA8": ["empresa"],   # RA dual: solo evaluado por empresa
}

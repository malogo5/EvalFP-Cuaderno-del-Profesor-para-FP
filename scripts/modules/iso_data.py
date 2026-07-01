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
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
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

# ─── CRITERIOS DE EVALUACIÓN (BOE RD 1629/2009 + Orden CLM) ──────────────────
CES = {
    "RA1": [
        {"id": "CR1", "texto": "Se han identificado los elementos funcionales de un sistema informático."},
        {"id": "CR2", "texto": "Se ha verificado la idoneidad del hardware para la instalación del sistema operativo."},
        {"id": "CR3", "texto": "Se han realizado instalaciones de distintos sistemas operativos."},
        {"id": "CR4", "texto": "Se han previsto y resuelto incidencias en la instalación."},
        {"id": "CR5", "texto": "Se han utilizado herramientas para gestionar las particiones del disco duro."},
        {"id": "CR6", "texto": "Se han documentado los procesos de instalación."},
        {"id": "CR7", "texto": "Se han realizado instalaciones sobre sistemas arrancados desde la red."},
        {"id": "CR8", "texto": "Se han aplicado preferencias en la configuración de entornos de escritorio."},
    ],
    "RA2": [
        {"id": "CR1",  "texto": "Se han identificado los tipos de software presentes en el sistema."},
        {"id": "CR2",  "texto": "Se han satisfecho las necesidades de explotación del software instalado."},
        {"id": "CR3",  "texto": "Se han obtenido actualizaciones del sistema operativo y del software instalado."},
        {"id": "CR4",  "texto": "Se han realizado tareas de instalación y desinstalación de aplicaciones."},
        {"id": "CR5",  "texto": "Se han utilizado herramientas para la automatización de instalaciones."},
        {"id": "CR6",  "texto": "Se han evaluado las repercusiones de la elección de una determinada licencia."},
        {"id": "CR7",  "texto": "Se han documentado los procesos realizados."},
        {"id": "CR8",  "texto": "Se han documentado las aplicaciones instaladas y los cambios realizados."},
        {"id": "CR9",  "texto": "Se han efectuado copias de seguridad del software instalado y configurado."},
        {"id": "CR10", "texto": "Se han utilizado herramientas para la administración remota del software."},
        {"id": "CR11", "texto": "Se han gestionado los repositorios de software."},
        {"id": "CR12", "texto": "Se han realizado actualizaciones del sistema."},
        {"id": "CR13", "texto": "Se han configurado los procesos de inicio del sistema."},
        {"id": "CR14", "texto": "Se han administrado los usuarios del sistema."},
        {"id": "CR15", "texto": "Se han administrado los grupos del sistema."},
        {"id": "CR16", "texto": "Se han realizado gestiones del sistema de archivos."},
        {"id": "CR17", "texto": "Se han administrado procesos del sistema."},
        {"id": "CR18", "texto": "Se han utilizado herramientas de acceso remoto."},
        {"id": "CR19", "texto": "Se ha obtenido información sobre el rendimiento del sistema."},
    ],
    "RA3": [
        {"id": "CR1", "texto": "Se han identificado los elementos a salvaguardar."},
        {"id": "CR2", "texto": "Se han realizado copias de seguridad."},
        {"id": "CR3", "texto": "Se han recuperado sistemas desde copias de seguridad."},
        {"id": "CR4", "texto": "Se ha comprobado la integridad de las copias de seguridad."},
        {"id": "CR5", "texto": "Se han obtenido imágenes de sistemas en funcionamiento."},
        {"id": "CR6", "texto": "Se han restaurado imágenes de sistemas."},
        {"id": "CR7", "texto": "Se han aplicado políticas de contraseñas."},
        {"id": "CR8", "texto": "Se han evaluado las herramientas de cifrado disponibles para el sistema."},
    ],
    "RA4": [
        {"id": "CR1", "texto": "Se han identificado la función del servicio de directorio, sus elementos y terminología."},
        {"id": "CR2", "texto": "Se ha instalado el servicio de directorio."},
        {"id": "CR3", "texto": "Se ha configurado el acceso seguro al servicio de directorio."},
        {"id": "CR4", "texto": "Se han creado dominios."},
        {"id": "CR5", "texto": "Se ha comprobado el funcionamiento del dominio."},
        {"id": "CR6", "texto": "Se han creado unidades organizativas."},
        {"id": "CR7", "texto": "Se han realizado tareas de administración de cuentas y grupos."},
        {"id": "CR8", "texto": "Se han aplicado plantillas de seguridad."},
    ],
    "RA5": [
        {"id": "CR1", "texto": "Se han incorporado equipos al dominio."},
        {"id": "CR2", "texto": "Se han definido perfiles móviles de usuarios."},
        {"id": "CR3", "texto": "Se han utilizado herramientas para gestionar el directorio."},
        {"id": "CR4", "texto": "Se han delegado competencias de gestión."},
        {"id": "CR5", "texto": "Se han aplicado directivas de grupo."},
        {"id": "CR6", "texto": "Se han construido relaciones de confianza con otros dominios."},
        {"id": "CR7", "texto": "Se ha documentado la estructura del dominio y las tareas realizadas."},
        {"id": "CR8", "texto": "Se han aplicado directivas de seguridad entre dominios."},
    ],
    "RA6": [
        {"id": "CR1",  "texto": "Se han descrito los procedimientos para el seguimiento del rendimiento del sistema."},
        {"id": "CR2",  "texto": "Se han identificado los recursos del sistema susceptibles de monitorización."},
        {"id": "CR3",  "texto": "Se ha gestionado el subsistema de memoria."},
        {"id": "CR4",  "texto": "Se ha gestionado el subsistema de disco."},
        {"id": "CR5",  "texto": "Se ha gestionado el subsistema de red."},
        {"id": "CR6",  "texto": "Se ha gestionado el subsistema de proceso."},
        {"id": "CR7",  "texto": "Se han valorado distintas opciones para mejorar el rendimiento del sistema."},
        {"id": "CR8",  "texto": "Se han diagnosticado y resuelto los problemas de rendimiento."},
        {"id": "CR9",  "texto": "Se han descrito las estadísticas generadas."},
        {"id": "CR10", "texto": "Se han documentado los procedimientos de supervisión."},
    ],
    "RA7": [
        {"id": "CR1", "texto": "Se ha instalado y configurado un servidor de actualizaciones."},
        {"id": "CR2", "texto": "Se han descrito los tipos de registros disponibles en el sistema."},
        {"id": "CR3", "texto": "Se han activado los registros del sistema."},
        {"id": "CR4", "texto": "Se han establecido mecanismos de control remoto."},
        {"id": "CR5", "texto": "Se han documentado los procedimientos de seguridad utilizados."},
        {"id": "CR6", "texto": "Se han aplicado directivas de restricción de software."},
        {"id": "CR7", "texto": "Se han aplicado directivas de auditoría."},
        {"id": "CR8", "texto": "Se han generado informes de auditoría."},
        {"id": "CR9", "texto": "Se han aplicado filtros sobre los registros de auditoría."},
    ],
    "RA8": [
        {"id": "CR1", "texto": "Se han descrito los conceptos y los estándares de redes de área local."},
        {"id": "CR2", "texto": "Se han instalado y configurado los protocolos de red."},
        {"id": "CR3", "texto": "Se han configurado dispositivos de interconexión de redes."},
        {"id": "CR4", "texto": "Se han integrado equipos en una red existente."},
        {"id": "CR5", "texto": "Se ha comprobado el funcionamiento de la red."},
        {"id": "CR6", "texto": "Se han aplicado criterios de seguridad en la configuración de la red."},
        {"id": "CR7", "texto": "Se han diagnosticado y resuelto los problemas de red."},
        {"id": "CR8", "texto": "Se han compartido recursos en la red."},
        {"id": "CR9", "texto": "Se han utilizado herramientas de resolución de incidencias de red."},
    ],
}

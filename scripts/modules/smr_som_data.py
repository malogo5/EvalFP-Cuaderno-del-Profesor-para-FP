"""EvalFP — Sistemas Operativos Monopuesto (SOM) · 0222 · 1º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Sistemas Operativos Monopuesto","codigo":"0222","abrev":"SOM",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Instalación de sistemas operativos propietarios","horas":35,"eval":1,"tags":"Windows · BIOS/UEFI · Particiones · Activación · Drivers"},
    {"id":"UT2","nombre":"Gestión de sistemas operativos propietarios","horas":35,"eval":1,"tags":"Usuario · Grupos · Permisos NTFS · Registro · Tareas"},
    {"id":"UT3","nombre":"Instalación de sistemas operativos libres","horas":30,"eval":2,"tags":"Linux · Ubuntu · Debian · GRUB · Particionado LVM"},
    {"id":"UT4","nombre":"Gestión de sistemas operativos libres","horas":30,"eval":2,"tags":"Terminal · Bash · Permisos · Usuarios · Cron"},
    {"id":"UT5","nombre":"Explotación de sistemas operativos","horas":30,"eval":3,"tags":"Virtualización · VirtualBox · Scripts · Copias de seguridad"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Instala sistemas operativos propietarios, relacionando las características del hardware con los requisitos del software."},
    {"id":"RA2","pond":25,"nombre":"Gestiona la información del sistema identificando las posibilidades y los modos de acceso."},
    {"id":"RA3","pond":20,"nombre":"Instala y gestiona sistemas operativos libres, planificando el proceso e interpretando la documentación técnica."},
    {"id":"RA4","pond":20,"nombre":"Realiza tareas básicas de administración de sistemas operativos libres, interpretando las necesidades y aplicando los procedimientos establecidos."},
    {"id":"RA5","pond":15,"nombre":"Realiza operaciones básicas de administración de sistemas en entornos de virtualización."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los requisitos mínimos de instalación del sistema operativo.",
        "Se han configurado las particiones del disco duro durante la instalación.",
        "Se ha instalado el sistema operativo siguiendo el proceso establecido.",
        "Se han instalado los controladores de los dispositivos.",
        "Se ha activado el sistema operativo.",
        "Se ha documentado el proceso de instalación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los sistemas de ficheros compatibles.",
        "Se han gestionado los usuarios y grupos del sistema.",
        "Se han asignado y modificado permisos de acceso a archivos y carpetas.",
        "Se han utilizado herramientas de administración del sistema.",
        "Se han gestionado los servicios del sistema.",
        "Se han realizado copias de seguridad y restauración del sistema.",
        "Se han documentado las tareas de administración.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado el proceso de instalación de un sistema operativo libre.",
        "Se han configurado las particiones para el sistema libre.",
        "Se ha instalado el sistema operativo libre.",
        "Se ha configurado el gestor de arranque.",
        "Se han instalado los controladores necesarios.",
        "Se ha comprobado el correcto funcionamiento del sistema.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han gestionado usuarios y grupos desde la terminal.",
        "Se han asignado permisos mediante los comandos chmod y chown.",
        "Se han instalado y eliminado paquetes de software.",
        "Se han programado tareas con cron.",
        "Se han gestionado los procesos del sistema.",
        "Se han utilizado scripts de shell para automatizar tareas.",
        "Se han monitorizado los recursos del sistema.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características de los sistemas de virtualización.",
        "Se han instalado y configurado aplicaciones de virtualización.",
        "Se han creado máquinas virtuales.",
        "Se han instalado sistemas operativos en máquinas virtuales.",
        "Se han realizado instantáneas (snapshots) de las máquinas virtuales.",
    ], start=1)],
}

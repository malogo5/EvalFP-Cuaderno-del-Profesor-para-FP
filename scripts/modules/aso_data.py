"""
EvalFP — Administración de Sistemas Operativos (ASO)
Módulo: 0374 · 2º ASIR · Ciclo: ASIR
Decreto: RD 1629/2009, de 30 de octubre
"""

MODULO = {
    "nombre":      "Administración de Sistemas Operativos",
    "codigo":      "0374",
    "abrev":       "ASO",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "curso":       "2º ASIR",
    "horas_sem":   7,
    "total_horas": 224,
    "anno":        "2026-2027",
    "eval_count":  3,
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Administración de software de base","horas":28,"eval":1,"tags":"Paquetes · Repositorios · apt · yum · dnf"},
    {"id":"UT2","nombre":"Administración de información del sistema","horas":28,"eval":1,"tags":"Logs · Journald · Syslog · SNMP"},
    {"id":"UT3","nombre":"Administración de dominios","horas":35,"eval":1,"tags":"Active Directory · LDAP · Kerberos · DNS AD"},
    {"id":"UT4","nombre":"Administración de procesos del sistema","horas":28,"eval":2,"tags":"Cron · Systemd · Daemon · Prioridades"},
    {"id":"UT5","nombre":"Administración de cuotas y acceso a recursos","horas":28,"eval":2,"tags":"Cuotas · NFS · CIFS/SMB · ACLs avanzadas"},
    {"id":"UT6","nombre":"Accesibilidad y trabajo en red","horas":35,"eval":2,"tags":"SSH · VNC · RDP · X11 forwarding"},
    {"id":"UT7","nombre":"Resolución de incidencias del sistema","horas":42,"eval":3,"tags":"Troubleshooting · Arranque · Recovery · Virtualización"},
]

RAS = [
    {"id":"RA1","pond":12,"nombre":"Administra el software del sistema, aplicando criterios de explotación y utilizando las herramientas de gestión de paquetes."},
    {"id":"RA2","pond":14,"nombre":"Administra la información del sistema, identificando las herramientas de supervisión del sistema y describiendo su funcionamiento."},
    {"id":"RA3","pond":18,"nombre":"Administra dominios en red, realizando tareas de gestión y describiendo las herramientas utilizadas."},
    {"id":"RA4","pond":14,"nombre":"Administra el acceso a dominios, gestionando la autenticación y verificando el correcto funcionamiento del sistema."},
    {"id":"RA5","pond":14,"nombre":"Administra el acceso a recursos, utilizando servidores de ficheros e impresión."},
    {"id":"RA6","pond":14,"nombre":"Administra servidores de impresión y gestiona las colas de impresión."},
    {"id":"RA7","pond":14,"nombre":"Integra sistemas operativos libres y propietarios en redes heterogéneas, describiendo las características de cada sistema."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]

EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"], 3:["RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se han descrito los tipos de licencias de software."},
        {"id":"CR2","texto":"Se ha gestionado el software instalado en sistemas operativos libres."},
        {"id":"CR3","texto":"Se ha gestionado el software instalado en sistemas operativos propietarios."},
        {"id":"CR4","texto":"Se han utilizado herramientas para la gestión de paquetes."},
        {"id":"CR5","texto":"Se han gestionado los repositorios de software."},
        {"id":"CR6","texto":"Se han documentado los procesos de instalación y actualización del software."},
        {"id":"CR7","texto":"Se han instalado y configurado entornos de virtualización."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se han descrito los tipos de registros del sistema."},
        {"id":"CR2","texto":"Se han activado y configurado los registros del sistema."},
        {"id":"CR3","texto":"Se han utilizado herramientas de monitorización del rendimiento del sistema."},
        {"id":"CR4","texto":"Se han gestionado los mensajes del núcleo del sistema operativo."},
        {"id":"CR5","texto":"Se han configurado alertas para la supervisión del sistema."},
        {"id":"CR6","texto":"Se han utilizado herramientas gráficas de supervisión del sistema."},
        {"id":"CR7","texto":"Se han obtenido informes sobre el funcionamiento del sistema."},
        {"id":"CR8","texto":"Se han documentado los procedimientos de supervisión."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se han identificado la función del servicio de directorio, sus elementos y terminología."},
        {"id":"CR2","texto":"Se han instalado y configurado los servicios de directorio."},
        {"id":"CR3","texto":"Se han utilizado herramientas de administración del servicio de directorio."},
        {"id":"CR4","texto":"Se han creado y administrado usuarios, grupos y unidades organizativas."},
        {"id":"CR5","texto":"Se han realizado copias de seguridad del servicio de directorio."},
        {"id":"CR6","texto":"Se han restaurado el servicio de directorio a partir de copias de seguridad."},
        {"id":"CR7","texto":"Se han aplicado directivas de grupo en sistemas Windows."},
        {"id":"CR8","texto":"Se ha documentado la estructura del dominio y las tareas de administración realizadas."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han configurado sistemas de autenticación centralizados."},
        {"id":"CR2","texto":"Se ha configurado el protocolo LDAP."},
        {"id":"CR3","texto":"Se ha configurado el protocolo Kerberos."},
        {"id":"CR4","texto":"Se han creado y gestionado perfiles de usuario en entornos de red."},
        {"id":"CR5","texto":"Se han delegado competencias de administración."},
        {"id":"CR6","texto":"Se han integrado sistemas Linux en dominios Windows."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se han descrito las características de los sistemas de ficheros en red."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores de ficheros NFS."},
        {"id":"CR3","texto":"Se han instalado y configurado servidores de ficheros Samba."},
        {"id":"CR4","texto":"Se ha configurado el acceso a los recursos compartidos desde sistemas cliente."},
        {"id":"CR5","texto":"Se han establecido y comprobado las restricciones de acceso a los recursos."},
        {"id":"CR6","texto":"Se han gestionado cuotas de disco."},
        {"id":"CR7","texto":"Se han aplicado medidas de seguridad en el acceso a los recursos."},
        {"id":"CR8","texto":"Se han documentado los recursos compartidos y los permisos asignados."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han descrito las características de los sistemas de impresión en red."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores de impresión."},
        {"id":"CR3","texto":"Se han conectado impresoras a la red y configurado los controladores."},
        {"id":"CR4","texto":"Se han gestionado las colas de impresión."},
        {"id":"CR5","texto":"Se han establecido permisos de impresión."},
        {"id":"CR6","texto":"Se ha verificado el funcionamiento de la impresión en red."},
    ],
    "RA7": [
        {"id":"CR1","texto":"Se han identificado las ventajas de la integración de sistemas operativos diferentes en una red."},
        {"id":"CR2","texto":"Se han descrito las características de los sistemas de ficheros empleados por los sistemas operativos."},
        {"id":"CR3","texto":"Se han compartido recursos entre sistemas operativos diferentes."},
        {"id":"CR4","texto":"Se han identificado los problemas de interoperabilidad."},
        {"id":"CR5","texto":"Se han descrito las características de los sistemas heterogéneos."},
        {"id":"CR6","texto":"Se han instalado y configurado emuladores y máquinas virtuales."},
        {"id":"CR7","texto":"Se han documentado los procesos de integración de los sistemas."},
    ],
}

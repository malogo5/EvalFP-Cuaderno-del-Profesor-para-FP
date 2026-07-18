"""EvalFP — Sistemas Operativos en Red (SOA) · 0225 · 2º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Sistemas Operativos en Red","codigo":"0225","abrev":"SOA",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Instalación de sistemas operativos en red","horas":30,"eval":1,"tags":"Windows Server · Ubuntu Server · Roles · Servicios"},
    {"id":"UT2","nombre":"Gestión de dominios Windows","horas":35,"eval":1,"tags":"Active Directory · DNS · DHCP · GPO · Unidades organizativas"},
    {"id":"UT3","nombre":"Administración de usuarios y grupos en red","horas":25,"eval":2,"tags":"Perfiles · Carpetas · Cuotas · Directivas de grupo"},
    {"id":"UT4","nombre":"Recursos compartidos y servicios de red","horas":35,"eval":2,"tags":"SMB/CIFS · NFS · Impresoras · FTP · Web"},
    {"id":"UT5","nombre":"Integración de sistemas Linux en dominios Windows","horas":35,"eval":3,"tags":"Samba · LDAP · Autenticación · Winbind"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Instala sistemas operativos en red describiendo sus características e interpretando la documentación técnica."},
    {"id":"RA2","pond":25,"nombre":"Gestiona usuarios y grupos de sistemas operativos en red, describiendo las funciones que deben realizar y las herramientas disponibles."},
    {"id":"RA3","pond":20,"nombre":"Realiza tareas de gestión sobre dominios identificando las necesidades de la organización y aplicando los procedimientos necesarios."},
    {"id":"RA4","pond":20,"nombre":"Gestiona los recursos compartidos del sistema reconociendo y describiendo sus características."},
    {"id":"RA5","pond":15,"nombre":"Realiza tareas de monitorización y uso del sistema operativo en red describiendo las herramientas utilizadas e identificando las incidencias."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA3"], 2:["RA2","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los requisitos de instalación de sistemas operativos en red.",
        "Se han planificado las particiones y roles del servidor.",
        "Se ha instalado el sistema operativo en red.",
        "Se han configurado los servicios de red básicos.",
        "Se han actualizado los sistemas operativos de red.",
        "Se ha documentado el proceso de instalación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado y configurado cuentas de usuario.",
        "Se han creado y configurado grupos de usuarios.",
        "Se han establecido perfiles de usuario.",
        "Se han configurado carpetas particulares de usuario.",
        "Se han establecido cuotas de disco por usuario.",
        "Se han documentado las tareas de gestión de usuarios.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado y configurado los servicios de directorio.",
        "Se ha creado y configurado el dominio.",
        "Se han incorporado equipos al dominio.",
        "Se han creado unidades organizativas.",
        "Se han aplicado directivas de grupo (GPO).",
        "Se han configurado los servicios DNS y DHCP integrados.",
        "Se ha documentado la estructura del dominio.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado y configurado recursos compartidos.",
        "Se han establecido permisos de acceso a los recursos compartidos.",
        "Se han configurado impresoras compartidas en red.",
        "Se han instalado y configurado servidores de ficheros.",
        "Se han configurado servicios FTP y web.",
        "Se han verificado los accesos a los recursos compartidos.",
        "Se han documentado los recursos disponibles y sus permisos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han integrado sistemas Linux en dominios Windows mediante Samba.",
        "Se han accedido a recursos Windows desde clientes Linux.",
        "Se han compartido recursos Linux con clientes Windows.",
        "Se han resuelto incidencias de integración entre sistemas.",
        "Se ha documentado el proceso de integración.",
    ], start=1)],
}

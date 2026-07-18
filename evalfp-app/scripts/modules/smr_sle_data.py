"""EvalFP — Servicios en Red (SLE) · 0228 · 2º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Servicios en Red","codigo":"0228","abrev":"SLE",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Instalación y configuración de servicios DHCP y DNS","horas":25,"eval":1,"tags":"DHCP · DNS · BIND · Resolución de nombres"},
    {"id":"UT2","nombre":"Instalación y configuración de servidor web","horas":25,"eval":1,"tags":"Apache · Nginx · HTTP · HTTPS · Hosts virtuales"},
    {"id":"UT3","nombre":"Instalación y configuración de servidor FTP","horas":20,"eval":2,"tags":"FTP · FTPS · vsftpd · Permisos · Usuarios"},
    {"id":"UT4","nombre":"Instalación y configuración de servidor de correo","horas":25,"eval":2,"tags":"SMTP · POP3 · IMAP · Postfix · Webmail"},
    {"id":"UT5","nombre":"Instalación y configuración de servicios de acceso remoto","horas":33,"eval":3,"tags":"SSH · VNC · RDP · VPN · Escritorio remoto"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Instala y administra servicios de resolución de nombres en una red local, interpretando la documentación técnica."},
    {"id":"RA2","pond":20,"nombre":"Instala y administra servicios de transferencia de ficheros en una red local, aplicando criterios de seguridad."},
    {"id":"RA3","pond":20,"nombre":"Instala y administra servicios de correo electrónico en una red local, aplicando criterios de seguridad."},
    {"id":"RA4","pond":20,"nombre":"Instala y administra servicios de mensajería instantánea en una red local, verificando el correcto funcionamiento."},
    {"id":"RA5","pond":20,"nombre":"Instala y administra servicios de gestión remota en una red local, verificando el correcto funcionamiento."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA1",["CR7","CR8"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado y configurado servicios DHCP.",
        "Se han definido rangos de direcciones y parámetros del DHCP.",
        "Se han configurado reservas DHCP para equipos específicos.",
        "Se ha instalado y configurado un servidor DNS.",
        "Se han configurado las zonas de resolución directa e inversa.",
        "Se ha instalado y configurado un servidor web.",
        "Se han creado y configurado hosts virtuales.",
        "Se ha configurado HTTPS con certificado.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado y configurado un servidor FTP.",
        "Se han creado usuarios y configurado permisos de acceso FTP.",
        "Se ha configurado el acceso anónimo al servidor FTP.",
        "Se han configurado los modos activo y pasivo del FTP.",
        "Se ha implantado acceso seguro mediante FTPS.",
        "Se han realizado pruebas de funcionamiento desde clientes FTP.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado y configurado agentes de transporte de correo (MTA).",
        "Se han creado cuentas de correo.",
        "Se han configurado los protocolos POP3 e IMAP.",
        "Se han configurado los registros DNS necesarios (MX, SPF).",
        "Se ha instalado y configurado un servicio de webmail.",
        "Se han configurado filtros antispam.",
        "Se ha documentado la configuración del servidor de correo.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características de los servicios de mensajería instantánea.",
        "Se ha instalado y configurado un servidor de mensajería.",
        "Se han creado cuentas de usuario en el servidor.",
        "Se han realizado pruebas de funcionamiento.",
        "Se han documentado los parámetros de configuración.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado y configurado un servidor SSH.",
        "Se han configurado claves públicas para autenticación SSH.",
        "Se ha instalado y configurado acceso por escritorio remoto.",
        "Se ha instalado y configurado una VPN.",
        "Se han aplicado medidas de seguridad al acceso remoto.",
        "Se han documentado los procedimientos de acceso remoto.",
    ], start=1)],
}

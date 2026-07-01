"""
EvalFP — Servicios de Red e Internet (SRI)
Módulo: 0375 · 2º ASIR · Ciclo: ASIR
Decreto: RD 1629/2009, de 30 de octubre
"""

MODULO = {
    "nombre":      "Servicios de Red e Internet",
    "codigo":      "0375",
    "abrev":       "SRI",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "curso":       "2º ASIR",
    "horas_sem":   8,
    "total_horas": 256,
    "anno":        "2026-2027",
    "eval_count":  3,
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Implantación de servicios DHCP","horas":28,"eval":1,"tags":"DHCP · ISC DHCP · Windows DHCP · Reservas"},
    {"id":"UT2","nombre":"Implantación de servicios DNS","horas":35,"eval":1,"tags":"BIND · DNS · Zonas · Registros SOA · MX · CNAME"},
    {"id":"UT3","nombre":"Implantación de servidores web","horas":35,"eval":1,"tags":"Apache · Nginx · VirtualHosts · SSL/TLS · Let's Encrypt"},
    {"id":"UT4","nombre":"Implantación de servidores FTP","horas":21,"eval":2,"tags":"vsftpd · ProFTPD · FTPS · SFTP"},
    {"id":"UT5","nombre":"Implantación de servidores de correo electrónico","horas":35,"eval":2,"tags":"Postfix · Dovecot · SMTP · IMAP · POP3 · SpamAssassin"},
    {"id":"UT6","nombre":"Implantación de servidores de acceso remoto","horas":28,"eval":2,"tags":"SSH · OpenVPN · WireGuard · VPN IPSec"},
    {"id":"UT7","nombre":"Implantación de proxies y cortafuegos","horas":35,"eval":3,"tags":"Squid · iptables · nftables · pfSense"},
    {"id":"UT8","nombre":"Implantación de servidores de autenticación","horas":39,"eval":3,"tags":"RADIUS · 802.1X · NPS · FreeRADIUS"},
]

RAS = [
    {"id":"RA1","pond":10,"nombre":"Administra servicios de resolución de nombres (DHCP), describiendo sus funciones y verificando el servicio."},
    {"id":"RA2","pond":15,"nombre":"Administra servicios de resolución de nombres (DNS), describiendo sus funciones y verificando el servicio."},
    {"id":"RA3","pond":15,"nombre":"Administra servicios de transferencia de ficheros, asegurando el acceso, la disponibilidad y el control."},
    {"id":"RA4","pond":15,"nombre":"Administra servicios de correo electrónico, verificando su correcto funcionamiento y realizando tareas de seguridad."},
    {"id":"RA5","pond":15,"nombre":"Administra servicios de mensajería instantánea, noticias y listas de distribución, verificando el correcto funcionamiento del sistema."},
    {"id":"RA6","pond":15,"nombre":"Administra servicios de acceso y control remoto, evaluando su necesidad y verificando su acceso."},
    {"id":"RA7","pond":15,"nombre":"Administra servicios de almacenamiento, evaluando su necesidad y verificando su correcto funcionamiento."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA3",["CR9","CR10"]),
    ("UT5","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT7","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT8","RA7",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]

EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"], 3:["RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se ha descrito el servicio de resolución de nombres dinámica (DHCP) y su problemática."},
        {"id":"CR2","texto":"Se han establecido los rangos de direcciones y los parámetros de configuración."},
        {"id":"CR3","texto":"Se han configurado clientes estáticos DHCP."},
        {"id":"CR4","texto":"Se han implantado y comprobado opciones DHCP."},
        {"id":"CR5","texto":"Se han implantado varios agentes de retransmisión DHCP."},
        {"id":"CR6","texto":"Se han implantado servidores DHCP en sistemas operativos libres y propietarios."},
        {"id":"CR7","texto":"Se han documentado los parámetros de configuración del servicio."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se ha descrito el servicio de resolución de nombres (DNS) y su problemática."},
        {"id":"CR2","texto":"Se han identificado los registros DNS y su función."},
        {"id":"CR3","texto":"Se han resuelto consultas DNS de forma gráfica y comandos."},
        {"id":"CR4","texto":"Se ha implantado un servidor DNS primario."},
        {"id":"CR5","texto":"Se han configurado las zonas de resolución directa e inversa."},
        {"id":"CR6","texto":"Se han implantado servidores DNS secundarios."},
        {"id":"CR7","texto":"Se han configurado las distintas tipologías de servidores DNS."},
        {"id":"CR8","texto":"Se han implantado soluciones de DNS dinámico."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se ha descrito el servicio de transferencia de ficheros y su problemática."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores FTP."},
        {"id":"CR3","texto":"Se han creado usuarios y grupos para el acceso al servidor FTP."},
        {"id":"CR4","texto":"Se han configurado permisos de acceso."},
        {"id":"CR5","texto":"Se ha configurado el modo pasivo y activo del protocolo FTP."},
        {"id":"CR6","texto":"Se han realizado pruebas de funcionamiento con clientes gráficos."},
        {"id":"CR7","texto":"Se han implantado mecanismos de seguridad en el acceso al servicio FTP."},
        {"id":"CR8","texto":"Se han instalado y configurado servidores web Apache y Nginx."},
        {"id":"CR9","texto":"Se han creado y configurado hosts virtuales."},
        {"id":"CR10","texto":"Se han implantado certificados SSL/TLS."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han descrito los protocolos de correo electrónico (SMTP, POP3, IMAP)."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores de correo."},
        {"id":"CR3","texto":"Se han creado cuentas de usuario y alias."},
        {"id":"CR4","texto":"Se han configurado los registros DNS necesarios para el correo."},
        {"id":"CR5","texto":"Se han utilizado clientes de correo para pruebas."},
        {"id":"CR6","texto":"Se han instalado y configurado filtros antispam."},
        {"id":"CR7","texto":"Se han instalado y configurado filtros antivirus."},
        {"id":"CR8","texto":"Se han implantado servicios de webmail."},
        {"id":"CR9","texto":"Se han documentado los parámetros de configuración."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se han descrito los servicios proxy y sus tipos."},
        {"id":"CR2","texto":"Se han instalado y configurado servicios proxy."},
        {"id":"CR3","texto":"Se han configurado filtros de contenido."},
        {"id":"CR4","texto":"Se han implementado cortafuegos mediante iptables y nftables."},
        {"id":"CR5","texto":"Se han definido y aplicado políticas de filtrado."},
        {"id":"CR6","texto":"Se han documentado las reglas del cortafuegos."},
        {"id":"CR7","texto":"Se han realizado pruebas de funcionamiento y registro."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han descrito métodos de control y acceso remoto."},
        {"id":"CR2","texto":"Se han instalado y configurado servicios de acceso remoto SSH."},
        {"id":"CR3","texto":"Se ha utilizado la autenticación mediante clave pública/privada."},
        {"id":"CR4","texto":"Se han configurado túneles SSH."},
        {"id":"CR5","texto":"Se han instalado y configurado VPNs (OpenVPN, WireGuard)."},
        {"id":"CR6","texto":"Se han aplicado medidas de seguridad en el acceso remoto."},
        {"id":"CR7","texto":"Se han documentado los procedimientos de acceso remoto."},
    ],
    "RA7": [
        {"id":"CR1","texto":"Se han descrito los servicios de autenticación RADIUS."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores RADIUS."},
        {"id":"CR3","texto":"Se ha configurado la autenticación 802.1X."},
        {"id":"CR4","texto":"Se han integrado sistemas de autenticación con servicios de directorio."},
        {"id":"CR5","texto":"Se han establecido políticas de acceso a la red."},
        {"id":"CR6","texto":"Se han documentado los parámetros de configuración."},
    ],
}

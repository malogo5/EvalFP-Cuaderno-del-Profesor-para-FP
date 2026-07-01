"""
EvalFP — Seguridad y Alta Disponibilidad (SAD)
Módulo: 0378 · 2º ASIR · Ciclo: ASIR
Decreto: RD 1629/2009, de 30 de octubre
"""

MODULO = {
    "nombre":      "Seguridad y Alta Disponibilidad",
    "codigo":      "0378",
    "abrev":       "SAD",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "curso":       "2º ASIR",
    "horas_sem":   5,
    "total_horas": 160,
    "anno":        "2026-2027",
    "eval_count":  3,
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Adopción de pautas de seguridad informática","horas":20,"eval":1,"tags":"Amenazas · Vulnerabilidades · Normativa · RGPD · ENS"},
    {"id":"UT2","nombre":"Implantación de soluciones de alta disponibilidad","horas":25,"eval":1,"tags":"Clustering · Balanceo · RAID · Heartbeat · Pacemaker"},
    {"id":"UT3","nombre":"Implantación de técnicas de acceso remoto seguro","horas":25,"eval":1,"tags":"SSH · VPN · IPSec · TLS · Certificados digitales"},
    {"id":"UT4","nombre":"Implantación de cortafuegos y DMZ","horas":30,"eval":2,"tags":"iptables · nftables · pfSense · DMZ · IDS/IPS"},
    {"id":"UT5","nombre":"Implantación de servidores proxy","horas":20,"eval":2,"tags":"Squid · HAProxy · Reverse Proxy · WAF"},
    {"id":"UT6","nombre":"Implantación de soluciones de monitorización","horas":20,"eval":3,"tags":"Nagios · Zabbix · Grafana · Prometheus · SIEM"},
    {"id":"UT7","nombre":"Análisis forense informático","horas":20,"eval":3,"tags":"Evidencias · Autopsy · Volatility · Chain of Custody"},
]

RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce la legislación y normativa sobre seguridad y protección de datos valorando su importancia."},
    {"id":"RA2","pond":20,"nombre":"Implanta soluciones de alta disponibilidad valorando las opciones de configuración posibles."},
    {"id":"RA3","pond":15,"nombre":"Implanta técnicas de seguridad remota eligiendo algoritmos y parámetros de configuración."},
    {"id":"RA4","pond":20,"nombre":"Implanta cortafuegos perimetrales definiendo reglas de filtrado de paquetes."},
    {"id":"RA5","pond":10,"nombre":"Implanta servidores proxy, aplicando criterios de configuración que garanticen el funcionamiento seguro del servicio."},
    {"id":"RA6","pond":10,"nombre":"Implanta soluciones de alta disponibilidad en un servidor, evaluando las necesidades y configurando el sistema."},
    {"id":"RA7","pond":10,"nombre":"Reconoce la legislación y normativa sobre seguridad y protección de datos, identificando derechos y obligaciones."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5"]),
]

EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se ha valorado la importancia de mantener la información segura."},
        {"id":"CR2","texto":"Se han descrito las diferencias entre seguridad física y lógica."},
        {"id":"CR3","texto":"Se han definido los términos de amenaza, riesgo y vulnerabilidad."},
        {"id":"CR4","texto":"Se han clasificado las principales amenazas a los sistemas informáticos."},
        {"id":"CR5","texto":"Se ha descrito la legislación sobre protección de datos de carácter personal."},
        {"id":"CR6","texto":"Se ha descrito la legislación sobre los servicios de la sociedad de la información y firma electrónica."},
        {"id":"CR7","texto":"Se han identificado los organismos de referencia en ciberseguridad (INCIBE, CCN-CERT, ENISA)."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se han valorado las ventajas e inconvenientes de los sistemas de alta disponibilidad."},
        {"id":"CR2","texto":"Se han descrito los diferentes sistemas de almacenamiento utilizados en sistemas redundantes."},
        {"id":"CR3","texto":"Se han seleccionado sistemas de almacenamiento en función de sus características."},
        {"id":"CR4","texto":"Se han implantado sistemas RAID en diferentes niveles."},
        {"id":"CR5","texto":"Se han implantado soluciones de clustering activo-activo y activo-pasivo."},
        {"id":"CR6","texto":"Se han implantado soluciones de balanceo de carga."},
        {"id":"CR7","texto":"Se han evaluado las prestaciones del sistema."},
        {"id":"CR8","texto":"Se han implantado sistemas de acceso a datos de alta disponibilidad (NAS, SAN)."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se han clasificado las zonas de riesgo de un sistema según criterios establecidos."},
        {"id":"CR2","texto":"Se han configurado dispositivos y software de comunicaciones para dotar al sistema de acceso remoto seguro."},
        {"id":"CR3","texto":"Se han implantado redes privadas virtuales (VPN)."},
        {"id":"CR4","texto":"Se han implantado protocolos de autenticación seguros."},
        {"id":"CR5","texto":"Se han configurado protocolos criptográficos seguros (TLS/SSL)."},
        {"id":"CR6","texto":"Se han gestionado certificados digitales."},
        {"id":"CR7","texto":"Se han documentado los procedimientos y parámetros de configuración."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han descrito las características, tipos y funciones de los cortafuegos."},
        {"id":"CR2","texto":"Se han clasificado los niveles del cortafuegos."},
        {"id":"CR3","texto":"Se han diseñado filtros para un cortafuegos a partir de una política de seguridad."},
        {"id":"CR4","texto":"Se han implantado cortafuegos en equipos de conexión entre redes."},
        {"id":"CR5","texto":"Se han implantado zonas desmilitarizadas (DMZ)."},
        {"id":"CR6","texto":"Se han realizado diagnósticos de incidencias en cortafuegos."},
        {"id":"CR7","texto":"Se han auditado las reglas del cortafuegos."},
        {"id":"CR8","texto":"Se han implantado sistemas IDS/IPS."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se han descrito los tipos y características de los servidores proxy."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores proxy de tipo caché."},
        {"id":"CR3","texto":"Se han configurado filtros de contenido."},
        {"id":"CR4","texto":"Se han instalado y configurado proxies inversos."},
        {"id":"CR5","texto":"Se ha implantado un balanceador de carga."},
        {"id":"CR6","texto":"Se han documentado los procedimientos y parámetros de configuración."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han descrito los sistemas y herramientas de monitorización disponibles."},
        {"id":"CR2","texto":"Se han instalado y configurado herramientas de monitorización de red y sistemas."},
        {"id":"CR3","texto":"Se han configurado alertas y notificaciones."},
        {"id":"CR4","texto":"Se han generado informes de rendimiento y disponibilidad."},
        {"id":"CR5","texto":"Se han establecido procesos de respuesta ante incidencias."},
        {"id":"CR6","texto":"Se han implantado sistemas SIEM básicos."},
    ],
    "RA7": [
        {"id":"CR1","texto":"Se ha descrito el proceso de análisis forense."},
        {"id":"CR2","texto":"Se han identificado y preservado las evidencias digitales."},
        {"id":"CR3","texto":"Se han utilizado herramientas de análisis forense."},
        {"id":"CR4","texto":"Se han documentado los hallazgos del análisis forense."},
        {"id":"CR5","texto":"Se ha elaborado un informe forense respetando la cadena de custodia."},
    ],
}

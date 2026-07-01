"""
EvalFP — Implantación de Aplicaciones Web (IAW)
Módulo: 0376 · 2º ASIR · Ciclo: ASIR
Decreto: RD 1629/2009, de 30 de octubre
"""

MODULO = {
    "nombre":      "Implantación de Aplicaciones Web",
    "codigo":      "0376",
    "abrev":       "IAW",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "curso":       "2º ASIR",
    "horas_sem":   4,
    "total_horas": 128,
    "anno":        "2026-2027",
    "eval_count":  3,
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Implantación de arquitecturas web","horas":20,"eval":1,"tags":"Apache · Nginx · LAMP · LEMP · Virtualización · Docker"},
    {"id":"UT2","nombre":"Instalación y administración de servidores web","horas":25,"eval":1,"tags":"VirtualHosts · SSL · .htaccess · Módulos · PHP-FPM"},
    {"id":"UT3","nombre":"Instalación de gestores de contenidos (CMS)","horas":25,"eval":2,"tags":"WordPress · Joomla · Drupal · Moodle · Nextcloud"},
    {"id":"UT4","nombre":"Implantación de aplicaciones de ofimática web","horas":20,"eval":2,"tags":"LibreOffice Online · Collabora · NextCloud Office"},
    {"id":"UT5","nombre":"Implantación de aplicaciones de comercio electrónico","horas":20,"eval":3,"tags":"PrestaShop · WooCommerce · OpenCart · Pasarelas de pago"},
    {"id":"UT6","nombre":"Implantación de servicios de correo web y repositorios","horas":18,"eval":3,"tags":"Roundcube · Gitea · GitLab CE · CI/CD básico"},
]

RAS = [
    {"id":"RA1","pond":20,"nombre":"Implanta arquitecturas Web analizando y aplicando criterios de funcionalidad."},
    {"id":"RA2","pond":25,"nombre":"Gestiona servidores Web, evaluando y aplicando criterios de configuración para el acceso seguro a los servicios."},
    {"id":"RA3","pond":20,"nombre":"Implanta aplicaciones Web en servidores de aplicaciones, evaluando y aplicando criterios de configuración para el acceso seguro a los servicios."},
    {"id":"RA4","pond":20,"nombre":"Implanta gestores de contenidos, seleccionándolos y estableciéndolos según los requerimientos."},
    {"id":"RA5","pond":15,"nombre":"Implanta servicios de comercio electrónico analizando y aplicando criterios de configuración."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA3",["CR7","CR8"]),
]

EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se han analizado y valorado las tecnologías de desarrollo de aplicaciones web."},
        {"id":"CR2","texto":"Se han analizado los modelos de ejecución de aplicaciones web."},
        {"id":"CR3","texto":"Se ha valorado la importancia del escalado y la disponibilidad en aplicaciones web."},
        {"id":"CR4","texto":"Se han instalado y configurado plataformas para el alojamiento de aplicaciones web."},
        {"id":"CR5","texto":"Se han documentado los procedimientos de instalación y configuración."},
        {"id":"CR6","texto":"Se han implantado arquitecturas LAMP y LEMP."},
        {"id":"CR7","texto":"Se ha configurado la virtualización mediante contenedores Docker."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se han descrito los fundamentos y protocolos en los que se basa el funcionamiento del servidor web."},
        {"id":"CR2","texto":"Se han instalado y configurado servidores web."},
        {"id":"CR3","texto":"Se han creado y configurado sitios virtuales."},
        {"id":"CR4","texto":"Se han configurado los mecanismos de autenticación y control de acceso del servidor web."},
        {"id":"CR5","texto":"Se ha implantado SSL en el servidor web."},
        {"id":"CR6","texto":"Se han configurado módulos del servidor web."},
        {"id":"CR7","texto":"Se han configurado restricciones de acceso y navegación."},
        {"id":"CR8","texto":"Se han documentado los parámetros de configuración del servidor web."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se han instalado y configurado servidores de aplicaciones."},
        {"id":"CR2","texto":"Se han instalado y configurado intérpretes de lenguajes de script orientados al servidor."},
        {"id":"CR3","texto":"Se ha verificado la integración del intérprete con el servidor web."},
        {"id":"CR4","texto":"Se han instalado y configurado módulos del intérprete."},
        {"id":"CR5","texto":"Se han establecido mecanismos para el mantenimiento de la información entre solicitudes."},
        {"id":"CR6","texto":"Se han implantado aplicaciones web en el servidor de aplicaciones."},
        {"id":"CR7","texto":"Se han configurado sistemas de acceso a repositorios de código."},
        {"id":"CR8","texto":"Se han instalado y configurado sistemas de gestión de repositorios git."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han valorado los gestores de contenidos disponibles."},
        {"id":"CR2","texto":"Se han instalado gestores de contenidos."},
        {"id":"CR3","texto":"Se han configurado y personalizado gestores de contenidos."},
        {"id":"CR4","texto":"Se han creado y gestionado usuarios y roles en el gestor de contenidos."},
        {"id":"CR5","texto":"Se han instalado y configurado módulos y plugins."},
        {"id":"CR6","texto":"Se han realizado tareas de mantenimiento y actualización."},
        {"id":"CR7","texto":"Se ha implantado un sistema de plataforma educativa (LMS)."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se han analizado las características y requisitos de las aplicaciones de comercio electrónico."},
        {"id":"CR2","texto":"Se han instalado y configurado plataformas de comercio electrónico."},
        {"id":"CR3","texto":"Se han configurado catálogos de productos."},
        {"id":"CR4","texto":"Se han integrado pasarelas de pago."},
        {"id":"CR5","texto":"Se han aplicado medidas de seguridad."},
        {"id":"CR6","texto":"Se han documentado los procedimientos de instalación y configuración."},
    ],
}

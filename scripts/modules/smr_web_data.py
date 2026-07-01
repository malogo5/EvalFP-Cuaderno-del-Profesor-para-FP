"""EvalFP — Aplicaciones Web · 0227 · 2º SMR
RD 1691/2007, de 14 de diciembre (BOE) · Decreto CLM 107/2009, de 4 de agosto (DOCM)
"""
MODULO = {
    "nombre":"Aplicaciones Web","codigo":"0227","abrev":"AWEB",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Gestores de contenidos (CMS)","horas":35,"eval":1,"tags":"WordPress · Joomla · Drupal · Instalación · Temas · Plugins · Menús"},
    {"id":"UT2","nombre":"Administración y personalización de CMS","horas":35,"eval":2,"tags":"Usuarios · Roles · Módulos · SEO · Multiidioma · Copias de seguridad"},
    {"id":"UT3","nombre":"Plataformas e-learning","horas":30,"eval":2,"tags":"Moodle · Cursos · Actividades · Calificaciones · Usuarios · Roles"},
    {"id":"UT4","nombre":"Portales web y tiendas online","horas":30,"eval":3,"tags":"Prestashop · WooCommerce · Catálogo · Pedidos · Pagos · SEO"},
    {"id":"UT5","nombre":"Videoconferencia y streaming","horas":30,"eval":3,"tags":"Jitsi · BigBlueButton · OBS · RTMP · Codecs · Seguridad"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Instala gestores de contenidos, describiendo sus características y ajustando la configuración del servidor de aplicaciones."},
    {"id":"RA2","pond":20,"nombre":"Administra gestores de contenidos adaptando su apariencia y funcionalidades al propósito requerido."},
    {"id":"RA3","pond":20,"nombre":"Instala servicios de gestión de aprendizaje a distancia describiendo su estructura y realizando las configuraciones básicas."},
    {"id":"RA4","pond":20,"nombre":"Instala y administra portales web describiendo su estructura y funcionalidades básicas."},
    {"id":"RA5","pond":20,"nombre":"Instala y verifica sistemas de videoconferencia y streaming describiendo su función y verificando su funcionamiento."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características y funcionalidades de los gestores de contenidos.",
        "Se ha instalado el servidor web, el gestor de bases de datos y el intérprete de lenguaje de scripting necesarios.",
        "Se han instalado y configurado los gestores de contenidos.",
        "Se han creado usuarios administradores y se han asignado los permisos correspondientes.",
        "Se ha configurado la zona horaria, el idioma y el tipo de contenido del gestor.",
        "Se han descrito las funciones del panel de administración del gestor de contenidos.",
        "Se han aplicado criterios de seguridad en la instalación y configuración del servidor.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de temas y plantillas disponibles.",
        "Se ha modificado el aspecto del gestor de contenidos mediante temas y hojas de estilo.",
        "Se han instalado y configurado los módulos y plugins necesarios.",
        "Se han creado y organizado los contenidos: páginas, artículos, categorías y menús.",
        "Se han gestionado los usuarios, grupos y permisos del gestor.",
        "Se han realizado y restaurado copias de seguridad del gestor y su base de datos.",
        "Se han optimizado el gestor aplicando técnicas básicas de SEO y rendimiento.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características y funcionalidades de las plataformas de e-learning.",
        "Se ha instalado y configurado la plataforma de gestión del aprendizaje.",
        "Se han creado y configurado cursos, categorías y formatos de curso.",
        "Se han dado de alta usuarios y se han asignado los roles de administrador, profesor y alumno.",
        "Se han creado actividades y recursos dentro de los cursos: tareas, cuestionarios, foros y archivos.",
        "Se ha configurado el libro de calificaciones y los métodos de evaluación.",
        "Se han realizado copias de seguridad de los cursos y restaurado en otra plataforma.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características y funcionalidades de los portales y tiendas web.",
        "Se ha instalado y configurado la plataforma de comercio electrónico.",
        "Se han creado y configurado categorías, productos y atributos.",
        "Se han configurado los métodos de pago y de envío.",
        "Se han gestionado pedidos, clientes y el inventario de productos.",
        "Se ha personalizado la apariencia del portal mediante temas y widgets.",
        "Se han aplicado medidas de seguridad: certificado SSL, copias de seguridad y actualizaciones.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características de los sistemas de videoconferencia y streaming.",
        "Se ha instalado y configurado el servidor de videoconferencia.",
        "Se han creado salas virtuales y gestionado los permisos de acceso.",
        "Se ha configurado y verificado el sistema de streaming de audio y vídeo.",
        "Se han identificado los formatos y codecs de vídeo y audio más habituales.",
        "Se han aplicado medidas de seguridad en el acceso a las salas y la transmisión.",
    ], start=1)],
}

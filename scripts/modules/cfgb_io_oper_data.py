"""EvalFP — Operaciones Auxiliares para la Configuración y la Explotación · 3030 · 
Decreto 80/2014, de 01/08/2014, currículo del ciclo de Formación Profesional Básica de Informática de Oficina en Castilla-La Mancha (DOCM, NID 2014/10283) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 338 h · 8 h/semana · 2º IO.
"""
MODULO = {
    "nombre":"Operaciones Auxiliares para la Configuración y la Explotación","codigo":"3030","abrev":"OACE",
    "ciclo":"","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"2º IO","horas_sem":8,"total_horas":338,"anno":"2026-2027","eval_count":3,
    "horas_aula":200,  # el resto hasta 338 h es formación en empresa
    "decreto":"Decreto 80/2014, de 01/08/2014, currículo del ciclo de Formación Profesional Básica de Informática de Oficina en Castilla-La Mancha (DOCM, NID 2014/10283) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Configura equipos informáticos para su funcionamiento en un entorno…","horas":49,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Configura equipos informáticos para su funcionamiento en un entorno…","horas":48,"eval":2,"tags":""},
    {"id":"UT3","nombre":"Paquete ofimático básico","horas":48,"eval":2,"tags":"Procesador de texto · Hoja de cálculo · Presentaciones · PDF · Macros"},
    {"id":"UT4","nombre":"Utilidades de Internet","horas":55,"eval":3,"tags":"Navegador · Correo · Mensajería · Almacenamiento nube · Seguridad web"},
]
RAS = [
    {"id":"RA1","pond":24,"nombre":"Configura equipos informáticos para su funcionamiento en un entorno monousuario, identificando la funcionalidad de la instalación."},
    {"id":"RA2","pond":24,"nombre":"Configura equipos informáticos para su funcionamiento en un entorno de red, identificando los permisos del usuario."},
    {"id":"RA3","pond":24,"nombre":"Utiliza aplicaciones de un paquete ofimático, relacionándolas con sus aplicaciones."},
    {"id":"RA4","pond":28,"nombre":"Emplea utilidades proporcionadas por Internet, configurándolas e identificando su funcionalidad y prestaciones."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado los parámetros básicos de la instalación.",
        "Se han aplicado las preferencias en la configuración del entorno personal.",
        "Se han utilizado los elementos de la interfaz de usuario para preparar el entorno de trabajo.",
        "Se han reconocido los atributos y los permisos en el sistema de archivos y directorios.",
        "Se han identificado las funcionalidades para el manejo del sistema de archivos y periféricos",
        "Se han utilizado las herramientas del sistema operativo para explorar los soportes de almacenamiento de datos.",
        "Se han realizado operaciones básicas de protección (instalación de antivirus, realización de copias de seguridad, entre otras).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado preferencias en la configuración del entorno personal.",
        "Se han configurado y gestionado cuentas de usuario.",
        "Se ha comprobado la conectividad del servidor con los equipos del cliente.",
        "Se han utilizado los servicios para compartir recurso.",
        "Se han asignado permisos a los recursos del sistema que se van a compartir.",
        "Se ha accedido a los recursos compartidos.",
        "Se han aplicado normas básicas de seguridad sobre recursos compartidos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las funciones y características de un procesador de textos relacionándolas con los tipos de documentos a elaborar.",
        "Se han utilizado los procedimientos de creación, modificación y manipulación de documentos utilizando las herramientas del procesador de textos.",
        "Se ha formateado un texto mejorando su presentación utilizando distintos tipos de letras y alineaciones.",
        "Se han utilizado las funciones para guardar e imprimir documentos elaborados.",
        "Se han realizado operaciones básicas para el uso de aplicaciones ofimáticas de hoja de cálculo y base de datos, sobre documentos previamente elaborados.",
        "Se han identificado las funciones básicas una aplicación para presentaciones.",
        "Se han elaborado presentaciones multimedia aplicando normas básicas de composición y diseño.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado las herramientas para la navegación por páginas Web reconociendo la estructura de Internet.",
        "Se ha personalizado el navegador adecuándolo a las necesidades establecidas.",
        "Se ha transferido información utilizando los recursos de Internet para descargar, enviar y almacenar ficheros.",
        "Se han identificado los medios y procedimientos de seguridad durante el acceso a páginas web describiendo los riesgos y fraudes posibles.",
        "Se han descrito las funcionalidades que ofrecen las herramientas de correo electrónico.",
        "Se ha creado una cuenta de correo a través de un servidor web que proporcione el servicio.",
        "Se han utilizado otros servicios disponibles en Internet (foro, mensajería instantánea, redes p2p, videoconferencia; entre otros).",
        "Se han configurado las opciones básicas de las aplicaciones.",
    ], start=1)],
}

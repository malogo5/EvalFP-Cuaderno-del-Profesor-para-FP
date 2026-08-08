"""EvalFP — Puesta en Producción Segura · 5023 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 120 h · 4 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Puesta en Producción Segura","codigo":"5023","abrev":"PPS",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Prueba de aplicaciones web y móviles","horas":22,"eval":1,"tags":"Lenguajes · Modelos de ejecución · Código fuente · Tipos de prueba · Sandboxes"},
    {"id":"UT2","nombre":"Determinación del nivel de seguridad requerido","horas":17,"eval":1,"tags":"ASVS · Niveles de verificación · Requisitos · Análisis de riesgos"},
    {"id":"UT3","nombre":"Vulnerabilidades web: detección y corrección","horas":30,"eval":2,"tags":"OWASP Top Ten · Inyección · Sesiones · Roles · Criptografía · Bastionado del servidor web"},
    {"id":"UT4","nombre":"Seguridad en aplicaciones móviles","horas":21,"eval":2,"tags":"Permisos · Almacenamiento seguro · Compras integradas · Monitorización de tráfico · Análisis de binarios"},
    {"id":"UT5","nombre":"Despliegue seguro y automatización (DevSecOps)","horas":30,"eval":3,"tags":"Control de versiones · Integración continua · Automatización · Tolerancia a fallos · Recuperación ante desastres"},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Prueba aplicaciones web y aplicaciones para dispositivos móviles analizando la estructura del código y su modelo de ejecución."},
    {"id":"RA2","pond":14,"nombre":"Determina el nivel de seguridad requerido por aplicaciones identificando los vectores de ataque habituales y sus riesgos asociados."},
    {"id":"RA3","pond":25,"nombre":"Detecta y corrige vulnerabilidades de aplicaciones web analizando su código fuente y configurando servidores web."},
    {"id":"RA4","pond":18,"nombre":"Detecta problemas de seguridad en las aplicaciones para dispositivos móviles, monitorizando su ejecución y analizando ficheros y datos."},
    {"id":"RA5","pond":25,"nombre":"Implanta sistemas seguros de desplegado de software, utilizando herramientas para la automatización de la construcción de sus elementos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han comparado diferentes lenguajes de programación de acuerdo a sus características principales.",
        "Se han descrito los diferentes modelos de ejecución de software.",
        "Se han reconocido los elementos básicos del código fuente, dándoles significado.",
        "Se han ejecutado diferentes tipos de prueba de software.",
        "Se han evaluado los lenguajes de programación de acuerdo a la infraestructura de seguridad que proporcionan.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han caracterizado los niveles de verificación de seguridad en aplicaciones establecidos por los estándares internacionales (ASVS, “Application Security Verification Standard”).",
        "Se ha identificado el nivel de verificación de seguridad requerido por las aplicaciones en función de sus riesgos de acuerdo a estándares reconocidos.",
        "Se han enumerado los requisitos de verificación necesarios asociados al nivel de seguridad establecido.",
        "Se han reconocido los principales riesgos de las aplicaciones desarrolladas, en función de sus características.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han validado las entradas de los usuarios.",
        "Se han detectado riesgos de inyección tanto en el servidor como en el cliente.",
        "Se ha gestionado correctamente la sesión del usuario durante el uso de la aplicación.",
        "Se ha hecho uso de roles para el control de acceso.",
        "Se han utilizado algoritmos criptográficos seguros para almacenar las contraseñas de usuario.",
        "Se han configurado servidores web para reducir el riesgo de sufrir ataques conocidos.",
        "Se han incorporado medidas para evitar los ataques a contraseñas, envío masivo de mensajes o registros de usuarios a través de programas automáticos (bots).",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han comparado los diferentes modelos de permisos de las plataformas móviles.",
        "Se han descrito técnicas de almacenamiento seguro de datos en los dispositivos, para evitar la fuga de información.",
        "Se ha implantado un sistema de validación de compras integradas en la aplicación haciendo uso de validación en el servidor.",
        "Se han utilizado herramientas de monitorización de tráfico de red para detectar el uso de protocolos inseguros de comunicación de las aplicaciones móviles.",
        "Se han inspeccionado binarios de aplicaciones móviles para buscar fugas de información sensible.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características, principios y objetivos de la integración del desarrollo y operación del software.",
        "Se han implantado sistemas de control de versiones, administrando los roles y permisos solicitados.",
        "Se han instalado, configurado y verificado sistemas de integración continua, conectándolos con sistemas de control de versiones.",
        "Se han planificado, implementado y automatizado planes de desplegado de software.",
        "Se ha evaluado la capacidad del sistema desplegado para reaccionar de forma automática a fallos.",
        "Se han documentado las tareas realizadas y los procedimientos a seguir para la recuperación ante desastres.",
        "Se han creado bucles de retroalimentación ágiles entre los miembros del equipo.",
    ], start=1)],
}

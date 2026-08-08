"""EvalFP — Gestión avanzada de la información · 0663 · Asistencia a la Dirección
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.3º · RA y CE: Decreto 41/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 284 h · 6 h/semana · 2º AD.
"""
MODULO = {
    "nombre":"Gestión avanzada de la información","codigo":"0663","abrev":"GAI",
    "ciclo":"Asistencia a la Dirección","ciclo_clave":"AD","ciclo_nivel":"CFGS",
    "curso":"2º AD","horas_sem":6,"total_horas":284,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.3º · RA y CE: Decreto 41/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Gestión de proyectos con aplicaciones específicas","horas":50,"eval":1,"tags":"Tareas e hitos · Recursos · Diagrama de Gantt · Costes · Seguimiento"},
    {"id":"UT2","nombre":"Documentos integrados","horas":57,"eval":1,"tags":"Vinculación e incrustación · Plantillas corporativas · Gráficos · Maquetación · PDF"},
    {"id":"UT3","nombre":"Presentaciones audiovisuales","horas":64,"eval":1,"tags":"Guion · Diseño · Audio y vídeo · Publicación · Exposición"},
    {"id":"UT4","nombre":"Herramientas colaborativas y Web 2.0","horas":49,"eval":2,"tags":"Trabajo en la nube · Documentos compartidos · Formularios · Redes profesionales · Firma digital"},
    {"id":"UT5","nombre":"Sistemas de gestión documental","horas":64,"eval":2,"tags":"Metadatos · Flujos de trabajo · Versionado · Digitalización certificada · Conservación"},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Gestiona las facetas administrativas de proyectos empresariales, administrando recursos mediante una aplicación específica de control."},
    {"id":"RA2","pond":20,"nombre":"Elabora documentos, integrando textos, datos, imágenes y gráficos a través de las aplicaciones informáticas adecuadas."},
    {"id":"RA3","pond":23,"nombre":"Elabora presentaciones audiovisuales relacionadas con la gestión empresarial o de proyectos, utilizando una aplicación de tratamiento de vídeo digital."},
    {"id":"RA4","pond":17,"nombre":"Realiza tareas de gestión empresarial y de proyectos, empleando herramientas de la Web 2.0."},
    {"id":"RA5","pond":22,"nombre":"Administra los documentos a través de un sistema de gestión documental."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","proyecto"],
    "RA2":["practica","examen"],
    "RA3":["practica","proyecto"],
    "RA4":["practica"],
    "RA5":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha elaborado una propuesta de gestión administrativa de un proyecto acorde con los objetivos que se pretenden con el mismo.",
        "Se han definido las tareas que se deben llevar a cabo relacionadas con el soporte administrativo del proyecto.",
        "Se han identificado las actividades, tareas y plazos de entrega o finalización de cada una de las fases de los proyectos.",
        "Se han gestionado los recursos y requisitos (tiempos, costes, calidad, recursos humanos), así como los riesgos derivados del proyecto.",
        "Se ha supervisado y revisado cada una de las fases del proyecto.",
        "Se ha establecido la estructura organizativa, asignando los diferentes roles y responsabilidades.",
        "Se han redactado y presentado informes a los diversos agentes interesados en el proyecto (stakeholders).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha determinado el tipo de aplicación ofimática necesaria para la elaboración y presentación de documentos.",
        "Se han elaborado plantillas específicas adaptadas al tipo de documento que se va a elaborar.",
        "Se han realizado las macros adecuadas para la automatización de trabajos repetitivos.",
        "Se han seleccionado los datos adecuados para la integración del documento.",
        "Se ha efectuado la combinación de la correspondencia a través de la selección de los datos necesarios.",
        "Se han utilizado páginas web para la obtención de posibles gráficos, diagramas o dibujos.",
        "Se han confeccionado documentos organizados con formato y presentación adecuados.",
        "Se ha presentado y publicado el trabajo final según los requerimientos de tiempo y forma.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha determinado el equipamiento y material necesario.",
        "Se ha efectuado un guion para la producción audiovisual.",
        "Se han descrito los formatos de audio y vídeo más habituales",
        "Se han seleccionado y ordenado los clips de audio y vídeo.",
        "Se han introducido los archivos de audio digital en la aplicación informática.",
        "Se han editado los archivos de audio y vídeo digital en la aplicación informática.",
        "Se han insertado los títulos y rótulos necesarios en la aplicación informática.",
        "Se ha efectuado la autoría y generación de la presentación en soporte óptico.",
        "Se ha efectuado la conversión a otros formatos aptos para su difusión por Internet.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado aplicaciones web para la gestión de mensajería electrónica.",
        "Se han realizado comunicaciones mediante aplicaciones web de telefonía y videoconferencia de bajo coste.",
        "Se han manejado calendarios y agendas de compromisos mediante aplicaciones web.",
        "Se han utilizado aplicaciones de ofimática colaborativa a través de aplicaciones web.",
        "Se han creado páginas web corporativas a través de las posibilidades de las aplicaciones web.",
        "Se han gestionado comunicaciones mediante mensajería instantánea a través de aplicaciones web.",
        "Se han realizado diversas gestiones empresariales a través de una aplicación web de oficina virtual.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado los elementos que componen un sistema de gestión documental: bases de datos documentales, hardware, software, redes, usuarios y administradores.",
        "Se han escaneado documentos mediante programas de gestión documental.",
        "Se han almacenado, clasificado y recuperado documentos, siguiendo los parámetros establecidos.",
        "Se han establecido mecanismos de custodia de los documentos.",
        "Se han diseñado reglas para el flujo de documentos entre diversos puestos de la organización: workflow.",
        "Se han caracterizado los condicionantes de tiempo y forma en la distribución de documentos.",
        "Se han diseñado mecanismos de colaboración en la creación de documentos compartidos: workflow.",
        "Se han cumplimentado los estándares de autenticación de los documentos ante las diferentes instancias (públicas y privadas).",
        "Se ha valorado la contribución de los programas de gestión documental a la conservación del medio ambiente.",
    ], start=1)],
}

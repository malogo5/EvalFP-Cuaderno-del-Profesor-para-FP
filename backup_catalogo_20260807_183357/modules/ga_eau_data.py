"""EvalFP — Empresa en el aula · 0446 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 145 h · 7 h/semana · 2º GA.
"""
MODULO = {
    "nombre":"Empresa en el aula","codigo":"0446","abrev":"EAU",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"2º GA","horas_sem":7,"total_horas":145,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"El proyecto de empresa en el aula","horas":18,"eval":1,"tags":"Actividad y sector · Organigrama · Puestos y rotación · Plan de empresa"},
    {"id":"UT2","nombre":"Comunicación interna y externa","horas":23,"eval":1,"tags":"Atención telefónica · Correo · Circulares · Registro · Trato a la clientela"},
    {"id":"UT3","nombre":"Organización de la información","horas":18,"eval":1,"tags":"Archivo manual e informático · Bases de datos · Copias de seguridad · Confidencialidad"},
    {"id":"UT4","nombre":"Documentación por departamentos","horas":21,"eval":2,"tags":"Compras · Ventas · Almacén · Tesorería · RRHH · Contabilidad"},
    {"id":"UT5","nombre":"Gestión comercial de compras y ventas","horas":18,"eval":2,"tags":"Proveedores · Pedidos · Facturación · Cobros · Atención a la clientela"},
    {"id":"UT6","nombre":"Resolución de incidencias y reclamaciones","horas":18,"eval":2,"tags":"Criterios de resolución · Procedimiento · Registro · Seguimiento · Satisfacción"},
    {"id":"UT7","nombre":"Trabajo en equipo y desempeño profesional","horas":29,"eval":2,"tags":"Roles · Responsabilidad · Iniciativa · Autoevaluación · Rúbricas de desempeño"},
]
RAS = [
    {"id":"RA1","pond":12,"nombre":"Identifica las características del proyecto de empresa creada en el aula tomando parte en la actividad que esta desarrolla."},
    {"id":"RA2","pond":17,"nombre":"Transmite información entre las distintas áreas y a clientela interna y externa de la empresa creada en el aula reconociendo y aplicando técnicas de comunicación."},
    {"id":"RA3","pond":12,"nombre":"Organiza información explicando los diferentes métodos manuales y sistemas informáticos previstos."},
    {"id":"RA4","pond":14,"nombre":"Elabora documentación administrativa, distinguiendo y aplicando las tareas administrativas de cada uno de los departamentos de la empresa."},
    {"id":"RA5","pond":12,"nombre":"Realiza las actividades derivadas de la política comercial, identificando las funciones del departamento de ventas y compras."},
    {"id":"RA6","pond":12,"nombre":"Atiende incidencias identificando criterios y procedimientos de resolución de problemas y reclamaciones."},
    {"id":"RA7","pond":21,"nombre":"Trabaja en equipo reconociendo y valorando las diferentes aportaciones de cada uno de los miembros del grupo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","proyecto"],
    "RA2":["practica","proyecto"],
    "RA3":["practica","proyecto"],
    "RA4":["practica","proyecto"],
    "RA5":["practica","proyecto"],
    "RA6":["practica","proyecto"],
    "RA7":["practica","proyecto"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características internas y externas de la empresa creada en el aula.",
        "Se han identificado los elementos que constituyen la red logística de la empresa creada: proveedores, clientela, sistemas de producción y/o comercialización, almacenaje, y otros.",
        "Se han identificado los procedimientos de trabajo en el desarrollo del proceso productivo o comercial.",
        "Se han relacionado características del mercado, tipo de clientela y proveedores y su posible influencia en el de - sarrollo de la actividad empresarial.",
        "Se ha valorado la polivalencia de los puestos de trabajo administrativos en el desarrollo de la actividad de la empresa.",
        "Se ha integrado en la empresa creada en el aula, describiendo su relación con el sector, su estructura organizativa y las funciones de cada departamento.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado la forma y técnicas adecuadas en la atención y asesoramiento a clientela interna y externa con la empresa.",
        "Se ha mantenido una actitud correcta en la atención y asesoramiento a clientes internos y externos con la em - presa.",
        "Se ha transmitido la información de forma clara y precisa.",
        "Se ha utilizado el tratamiento protocolario adecuado.",
        "Se han identificado emisor y receptor en una conversación telefónica o presencial.",
        "Se ha identificado al remitente y destinatario en comunicaciones escritas recibidas.",
        "Se ha registrado la información relativa a las consultas realizadas en la herramienta de gestión de la relación con el cliente.",
        "Se han aplicado técnicas de negociación básicas con clientela y proveedores.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado procedimientos adecuados para la obtención de información necesaria en la gestión de control de calidad del servicio prestado.",
        "Se ha tramitado correctamente la información ante la persona o departamento de la empresa que corresponda.",
        "Se han aplicado las técnicas de organización de la información.",
        "Se ha analizado y sintetizado la información suministrada.",
        "Se ha manejado como usuario la aplicación informática de control y seguimiento de clientes, proveedores y otros.",
        "Se han aplicado las técnicas de archivo manuales e informáticas predecididas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han ejecutado las tareas administrativas del área de aprovisionamiento de la empresa.",
        "Se han ejecutado las tareas administrativas del área comercial de la empresa.",
        "Se han ejecutado las tareas administrativas del área de recursos humanos de la empresa.",
        "Se han ejecutado las tareas administrativas del área de contabilidad de la empresa.",
        "Se han ejecutado las tareas administrativas del área financiera de la empresa.",
        "Se han ejecutado las tareas administrativas del área fiscal de la empresa.",
        "Se ha aplicado la normativa vigente.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha elaborado y/o actualizado el catálogo de productos de la empresa.",
        "Se ha manejado la base de datos de proveedores, comparando ofertas y estableciendo negociaciones de condi - ciones de compras.",
        "Se han elaborado y/o actualizado las fichas de los clientes.",
        "Se han elaborado listas de precios.",
        "Se han confeccionado ofertas.",
        "Se han identificado los canales de comercialización más frecuentes en la actividad específica.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado la naturaleza y el origen de los problemas y reclamaciones.",
        "Se ha identificado la documentación que se utiliza para recoger una reclamación.",
        "Se han aplicado técnicas de comportamiento asertivo, resolutivo y positivo.",
        "Se han buscado y propuesto soluciones a la resolución de los problemas.",
        "Se ha seguido el proceso establecido para una reclamación.",
        "Se ha verificado que el proceso de reclamación se ha seguido íntegramente.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha mantenido una actitud de respeto al profesor/a-gerente y a los compañeros y compañeras.",
        "Se han cumplido las órdenes recibidas.",
        "Se ha mantenido una comunicación fluida con los compañeros y compañeras.",
        "Se han expuesto opiniones y puntos de vista ante una tarea.",
        "Se ha valorado la organización de la propia tarea.",
        "Se ha complementado el trabajo entre los compañeros y compañeras.",
        "Se ha transmitido la imagen de la empresa.",
        "Se ha realizado cada tarea con rigurosidad y corrección para obtener un resultado global satisfactorio",
        "Se han respetado las normas establecidas y la cultura empresarial.",
        "Se ha mantenido una actitud proactiva, participando en el grupo y desarrollando iniciativa emprendedora.",
    ], start=1)],
}

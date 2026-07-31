"""EvalFP — Aplicaciones básicas de ofimática · 3002 · Servicios Administrativos
Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 387 h · 9 h/semana · 2º SA.
"""
MODULO = {
    "nombre":"Aplicaciones básicas de ofimática","codigo":"3002","abrev":"ABO",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"2º SA","horas_sem":9,"total_horas":387,"anno":"2026-2027","eval_count":3,
    "horas_aula":225,  # el resto hasta 387 h es formación en empresa
    "decreto":"Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Internet e intranet en la oficina","horas":61,"eval":1,"tags":"Navegador · Búsquedas · Descargas · Certificado digital · Seguridad en la red"},
    {"id":"UT2","nombre":"Correo electrónico y agenda","horas":60,"eval":1,"tags":"Cuentas · Mensajes y adjuntos · Libreta de direcciones · Filtros · Agenda y tareas"},
    {"id":"UT3","nombre":"Hoja de cálculo","horas":52,"eval":2,"tags":"Celdas y rangos · Fórmulas y funciones básicas · Formatos · Gráficos · Impresión"},
    {"id":"UT4","nombre":"Presentaciones gráficas","horas":52,"eval":3,"tags":"Diapositivas · Plantillas · Imágenes y transiciones · Notas · Exposición"},
]
RAS = [
    {"id":"RA1","pond":27,"nombre":"Tramita información en línea aplicando herramientas de Internet, intranet y otras redes."},
    {"id":"RA2","pond":27,"nombre":"Realiza comunicaciones internas y externas mediante las utilidades de correo electrónico siguiendo las pautas marcadas."},
    {"id":"RA3","pond":23,"nombre":"Elabora documentos utilizando las aplicaciones básicas de hojas de cálculo."},
    {"id":"RA4","pond":23,"nombre":"Elabora presentaciones gráficas utilizando aplicaciones informáticas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["practica"],
    "RA3":["practica","examen"],
    "RA4":["practica","proyecto"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las distintas redes informáticas a las que podemos acceder.",
        "Se han diferenciado distintos métodos de búsqueda de información en redes informáticas.",
        "Se ha accedido a información a través de Internet, intranet, y otras redes de área local.",
        "Se han localizado documentos utilizando herramientas de Internet.",
        "Se han situado y recuperado archivos almacenados en servicios de alojamiento de archivos compartidos (“la nube”).",
        "Se ha comprobado la veracidad de la información localizada.",
        "Se ha valorado la utilidad de páginas institucionales y de Internet en general para la realización de trámites administrativos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes procedimientos de trasmisión y recepción de mensajes internos y externos.",
        "Se ha utilizado el correo electrónico para enviar y recibir mensajes, tanto internos como externos.",
        "Se han anexado documentos, vínculos, entre otros en mensajes de correo electrónico.",
        "Se han empleado las utilidades del correo electrónico para clasificar contactos y listas de distribución de información entre otras.",
        "Se han aplicado criterios de prioridad, importancia y seguimiento entre otros en el envío de mensajes siguiendo las instrucciones recibidas.",
        "Se han comprobado las medidas de seguridad y confidencialidad en la custodia o envío de información siguiendo pautas prefijadas.",
        "Se ha organizado la agenda incluyendo tareas, avisos y otras herramientas de planificación del trabajo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado los diversos tipos de datos y referencia para celdas, rangos, hojas y libros.",
        "Se han aplicado fórmulas y funciones básicas.",
        "Se han generado y modificado gráficos de diferentes tipos.",
        "Se ha utilizado la hoja de cálculo como base de datos sencillos.",
        "Se ha utilizado aplicaciones y periféricos para introducir textos, números, códigos e imágenes.",
        "Se han aplicado las reglas de ergonomía y salud en el desarrollo de las actividades.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las opciones básicas de las aplicaciones de presentaciones.",
        "Se reconocen los distintos tipos de vista asociados a una presentación.",
        "Se han aplicado y reconocido las distintas tipografías y normas básicas de composición, diseño y utilización del color.",
        "Se han creado presentaciones sencillas incorporando texto, gráficos, objetos y archivos multimedia.",
        "Se han diseñado plantillas de presentaciones.",
        "Se han utilizado periféricos para ejecutar presentaciones asegurando el correcto funcionamiento.",
    ], start=1)],
}

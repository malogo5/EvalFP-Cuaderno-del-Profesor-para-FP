"""EvalFP — Sistemas de Big Data · 5074 · CE Inteligencia Artificial y Big Data
Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM, NID 2022/6683) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 100 h · 3 h/semana · CE IA y Big Data.
"""
MODULO = {
    "nombre":"Sistemas de Big Data","codigo":"5074","abrev":"SBD",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":3,"total_horas":100,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM, NID 2022/6683) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Aplica técnicas de análisis de datos que integran","horas":30,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Configura cuadros de mando en diferentes entornos computacionales…","horas":22,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Gestiona y almacena datos facilitando la búsqueda de respuestas en…","horas":22,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Aplica herramientas para la visualización de datos utilizadas en las…","horas":26,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Aplica técnicas de análisis de datos que integran, procesan y analizan la información, adaptando e implementando sistemas que las utilicen."},
    {"id":"RA2","pond":22,"nombre":"Configura cuadros de mando en diferentes entornos computacionales usando técnicas de análisis de datos."},
    {"id":"RA3","pond":22,"nombre":"Gestiona y almacena datos facilitando la búsqueda de respuestas en grandes conjuntos de datos."},
    {"id":"RA4","pond":26,"nombre":"Aplica herramientas para la visualización de datos utilizadas en las soluciones Big Data facilitando las tareas de análisis y presentación de resultados."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","proyecto"],
    "RA2":["practica","proyecto"],
    "RA3":["practica","proyecto"],
    "RA4":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado conceptos básicos de matemática discreta, lógica algorítmica y complejidad computacional, y su aplicación para el tratamiento automático de la información por medio de sistemas computacionales.",
        "Se ha extraído de forma automática información y conocimiento a partir de grandes volúmenes de datos.",
        "Se han combinado diferentes fuentes y tipos de datos.",
        "Se ha construido un conjunto de datos complejos y se han relacionado entre sí.",
        "Se han establecido objetivos y prioridades, secuenciación y organización del tiempo de realización.",
        "Se han seleccionado e integrado sistemas de información que satisfacen las necesidades del problema.",
        "Se han determinado criterios de coste y calidad necesarios para la eficacia y eficiencia de la implementación de un sistema Big Data.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado diferentes librerías e implementaciones de las técnicas de representación de la información.",
        "Se ha cruzado información sobre el objetivo a conseguir y la naturaleza de los datos.",
        "Se ha realizado un cuadro de mandos utilizando técnicas sencillas.",
        "Se han utilizado técnicas predictivas complejas para anticiparse a lo que ocurra.",
        "Se ha evaluado el impacto del análisis de datos en la consecución de los objetivos propuestos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han extraído y almacenado datos de diversas fuentes, para ser tratados en distintos escenarios.",
        "Se ha fijado el objetivo de extraer valor de los datos para lo que es necesario contar con tecnologías eficientes.",
        "Se ha comprobado que la revolución digital exige poder almacenar y procesar ingentes cantidades de datos de distinto tipo y descubrir su valor.",
        "Se han desarrollado sistemas de gestión, almacenamiento y procesamiento de grandes volúmenes de datos de manera eficiente y segura, teniendo en cuenta la normativa existente.",
        "Se han utilizado habilidades científicas en entornos de trabajo multidisciplinares.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han examinado distintos escenarios y tipologías de datos no estructurados.",
        "Se ha implantado la aplicación de la BI (Business Intelligence) para la extracción de valor.",
        "Se ha reconocido la importancia de almacenar grandes volúmenes de datos de forma distribuida y redundante en un clúster de máquinas.",
        "Se han determinado las diferencias en el entorno de aplicaciones relacionadas que facilitan el procesamiento de datos de manera rápida, eficiente y eficaz.",
        "Se ha comprobado la manera de programar y procesar automáticamente la estructura de datos.",
        "Se han valorado las diferentes formas de visualizar los datos que nos interese representar gráficamente, facilitando así las tareas de análisis y presentación de resultados.",
    ], start=1)],
}

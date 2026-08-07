"""EvalFP — Big Data aplicado · 5075 · CE Inteligencia Artificial y Big Data
Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM, NID 2022/6683) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 140 h · 4 h/semana · CE IA y Big Data.
"""
MODULO = {
    "nombre":"Big Data aplicado","codigo":"5075","abrev":"BDA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":4,"total_horas":140,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM, NID 2022/6683) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Gestiona soluciones a problemas propuestos","horas":27,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Gestiona sistemas de almacenamiento y el amplio ecosistema alrededor…","horas":27,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Genera mecanismos de integridad de los datos","horas":22,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Realiza el seguimiento de la monitorización de un sistema","horas":32,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Valida las técnicas de Big Data para transformar una gran cantidad…","horas":32,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":19,"nombre":"Gestiona soluciones a problemas propuestos, utilizando sistemas de almacenamiento y herramientas asociadas al centro de datos."},
    {"id":"RA2","pond":19,"nombre":"Gestiona sistemas de almacenamiento y el amplio ecosistema alrededor de ellos facilitando el procesamiento de grandes cantidades de datos sin fallos y de forma rápida."},
    {"id":"RA3","pond":16,"nombre":"Genera mecanismos de integridad de los datos, comprobando su mantenimiento en los sistemas de ficheros distribuidos y valorando la sobrecarga que conlleva en el tratamiento de los datos."},
    {"id":"RA4","pond":23,"nombre":"Realiza el seguimiento de la monitorización de un sistema, asegurando la fiabilidad y estabilidad de los servicios que se proveen."},
    {"id":"RA5","pond":23,"nombre":"Valida las técnicas de Big Data para transformar una gran cantidad de datos en información significativa, facilitando la toma de decisiones de negocios."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["proyecto","presentacion"],
    "RA2":["proyecto","presentacion"],
    "RA3":["proyecto","presentacion"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha caracterizado el proceso de diseño y construcción de soluciones en sistemas de almacenamiento de datos.",
        "Se han determinado los procedimientos y mecanismos para la ingestión de datos.",
        "Se ha determinado el formato de datos adecuado para el almacenamiento.",
        "Se han procesado los datos almacenados,",
        "Se han presentado los resultados y las soluciones al cliente final en una forma fácil de interpretar.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha determinado la importancia de los sistemas de almacenamiento para depositar y procesar grandes cantidades de cualquier tipo de datos rápidamente.",
        "Se ha comprobado el poder de procesamiento de su modelo de computación distribuida.",
        "Se ha probado la tolerancia a fallos de los sistemas.",
        "Se ha determinado que se pueden almacenar tantos datos como se desee y decidir cómo utilizarlos más tarde.",
        "Se ha visualizado que el sistema puede crecer fácilmente añadiendo módulos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de la calidad de los datos en los sistemas de ficheros distribuidos.",
        "Se ha valorado que a mayor volumen de tratamiento de datos corresponde un mayor peligro relacionado con la integridad de los datos.",
        "Se ha reconocido que los sistemas de ficheros distribuidos implementan una suma de verificación para la comprobación de los contenidos de los archivos.",
        "Se ha reconocido el papel del servidor en los procesos previos a la suma de verificación.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado herramientas de monitorización eficiente de los recursos.",
        "Se han recogido métricas, procesamiento y visualización de los datos.",
        "Se han generado alertas para detectar un riesgo o mal funcionamiento.",
        "Se ha comprobado que las herramientas usadas ofrecen un rendimiento elevado con rapidez.",
        "Se ha comprobado la fiabilidad de los datos según respuestas.",
        "Se ha analizado la estabilidad de servicios.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado gran cantidad de datos estructurados y no estructurados para reforzar la función de BI.",
        "Se ha realizado la limpieza y transformación de datos en base a los objetivos predeterminados.",
        "Se ha comprobado que el Big Data multiplica la relevancia y la utilidad del BI para el negocio.",
        "Se han conjugado dentro de un modelo de empresa datos de clientes, financieros de ventas, de productos, de marketing, de redes sociales, de la competencia, entre otros, para extraer un análisis valioso y efectivo para el negocio.",
        "Se ha evaluado e interpretado la información extraída de los datos y su influencia en el triunfo de diferentes negocios.",
        "Se ha simulado la implantación de un modelo de Inteligencia de negocios BI.",
    ], start=1)],
}

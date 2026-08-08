"""EvalFP — Análisis de datos con Python · 5101 · CE Desarrollo de aplicaciones en lenguaje Python
Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio
RA y CE literales del Anexo II del Decreto 79/2025 de Castilla-La Mancha (DOCM).
Duración: 150 h · 5 h/semana (tres trimestres) · equivalencia 9 créditos ECTS.
Las unidades de trabajo, las ponderaciones y el reparto por evaluación son
propuesta didáctica, no vienen del decreto: se ajustan en Programación.
"""
MODULO = {
    "nombre":"Análisis de datos con Python","codigo":"5101","abrev":"ADP",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":5,"total_horas":150,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio",
}
UTS = [
    {"id":"UT1","nombre":"Manejo, limpieza y normalización de distintos tipos de datos…","horas":45,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Limpia y estandariza lotes de datos de forma lógica y…","horas":45,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Realiza análisis exploratorios en datos teniendo en función…","horas":30,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Desarrolla modelos en lenguaje Python dando solución al…","horas":30,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Manejo, limpieza y normalización de distintos tipos de datos en función del problema a resolver."},
    {"id":"RA2","pond":30,"nombre":"Limpia y estandariza lotes de datos de forma lógica y eficiente para su tratamiento posterior de acuerdo al problema a resolver."},
    {"id":"RA3","pond":20,"nombre":"Realiza análisis exploratorios en datos teniendo en función del alcance del problema a resolver."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla modelos en lenguaje Python dando solución al problema planteado."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
]
EVAL_RAS = {1:["RA1", "RA2"], 2:["RA3", "RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se conocen y se importan las librerías usadas en ciencia de datos.",
        "Se ha escrito código que permite leer datos de distintos orígenes (csv, xlsx, entre otros).",
        "Se ha escrito código que permite exportar datos previamente leídos en ficheros de distinto formato (csv, xlsx, entre otros).",
        "Se ha escrito código que permite acceder a bases de datos usando librerías de ciencia de datos.",
        "Se manejan selecciones, actualizaciones, adiciones y eliminaciones de datos de una base de datos usando las librerías de Python aplicadas en ciencia de datos.",
        "Se han realizado pruebas intermedias de verificación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los datos leídos.",
        "Se han deducido las operaciones para normalizar y estandarizar datos en Python.",
        "Se ha escrito código que permite limpiar y estandarizar datos basándose en el problema que hay que resolver.",
        "Se han aplicado intervalos en series de datos para realizar agrupaciones de forma coherente.",
        "Se han identificado los datos a convertir de categóricos a numéricos.",
        "Se ha escrito código que modifica variables categóricas en variables cuantitativas en Python.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha resumido grandes cantidades de datos para toma decisiones.",
        "Se ha sido capaz de responder preguntas relevantes relativos a los datos.",
        "Se han reconocido patrones en los datos.",
        "Se ha escrito código en Python que permita conocer la correlación entre variables.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado la relación entre una variable continua y una o más variables independientes mediante el ajuste de una ecuación lineal.",
        "Se ha modelado una relación no lineal entre variables independientes y dependientes.",
        "Se ha determinado correctamente la muestra en la que se ensayará el procedimiento a evaluar.",
        "Se ha realizado una predicción y se ha comprobado su precisión y validez usando una muestra de datos válida.",
    ], start=1)],
}

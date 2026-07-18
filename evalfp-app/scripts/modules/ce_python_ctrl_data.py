"""EvalFP — Estructuras de Control en Python · CE Desarrollo de Aplicaciones en Python"""
MODULO = {
    "nombre":"Estructuras de Control en Python","codigo":"PYCTRL","abrev":"PYCTRL",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"CE Desarrollo de Aplicaciones en Python (Decreto CLM — Turno Diurno)",
}
UTS = [
    {"id":"UT1","nombre":"Estructuras de selección y bucles","horas":20,"eval":1,"tags":"if · elif · else · for · while · break · continue · range · comprensiones"},
    {"id":"UT2","nombre":"Funciones y recursividad","horas":20,"eval":1,"tags":"def · return · args · kwargs · lambda · recursividad · scope · docstrings"},
    {"id":"UT3","nombre":"Ficheros, excepciones y expresiones regulares","horas":20,"eval":2,"tags":"open · with · try/except · raise · re · CSV · JSON · Logging"},
]
RAS = [
    {"id":"RA1","pond":35,"nombre":"Implementa estructuras de control de flujo en Python para la resolución de problemas algorítmicos."},
    {"id":"RA2","pond":35,"nombre":"Define y utiliza funciones en Python, aplicando buenas prácticas de programación modular."},
    {"id":"RA3","pond":30,"nombre":"Gestiona ficheros, excepciones y expresiones regulares en programas Python."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","ejercicio"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han implementado estructuras condicionales simples y anidadas con if/elif/else.",
        "Se han utilizado bucles for para iterar sobre colecciones y rangos.",
        "Se han implementado bucles while con condiciones de parada y control con break/continue.",
        "Se han aplicado comprensiones de listas y diccionarios para transformar colecciones de forma concisa.",
        "Se han resuelto problemas algorítmicos seleccionando la estructura de control más adecuada.",
        "Se ha analizado la complejidad algorítmica de los programas desarrollados.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido funciones con parámetros posicionales, con valores por defecto y con *args/**kwargs.",
        "Se han utilizado funciones lambda para definir funciones anónimas de una expresión.",
        "Se han implementado funciones recursivas para la resolución de problemas.",
        "Se ha descrito el scope de las variables en Python (local, global, enclosing).",
        "Se han documentado las funciones con docstrings siguiendo las convenciones PEP 257.",
        "Se han aplicado el principio DRY (Don't Repeat Yourself) mediante la modularización con funciones.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han leído y escrito ficheros de texto utilizando open() y el gestor de contexto with.",
        "Se han procesado ficheros CSV y JSON con los módulos csv y json de la biblioteca estándar.",
        "Se han gestionado excepciones con try/except/else/finally para el control de errores.",
        "Se han creado excepciones personalizadas mediante la herencia de la clase Exception.",
        "Se han aplicado expresiones regulares con el módulo re para la búsqueda y validación de patrones.",
        "Se ha implementado un sistema de logging para el registro de eventos en aplicaciones Python.",
    ], start=1)],
}

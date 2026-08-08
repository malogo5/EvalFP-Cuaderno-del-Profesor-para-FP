"""EvalFP — Entornos y sintaxis en Python · 5098 · CE Desarrollo de aplicaciones en lenguaje Python
Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio
RA y CE literales del Anexo II del Decreto 79/2025 de Castilla-La Mancha (DOCM).
Duración: 50 h · 2 h/semana (tres trimestres) · equivalencia 3 créditos ECTS.
Las unidades de trabajo, las ponderaciones y el reparto por evaluación son
propuesta didáctica, no vienen del decreto: se ajustan en Programación.
"""
MODULO = {
    "nombre":"Entornos y sintaxis en Python","codigo":"5098","abrev":"ENSP",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":2,"total_horas":50,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio",
}
UTS = [
    {"id":"UT1","nombre":"Analiza los problemas planteados, identificando los entornos…","horas":9,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Caracteriza elementos de la programación en Python,…","horas":11,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Evalúa entornos de trabajo para el desarrollo de…","horas":8,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Utiliza el IDLE básico de Python y la ventana Shell,…","horas":13,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica la sintaxis y operadores y tipos simples y complejos…","horas":9,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":19,"nombre":"Analiza los problemas planteados, identificando los entornos de aplicación y proponiendo estrategias para su resolución."},
    {"id":"RA2","pond":22,"nombre":"Caracteriza elementos de la programación en Python, identificando los bloques fundamentales de construcción de un programa."},
    {"id":"RA3","pond":15,"nombre":"Evalúa entornos de trabajo para el desarrollo de aplicaciones en Python, indicando sus diferencias y áreas específicas de trabajo."},
    {"id":"RA4","pond":25,"nombre":"Utiliza el IDLE básico de Python y la ventana Shell, introduciendo los principios de la escritura de software en Python."},
    {"id":"RA5","pond":19,"nombre":"Aplica la sintaxis y operadores y tipos simples y complejos en Python, escribiendo instrucciones básicas y verificando sus resultados."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1", "RA2", "RA3"], 2:["RA4", "RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características principales de los entornos de aplicación.",
        "Se han definido estrategias conducentes a la resolución del problema.",
        "Se han analizado las dificultades que puedan presentarse.",
        "Se han realizado diagramas de flujo de las soluciones propuestas.",
        "Se ha seleccionado el diagrama de flujo considerado óptimo.",
        "Se ha verificado que la solución propuesta es susceptible de ser implementada en Python.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los aspectos fundamentales de la programación de alto nivel.",
        "Se han establecido las diferencias entre lenguajes compilados e interpretados.",
        "Se han analizado los bloques principales en la construcción de un programa en Python.",
        "Se han establecido las diferencias entre diferentes versiones de Python.",
        "Se han identificado los errores más frecuentes en la programación en Python.",
        "Se ha valorado la importancia de la depuración de código.",
        "Se han analizado segmentos de código, antes y después de la depuración.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los IDE´s (Integrated Development Environment) (entornos de desarrollo integrado) más habituales usados en la programación en Python.",
        "Se han seleccionado IDE´s, en función del desarrollo a realizar.",
        "Se han analizado las ventajas del uso de frameworks (marcos, esquemas) en el desarrollo de software con Python.",
        "Se han comparado diversos editores de código en Python relacionándolos con desarrollos de aplicaciones concretas.",
        "Se ha puesto de manifiesto la utilidad del uso de IDLE´s (Integrated Development and Learning Environment) y frameworks mediante el análisis de software real.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han escrito instrucciones elementales para visualizar el funcionamiento básico del lenguaje.",
        "Se ha escrito una instrucción en una sola línea.",
        "Se ha razonado la mala praxis de escribir varías instrucciones en una línea.",
        "Se ha escrito una instrucción en varias líneas.",
        "Se han escrito en consola las instrucciones.",
        "Se han utilizado sangrados explicando su utilidad.",
        "Se han escrito comentarios en Python.",
        "Se han instalado y probado editores de texto no integrados en el entorno.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha escrito código con sintaxis básica.",
        "Se conocen y distinguen los distintos tipos de operadores.",
        "Se han escrito instrucciones básicas con cada tipo de operador.",
        "Se distinguen y utilizan los distintos tipos de datos.",
        "Se han utilizado los distintos tipos de operadores en un código básico.",
        "Se han hecho operaciones entre iguales y distintos tipos de datos.",
    ], start=1)],
}

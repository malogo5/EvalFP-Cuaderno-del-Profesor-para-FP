"""EvalFP — Estructuras de control en Python · 5099 · CE Desarrollo de aplicaciones en lenguaje Python
Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio
RA y CE literales del Anexo II del Decreto 79/2025 de Castilla-La Mancha (DOCM).
Duración: 80 h · 2 h/semana (tres trimestres) · equivalencia 5 créditos ECTS.
Las unidades de trabajo, las ponderaciones y el reparto por evaluación son
propuesta didáctica, no vienen del decreto: se ajustan en Programación.
"""
MODULO = {
    "nombre":"Estructuras de control en Python","codigo":"5099","abrev":"ECP",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":2,"total_horas":80,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio",
}
UTS = [
    {"id":"UT1","nombre":"Identifica las estructuras de control en Python…","horas":16,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Reconoce las sentencias condicionales en Python aplicándolas…","horas":24,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Utiliza sentencias iterativas analizando las necesidades del…","horas":14,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Aplica funciones de Python de distintos tipos mejorando la…","horas":12,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Crea arquitectura de código de forma eficiente y escribe…","horas":14,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Identifica las estructuras de control en Python relacionándolas con aplicaciones reales."},
    {"id":"RA2","pond":29,"nombre":"Reconoce las sentencias condicionales en Python aplicándolas a la resolución de problemas que impliquen toma de decisiones."},
    {"id":"RA3","pond":18,"nombre":"Utiliza sentencias iterativas analizando las necesidades del código para resolver un problema."},
    {"id":"RA4","pond":15,"nombre":"Aplica funciones de Python de distintos tipos mejorando la eficiencia del programa."},
    {"id":"RA5","pond":18,"nombre":"Crea arquitectura de código de forma eficiente y escribe código robusto."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
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
        "Se han identificado las estructuras de control que permiten modificar el flujo de las instrucciones.",
        "Se han representado en un diagrama de flujo gráfico las estructuras de control.",
        "Se han analizado la importancia de las condiciones en cada estructura de control.",
        "Se han tenido en cuenta la importancia de los sangrados en las estructuras de control.",
        "Se han escrito bloques de control secuencial.",
        "Se han escrito bloques de control de selección.",
        "Se han escrito bloques de control de repetición.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado el concepto de sentencia condicional.",
        "Se han identificado las partes de las que consta una sentencia condicional.",
        "Se ha aplicado correctamente el sangrado.",
        "Se ha aplicado la ejecución condicional y control de variables.",
        "Se han interpretado el funcionamiento de las sentencias condicionales.",
        "Se han aplicado correctamente las sentencias condicionales.",
        "Se han interpretado y aplicado correctamente las anidaciones.",
        "Se aplica correctamente la sintaxis a aplicar en estructuras compactas.",
        "Se han escrito bloques de programas utilizando sentencias condicionales.",
        "Se han escrito bloques de programas utilizando sentencias condicionales anidadas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado el concepto de sentencia iterativa.",
        "Se ha diferenciado entre estructuras condicionales e iterativas.",
        "Se ha verificado el funcionamiento de las sentencias iterativas.",
        "Se han aplicado las sentencias iterativas de acuerdo a las necesidades.",
        "Se han escrito bloques de programas utilizando los bucles «for» y «while».",
        "Se han interpretado y aplicado los anidamientos de estructuras.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se comprende la necesidad de usar funciones de Python y sus ventajas.",
        "Se ha escrito código que incluya funciones Build-in de Python.",
        "Se ha escrito un programa con funciones definidas por la propia persona usuaria.",
        "Se aplican correctamente las funciones lambda en un programa de Python.",
        "Se han creado funciones recursivas partiendo de funciones definidas anteriormente por la persona usuaria.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha diferenciado entre el concepto de excepción y los errores de sintaxis.",
        "Se ha escrito instrucciones de captura de excepciones.",
        "Se han capturado y tratado excepciones.",
        "Se han tratado excepciones.",
        "Se han realizado depuraciones de excepciones correctamente.",
        "Se han escrito bloques de código robusto utilizando las sentencias adecuadas.",
    ], start=1)],
}

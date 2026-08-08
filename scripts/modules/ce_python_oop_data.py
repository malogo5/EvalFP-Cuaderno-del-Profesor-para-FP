"""EvalFP — Programación orientada a objetos · 5100 · CE Desarrollo de aplicaciones en lenguaje Python
Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio
RA y CE literales del Anexo II del Decreto 79/2025 de Castilla-La Mancha (DOCM).
Duración: 150 h · 5 h/semana (tres trimestres) · equivalencia 9 créditos ECTS.
Las unidades de trabajo, las ponderaciones y el reparto por evaluación son
propuesta didáctica, no vienen del decreto: se ajustan en Programación.
"""
MODULO = {
    "nombre":"Programación orientada a objetos","codigo":"5100","abrev":"POO",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":5,"total_horas":150,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 79/2025, de 14/10/2025 (DOCM núm. 205, de 23/10/2025, pág. 33217, NID 2025/7868) · Horas: Anexo I · RA y CE literales del Anexo II · Complementa el Real Decreto 566/2024, de 18 de junio",
}
UTS = [
    {"id":"UT1","nombre":"Caracteriza la programación orientada a objetos…","horas":29,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Aplica la programación orientada a objetos para generar…","horas":29,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Gestiona y maneja la creación de ficheros usando código Python","horas":19,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Conecta y gestiona bases de datos partiendo de entradas de…","horas":33,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Escribe programas en Python dando respuesta a problemas…","horas":40,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Caracteriza la programación orientada a objetos organizándolos y relacionándolos con el código para manejarlos."},
    {"id":"RA2","pond":19,"nombre":"Aplica la programación orientada a objetos para generar código eficiente y correctamente estructurado."},
    {"id":"RA3","pond":12,"nombre":"Gestiona y maneja la creación de ficheros usando código Python."},
    {"id":"RA4","pond":22,"nombre":"Conecta y gestiona bases de datos partiendo de entradas de datos desde aplicaciones Web."},
    {"id":"RA5","pond":27,"nombre":"Escribe programas en Python dando respuesta a problemas reales en diferentes campos de aplicación y teniendo en cuenta el contexto de uso."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
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
        "Se ha definido el concepto de objeto.",
        "Se ha definido la forma de agrupar datos (atributos).",
        "Se ha descrito las operaciones a ejecutar sobre los datos (métodos).",
        "Se han descrito las clases y las instancias de los objetos.",
        "Se ha caracterizado el concepto de constructor.",
        "Se ha caracterizado el concepto de destructor.",
        "Se ha definido el concepto de ortogonalidad de los métodos.",
        "Se ha caracterizado los tipos de métodos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha escrito una clase que se pueda reutilizar con herencias.",
        "Se ha escrito una clase nueva en base de una clase ya creada.",
        "Se ha escrito un programa usando objetos y atributos.",
        "Se han escrito instrucciones self en métodos.",
        "Se ha escrito un programa usando las propiedades de polimorfismo y encapsulación.",
        "Se han escrito programas que incluyan constructores.",
        "Se han escrito programas que incluyan destructores.",
        "Se han escrito módulos y paquetes y se han usado en un programa de forma correcta.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han escrito líneas de código que permiten la apertura de ficheros.",
        "Se han utilizado distintos métodos del objeto File.",
        "Se conocen propiedades del objeto File y se han usado correctamente en el código.",
        "Se ha escrito código para tratar ficheros JSON.",
        "Se ha escrito código permite cambiar objetos a cadenas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha conectado con éxito una base de datos usando código Python.",
        "Se ha creado una nueva base de datos usando código Python.",
        "Se han realizado consultas contra la base de datos conectada.",
        "Se han incluido nuevos registros en la base de datos.",
        "Se han eliminado registros en bloque de la base de datos.",
        "Se ha creado un interfaz web usando Python.",
        "Se ha conectado la base de datos a una web y se permite escribir nuevos registros usando entrada de texto desde la web.",
        "Se conocen los requisitos de seguridad web en Python.",
        "Se han verificado los requisitos de seguridad mínimos establecidos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado el problema a resolver documentándolo de forma rigurosa.",
        "Se han indicado posibles soluciones al problema.",
        "Se ha seleccionado la solución considerada más adecuada de acuerdo al contexto y al posible costo de la implementación.",
        "Se ha escrito la solución en Python, documentándola debidamente.",
        "Se ha utilizado el depurador.",
        "Se han diseñado pruebas para cada una de las partes del programa.",
        "Se han ejecutado las pruebas y documentado los resultados.",
        "Se ha verificado que los resultados son los esperados.",
        "Se han realizado cambios en caso de ser necesarios, documentándolos.",
        "Se ha probado el programa en su conjunto.",
        "Se han documentado cambios en caso de producirse.",
    ], start=1)],
}

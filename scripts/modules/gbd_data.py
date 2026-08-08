"""EvalFP — Gestión de Bases de Datos · 0372 · Administración de Sistemas Informáticos en Red (ASIR)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 134 h · 4 h/semana · 1º ASIR.
"""
MODULO = {
    "nombre":"Gestión de Bases de Datos","codigo":"0372","abrev":"GBD",
    "ciclo":"Administración de Sistemas Informáticos en Red (ASIR)","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":4,"total_horas":134,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Sistemas de almacenamiento y gestores de bases de datos","horas":18,"eval":1,"tags":"SGBD · MySQL · PostgreSQL · Oracle"},
    {"id":"UT2","nombre":"Diseña modelos lógicos normalizados","horas":28,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Realiza el diseño físico de bases de datos","horas":26,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Consulta la información almacenada manejando asistentes","horas":18,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Modifica la información almacenada","horas":23,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Ejecuta tareas de aseguramiento de la información","horas":21,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de sistemas gestores."},
    {"id":"RA2","pond":21,"nombre":"Diseña modelos lógicos normalizados interpretando diagramas entidad/relación."},
    {"id":"RA3","pond":19,"nombre":"Realiza el diseño físico de bases de datos utilizando asistentes, herramientas gráficas y el lenguaje de definición de datos."},
    {"id":"RA4","pond":14,"nombre":"Consulta la información almacenada manejando asistentes, herramientas gráficas y el lenguaje de manipulación de datos."},
    {"id":"RA5","pond":17,"nombre":"Modifica la información almacenada utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos."},
    {"id":"RA6","pond":15,"nombre":"Ejecuta tareas de aseguramiento de la información, analizándolas y aplicando mecanismos de salvaguarda y transferencia."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica"],
    "RA3":["examen","practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los distintos sistemas lógicos de almacenamiento y sus funciones.",
        "Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado.",
        "Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información.",
        "Se ha reconocido la utilidad de un sistema gestor de bases de datos.",
        "Se ha descrito la función de cada uno de los elementos de un sistema gestor de bases de datos.",
        "Se han clasificado los sistemas gestores de bases de datos.",
        "Se han identificado los nuevos sistemas de almacenamiento de información.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado el significado de la simbología propia de los diagramas entidad/relación.",
        "Se han utilizado herramientas gráficas para representar el diseño lógico.",
        "Se han identificado las tablas del diseño lógico.",
        "Se han identificado los campos que forman parte de las tablas del diseño lógico.",
        "Se han identificado las relaciones entre las tablas del diseño lógico.",
        "Se han definido los campos clave.",
        "Se han aplicado las reglas de integridad.",
        "Se han aplicado las reglas de normalización hasta un nivel adecuado.",
        "Se han identificado y documentado las restricciones que no pueden plasmarse en el diseño lógico.",
        "Se han identificado otros modelos de datos para el diseño lógico de bases de datos.",
        "Se han convertido diagramas Entidad Relación al modelo conceptual Lenguaje Unificado de modelado (UML).",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido las estructuras físicas de almacenamiento.",
        "Se han creado tablas.",
        "Se han seleccionado los tipos de datos adecuados.",
        "Se han definido los campos clave en las tablas.",
        "Se han implantado todas las restricciones reflejadas en el diseño lógico.",
        "Se ha verificado mediante un conjunto de datos de prueba que la implementación se ajusta al modelo.",
        "Se han utilizado asistentes y herramientas gráficas.",
        "Se ha utilizado el lenguaje de definición de datos.",
        "Se ha definido y documentado el diccionario de datos.",
        "Se han creado los dominios de atributos adecuados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas y sentencias para realizar consultas.",
        "Se han realizado consultas simples sobre una tabla.",
        "Se han realizado consultas que generan valores de resumen.",
        "Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas.",
        "Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas.",
        "Se han realizado consultas con subconsultas.",
        "Se han valorado las ventajas e inconvenientes de las distintas opciones válidas para llevar a cabo una consulta determinada.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos.",
        "Se han insertado, borrado y actualizado datos en las tablas.",
        "Se ha incluido en una tabla la información resultante de la ejecución de una consulta.",
        "Se han adoptado medidas para mantener la integridad y consistencia de la información.",
        "Se han diseñado guiones de sentencias para llevar a cabo tareas complejas.",
        "Se ha reconocido el funcionamiento de las transacciones.",
        "Se han anulado parcial o totalmente los cambios producidos por una transacción.",
        "Se han identificado los efectos de las distintas políticas de bloqueo de registros.",
        "Se han realizado agrupación de sentencias utilizando procedimientos, funciones y cursores para llevar a cabo tareas complejas.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado herramientas gráficas y en línea de comandos para la administración de copias de seguridad.",
        "Se han realizado copias de seguridad.",
        "Se han restaurado copias de seguridad.",
        "Se han identificado las herramientas para importar y exportar datos.",
        "Se han exportado datos a diversos formatos.",
        "Se han importado datos con distintos formatos.",
        "Se ha interpretado correctamente la información suministrada por los mensajes de error y los ficheros de registro.",
        "Se ha transferido información entre sistemas gestores.",
    ], start=1)],
}

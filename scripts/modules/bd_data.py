"""EvalFP — Bases de Datos · 0484 · DAM
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 163 h · 5 h/semana · 1º DAM.
"""
MODULO = {
    "nombre":"Bases de Datos","codigo":"0484","abrev":"BD",
    "ciclo":"DAM","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":5,"total_horas":163,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de elementos de bases de datos relacionales","horas":23,"eval":1,"tags":"Modelo relacional · Entidad/Relación · Normalización"},
    {"id":"UT2","nombre":"Gestión de la información almacenada (DDL/DCL)","horas":23,"eval":1,"tags":"CREATE · ALTER · DROP · GRANT · REVOKE · Transacciones"},
    {"id":"UT3","nombre":"Consulta la información almacenada en una base de datos empleando…","horas":18,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Modifica la información almacenada en la base de datos","horas":23,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Programación de bases de datos","horas":26,"eval":2,"tags":"Procedimientos · Funciones · Triggers · Cursores · PL/SQL"},
    {"id":"UT6","nombre":"Diseña modelos relacionales normalizados","horas":32,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Gestiona la información almacenada en bases de datos objeto-relacionales","horas":18,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores."},
    {"id":"RA2","pond":14,"nombre":"Crea bases de datos definiendo su estructura y las características de sus elementos según el modelo relacional."},
    {"id":"RA3","pond":11,"nombre":"Consulta la información almacenada en una base de datos empleando asistentes, herramientas gráficas y el lenguaje de manipulación de datos."},
    {"id":"RA4","pond":14,"nombre":"Modifica la información almacenada en la base de datos utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos."},
    {"id":"RA5","pond":16,"nombre":"Desarrolla procedimientos almacenados evaluando y utilizando las sentencias del lenguaje incorporado en el sistema gestor de bases de datos."},
    {"id":"RA6","pond":20,"nombre":"Diseña modelos relacionales normalizados interpretando diagramas entidad/relación."},
    {"id":"RA7","pond":11,"nombre":"Gestiona la información almacenada en bases de datos objeto-relacionales, evaluando y utilizando las posibilidades que proporciona el sistema gestor."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los sistemas lógicos de almacenamiento y sus características.",
        "Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado.",
        "Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información.",
        "Se ha evaluado la utilidad de un sistema gestor de bases de datos.",
        "Se ha reconocido la función de cada uno de los elementos de un sistema gestor de bases de datos.",
        "Se han clasificado los sistemas gestores de bases de datos.",
        "Se ha reconocido la utilidad de las bases de datos distribuidas.",
        "Se han analizado las políticas de fragmentación de la información.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado el formato de almacenamiento de la información.",
        "Se han creado las tablas y las relaciones entre ellas.",
        "Se han seleccionado los tipos de datos adecuados.",
        "Se han definido los campos clave en las tablas.",
        "Se han implantado las restricciones reflejadas en el diseño lógico.",
        "Se han creado vistas.",
        "Se han creado los usuarios y se les han asignado privilegios.",
        "Se han utilizando asistentes, herramientas gráficas y los lenguajes de definición y control de datos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas y sentencias para realizar consultas.",
        "Se han realizado consultas simples sobre una tabla.",
        "Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas.",
        "Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas.",
        "Se han realizado consultas resumen.",
        "Se han realizado consultas con subconsultas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos.",
        "Se han insertado, borrado y actualizado datos en las tablas.",
        "Se ha incluido en una tabla la información resultante de la ejecución de una consulta.",
        "Se han diseñado guiones de sentencias para llevar a cabo tareas complejas.",
        "Se ha reconocido el funcionamiento de las transacciones.",
        "Se han anulado parcial o totalmente los cambios producidos por una transacción.",
        "Se han identificado los efectos de las distintas políticas de bloqueo de registros.",
        "Se han adoptado medidas para mantener la integridad y consistencia de la información.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las diversas formas de automatizar tareas.",
        "Se han reconocido los métodos de ejecución de guiones.",
        "Se han identificado las herramientas disponibles para editar guiones.",
        "Se han definido y utilizado guiones para automatizar tareas.",
        "Se ha hecho uso de las funciones proporcionadas por el sistema gestor.",
        "Se han definido funciones de usuario.",
        "Se han utilizado estructuras de control de flujo.",
        "Se han definido disparadores.",
        "Se han utilizado cursores.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado herramientas gráficas para representar el diseño lógico.",
        "Se han identificado las tablas del diseño lógico.",
        "Se han identificado las entidades e interrelaciones en un universo del discurso.",
        "Se han identificado los atributos que forman parte del esquema.",
        "Se han identificado los distintos tipos de atributos.",
        "Se han identificado los campos que forman parte de las tablas del diseño lógico.",
        "Se han analizado las relaciones entre las tablas del diseño lógico.",
        "Se han identificado los campos clave.",
        "Se han aplicado reglas de integridad.",
        "Se han aplicado reglas de normalización.",
        "Se han analizado y documentado las restricciones que no pueden plasmarse en el diseño lógico.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características de las bases de datos objeto- relacionales.",
        "Se han creado tipos de datos objeto, sus atributos y métodos.",
        "Se han creado tablas de objetos y tablas de columnas tipo objeto.",
        "Se han creado tipos de datos colección.",
        "Se han realizado consultas.",
        "Se ha modificado la información almacenada manteniendo la integridad y consistencia de los datos.",
    ], start=1)],
}

"""EvalFP — Bases de Datos (BD) · 0484 · 1º DAM/DAW · RD 450/2010 / RD 686/2010"""
MODULO = {
    "nombre":"Bases de Datos","codigo":"0485","abrev":"BD",
    "ciclo":"DAM","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de elementos de bases de datos relacionales","horas":20,"eval":1,"tags":"Modelo relacional · Entidad/Relación · Normalización"},
    {"id":"UT2","nombre":"Realización de consultas (SQL DML)","horas":40,"eval":1,"tags":"SELECT · JOIN · GROUP BY · Subconsultas · Funciones agregadas"},
    {"id":"UT3","nombre":"Gestión de la información almacenada (DDL/DCL)","horas":30,"eval":2,"tags":"CREATE · ALTER · DROP · GRANT · REVOKE · Transacciones"},
    {"id":"UT4","nombre":"Programación de bases de datos","horas":30,"eval":2,"tags":"Procedimientos · Funciones · Triggers · Cursores · PL/SQL"},
    {"id":"UT5","nombre":"Uso de bases de datos objeto-relacionales","horas":20,"eval":3,"tags":"Tipos objeto · Colecciones · Métodos · MongoDB · NoSQL"},
    {"id":"UT6","nombre":"Administración de gestores de bases de datos","horas":20,"eval":3,"tags":"Usuarios · Roles · Backup · Restore · Tuning · Importación"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores."},
    {"id":"RA2","pond":25,"nombre":"Crea bases de datos definiendo su estructura y las características de sus elementos según el modelo relacional."},
    {"id":"RA3","pond":20,"nombre":"Realiza consultas sobre una o varias tablas procesando la información almacenada según las necesidades del usuario."},
    {"id":"RA4","pond":20,"nombre":"Modifica la información almacenada en la base de datos utilizando las herramientas proporcionadas por el gestor."},
    {"id":"RA5","pond":10,"nombre":"Desarrolla procedimientos almacenados evaluando y utilizando las sentencias del lenguaje incorporado en el gestor de bases de datos."},
    {"id":"RA6","pond":10,"nombre":"Gestiona la información almacenada en bases de datos objeto-relacionales, evaluando y utilizando las posibilidades que proporciona el gestor."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT6","RA2",["CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han analizado los sistemas lógicos de almacenamiento y sus funciones."},
        {"id":"CR2","texto":"Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado."},
        {"id":"CR3","texto":"Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información."},
        {"id":"CR4","texto":"Se ha evaluado la utilidad de un sistema gestor de bases de datos."},
        {"id":"CR5","texto":"Se ha descrito la función de cada uno de los elementos de un sistema gestor de bases de datos."},
        {"id":"CR6","texto":"Se han clasificado los sistemas gestores de bases de datos."},
        {"id":"CR7","texto":"Se ha reconocido la utilidad de las bases de datos distribuidas."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se ha analizado el formato de almacenamiento de la información."},
        {"id":"CR2","texto":"Se han creado las tablas y las relaciones entre ellas."},
        {"id":"CR3","texto":"Se han seleccionado los tipos de datos adecuados."},
        {"id":"CR4","texto":"Se han definido los campos clave en las tablas."},
        {"id":"CR5","texto":"Se han implantado todas las restricciones reflejadas en el diseño lógico."},
        {"id":"CR6","texto":"Se ha verificado mediante datos de prueba que la implementación se ajusta al modelo."},
        {"id":"CR7","texto":"Se ha definido y documentado el diccionario de datos."},
        {"id":"CR8","texto":"Se han creado y gestionado usuarios y roles."},
        {"id":"CR9","texto":"Se han realizado copias de seguridad y restauración de la base de datos."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han identificado las herramientas y sentencias para realizar consultas."},
        {"id":"CR2","texto":"Se han realizado consultas simples sobre una tabla."},
        {"id":"CR3","texto":"Se han realizado consultas que generan valores de resumen."},
        {"id":"CR4","texto":"Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas."},
        {"id":"CR5","texto":"Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas."},
        {"id":"CR6","texto":"Se han realizado consultas con subconsultas."},
        {"id":"CR7","texto":"Se han valorado las ventajas e inconvenientes de las distintas opciones válidas para llevar a cabo una consulta determinada."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos."},
        {"id":"CR2","texto":"Se han insertado, borrado y actualizado datos en las tablas."},
        {"id":"CR3","texto":"Se han diseñado consultas de acción."},
        {"id":"CR4","texto":"Se han diseñado vistas."},
        {"id":"CR5","texto":"Se han gestionado transacciones (commit, rollback)."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado las ventajas de utilizar procedimientos almacenados."},
        {"id":"CR2","texto":"Se han definido procedimientos almacenados."},
        {"id":"CR3","texto":"Se ha utilizado el lenguaje incorporado en el gestor de bases de datos."},
        {"id":"CR4","texto":"Se han definido y utilizado cursores."},
        {"id":"CR5","texto":"Se han utilizado las funciones de tratamiento de errores."},
        {"id":"CR6","texto":"Se han definido disparadores (triggers)."},
        {"id":"CR7","texto":"Se han utilizado los disparadores para garantizar la integridad de la información."},
    ],
    "RA6":[
        {"id":"CR1","texto":"Se han identificado las características de las bases de datos objeto-relacionales."},
        {"id":"CR2","texto":"Se han creado tipos de datos objeto, tablas de objetos y tablas con columnas de tipos objeto."},
        {"id":"CR3","texto":"Se han creado tipos de datos colección."},
        {"id":"CR4","texto":"Se han realizado consultas sobre tablas con columnas de tipos objeto."},
        {"id":"CR5","texto":"Se han evaluado características de bases de datos NoSQL."},
    ],
}

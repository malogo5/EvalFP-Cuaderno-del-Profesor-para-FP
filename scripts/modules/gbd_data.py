"""
EvalFP — Gestión de Bases de Datos (GBD)
Módulo: 0372 · 1º ASIR · Ciclo: ASIR
Decreto: RD 1629/2009 + Orden CLM DOCM
"""

MODULO = {
    "nombre":      "Gestión de Bases de Datos",
    "codigo":      "0372",
    "abrev":       "GBD",
    "ciclo":       "Administración de Sistemas Informáticos en Red (ASIR)",
    "curso":       "1º ASIR",
    "horas_sem":   5,
    "total_horas": 155,
    "anno":        "2026-2027",
    "eval_count":  3,
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Sistemas de almacenamiento y gestores de bases de datos","horas":15,"eval":1,"tags":"SGBD · MySQL · PostgreSQL · Oracle"},
    {"id":"UT2","nombre":"Modelo relacional y diseño de bases de datos","horas":25,"eval":1,"tags":"ER · Normalización · 1FN · 2FN · 3FN"},
    {"id":"UT3","nombre":"Creación y manipulación de bases de datos (DDL/DML)","horas":30,"eval":1,"tags":"CREATE · INSERT · UPDATE · DELETE"},
    {"id":"UT4","nombre":"Consultas SQL avanzadas","horas":30,"eval":2,"tags":"JOIN · Subconsultas · GROUP BY · Funciones"},
    {"id":"UT5","nombre":"Programación en bases de datos","horas":30,"eval":2,"tags":"Procedimientos · Funciones · Cursores · Triggers"},
    {"id":"UT6","nombre":"Bases de datos objeto-relacionales y NoSQL","horas":25,"eval":3,"tags":"Tipos objeto · MongoDB · JSON · XML"},
]

RAS = [
    {"id":"RA1","pond":10,"nombre":"Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores."},
    {"id":"RA2","pond":20,"nombre":"Crea bases de datos definiendo su estructura y las características de sus elementos según el modelo relacional."},
    {"id":"RA3","pond":25,"nombre":"Realiza consultas sobre una o varias tablas procesando la información almacenada según las necesidades del usuario."},
    {"id":"RA4","pond":15,"nombre":"Modifica la información almacenada en la base de datos utilizando las herramientas proporcionadas por el gestor."},
    {"id":"RA5","pond":20,"nombre":"Desarrolla procedimientos almacenados evaluando y utilizando las sentencias del lenguaje incorporado en el gestor de bases de datos."},
    {"id":"RA6","pond":10,"nombre":"Diseña modelos relacionales normalizados interpretando diagramas entidad/relación."},
    {"id":"RA7","pond": 0,"nombre":"Gestiona la información almacenada en bases de datos objeto-relacionales, evaluando y utilizando las posibilidades que proporciona el gestor."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA7",["CR1","CR2","CR3","CR4","CR5"]),
]

EVAL_RAS = {
    1: ["RA1","RA2","RA6"],
    2: ["RA3","RA4","RA5"],
    3: ["RA7"],
}

DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica"],
    "RA3":["examen","practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["examen"],
    "RA7":["practica"],
}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se han analizado los sistemas lógicos de almacenamiento y sus funciones."},
        {"id":"CR2","texto":"Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado."},
        {"id":"CR3","texto":"Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información."},
        {"id":"CR4","texto":"Se ha evaluado la utilidad de un sistema gestor de bases de datos."},
        {"id":"CR5","texto":"Se ha descrito la función de cada uno de los elementos de un sistema gestor de bases de datos."},
        {"id":"CR6","texto":"Se han clasificado los sistemas gestores de bases de datos."},
        {"id":"CR7","texto":"Se ha reconocido la utilidad de las bases de datos distribuidas."},
        {"id":"CR8","texto":"Se han analizado las políticas de fragmentación de la información."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se ha analizado el formato de almacenamiento de la información."},
        {"id":"CR2","texto":"Se han creado las tablas y las relaciones entre ellas."},
        {"id":"CR3","texto":"Se han seleccionado los tipos de datos adecuados."},
        {"id":"CR4","texto":"Se han definido los campos clave en las tablas."},
        {"id":"CR5","texto":"Se han implantado todas las restricciones reflejadas en el diseño lógico."},
        {"id":"CR6","texto":"Se ha verificado mediante un conjunto de datos de prueba que la implementación se ajusta al modelo."},
        {"id":"CR7","texto":"Se ha definido y documentado el diccionario de datos."},
        {"id":"CR8","texto":"Se ha utilizado el asistente de importación/exportación de datos."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se han identificado las herramientas y sentencias para realizar consultas."},
        {"id":"CR2","texto":"Se han realizado consultas simples sobre una tabla."},
        {"id":"CR3","texto":"Se han realizado consultas que generan valores de resumen."},
        {"id":"CR4","texto":"Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas."},
        {"id":"CR5","texto":"Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas."},
        {"id":"CR6","texto":"Se han realizado consultas con subconsultas."},
        {"id":"CR7","texto":"Se han valorado las ventajas e inconvenientes de las distintas opciones válidas para llevar a cabo una consulta determinada."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos."},
        {"id":"CR2","texto":"Se han insertado, borrado y actualizado datos en las tablas."},
        {"id":"CR3","texto":"Se ha incluido en una consulta información procedente de distintas tablas mediante subconsultas."},
        {"id":"CR4","texto":"Se han diseñado consultas de acción."},
        {"id":"CR5","texto":"Se han diseñado vistas."},
        {"id":"CR6","texto":"Se han analizado las ventajas e inconvenientes de la utilización de vistas."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se han identificado las ventajas de utilizar procedimientos almacenados."},
        {"id":"CR2","texto":"Se han utilizado las sentencias para definir procedimientos almacenados."},
        {"id":"CR3","texto":"Se ha utilizado el lenguaje incorporado en el gestor de bases de datos."},
        {"id":"CR4","texto":"Se han definido y utilizado cursores."},
        {"id":"CR5","texto":"Se han utilizado las funciones de tratamiento de errores."},
        {"id":"CR6","texto":"Se han definido disparadores (triggers)."},
        {"id":"CR7","texto":"Se han utilizado los disparadores para garantizar la integridad de la información."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han utilizado herramientas gráficas para representar el diseño de la base de datos."},
        {"id":"CR2","texto":"Se han identificado las tablas del modelo relacional."},
        {"id":"CR3","texto":"Se han identificado los campos que son clave primaria o ajena."},
        {"id":"CR4","texto":"Se han aplicado las reglas de transformación de las relaciones."},
        {"id":"CR5","texto":"Se han analizado las tablas obtenidas indicando las anomalías de actualización."},
        {"id":"CR6","texto":"Se han aplicado reglas de normalización."},
        {"id":"CR7","texto":"Se han analizado e interpretado diagramas entidad/relación complejos."},
        {"id":"CR8","texto":"Se han reconocido los distintos tipos de relación entre las tablas."},
    ],
    "RA7": [
        {"id":"CR1","texto":"Se han identificado las características de las bases de datos objeto-relacionales."},
        {"id":"CR2","texto":"Se han creado tipos de datos objeto, tablas de objetos y tablas con columnas de tipos objeto."},
        {"id":"CR3","texto":"Se han creado tipos de datos colección."},
        {"id":"CR4","texto":"Se han realizado consultas sobre tablas con columnas de tipos objeto."},
        {"id":"CR5","texto":"Se ha modificado la información almacenada manteniendo la integridad de la información."},
    ],
}

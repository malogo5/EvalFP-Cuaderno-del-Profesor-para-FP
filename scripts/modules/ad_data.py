"""EvalFP — Acceso a Datos · 0486 · Desarrollo de Aplicaciones Multiplataforma (DAM)
Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 233 h · 6 h/semana · 2º DAM.
"""
MODULO = {
    "nombre":"Acceso a Datos","codigo":"0486","abrev":"AD",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":6,"total_horas":233,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Desarrolla aplicaciones que gestionan información almacenada en ficheros","horas":31,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Desarrolla aplicaciones que gestionan información almacenada en…","horas":47,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Gestiona la persistencia de los datos","horas":39,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Desarrolla aplicaciones que gestionan la información almacenada en…","horas":46,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Desarrolla aplicaciones que gestionan la información almacenada en…","horas":35,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Programa componentes de acceso a datos","horas":35,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":13,"nombre":"Desarrolla aplicaciones que gestionan información almacenada en ficheros identificando el campo de aplicación de los mismos y utilizando clases específicas."},
    {"id":"RA2","pond":20,"nombre":"Desarrolla aplicaciones que gestionan información almacenada en bases de datos relacionales identificando y utilizando mecanismos de conexión."},
    {"id":"RA3","pond":17,"nombre":"Gestiona la persistencia de los datos identificando herramientas de mapeo objeto relacional (ORM) y desarrollando aplicaciones que las utilizan."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla aplicaciones que gestionan la información almacenada en bases de datos objeto relacionales y orientadas a objetos valorando sus características y utilizando los mecanismos de acceso incorporados."},
    {"id":"RA5","pond":15,"nombre":"Desarrolla aplicaciones que gestionan la información almacenada en bases de datos nativas XML evaluando y utilizando clases específicas."},
    {"id":"RA6","pond":15,"nombre":"Programa componentes de acceso a datos identificando las características que debe poseer un componente y utilizando herramientas de desarrollo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado clases para la gestión de ficheros y directorios.",
        "Se han valorado las ventajas y los inconvenientes de las distintas formas de acceso.",
        "Se han utilizado las operaciones básicas para acceder a ficheros de acceso secuencial, directo y aleatorio.",
        "Se han utilizado clases para recuperar información almacenada en un fichero XML.",
        "Se han utilizado clases para almacenar información en un fichero XML.",
        "Se han utilizado clases para convertir a otro formato información contenida en un fichero XML.",
        "Se han previsto y gestionado las excepciones.",
        "Se han probado y documentado las aplicaciones desarrolladas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han valorado las ventajas e inconvenientes de utilizar conectores.",
        "Se han utilizado gestores de bases de datos embebidos e independientes.",
        "Se ha utilizado el conector idóneo en la aplicación.",
        "Se ha establecido la conexión.",
        "Se ha definido la estructura de la base de datos.",
        "Se han desarrollado aplicaciones que modifican el contenido de la base de datos.",
        "Se han definido los objetos destinados a almacenar el resultado de las consultas.",
        "Se han desarrollado aplicaciones que efectúan consultas.",
        "Se han ejecutado procedimientos en la base de datos.",
        "Se han eliminado los objetos una vez finalizada su función.",
        "Se han gestionado las transacciones.",
        "Se han definido modelos que comunican con la base de datos. Patrón Modelo-Vista-Controlador (MVC)",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado la herramienta ORM.",
        "Se ha configurado la herramienta ORM.",
        "Se han definido los ficheros de mapeo.",
        "Se han aplicado mecanismos de persistencia a los objetos.",
        "Se han desarrollado aplicaciones que modifican y recuperan objetos persistentes.",
        "Se han desarrollado aplicaciones que realizan consultas usando el lenguaje SQL.",
        "Se ha valorado la utilización de lenguajes propios de la herramienta ORM.",
        "Se han gestionado las transacciones.",
        "Se han creado diagramas ORM que presentan el mapeo entre clases persistentes y entidades.",
        "Se han sincronizado diagramas de clase con diagramas entidad relación.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las ventajas e inconvenientes de las bases de datos que almacenan objetos.",
        "Se han establecido y cerrado conexiones.",
        "Se han identificado distintos tipos de objetos y sus componentes.",
        "Se ha gestionado la persistencia de objetos simples.",
        "Se ha gestionado la persistencia de objetos estructurados.",
        "Se ha utilizado jerarquías de tipo, herencia y polimorfismo para gestionar objetos complejos.",
        "Se han desarrollado aplicaciones que realizan consultas.",
        "Se han modificado los objetos almacenados.",
        "Se han identificado las características principales del estándar ODMG.",
        "Se han gestionado las transacciones.",
        "Se han probado y documentado las aplicaciones desarrolladas.",
        "Se ha utilizado el lenguaje de consultas OQL.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han valorado las ventajas e inconvenientes de utilizar una base de datos nativa XML.",
        "Se ha instalado el gestor de base de datos.",
        "Se ha configurado el gestor de base de datos.",
        "Se ha establecido la conexión con la base de datos.",
        "Se han desarrollado aplicaciones que efectúan consultas sobre el contenido de la base de datos.",
        "Se han utilizado los lenguajes de consulta suministrados por el gestor de bases de datos.",
        "Se han añadido y eliminado colecciones de la base de datos.",
        "Se han desarrollado aplicaciones para añadir, modificar y eliminar documentos XML de la base de datos.",
        "Se han desarrollado modelos de datos XML.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han valorado las ventajas e inconvenientes de utilizar programación orientada a componentes.",
        "Se han identificado herramientas de desarrollo de componentes.",
        "Se han programado componentes que gestionan información almacenada en ficheros.",
        "Se han programado componentes que gestionan mediante conectores información almacenada en bases de datos.",
        "Se han programado componentes que gestionan información usando mapeo objeto relacional.",
        "Se han programado componentes que gestionan información almacenada en bases de datos objeto relacionales y orientadas a objetos.",
        "Se han programado componentes que gestionan información almacenada en una base de datos nativa XML.",
        "Se han probado y documentado los componentes desarrollados.",
        "Se han integrado los componentes desarrollados en aplicaciones.",
    ], start=1)],
}

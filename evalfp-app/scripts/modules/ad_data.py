"""EvalFP — Acceso a Datos (AD) · 0488 · 2º DAM · RD 450/2010"""
MODULO = {
    "nombre":"Acceso a Datos","codigo":"0488","abrev":"AD",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":6,"total_horas":192,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Gestión de la información almacenada en ficheros","horas":28,"eval":1,"tags":"Ficheros · Streams · NIO2 · JSON · XML · CSV"},
    {"id":"UT2","nombre":"Gestión de la información en bases de datos relacionales (JDBC)","horas":40,"eval":1,"tags":"JDBC · PreparedStatement · ResultSet · Transacciones · Pool"},
    {"id":"UT3","nombre":"Mapeo objeto-relacional (ORM)","horas":40,"eval":2,"tags":"JPA · Hibernate · EntityManager · JPQL · Spring Data"},
    {"id":"UT4","nombre":"Gestión de bases de datos XML","horas":20,"eval":2,"tags":"DOM · SAX · JAXB · XPath · XMLBeans"},
    {"id":"UT5","nombre":"Bases de datos NoSQL: documentales y clave/valor","horas":32,"eval":3,"tags":"MongoDB · Redis · Elasticsearch · Morphia · Spring Data Mongo"},
    {"id":"UT6","nombre":"Herramientas y técnicas ORM avanzadas","horas":32,"eval":3,"tags":"Spring Boot · Data JPA · Paginación · Caché · Auditoría"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Maneja información almacenada en ficheros reconociendo su uso y aplicando algoritmos de codificación/decodificación."},
    {"id":"RA2","pond":25,"nombre":"Desarrolla aplicaciones que gestionan información de bases de datos relacionales utilizando las características propias del lenguaje de programación."},
    {"id":"RA3","pond":25,"nombre":"Desarrolla aplicaciones que gestionan la información de bases de datos utilizando técnicas de mapeo objeto-relacional."},
    {"id":"RA4","pond":15,"nombre":"Desarrolla aplicaciones que gestionan la información almacenada en bases de datos XML evaluando y utilizando las posibilidades que proporciona."},
    {"id":"RA5","pond":20,"nombre":"Desarrolla aplicaciones que gestionan la información almacenada en bases de datos NoSQL, evaluando sus características y posibilidades."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA3",["CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han utilizado clases para manipular ficheros y directorios."},
        {"id":"CR2","texto":"Se han valorado las ventajas e inconvenientes de las distintas formas de acceso."},
        {"id":"CR3","texto":"Se han utilizado flujos de datos para leer y escribir información."},
        {"id":"CR4","texto":"Se ha obtenido información sobre los ficheros almacenados en el sistema de ficheros."},
        {"id":"CR5","texto":"Se ha trabajado con ficheros de acceso aleatorio."},
        {"id":"CR6","texto":"Se han aplicado filtros para el acceso a información en ficheros."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han identificado las características y ventajas de cada una de las alternativas de acceso a datos."},
        {"id":"CR2","texto":"Se han programado aplicaciones que establecen conexiones con bases de datos."},
        {"id":"CR3","texto":"Se ha escrito código para almacenar información en bases de datos."},
        {"id":"CR4","texto":"Se han creado programas para recuperar y mostrar información de bases de datos."},
        {"id":"CR5","texto":"Se han efectuado borrados y modificaciones sobre la información almacenada."},
        {"id":"CR6","texto":"Se han creado aplicaciones que ejecutan consultas sobre bases de datos."},
        {"id":"CR7","texto":"Se han creado aplicaciones para posibilitar la gestión de la información mediante transacciones."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han instalado y configurado herramientas de mapeo objeto-relacional."},
        {"id":"CR2","texto":"Se han definido la correspondencia entre clases y tablas."},
        {"id":"CR3","texto":"Se han aplicado los mecanismos de persistencia de objetos."},
        {"id":"CR4","texto":"Se han desarrollado aplicaciones que realizan operaciones CRUD sobre bases de datos."},
        {"id":"CR5","texto":"Se han realizado consultas mediante el lenguaje de la herramienta de mapeo."},
        {"id":"CR6","texto":"Se han eliminado inconvenientes del acceso a bases de datos mediante técnicas de mapeo."},
        {"id":"CR7","texto":"Se han documentado los programas y se han efectuado pruebas."},
        {"id":"CR8","texto":"Se han implementado relaciones entre entidades con anotaciones JPA."},
        {"id":"CR9","texto":"Se ha utilizado un framework de persistencia (Spring Data) en una aplicación real."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han reconocido los sistemas gestores de bases de datos XML más utilizados."},
        {"id":"CR2","texto":"Se han identificado sus características y los escenarios de uso recomendados."},
        {"id":"CR3","texto":"Se han instalado y analizado sistemas gestores de bases de datos XML."},
        {"id":"CR4","texto":"Se han realizado consultas XPath y XQuery."},
        {"id":"CR5","texto":"Se han desarrollado aplicaciones que procesan documentos XML con SAX y DOM."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado las características de las distintas bases de datos NoSQL."},
        {"id":"CR2","texto":"Se han seleccionado y utilizado sistemas de bases de datos NoSQL orientados a documentos."},
        {"id":"CR3","texto":"Se han utilizado sistemas de bases de datos NoSQL clave/valor."},
        {"id":"CR4","texto":"Se han programado aplicaciones que acceden a la información de bases de datos NoSQL."},
        {"id":"CR5","texto":"Se han adaptado aplicaciones a los modelos de datos NoSQL."},
        {"id":"CR6","texto":"Se han analizado los escenarios de uso de las distintas soluciones NoSQL."},
    ],
}

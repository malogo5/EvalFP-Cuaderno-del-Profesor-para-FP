"""
EvalFP — Desarrollo Web en Entorno Servidor (DWES)
Módulo: 0613 · 2º DAW · Ciclo: DAW
Decreto: RD 686/2010 (actualizado RD 405/2023)
"""
MODULO = {
    "nombre":"Desarrollo Web en Entorno Servidor","codigo":"0613","abrev":"DWES",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":8,"total_horas":256,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 686/2010, de 20 de mayo · Decreto CLM 230/2011, de 28 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Selección de arquitecturas y herramientas de programación","horas":20,"eval":1,"tags":"PHP · Python · Node.js · MVC · Frameworks"},
    {"id":"UT2","nombre":"Inserción de código en páginas web","horas":30,"eval":1,"tags":"PHP · Variables · Formularios · Sesiones · Cookies"},
    {"id":"UT3","nombre":"Programación orientada a objetos con PHP","horas":35,"eval":1,"tags":"Clases · Herencia · Interfaces · Namespaces · Composer"},
    {"id":"UT4","nombre":"Desarrollo de aplicaciones web utilizando código embebido","horas":35,"eval":2,"tags":"MySQL · PDO · CRUD · Preparadas · Transacciones"},
    {"id":"UT5","nombre":"Desarrollo de aplicaciones web utilizando frameworks","horas":45,"eval":2,"tags":"Laravel · Symfony · ORM · Eloquent · Migrations"},
    {"id":"UT6","nombre":"Utilización de técnicas de acceso a datos","horas":35,"eval":3,"tags":"APIs REST · JSON · JWT · OAuth · Swagger"},
    {"id":"UT7","nombre":"Servicios web y seguridad","horas":56,"eval":3,"tags":"SOAP · REST · Autenticación · XSS · CSRF · SQLi"},
]
RAS = [
    {"id":"RA1","pond":10,"nombre":"Selecciona las arquitecturas y tecnologías de programación sobre clientes web, identificando y analizando las capacidades y características de cada una."},
    {"id":"RA2","pond":20,"nombre":"Escribe sentencias ejecutables por un servidor web reconociendo y aplicando procedimientos de integración del código en lenguajes de marcas."},
    {"id":"RA3","pond":20,"nombre":"Escribe bloques de sentencias embebidos en lenguajes de marcas, seleccionando y utilizando las estructuras de programación del lenguaje."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla aplicaciones web embebidas en lenguajes de marcas analizando e incorporando funcionalidades de acuerdo al enunciado."},
    {"id":"RA5","pond":15,"nombre":"Desarrolla aplicaciones web identificando y aplicando mecanismos para separar el código de presentación de la lógica de negocio."},
    {"id":"RA6","pond":15,"nombre":"Desarrolla aplicaciones de acceso a datos web, analizando y utilizando características avanzadas del lenguaje."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT7","RA6",["CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han caracterizado y diferenciado los modelos de ejecución de código en el servidor y en el cliente web."},
        {"id":"CR2","texto":"Se han reconocido las ventajas que proporciona la separación de la lógica de negocio y la capa de presentación en el desarrollo de aplicaciones web."},
        {"id":"CR3","texto":"Se han evaluado las tecnologías y lenguajes de programación de servidor más utilizados."},
        {"id":"CR4","texto":"Se han identificado y caracterizado los principales frameworks de desarrollo web del servidor."},
        {"id":"CR5","texto":"Se han identificado los mecanismos de ejecución de código del servidor web."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han reconocido los mecanismos de generación de páginas web a partir de lenguajes de marcas con código embebido."},
        {"id":"CR2","texto":"Se han identificado las principales tecnologías asociadas."},
        {"id":"CR3","texto":"Se han utilizado etiquetas para la inclusión de código en el lenguaje de marcas."},
        {"id":"CR4","texto":"Se han reconocido la sintaxis del lenguaje de programación del servidor."},
        {"id":"CR5","texto":"Se han escrito sentencias simples y se han comprobado sus efectos en el documento resultante."},
        {"id":"CR6","texto":"Se han utilizado directivas para modificar el comportamiento predeterminado."},
        {"id":"CR7","texto":"Se han utilizado los distintos tipos de variables y operadores disponibles en el lenguaje."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han utilizado mecanismos de decisión en la creación de bloques de sentencias de código."},
        {"id":"CR2","texto":"Se han utilizado bucles y se ha verificado su funcionamiento."},
        {"id":"CR3","texto":"Se han utilizado arrays."},
        {"id":"CR4","texto":"Se han creado y utilizado funciones."},
        {"id":"CR5","texto":"Se han utilizado formularios web para la obtención y procesado de información del usuario."},
        {"id":"CR6","texto":"Se han empleado métodos para recuperar la información introducida en el formulario."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han utilizado objetos predefinidos del lenguaje."},
        {"id":"CR2","texto":"Se han creado clases y objetos."},
        {"id":"CR3","texto":"Se han utilizado mecanismos para el mantenimiento de la información entre peticiones HTTP."},
        {"id":"CR4","texto":"Se han utilizado mecanismos para el control de errores y excepciones."},
        {"id":"CR5","texto":"Se ha probado y documentado el código."},
        {"id":"CR6","texto":"Se han identificado y caracterizado los frameworks MVC del servidor."},
        {"id":"CR7","texto":"Se han utilizado librerías de acceso a datos (ORM)."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han valorado los mecanismos disponibles para el mantenimiento de la información."},
        {"id":"CR2","texto":"Se han utilizado mecanismos para gestionar sesiones de usuario."},
        {"id":"CR3","texto":"Se han utilizado mecanismos de autenticación basados en tokens (JWT)."},
        {"id":"CR4","texto":"Se ha utilizado un framework MVC para el desarrollo de aplicaciones web."},
        {"id":"CR5","texto":"Se han utilizado sistemas de plantillas para separar vista y lógica."},
        {"id":"CR6","texto":"Se han aplicado principios de diseño en capas."},
        {"id":"CR7","texto":"Se han utilizado gestores de dependencias (Composer, npm)."},
    ],
    "RA6":[
        {"id":"CR1","texto":"Se han desarrollado aplicaciones de acceso a datos web con tecnologías de servidor."},
        {"id":"CR2","texto":"Se ha utilizado la API REST para el acceso a recursos del servidor."},
        {"id":"CR3","texto":"Se han utilizado formatos de intercambio de datos: JSON y XML."},
        {"id":"CR4","texto":"Se han documentado las APIs con herramientas estándar (Swagger/OpenAPI)."},
        {"id":"CR5","texto":"Se han implementado mecanismos de autenticación y autorización."},
        {"id":"CR6","texto":"Se han identificado y aplicado medidas de seguridad en aplicaciones web."},
        {"id":"CR7","texto":"Se han aplicado medidas de protección frente a XSS, CSRF e inyección SQL."},
        {"id":"CR8","texto":"Se han realizado pruebas de las aplicaciones desarrolladas."},
    ],
}

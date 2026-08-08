"""EvalFP — Desarrollo Web en Entorno Cliente · 0612 · Desarrollo de Aplicaciones Web (DAW)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 2º · RA y CE: Decreto 230/2011, de 28/07/2011 (DOCM núm. 155, de 09/08/2011), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 224 h · 6 h/semana · 2º DAW.
"""
MODULO = {
    "nombre":"Desarrollo Web en Entorno Cliente","codigo":"0612","abrev":"DWEC",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":6,"total_horas":224,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 2º · RA y CE: Decreto 230/2011, de 28/07/2011 (DOCM núm. 155, de 09/08/2011), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Selección de arquitecturas y herramientas de programación","horas":24,"eval":1,"tags":"JS · ECMAScript · Navegadores · DOM · BOM"},
    {"id":"UT2","nombre":"Programación con arrays, funciones y objetos definidos por el usuario","horas":32,"eval":1,"tags":"Arrow functions · Closures · Prototipos · Clases ES6"},
    {"id":"UT3","nombre":"Aplicación de los objetos predefinidos del lenguaje","horas":32,"eval":1,"tags":"String · Array · Date · Math · RegExp"},
    {"id":"UT4","nombre":"Programa código para clientes Web","horas":36,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Interacción con el usuario: formularios y validación","horas":32,"eval":2,"tags":"Formularios · Validación · HTML5 Constraint API"},
    {"id":"UT6","nombre":"Manejo del DOM y eventos","horas":32,"eval":3,"tags":"DOM · Events · querySelector · addEventListener"},
    {"id":"UT7","nombre":"Comunicación asíncrona: AJAX y Fetch API","horas":36,"eval":3,"tags":"AJAX · Fetch · Promesas · async/await · REST"},
]
RAS = [
    {"id":"RA1","pond":11,"nombre":"Selecciona las arquitecturas y tecnologías de programación sobre clientes Web, identificando y analizando las capacidades y características de cada una."},
    {"id":"RA2","pond":15,"nombre":"Escribe sentencias simples, aplicando la sintaxis del lenguaje y verificando su ejecución sobre navegadores Web."},
    {"id":"RA3","pond":14,"nombre":"Escribe código, identificando y aplicando las funcionalidades aportadas por los objetos predefinidos del lenguaje."},
    {"id":"RA4","pond":16,"nombre":"Programa código para clientes Web analizando y utilizando estructuras definidas por el usuario."},
    {"id":"RA5","pond":14,"nombre":"Desarrolla aplicaciones Web interactivas integrando mecanismos de manejo de eventos."},
    {"id":"RA6","pond":14,"nombre":"Desarrolla aplicaciones web analizando y aplicando las características del modelo de objetos del documento."},
    {"id":"RA7","pond":16,"nombre":"Desarrolla aplicaciones Web dinámicas, reconociendo y aplicando mecanismos de comunicación asíncrona entre cliente y servidor."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6","RA7"]}
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
        "Se han caracterizado y diferenciado los modelos de ejecución de código en el servidor y en el cliente Web.",
        "Se han identificado las capacidades y mecanismos de ejecución de código de los navegadores Web.",
        "Se han identificado y caracterizado los principales lenguajes relacionados con la programación de clientes Web.",
        "Se han reconocido las particularidades de la programación de guiones y sus ventajas y desventajas sobre la programación tradicional.",
        "Se han verificado los mecanismos de integración de los lenguajes de marcas con los lenguajes de programación de clientes Web.",
        "Se han reconocido y evaluado las herramientas de programación sobre clientes Web.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha seleccionado un lenguaje de programación de clientes Web en función de sus posibilidades.",
        "Se han utilizado los distintos tipos de variables y operadores disponibles en el lenguaje.",
        "Se han identificado los ámbitos de utilización de las variables.",
        "Se han reconocido y comprobado las peculiaridades del lenguaje respecto a las conversiones entre distintos tipos de datos.",
        "Se han utilizado mecanismos de decisión en la creación de bloques de sentencias.",
        "Se han utilizado bucles y se ha verificado su funcionamiento.",
        "Se han añadido comentarios al código.",
        "Se han utilizado herramientas y entornos para facilitar la programación, prueba y depuración del código.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los objetos predefinidos del lenguaje.",
        "Se han analizado los objetos referentes a las ventanas del navegador y los documentos web que contienen.",
        "Se han escrito sentencias que utilicen los objetos predefinidos del lenguaje para cambiar el aspecto del navegador y el documento que contiene.",
        "Se han generado textos y etiquetas como resultado de la ejecución de código en el navegador.",
        "Se han escrito sentencias que utilicen los objetos predefinidos del lenguaje para interactuar con el usuario.",
        "Se han utilizado las características propias del lenguaje en documentos compuestos por varias ventanas y marcos.",
        "Se han utilizado “cookies” para almacenar información y recuperar su contenido.",
        "Se ha depurado y documentado el código.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado y utilizado las funciones predefinidas del lenguaje.",
        "Se han creado y utilizado funciones definidas por el usuario.",
        "Se han reconocido las características del lenguaje relativas a la creación y uso de arrays.",
        "Se han creado y utilizado arrays.",
        "Se han reconocido las características de orientación a objetos del lenguaje.",
        "Se ha creado código para definir la estructura de objetos.",
        "Se han creado métodos y propiedades.",
        "Se ha creado código que haga uso de objetos definidos por el usuario.",
        "Se ha depurado y documentado el código.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las posibilidades del lenguaje de marcas relativas a la captura de los eventos producidos.",
        "Se han identificado las características del lenguaje de programación relativas a la gestión de los eventos.",
        "Se han diferenciado los tipos de eventos que se pueden manejar.",
        "Se ha creado un código que capture y utilice eventos.",
        "Se han reconocido las capacidades del lenguaje relativas a la gestión de formularios Web.",
        "Se han validado formularios web utilizando eventos.",
        "Se han utilizado expresiones regulares para facilitar los procedimientos de validación.",
        "Se ha probado y documentado el código.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido el modelo de objetos del documento de una página Web.",
        "Se han identificado los objetos del modelo, sus propiedades y métodos.",
        "Se ha creado y verificado un código que acceda a la estructura del documento.",
        "Se han creado nuevos elementos de la estructura y modificado elementos ya existentes.",
        "Se han asociado acciones a los eventos del modelo.",
        "Se han identificado las diferencias que presenta el modelo en diferentes navegadores.",
        "Se han programado aplicaciones Web de forma que funcionen en navegadores con diferentes implementaciones del modelo.",
        "Se han independizado las tres facetas (contenido, aspecto y comportamiento), en aplicaciones Web.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado las ventajas e inconvenientes de utilizar mecanismos de comunicación asíncrona entre cliente y servidor Web.",
        "Se han analizado los mecanismos disponibles para el establecimiento de la comunicación asíncrona.",
        "Se han utilizado los objetos relacionados.",
        "Se han identificado sus propiedades y sus métodos.",
        "Se ha utilizado comunicación asíncrona en la actualización dinámica del documento Web.",
        "Se han utilizado distintos formatos en el envío y recepción de información.",
        "Se han programado aplicaciones Web asíncronas de forma que funcionen en diferentes navegadores.",
        "Se han clasificado y analizado librerías que faciliten la incorporación de las tecnologías de actualización dinámica a la programación de páginas Web.",
        "Se han creado y depurado programas que utilicen estas librerías.",
    ], start=1)],
}

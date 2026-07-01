"""
EvalFP — Desarrollo Web en Entorno Cliente (DWEC)
Módulo: 0612 · 2º DAW · Ciclo: DAW
Decreto: RD 686/2010, de 20 de mayo (actualizado RD 405/2023)
"""
MODULO = {
    "nombre":"Desarrollo Web en Entorno Cliente","codigo":"0612","abrev":"DWEC",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":8,"total_horas":256,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 686/2010, de 20 de mayo · Decreto CLM 230/2011, de 28 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Selección de arquitecturas y herramientas de programación","horas":20,"eval":1,"tags":"JS · ECMAScript · Navegadores · DOM · BOM"},
    {"id":"UT2","nombre":"Manejo del DOM y eventos","horas":35,"eval":1,"tags":"DOM · Events · querySelector · addEventListener"},
    {"id":"UT3","nombre":"Aplicación de los objetos predefinidos del lenguaje","horas":30,"eval":1,"tags":"String · Array · Date · Math · RegExp"},
    {"id":"UT4","nombre":"Programación con arrays, funciones y objetos definidos por el usuario","horas":35,"eval":2,"tags":"Arrow functions · Closures · Prototipos · Clases ES6"},
    {"id":"UT5","nombre":"Interacción con el usuario: formularios y validación","horas":30,"eval":2,"tags":"Formularios · Validación · HTML5 Constraint API"},
    {"id":"UT6","nombre":"Comunicación asíncrona: AJAX y Fetch API","horas":35,"eval":2,"tags":"AJAX · Fetch · Promesas · async/await · REST"},
    {"id":"UT7","nombre":"Frameworks JavaScript modernos","horas":40,"eval":3,"tags":"React · Vue · Angular · Components · State management"},
    {"id":"UT8","nombre":"Almacenamiento y seguridad en cliente","horas":31,"eval":3,"tags":"localStorage · sessionStorage · Cookies · CORS · CSP"},
]
RAS = [
    {"id":"RA1","pond":10,"nombre":"Selecciona las arquitecturas y tecnologías de programación sobre clientes web, identificando y analizando las capacidades y características de cada una."},
    {"id":"RA2","pond":15,"nombre":"Escribe sentencias simples aplicando la sintaxis del lenguaje y verificando su ejecución sobre navegadores web."},
    {"id":"RA3","pond":15,"nombre":"Escribe código, identificando y aplicando las funcionalidades aportadas por los objetos predefinidos del lenguaje."},
    {"id":"RA4","pond":15,"nombre":"Programa código para clientes web analizando y utilizando las capacidades y características del lenguaje de guiones."},
    {"id":"RA5","pond":15,"nombre":"Desarrolla aplicaciones web interactivas integrando mecanismos de manejo de eventos."},
    {"id":"RA6","pond":15,"nombre":"Desarrolla aplicaciones web analizando y aplicando las características del modelo de objetos del documento."},
    {"id":"RA7","pond":15,"nombre":"Desarrolla aplicaciones web dinámicas, reconociendo y aplicando mecanismos de comunicación asíncrona entre cliente y servidor."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT7","RA4",["CR7","CR8"]),
    ("UT8","RA4",["CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"], 3:["RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han caracterizado y diferenciado los modelos de ejecución de código en el servidor y en el cliente web."},
        {"id":"CR2","texto":"Se han reconocido las capacidades y limitaciones de ejecución de los navegadores web."},
        {"id":"CR3","texto":"Se ha analizado la compatibilidad de los navegadores con los estándares."},
        {"id":"CR4","texto":"Se han identificado los lenguajes de programación de clientes web."},
        {"id":"CR5","texto":"Se han analizado las herramientas de desarrollo de código disponibles."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se ha identificado la sintaxis básica del lenguaje de guiones."},
        {"id":"CR2","texto":"Se han utilizado tipos de datos del lenguaje."},
        {"id":"CR3","texto":"Se han utilizado las instrucciones del lenguaje."},
        {"id":"CR4","texto":"Se han utilizado los operadores del lenguaje."},
        {"id":"CR5","texto":"Se han probado y depurado el código JavaScript en los navegadores."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han identificado los objetos predefinidos del lenguaje."},
        {"id":"CR2","texto":"Se han utilizado los objetos de la jerarquía del navegador."},
        {"id":"CR3","texto":"Se han utilizado los objetos String, Array, Math y Date."},
        {"id":"CR4","texto":"Se han aplicado las expresiones regulares."},
        {"id":"CR5","texto":"Se han identificado las diferencias de compatibilidad entre navegadores."},
        {"id":"CR6","texto":"Se han utilizado métodos de depuración y documentación del código."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han definido y utilizado funciones en el lenguaje."},
        {"id":"CR2","texto":"Se han utilizado funciones de orden superior."},
        {"id":"CR3","texto":"Se han utilizado funciones flecha (arrow functions)."},
        {"id":"CR4","texto":"Se han definido clases mediante la sintaxis de ECMAScript moderno."},
        {"id":"CR5","texto":"Se han utilizado módulos JavaScript (ES Modules)."},
        {"id":"CR6","texto":"Se han aplicado patrones de diseño en el desarrollo."},
        {"id":"CR7","texto":"Se han utilizado frameworks JavaScript modernos."},
        {"id":"CR8","texto":"Se han desarrollado componentes de interfaz de usuario reutilizables."},
        {"id":"CR9","texto":"Se han gestionado el estado de la aplicación."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado los eventos del modelo de objetos del documento."},
        {"id":"CR2","texto":"Se han utilizado los eventos de teclado."},
        {"id":"CR3","texto":"Se han utilizado los eventos de ratón."},
        {"id":"CR4","texto":"Se han utilizado los eventos de los formularios."},
        {"id":"CR5","texto":"Se han creado controladores de eventos."},
        {"id":"CR6","texto":"Se han utilizado las capacidades del lenguaje para modificar los formularios."},
        {"id":"CR7","texto":"Se han validado formularios utilizando técnicas de programación y HTML5."},
    ],
    "RA6":[
        {"id":"CR1","texto":"Se ha reconocido el modelo de objetos del documento (DOM)."},
        {"id":"CR2","texto":"Se han identificado las diferencias entre el modelo de objetos del documento dinámico y el estático."},
        {"id":"CR3","texto":"Se han creado y modificado elementos del documento."},
        {"id":"CR4","texto":"Se han eliminado elementos del documento."},
        {"id":"CR5","texto":"Se han realizado modificaciones sobre los estilos del documento."},
        {"id":"CR6","texto":"Se han asociado acciones a los eventos del documento con manejadores de eventos."},
        {"id":"CR7","texto":"Se han reconocido y comprobado las posibilidades de animación ofrecidas por el lenguaje."},
    ],
    "RA7":[
        {"id":"CR1","texto":"Se han evaluado las ventajas e inconvenientes de utilizar comunicación asíncrona entre cliente y servidor web."},
        {"id":"CR2","texto":"Se han analizado los objetos que permiten comunicación asíncrona en JavaScript."},
        {"id":"CR3","texto":"Se han creado peticiones HTTP asíncronas."},
        {"id":"CR4","texto":"Se ha analizado y utilizado la API Fetch."},
        {"id":"CR5","texto":"Se han utilizado Promesas y async/await."},
        {"id":"CR6","texto":"Se han enviado parámetros y recuperado contenido."},
        {"id":"CR7","texto":"Se han construido frontends que consumen APIs REST."},
    ],
}

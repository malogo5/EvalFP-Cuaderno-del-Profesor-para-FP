"""
EvalFP — Programación (PRG)
Módulo: 0485 · 1º DAM · Ciclos: DAM, DAW
Decreto: RD 450/2010 (DAM), RD 686/2010 (DAW)
"""

MODULO = {
    "nombre":      "Programación",
    "codigo":      "0486",
    "abrev":       "PRG",
    "ciclo":       "Desarrollo de Aplicaciones Multiplataforma / Web (DAM/DAW)",
    "ciclo_clave": "DAM",
    "ciclo_nivel": "CFGS",
    "curso":       "1º DAM",
    "horas_sem":   8,
    "total_horas": 256,
    "anno":        "2026-2027",
    "eval_count":  3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Introducción a la programación","horas":20,"eval":1,"tags":"Algoritmos · Pseudocódigo · Diagramas de flujo · Tipos de datos"},
    {"id":"UT2","nombre":"Programación estructurada","horas":35,"eval":1,"tags":"Java · Python · Estructuras de control · Funciones"},
    {"id":"UT3","nombre":"Programación orientada a objetos","horas":45,"eval":1,"tags":"Clases · Objetos · Herencia · Polimorfismo · Encapsulación"},
    {"id":"UT4","nombre":"Desarrollo de clases y colecciones","horas":40,"eval":2,"tags":"ArrayList · HashMap · Generics · Iteradores · Lambdas"},
    {"id":"UT5","nombre":"Lectura y escritura de información","horas":30,"eval":2,"tags":"Ficheros · Streams · Serialización · JSON · XML"},
    {"id":"UT6","nombre":"Aplicación de las estructuras de almacenamiento","horas":30,"eval":2,"tags":"Listas · Pilas · Colas · Árboles · Grafos"},
    {"id":"UT7","nombre":"Utilización avanzada de clases e interfaces","horas":30,"eval":3,"tags":"Interfaces · Clases abstractas · Patrones de diseño · UML"},
    {"id":"UT8","nombre":"Mantenimiento del software","horas":26,"eval":3,"tags":"Testing · JUnit · Depuración · Refactoring · Control de versiones"},
]

RAS = [
    {"id":"RA1","pond":10,"nombre":"Reconoce la estructura de un programa informático, identificando y relacionando los elementos propios del lenguaje de programación utilizado."},
    {"id":"RA2","pond":15,"nombre":"Escribe y prueba programas sencillos, reconociendo y aplicando los fundamentos de la programación orientada a objetos."},
    {"id":"RA3","pond":20,"nombre":"Escribe y depura código, analizando y utilizando las estructuras de control del lenguaje."},
    {"id":"RA4","pond":15,"nombre":"Desarrolla programas organizados en clases analizando y aplicando los principios de la programación orientada a objetos."},
    {"id":"RA5","pond":10,"nombre":"Realiza operaciones de entrada y salida de información, utilizando procedimientos específicos del lenguaje y librerías de clases."},
    {"id":"RA6","pond":15,"nombre":"Escribe programas que manipulen información seleccionando y utilizando tipos avanzados de datos."},
    {"id":"RA7","pond":15,"nombre":"Desarrolla programas aplicando características avanzadas de los lenguajes orientados a objetos y del entorno de programación."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR6","CR7","CR8"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT8","RA7",["CR8","CR9"]),
]

EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"], 3:["RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se han identificado los bloques que componen la estructura de un programa informático."},
        {"id":"CR2","texto":"Se han creado proyectos de desarrollo de aplicaciones."},
        {"id":"CR3","texto":"Se han utilizado entornos integrados de desarrollo."},
        {"id":"CR4","texto":"Se han identificado los distintos tipos de variables y la utilidad específica de cada uno."},
        {"id":"CR5","texto":"Se ha modificado el código de un programa para crear y utilizar literales, constantes y variables."},
        {"id":"CR6","texto":"Se han clasificado, reconocido y utilizado en expresiones los operadores del lenguaje."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se han identificado los fundamentos de la programación orientada a objetos."},
        {"id":"CR2","texto":"Se han escrito y probado programas sencillos."},
        {"id":"CR3","texto":"Se han instanciado objetos a partir de clases predefinidas."},
        {"id":"CR4","texto":"Se han utilizado métodos y propiedades de los objetos."},
        {"id":"CR5","texto":"Se han escrito llamadas a métodos estáticos."},
        {"id":"CR6","texto":"Se han utilizado parámetros en la llamada a métodos."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se ha escrito y probado código que haga uso de estructuras de selección."},
        {"id":"CR2","texto":"Se han utilizado estructuras de repetición."},
        {"id":"CR3","texto":"Se han reconocido las posibilidades de las sentencias de salto y se han utilizado."},
        {"id":"CR4","texto":"Se han escrito programas que recorran arrays."},
        {"id":"CR5","texto":"Se han creado inicializado y recorrido arrays."},
        {"id":"CR6","texto":"Se han creado arrays multidimensionales."},
        {"id":"CR7","texto":"Se han analizado, escrito y probado código con arrays bidimensionales."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se ha reconocido la sintaxis, estructura y componentes típicos de una clase."},
        {"id":"CR2","texto":"Se han definido clases a partir de las cuales se pueden instanciar objetos."},
        {"id":"CR3","texto":"Se han creado constructores."},
        {"id":"CR4","texto":"Se han desarrollado programas que instancien y utilicen objetos de las clases creadas."},
        {"id":"CR5","texto":"Se han utilizado mecanismos para controlar la visibilidad de las clases y de sus miembros."},
        {"id":"CR6","texto":"Se han definido y utilizado clases heredadas."},
        {"id":"CR7","texto":"Se han creado y utilizado métodos estáticos."},
        {"id":"CR8","texto":"Se han definido y utilizado interfaces."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se ha utilizado la consola para realizar operaciones de entrada y salida de información."},
        {"id":"CR2","texto":"Se han aplicado formatos en la visualización de la información."},
        {"id":"CR3","texto":"Se han reconocido las posibilidades de entrada/salida del lenguaje y las librerías asociadas."},
        {"id":"CR4","texto":"Se han utilizado ficheros para almacenar y recuperar información."},
        {"id":"CR5","texto":"Se han creado programas que utilicen diversos métodos de acceso al contenido de los ficheros."},
        {"id":"CR6","texto":"Se han utilizado las herramientas del entorno de desarrollo para crear interfaces gráficas sencillas."},
        {"id":"CR7","texto":"Se han programado controladores de eventos."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han identificado las características de las colecciones de objetos."},
        {"id":"CR2","texto":"Se han distinguido los diferentes tipos de colecciones."},
        {"id":"CR3","texto":"Se han programado aplicaciones que utilicen colecciones."},
        {"id":"CR4","texto":"Se han usado iteradores para recorrer los elementos de las colecciones."},
        {"id":"CR5","texto":"Se han utilizado las clases de colección de la librería estándar."},
        {"id":"CR6","texto":"Se han identificado las operaciones sobre estructuras de datos (árboles, grafos)."},
        {"id":"CR7","texto":"Se han implementado y utilizado estructuras de datos simples."},
        {"id":"CR8","texto":"Se han utilizado expresiones lambda y streams."},
    ],
    "RA7": [
        {"id":"CR1","texto":"Se han identificado los conceptos de herencia, superclase y subclase."},
        {"id":"CR2","texto":"Se han utilizado modificadores para bloquear y forzar la herencia de clases."},
        {"id":"CR3","texto":"Se ha reconocido la incidencia de los constructores en la herencia."},
        {"id":"CR4","texto":"Se han creado clases que heredan de otras."},
        {"id":"CR5","texto":"Se han utilizado clases e interfaces del lenguaje."},
        {"id":"CR6","texto":"Se han utilizado los mecanismos de polimorfismo."},
        {"id":"CR7","texto":"Se han aplicado principios SOLID de diseño de software."},
        {"id":"CR8","texto":"Se han escrito y ejecutado pruebas unitarias con frameworks de testing."},
        {"id":"CR9","texto":"Se han utilizado herramientas de control de versiones (Git)."},
    ],
}

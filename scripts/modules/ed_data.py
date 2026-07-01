"""EvalFP — Entornos de Desarrollo (ED) · 0487 · 1º DAM/DAW · RD 450/2010 / RD 686/2010"""
MODULO = {
    "nombre":"Entornos de Desarrollo","codigo":"0487","abrev":"ED",
    "ciclo":"DAM","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":3,"total_horas":96,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de elementos del desarrollo de software","horas":14,"eval":1,"tags":"Ciclo de vida · Metodologías · SDLC"},
    {"id":"UT2","nombre":"Evaluación de entornos integrados de desarrollo","horas":14,"eval":1,"tags":"IntelliJ · VS Code · Eclipse · NetBeans"},
    {"id":"UT3","nombre":"Diseño y realización de pruebas","horas":25,"eval":2,"tags":"JUnit · Pytest · TDD · Pruebas unitarias · Cobertura"},
    {"id":"UT4","nombre":"Optimización y documentación","horas":18,"eval":2,"tags":"Refactoring · Javadoc · Docstrings · SonarQube"},
    {"id":"UT5","nombre":"Elaboración de diagramas de clases","horas":13,"eval":3,"tags":"UML · Clases · Relaciones · Herramientas CASE"},
    {"id":"UT6","nombre":"Elaboración de diagramas de comportamiento","horas":12,"eval":3,"tags":"Secuencia · Casos de uso · Actividad · Colaboración"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce los elementos y herramientas que intervienen en el desarrollo de un programa informático, analizando sus características y las fases en las que actúan hasta llegar a su ejecución."},
    {"id":"RA2","pond":20,"nombre":"Evalúa entornos integrados de desarrollo analizando sus características para editar código fuente y generar ejecutables."},
    {"id":"RA3","pond":25,"nombre":"Verifica el funcionamiento de programas diseñando y realizando pruebas."},
    {"id":"RA4","pond":20,"nombre":"Optimiza código empleando las herramientas disponibles en el entorno de desarrollo."},
    {"id":"RA5","pond":10,"nombre":"Genera diagramas de clases valorando su importancia en el desarrollo de aplicaciones y empleando las herramientas disponibles en el entorno."},
    {"id":"RA6","pond":10,"nombre":"Genera diagramas de comportamiento valorando su importancia en el desarrollo de aplicaciones y empleando las herramientas disponibles en el entorno."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se ha reconocido la relación de los programas con los componentes del sistema informático."},
        {"id":"CR2","texto":"Se han identificado las fases de desarrollo de una aplicación informática."},
        {"id":"CR3","texto":"Se han diferenciado los conceptos de código fuente, objeto y ejecutable."},
        {"id":"CR4","texto":"Se han reconocido las características de la generación de código intermedio para su ejecución en máquinas virtuales."},
        {"id":"CR5","texto":"Se han clasificado los lenguajes de programación."},
        {"id":"CR6","texto":"Se ha distinguido la programación estructurada y la orientada a objetos."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han instalado entornos de desarrollo, propietarios y libres."},
        {"id":"CR2","texto":"Se han añadido y eliminado módulos en el entorno de desarrollo."},
        {"id":"CR3","texto":"Se ha personalizado y automatizado el entorno de desarrollo."},
        {"id":"CR4","texto":"Se ha configurado el sistema de actualización del entorno de desarrollo."},
        {"id":"CR5","texto":"Se han generado ejecutables a partir de código fuente de diferentes lenguajes."},
        {"id":"CR6","texto":"Se han generado ejecutables a partir de un código fuente utilizando distintos entornos de desarrollo."},
        {"id":"CR7","texto":"Se han identificado las características comunes y específicas de diversos entornos de desarrollo."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han identificado los diferentes tipos de pruebas."},
        {"id":"CR2","texto":"Se han definido casos de prueba."},
        {"id":"CR3","texto":"Se han identificado las herramientas de depuración y prueba de aplicaciones ofrecidas por el entorno de desarrollo."},
        {"id":"CR4","texto":"Se han utilizado herramientas de depuración para definir puntos de ruptura y seguimiento."},
        {"id":"CR5","texto":"Se han utilizado las herramientas de depuración para examinar y modificar el comportamiento de un programa en tiempo de ejecución."},
        {"id":"CR6","texto":"Se ha documentado el plan de pruebas."},
        {"id":"CR7","texto":"Se han automatizado pruebas unitarias con frameworks especializados."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se ha identificado el concepto de refactorización."},
        {"id":"CR2","texto":"Se han identificado los patrones de refactorización de uso frecuente."},
        {"id":"CR3","texto":"Se han realizado operaciones de refactorización con las herramientas que proporciona el entorno de desarrollo."},
        {"id":"CR4","texto":"Se han controlado las versiones del código fuente mediante un repositorio."},
        {"id":"CR5","texto":"Se ha generado la documentación de los proyectos de forma automatizada."},
        {"id":"CR6","texto":"Se han utilizado herramientas de análisis de calidad de código."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado los conceptos básicos de la programación orientada a objetos."},
        {"id":"CR2","texto":"Se ha instalado el módulo del entorno integrado de desarrollo que permite la utilización de diagramas de clases."},
        {"id":"CR3","texto":"Se han identificado las herramientas para la elaboración de diagramas de clases."},
        {"id":"CR4","texto":"Se ha interpretado el significado de diagramas de clases."},
        {"id":"CR5","texto":"Se han trazado diagramas de clases a partir de las especificaciones de aplicaciones."},
        {"id":"CR6","texto":"Se ha generado código a partir de un diagrama de clases."},
    ],
    "RA6":[
        {"id":"CR1","texto":"Se han identificado los distintos tipos de diagramas de comportamiento."},
        {"id":"CR2","texto":"Se ha reconocido el significado de los diagramas de casos de uso."},
        {"id":"CR3","texto":"Se han interpretado diagramas de interacción."},
        {"id":"CR4","texto":"Se han elaborado diagramas de interacción sencillos."},
        {"id":"CR5","texto":"Se han interpretado y elaborado diagramas de actividades."},
        {"id":"CR6","texto":"Se han interpretado y elaborado diagramas de estados."},
    ],
}

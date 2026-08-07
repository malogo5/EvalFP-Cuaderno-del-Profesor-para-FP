"""EvalFP — Entornos de Desarrollo · 0487 · DAM
Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 81 h · 2 h/semana · 1º DAM.
"""
MODULO = {
    "nombre":"Entornos de Desarrollo","codigo":"0487","abrev":"ED",
    "ciclo":"DAM","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":2,"total_horas":81,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de elementos del desarrollo de software","horas":10,"eval":1,"tags":"Ciclo de vida · Metodologías · SDLC"},
    {"id":"UT2","nombre":"Evaluación de entornos integrados de desarrollo","horas":14,"eval":1,"tags":"IntelliJ · VS Code · Eclipse · NetBeans"},
    {"id":"UT3","nombre":"Diseño y realización de pruebas","horas":13,"eval":2,"tags":"JUnit · Pytest · TDD · Pruebas unitarias · Cobertura"},
    {"id":"UT4","nombre":"Optimización y documentación","horas":12,"eval":2,"tags":"Refactoring · Javadoc · Docstrings · SonarQube"},
    {"id":"UT5","nombre":"Elaboración de diagramas de clases","horas":12,"eval":3,"tags":"UML · Clases · Relaciones · Herramientas CASE"},
    {"id":"UT6","nombre":"Elaboración de diagramas de comportamiento","horas":20,"eval":3,"tags":"Secuencia · Casos de uso · Actividad · Colaboración"},
]
RAS = [
    {"id":"RA1","pond":12,"nombre":"Reconoce los elementos y herramientas que intervienen en el desarrollo de un programa informático, analizando sus características y las fases en las que actúan hasta llegar a su puesta en funcionamiento."},
    {"id":"RA2","pond":17,"nombre":"Evalúa entornos integrados de desarrollo, analizando, sus características para editar código fuente y generar ejecutables."},
    {"id":"RA3","pond":17,"nombre":"Verifica el funcionamiento de programas, diseñando y realizando pruebas."},
    {"id":"RA4","pond":15,"nombre":"Optimiza código empleando las herramientas disponibles en el entorno de desarrollo."},
    {"id":"RA5","pond":14,"nombre":"Genera diagramas de clases valorando su importancia en el desarrollo de aplicaciones y empleando las herramientas disponibles en el entorno."},
    {"id":"RA6","pond":25,"nombre":"Genera diagramas de comportamiento valorando su importancia en el desarrollo de aplicaciones y empleando las herramientas disponibles en el entorno."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
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
        "Se ha reconocido la relación de los programas con los componentes del sistema informático: memoria, procesador y periféricos, entre otros.",
        "Se han identificado las fases de desarrollo de una aplicación informática.",
        "Se han diferenciado los conceptos de código fuente, código objeto y código ejecutable.",
        "Se han reconocido las características de la generación de código intermedio para su ejecución en máquinas virtuales.",
        "Se han clasificado los lenguajes de programación.",
        "Se ha evaluado la funcionalidad ofrecida por las herramientas utilizadas en programación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado entornos de desarrollo, propietarios y libres.",
        "Se han añadido y eliminado módulos en el entorno de desarrollo.",
        "Se ha personalizado y automatizado el entorno de desarrollo.",
        "Se ha configurado el sistema de actualización del entorno de desarrollo.",
        "Se han generado ejecutables a partir de código fuente de diferentes lenguajes en un mismo entorno de desarrollo.",
        "Se han generado ejecutables a partir de un mismo código fuente con varios entornos de desarrollo.",
        "Se han identificado las características comunes y específicas de diversos entornos de desarrollo.",
        "Se han identificado ventajas e inconvenientes en el uso de distintos entornos de desarrollo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes tipos de pruebas.",
        "Se han definido casos de prueba.",
        "Se han identificado las herramientas de depuración y prueba de aplicaciones ofrecidas por el entorno de desarrollo.",
        "Se han utilizado herramientas de depuración para definir puntos de ruptura y seguimiento.",
        "Se han utilizado las herramientas de depuración para examinar y modificar el comportamiento de un programa en tiempo de ejecución.",
        "Se han efectuado pruebas unitarias de clases y funciones.",
        "Se han implementado pruebas automáticas.",
        "Se han documentado las incidencias detectadas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los patrones de refactorización más usuales.",
        "Se han elaborado las pruebas asociadas a la refactorización.",
        "Se ha revisado el código fuente usando un analizador de código.",
        "Se han identificado las posibilidades de configuración de un analizador de código.",
        "Se han aplicado patrones de refactorización con las herramientas que proporciona el entorno de desarrollo.",
        "Se ha realizado el control de versiones integrado en el entorno de desarrollo.",
        "Se han utilizado herramientas del entorno de desarrollo para documentar las clases.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los conceptos básicos de la programación orientada a objetos.",
        "Se ha instalado el módulo del entorno integrado de desarrollo que permite la utilización de diagramas de clases.",
        "Se han identificado las herramientas para la elaboración de diagramas de clases.",
        "Se ha interpretado el significado de diagramas de clases.",
        "Se han trazado diagramas de clases a partir de las especificaciones de las mismas.",
        "Se ha generado código a partir de un diagrama de clases.",
        "Se ha generado un diagrama de clases mediante ingeniería inversa.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de diagramas de comportamiento.",
        "Se ha reconocido el significado de los diagramas de casos de uso.",
        "Se han interpretado diagramas de interacción.",
        "Se han elaborado diagramas de interacción sencillos.",
        "Se ha interpretado el significado de diagramas de secuencia.",
        "Se han elaborado diagramas de secuencia sencillos.",
        "Se ha interpretado el significado de diagramas de colaboración.",
        "Se han elaborado diagramas de colaboración sencillos.",
        "Se ha interpretado el significado de diagramas de actividades.",
        "Se han elaborado diagramas de actividades sencillos.",
        "Se han interpretado diagramas de estados.",
        "Se han planteado diagramas de estados sencillos.",
    ], start=1)],
}

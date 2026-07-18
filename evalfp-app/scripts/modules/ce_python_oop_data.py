"""EvalFP — Programación Orientada a Objetos · CE Desarrollo de Aplicaciones en Python"""
MODULO = {
    "nombre":"Programación Orientada a Objetos","codigo":"PYOOP","abrev":"PYOOP",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":5,"total_horas":150,"anno":"2026-2027","eval_count":2,
    "decreto":"CE Desarrollo de Aplicaciones en Python (Decreto CLM — Turno Diurno)",
}
UTS = [
    {"id":"UT1","nombre":"Clases, objetos y encapsulamiento","horas":30,"eval":1,"tags":"class · __init__ · self · Atributos · Métodos · Propiedades · @property"},
    {"id":"UT2","nombre":"Herencia, polimorfismo e interfaces","horas":30,"eval":1,"tags":"Herencia · super() · Polimorfismo · ABC · Métodos abstractos · MRO"},
    {"id":"UT3","nombre":"Patrones de diseño y pruebas unitarias","horas":30,"eval":2,"tags":"SOLID · Singleton · Factory · Observer · unittest · pytest · TDD"},
    {"id":"UT4","nombre":"Acceso a bases de datos y APIs REST","horas":30,"eval":2,"tags":"SQLAlchemy · ORM · SQLite · requests · REST · JSON · FastAPI"},
    {"id":"UT5","nombre":"Proyecto integrador OOP","horas":30,"eval":2,"tags":"Proyecto · Arquitectura · Refactorización · Documentación · Git · UML"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Diseña e implementa clases en Python aplicando los principios de encapsulamiento y abstracción."},
    {"id":"RA2","pond":25,"nombre":"Aplica los mecanismos de herencia y polimorfismo en el diseño de jerarquías de clases."},
    {"id":"RA3","pond":20,"nombre":"Aplica patrones de diseño y desarrolla pruebas unitarias para garantizar la calidad del software."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla aplicaciones Python que acceden a bases de datos y consumen APIs REST."},
    {"id":"RA5","pond":10,"nombre":"Desarrolla un proyecto integrador aplicando los principios de la programación orientada a objetos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {"RA1":["practica"],"RA2":["practica"],"RA3":["practica"],"RA4":["practica"],"RA5":["proyecto"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido clases con atributos de instancia y de clase.",
        "Se han implementado métodos de instancia, de clase (@classmethod) y estáticos (@staticmethod).",
        "Se han aplicado el encapsulamiento mediante atributos privados y propiedades @property.",
        "Se han sobrecargado operadores utilizando métodos dunder (__str__, __repr__, __eq__, etc.).",
        "Se han utilizado dataclasses para simplificar la definición de clases de datos.",
        "Se ha aplicado el principio de responsabilidad única (SRP) en el diseño de clases.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha implementado herencia simple y múltiple entre clases Python.",
        "Se ha utilizado super() para invocar métodos de la clase padre.",
        "Se han aplicado los principios del polimorfismo para el tratamiento genérico de objetos.",
        "Se han definido clases abstractas con el módulo ABC (Abstract Base Classes).",
        "Se ha analizado el orden de resolución de métodos (MRO) en jerarquías complejas.",
        "Se ha aplicado el principio de sustitución de Liskov (LSP) en el diseño de jerarquías.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y aplicado los principios SOLID en el diseño orientado a objetos.",
        "Se han implementado los patrones de diseño Singleton, Factory y Observer.",
        "Se han desarrollado pruebas unitarias con el módulo unittest y con pytest.",
        "Se ha aplicado la metodología TDD (Test-Driven Development) en el desarrollo de funcionalidades.",
        "Se ha medido la cobertura de las pruebas con herramientas como coverage.py.",
        "Se ha realizado refactorización de código aplicando buenas prácticas y principios SOLID.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha conectado una aplicación Python a una base de datos SQLite mediante el módulo sqlite3.",
        "Se ha utilizado SQLAlchemy como ORM para el mapeo objeto-relacional.",
        "Se han consumido APIs REST externas utilizando la librería requests.",
        "Se han procesado respuestas JSON de APIs REST e integrado los datos en la aplicación.",
        "Se ha desarrollado una API REST sencilla con FastAPI o Flask.",
        "Se han aplicado buenas prácticas de seguridad en el acceso a bases de datos y APIs.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha diseñado la arquitectura del proyecto aplicando los principios OOP y SOLID.",
        "Se ha implementado el proyecto utilizando control de versiones con Git.",
        "Se ha documentado el proyecto con docstrings, README y diagramas UML.",
        "Se ha realizado una refactorización del código mejorando su calidad y mantenibilidad.",
        "Se ha presentado y defendido el proyecto ante el grupo, justificando las decisiones de diseño.",
    ], start=1)],
}

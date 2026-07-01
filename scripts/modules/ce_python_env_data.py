"""EvalFP — Entornos y Sintaxis en Python · CE Desarrollo de Aplicaciones en Python
Decreto CLM (Turno Diurno) · RD/Orden ministerial pendiente de publicación BOE
"""
MODULO = {
    "nombre":"Entornos y Sintaxis en Python","codigo":"PYENV","abrev":"PYENV",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"CE Desarrollo de Aplicaciones en Python (Decreto CLM — Turno Diurno)",
}
UTS = [
    {"id":"UT1","nombre":"Instalación y configuración del entorno Python","horas":15,"eval":1,"tags":"Python · Conda · venv · pip · IDE · VSCode · PyCharm · Jupyter"},
    {"id":"UT2","nombre":"Sintaxis fundamental de Python","horas":25,"eval":1,"tags":"Variables · Tipos · Operadores · Strings · Entrada/Salida · Funciones integradas"},
    {"id":"UT3","nombre":"Estructuras de datos y módulos","horas":20,"eval":2,"tags":"Listas · Tuplas · Diccionarios · Sets · Módulos · Paquetes · pip"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Configura entornos de desarrollo Python, diferenciando los distintos gestores de entornos y herramientas disponibles."},
    {"id":"RA2","pond":45,"nombre":"Escribe programas en Python utilizando la sintaxis fundamental del lenguaje."},
    {"id":"RA3","pond":30,"nombre":"Utiliza las principales estructuras de datos de Python y gestiona módulos y paquetes externos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","ejercicio"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado Python y se han configurado entornos virtuales con venv y conda.",
        "Se han utilizado gestores de paquetes (pip, conda) para instalar y actualizar librerías.",
        "Se ha configurado un IDE (VSCode, PyCharm) con las extensiones Python necesarias.",
        "Se han utilizado Jupyter Notebooks para el desarrollo interactivo.",
        "Se han descrito las ventajas del uso de entornos virtuales en proyectos Python.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han declarado variables y constantes utilizando los tipos de datos básicos de Python.",
        "Se han aplicado los operadores aritméticos, lógicos, de comparación y de asignación.",
        "Se han manipulado cadenas de texto utilizando los métodos y operaciones del tipo str.",
        "Se han leído datos del usuario mediante input() y se han mostrado resultados con print() y f-strings.",
        "Se han utilizado las funciones integradas más habituales de Python (len, range, type, etc.).",
        "Se ha depurado código Python utilizando el debugger del IDE y sentencias de traza.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado y manipulado listas, realizando operaciones de acceso, inserción y eliminación.",
        "Se han utilizado tuplas para almacenar datos inmutables.",
        "Se han creado y operado diccionarios para el almacenamiento de pares clave-valor.",
        "Se han utilizado conjuntos (sets) para operaciones de álgebra de conjuntos.",
        "Se han importado y utilizado módulos de la biblioteca estándar (math, os, sys, datetime).",
        "Se han instalado y utilizado paquetes externos mediante pip, gestionando el archivo requirements.txt.",
    ], start=1)],
}

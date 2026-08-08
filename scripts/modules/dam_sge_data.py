"""EvalFP — Sistemas de Gestión Empresarial · 0491 · Desarrollo de Aplicaciones Multiplataforma
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 158 h · 4 h/semana · 2º DAM.
"""
MODULO = {
    "nombre":"Sistemas de Gestión Empresarial","codigo":"0491","abrev":"SGE",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":4,"total_horas":158,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Identificación de sistemas ERP-CRM","horas":36,"eval":1,"tags":"ERP · CRM · Módulos · Licencias · Implantación · Mercado · SAP · Odoo"},
    {"id":"UT2","nombre":"Implanta sistemas ERP-CRM","horas":35,"eval":2,"tags":""},
    {"id":"UT3","nombre":"Realiza operaciones de gestión y consulta de la información","horas":28,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Adapta sistemas ERP-CRM","horas":35,"eval":3,"tags":""},
    {"id":"UT5","nombre":"Desarrolla componentes para un sistema ERP-CRM","horas":24,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":23,"nombre":"Identifica sistemas de planificación de recursos empresariales y de gestión de relaciones con clientes (ERP-CRM) reconociendo sus características y verificando la configuración del sistema informático."},
    {"id":"RA2","pond":23,"nombre":"Implanta sistemas ERP-CRM interpretando la documentación técnica e identificando las diferentes opciones y módulos."},
    {"id":"RA3","pond":17,"nombre":"Realiza operaciones de gestión y consulta de la información siguiendo las especificaciones de diseño y utilizando las herramientas proporcionadas por los sistemas ERP-CRM."},
    {"id":"RA4","pond":22,"nombre":"Adapta sistemas ERP-CRM identificando los requerimientos de un supuesto empresarial y utilizando las herramientas proporcionadas por los mismos."},
    {"id":"RA5","pond":15,"nombre":"Desarrolla componentes para un sistema ERP-CRM analizando y utilizando el lenguaje de programación incorporado."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la organización de una empresa.",
        "Se han reconocido los diferentes sistemas ERP-CRM que existen en el mercado.",
        "Se han comparado sistemas ERP-CRM en función de sus características y requisitos.",
        "Se ha identificado el sistema operativo adecuado a cada sistema ERP-CRM.",
        "Se ha identificado el sistema gestor de datos adecuado a cada sistema ERP-CRM.",
        "Se han verificado las configuraciones del sistema operativo y del gestor de datos para garantizar la funcionalidad del ERP-CRM.",
        "Se ha identificado el sistema de gestión empresarial con acceso móvil.",
        "Se han documentado las operaciones realizadas.",
        "Se han documentado las incidencias producidas durante el proceso.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes tipos de licencia.",
        "Se han identificado los módulos que componen el ERP-CRM.",
        "Se han realizado instalaciones monopuesto.",
        "Se han realizado instalaciones cliente/servidor.",
        "Se han configurado los módulos instalados.",
        "Se han realizado instalaciones adaptadas a las necesidades planteadas en diferentes supuestos.",
        "Se ha verificado el funcionamiento del ERP-CRM.",
        "Se han documentado las operaciones realizadas y las incidencias.",
        "Se ha instalado y configurado la asistencia técnica y remota en un sistema ERP-CRM.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado herramientas y lenguajes de consulta y manipulación de datos proporcionados por los sistemas ERP-CRM.",
        "Se han generado formularios.",
        "Se han generado informes.",
        "Se han exportado datos e informes.",
        "Se han automatizado las extracciones de datos mediante procesos.",
        "Se han realizado auditorías de control de acceso a datos y trazas del sistema.",
        "Se han documentado las operaciones realizadas y las incidencias observadas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las posibilidades de adaptación del ERP-CRM.",
        "Se han adaptado definiciones de campos, tablas y vistas de la base de datos del ERP-CRM.",
        "Se han adaptado consultas.",
        "Se han adaptado interfaces de entrada de datos y de procesos.",
        "Se han personalizado informes.",
        "Se han creado gráficos personalizados.",
        "Se han adaptado procedimientos almacenados de servidor.",
        "Se han realizado pruebas.",
        "Se han documentado las operaciones realizadas y las incidencias observadas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las sentencias del lenguaje propio del sistema ERP-CRM.",
        "Se han utilizado los elementos de programación del lenguaje para crear componentes de manipulación de datos.",
        "Se han modificado componentes software para añadir nuevas funcionalidades al sistema.",
        "Se han integrado los nuevos componentes software en el sistema ERP-CRM.",
        "Se ha verificado el correcto funcionamiento de los componentes creados.",
        "Se han documentado todos los componentes creados o modificados.",
    ], start=1)],
}

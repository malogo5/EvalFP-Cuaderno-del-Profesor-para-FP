"""EvalFP — Sistemas de Gestión Empresarial · 0492 · 2º DAM
RD 450/2010, de 16 de abril (BOE) · Decreto CLM 252/2011, de 17 de noviembre (DOCM)
"""
MODULO = {
    "nombre":"Sistemas de Gestión Empresarial","codigo":"0492","abrev":"SGE",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 450/2010, de 16 de abril · Decreto CLM 252/2011, de 17 de noviembre (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Identificación de sistemas ERP-CRM","horas":25,"eval":1,"tags":"ERP · CRM · Módulos · Licencias · Implantación · Mercado · SAP · Odoo"},
    {"id":"UT2","nombre":"Instalación y configuración de ERP","horas":35,"eval":1,"tags":"Odoo · PostgreSQL · Instancias · Módulos · Empresa · Moneda · Idioma"},
    {"id":"UT3","nombre":"Gestión de la información en el ERP","horas":35,"eval":2,"tags":"Ventas · Compras · Almacén · Contabilidad · RRHH · Importar · Exportar"},
    {"id":"UT4","nombre":"Adaptación de ERP-CRM","horas":35,"eval":2,"tags":"Vistas · Informes · Workflows · Módulos propios · Python · XML · ORM"},
    {"id":"UT5","nombre":"Desarrollo de componentes en ERP","horas":30,"eval":3,"tags":"Modelos · Vistas · Controladores · Herencia · Wizards · API REST"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Identifica sistemas de planificación de recursos empresariales y de gestión de relaciones con clientes reconociendo sus características y verificando su implantación."},
    {"id":"RA2","pond":20,"nombre":"Instala sistemas de planificación de recursos empresariales y gestión de relaciones con clientes interpretando las especificaciones técnicas."},
    {"id":"RA3","pond":20,"nombre":"Realiza operaciones de gestión y consulta de la información en sistemas ERP-CRM aplicando criterios de integridad de datos."},
    {"id":"RA4","pond":25,"nombre":"Adapta sistemas de planificación de recursos empresariales y de gestión de relaciones con clientes modificando su configuración."},
    {"id":"RA5","pond":20,"nombre":"Desarrolla componentes para sistemas de planificación de recursos empresariales y de gestión de relaciones con clientes verificando su funcionamiento."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las principales funciones de los sistemas ERP y CRM.",
        "Se han valorado las ventajas de los sistemas ERP-CRM frente a aplicaciones aisladas.",
        "Se han identificado los módulos principales de los sistemas ERP-CRM y su funcionalidad.",
        "Se han clasificado los principales sistemas ERP-CRM del mercado (libres y propietarios).",
        "Se ha analizado el proceso de implantación de un sistema ERP-CRM en una empresa.",
        "Se han identificado los tipos de licencias y los costes asociados.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado el servidor de bases de datos y el servidor de aplicaciones necesarios.",
        "Se ha instalado el sistema ERP-CRM y se han realizado las configuraciones iniciales.",
        "Se han creado la empresa y los datos maestros básicos.",
        "Se han instalado y activado los módulos necesarios.",
        "Se han creado usuarios y se han asignado los roles y perfiles correspondientes.",
        "Se ha verificado el correcto funcionamiento del sistema tras la instalación.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han introducido datos en el sistema siguiendo los procedimientos establecidos.",
        "Se han realizado consultas y búsquedas de información en el sistema.",
        "Se han realizado operaciones propias de los módulos de ventas, compras y almacén.",
        "Se han generado informes y listados con la información del sistema.",
        "Se han importado y exportado datos entre el sistema ERP y otras aplicaciones.",
        "Se han realizado copias de seguridad y restauración de los datos del sistema.",
        "Se ha verificado la integridad de los datos tras operaciones de importación y exportación.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha modificado la apariencia del sistema adaptándola a los requisitos del cliente.",
        "Se han modificado informes y listados existentes.",
        "Se han creado nuevos informes adaptados a los requisitos del cliente.",
        "Se han añadido campos personalizados a los formularios existentes.",
        "Se han configurado flujos de trabajo (workflows) según los procesos de la empresa.",
        "Se han creado y configurado vistas personalizadas del sistema.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las tecnologías y lenguajes de programación utilizados en el desarrollo de componentes.",
        "Se ha configurado el entorno de desarrollo del sistema ERP-CRM.",
        "Se han creado nuevos modelos de datos en el sistema.",
        "Se han desarrollado nuevas vistas y formularios para los modelos creados.",
        "Se han implementado métodos y lógica de negocio en los modelos.",
        "Se han desarrollado asistentes (wizards) para automatizar procesos del sistema.",
    ], start=1)],
}

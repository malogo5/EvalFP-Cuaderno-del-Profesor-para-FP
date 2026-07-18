"""EvalFP — Administración de Sistemas Gestores de Bases de Datos · 0377 · 2º ASIR
RD 1629/2009, de 30 de octubre (BOE) · Decreto CLM 200/2010, de 3 de agosto (DOCM)
"""
MODULO = {
    "nombre":"Administración de Sistemas Gestores de Bases de Datos","codigo":"0377","abrev":"ASGBD",
    "ciclo":"Administración de Sistemas Informáticos en Red","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"2º ASIR","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Instalación y configuración del SGBD","horas":30,"eval":1,"tags":"Oracle · MySQL · PostgreSQL · SQL Server · Instalación · Instancias · Parámetros"},
    {"id":"UT2","nombre":"Administración del almacenamiento","horas":30,"eval":1,"tags":"Tablespaces · Datafiles · Redo logs · Segmentos · Extensiones · ASM"},
    {"id":"UT3","nombre":"Seguridad y control de acceso","horas":35,"eval":2,"tags":"Usuarios · Roles · Privilegios · Auditoría · Cifrado · Perfiles"},
    {"id":"UT4","nombre":"Optimización del rendimiento","horas":35,"eval":2,"tags":"Índices · Estadísticas · Plan de ejecución · Caché · Tunning · AWR"},
    {"id":"UT5","nombre":"Copia de seguridad y recuperación","horas":30,"eval":3,"tags":"RMAN · Backup físico · Lógico · Export/Import · PITR · DataGuard"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Instala sistemas gestores de bases de datos, describiendo sus características y ajustando la configuración del sistema."},
    {"id":"RA2","pond":20,"nombre":"Configura el sistema gestor de bases de datos interpretando las especificaciones técnicas y los requisitos de explotación."},
    {"id":"RA3","pond":20,"nombre":"Implanta métodos de control de acceso utilizando los mecanismos de seguridad del SGBD."},
    {"id":"RA4","pond":20,"nombre":"Automatiza tareas de administración del gestor de bases de datos describiendo los procedimientos de ejecución."},
    {"id":"RA5","pond":20,"nombre":"Realiza planes de copias de seguridad y recuperación describiendo los procedimientos de ejecución."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características y tipos de sistemas gestores de bases de datos.",
        "Se han identificado los distintos tipos de licencias de los SGBD y sus condiciones de uso.",
        "Se ha instalado el SGBD y se han configurado los parámetros de inicialización básicos.",
        "Se han creado y configurado las instancias del SGBD.",
        "Se ha verificado el funcionamiento del SGBD tras la instalación.",
        "Se ha documentado el proceso de instalación y los parámetros de configuración aplicados.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado el almacenamiento del SGBD: espacios de tabla, ficheros de datos y redo logs.",
        "Se han creado y gestionado bases de datos con la estructura de almacenamiento adecuada.",
        "Se han configurado los parámetros de memoria del SGBD para optimizar el rendimiento.",
        "Se han creado y gestionado esquemas de usuario y sus objetos asociados.",
        "Se han configurado los procesos en segundo plano del SGBD.",
        "Se ha administrado el diccionario de datos del sistema.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado usuarios del SGBD con los parámetros de autenticación y perfil adecuados.",
        "Se han asignado y revocado privilegios de sistema y de objeto a usuarios y roles.",
        "Se han creado roles y se han asignado a usuarios para simplificar la gestión de privilegios.",
        "Se han definido perfiles de usuario para gestionar los recursos del sistema.",
        "Se ha configurado la auditoría del SGBD para registrar accesos y operaciones.",
        "Se han aplicado técnicas de cifrado de datos y comunicaciones.",
        "Se ha verificado que los controles de acceso implementados cumplen las políticas de seguridad.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las tareas de administración susceptibles de ser automatizadas.",
        "Se han creado procedimientos y funciones almacenadas para automatizar tareas administrativas.",
        "Se han programado trabajos planificados con el scheduler del SGBD.",
        "Se han creado alertas para notificar eventos críticos del sistema.",
        "Se han analizado los planes de ejecución para identificar consultas ineficientes.",
        "Se han creado y gestionado índices para mejorar el rendimiento de las consultas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los tipos de fallos que pueden producirse en un SGBD y sus consecuencias.",
        "Se han identificado las herramientas disponibles para la realización de copias de seguridad.",
        "Se ha diseñado un plan de copias de seguridad atendiendo a los requisitos de disponibilidad.",
        "Se han realizado copias de seguridad físicas y lógicas de la base de datos.",
        "Se han realizado restauraciones completas e incompletas (PITR) de la base de datos.",
        "Se han verificado la integridad de las copias de seguridad restaurándolas en un entorno de prueba.",
        "Se ha documentado el plan de copias de seguridad y los procedimientos de recuperación.",
    ], start=1)],
}

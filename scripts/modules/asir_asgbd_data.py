"""EvalFP — Administración de Sistemas Gestores de Bases de Datos · 0377 · Administración de Sistemas Informáticos en Red
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 65 h · 2 h/semana · 2º ASIR.
"""
MODULO = {
    "nombre":"Administración de Sistemas Gestores de Bases de Datos","codigo":"0377","abrev":"ASGBD",
    "ciclo":"Administración de Sistemas Informáticos en Red","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"2º ASIR","horas_sem":2,"total_horas":65,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Implanta sistemas gestores de bases de datos","horas":14,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Administración del almacenamiento","horas":11,"eval":1,"tags":"Tablespaces · Datafiles · Redo logs · Segmentos · Extensiones · ASM"},
    {"id":"UT3","nombre":"Implanta métodos de control de acceso","horas":11,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Automatiza tareas de administración del gestor describiéndolas y","horas":10,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Optimiza el rendimiento del sistema","horas":10,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Aplica criterios de disponibilidad analizándolos y ajustando la…","horas":9,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":22,"nombre":"Implanta sistemas gestores de bases de datos analizando sus características y ajustándose a los requerimientos del sistema."},
    {"id":"RA2","pond":16,"nombre":"Configura el sistema gestor de bases de datos interpretando las especificaciones técnicas y los requisitos de explotación."},
    {"id":"RA3","pond":16,"nombre":"Implanta métodos de control de acceso utilizando asistentes, herramientas gráficas y comandos del lenguaje del sistema gestor."},
    {"id":"RA4","pond":16,"nombre":"Automatiza tareas de administración del gestor describiéndolas y utilizando guiones de sentencias."},
    {"id":"RA5","pond":16,"nombre":"Optimiza el rendimiento del sistema aplicando técnicas de monitorización y realizando adaptaciones."},
    {"id":"RA6","pond":14,"nombre":"Aplica criterios de disponibilidad analizándolos y ajustando la configuración del sistema gestor."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la utilidad y función de cada uno de los elementos de un sistema gestor de bases de datos.",
        "Se han analizado las características de los principales sistemas gestores de bases de datos.",
        "Se ha seleccionado el sistema gestor de bases de datos.",
        "Se ha identificado el software necesario para llevar a cabo la instalación.",
        "Se ha verificado el cumplimiento de los requisitos hardware.",
        "Se han instalado sistemas gestores de bases de datos.",
        "Se ha documentado el proceso de instalación.",
        "Se ha interpretado la información suministrada por los mensajes de error y ficheros de registro.",
        "Se han resuelto las incidencias de la instalación.",
        "Se ha verificado el funcionamiento del sistema gestor de bases de datos.",
        "Se han reconocido las diferencias existentes entre sistemas gestores de bases de datos transaccionales (OLTP) y sistemas gestores de bases de datos orientadas al procesamiento analítico (OLAP).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las condiciones de inicio y parada del sistema gestor.",
        "Se ha seleccionado el motor de base de datos.",
        "Se han asegurado las cuentas de administración.",
        "Se han configurado las herramientas y software cliente del sistema gestor.",
        "Se ha configurado la conectividad en red del sistema gestor.",
        "Se han definido las características por defecto de las bases de datos.",
        "Se han definido los parámetros relativos a las conexiones (tiempos de espera, número máximo de conexiones, entre otros).",
        "Se ha documentado el proceso de configuración.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado vistas personalizadas para cada tipo de usuario.",
        "Se han creado sinónimos de tablas y vistas.",
        "Se han definido y eliminado cuentas de usuario.",
        "Se han identificado los privilegios sobre las bases de datos y sus elementos.",
        "Se han agrupado y desagrupado privilegios.",
        "Se han asignado y eliminado privilegios a usuarios.",
        "Se han asignado y eliminado grupos de privilegios a usuarios.",
        "Se ha garantizando el cumplimiento de los requisitos de seguridad.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la importancia de automatizar tareas administrativas.",
        "Se han descrito los distintos métodos de ejecución de guiones.",
        "Se han identificado las herramientas disponibles para redactar guiones.",
        "Se han definido y utilizado guiones para automatizar tareas.",
        "Se han identificado los eventos susceptibles de activar disparadores.",
        "Se han definido disparadores.",
        "Se han utilizado estructuras de control de flujo.",
        "Se han adoptado medidas para mantener la integridad y consistencia de la información.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas de monitorización disponibles para el sistema gestor.",
        "Se han descrito las ventajas e inconvenientes de la creación de índices.",
        "Se han creado índices en tablas y vistas.",
        "Se ha optimizado la estructura de la base de datos.",
        "Se han optimizado los recursos del sistema gestor.",
        "Se ha obtenido información sobre el rendimiento de las consultas para su optimización.",
        "Se han programado alertas de rendimiento.",
        "Se han realizado modificaciones en la configuración del sistema operativo para mejorar el rendimiento del gestor.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la utilidad de las bases de datos distribuidas.",
        "Se han descrito las distintas políticas de fragmentación de la información.",
        "Se ha implantado una base de datos distribuida homogénea.",
        "Se ha creado una base de datos distribuida mediante la integración de un conjunto de bases de datos preexistentes.",
        "Se ha configurado un «nodo» maestro y varios «esclavos» para llevar a cabo la replicación del primero.",
        "Se ha configurado un sistema de replicación en cadena.",
        "Se ha comprobado el efecto de la parada de determinados nodos sobre los sistemas distribuidos y replicados.",
    ], start=1)],
}

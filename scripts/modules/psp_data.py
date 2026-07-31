"""EvalFP — Programación de Servicios y Procesos · 0490 · Desarrollo de Aplicaciones Multiplataforma (DAM)
Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 84 h · 2 h/semana · 2º DAM.
"""
MODULO = {
    "nombre":"Programación de Servicios y Procesos","codigo":"0490","abrev":"PSP",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":2,"total_horas":84,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Programación multiproceso","horas":18,"eval":1,"tags":"Procesos · Fork · ProcessBuilder · IPC · Pipes · Señales"},
    {"id":"UT2","nombre":"Programación multihilo","horas":17,"eval":1,"tags":"Threads · Runnable · Sincronización · Semáforos · Monitores"},
    {"id":"UT3","nombre":"Programa mecanismos de comunicación en red empleando sockets y","horas":17,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Generación de servicios en red","horas":15,"eval":3,"tags":"APIs REST · Spring Boot · WebSockets · gRPC · Microservicios"},
    {"id":"UT5","nombre":"Protege las aplicaciones y los datos definiendo y","horas":17,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":21,"nombre":"Desarrolla aplicaciones compuestas por varios procesos reconociendo y aplicando principios de programación paralela."},
    {"id":"RA2","pond":21,"nombre":"Desarrolla aplicaciones compuestas por varios hilos de ejecución analizando y aplicando librerías específicas del lenguaje de programación."},
    {"id":"RA3","pond":20,"nombre":"Programa mecanismos de comunicación en red empleando sockets y analizando el escenario de ejecución."},
    {"id":"RA4","pond":18,"nombre":"Desarrolla aplicaciones que ofrecen servicios en red, utilizando librerías de clases y aplicando criterios de eficiencia y disponibilidad."},
    {"id":"RA5","pond":20,"nombre":"Protege las aplicaciones y los datos definiendo y aplicando criterios de seguridad en el acceso, almacenamiento y transmisión de la información."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las características de la programación concurrente y sus ámbitos de aplicación.",
        "Se han identificado las diferencias entre programación paralela y programación distribuida, sus ventajas e inconvenientes.",
        "Se han analizado las características de los procesos y de su ejecución por el sistema operativo.",
        "Se han caracterizado los hilos de ejecución y descrito su relación con los procesos.",
        "Se han utilizado clases para programar aplicaciones que crean subprocesos.",
        "Se han utilizado mecanismos para sincronizar y obtener el valor devuelto por los subprocesos iniciados.",
        "Se han desarrollado aplicaciones que gestionen y utilicen procesos para la ejecución de varias tareas en paralelo.",
        "Se han depurado y documentado las aplicaciones desarrolladas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado situaciones en las que resulte útil la utilización de varios hilos en un programa.",
        "Se han reconocido los mecanismos para crear, iniciar y finalizar hilos.",
        "Se han programado aplicaciones que implementen varios hilos.",
        "Se han identificado los posibles estados de ejecución de un hilo y programado aplicaciones que los gestionen.",
        "Se han utilizado mecanismos para compartir información entre varios hilos de un mismo proceso.",
        "Se han desarrollado programas formados por varios hilos sincronizados mediante técnicas específicas.",
        "Se ha establecido y controlado la prioridad de cada uno de los hilos de ejecución.",
        "Se han depurado y documentado los programas desarrollados.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado escenarios que precisan establecer comunicación en red entre varias aplicaciones.",
        "Se han identificado los roles de cliente y de servidor y sus funciones asociadas.",
        "Se han reconocido librerías y mecanismos del lenguaje de programación que permiten programar aplicaciones en red.",
        "Se ha analizado el concepto de socket, sus tipos y características.",
        "Se han utilizado sockets para programar una aplicación cliente que se comunique con un servidor.",
        "Se ha desarrollado una aplicación servidor en red y verificado su funcionamiento.",
        "Se han desarrollado aplicaciones que utilizan sockets para intercambiar información.",
        "Se han utilizado hilos para implementar los procedimientos de las aplicaciones relativos a la comunicación en red.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado librerías que permitan implementar protocolos estándar de comunicación en red.",
        "Se han programado clientes de protocolos estándar de comunicaciones y verificado su funcionamiento.",
        "Se han desarrollado y probado servicios de comunicación en red.",
        "Se han analizado los requerimientos necesarios para crear servicios capaces de gestionar varios clientes concurrentes.",
        "Se han incorporado mecanismos para posibilitar la comunicación simultánea de varios clientes con el servicio.",
        "Se ha verificado la disponibilidad del servicio.",
        "Se han depurado y documentado las aplicaciones desarrolladas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y aplicado principios y prácticas de programación segura.",
        "Se han analizado las principales técnicas y prácticas criptográficas.",
        "Se han definido e implantado políticas de seguridad para limitar y controlar el acceso de los usuarios a las aplicaciones desarrolladas.",
        "Se han utilizado esquemas de seguridad basados en roles.",
        "Se han empleado algoritmos criptográficos para proteger el acceso a la información almacenada.",
        "Se han identificado métodos para asegurar la información transmitida.",
        "Se han desarrollado aplicaciones que utilicen sockets seguros para la transmisión de información.",
        "Se han depurado y documentado las aplicaciones desarrolladas.",
    ], start=1)],
}

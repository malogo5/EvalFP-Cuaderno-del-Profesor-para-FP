"""EvalFP — Programación de Servicios y Procesos (PSP) · 0489 · 2º DAM · RD 450/2010"""
MODULO = {
    "nombre":"Programación de Servicios y Procesos","codigo":"0489","abrev":"PSP",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":3,"total_horas":96,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Programación multiproceso","horas":24,"eval":1,"tags":"Procesos · Fork · ProcessBuilder · IPC · Pipes · Señales"},
    {"id":"UT2","nombre":"Programación multihilo","horas":30,"eval":2,"tags":"Threads · Runnable · Sincronización · Semáforos · Monitores"},
    {"id":"UT3","nombre":"Programación de comunicaciones en red","horas":24,"eval":2,"tags":"Sockets · TCP · UDP · ServerSocket · Protocolo HTTP"},
    {"id":"UT4","nombre":"Generación de servicios en red","horas":18,"eval":3,"tags":"APIs REST · Spring Boot · WebSockets · gRPC · Microservicios"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Desarrolla aplicaciones compuestas por varios procesos reconociendo y aplicando principios de programación paralela."},
    {"id":"RA2","pond":30,"nombre":"Desarrolla aplicaciones compuestas por varios hilos de ejecución analizando y aplicando librerías específicas del lenguaje de programación."},
    {"id":"RA3","pond":25,"nombre":"Programa mecanismos de comunicación en red empleando interfaces estándar de programación de red para intercambiar información entre aplicaciones."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla aplicaciones que ofrecen servicios en red, utilizando librerías de clases y aplicando criterios de eficiencia y disponibilidad."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han reconocido las características de los procesos y de su ejecución."},
        {"id":"CR2","texto":"Se han descrito las diferencias entre programación secuencial y paralela."},
        {"id":"CR3","texto":"Se ha lanzado la ejecución de procesos desde el programa."},
        {"id":"CR4","texto":"Se han obtenido y procesado los resultados devueltos por los procesos ejecutados."},
        {"id":"CR5","texto":"Se han utilizado mecanismos para sincronizar y obtener el valor retornado por los procesos."},
        {"id":"CR6","texto":"Se han utilizado mecanismos de comunicación entre procesos (pipes, memoria compartida)."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han identificado situaciones en las que resulta útil la utilización de varios hilos en un programa."},
        {"id":"CR2","texto":"Se han reconocido los mecanismos disponibles en el lenguaje de programación para crear y gestionar hilos."},
        {"id":"CR3","texto":"Se han desarrollado programas con varios hilos."},
        {"id":"CR4","texto":"Se han identificado los posibles estados de ejecución de un hilo."},
        {"id":"CR5","texto":"Se han utilizado mecanismos para compartir información entre varios hilos de un mismo proceso."},
        {"id":"CR6","texto":"Se han desarrollado programas formados por varios hilos sincronizados mediante semáforos."},
        {"id":"CR7","texto":"Se ha establecido y controlado la prioridad de los hilos."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han identificado las características y funciones de las interfaces de programación de red."},
        {"id":"CR2","texto":"Se han utilizado sockets para programar aplicaciones que se comunican mediante el protocolo TCP."},
        {"id":"CR3","texto":"Se han desarrollado aplicaciones que se comunican mediante el protocolo UDP."},
        {"id":"CR4","texto":"Se han utilizado las clases proporcionadas por el lenguaje de programación para transmitir objetos a través de la red."},
        {"id":"CR5","texto":"Se han utilizado sockets seguros para el intercambio de información."},
        {"id":"CR6","texto":"Se han utilizado las clases proporcionadas por el lenguaje de programación para programar comunicaciones HTTP."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han analizado las características necesarias para el desarrollo de servicios en red."},
        {"id":"CR2","texto":"Se han desarrollado servidores de transferencia de ficheros."},
        {"id":"CR3","texto":"Se han desarrollado servidores de correo electrónico y de mensajería."},
        {"id":"CR4","texto":"Se han desarrollado servicios de comunicaciones."},
        {"id":"CR5","texto":"Se ha programado un servidor HTTP con soporte de tecnología dinámica."},
        {"id":"CR6","texto":"Se han desarrollado servicios interoperables mediante APIs REST y formatos estándar."},
    ],
}

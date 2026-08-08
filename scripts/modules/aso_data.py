"""EvalFP — Administración de Sistemas Operativos · 0374 · Administración de Sistemas Informáticos en Red (ASIR)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 242 h · 6 h/semana · 2º ASIR.
"""
MODULO = {
    "nombre":"Administración de Sistemas Operativos","codigo":"0374","abrev":"ASO",
    "ciclo":"Administración de Sistemas Informáticos en Red (ASIR)","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"2º ASIR","horas_sem":6,"total_horas":242,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Administra el servicio de directorio","horas":38,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Administra procesos del sistema describiéndolos y","horas":34,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Gestiona la automatización de tareas del sistema","horas":34,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Administra de forma remota el sistema operativo en red","horas":34,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Administra servidores de impresión","horas":34,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Integra sistemas operativos libres y propietarios","horas":34,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Utiliza lenguajes de guiones en sistemas operativos","horas":34,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Administra el servicio de directorio interpretando especificaciones e integrándolo en una red."},
    {"id":"RA2","pond":14,"nombre":"Administra procesos del sistema describiéndolos y aplicando criterios de seguridad y eficiencia."},
    {"id":"RA3","pond":14,"nombre":"Gestiona la automatización de tareas del sistema, aplicando criterios de eficiencia y utilizando comandos y herramientas gráficas."},
    {"id":"RA4","pond":14,"nombre":"Administra de forma remota el sistema operativo en red valorando su importancia y aplicando criterios de seguridad."},
    {"id":"RA5","pond":14,"nombre":"Administra servidores de impresión describiendo sus funciones e integrándolos en una red."},
    {"id":"RA6","pond":14,"nombre":"Integra sistemas operativos libres y propietarios, justificando y garantizando su interoperabilidad."},
    {"id":"RA7","pond":14,"nombre":"Utiliza lenguajes de guiones en sistemas operativos, describiendo su aplicación y administrando servicios del sistema operativo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado la función, los elementos y las estructuras lógicas del servicio de directorio.",
        "Se ha determinado y creado el esquema del servicio de directorio.",
        "Se ha realizado la instalación del servicio de directorio en el servidor.",
        "Se ha realizado la configuración y personalización del servicio de directorio.",
        "Se ha integrado el servicio de directorio con otros servicios.",
        "Se han aplicado filtros de búsqueda en el servicio de directorio.",
        "Se ha utilizado el servicio de directorio como mecanismo de acreditación centralizada de los usuarios en una red.",
        "Se ha realizado la configuración del cliente para su integración en el servicio de directorio.",
        "Se han utilizado herramientas gráficas y comandos para la administración del servicio de directorio.",
        "Se ha documentado la estructura e implantación del servicio de directorio.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito el concepto de proceso del sistema, tipos, estados y ciclo de vida.",
        "Se han utilizado interrupciones y excepciones para describir los eventos internos del procesador.",
        "Se ha diferenciado entre proceso, hilo y trabajo.",
        "Se han realizado tareas de creación, manipulación y terminación de procesos.",
        "Se ha utilizado el sistema de archivos como medio lógico para el registro e identificación de los procesos del sistema.",
        "Se han utilizado herramientas gráficas y comandos para el control y seguimiento de los procesos del sistema.",
        "Se ha comprobado la secuencia de arranque del sistema, los procesos implicados y la relación entre ellos.",
        "Se han tomado medidas de seguridad ante la aparición de procesos no identificados.",
        "Se han documentado los procesos habituales del sistema, su función y relación entre ellos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las ventajas de la automatización de las tareas repetitivas en el sistema.",
        "Se han utilizado los comandos del sistema para la planificación de tareas.",
        "Se han establecido restricciones de seguridad.",
        "Se han realizado planificaciones de tareas repetitivas o puntuales relacionadas con la administración del sistema.",
        "Se ha automatizado la administración de cuentas.",
        "Se han instalado y configurado herramientas gráficas para la planificación de tareas.",
        "Se han utilizado herramientas gráficas para la planificación de tareas.",
        "Se han documentado los procesos programados como tareas automáticas.",
        "Se han creado perfiles de usuarios.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito métodos de acceso y administración remota de sistemas.",
        "Se ha diferenciado entre los servicios orientados a sesión y los no orientados a sesión.",
        "Se han utilizado herramientas de administración remota suministradas por el propio sistema operativo.",
        "Se han instalado servicios de acceso y administración remota.",
        "Se han utilizado comandos y herramientas gráficas para gestionar los servicios de acceso y administración remota.",
        "Se han creado cuentas de usuario para el acceso remoto.",
        "Se han realizado pruebas de acceso y administración remota entre sistemas heterogéneos.",
        "Se han utilizado mecanismos de encriptación de la información transferida.",
        "Se han documentado los procesos y servicios del sistema administrados de forma remota.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la funcionalidad de los sistemas y servidores de impresión.",
        "Se han identificado los puertos y los protocolos utilizados.",
        "Se han utilizado las herramientas para la gestión de impresoras integradas en el sistema operativo.",
        "Se ha instalado y configurado un servidor de impresión en entorno Web.",
        "Se han creado y clasificado impresoras lógicas.",
        "Se han creado grupos de impresión.",
        "Se han gestionado impresoras y colas de trabajos mediante comandos y herramientas gráficas.",
        "Se han compartido impresoras en red entre sistemas operativos diferentes.",
        "Se ha documentado la configuración del servidor de impresión y de las impresoras creadas.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la necesidad de compartir recursos en red entre diferentes sistemas operativos.",
        "Se han establecido niveles de seguridad para controlar el acceso del cliente a los recursos compartidos en red.",
        "Se ha comprobado la conectividad de la red en un escenario heterogéneo.",
        "Se ha descrito la funcionalidad de los servicios que permiten compartir recursos en red.",
        "Se han instalado y configurado servicios para compartir recursos en red.",
        "Se ha comprobado el funcionamiento de los servicios instalados.",
        "Se ha trabajado en grupo para acceder a sistemas de archivos e impresoras en red desde equipos con diferentes sistemas operativos.",
        "Se ha documentado la configuración de los servicios instalados.",
        "Administra la información ubicada en sistemas de archivos remotos de modo centralizado",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado y combinado las estructuras del lenguaje para crear guiones.",
        "Se han utilizado herramientas para depurar errores sintácticos y de ejecución.",
        "Se han interpretado guiones de configuración del sistema operativo.",
        "Se han realizado cambios y adaptaciones de guiones del sistema.",
        "Se han creado y probado guiones de administración de servicios.",
        "Se han creado y probado guiones de automatización de tareas.",
        "Se han implantado guiones en sistemas libres y propietarios.",
        "Se han consultado y utilizado librerías de funciones.",
        "Se han documentado los guiones creados.",
    ], start=1)],
}

"""EvalFP — Sistemas Operativos Monopuesto · 0222 · Sistemas Microinformáticos y Redes (SMR)
Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 169 h · 5 h/semana · 1º SMR.
"""
MODULO = {
    "nombre":"Sistemas Operativos Monopuesto","codigo":"0222","abrev":"SOM",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":5,"total_horas":169,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Reconoce las características de los sistemas de archivo","horas":28,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Instala sistemas operativos","horas":49,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Realiza tareas básicas de configuración de sistemas operativos","horas":32,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Realiza operaciones básicas de administración de sistemas operativos","horas":32,"eval":3,"tags":""},
    {"id":"UT5","nombre":"Crea máquinas virtuales","horas":28,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":17,"nombre":"Reconoce las características de los sistemas de archivo, describiendo sus tipos y aplicaciones."},
    {"id":"RA2","pond":28,"nombre":"Instala sistemas operativos, relacionando sus características con el hardware del equipo y el software de aplicación."},
    {"id":"RA3","pond":19,"nombre":"Realiza tareas básicas de configuración de sistemas operativos, interpretando requerimientos y describiendo los procedimientos seguidos."},
    {"id":"RA4","pond":19,"nombre":"Realiza operaciones básicas de administración de sistemas operativos, interpretando requerimientos y optimizando el sistema para su uso."},
    {"id":"RA5","pond":17,"nombre":"Crea máquinas virtuales identificando su campo de aplicación e instalando software específico."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
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
        "Se han identificado y descrito los elementos funcionales de un sistema informático.",
        "Se ha codificado y relacionado la información en los diferentes sistemas de representación.",
        "Se han identificado los procesos y sus estados.",
        "Se ha descrito la estructura y organización del sistema de archivos.",
        "Se han distinguido los atributos de un archivo y un directorio.",
        "Se han reconocido los permisos de archivos y directorios.",
        "Se ha constatado la utilidad de los sistemas transaccionales y sus repercusiones al seleccionar un sistema de archivos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido e identificado qué es y para qué sirve un Sistema Operativo.",
        "Se han analizando las funciones del sistema operativo.",
        "Se ha descrito la arquitectura del sistema operativo.",
        "Se ha verificado la idoneidad del hardware.",
        "Se ha seleccionado el sistema operativo.",
        "Se ha elaborado un plan de instalación.",
        "Se han configurado parámetros básicos de la instalación.",
        "Se ha configurado un gestor de arranque.",
        "Se han descrito las incidencias de la instalación.",
        "Se han respetado las normas de utilización del software (licencias).",
        "Se ha actualizado el sistema operativo.",
        "Identificar las características de instalación de diversos sistemas operativos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los interfaces de usuario según sus propiedades.",
        "Se han aplicado preferencias en la configuración del entorno personal.",
        "Se han gestionado los sistemas de archivos específicos.",
        "Se han aplicado métodos para la recuperación del sistema operativo.",
        "Se ha realizado la configuración para la actualización del sistema operativo.",
        "Se han realizado operaciones de instalación/desinstalación de utilidades.",
        "Se han utilizado los asistentes de configuración del sistema (acceso a redes, dispositivos, entre otros).",
        "Se han ejecutado operaciones para la automatización de tareas del sistema.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado perfiles de persona usuaria y grupo.",
        "Se han utilizado herramientas gráficas para describir la organización de los archivos del sistema.",
        "Se ha actuado sobre los procesos del usuario en función de las necesidades puntuales.",
        "Se ha actuado sobre los servicios del sistema en función de las necesidades puntuales.",
        "Se han aplicado criterios para la optimización de la memoria disponible.",
        "Se ha analizado la actividad del sistema a partir de las trazas generadas por el propio sistema.",
        "Se ha optimizado el funcionamiento de los dispositivos de almacenamiento.",
        "Se han reconocido y configurado los recursos compartibles del sistema. I) Se ha interpretado la información de configuración del sistema operativo.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha diferenciado entre máquina real y máquina virtual.",
        "Se han establecido las ventajas e inconvenientes de la utilización de máquinas virtuales.",
        "Se ha instalado el software libre y propietario para la creación de máquinas virtuales.",
        "Se han creado máquinas virtuales a partir de sistemas operativos libres y propietarios.",
        "Se han configurado máquinas virtuales.",
        "Se ha relacionado la máquina virtual con el sistema operativo anfitrión.",
        "Se han realizado pruebas de rendimiento del sistema.",
    ], start=1)],
}

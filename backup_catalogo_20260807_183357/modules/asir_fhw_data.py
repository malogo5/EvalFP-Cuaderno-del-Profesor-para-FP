"""EvalFP — Fundamentos de Hardware · 0371 · Administración de Sistemas Informáticos en Red
Decreto 200/2010, de 03/08/2010, currículo del ciclo de Administración de Sistemas Informáticos en Red en Castilla-La Mancha (DOCM, NID 2010/13389) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 116 h · 3 h/semana · 1º ASIR.
"""
MODULO = {
    "nombre":"Fundamentos de Hardware","codigo":"0371","abrev":"FH",
    "ciclo":"Administración de Sistemas Informáticos en Red","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":3,"total_horas":116,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 200/2010, de 03/08/2010, currículo del ciclo de Administración de Sistemas Informáticos en Red en Castilla-La Mancha (DOCM, NID 2010/13389) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Configura equipos microinformáticos","horas":27,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Instala software de propósito general","horas":30,"eval":2,"tags":""},
    {"id":"UT3","nombre":"Ejecuta procedimientos para recuperar el software base de un equipo","horas":21,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Implanta hardware específico de centros de proceso de datos (CPD)","horas":20,"eval":3,"tags":""},
    {"id":"UT5","nombre":"Cumple las normas de prevención de riesgos laborales y de protección…","horas":18,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":23,"nombre":"Configura equipos microinformáticos, componentes y periféricos, analizando sus características y relación con el conjunto."},
    {"id":"RA2","pond":25,"nombre":"Instala software de propósito general evaluando sus características y entornos de aplicación."},
    {"id":"RA3","pond":18,"nombre":"Ejecuta procedimientos para recuperar el software base de un equipo, analizándolos y utilizando imágenes almacenadas en memoria auxiliar."},
    {"id":"RA4","pond":18,"nombre":"Implanta hardware específico de centros de proceso de datos (CPD), analizando sus características y aplicaciones."},
    {"id":"RA5","pond":16,"nombre":"Cumple las normas de prevención de riesgos laborales y de protección ambiental, identificando los riesgos asociados, las medidas y equipos para prevenirlos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
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
        "Se han identificado y caracterizado los dispositivos que constituyen los bloques funcionales de un equipo microinformático.",
        "Se ha descrito el papel de los elementos físicos y lógicos que intervienen en el proceso de puesta en marcha de un equipo.",
        "Se ha analizado la arquitectura general de un equipo y los mecanismos de conexión entre dispositivos.",
        "Se han establecido los parámetros de configuración (hardware y software) de un equipo microinformático con las utilidades específicas.",
        "Se ha evaluado las prestaciones del equipo.",
        "Se han ejecutado utilidades de chequeo y diagnóstico.",
        "Se han identificado averías y sus causas.",
        "Se han clasificado los dispositivos periféricos y sus mecanismos de comunicación.",
        "Se han utilizado protocolos estándar de comunicación inalámbrica entre dispositivos.",
        "Se han instalado y configurado periféricos con sus drivers y utilidades específicas.",
        "Se ha configurado la BIOS de acuerdo a los requerimientos de la máquina.",
        "Se ha utilizado el software de configuración e interconexión de dispositivos móviles.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han catalogado los tipos de software según su licencia, distribución y propósito.",
        "Se han analizado las necesidades específicas de software asociadas al uso de sistemas informáticos en diferentes entornos productivos.",
        "Se han instalado y evaluado utilidades para la gestión de archivos, recuperación de datos, mantenimiento y optimización del sistema.",
        "Se han instalado y evaluado utilidades de seguridad básica.",
        "Se ha instalado y evaluado software ofimático y de utilidad general.",
        "Se ha consultado la documentación y las ayudas interactivas.",
        "Se ha verificado la repercusión de la eliminación, modificación y/o actualización de las utilidades instaladas en el sistema.",
        "Se han probado y comparado aplicaciones portables y no portables.",
        "Se han realizado inventarios del software instalado y las características de su licencia.",
        "Se han probado y comparado utilidades integradas en el sistema operativo y aplicaciones de utilidad específicas.",
        "Se ha monitorizado el funcionamiento del sistema para comprobar su buen funcionamiento.",
        "Se han documentado las tareas de instalación, mantenimiento y uso de software y hardware de un sistema informático.",
        "Se han instalado antivirus, antiespías y cortafuegos, y otras opciones de seguridad para reducir los accesos externos e internos a los equipos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los soportes de memoria auxiliar adecuados para el almacenaje y restauración de imágenes de software.",
        "Se ha reconocido la diferencia entre una instalación estándar y una preinstalación o imagen de software.",
        "Se han identificado y probado las distintas secuencias de arranque configurables en un equipo.",
        "Se han utilizado herramientas para el particionado de discos.",
        "Se han empleado distintas utilidades y soportes para realizar imágenes.",
        "Se han restaurado imágenes desde distintas ubicaciones.",
        "Se han utilizado herramientas de chequeo y reparación del arranque",
        "Se han utilizado herramientas para gestión de imágenes desde un servidor de imágenes de disco.",
        "Se han instalado aplicaciones ofimáticas para la gestión.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las diferencias entre las configuraciones hardware de tipo personal y empresarial.",
        "Se han analizado entornos que requieren implantar soluciones hardware específicas.",
        "Se han detallado componentes hardware específicos para soluciones empresariales.",
        "Se han analizado los requerimientos básicos de seguridad física, organización y condiciones ambientales de un CPD.",
        "Se han implantado sistemas de alimentación ininterrumpida y estabilizadores de tensión.",
        "Se han manipulado correctamente dispositivos hardware para almacenamiento y alimentación con conexión en caliente.",
        "Se han documentado procedimientos, incidencias y parámetros utilizados en la instalación y configuración de dispositivos hardware.",
        "Se han utilizado herramientas de inventariado, registrando las características de los dispositivos hardware.",
        "Se ha clasificado y organizado la documentación técnica, controladores, utilidades y accesorios del hardware.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos y el nivel de peligrosidad que suponen la manipulación de los materiales, herramientas, útiles, máquinas y medios de transporte.",
        "Se han operado las máquinas respetando las normas de seguridad.",
        "Se han identificado las causas más frecuentes de accidentes en la manipulación de materiales y herramientas, entre otras.",
        "Se han descrito los elementos de seguridad (protecciones, alarmas, y pasos de emergencia, entre otros) de las máquinas y los equipos de protección individual (calzado, protección ocular e indumentaria, entre otros) que se deben emplear en las distintas operaciones de montaje y mantenimiento.",
        "Se ha relacionado la manipulación de materiales, herramientas y máquinas con las medidas de seguridad y protección personal requeridos.",
        "Se han identificado las posibles fuentes de contaminación del entorno ambiental.",
        "Se han clasificado los residuos generados para su retirada selectiva.",
        "Se ha valorado el orden y la limpieza de instalaciones y equipos como primer factor de prevención de riesgos.",
    ], start=1)],
}

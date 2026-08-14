"""EvalFP — Implantación de Sistemas Operativos · 0369 · Administración de Sistemas Informáticos en Red (ASIR)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de curriculo del decreto de Castilla-La Mancha (DOCM).
UT, horas y asignacion de CE alineadas con el temario del modulo (revision de 12/08/2026).
Duración: 186 h · 6 h/semana · 1º ASIR.
"""
MODULO = {
    "nombre":"Implantación de Sistemas Operativos","codigo":"0369","abrev":"ISO",
    "ciclo":"Administración de Sistemas Informáticos en Red (ASIR)","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":6,"total_horas":186,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Instalación de software libre y propietario","horas":30,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Administración de software base","horas":25,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Administración y aseguramiento de la información","horas":22,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Administración de dominios","horas":30,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Administración de acceso al dominio","horas":25,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Supervisión del rendimiento del sistema","horas":22,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Directivas de seguridad y auditorías","horas":22,"eval":3,"tags":""},
    {"id":"UT8","nombre":"Resolución de incidencias y asistencia técnica","horas":10,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":13,"llave":True,"nombre":"Instala sistemas operativos, analizando sus características e interpretando la documentación técnica."},
    {"id":"RA2","pond":19,"llave":True,"nombre":"Configura el software de base, analizando las necesidades de explotación del sistema informático."},
    {"id":"RA3","pond":9,"nombre":"Asegura la información del sistema, describiendo los procedimientos y utilizando copias de seguridad y sistemas tolerantes a fallos."},
    {"id":"RA4","pond":16,"nombre":"Centraliza la información en servidores administrando estructuras de dominios y analizando sus ventajas."},
    {"id":"RA5","pond":15,"nombre":"Administra el acceso a dominios analizando y respetando requerimientos de seguridad."},
    {"id":"RA6","pond":12,"nombre":"Detecta problemas de rendimiento, monitorizando el sistema con las herramientas adecuadas y documentando el procedimiento."},
    {"id":"RA7","pond":11,"nombre":"Audita la utilización y acceso a recursos, identificando y respetando las necesidades de seguridad del sistema."},
    {"id":"RA8","pond":5,"nombre":"Implanta software específico con estructura cliente/servidor dando respuesta a los requisitos funcionales."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT1","RA2",["CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR10","CR11","CR12","CR13","CR14","CR16","CR17","CR19"]),
    ("UT2","RA7",["CR1"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA2",["CR9","CR15","CR18"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT7","RA7",["CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7","RA5",["CR8"]),
    ("UT8","RA8",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"],
            2:["RA4"],
            3:["RA5","RA6","RA7","RA8"]}
DUAL_RA = "RA8"
RA_INSTRUMENTOS = {
    "RA1":["examen","practica","empresa"],
    "RA2":["examen","practica","empresa"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica","empresa"],
    "RA5":["examen","practica","empresa"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
    "RA8":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos funcionales de un sistema informático.",
        "Se han identificado las características, funciones y arquitectura de un sistema operativo.",
        "Se han comparado diferentes sistemas operativos, sus versiones y licencias de uso, en función de sus requisitos, características y campos de aplicación.",
        "Se han realizado instalaciones de diferentes sistemas operativos.",
        "Se han previsto y aplicado técnicas de actualización y recuperación del sistema.",
        "Se han solucionado incidencias del sistema y del proceso de inicio.",
        "Se han utilizado herramientas para conocer el software instalado en el sistema y su origen.",
        "Se ha elaborado documentación de soporte relativa a las instalaciones efectuadas y a las incidencias detectadas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han planificado, creado y configurado cuentas de usuario, grupos, perfiles y políticas de contraseñas locales.",
        "Se ha asegurado el acceso al sistema mediante el uso de directivas de cuenta y directivas de contraseñas.",
        "Se ha actuado sobre los servicios y procesos en función de las necesidades del sistema.",
        "Se han instalado, configurado y verificado protocolos de red.",
        "Se han analizado y configurado los diferentes métodos de resolución de nombres.",
        "Se ha optimizado el uso de los sistemas operativos para sistemas portátiles.",
        "Se han utilizado máquinas virtuales para realizar tareas de configuración de sistemas operativos y analizar sus resultados.",
        "Se han documentado las tareas de configuración del software de base.",
        "Se ha creado cuotas de disco para los usuarios locales.",
        "Se han identificado, creado, modificado y eliminado adecuadamente claves del registro del sistema.",
        "Se han ejecutado procesos con identidad de otro usuario.",
        "Se ha instalado y configurado software que amplía el número de escritorios disponibles.",
        "Se han ocultado carpetas o protegido por contraseña en el sistema de archivos con software específico.",
        "Se han instalado y configurado suites de aplicaciones portables",
        "Se ha usado un editor hexadecimal para comprobar la estructura interna de archivos y de discos duros.",
        "Se han creado consolas de gestión (MMC) para gestionar apartados del SO.",
        "Se han creado y configurado perfiles de hardware para distintos usuarios.",
        "Se ha tomado posesión de carpetas de otros usuarios para poder acceder a ellas.",
        "Se han configurado las opciones de energía del equipo para adaptarlo a determinadas situaciones.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han comparado diversos sistemas de archivos y analizado sus diferencias y ventajas de implementación.",
        "Se ha descrito la estructura de directorios del sistema operativo.",
        "Se han identificado los directorios contenedores de los archivos de configuración del sistema (binarios, órdenes y librerías).",
        "Se han utilizado herramientas de administración de discos para crear particiones, unidades lógicas, volúmenes simples y volúmenes distribuidos.",
        "Se han implantado sistemas de almacenamiento redundante (RAID).",
        "Se han implementado y automatizado planes de copias de seguridad.",
        "Se han administrado cuotas de disco.",
        "Se han documentado las operaciones realizadas y los métodos a seguir para la recuperación ante desastres.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han implementado dominios.",
        "Se han administrado cuentas de usuario y cuentas de equipo.",
        "Se ha centralizado la información personal de los usuarios del dominio mediante el uso de perfiles móviles y carpetas personales.",
        "Se han creado y administrado grupos de seguridad.",
        "Se han creado plantillas que faciliten la administración de usuarios con características similares.",
        "Se han organizado los objetos del dominio para facilitar su administración.",
        "Se han utilizado máquinas virtuales para administrar dominios y verificar su funcionamiento.",
        "Se ha documentado la estructura del dominio y las tareas realizadas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han incorporado equipos al dominio.",
        "Se han previsto bloqueos de accesos no autorizados al dominio.",
        "Se ha administrado el acceso a recursos locales y recursos de red.",
        "Se han tenido en cuenta los requerimientos de seguridad.",
        "Se han implementado y verificado directivas de grupo.",
        "Se han asignado directivas de grupo.",
        "Se han documentado las tareas y las incidencias.",
        "Se han localizado directivas de grupo local usadas para algún motivo concreto",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los objetos monitorizables en un sistema informático.",
        "Se han identificado los tipos de sucesos.",
        "Se han utilizado herramientas de monitorización en tiempo real.",
        "Se ha monitorizado el rendimiento mediante registros de contador y de seguimiento del sistema.",
        "Se han planificado y configurado alertas de rendimiento.",
        "Se han interpretado los registros de rendimiento almacenados.",
        "Se ha analizado el sistema mediante técnicas de simulación para optimizar el rendimiento.",
        "Se ha elaborado documentación de soporte y de incidencias.",
        "Se han identificado los procesos ejecutados en el sistema, y se han relacionado con las aplicaciones a las que pertenecen.",
        "Se han identificado y eliminado posibles procesos malignos para el SO.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han administrado derechos de usuario y directivas de seguridad.",
        "Se han identificado los objetos y sucesos auditables.",
        "Se ha elaborado un plan de auditorias.",
        "Se han identificado las repercusiones de las auditorias en el rendimiento del sistema.",
        "Se han auditado sucesos correctos y erróneos.",
        "Se han auditado los intentos de acceso y los accesos a recursos del sistema.",
        "Se han gestionado los registros de auditoria.",
        "Se ha documentado el proceso de auditoria y sus resultados.",
        "Se han controlado las aplicaciones instaladas desde una fecha concreta.",
    ], start=1)],
    "RA8":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado software específico según la documentación técnica.",
        "Se han realizado instalaciones desatendidas.",
        "Se ha configurado y utilizado un servidor de actualizaciones.",
        "Se han planificado protocolos de actuación para resolver incidencias.",
        "Se han seguido los protocolos de actuación para resolver incidencias.",
        "Se ha dado asistencia técnica a través de la red documentando las incidencias.",
        "Se han elaborado guías visuales y manuales para instruir en el uso de sistemas operativos o aplicaciones.",
        "Se han documentado las tareas realizadas.",
        "Se ha accedido al equipo de forma remota desde otro, ya sea en la misma red o desde Internet.",
    ], start=1)],
}

# Criterios que se trabajan también durante la fase de formación en empresa.
# Se califican al 50 % en el centro y al 50 % con el informe de la tutoría de la
# empresa, conforme a los criterios de calificación del módulo. Los criterios no
# listados se evalúan íntegramente en el centro, y todos los criterios de un
# mismo RA ponderan por igual dentro de él.
DUAL_CES = {
    "RA1": ["CR4", "CR5", "CR6"],
    "RA2": ["CR1", "CR2", "CR3", "CR4"],
    "RA4": ["CR2", "CR3", "CR4", "CR6"],
    "RA5": ["CR1", "CR2", "CR3", "CR4"],
}

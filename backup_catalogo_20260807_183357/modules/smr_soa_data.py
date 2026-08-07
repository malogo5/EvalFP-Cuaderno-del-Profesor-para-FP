"""EvalFP — Sistemas Operativos en Red · 0224 · Sistemas Microinformáticos y Redes (SMR)
Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 223 h · 6 h/semana · 2º SMR.
"""
MODULO = {
    "nombre":"Sistemas Operativos en Red","codigo":"0224","abrev":"SOR",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":6,"total_horas":223,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Instalación de sistemas operativos en red","horas":40,"eval":1,"tags":"Windows Server · Ubuntu Server · Roles · Servicios"},
    {"id":"UT2","nombre":"Gestiona usuarios y grupos de sistemas operativos en red","horas":30,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Realiza tareas de gestión sobre dominios","horas":27,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Gestiona los recursos compartidos del sistema","horas":23,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Integración de sistemas Linux en dominios Windows","horas":20,"eval":2,"tags":"Samba · LDAP · Autenticación · Winbind"},
    {"id":"UT6","nombre":"Realiza tareas de integración de sistemas operativos libres y…","horas":30,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Realiza tareas de explotación de sistemas operativos en red a través…","horas":27,"eval":3,"tags":""},
    {"id":"UT8","nombre":"Gestiona los recursos del sistema a través de herramientas…","horas":26,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Instala sistemas operativos en red describiendo sus características e interpretando la documentación técnica."},
    {"id":"RA2","pond":13,"nombre":"Gestiona usuarios y grupos de sistemas operativos en red, interpretando especificaciones y aplicando herramientas del sistema."},
    {"id":"RA3","pond":12,"nombre":"Realiza tareas de gestión sobre dominios identificando necesidades y aplicando herramientas de administración de dominios."},
    {"id":"RA4","pond":11,"nombre":"Gestiona los recursos compartidos del sistema, interpretando especificaciones y determinando niveles de seguridad."},
    {"id":"RA5","pond":9,"nombre":"Realiza tareas de monitorización y uso del sistema operativo en red, describiendo las herramientas utilizadas e identificando las principales incidencias."},
    {"id":"RA6","pond":13,"nombre":"Realiza tareas de integración de sistemas operativos libres y propietarios, describiendo las ventajas de compartir recursos e instalando software específico."},
    {"id":"RA7","pond":12,"nombre":"Realiza tareas de explotación de sistemas operativos en red a través de diferentes servicios de terminales."},
    {"id":"RA8","pond":12,"nombre":"Gestiona los recursos del sistema a través de herramientas administrativas centralizadas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT8","RA8",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7","RA8"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
    "RA8":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha realizado el estudio de compatibilidad del sistema informático.",
        "Se han analizado las funciones del sistema operativo.",
        "Se ha verificado la idoneidad del hardware.",
        "Se ha comparado con la instalación y arquitectura con un sistema operativo monousuario.",
        "Se han diferenciado los modos de instalación.",
        "Se ha planificado y realizado el particionado del disco del servidor.",
        "Se han seleccionado y aplicado los sistemas de archivos.",
        "Se han seleccionado los componentes a instalar.",
        "Se han aplicado procedimientos para la automatización de instalaciones.",
        "Se han aplicado preferencias en la configuración del entorno personal.",
        "Se ha actualizado el sistema operativo en red.",
        "Se ha comprobado la conectividad del servidor con los equipos cliente.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado y gestionado cuentas de persona usuaria.",
        "Se han configurado y gestionado perfiles de persona usuaria.",
        "Se han configurado y gestionado cuentas de equipo.",
        "Se ha distinguido el propósito de los grupos, sus tipos y ámbitos.",
        "Se han configurado y gestionado grupos.",
        "Se ha gestionado la pertenencia de usuarios a grupos.",
        "Se han identificado las características de personas usuarias y grupos predeterminados y especiales.",
        "Se han planificado perfiles móviles de usuarios.",
        "Se han utilizado herramientas para la administración de persona usuarias y grupos, incluidas en el sistema operativo en red.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la función del servicio de directorio, sus elementos y nomenclatura.",
        "Se ha reconocido el concepto de dominio y sus funciones.",
        "Se han establecido relaciones de confianza entre dominios.",
        "Se ha realizado la instalación del servicio de directorio.",
        "Se ha realizado la configuración básica del servicio de directorio.",
        "Se han utilizado agrupaciones de elementos para la creación de modelos administrativos.",
        "Se ha analizado la estructura del servicio de directorio.",
        "Se han utilizado herramientas de administración de dominios.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la diferencia entre permiso y derecho.",
        "Se han identificado los recursos del sistema que se van a compartir y en qué condiciones.",
        "Se han asignado permisos a los recursos del sistema que se van a compartir.",
        "Se han compartido impresoras en red.",
        "Se ha utilizado el entorno gráfico para compartir recursos.",
        "Se han establecido niveles de seguridad para controlar el acceso del cliente a los recursos compartidos en red.",
        "Se ha trabajado en grupo para comprobar el acceso a los recursos compartidos del sistema.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características de los programas de monitorización.",
        "Se han identificado problemas de rendimiento en los dispositivos de almacenamiento.",
        "Se ha observado la actividad del sistema operativo en red a partir de las trazas generadas por el propio sistema.",
        "Se han realizado tareas de mantenimiento del software instalado en el sistema.",
        "Se han ejecutado operaciones para la automatización de tareas del sistema.",
        "Se ha interpretado la información de configuración del sistema operativo en red.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la necesidad de compartir recursos en red entre diferentes sistemas operativos.",
        "Se ha comprobado la conectividad de la red en un escenario heterogéneo.",
        "Se ha descrito la funcionalidad de los servicios que permiten compartir recursos en red.",
        "Se han instalado y configurado servicios para compartir recursos en red.",
        "Se ha accedido a sistemas de archivos en red desde equipos con diferentes sistemas operativos.",
        "Se ha accedido a impresoras desde equipos con diferentes sistemas operativos.",
        "Se ha trabajado en grupo.",
        "Se han establecido niveles de seguridad para controlar el acceso del usuario a los recursos compartidos en red.",
        "Se ha comprobado el funcionamiento de los servicios instalados.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la necesidad de utilizar los recursos del sistema operativo en red desde diferentes lugares de la red.",
        "Se ha identificado la necesidad de utilizar los recursos del sistema operativo en red entre diferentes usuarios.",
        "Se ha descrito la funcionalidad de los servicios que permiten explotar sistemas operativos en red remotamente.",
        "Se han instalado y configurado servicios para acceder a través de terminales al sistema operativo en red.",
        "Se ha accedido a sistemas operativos en red desde equipos con diferentes sistemas operativos.",
        "Se han establecido niveles de seguridad para controlar el acceso del usuario a los sistemas operativos en red.",
        "Se ha comprobado el funcionamiento de los servicios instalados.",
        "Se ha identificado las diferentes licencias de servicio de terminales en sistemas operativos propietario.",
    ], start=1)],
    "RA8":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características de las herramientas administrativas centralizadas.",
        "Se ha identificado la necesidad de utilización de herramientas que permitan gestionar recursos del sistema operativo en red de forma centralizada.",
        "Se ha identificado la necesidad de personalizar las herramientas administrativas atendiendo a los recursos que se pretenden gestionar.",
        "Se han identificado las principales funciones de las herramientas centralizadas.",
        "Se ha realizado la configuración básica de los principales recursos del sistema operativo en red a través de herramientas administrativas.",
        "Se han establecido niveles de seguridad para controlar el acceso del usuario las herramientas administrativas.",
        "Instala y configura herramientas administrativas centralizadas en sistemas operativos en red.",
        "Se ha identificado la necesidad de gestionar los recursos del sistema operativo en red mediante herramientas administrativas remotamente.",
    ], start=1)],
}

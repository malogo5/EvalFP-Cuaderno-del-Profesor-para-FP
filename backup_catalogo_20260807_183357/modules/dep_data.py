"""EvalFP — Despliegue de Aplicaciones Web · 0614 · Desarrollo de Aplicaciones Web (DAW)
Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 130 h · 3 h/semana · 2º DAW.
"""
MODULO = {
    "nombre":"Despliegue de Aplicaciones Web","codigo":"0614","abrev":"DEAW",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":3,"total_horas":130,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Implantación de arquitecturas web","horas":24,"eval":1,"tags":"DNS · Dominios · Hosting · VPS · CDN · HTTPS"},
    {"id":"UT2","nombre":"Administración de servidores web","horas":24,"eval":1,"tags":"Nginx · Apache · Virtualhost · SSL/TLS · WAF"},
    {"id":"UT3","nombre":"Implanta aplicaciones web en servidores de aplicaciones","horas":23,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Administra servidores de transferencia de archivos","horas":23,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Verifica la ejecución de aplicaciones Web comprobando los parámetros…","horas":18,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Elabora la documentación de la aplicación web","horas":18,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Implanta arquitecturas web analizando y aplicando criterios de funcionalidad."},
    {"id":"RA2","pond":18,"nombre":"Gestiona servidores web, evaluando y aplicando criterios de configuración para el acceso seguro a los servicios."},
    {"id":"RA3","pond":18,"nombre":"Implanta aplicaciones web en servidores de aplicaciones, evaluando y aplicando criterios de configuración para su funcionamiento seguro."},
    {"id":"RA4","pond":18,"nombre":"Administra servidores de transferencia de archivos, evaluando y aplicando criterios de configuración que garanticen la disponibilidad del servicio."},
    {"id":"RA5","pond":14,"nombre":"Verifica la ejecución de aplicaciones Web comprobando los parámetros de configuración de servicios de red."},
    {"id":"RA6","pond":14,"nombre":"Elabora la documentación de la aplicación web evaluando y seleccionando herramientas de generación de documentación y control de versiones."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado aspectos generales de arquitecturas web, sus características, ventajas e inconvenientes.",
        "Se han descrito los fundamentos y protocolos en los que se basa el funcionamiento de un servidor web.",
        "Se ha realizado la instalación y configuración básica de servidores web.",
        "Se han clasificado y descrito los principales servidores de aplicaciones.",
        "Se ha realizado la instalación y configuración básica de servidores de aplicaciones.",
        "Se han realizado pruebas de funcionamiento de los servidores web y de aplicaciones.",
        "Se ha analizado la estructura y recursos que componen una aplicación web.",
        "Se han descrito los requerimientos del proceso de implantación de una aplicación web.",
        "Se han documentado los procesos de instalación y configuración realizados sobre los servidores web y sobre las aplicaciones.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido los parámetros de administración más importantes del servidor web.",
        "Se ha ampliado la funcionalidad del servidor mediante la activación y configuración de módulos.",
        "Se han creado y configurado sitios virtuales.",
        "Se han configurado los mecanismos de autenticación y control de acceso del servidor.",
        "Se han obtenido e instalado certificados digitales.",
        "Se han establecido mecanismos para asegurar las comunicaciones entre el cliente y el servidor.",
        "Se han realizado pruebas de funcionamiento y rendimiento del servidor web.",
        "Se ha elaborado documentación relativa a la configuración, administración segura y recomendaciones de uso del servidor.",
        "Se han realizado los ajustes necesarios para la implantación de aplicaciones en el servidor web.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los componentes y el funcionamiento de los servicios proporcionados por el servidor de aplicaciones.",
        "Se han identificado los principales archivos de configuración y de bibliotecas compartidas.",
        "Se ha configurado el servidor de aplicaciones para cooperar con el servidor web.",
        "Se han configurado y activado los mecanismos de seguridad del servidor de aplicaciones.",
        "Se han configurado y utilizado los componentes web del servidor de aplicaciones.",
        "Se han realizado los ajustes necesarios para el despliegue de aplicaciones sobre el servidor.",
        "Se han realizado pruebas de funcionamiento y rendimiento de la aplicación web desplegada.",
        "Se ha elaborado documentación relativa a la administración y recomendaciones de uso del servidor de aplicaciones.",
        "Se ha elaborado documentación relativa al despliegue de aplicaciones sobre el servidor de aplicaciones.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado y configurado servidores de transferencia de archivos.",
        "Se han creado usuarios y grupos para el acceso remoto al servidor.",
        "Se ha configurado el acceso anónimo.",
        "Se ha comprobado el acceso al servidor, tanto en modo activo como en modo pasivo.",
        "Se han realizado pruebas con clientes en línea de comandos y clientes en modo gráfico.",
        "Se ha utilizado el protocolo seguro de transferencia de archivos.",
        "Se han configurado y utilizado servicios de transferencia de archivos integrados en servidores web.",
        "Se ha utilizado el navegador como cliente del servicio de transferencia de archivos.",
        "Se ha elaborado documentación relativa a la configuración y administración del servicio de transferencia de archivos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la estructura, nomenclatura y funcionalidad de los sistemas de nombres jerárquicos.",
        "Se han identificado las necesidades de configuración del servidor de nombres en función de los requerimientos de ejecución de las aplicaciones Web desplegadas.",
        "Se han identificado la función, elementos y estructuras lógicas del servicio de directorio.",
        "Se ha analizado la configuración y personalización del servicio de directorio.",
        "Se ha analizado la capacidad del servicio de directorio como mecanismo de autenticación centralizada de los usuarios en una red.",
        "Se han especificado los parámetros de configuración en el servicio de directorios adecuados para el proceso de validación de usuarios de la aplicación web.",
        "Se ha elaborado documentación relativa a las adaptaciones realizadas en los servicios de red.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado diferentes herramientas de generación de documentación.",
        "Se han documentado los componentes software utilizando los generadores específicos de las plataformas.",
        "Se han utilizado diferentes formatos para la documentación.",
        "Se han utilizado herramientas colaborativas para la elaboración y mantenimiento de la documentación.",
        "Se ha instalado, configurado y utilizado un sistema de control de versiones.",
        "Se ha garantizado la accesibilidad y seguridad de la documentación almacenada por el sistema de control de versiones.",
        "Se ha documentado la instalación, configuración y uso del sistema de control de versiones utilizado.",
    ], start=1)],
}

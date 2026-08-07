"""EvalFP — Sistemas Informáticos · 0483 · DAW
Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 163 h · 5 h/semana · 1º DAW.
"""
MODULO = {
    "nombre":"Sistemas Informáticos","codigo":"0483","abrev":"SI",
    "ciclo":"DAW","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"1º DAW","horas_sem":5,"total_horas":163,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Representación de la información","horas":22,"eval":1,"tags":"Binario · Hexadecimal · ASCII · Unicode · Aritmética binaria"},
    {"id":"UT2","nombre":"Software: sistemas operativos","horas":28,"eval":1,"tags":"Linux · Windows · Procesos · Memoria · Sistemas de ficheros"},
    {"id":"UT3","nombre":"Gestiona la información del sistema","horas":22,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Gestiona sistemas operativos","horas":25,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Redes de área local","horas":28,"eval":3,"tags":"TCP/IP · Ethernet · Switch · Router · Direccionamiento"},
    {"id":"UT6","nombre":"Virtualización y cloud","horas":19,"eval":3,"tags":"VirtualBox · VMware · Docker · AWS · Azure basics"},
    {"id":"UT7","nombre":"Elabora documentación","horas":19,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Evalúa sistemas informáticos identificando sus componentes y características."},
    {"id":"RA2","pond":17,"nombre":"Instala sistemas operativos planificando el proceso e interpretando documentación técnica."},
    {"id":"RA3","pond":13,"nombre":"Gestiona la información del sistema identificando las estructuras de almacenamiento y aplicando medidas para asegurar la integridad de los datos."},
    {"id":"RA4","pond":15,"nombre":"Gestiona sistemas operativos utilizando comandos y herramientas gráficas y evaluando las necesidades del sistema."},
    {"id":"RA5","pond":17,"nombre":"Interconecta sistemas en red configurando dispositivos y protocolos."},
    {"id":"RA6","pond":12,"nombre":"Opera sistemas en red gestionando sus recursos e identificando las restricciones de seguridad existentes."},
    {"id":"RA7","pond":12,"nombre":"Elabora documentación valorando y utilizando aplicaciones informáticas de propósito general."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6","RA7"]}
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
        "Se han reconocido los componentes físicos de un sistema informático y sus mecanismos de interconexión.",
        "Se ha verificado el proceso de puesta en marcha de un equipo.",
        "Se han clasificado, instalado y configurado diferentes tipos de dispositivos periféricos.",
        "Se han identificado los tipos de redes y sistemas de comunicación.",
        "Se han identificado los componentes de una red informática.",
        "Se han interpretado mapas físicos y lógicos de una red informática.",
        "Se han utilizado diferentes sistemas de numeración.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos funcionales de un sistema informático.",
        "Se han analizado las características, funciones y arquitectura de un sistema operativo.",
        "Se han comparado sistemas operativos en base a sus requisitos, características, campos de aplicación y licencias de uso.",
        "Se han instalado diferentes sistemas operativos.",
        "Se han aplicado técnicas de actualización y recuperación del sistema.",
        "Se han utilizado maquinas virtuales para instalar y probar sistemas operativos.",
        "Se han documentado los procesos realizados.",
        "Se ha configurado el arranque del sistema",
        "Se ha verificado el correcto funcionamiento de los controladores de dispositivos",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han comparado sistemas de archivos.",
        "Se ha identificado la estructura y función de los directorios del sistema operativo.",
        "Se han utilizado herramientas en entorno gráfico y comandos para localizar información en el sistema de archivos.",
        "Se han creado diferentes tipos de particiones y unidades lógicas.",
        "Se han realizado copias de seguridad y su posterior restauración",
        "Se han automatizado tareas.",
        "Se han instalado y evaluado utilidades relacionadas con la gestión de información.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado cuentas de usuarios locales y de grupos.",
        "Se ha asegurado el acceso al sistema mediante el uso de directivas de cuenta y directivas de contraseñas.",
        "Se han identificado, arrancado y detenido servicios y procesos.",
        "Se ha protegido el acceso a la información mediante el uso de permisos locales.",
        "Se han utilizado comandos para realizar las tareas básicas de configuración del sistema.",
        "Se ha monitorizado el sistema.",
        "Se han instalado y evaluado utilidades para el mantenimiento y optimización del sistema.",
        "Se han evaluado las necesidades del sistema informático en relación con el desarrollo de aplicaciones.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado el protocolo TCP/IP.",
        "Se han configurado redes de área local cableadas.",
        "Se han configurado redes de área local inalámbricas.",
        "Se han utilizado dispositivos de interconexión de redes.",
        "Se ha configurado el acceso a redes de área extensa.",
        "Se han gestionado puertos de comunicaciones.",
        "Se ha verificado el funcionamiento de la red mediante el uso de comandos y herramientas básicas.",
        "Se han aplicado protocolos seguros de comunicaciones.",
        "Se han configurado servidores para mejorar la gestión de las comunicaciones.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado el acceso a recursos locales y recursos de red.",
        "Se han identificado los derechos de usuario y directivas de seguridad.",
        "Se han explotado servidores de ficheros, servidores de impresión y servidores de aplicaciones.",
        "Se ha accedido a los servidores utilizando técnicas de conexión remota.",
        "Se ha evaluado la necesidad de proteger los recursos y el sistema.",
        "Se han instalado y evaluado utilidades de seguridad básica.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha clasificado software en función de su licencia y propósito.",
        "Se han analizado las necesidades específicas de software asociadas al uso de sistemas informáticos en diferentes entornos productivos.",
        "Se han realizado tareas de documentación mediante el uso de herramientas ofimáticas.",
        "Se han utilizado sistemas de correo y mensajería electrónica.",
        "Se han utilizado los servicios de transferencia de ficheros.",
        "Se han utilizado métodos de búsqueda de documentación técnica mediante el uso de servicios de Internet.",
    ], start=1)],
}

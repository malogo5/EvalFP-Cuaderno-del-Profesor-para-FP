"""EvalFP — Sistemas Informáticos (SI) · 0483 · 1º DAM/DAW · RD 450/2010 / RD 686/2010"""
MODULO = {
    "nombre":"Sistemas Informáticos","codigo":"0484","abrev":"SI",
    "ciclo":"DAM","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Representación de la información","horas":20,"eval":1,"tags":"Binario · Hexadecimal · ASCII · Unicode · Aritmética binaria"},
    {"id":"UT2","nombre":"Hardware: arquitectura y componentes","horas":30,"eval":1,"tags":"CPU · RAM · Almacenamiento · Buses · Periféricos · Ensamblado"},
    {"id":"UT3","nombre":"Software: sistemas operativos","horas":30,"eval":2,"tags":"Linux · Windows · Procesos · Memoria · Sistemas de ficheros"},
    {"id":"UT4","nombre":"Redes de área local","horas":30,"eval":2,"tags":"TCP/IP · Ethernet · Switch · Router · Direccionamiento"},
    {"id":"UT5","nombre":"Uso de sistemas operativos libres (Linux)","horas":30,"eval":3,"tags":"Bash · Gestión de usuarios · Permisos · Servicios · Shell scripting"},
    {"id":"UT6","nombre":"Virtualización y cloud","horas":20,"eval":3,"tags":"VirtualBox · VMware · Docker · AWS · Azure basics"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Evalúa sistemas informáticos identificando sus componentes y características."},
    {"id":"RA2","pond":20,"nombre":"Instala sistemas operativos planificando el proceso e interpretando documentación técnica."},
    {"id":"RA3","pond":20,"nombre":"Gestiona la información del sistema identificando las posibilidades derivadas de la configuración del sistema operativo."},
    {"id":"RA4","pond":20,"nombre":"Gestiona sistemas operativos utilizando métodos seguros de acceso, almacenamiento y transmisión de información."},
    {"id":"RA5","pond":15,"nombre":"Conecta sistemas en red configurando dispositivos y protocolos."},
    {"id":"RA6","pond":10,"nombre":"Opera sistemas en red gestionando sus recursos e identificando las restricciones de seguridad existentes."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA1",["CR6","CR7","CR8"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3","RA5"], 3:["RA4","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han reconocido los tipos de memoria del sistema y sus características."},
        {"id":"CR2","texto":"Se han identificado los dispositivos de almacenamiento."},
        {"id":"CR3","texto":"Se han diferenciado los tipos de aplicaciones software."},
        {"id":"CR4","texto":"Se ha representado la información en diferentes sistemas de numeración."},
        {"id":"CR5","texto":"Se han descrito las arquitecturas hardware más comunes."},
        {"id":"CR6","texto":"Se han identificado los componentes hardware de un equipo."},
        {"id":"CR7","texto":"Se han montado y desmontado equipos informáticos."},
        {"id":"CR8","texto":"Se han evaluado las prestaciones de los diferentes equipos."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han descrito los tipos de instalación de sistemas operativos."},
        {"id":"CR2","texto":"Se ha planificado y realizado la instalación de sistemas operativos libres y propietarios."},
        {"id":"CR3","texto":"Se han configurado parámetros de instalación."},
        {"id":"CR4","texto":"Se han instalado y configurado controladores de dispositivos."},
        {"id":"CR5","texto":"Se han documentado los procesos de instalación."},
        {"id":"CR6","texto":"Se han instalado entornos de desarrollo en el sistema operativo."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se ha operado con el sistema de ficheros del sistema operativo."},
        {"id":"CR2","texto":"Se han aplicado permisos y atributos al sistema de ficheros."},
        {"id":"CR3","texto":"Se han administrado los usuarios del sistema."},
        {"id":"CR4","texto":"Se han utilizado los procesadores de comandos del sistema."},
        {"id":"CR5","texto":"Se han creado scripts de administración básicos."},
        {"id":"CR6","texto":"Se han utilizado herramientas de gestión del sistema."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se ha configurado el acceso seguro al sistema."},
        {"id":"CR2","texto":"Se han realizado copias de seguridad."},
        {"id":"CR3","texto":"Se han restaurado sistemas a partir de copias de seguridad."},
        {"id":"CR4","texto":"Se han identificado mecanismos de cifrado de la información."},
        {"id":"CR5","texto":"Se han aplicado medidas de seguridad básicas."},
        {"id":"CR6","texto":"Se ha configurado el cortafuegos del sistema."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado los protocolos de comunicación en red."},
        {"id":"CR2","texto":"Se ha configurado la conexión de red del sistema."},
        {"id":"CR3","texto":"Se ha comprobado el funcionamiento de la red."},
        {"id":"CR4","texto":"Se han configurado los parámetros TCP/IP."},
        {"id":"CR5","texto":"Se han diagnosticado incidencias de red."},
        {"id":"CR6","texto":"Se han utilizado herramientas de diagnóstico de red."},
    ],
    "RA6":[
        {"id":"CR1","texto":"Se han descrito las características de los sistemas en red."},
        {"id":"CR2","texto":"Se ha configurado el acceso a recursos compartidos en red."},
        {"id":"CR3","texto":"Se han utilizado sistemas de virtualización."},
        {"id":"CR4","texto":"Se han identificado servicios básicos en la nube."},
        {"id":"CR5","texto":"Se han aplicado restricciones de seguridad en el acceso a la red."},
    ],
}

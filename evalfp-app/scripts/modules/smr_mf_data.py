"""EvalFP — Montaje y Mantenimiento de Equipos (MME) · 0221 · 1º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Montaje y Mantenimiento de Equipos","codigo":"0221","abrev":"MME",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":7,"total_horas":224,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Componentes hardware de un equipo microinformático","horas":35,"eval":1,"tags":"CPU · RAM · Placa base · Fuente de alimentación · Buses"},
    {"id":"UT2","nombre":"Montaje de equipos microinformáticos","horas":35,"eval":1,"tags":"Ensamblaje · Herramientas · ESD · POST · BIOS/UEFI"},
    {"id":"UT3","nombre":"Instalación de sistemas operativos","horas":35,"eval":1,"tags":"Windows · Linux · Particionado · Arranque dual · Drivers"},
    {"id":"UT4","nombre":"Dispositivos de almacenamiento","horas":28,"eval":2,"tags":"HDD · SSD · RAID · NAS · Sistemas de ficheros"},
    {"id":"UT5","nombre":"Periféricos e impresoras","horas":28,"eval":2,"tags":"USB · Bluetooth · Impresoras · Escáneres · Instalación"},
    {"id":"UT6","nombre":"Mantenimiento preventivo y correctivo","horas":28,"eval":2,"tags":"Limpieza · Diagnóstico · Herramientas · Piezas de repuesto"},
    {"id":"UT7","nombre":"Seguridad y prevención de riesgos laborales","horas":35,"eval":3,"tags":"PRL · EPI · Normativa · Reciclaje RAEE"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce los elementos funcionales de un equipo microinformático describiendo sus características y funciones."},
    {"id":"RA2","pond":20,"nombre":"Integra los componentes hardware constituyentes de un equipo microinformático ensamblándolos correctamente."},
    {"id":"RA3","pond":20,"nombre":"Instala sistemas operativos planificando el proceso e interpretando documentación técnica."},
    {"id":"RA4","pond":15,"nombre":"Instala y configura los dispositivos hardware de un equipo microinformático, describiendo sus características."},
    {"id":"RA5","pond":15,"nombre":"Mantiene equipos microinformáticos interpretando las averías y aplicando técnicas de diagnóstico y reparación."},
    {"id":"RA6","pond":15,"nombre":"Cumple las normas de prevención de riesgos laborales y de protección medioambiental."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA4",["CR6","CR7","CR8"]),
    ("UT6","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT7","RA6",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los componentes básicos de un equipo microinformático.",
        "Se han descrito las características técnicas de cada componente.",
        "Se ha relacionado cada componente con la función que realiza dentro del equipo.",
        "Se han identificado los tipos de memoria y sus características.",
        "Se han identificado los tipos de buses y sus velocidades.",
        "Se han reconocido los conectores y puertos del equipo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado la documentación técnica de los componentes.",
        "Se han montado ordenadores aplicando las técnicas y procedimientos establecidos.",
        "Se han utilizado las herramientas adecuadas para el montaje.",
        "Se han aplicado medidas para evitar daños por electricidad estática.",
        "Se ha verificado la correcta conexión de todos los componentes.",
        "Se ha configurado la BIOS/UEFI del equipo.",
        "Se han realizado pruebas de verificación del sistema ensamblado.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han planificado las particiones del sistema.",
        "Se ha instalado el sistema operativo siguiendo los pasos del proceso de instalación.",
        "Se han instalado los controladores de los dispositivos.",
        "Se han realizado actualizaciones del sistema operativo.",
        "Se han configurado los parámetros básicos del sistema operativo.",
        "Se ha documentado el proceso de instalación.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de dispositivos de almacenamiento.",
        "Se han instalado y configurado discos duros y unidades de estado sólido.",
        "Se han configurado sistemas RAID.",
        "Se han instalado y configurado periféricos.",
        "Se han instalado los controladores de impresoras y escáneres.",
        "Se han realizado pruebas de funcionamiento de los periféricos.",
        "Se han compartido periféricos en red.",
        "Se han documentado los dispositivos instalados.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los síntomas de avería más frecuentes.",
        "Se han utilizado herramientas de diagnóstico para localizar averías.",
        "Se han aplicado técnicas de mantenimiento preventivo.",
        "Se han sustituido componentes defectuosos.",
        "Se ha verificado el correcto funcionamiento tras la reparación.",
        "Se ha documentado el proceso de reparación.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos laborales asociados al montaje y mantenimiento de equipos.",
        "Se han aplicado las medidas de seguridad establecidas en la normativa.",
        "Se han utilizado los equipos de protección individual necesarios.",
        "Se han seguido los procedimientos de gestión de residuos electrónicos (RAEE).",
        "Se ha respetado la normativa medioambiental.",
    ], start=1)],
}

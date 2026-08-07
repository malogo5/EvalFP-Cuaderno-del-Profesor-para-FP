"""EvalFP — Redes Locales · 0225 · Sistemas Microinformáticos y Redes (SMR)
Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 169 h · 5 h/semana · 1º SMR.
"""
MODULO = {
    "nombre":"Redes Locales","codigo":"0225","abrev":"RL",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":5,"total_horas":169,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Reconoce la estructura de redes locales cableadas","horas":24,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Despliega el cableado de una red local","horas":29,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Interconecta equipos en redes locales cableadas","horas":26,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Instala equipos en red","horas":44,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Mantiene una red local","horas":23,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Cumple las normas de prevención de riesgos laborales y de protección…","horas":23,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Reconoce la estructura de redes locales cableadas analizando las características de entornos de aplicación y describiendo la funcionalidad de sus componentes."},
    {"id":"RA2","pond":17,"nombre":"Despliega el cableado de una red local interpretando especificaciones y aplicando técnicas de montaje."},
    {"id":"RA3","pond":15,"nombre":"Interconecta equipos en redes locales cableadas describiendo estándares de cableado y aplicando técnicas de montaje de conectores."},
    {"id":"RA4","pond":26,"nombre":"Instala equipos en red, describiendo sus prestaciones y aplicando técnicas de montaje."},
    {"id":"RA5","pond":14,"nombre":"Mantiene una red local interpretando recomendaciones de los fabricantes de hardware o software y estableciendo la relación entre disfunciones y sus causas."},
    {"id":"RA6","pond":14,"nombre":"Cumple las normas de prevención de riesgos laborales y de protección ambiental, identificando los riesgos asociados, las medidas y equipos para prevenirlos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13","CR14","CR15"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
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
        "Se han descrito los principios de funcionamiento de las redes locales.",
        "Se han identificado los distintos tipos de redes.",
        "Se han descrito los elementos de la red local y su función.",
        "Se han identificado y clasificado los medios de transmisión.",
        "Se ha reconocido el mapa físico de la red local.",
        "Se han utilizado aplicaciones para representar el mapa físico de la red local.",
        "Se han reconocido las distintas topologías de red.",
        "Se han identificado estructuras alternativas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido los principios funcionales de las redes locales.",
        "Se han identificado los distintos tipos de redes.",
        "Se han diferenciado los medios de transmisión.",
        "Se han reconocido los detalles del cableado de la instalación y su despliegue (categoría del cableado, espacios por los que discurre, soporte para las canalizaciones, entre otros).",
        "Se han seleccionado y montado las canalizaciones y tubos.",
        "Se han montado los armarios de comunicaciones y sus accesorios.",
        "Se han montado y conexionado las tomas de usuario y paneles de parcheo.",
        "Se han probado las líneas de comunicación entre las tomas de usuario y paneles de parcheo.",
        "Se han etiquetado los cables y tomas de usuario.",
        "Se ha trabajado con la calidad y seguridad requeridas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características que definen una red Ethernet.",
        "Se ha interpretado el plan de montaje lógico de la red.",
        "Se han montado los adaptadores de red en los equipos.",
        "Se han montado conectores sobre cables (cobre y fibra) de red.",
        "Se han montado los equipos de conmutación en los armarios de comunicaciones.",
        "Se han conectado los equipos de conmutación a los paneles de parcheo.",
        "Se ha verificado la conectividad de la instalación.",
        "Se ha trabajado con la calidad requerida.",
        "Se ha realizado la interconexión de redes distintas utilizando los dispositivos de interconexión adecuados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la estructura y características del modelo TCP/IP.",
        "Se ha reconocido la estructura y funciones de las direcciones MAC.",
        "Se ha reconocido la estructura y funciones de las direcciones IP.",
        "Se han segmentado redes LAN empleando distintas técnicas.",
        "Se ha configurado la conexión a internet.",
        "Se han identificado las características funcionales de las redes inalámbricas.",
        "Se han identificado los modos de funcionamiento de las redes inalámbricas.",
        "Se han instalado adaptadores y puntos de acceso inalámbrico.",
        "Se han configurado los modos de funcionamiento y los parámetros básicos.",
        "Se ha comprobado la conectividad entre diversos dispositivos y adaptadores inalámbricos.",
        "Se ha instalado el software correspondiente.",
        "Se han identificado los protocolos.",
        "Se han configurado los parámetros básicos.",
        "Se han aplicado mecanismos básicos de seguridad.",
        "Se han creado y configurado VLANS.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado incidencias y comportamientos anómalos.",
        "Se ha identificado si la disfunción es debida al hardware o al software.",
        "Se han monitorizado las señales visuales de los dispositivos de interconexión.",
        "Se han verificado los protocolos de comunicaciones.",
        "Se ha localizado la causa de la disfunción.",
        "Se ha restituido el funcionamiento sustituyendo equipos o elementos.",
        "Se han solucionado las disfunciones software.0 (configurando o reinstalando).",
        "Se ha elaborado un informe de incidencias.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos y el nivel de peligrosidad que suponen la manipulación de los materiales, herramientas, útiles, máquinas y medios de transporte.",
        "Se han operado las máquinas respetando las normas de seguridad.",
        "Se han identificado las causas más frecuentes de accidentes en la manipulación de materiales, herramientas, máquinas de corte y conformado, entre otras.",
        "Se han descrito los elementos de seguridad (protecciones, alarmas, pasos de emergencia, entre otros) de las máquinas y los equipos de protección individual (calzado, protección ocular, indumentaria, entre otros) que se deben emplear en las operaciones de montaje y mantenimiento.",
        "Se ha relacionado la manipulación de materiales, herramientas y máquinas con las medidas de seguridad y protección personal requeridos.",
        "Se han identificado las posibles fuentes de contaminación del entorno ambiental.",
        "Se han clasificado los residuos generados para su retirada selectiva.",
        "Se ha valorado el orden y la limpieza de instalaciones y equipos como primer factor de prevención de riesgos.",
    ], start=1)],
}

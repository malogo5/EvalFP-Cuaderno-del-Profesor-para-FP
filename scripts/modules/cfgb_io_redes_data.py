"""EvalFP — Instalación y Mantenimiento de Redes para Transmisión de Datos · 3016 · 
Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 80/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 338 h · 8 h/semana · 2º IO.
"""
MODULO = {
    "nombre":"Instalación y Mantenimiento de Redes para Transmisión de Datos","codigo":"3016","abrev":"IMRTD",
    "ciclo":"Informática de Oficina","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"2º IO","horas_sem":8,"total_horas":338,"anno":"2026-2027","eval_count":3,
    "horas_aula":200,  # el resto hasta 338 h es formación en empresa
    "decreto":"Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 80/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Elementos de redes de voz y datos","horas":27,"eval":1,"tags":"Cableado · Conectores · Canaletas · Armarios · Equipos activos · Topologías"},
    {"id":"UT2","nombre":"Monta canalizaciones","horas":37,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Despliega el cableado de una red de voz y datos","horas":32,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Instala elementos y sistemas de transmisión de voz y datos","horas":36,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Realiza operaciones básicas de configuración en redes locales cableadas","horas":32,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Prevención de riesgos laborales y medioambiente","horas":36,"eval":3,"tags":"EPI · Escaleras · Herramientas eléctricas · Residuos · Normativa"},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Selecciona los elementos que configuran las redes para la transmisión de voz y datos, describiendo sus principales características y funcionalidad."},
    {"id":"RA2","pond":18,"nombre":"Monta canalizaciones, soportes y armarios en redes de transmisión de voz y datos, identificando los elementos en el plano de la instalación y aplicando técnicas de montaje."},
    {"id":"RA3","pond":16,"nombre":"Despliega el cableado de una red de voz y datos analizando su trazado."},
    {"id":"RA4","pond":18,"nombre":"Instala elementos y sistemas de transmisión de voz y datos, reconociendo y aplicando las diferentes técnicas de montaje."},
    {"id":"RA5","pond":16,"nombre":"Realiza operaciones básicas de configuración en redes locales cableadas relacionándolas con sus aplicaciones."},
    {"id":"RA6","pond":18,"nombre":"Cumple las normas de prevención de riesgos laborales y de protección ambiental, identificando los riesgos asociados, las medidas y sistemas para prevenirlos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de instalaciones relacionados con las redes de transmisión de voz y datos.",
        "Se han identificado los elementos (canalizaciones, cableados, antenas, armarios, «racks» y cajas, entre otros) de una red de transmisión de datos.",
        "Se han clasificado los tipos de conductores (par de cobre, cable coaxial, fibra óptica, entre otros).",
        "Se ha determinado la tipología de las diferentes cajas (registros, armarios, «racks», cajas de superficie, de empotrar, entre otros).",
        "Se han descrito los tipos de fijaciones (tacos, bridas, tornillos, tuercas, grapas, entre otros) de canalizaciones y sistemas.",
        "Se han relacionado las fijaciones con el elemento a sujetar.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado las técnicas y herramientas empleadas para la instalación de canalizaciones y su adaptación.",
        "Se han tenido en cuenta las fases típicas para el montaje de un «rack».",
        "Se han identificado en un croquis del edificio o parte del edificio los lugares de ubicación de los elementos de la instalación.",
        "Se ha preparado la ubicación de cajas y canalizaciones.",
        "Se han preparado y/o mecanizado las canalizaciones y cajas.",
        "Se han montado los armarios («racks») interpretando el plano.",
        "Se han montado canalizaciones, cajas y tubos, entre otros, asegurando su fijación mecánica.",
        "Se han aplicado normas de seguridad en el uso de herramientas y sistemas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los medios de transmisión empleados para voz y datos.",
        "Se han reconocido los detalles del cableado de la instalación y su despliegue (categoría del cableado, espacios por los que discurre, soporte para las canalizaciones, entre otros).",
        "Se han utilizado los tipos de guías pasacables, indicando la forma óptima de sujetar cables y guía.",
        "Se ha cortado y etiquetado el cable.",
        "Se han montado los armarios de comunicaciones y sus accesorios.",
        "Se han montado y conexionado las tomas de usuario y paneles de parcheo.",
        "Se ha trabajado con la calidad y seguridad requeridas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han ensamblado los elementos que consten de varias piezas.",
        "Se han identificado el cableado en función de su etiquetado o colores.",
        "Se han colocado los sistemas o elementos (antenas, amplificadores, entre otros) en su lugar de ubicación.",
        "Se han seleccionado herramientas.",
        "Se han fijado los sistemas o elementos.",
        "Se ha conectado el cableado con los sistemas y elementos, asegurando un buen contacto.",
        "Se han colocado los embellecedores, tapas y elementos decorativos.",
        "Se han aplicado normas de seguridad, en el uso de herramientas y sistemas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los principios de funcionamiento de las redes locales.",
        "Se han identificado los distintos tipos de redes y sus estructuras alternativas.",
        "Se han reconocido los elementos de la red local identificándolos con su función.",
        "Se han descrito los medios de transmisión.",
        "Se ha interpretado el mapa físico de la red local.",
        "Se ha representado el mapa físico de la red local.",
        "Se han utilizado aplicaciones informáticas para representar el mapa físico de la red local.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos y el nivel de peligrosidad que suponen la manipulación de los materiales, herramientas, útiles, máquinas y medios de transporte.",
        "Se han operado las máquinas respetando las normas de seguridad.",
        "Se han identificado las causas más frecuentes de accidentes en la manipulación de materiales, herramientas, máquinas de corte y conformado, entre otras.",
        "Se han descrito los elementos de seguridad (protecciones, alarmas, pasos de emergencia, entre otros) de las máquinas y los sistemas de protección individual (calzado, protección ocular, indumentaria, entre otros) que se deben emplear en las operaciones de montaje y mantenimiento.",
        "Se ha relacionado la manipulación de materiales, herramientas y máquinas con las medidas de seguridad y protección personal requeridos.",
        "Se han identificado las posibles fuentes de contaminación del entorno ambiental.",
        "Se han clasificado los residuos generados para su retirada selectiva.",
        "Se ha valorado el orden y la limpieza de instalaciones y sistemas como primer factor de prevención de riesgos.",
    ], start=1)],
}

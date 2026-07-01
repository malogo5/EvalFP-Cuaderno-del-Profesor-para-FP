"""EvalFP — Montaje y Mantenimiento de Sistemas · 3029 · FPB Informática de Oficina
RD 356/2014, de 16 de mayo (BOE) · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])
"""
MODULO = {
    "nombre":"Montaje y Mantenimiento de Sistemas y Componentes Informáticos","codigo":"3029","abrev":"MONT",
    "ciclo":"","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"","horas_sem":9,"total_horas":288,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 356/2014, de 16 de mayo · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])",
}
UTS = [
    {"id":"UT1","nombre":"Componentes hardware y herramientas de montaje","horas":45,"eval":1,"tags":"CPU · RAM · Placa base · Almacenamiento · Fuente · Herramientas"},
    {"id":"UT2","nombre":"Ensamblaje de equipos microinformáticos","horas":50,"eval":1,"tags":"Montaje · Conexionado · Verificación · ESD · Caja"},
    {"id":"UT3","nombre":"Instalación de sistemas operativos monopuesto","horas":50,"eval":2,"tags":"Windows · Linux · Particionado · Controladores · Actualizaciones"},
    {"id":"UT4","nombre":"Comprobación y verificación del sistema","horas":48,"eval":2,"tags":"BIOS/UEFI · POST · Periféricos · Impresoras · Escáneres"},
    {"id":"UT5","nombre":"Mantenimiento básico de sistemas","horas":48,"eval":3,"tags":"Limpieza · Diagnóstico · Antivirus · Copias de seguridad · Consumibles"},
    {"id":"UT6","nombre":"Almacenamiento y conservación de equipos","horas":47,"eval":3,"tags":"Embalaje · Etiquetado · Almacén · Normativa · Inventario"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Selecciona los componentes y herramientas para la realización del montaje y mantenimiento de sistemas microinformáticos, describiendo sus características y relacionándolos con sus aplicaciones."},
    {"id":"RA2","pond":20,"nombre":"Ensambla los componentes hardware de un equipo microinformático, interpretando esquemas e instrucciones."},
    {"id":"RA3","pond":20,"nombre":"Instala sistemas operativos monopuesto identificando las fases del proceso e interpretando la documentación técnica."},
    {"id":"RA4","pond":15,"nombre":"Comprueba la funcionalidad de los sistemas, soportes y periféricos instalados ejecutando los procedimientos de verificación."},
    {"id":"RA5","pond":20,"nombre":"Realiza el mantenimiento básico de sistemas informáticos, soportes y periféricos, aplicando los procedimientos establecidos."},
    {"id":"RA6","pond":10,"nombre":"Almacena equipos, periféricos y consumibles, describiendo las condiciones de conservación y etiquetado."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de carcasas o cajas de ordenador, relacionándolos con los factores de forma de las placas base.",
        "Se han identificado los distintos tipos de placas base según su funcionalidad.",
        "Se han identificado los distintos tipos de memoria RAM, relacionando sus características con su rendimiento.",
        "Se han identificado los distintos tipos de microprocesadores, relacionando sus características técnicas con sus prestaciones.",
        "Se han identificado los distintos tipos de dispositivos de almacenamiento, relacionando sus características con sus prestaciones.",
        "Se han identificado los distintos tipos de tarjetas de expansión, relacionando sus características con su funcionalidad.",
        "Se han identificado los distintos tipos de periféricos de entrada, salida y entrada-salida, relacionándolos con sus características técnicas.",
        "Se han identificado los útiles y herramientas necesarios para el montaje y el mantenimiento de equipos microinformáticos.",
        "Se ha reconocido la normativa de prevención de riesgos laborales aplicable al montaje y mantenimiento de equipos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han interpretado esquemas y diagramas de conexionado de los componentes de un equipo microinformático.",
        "Se ha montado la placa base en la carcasa instalando el microprocesador, la memoria y las tarjetas de expansión.",
        "Se han conectado los distintos dispositivos de almacenamiento en los buses del sistema.",
        "Se han conectado los distintos cables de alimentación, de datos y los paneles delanteros de la carcasa.",
        "Se ha comprobado que todos los componentes se han instalado correctamente y están bien asentados.",
        "Se han observado las medidas de prevención de riesgos laborales en el proceso de ensamblaje.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los pasos del proceso de arranque de un equipo microinformático.",
        "Se han configurado los parámetros básicos de la BIOS/UEFI.",
        "Se ha realizado el particionado del disco duro, describiendo los tipos de particiones y sistemas de archivos.",
        "Se ha instalado el sistema operativo siguiendo las instrucciones del proceso.",
        "Se han instalado y actualizado los controladores de los dispositivos.",
        "Se han instalado las aplicaciones de usuario, siguiendo las instrucciones facilitadas.",
        "Se han realizado copias de seguridad e imágenes de respaldo del sistema operativo instalado.",
        "Se han aplicado actualizaciones y parches del sistema operativo.",
        "Se ha verificado el proceso de instalación comprobando la funcionalidad del sistema.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han ejecutado las utilidades de diagnóstico de los componentes del sistema.",
        "Se han verificado las prestaciones del equipo utilizando software de diagnóstico.",
        "Se ha comprobado el funcionamiento de los dispositivos de almacenamiento, comprobando su velocidad y capacidad.",
        "Se ha verificado el funcionamiento de los periféricos de entrada y salida.",
        "Se ha comprobado la funcionalidad de la impresora, realizando trabajos de impresión.",
        "Se ha verificado la conectividad a través de los puertos e interfaces de comunicaciones.",
        "Se han identificado y resuelto las incidencias básicas detectadas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha realizado la limpieza física de equipos informáticos, soportes y periféricos, usando los útiles y productos adecuados.",
        "Se han sustituido consumibles de periféricos —cartuchos, tóner, papel— siguiendo las instrucciones del fabricante.",
        "Se ha comprobado el estado de los sistemas de alimentación y la gestión de la energía del equipo.",
        "Se han instalado y actualizado aplicaciones de seguridad, ejecutando análisis del sistema.",
        "Se han realizado copias de seguridad de los archivos de usuario, verificando su integridad.",
        "Se han desfragmentado los discos duros y realizado comprobaciones del sistema de archivos.",
        "Se han detectado y resuelto las incidencias básicas de hardware y software, registrando el proceso.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos elementos de embalaje necesarios para el almacenamiento de equipos y periféricos.",
        "Se han identificado las condiciones de almacenamiento que deben cumplir los equipos, componentes y consumibles.",
        "Se ha verificado el estado de los equipos, componentes y consumibles antes de su almacenamiento.",
        "Se han embalado los equipos y componentes en función de sus características, siguiendo las instrucciones facilitadas.",
        "Se han etiquetado correctamente los equipos, componentes y consumibles almacenados.",
        "Se han organizado y clasificado los elementos en el almacén, siguiendo los criterios establecidos.",
        "Se ha gestionado el inventario de equipos, periféricos y consumibles, actualizando los registros.",
        "Se ha aplicado la normativa vigente en materia de protección del medio ambiente en la gestión de residuos.",
    ], start=1)],
}

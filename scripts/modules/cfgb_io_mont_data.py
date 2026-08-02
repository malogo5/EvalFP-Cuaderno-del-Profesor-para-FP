"""EvalFP — Montaje y Mantenimiento de Sistemas y Componentes Informáticos · 3029 · 
Decreto 80/2014, de 01/08/2014, currículo del ciclo de Formación Profesional Básica de Informática de Oficina en Castilla-La Mancha (DOCM, NID 2014/10283) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 335 h · 10 h/semana · 1º IO.
"""
MODULO = {
    "nombre":"Montaje y Mantenimiento de Sistemas y Componentes Informáticos","codigo":"3029","abrev":"MMSCI",
    "ciclo":"Informática de Oficina","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"1º IO","horas_sem":10,"total_horas":335,"anno":"2026-2027","eval_count":3,
    "horas_aula":300,  # el resto hasta 335 h es formación en empresa
    "decreto":"Decreto 80/2014, de 01/08/2014, currículo del ciclo de Formación Profesional Básica de Informática de Oficina en Castilla-La Mancha (DOCM, NID 2014/10283) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Selecciona los componentes y herramientas para la realización del…","horas":59,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Ensamblaje de equipos microinformáticos","horas":39,"eval":1,"tags":"Montaje · Conexionado · Verificación · ESD · Caja"},
    {"id":"UT3","nombre":"Instala sistemas operativos monopuesto","horas":59,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Comprueba la funcionalidad de los sistemas","horas":46,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Realiza el mantenimiento básico de sistemas informáticos","horas":45,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Almacenamiento y conservación de equipos","horas":52,"eval":3,"tags":"Embalaje · Etiquetado · Almacén · Normativa · Inventario"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Selecciona los componentes y herramientas para la realización del montaje y mantenimiento de sistemas microinformáticos, describiéndolos y relacionándolos con su función y aplicación en la instalación."},
    {"id":"RA2","pond":13,"nombre":"Ensambla los componentes hardware de un equipo microinformático, interpretando guías e instrucciones y aplicando técnicas de montaje."},
    {"id":"RA3","pond":20,"nombre":"Instala sistemas operativos monopuesto identificando las fases del proceso y relacionándolas con la funcionalidad de la instalación."},
    {"id":"RA4","pond":15,"nombre":"Comprueba la funcionalidad de los sistemas, soportes y periféricos instalados relacionando las intervenciones con los resultados a conseguir."},
    {"id":"RA5","pond":15,"nombre":"Realiza el mantenimiento básico de sistemas informáticos, soportes y periféricos, relacionando las intervenciones con los resultados que hay que conseguir."},
    {"id":"RA6","pond":17,"nombre":"Almacena equipos, periféricos y consumibles, describiendo las condiciones de conservación y etiquetado."},
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
        "Se han descrito las características de los elementos eléctricos y electrónicos utilizados en el montaje de sistemas.",
        "Se han descrito las operaciones y comprobaciones previas a la manipulación segura de componentes eléctricos y/o electrónicos.",
        "Se han identificado los dispositivos y herramientas necesarios en la manipulación segura de sistemas electrónicos.",
        "Se han seleccionado las herramientas necesarias para el procedimiento de montaje, sustitución o conexión de componentes hardware de un sistema microinformático.",
        "Se han identificado funcionalmente los componentes hardware para el ensamblado y/o mantenimiento de un equipo microinformático.",
        "Se han descrito las características técnicas de cada uno de los componentes hardware (internos y externos) utilizados en el montaje y/o mantenimiento de un equipo microinformático.",
        "Se han localizado los bloques funcionales en placas bases utilizadas en los sistemas microinformáticos.",
        "Se han identificado los tipos de puertos, bahías internas y cables de conexión (de datos y eléctricos, entre otros) existentes de un equipo microinformático.",
        "Se han seguido las instrucciones recibidas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha comprobado cada componente antes de su utilización, siguiendo las normas de seguridad establecidas.",
        "Se han interpretado las guías de instrucciones referentes a los procedimientos de integración o ensamblado, sustitución y conexión del componente hardware de un sistema microinformático.",
        "Se han reconocido en distintas placas base cada uno de los zócalos de conexión de microprocesadores y los disipadores, entre otros.",
        "Se han ensamblado los componentes hardware internos (memoria, procesador, tarjeta de video, pila, entre otros) en la placa base del sistema microinformático.",
        "Se ha fijado cada dispositivo o tarjeta en la ranura o bahía correspondiente, según guías detalladas de instalación.",
        "Se han conectado adecuadamente aquellos componentes hardware internos (disco duro, DVD, CD-ROM, entre otros) que necesiten cables de conexión para su integración en el sistema microinformático.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los pasos a seguir para la instalación o actualización.",
        "Se ha verificado la ausencia de errores durante el proceso de carga del sistema operativo.",
        "Se han utilizado las herramientas de control para la estructura de directorios y la gestión de permisos.",
        "Se han instalado actualizaciones y parches del sistema operativo según las instrucciones recibidas.",
        "Se han realizado copias de seguridad de los datos",
        "Se han anotado los posibles fallos producidos en la fase de arranque del equipo microinformático.",
        "Se han descrito las funciones de replicación física (“clonación”) de discos y particiones en sistemas microinformáticos.",
        "Se han utilizado herramientas software para la instalación de imágenes de discos o particiones señalando las restricciones de aplicación de las mismas.",
        "Se ha verificado la funcionalidad de la imagen instalada, teniendo en cuenta el tipo de “clonación” realizada.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha aplicado a cada componente hardware y periférico el procedimiento de testeo adecuado.",
        "Se ha verificado que el equipo microinformático realiza el procedimiento de encendido y de POST (Power On Self Test), identificando el origen de los problemas, en su caso.",
        "Se ha comprobado la funcionalidad de los soportes para almacenamiento de información.",
        "Se ha verificado la funcionalidad en la conexión entre componentes del equipo microinformático y con los periféricos.",
        "Se han utilizado herramientas de configuración, testeo y comprobación para verificar el funcionamiento del sistema.",
        "Se han utilizado las herramientas y guías de uso para comprobar el estado de los soportes y de la información contenida en los mismos.",
        "Se han registrado los resultados y las incidencias producidas en los procesos de comprobación.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha comprobado por medio de indicadores luminosos, que los periféricos conectados tienen alimentación eléctrica y las conexiones de datos.",
        "Se han descrito los elementos consumibles necesarios para ser utilizados en los periféricos de sistemas microinformáticos.",
        "Se han utilizado las guías técnicas detalladas para sustituir elementos consumibles.",
        "Se han descrito las características de los componentes, de los soportes y de los periféricos para conocer los aspectos que afecten a su mantenimiento.",
        "Se han utilizado las guías de los fabricantes para identificar los procedimientos de limpieza de componentes, soportes y periféricos.",
        "Se ha realizado la limpieza de componentes, soportes y periféricos respetando las disposiciones técnicas establecidas por el fabricante manteniendo su funcionalidad.",
        "Se han recogido los residuos y elementos desechables de manera adecuada para su eliminación o reciclaje.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las condiciones para manipular, transportar y almacenar componentes y periféricos de un sistema microinformático.",
        "Se han identificado los tipos de embalaje para el transporte y/o almacenaje de cada dispositivo, periférico y consumible.",
        "Se han utilizado las herramientas necesarias para realizar las tareas de etiquetado previas al embalaje y/o almacenamiento de sistemas, periféricos y consumibles.",
        "Se han utilizado los medios auxiliares adecuados a los elementos a transportar.",
        "Se han aplicado las normas de seguridad en la manipulación y el transporte de elementos y equipos.",
        "Se ha comprobado que los componentes recepcionados se corresponden con el albarán de entrega y que se encuentran en buen estado.",
        "Se han registrado las operaciones realizadas siguiendo los formatos establecidos.",
        "Se han recogido los elementos desechables para su eliminación o reciclaje.",
    ], start=1)],
}

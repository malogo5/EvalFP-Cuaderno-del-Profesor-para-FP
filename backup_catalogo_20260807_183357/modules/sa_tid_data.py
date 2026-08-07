"""EvalFP — Tratamiento informático de datos · 3001 · Servicios Administrativos
Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 268 h · 8 h/semana · 1º SA.
"""
MODULO = {
    "nombre":"Tratamiento informático de datos","codigo":"3001","abrev":"TID",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"1º SA","horas_sem":8,"total_horas":268,"anno":"2026-2027","eval_count":3,
    "horas_aula":240,  # el resto hasta 268 h es formación en empresa
    "decreto":"Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Equipos y materiales de oficina","horas":49,"eval":1,"tags":"Ordenador y periféricos · Consumibles · Ergonomía del puesto · Mantenimiento básico · Seguridad"},
    {"id":"UT2","nombre":"Grabación de datos y mecanografía","horas":71,"eval":1,"tags":"Teclado · Escritura al tacto · Velocidad y precisión · Corrección de errores · Postura"},
    {"id":"UT3","nombre":"Tratamiento de textos y datos","horas":49,"eval":2,"tags":"Procesador de textos · Hoja de cálculo · Formatos · Plantillas · Impresión"},
    {"id":"UT4","nombre":"Archivo, impresión y transmisión de documentos","horas":71,"eval":3,"tags":"Carpetas y nomenclatura · Copias de seguridad · Impresión · Correo electrónico · Confidencialidad"},
]
RAS = [
    {"id":"RA1","pond":21,"nombre":"Prepara los equipos y materiales necesarios para su trabajo, reconociendo sus principales funciones y aplicaciones y sus necesidades de mantenimiento."},
    {"id":"RA2","pond":29,"nombre":"Graba informáticamente datos, textos y otros documentos, valorando la rapidez y exactitud del proceso."},
    {"id":"RA3","pond":21,"nombre":"Trata textos y datos informáticamente, seleccionando las aplicaciones informáticas en función de la tarea."},
    {"id":"RA4","pond":29,"nombre":"Tramita documentación mediante su archivo, impresión y transmisión de los mismos, relacionado el tipo de documento con su ubicación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["practica"],
    "RA3":["practica","examen"],
    "RA4":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y clasificado los equipos informáticos y sus periféricos en función de su utilidad en el proceso ofimático.",
        "Se han identificado las distintas aplicaciones informáticas asociándolas a las diferentes labores que se van a realizar",
        "Se han comprobado las conexiones entre los distintos elementos informáticos, subsanando, en su caso, los errores observados.",
        "Se ha comprobado el funcionamiento de las aplicaciones informáticas a utilizar.",
        "Se ha realizado el mantenimiento de primer nivel de los diferentes equipos informáticos.",
        "Se han adoptado las medidas de seguridad necesarias para evitar los riesgos laborales derivados de la conexión y desconexión de los equipos.",
        "Se han situado los equipos teniendo en cuenta criterios de ergonomía y salud laboral.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han organizado los documentos que contienen los datos a grabar disponiéndolos de manera ordenada.",
        "Se ha comprobado que los datos y documentos no están previamente grabados con el fin de evitar duplicidades.",
        "Se han situado correctamente los dedos sobre el teclado.",
        "Se han identificado los distintos caracteres del teclado por el tacto y la posición de los dedos.",
        "Se ha manejado el teclado extendido con rapidez y exactitud, sin necesidad de desviar la mirada hacia las teclas.",
        "Se ha obtenido un grado de corrección elevado en la grabación de datos, con un máximo de un 5% de errores.",
        "Se ha utilizado correctamente el escáner para digitalizar imágenes y otros documentos.",
        "Se han corregido las anomalías y errores detectados en los resultados.",
        "Se ha mantenido la confidencialidad respecto de los datos y textos grabados.",
        "Se han seguido las normas ergonómicas y de higiene postural en la realización de las labores encomendadas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y seleccionado las aplicaciones a utilizar en cada uno de los ejercicios propuestos.",
        "Se han elaborado textos mediante herramientas de procesado de textos utilizando distintos formatos.",
        "Se han insertando imágenes, tablas y otros objetos en los textos.",
        "Se han guardado los documentos realizados en el lugar indicado, nombrándolos de manera que sean fácilmente identificables",
        "Se ha procedido a la grabación sistemática del trabajo realizado con objeto de que no se produzcan pérdidas fortuitas.",
        "Se ha identificado la periodicidad con que han de realizarse las copias de seguridad.",
        "Se han seguido las instrucciones recibidas y las normas ergonómicas y de higiene postural en la realización de las labores encomendadas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y clasificado los distintos documentos obtenidos de acuerdo con sus características y contenido.",
        "Se han identificado las posibles ubicaciones de archivo en soporte digital.",
        "Se han archivado digitalmente los documentos en el lugar correspondiente.",
        "Se ha accedido a documentos archivados previamente.",
        "Se ha comprobado el estado de los consumibles de impresión y se han repuesto en su caso.",
        "Se han seleccionado las opciones de impresión adecuadas a cada caso.",
        "Se han impreso los documentos correctamente.",
        "Se han utilizado las herramientas de mensajería informática interna, asegurando la recepción correcta de los documentos.",
        "Se ha demostrado responsabilidad y confidencialidad en el tratamiento de la información.",
        "Se han dejado los equipos informáticos en perfecto estado de uso al finalizar la jornada.",
    ], start=1)],
}

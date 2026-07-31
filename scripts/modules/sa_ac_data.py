"""EvalFP — Archivo y comunicación · 3004 · Servicios Administrativos
Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 144 h · 4 h/semana · 1º SA.
"""
MODULO = {
    "nombre":"Archivo y comunicación","codigo":"3004","abrev":"AC",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"1º SA","horas_sem":4,"total_horas":144,"anno":"2026-2027","eval_count":3,
    "horas_aula":120,  # el resto hasta 144 h es formación en empresa
    "decreto":"Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Reprografía de documentos","horas":31,"eval":1,"tags":"Fotocopiadora · Escáner · Encuadernación · Calidad · Mantenimiento y residuos"},
    {"id":"UT2","nombre":"Archivo convencional de documentos","horas":34,"eval":1,"tags":"Sistemas de clasificación · Ordenación · Expurgo · Custodia · Protección de datos"},
    {"id":"UT3","nombre":"Comunicación telefónica","horas":28,"eval":2,"tags":"Centralita · Recepción y emisión de llamadas · Notas de aviso · Cortesía · Vocabulario profesional"},
    {"id":"UT4","nombre":"Recepción de visitas y protocolo","horas":27,"eval":3,"tags":"Acogida · Identificación · Acompañamiento · Imagen personal · Normas de protocolo"},
]
RAS = [
    {"id":"RA1","pond":26,"nombre":"Realiza labores de reprografía de documentos valorando la calidad del resultado obtenido."},
    {"id":"RA2","pond":28,"nombre":"Archiva documentos convencionales utilizados en las operaciones comerciales y administrativas relacionando el tipo de documento con su ubicación o destino."},
    {"id":"RA3","pond":23,"nombre":"Se comunica telefónicamente, en el ámbito profesional, distinguiendo el origen y destino de llamadas y mensajes."},
    {"id":"RA4","pond":23,"nombre":"Recibe a personas externas a la organización reconociendo y aplicando normas de protocolo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica","examen"],
    "RA3":["practica"],
    "RA4":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los distintos equipos de reproducción y encuadernación.",
        "Se han relacionado las distintas modalidades de encuadernación básica.",
        "Se han reconocido las anomalías más frecuentes en los equipos de reproducción.",
        "Se han obtenido las copias necesarias de los documentos de trabajo en la calidad y cantidad requeridas.",
        "Se han cortado los documentos, adaptándolos al tamaño requerido, utilizando herramientas específicas.",
        "Se han observado las medidas de seguridad requeridas.",
        "Se han encuadernado documentos utilizando distintos métodos básicos (grapado, encanutado y otros).",
        "Se ha puesto especial cuidado en mantener el correcto orden de los documentos encuadernados.",
        "Se ha puesto interés en mantener en condiciones de funcionamiento óptimo los equipos utilizados.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de archivo.",
        "Se han descrito los diferentes criterios utilizados para archivar.",
        "Se han indicado los procesos básicos de archivo.",
        "Se han archivado documentos en soporte convencional siguiendo los criterios establecidos.",
        "Se ha accedido a documentos previamente archivados.",
        "Se ha distinguido la información fundamental que deben incluir los distintos documentos comerciales y administrativos básicos.",
        "Se han registrado los diferentes documentos administrativos básicos.",
        "Se ha comprobado la veracidad y la corrección de la información contenida en los distintos documentos.",
        "Se han elaborado los diferentes registros de manera limpia, ordenada y precisa.",
        "Se ha valorado el empleo de aplicaciones informáticas en la elaboración de los registros.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido diferentes equipos de telefonía.",
        "Se han valorado las distintas opciones de la centralita telefónica",
        "Se han atendido las llamadas telefónicas siguiendo los protocolos establecidos.",
        "Se han derivado las llamadas telefónicas hacia su destinatario final.",
        "Se ha informado, al destinatario final de la llamada, del origen de la misma.",
        "Se han cumplimentado notas de aviso telefónico de manera clara y precisa.",
        "Se ha demostrado interés en utilizar los distintos equipos telefónicos de una manera eficaz.",
        "Se ha mostrado cortesía y prontitud en la atención a las llamadas telefónicas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las distintas normas de cortesía aplicando el protocolo de saludo y despedida.",
        "Se ha empleado un lenguaje cortés y apropiado según la situación.",
        "Se han diferenciado costumbres características de otras culturas.",
        "Se ha informado previamente de datos relevantes de la persona esperada.",
        "Se ha identificado ante la visita y solicitado la información necesaria de ésta.",
        "Se ha notificado al destinatario de la visita la llegada de ésta y transmitido los datos identificativos.",
        "Se ha transmitido durante la comunicación la imagen corporativa de la organización.",
        "Se ha demostrado interés por ofrecer un trato personalizado.",
    ], start=1)],
}

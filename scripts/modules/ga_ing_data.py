"""EvalFP — Inglés profesional (GM) · 0156 · Gestión Administrativa
Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo IX del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 60 h · 2 h/semana · 1º GA.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Inglés profesional (GM)","codigo":"0156","abrev":"INGP",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"1º GA","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo IX del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Comprende información, de índole profesional y cotidiana,…","horas":12,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Comprende información profesional contenida en textos…","horas":12,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Produce mensajes orales sencillos, claros y estructurados,…","horas":17,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Redacta textos sencillos en lengua estándar, relacionando…","horas":13,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica actitudes y comportamientos profesionales en…","horas":6,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Comprende información, de índole profesional y cotidiana, contenida en discursos orales sencillos, emitidos en lengua estándar, descifrando el contenido global del mensaje, y relacionándolo con los recursos lingüísticos correspondientes."},
    {"id":"RA2","pond":19,"nombre":"Comprende información profesional contenida en textos escritos sencillos, analizando de forma comprensiva su contenido."},
    {"id":"RA3","pond":28,"nombre":"Produce mensajes orales sencillos, claros y estructurados, participando como agente activo en conversaciones profesionales."},
    {"id":"RA4","pond":22,"nombre":"Redacta textos sencillos en lengua estándar, relacionando las reglas gramaticales con la finalidad de los mismos."},
    {"id":"RA5","pond":11,"nombre":"Aplica actitudes y comportamientos profesionales en situaciones de comunicación, describiendo las relaciones típicas características del país de la lengua extranjera."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1", "RA2", "RA3"], 2:["RA4", "RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha situado el mensaje en su contexto por medio del análisis de sus características textuales y contextuales.",
        "Se ha identificado el hilo argumental de mensajes orales y determinado los roles que aparecen en los mismos.",
        "Se ha reconocido la finalidad del mensaje, ya se trate de un mensaje directo, telefónico o en cualquier otro medio auditivo.",
        "Se ha extraído información específica contenida en discursos orales, en lengua estándar, relacionados con la vida social, profesional o académica.",
        "Se han secuenciado los elementos constituyentes del mensaje.",
        "Se han identificado y resumido con claridad las ideas principales de un discurso sobre temas conocidos, transmitido por los medios de comunicación y emitido en lengua estándar.",
        "Se han reconocido las instrucciones orales y se han seguido las indicaciones siendo capaz de concluir si precisan de una respuesta verbal o de una no verbal.",
        "Se ha tomado conciencia de la importancia de comprender globalmente un mensaje, sin necesidad de entender todos y cada uno de los elementos del mismo.",
        "Se ha servido del análisis de la entonación y de los elementos visuales para identificar los diversos significados e intenciones comunicativas del emisor.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado los materiales de consulta y diccionarios técnicos. para la comprensión del texto.",
        "Se han leído de forma comprensiva textos claros en lengua estándar.",
        "Se ha relacionado el texto con el ámbito del sector a que se refiere.",
        "Se han reconocido las ideas principales de un texto escrito identificando la información relevante, sin necesidad de entender todos y cada uno de los elementos de dicho texto.",
        "Se ha identificado la terminología utilizada, así como las estructuras gramaticales y demás elementos característicos de cada tipología discursiva.",
        "Se han realizado traducciones de textos en lengua estándar utilizando material de apoyo en caso necesario.",
        "Se ha interpretado el mensaje recibido a través de soportes telemáticos o cualquier otro tipo de soporte.",
        "Se ha reconocido la finalidad de distintos textos escritos en cualquier soporte, en lengua estándar y relacionados con la actividad profesional.",
        "Se ha extraído información específica de textos de diferente naturaleza, relativos a su profesión y contenidos en distintos soportes.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado los registros más adecuados para la emisión del mensaje.",
        "Se ha comunicado utilizando fórmulas, nexos de unión, marcadores discursivos y estrategias de interacción acordes a la situación de comunicación.",
        "Se han descrito hechos breves e imprevistos relacionados con su profesión.",
        "Se ha utilizado correctamente la terminología de la profesión.",
        "Se han expresado sentimientos, ideas u opiniones.",
        "Se han enumerado las actividades propias de la tarea profesional.",
        "Se ha descrito y secuenciado un proceso de trabajo de su competencia.",
        "Se ha justificado la aceptación o no de propuestas realizadas haciendo uso de normas de cortesía y de modales apropiados.",
        "Se ha intercambiado, con relativa fluidez, información específica y detallada utilizando frases de estructura sencilla y diferentes soportes telemáticos.",
        "Se han realizado, de manera clara, presentaciones breves y preparadas sobre un tema dentro de su especialidad, haciendo uso de los protocolos adecuados.",
        "Se ha comunicado espontáneamente adoptando un nivel de formalidad adecuado a las circunstancias.",
        "Se han respondido preguntas relativas a su vida socio-profesional, incluidas las propias de una entrevista de trabajo.",
        "Se ha solicitado la reformulación del discurso o la aclaración de parte del mismo cuando se ha considerado necesario para una mejor comprensión.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado las estrategias, estructuras, vocabulario y convenciones más adecuadas para el tipo de texto que se va a crear (fax, nota, carta o correo electrónico, entre otros).",
        "Se han redactado textos breves relacionados con aspectos cotidianos y/o profesionales.",
        "Se ha organizado la información de manera coherente y cohesionada.",
        "Se han realizado resúmenes de textos relacionados con su entorno profesional, identificando las ideas principales de los mismos.",
        "Se ha cumplimentado documentación específica de su campo profesional, aplicando las fórmulas establecidas y el vocabulario específico.",
        "Se ha cumplimentado un texto dado con apoyos visuales y claves lingüísticas aportadas.",
        "Se han utilizado las fórmulas de cortesía propias del documento que se va a elaborar.",
        "Se ha escrito correspondencia formal básica en formato físico o digital destinada principalmente a pedir información, solicitar un servicio o llevar a cabo una reclamación u otra gestión sencilla, siempre atendiendo a las convenciones de la tipología textual.",
        "Se han tomado notas, y mensajes, con información sencilla sobre aspectos propios de su labor profesional.",
        "Se ha solicitado, de forma escrita, información referente a aspectos relacionados con su campo profesional (página web y correo electrónico, entre otros).",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los rasgos más significativos de las costumbres y usos de la comunidad donde se habla la lengua extranjera.",
        "Se han descrito los protocolos y normas de relación social propios del país.",
        "Se han identificado los valores y creencias propios de la comunidad donde se habla la lengua extranjera.",
        "Se han identificado los aspectos socio-profesionales propios del sector, en cualquier tipo de texto.",
        "Se han aplicado los protocolos y normas de relación social propios del país de la lengua extranjera.",
    ], start=1)],
}

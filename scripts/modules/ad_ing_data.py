"""EvalFP — Inglés profesional (GS) · 0179 · Asistencia a la Dirección
Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo X del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 60 h · 2 h/semana · 1º AD.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Inglés profesional (GS)","codigo":"0179","abrev":"INGP",
    "ciclo":"Asistencia a la Dirección","ciclo_clave":"AD","ciclo_nivel":"CFGS",
    "curso":"1º AD","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo X del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Comprende información, de índole profesional, académica y…","horas":11,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Comprende mensajes escritos, de naturaleza profesional,…","horas":14,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Produce mensajes orales claros y bien estructurados,…","horas":15,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Redacta documentos e informes, propios del sector o de la…","horas":11,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica actitudes y comportamientos profesionales en…","horas":9,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":19,"nombre":"Comprende información, de índole profesional, académica y cotidiana, contenida en todo tipo de discursos orales, emitidos por cualquier medio de comunicación en lengua estándar, interpretando con precisión el contenido del mensaje."},
    {"id":"RA2","pond":23,"nombre":"Comprende mensajes escritos, de naturaleza profesional, académica y cotidiana, de relativa dificultad, analizando de forma comprensiva su contenido."},
    {"id":"RA3","pond":25,"nombre":"Produce mensajes orales claros y bien estructurados, analizando el contenido de la situación y adaptándose al registro lingüístico del interlocutor."},
    {"id":"RA4","pond":19,"nombre":"Redacta documentos e informes, propios del sector o de la vida académica y cotidiana, relacionando los recursos lingüísticos con el propósito de los mismos."},
    {"id":"RA5","pond":14,"nombre":"Aplica actitudes y comportamientos profesionales en situaciones de comunicación, describiendo las relaciones típicas características del país de la lengua extranjera."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
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
        "Se ha identificado la idea principal de mensajes en lengua estándar relacionados con la vida social, profesional o académica.",
        "Se ha reconocido la finalidad de mensajes directos o emitidos en cualquier soporte en lengua estándar.",
        "Se ha extraído información específica contenida en distintos discursos orales en lengua estándar, relacionada con la vida social, profesional o académica.",
        "Se ha identificado el punto de vista y la actitud del hablante.",
        "Se ha identificado el hilo argumental de mensajes orales y determinado los roles que aparecen en dichos mensajes.",
        "Se han comprendido adecuadamente mensajes en lengua estándar en ambientes con contaminación acústica.",
        "Se han extraído las ideas principales de conferencias, charlas e informes, y otras formas de presentación académica y profesional, lingüísticamente complejas.",
        "Se ha tomado conciencia de la importancia de comprender globalmente un mensaje sin entender todos y cada uno de los elementos del mismo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la idea principal de textos específicos de su ámbito social, profesional o académico.",
        "Se ha reconocido la finalidad de distintos textos escritos en cualquier soporte, en lengua estándar y relacionados con la actividad profesional.",
        "Se ha extraído información específica de textos, de diferente naturaleza, relativos a su profesión, y contenidos en distintos soportes.",
        "Se ha tomado conciencia de la importancia de comprender globalmente un texto sin entender todos y cada uno de los elementos del mismo.",
        "Se han leído y comprendido, de manera autónoma, textos relacionados con el sector con la velocidad y estilo de lectura propia del nivel competencial.",
        "Se ha interpretado la correspondencia relativa a su especialidad, captando fácilmente el significado esencial.",
        "Se han interpretado textos extensos, y de cierta complejidad, relacionados o no con su especialidad, pudiendo realizar varias lecturas del mismo.",
        "Se ha identificado con rapidez el contenido y la importancia de noticias, artículos e informes sobre una amplia serie de temas profesionales.",
        "Se han interpretado instrucciones, con distintos niveles de dificultad, y mensajes técnicos recibidos a través de soportes digitales.",
        "Se han traducido textos de cierta complejidad, utilizando material de apoyo en caso necesario.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han emitido mensajes generales propios de sector y de la vida cotidiana, utilizando nexos y estrategias de interacción.",
        "Se ha intercambiado con fluidez información específica y detallada utilizando estructuras de una complejidad acorde al nivel competencial.",
        "Se han seleccionado y aplicado los registros adecuados para la emisión del mensaje, así como protocolos y normas de relación social propios del país.",
        "Se han realizado presentaciones, bien estructuradas, sobre temas de su ámbito profesional, haciendo uso de los protocolos establecidos.",
        "Se ha utilizado correctamente la terminología de la profesión.",
        "Se ha descrito y secuenciado oralmente un proceso de trabajo de su competencia.",
        "Se ha solicitado la reformulación del discurso o parte del mismo cuando se ha considerado necesario.",
        "Se ha interaccionado espontáneamente, adoptando un nivel de formalidad adecuado a las circunstancias.",
        "Se ha expresado con fluidez, precisión y eficacia sobre una amplia serie de temas generales, académicos, profesionales o de ocio, marcando con claridad la relación entre las ideas.",
        "Se han expresado y defendido puntos de vista con claridad, proporcionando explicaciones y argumentos adecuados.",
        "Se ha respondido a preguntas relativas a su vida socio-profesional, incluidas las propias de una entrevista de trabajo.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han escrito textos claros y detallados sobre una variedad de temas relacionados con su profesión, sintetizando y evaluando información y argumentos procedentes de varias fuentes.",
        "Se ha cumplimentado documentación específica de su campo profesional, utilizando vocabulario específico y protocolos y normas de relación social propios del país.",
        "Se ha organizado la información con corrección, precisión, con cohesión y coherencia, solicitando y/o facilitando información de tipo general o detallada.",
        "Se han cumplimentado textos mediante apoyos visuales y claves lingüísticas.",
        "Se han elaborado informes, destacando los aspectos significativos y ofreciendo detalles relevantes que sirvan de apoyo.",
        "Se han escrito cartas, formales e informales, empleando las fórmulas de cortesía establecidas y el vocabulario específico para la elaboración de las mismas.",
        "Se han resumido diferentes tipos de documentos escritos, utilizando sus propios recursos lingüísticos.",
        "Se han utilizado las fórmulas de cortesía propias del documento que se va a elaborar.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los rasgos más significativos de las costumbres y usos de la comunidad donde se habla la lengua extranjera.",
        "Se han descrito los protocolos y normas de relación social propios del país.",
        "Se han identificado los valores y creencias propios de la comunidad donde se habla la lengua extranjera.",
        "Se ha identificado los aspectos socio-profesionales propios del sector, en cualquier tipo de texto.",
        "Se han aplicado los protocolos y normas de relación social propios del país de la lengua extranjera.",
        "Se han reconocido los marcadores lingüísticos de la procedencia regional.",
    ], start=1)],
}

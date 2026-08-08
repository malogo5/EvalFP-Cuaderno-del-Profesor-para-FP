"""EvalFP — Atención al cliente · 3005 · Servicios Administrativos
Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 83/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 117 h · 3 h/semana · 2º SA.
"""
MODULO = {
    "nombre":"Atención al cliente","codigo":"3005","abrev":"ATC",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"2º SA","horas_sem":3,"total_horas":117,"anno":"2026-2027","eval_count":3,
    "horas_aula":75,  # el resto hasta 117 h es formación en empresa
    "decreto":"Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 83/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Comunicación con la clientela","horas":22,"eval":1,"tags":"Proceso de comunicación · Escucha activa · Comunicación no verbal · Barreras"},
    {"id":"UT2","nombre":"Información del servicio","horas":19,"eval":2,"tags":"Argumentario · Ventajas del servicio · Precio y condiciones · Asesoramiento"},
    {"id":"UT3","nombre":"Seguimiento y cierre del servicio","horas":19,"eval":2,"tags":"Justificación de las operaciones · Documentación de entrega · Encuestas de satisfacción"},
    {"id":"UT4","nombre":"Reclamaciones y quejas","horas":15,"eval":3,"tags":"Protocolo de actuación · Hoja de reclamaciones · Derivación · Registro y seguimiento"},
]
RAS = [
    {"id":"RA1","pond":29,"nombre":"Atiende a posibles clientes, reconociendo las diferentes técnicas de comunicación."},
    {"id":"RA2","pond":26,"nombre":"Comunica al posible cliente las diferentes posibilidades del servicio, justificándolas desde el punto de vista técnico."},
    {"id":"RA3","pond":26,"nombre":"Informa al probable cliente del servicio realizado, justificando las operaciones ejecutadas."},
    {"id":"RA4","pond":19,"nombre":"Atiende reclamaciones de posibles clientes, reconociendo el protocolo de actuación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado el comportamiento del posible cliente.",
        "Se han adaptado adecuadamente la actitud y discurso a la situación de la que se parte.",
        "Se ha obtenido la información necesaria del posible cliente.",
        "Se ha favorecido la comunicación con el empleo de las técnicas y actitudes apropiadas al desarrollo de la misma.",
        "Se ha mantenido una conversación, utilizando las fórmulas, léxico comercial y nexos de comunicación (pedir aclaraciones, solicitar información, pedir a alguien que repita y otros).",
        "Se ha dado respuesta a una pregunta de fácil solución, utilizando el léxico comercial adecuado.",
        "Se ha expresado un tema prefijado de forma oral delante de un grupo o en una relación de comunicación en la que intervienen dos interlocutores.",
        "Se ha mantenido una actitud conciliadora y sensible a los demás, demostrando cordialidad y amabilidad en el trato.",
        "Se ha trasmitido información con claridad, de manera ordenada, estructura clara y precisa.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado las diferentes tipologías de público.",
        "Se han diferenciado clientes de proveedores, y éstos del público en general.",
        "Se ha reconocido la terminología básica de comunicación comercial.",
        "Se ha diferenciado entre información y publicidad.",
        "Se han adecuado las respuestas en función de las preguntas del público.",
        "Se ha informado al cliente de las características del servicio, especialmente de las calidades esperables.",
        "Se ha asesorado al cliente sobre la opción más recomendable, cuando existen varias posibilidades, informándole de las características y acabados previsibles de cada una de ellas.",
        "Se ha solicitado al cliente que comunique la elección de la opción elegida.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha hecho entrega al cliente de los artículos procesados, informando de los servicios realizados en los artículos.",
        "Se han transmitido al cliente, de modo oportuno, las operaciones a llevar a cabo en los artículos entregados y los tiempos previstos para ello.",
        "Se han identificado los documentos de entrega asociados al servicio o producto.",
        "Se ha recogido la conformidad del cliente con el acabado obtenido, tomando nota, en caso contrario, de sus objeciones, de modo adecuado.",
        "Se ha valorado la pulcritud y corrección, tanto en el vestir como en la imagen corporal, elementos clave en la atención al cliente.",
        "Se ha mantenido en todo momento el respeto hacia el cliente",
        "Se ha intentado la fidelización del cliente con el buen resultado del trabajo.",
        "Se ha definido periodo de garantía y las obligaciones legales aparejadas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han ofrecido alternativas al cliente ante reclamaciones fácilmente subsanables, exponiendo claramente los tiempos y condiciones de las operaciones a realizar, así como del nivel de probabilidad de modificación esperable.",
        "Se han reconocido los aspectos principales en los que incide la legislación vigente, en relación con las reclamaciones.",
        "Se ha suministrado la información y documentación necesaria al cliente para la presentación de una reclamación escrita, si éste fuera el caso.",
        "Se han recogido los formularios presentados por el cliente para la realización de una reclamación.",
        "Se ha cumplimentado una hoja de reclamación",
        "Se ha compartido información con el equipo de trabajo.",
    ], start=1)],
}

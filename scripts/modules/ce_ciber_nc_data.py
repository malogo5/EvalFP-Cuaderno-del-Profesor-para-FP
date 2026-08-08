"""EvalFP — Normativa de Ciberseguridad · 5026 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 55 h · 2 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Normativa de Ciberseguridad","codigo":"5026","abrev":"NC",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":2,"total_horas":55,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Identifica los puntos principales de aplicación para asegurar el…","horas":11,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Diseña sistemas de cumplimiento normativo","horas":9,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Relaciona la normativa relevante para el cumplimiento de la…","horas":9,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Aplica la legislación nacional de protección de datos de carácter…","horas":15,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Recopila y aplica la normativa vigente de ciberseguridad de ámbito…","horas":11,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Identifica los puntos principales de aplicación para asegurar el cumplimiento normativo reconociendo funciones y responsabilidades."},
    {"id":"RA2","pond":16,"nombre":"Diseña sistemas de cumplimiento normativo seleccionando la legislación y jurisprudencia de aplicación."},
    {"id":"RA3","pond":16,"nombre":"Relaciona la normativa relevante para el cumplimiento de la responsabilidad penal de las organizaciones y personas jurídicas con los procedimientos establecidos, recopilando y aplicando las normas vigentes."},
    {"id":"RA4","pond":28,"nombre":"Aplica la legislación nacional de protección de datos de carácter personal, relacionando los procedimientos establecidos con las leyes vigentes y con la jurisprudencia existente sobre la materia."},
    {"id":"RA5","pond":20,"nombre":"Recopila y aplica la normativa vigente de ciberseguridad de ámbito nacional e internacional, actualizando los procedimientos establecidos de acuerdo con las leyes y con la jurisprudencia existente sobre la materia."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["practica","examen"],
    "RA3":["practica","examen"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las bases del cumplimiento normativo a tener en cuenta en las organizaciones.",
        "Se han descrito y aplicado los principios de un buen gobierno y su relación con la ética profesional.",
        "Se han definido las políticas y procedimientos, así como la estructura organizativa que establezca la cultura del cumplimiento normativo dentro de las organizaciones.",
        "Se han descrito las funciones o competencias del responsable del cumplimiento normativo dentro de las organizaciones.",
        "Se han establecido las relaciones con terceros para un correcto cumplimiento normativo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han recogido las principales normativas que afectan a los diferentes tipos de organizaciones.",
        "Se han establecido las recomendaciones válidas para diferentes tipos de organizaciones de acuerdo con la normativa vigente (ISO 19.600 entre otras).",
        "Se han realizado análisis y evaluaciones de los riesgos de diferentes tipos de organizaciones de acuerdo con la normativa vigente (ISO 31.000 entre otras).",
        "Se ha documentado el sistema de cumplimiento normativo diseñado.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos penales aplicables a diferentes organizaciones.",
        "Se han implantado las medidas necesarias para eliminar o minimizar los riesgos identificados.",
        "Se ha establecido un sistema de gestión de cumplimiento normativo penal de acuerdo con la legislación y normativa vigente (Código Penal y UNE 19.601, entre otros).",
        "Se han determinado los principios básicos dentro de las organizaciones para combatir el soborno y promover una cultura empresarial ética de acuerdo con la legislación y normativa vigente (ISO 37.001 entre otros).",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las fuentes del derecho de acuerdo con el ordenamiento jurídico en materia de protección de datos de carácter personal.",
        "Se han aplicado los principios relacionados con la protección de datos de carácter personal tanto a nivel nacional como internacional.",
        "Se han establecido los requisitos necesarios para afrontar la privacidad desde las bases del diseño.",
        "Se han configurado las herramientas corporativas contemplando el cumplimiento normativo por defecto.",
        "Se ha realizado un análisis de riesgos para el tratamiento de los derechos a la protección de datos.",
        "Se han implantado las medidas necesarias para eliminar o minimizar los riesgos identificados en la protección de datos.",
        "Se han descrito las funciones o competencias del delegado de protección de datos dentro de las organizaciones.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido el plan de revisiones de la normativa, jurisprudencia, notificaciones, etc. jurídicas que puedan afectar a la organización.",
        "Se ha detectado nueva normativa consultando las bases de datos jurídicas siguiendo el plan de revisiones establecido.",
        "Se ha analizado la nueva normativa para determinar si aplica a la actividad de la organización.",
        "Se ha incluido en el plan de revisiones las modificaciones necesarias, sobre la nueva normativa aplicable a la organización, para un correcto cumplimiento normativo.",
        "Se han determinado e implementado los controles necesarios para garantizar el correcto cumplimiento normativo de las nuevas normativas. incluidas en el plan de revisiones.",
    ], start=1)],
}

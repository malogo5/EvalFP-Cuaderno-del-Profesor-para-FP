"""EvalFP — Modelos de Inteligencia Artificial · 5071 · CE Inteligencia Artificial y Big Data
Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 60 h · 2 h/semana · CE IA y Big Data.
"""
MODULO = {
    "nombre":"Modelos de Inteligencia Artificial","codigo":"5071","abrev":"MIA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Caracteriza sistemas de Inteligencia Artificial","horas":8,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Utiliza modelos de sistemas de Inteligencia Artificial implementando…","horas":11,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Relaciona el procesamiento de lenguaje natural con sus aplicaciones…","horas":13,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Analiza sistemas robotizados","horas":8,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica sistemas expertos","horas":9,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Aplica principios legales y éticos al desarrollo de la Inteligencia…","horas":11,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":12,"nombre":"Caracteriza sistemas de Inteligencia Artificial relacionándolos con la mejora de la eficiencia operativa de las organizaciones y empresas."},
    {"id":"RA2","pond":19,"nombre":"Utiliza modelos de sistemas de Inteligencia Artificial implementando sistemas de resolución de problemas."},
    {"id":"RA3","pond":22,"nombre":"Relaciona el procesamiento de lenguaje natural con sus aplicaciones determinando su potencial e identificando sus limitaciones."},
    {"id":"RA4","pond":12,"nombre":"Analiza sistemas robotizados, evaluando opciones de diseño e implementación."},
    {"id":"RA5","pond":16,"nombre":"Aplica sistemas expertos evaluando la influencia de los controladores inteligentes en el comportamiento del sistema."},
    {"id":"RA6","pond":19,"nombre":"Aplica principios legales y éticos al desarrollo de la Inteligencia Artificial integrándolos como parte del proceso."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","proyecto"],
    "RA2":["practica","proyecto"],
    "RA3":["practica","proyecto"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principios fundamentales de los sistemas inteligentes.",
        "Se ha recopilado información sobre campos donde se aplica Inteligencia Artificial.",
        "Se han identificado las técnicas básicas a utilizar en el entorno de la IA.",
        "Se han identificado nuevas formas de interacciones en los negocios que mejore la eficiencia operativa.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado los requisitos básicos a implementar en un sistema de resolución de problemas.",
        "Se han clasificado modelos de Inteligencia Artificial.",
        "Se han caracterizado los modelos de automatización de tareas.",
        "Se han caracterizado los modelos de razonamiento impreciso.",
        "Se han caracterizado los modelos de sistemas basados en reglas.",
        "Se ha valorado la adecuación de los modelos a la implementación del sistema de resolución de problemas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha caracterizado el procesamiento de lenguaje natural.",
        "Se ha justificado el papel del lingüista en un proyecto de Inteligencia Artificial.",
        "Se ha determinado el potencial de las técnicas existentes de procesamiento de lenguaje, así como sus limitaciones.",
        "Se ha considerado en qué casos es factible aplicar estas técnicas en la resolución de un problema.",
        "Se ha evaluado el trabajo cooperativo entre lingüistas e informáticos en el campo del procesamiento del lenguaje natural.",
        "Se ha descrito la formación teórica que precisa el investigador en procesamiento del lenguaje natural.",
        "Se ha elaborado un sistema de procesamiento de lenguaje orientado a una tarea específica.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han recopilado los problemas del modelado y control cinemático en robots manipuladores.",
        "Se han buscado soluciones a los problemas de los robots.",
        "Se han valorado las características diferenciadoras de las técnicas de programación de robots y de sistemas robotizados.",
        "Se han evaluado diferentes opciones en el diseño e implementación de sistemas robotizados.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la dinámica y las estructuras elementales de los sistemas expertos.",
        "Se han determinado las destrezas necesarias para representar y simular comportamientos básicos de sistemas de muy diversos ámbitos.",
        "Se ha razonado cómo influye la variación de las características de los sistemas en su dinámica de actuación.",
        "Se han desarrollado estrategias de control definiendo los objetivos y las especificaciones de la respuesta del sistema.",
        "Se han relacionado los controladores inteligentes con el comportamiento del sistema.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han argumentado los posibles riesgos legales y éticos de la aplicación de Inteligencia Artificial.",
        "Se ha reconocido la necesidad de respetar la privacidad de los datos.",
        "Se ha decidido el cumplimiento estricto de la legalidad en su aplicación.",
        "Se ha integrado como parte del proceso la protección frente a previsibles errores y ataques (security by design).",
        "Se ha comprobado que se cumplen todas las normas legales y éticas en todas las áreas de la Inteligencia Artificial (privacy by design).",
        "Se han identificado y corregido los posibles sesgos de género en el desarrollo y aplicaciones de Inteligencia Artificial y Big Data.",
    ], start=1)],
}

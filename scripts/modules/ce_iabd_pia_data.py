"""EvalFP — Programación de Inteligencia Artificial · 5073 · CE Inteligencia Artificial y Big Data
Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 200 h · 6 h/semana · CE IA y Big Data.
"""
MODULO = {
    "nombre":"Programación de Inteligencia Artificial","codigo":"5073","abrev":"PIA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":6,"total_horas":200,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Lenguajes de programación para IA","horas":60,"eval":1,"tags":"Estructura de un programa · Python · R · Java · JavaScript · NodeJS · JSON · Lenguajes de marcado"},
    {"id":"UT2","nombre":"Desarrollo de aplicaciones de IA","horas":50,"eval":2,"tags":"Plataformas de IA · Entornos de modelado · Definición del modelo · Implementación · Evaluación de resultados"},
    {"id":"UT3","nombre":"Convergencia tecnológica en los negocios","horas":50,"eval":3,"tags":"Unificación de procesos y servicios · Conexión tecnológica · Seguridad · Decisiones estratégicas"},
    {"id":"UT4","nombre":"Automatización industrial y de negocio","horas":40,"eval":3,"tags":"Estrategias corporativas · Relación empresa-cliente · Modelos de automatización · Resultados esperados"},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Caracteriza lenguajes de programación valorando su idoneidad en el desarrollo de Inteligencia Artificial."},
    {"id":"RA2","pond":25,"nombre":"Desarrolla aplicaciones de Inteligencia artificial utilizando entornos de modelado."},
    {"id":"RA3","pond":25,"nombre":"Evalúa las mejoras en los negocios integrando convergencia tecnológica."},
    {"id":"RA4","pond":20,"nombre":"Evalúa modelos de automatización industrial y de negocio relacionándolos con los resultados esperados por las empresas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2"], 3:["RA3","RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","proyecto"],
    "RA3":["examen"],
    "RA4":["examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la estructura de un programa informático.",
        "Se han valorado características en los lenguajes de programación adecuadas al tipo de aplicaciones a implementar.",
        "Se ha determinado el lenguaje de programación más apropiado para el desarrollo de la aplicación.",
        "Se han valorado características de los lenguajes de programación para el desarrollo de Inteligencia Artificial.",
        "Se ha determinado el lenguaje de programación más apropiado para el desarrollo de la aplicación de Inteligencia Artificial.",
        "Se han caracterizado lenguajes de marcado destacando la información que contienen sus etiquetas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado plataformas de Inteligencia Artificial.",
        "Se han caracterizado entornos de modelo de aplicaciones de Inteligencia Artificial.",
        "Se ha definido el modelo que se quiere implementar según el problema planteado.",
        "Se ha implementado la aplicación de Inteligencia Artificial.",
        "Se han evaluado los resultados obtenidos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las ventajas que ofrece unificar procesos, servicios, herramientas, métodos y sectores.",
        "Se han identificado sistemas que facilitan la conexión tecnológica.",
        "Se han evaluado las características de dichos sistemas.",
        "Se ha evaluado como la convergencia tecnológica aporta seguridad en los negocios.",
        "Se ha evaluado la mejora en la capacidad de toma de decisiones estratégicas en un negocio conectado.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las nuevas estrategias corporativas y modelos de negocio en las empresas.",
        "Se ha definido la relación entre empresas y clientes y su efecto en la forma en que las empresas organizan y gestionan sus activos y recursos.",
        "Se han evaluado modelos de automatización para los nuevos requerimientos industriales y de negocio.",
        "Se ha evaluado la conveniencia de cada modelo para conseguir los resultados esperados por las empresas.",
    ], start=1)],
}

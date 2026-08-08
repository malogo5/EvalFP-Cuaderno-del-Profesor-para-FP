"""EvalFP — Proyecto intermodular · 1713 · Sistemas Microinformáticos y Redes
Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo II del Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024) (por remisión expresa del Decreto 79/2024, Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024))
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 55 h · 1 h/semana · 2º SMR.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Proyecto intermodular","codigo":"1713","abrev":"PROY",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":1,"total_horas":55,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo II del Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024) (por remisión expresa del Decreto 79/2024, Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024))",
}
UTS = [
    {"id":"UT1","nombre":"Caracteriza las empresas del sector atendiendo a su…","horas":13,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Plantea soluciones a las necesidades del sector teniendo en…","horas":15,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Planifica la ejecución de las actividades propuestas a la…","horas":13,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Realiza el seguimiento de la ejecución de las actividades…","horas":8,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Transmite información con claridad, de manera ordenada y…","horas":6,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":23,"nombre":"Caracteriza las empresas del sector atendiendo a su organización y al tipo de producto o servicio que ofrecen."},
    {"id":"RA2","pond":28,"nombre":"Plantea soluciones a las necesidades del sector teniendo en cuenta la viabilidad de las mismas, los costes asociados y elaborando un pequeño proyecto."},
    {"id":"RA3","pond":23,"nombre":"Planifica la ejecución de las actividades propuestas a la solución planteada, determinando el plan de intervención y elaborando la documentación correspondiente."},
    {"id":"RA4","pond":16,"nombre":"Realiza el seguimiento de la ejecución de las actividades planteadas, verificando que se cumple con la planificación."},
    {"id":"RA5","pond":10,"nombre":"Transmite información con claridad, de manera ordenada y estructurada."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4"]),
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
        "Se han identificado las empresas tipo más representativas del sector.",
        "Se ha descrito la estructura organizativa de las empresas.",
        "Se han caracterizado los principales departamentos.",
        "Se han determinado las funciones de cada departamento.",
        "Se ha evaluado el volumen de negocio de acuerdo a las necesidades de los clientes.",
        "Se ha definido la estrategia para dar respuesta a las demandas.",
        "Se han valorado los recursos humanos y materiales necesarios.",
        "Se ha realizado el seguimiento de los resultados de acuerdo a la estrategia aplicada.",
        "Se han relacionado los productos o servicios con su posible contribución a los ODS (Objetivos de Desarrollo Sostenible).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las necesidades.",
        "Se han planteado en grupo posibles soluciones.",
        "Se ha obtenido la información relativa a las soluciones planteadas.",
        "Se han identificado aspectos innovadores que puedan ser de aplicación.",
        "Se ha realizado el estudio de viabilidad técnica.",
        "Se han identificado las partes que componen el proyecto.",
        "Se han previsto los recursos materiales y humanos para realizarlo.",
        "Se ha realizado el presupuesto económico correspondiente.",
        "Se ha definido y elaborado la documentación para su diseño.",
        "Se han identificado los aspectos relacionados con la calidad del proyecto.",
        "Se han presentado en público las ideas más relevantes de los proyectos propuestos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han temporizado las secuencias de las actividades.",
        "Se han determinado los recursos y la logística de cada actividad.",
        "Se han identificado permisos y autorizaciones en caso de ser necesarios.",
        "Se han identificado las actividades que implican riesgos en su ejecución.",
        "Se ha tenido en cuenta el plan de prevención de riesgos y los medios y equipos necesarios.",
        "Se han asignado recursos materiales y humanos a cada actividad.",
        "Se han tenido en cuenta posibles imprevistos.",
        "Se han propuesto soluciones a los posibles imprevistos.",
        "Se ha elaborado la documentación necesaria.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido el procedimiento de seguimiento de las actividades.",
        "Se ha verificado la calidad de los resultados de las actividades.",
        "Se han identificado posibles desviaciones de la planificación y/o los resultados esperados.",
        "Se ha informado de las desviaciones en caso de ser necesario.",
        "Se han solucionado las desviaciones y se han documentado las intervenciones.",
        "Se ha definido y elaborado la documentación necesaria para la evaluación de las actividades y del proyecto en su conjunto.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha mantenido una actitud ordenada y metódica en la transmisión de la información.",
        "Se ha transmitido información verbal tanto horizontal como verticalmente.",
        "Se ha transmitido información entre los miembros del grupo utilizando medios informáticos.",
        "Se han conocido los términos técnicos en otras lenguas que sean estándares del sector.",
    ], start=1)],
}

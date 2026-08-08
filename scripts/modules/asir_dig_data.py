"""EvalFP — Digitalización aplicada a los sectores productivos (GS) · 1665 · Administración de Sistemas Informáticos en Red
Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VII del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 50 h · 2 h/semana · 1º ASIR.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Digitalización aplicada a los sectores productivos (GS)","codigo":"1665","abrev":"DIG",
    "ciclo":"Administración de Sistemas Informáticos en Red","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":2,"total_horas":50,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VII del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Analiza el concepto de digitalización y su repercusión en…","horas":8,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Caracteriza las tecnologías habilitadoras digitales…","horas":8,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Identifica sistemas basados en cloud/nube y su influencia en…","horas":5,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Identifica aplicaciones de la IA (inteligencia artificial)…","horas":7,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Evalúa la importancia de los datos, así como su protección…","horas":10,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Desarrolla un proyecto de transformación digital de una…","horas":12,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Analiza el concepto de digitalización y su repercusión en los sectores productivos teniendo en cuenta la actividad de la empresa e identificando entornos IT (Information Technology: tecnología de la información) y OT (Operation Technology: tecnología de operación) característicos."},
    {"id":"RA2","pond":16,"nombre":"Caracteriza las tecnologías habilitadoras digitales necesarias para la adecuación/transformación de las empresas a entornos digitales describiendo sus características y aplicaciones."},
    {"id":"RA3","pond":11,"nombre":"Identifica sistemas basados en cloud/nube y su influencia en el desarrollo de los sistemas digitales."},
    {"id":"RA4","pond":13,"nombre":"Identifica aplicaciones de la IA (inteligencia artificial) en entornos del sector donde está enmarcado el título describiendo las mejoras implícitas en su implementación."},
    {"id":"RA5","pond":20,"nombre":"Evalúa la importancia de los datos, así como su protección en una economía digital globalizada, definiendo sistemas de seguridad y ciberseguridad tanto a nivel de equipo/sistema, como globales."},
    {"id":"RA6","pond":24,"nombre":"Desarrolla un proyecto de transformación digital de una empresa de un sector relacionado con el título, teniendo en cuenta los cambios que se deben producir en función de los objetivos de la empresa."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
]
EVAL_RAS = {1:["RA1", "RA2", "RA3"], 2:["RA4", "RA5", "RA6"]}
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
        "Se ha descrito en qué consiste el concepto de digitalización.",
        "Se ha relacionado la implantación de la tecnología digital con la organización de las empresas.",
        "Se han establecido las diferencias y similitudes entre los entornos IT y OT.",
        "Se han identificado los departamentos típicos de las empresas que pueden constituir entornos IT.",
        "Se han seleccionado las tecnologías típicas de la digitalización en planta y en negocio.",
        "Se ha analizado la importancia de la conexión entre entornos IT y OT.",
        "Se han analizado las ventajas de digitalizar una empresa industrial de extremo a extremo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las principales tecnologías habilitadoras digitales.",
        "Se han relacionado las THD con el desarrollo de productos y servicios.",
        "Se ha relacionado la importancia de las THD con la economía sostenible y eficiente.",
        "Se han identificado nuevos mercados generados por las THD.",
        "Se ha analizado la implicación de THD tanto en la parte de negocio como en la parte de planta.",
        "Se han identificado las mejoras producidas debido a la implantación de las tecnologías habilitadoras en relación con los entornos IT y OT.",
        "Se ha elaborado un informe que relacione, las tecnologías con sus características y áreas de aplicación.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes niveles de la cloud/nube.",
        "Se han identificado las principales funciones de la cloud/nube (procesamiento de datos, intercambio de información, ejecución de aplicaciones, entre otros).",
        "Se ha descrito el concepto de edge computing y su relación con la cloud/nube.",
        "Se han definido los conceptos de fog y mist y sus zonas de aplicación en el conjunto.",
        "Se han identificado las ventajas que proporciona la utilización de la cloud/nube en los sistemas conectados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la importancia de la IA en la automatización de procesos y su optimización.",
        "Se ha relacionado la IA con la recogida masiva de datos (Big Data) y su tratamiento (análisis) con la rentabilidad de las empresas.",
        "Se ha valorado la importancia presente y futura de la IA.",
        "Se han identificado los sectores con implantación más relevante de IA.",
        "Se han identificado los lenguajes de programación en IA.",
        "Se ha descrito como influye la IA en el sector del título.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la diferencia entre dato e información.",
        "Se ha descrito el ciclo de vida del dato.",
        "Se ha identificado la relación entre Big Data, análisis de datos, machine/ deep learning e inteligencia artificial.",
        "Se han descrito las características que definen Big Data.",
        "Se han descrito las etapas típicas de la ciencia de datos y su relación en el proceso.",
        "Se han descrito los procedimientos de almacenaje de datos en la cloud/nube.",
        "Se ha descrito la importancia del cloud computing.",
        "Se han identificado los principales objetivos de la ciencia de datos en las diferentes empresas.",
        "Se ha valorado la importancia de la seguridad y su regulación en relación con los datos.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los objetivos estratégicos de la empresa.",
        "Se han identificado y alineado las áreas de producción/negocio y de comunicaciones.",
        "Se han identificado las áreas susceptibles de ser digitalizadas.",
        "Se ha analizado el encaje de AD (áreas digitalizadas) entre sí y con las que no lo están.",
        "Se han tenido en cuenta las necesidades presentes y futuras de la empresa.",
        "Se han relacionado cada una de las áreas con la implantación de las tecnologías.",
        "Se han analizado las posibles brechas de seguridad en cada una de las áreas.",
        "Se ha definido el tratamiento de los datos y su análisis.",
        "Se ha tenido en cuenta la integración entre datos, aplicaciones, plataformas que los soportan, entre otros.",
        "Se han documentado los cambios realizados en función de la estrategia.",
        "Se han tenido en cuenta la idoneidad de los recursos humanos.",
    ], start=1)],
}

"""EvalFP — Itinerario Personal para la Empleabilidad · 3159 · CFGB Servicios Administrativos
Decreto CLM de modificación de los currículos de CF de Grado Básico (nueva Ley de FP) · Anexo II
RA y CE literales del Anexo II del decreto de Castilla-La Mancha.
Duración CLM: 60 h · 2 h/semana · 1er curso (Anexo I, tabla del ciclo Servicios Administrativos).
"""
MODULO = {
    "nombre":"Itinerario Personal para la Empleabilidad","codigo":"3159","abrev":"IPE",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"1º SA","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo II (texto literal de Castilla-La Mancha)",
}
UTS = [
    {"id":"UT1","nombre":"Prevención de riesgos laborales","horas":18,"eval":1,"tags":"Cultura preventiva · Factores de riesgo · Evaluación de riesgos · Señalización · Emergencias · Primeros auxilios"},
    {"id":"UT2","nombre":"Autoconocimiento profesional","horas":10,"eval":1,"tags":"Intereses · Motivaciones · Competencias personales · Autoestima · DAFO personal"},
    {"id":"UT3","nombre":"Habilidades sociales para el empleo","horas":12,"eval":2,"tags":"Asertividad · Comunicación oral y escrita · Trabajo en equipo · Inteligencia emocional · Gestión de conflictos"},
    {"id":"UT4","nombre":"Itinerarios académicos y profesionales","horas":10,"eval":2,"tags":"Entorno sociolaboral · Itinerarios formativos · Formación permanente · Sin estereotipos vocacionales"},
    {"id":"UT5","nombre":"Proyecto profesional propio","horas":5,"eval":3,"tags":"Ventajas e inconvenientes · Toma de decisiones · Metas profesionales"},
    {"id":"UT6","nombre":"Búsqueda de empleo por cuenta ajena","horas":5,"eval":3,"tags":"Proceso de búsqueda · Fuentes de información · Técnicas · Herramientas (CV, carta, entrevista)"},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Analiza los riesgos derivados de su actividad, analizando las condiciones de trabajo y los factores de riesgo presentes en su entorno laboral."},
    {"id":"RA2","pond":15,"nombre":"Desarrolla actividades de autoconocimiento que le permiten orientarse a campos profesionales motivadores en los que puede desplegar todas sus capacidades."},
    {"id":"RA3","pond":20,"nombre":"Desarrolla habilidades sociales concretas que se han demostrado como fundamentales a la hora de encontrar un empleo y mantenerlo."},
    {"id":"RA4","pond":15,"nombre":"Accede a la información de los posibles itinerarios académicos y/o profesionales que tiene a su alcance a través de la investigación y la reflexión libre de estereotipos vocacionales."},
    {"id":"RA5","pond":10,"nombre":"Pone en marcha un itinerario propio analizando las distintas opciones educativas y profesionales, valorando las ventajas e inconvenientes de cada una de ellas y examinando aquellas que mejor se ajustan a sus posibilidades y preferencias."},
    {"id":"RA6","pond":10,"nombre":"Conoce las estrategias de acceso al mercado de trabajo por cuenta ajena y utiliza las herramientas necesarias para el proceso de inserción laboral."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3"]),
    ("UT5","RA5",["CR1","CR2","CR3"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {"RA1":["examen","practica"], "RA2":["practica"], "RA3":["practica"],
                   "RA4":["practica"], "RA5":["proyecto"], "RA6":["practica"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de la cultura preventiva en todos los ámbitos o actividades de la empresa u organismo equiparado y se identifica la normativa básica de prevención de riesgos y organismos públicos relacionados.",
        "Se han identificado y clasificado los factores de riesgo de la actividad derivado de las condiciones de trabajo y los daños derivados de los mismos, especialmente los relacionados con el título.",
        "Se ha determinado la evaluación de riesgos en la empresa u organismo equiparado y definido las técnicas de prevención y de protección que deben aplicarse para evitar los daños en su origen y minimizar sus consecuencias e identificado la señalización en los lugares de trabajo.",
        "Se han analizado los protocolos de actuación en caso de emergencia.",
        "Se ha valorado la importancia de que exista un plan preventivo en la empresa que incluya la secuenciación de acciones a realizar en caso de emergencia, así como tiene conocimiento de la documentación básica en prevención de riesgos.",
        "Se han identificado las técnicas básicas de primeros auxilios que han de ser aplicadas en el lugar del accidente ante distintos tipos de daños.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado los propios intereses, motivaciones, habilidades y destrezas en el marco de un proceso de autoconocimiento.",
        "Se han determinado las competencias personales y sociales con valor para el empleo.",
        "Se ha valorado el concepto de autoestima en el proceso de búsqueda de empleo.",
        "Se han identificado las fortalezas, debilidades, amenazas y oportunidades propias para la inserción profesional, así como las estrategias para sacarles el mayor aprovechamiento.",
        "Se han identificado expectativas de futuro para la inserción profesional analizando competencias, intereses y destrezas personales.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de las competencias personales y sociales en la empleabilidad.",
        "Se han aplicado estrategias para canalizar las emociones de manera asertiva en las relaciones con otras personas, diferenciándolas de conductas agresivas y/o pasivas.",
        "Se han puesto en práctica técnicas de presentación, orales y escritas, para una comunicación efectiva y afectiva valorando su importancia como recurso personal para la empleabilidad.",
        "Se han identificado los beneficios del trabajo en equipo, así como las diferentes formas de llevarlo a cabo.",
        "Se ha reaccionado de forma flexible y positiva ante conflictos y situaciones nuevas, aprovechando las oportunidades y gestionando las dificultades haciendo uso de estrategias relacionadas con la inteligencia emocional.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha determinado la realidad del entorno sociolaboral actual.",
        "Se han identificado los itinerarios académicos y profesionales afines a sus intereses y se han valorado las opciones que mejor se ajustan a sus perfiles profesionales y sus preferencias.",
        "Se ha valorado la importancia de la formación permanente como factor clave para el empleo y la adaptación al cambio.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han valorado las ventajas e inconvenientes de cada una de las opciones posibles.",
        "Se han analizado y seleccionado las opciones que más se ajustan a sus perfiles profesionales.",
        "Se ha realizado un proceso de toma de decisiones identificando el itinerario académico y profesional personal, a partir de sus preferencias profesionales, intereses y metas en el marco de un proyecto profesional.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado la búsqueda de empleo como un proceso.",
        "Se han identificado las diferentes fuentes de información de acceso al empleo.",
        "Se han analizado las distintas técnicas utilizadas para la búsqueda de empleo por cuenta ajena.",
        "Se han puesto en práctica las diferentes herramientas que permitan una búsqueda de empleo óptima.",
    ], start=1)],
}

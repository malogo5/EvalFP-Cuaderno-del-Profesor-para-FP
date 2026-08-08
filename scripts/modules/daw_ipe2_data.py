"""EvalFP — Itinerario personal para la empleabilidad II · 1710 · Desarrollo de Aplicaciones Web
Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo V del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 60 h · 3 h/semana · 2º DAW.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Itinerario personal para la empleabilidad II","codigo":"1710","abrev":"IPE2",
    "ciclo":"Desarrollo de Aplicaciones Web","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":3,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo V del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Planifica y pone en marcha estrategias en los diferentes…","horas":7,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Aplica estrategias relacionadas con las competencias…","horas":12,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Pone en práctica las habilidades emprendedoras necesarias…","horas":10,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Identifica, define y valida ideas de emprendimiento…","horas":16,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Desarrolla un proyecto emprendedor de innovación social y/o…","horas":15,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":11,"nombre":"Planifica y pone en marcha estrategias en los diferentes procesos selectivos de empleo que le permiten mejorar sus posibilidades de inserción laboral."},
    {"id":"RA2","pond":20,"nombre":"Aplica estrategias relacionadas con las competencias personales, sociales y emocionales para el empleo en búsqueda de la mejora de su empleabilidad."},
    {"id":"RA3","pond":17,"nombre":"Pone en práctica las habilidades emprendedoras necesarias para el desarrollo de procesos de innovación e investigación aplicadas que promuevan la modernización del sector productivo hacia un modelo sostenible."},
    {"id":"RA4","pond":26,"nombre":"Identifica, define y valida ideas de emprendimiento generadoras de nuevas oportunidades a partir de estrategias de análisis del entorno socio productivo utilizando metodologías ágiles para el emprendimiento."},
    {"id":"RA5","pond":26,"nombre":"Desarrolla un proyecto emprendedor de innovación social y/o tecnológica aplicada en colaboración con el entorno."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
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
        "Se han determinado las técnicas utilizadas actualmente en el sector para el proceso de selección de personal.",
        "Se han desarrollado estrategias para la búsqueda de empleo relacionadas con las técnicas actuales más utilizadas contextualizadas al sector.",
        "Se han valorado las actitudes y aptitudes que permiten superar procesos selectivos en el sector privado y en el sector público.",
        "Se ha construido una marca personal identificando las necesidades del mercado actual, sus habilidades, destrezas y su aporte de valor.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de las competencias personales y sociales en la empleabilidad en el sector de referencia.",
        "Se ha participado activamente en el establecimiento de los objetivos del equipo y en la toma de decisiones del mismo y asumido la responsabilidad de las acciones y decisiones del grupo, participando activamente en el logro de unos objetivos compartidos cooperando con otras personas y compartiendo el liderazgo.",
        "Se han incorporado al propio proceso de aprendizaje las técnicas y recursos de presentación y comunicación, tanto orales como escritos, adecuados para una comunicación efectiva y afectiva siendo capaz de adaptarlos a cada situación y circunstancias, valorando las oportunidades y dificultades que ofrece cada una de ellas.",
        "Se han aplicado técnicas y estrategias para la gestión del tiempo disponible para alcanzar los objetivos tanto individuales como del equipo y programado las actividades necesarias.",
        "Se han aplicado estrategias para canalizar las emociones mostrando una actitud flexible en las relaciones con otras personas.",
        "Se han desarrollado estrategias para la programación de actividades atendiendo a criterios de organización eficiente y previendo las posibles dificultades.",
        "Se ha reaccionado de forma flexible y positiva ante conflictos y situaciones nuevas, aprovechando las oportunidades y gestionando las dificultades haciendo uso de estrategias relacionadas con la inteligencia emocional.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado el concepto de innovación y su relación con la construcción de una sociedad más sostenible que mejore en el bienestar de los individuos.",
        "Se han analizado las distintas metodologías para emprender y su importancia para favorecer la innovación y como fuente de creación de empleo y bienestar social.",
        "Se han aplicado las habilidades emprendedoras necesarias para promover el emprendimiento y el intraemprendimiento.",
        "Se ha puesto en práctica el trabajo colaborativo como requisito para el desarrollo de procesos de innovación.",
        "Se ha desarrollado la competencia digital necesaria para la mejora de los procesos de innovación e investigación aplicadas que promuevan la modernización del sector productivo.",
        "Se han incorporado los objetivos de las políticas e iniciativas relacionadas con la sostenibilidad y el medio ambiente a la estrategia empresarial enfocada al desarrollo de un modelo económico y social sostenible.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los problemas de las personas destinatarias potenciales del proyecto emprendedor como paso previo a la propuesta de soluciones que se conviertan en oportunidades.",
        "Se ha puesto en práctica el proceso creativo con el fin de conseguir una idea emprendedora que aporte valor económico, social y/o cultural.",
        "Se ha diseñado un modelo de negocio y/o gestión derivado de la idea emprendedora.",
        "Se han incorporado valores éticos y sociales a la idea emprendedora analizando modelos de balance social.",
        "Se ha analizado la contribución de la Economía Circular y la Economía del Bien Común al desarrollo de un modelo económico y social basado en la equidad, la justicia social y la sostenibilidad.",
        "Se han analizado los principales componentes del entorno general y específico, y su impacto en la idea emprendedora.",
        "Se han realizado entrevistas de problema para validar el perfil y el problema de las personas destinatarias de la idea emprendedora.",
        "Se ha validado la solución mediante la creación de prototipos buscando el encaje problema-solución.",
        "Se ha experimentado con la puesta en práctica de estrategias de marketing para desarrollar destrezas en técnicas de comunicación y venta.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los conceptos básicos del emprendimiento y la innovación social.",
        "Se ha reflexionado sobre la necesidad del liderazgo ético y sostenible en las organizaciones.",
        "Se ha reflexionado sobre la tecnología como base para el cambio del modelo productivo.",
        "Se han puesto en marcha las estrategias propias del pensamiento de diseño para detectar necesidades sociales y medioambientales.",
        "Se han analizado los elementos del diseño de modelos de negocio ecosociales y/o de base tecnológica.",
        "Se han alineado metas de desarrollo sostenible con el diseño de modelos de negocio ecosociales y/o de base tecnológica.",
        "Se han aplicado las estrategias necesarias para analizar la viabilidad del proyecto emprendedor.",
        "Se han investigado las opciones financieras socialmente responsables.",
        "Se han definido los agentes implicados en el proyecto, así como su participación en el mismo.",
    ], start=1)],
}

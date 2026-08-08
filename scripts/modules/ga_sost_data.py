"""EvalFP — Sostenibilidad aplicada al sistema productivo · 1708 · Gestión Administrativa
Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VIII del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 40 h · 1 h/semana · 1º GA.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Sostenibilidad aplicada al sistema productivo","codigo":"1708","abrev":"SOST",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"1º GA","horas_sem":1,"total_horas":40,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VIII del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Identifica los aspectos ambientales, sociales y de…","horas":7,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Caracteriza los retos ambientales y sociales a los que se…","horas":6,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Establece la aplicación de criterios de sostenibilidad en el…","horas":3,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Propón productos y servicios responsables teniendo en cuenta…","horas":7,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Realiza actividades sostenibles minimizando el impacto de…","horas":11,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Analiza un plan de sostenibilidad de una empresa del sector,…","horas":6,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Identifica los aspectos ambientales, sociales y de gobernanza (ASG) relativos a la sostenibilidad teniendo en cuenta el concepto de desarrollo sostenible y los marcos internacionales que contribuyen a su consecución."},
    {"id":"RA2","pond":15,"nombre":"Caracteriza los retos ambientales y sociales a los que se enfrenta la sociedad, describiendo los impactos sobre las personas y los sectores productivos y proponiendo acciones para minimizarlos."},
    {"id":"RA3","pond":9,"nombre":"Establece la aplicación de criterios de sostenibilidad en el desempeño profesional y personal, identificando los elementos necesarios."},
    {"id":"RA4","pond":17,"nombre":"Propón productos y servicios responsables teniendo en cuenta los principios de la economía circular."},
    {"id":"RA5","pond":26,"nombre":"Realiza actividades sostenibles minimizando el impacto de las mismas en el medio ambiente."},
    {"id":"RA6","pond":15,"nombre":"Analiza un plan de sostenibilidad de una empresa del sector, identificando sus grupos de interés, los aspectos ASG materiales y justificando acciones para su gestión y medición."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
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
        "Se ha descrito el concepto de sostenibilidad, estableciendo los marcos internacionales asociados al desarrollo sostenible.",
        "Se han identificado los asuntos ambientales, sociales y de gobernanza que influyen en el desarrollo sostenible de las organizaciones empresariales.",
        "Se han relacionado los Objetivos de Desarrollo Sostenible (ODS) con su importancia para la consecución de la Agenda 2030.",
        "Se ha analizado la importancia de identificar los aspectos ASG más relevantes para los grupos de interés de las organizaciones relacionándolos con los riesgos y oportunidades que suponen para la propia organización.",
        "Se han identificado los principales estándares de métricas para la evaluación del desempeño en sostenibilidad y su papel en la rendición de cuentas que marca la legislación vigente y las futuras regulaciones en desarrollo.",
        "Se ha descrito la inversión socialmente responsable y el papel de los analistas, inversores, agencias e índices de sostenibilidad en el fomento de la sostenibilidad.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales retos ambientales y sociales.",
        "Se han relacionado los retos ambientales y sociales con el desarrollo de la actividad económica.",
        "Se ha analizado el efecto de los impactos ambientales y sociales sobre las personas y los sectores productivos.",
        "Se han identificado las medidas y acciones encaminadas a minimizar los impactos ambientales y sociales.",
        "Se ha analizado la importancia de establecer alianzas y trabajar de manera transversal y coordinada para abordar con éxito los retos ambientales y sociales.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los ODS más relevantes para la actividad profesional que realiza.",
        "Se han analizado los riesgos y oportunidades que representan los ODS.",
        "Se han identificado las acciones necesarias para atender algunos de los retos ambientales y sociales desde la actividad profesional y el entorno personal.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha caracterizado el modelo de producción y consumo actual.",
        "Se han identificado los principios de la economía verde y circular.",
        "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción.",
        "Se han aplicado principios de ecodiseño.",
        "Se ha analizado el ciclo de vida del producto.",
        "Se han identificado los procesos de producción y los criterios de sostenibilidad aplicados.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha caracterizado el modelo de producción y consumo actual.",
        "Se han identificado los principios de la economía verde y circular.",
        "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción.",
        "Se ha evaluado el impacto de las actividades personales y profesionales.",
        "Se han aplicado principios de ecodiseño.",
        "Se han aplicado estrategias sostenibles.",
        "Se ha analizado el ciclo de vida del producto.",
        "Se han identificado los procesos de producción y los criterios de sostenibilidad aplicados.",
        "Se ha aplicado la normativa ambiental.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales grupos de interés de la empresa.",
        "Se han analizado los aspectos ASG materiales, las expectativas de los grupos de interés y la importancia de los aspectos ASG en relación con los objetivos empresariales.",
        "Se han definido acciones encaminadas a minimizar los impactos negativos y aprovechar las oportunidades que plantean los principales aspectos ASG identificados.",
        "Se han determinado las métricas de evaluación del desempeño de la empresa de acuerdo con los estándares de sostenibilidad más ampliamente utilizados.",
        "Se ha elaborado un informe de sostenibilidad con el plan y los indicadores propuestos.",
    ], start=1)],
}

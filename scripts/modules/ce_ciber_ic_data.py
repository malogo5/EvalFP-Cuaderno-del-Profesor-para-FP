"""EvalFP — Incidentes de Ciberseguridad · 5021 · CE Ciberseguridad
RD 479/2020, de 7 de abril (BOE) · Decreto CLM 77/2022, de 12 de julio (DOCM)
"""
MODULO = {
    "nombre":"Incidentes de Ciberseguridad","codigo":"5021","abrev":"IC",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 479/2020, de 7 de abril · Decreto CLM 77/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Desarrollo de planes de prevención y concienciación","horas":25,"eval":1,"tags":"Plan de seguridad · Políticas · Concienciación · Normativa · ISO 27001"},
    {"id":"UT2","nombre":"Auditoría de incidentes de ciberseguridad","horas":30,"eval":1,"tags":"SIEM · Logs · Correlación · Alertas · IDS/IPS · SOC"},
    {"id":"UT3","nombre":"Investigación de los incidentes de ciberseguridad","horas":30,"eval":2,"tags":"Análisis · Evidencias · Cadena de custodia · Herramientas forenses"},
    {"id":"UT4","nombre":"Implementación de medidas de ciberseguridad","horas":20,"eval":2,"tags":"Hardening · Parches · Firewall · WAF · Cifrado · Bastionado"},
    {"id":"UT5","nombre":"Documentación y notificación de incidentes","horas":15,"eval":2,"tags":"ENISA · INCIBE · CCN-CERT · Notificación RGPD · Informes"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Desarrolla planes de prevención y concienciación en ciberseguridad, analizando las necesidades de la organización."},
    {"id":"RA2","pond":20,"nombre":"Analiza incidentes de ciberseguridad utilizando herramientas, mecanismos de detección y alertas de seguridad."},
    {"id":"RA3","pond":25,"nombre":"Investiga incidentes de ciberseguridad analizando los riesgos implicados y definiendo las acciones correctivas."},
    {"id":"RA4","pond":20,"nombre":"Implementa medidas de ciberseguridad en redes y sistemas respondiendo a los incidentes detectados."},
    {"id":"RA5","pond":15,"nombre":"Detecta y documenta incidentes de ciberseguridad siguiendo procedimientos de actuación establecidos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales tipos de incidentes de ciberseguridad.",
        "Se han definido políticas de prevención de incidentes para los activos de la organización.",
        "Se ha elaborado un plan de concienciación en ciberseguridad para los usuarios.",
        "Se han identificado las fases de un plan de respuesta a incidentes.",
        "Se han definido los roles y responsabilidades del equipo de respuesta a incidentes.",
        "Se ha evaluado la eficacia del plan de prevención mediante simulacros y auditorías.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado los incidentes de ciberseguridad según su tipología e impacto.",
        "Se han utilizado herramientas SIEM para la recopilación y correlación de eventos.",
        "Se han configurado alertas en sistemas de detección de intrusiones (IDS/IPS).",
        "Se han analizado logs del sistema, de aplicaciones y de red para detectar anomalías.",
        "Se ha verificado la integridad de los sistemas ante posibles compromisos.",
        "Se han identificado los indicadores de compromiso (IoC) del incidente.",
        "Se ha documentado el proceso de detección y los hallazgos obtenidos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han recopilado evidencias digitales siguiendo procedimientos forenses.",
        "Se ha mantenido la cadena de custodia de las evidencias obtenidas.",
        "Se ha analizado el alcance e impacto del incidente en los sistemas afectados.",
        "Se han identificado las técnicas, tácticas y procedimientos del atacante.",
        "Se ha determinado el vector de ataque y las vulnerabilidades explotadas.",
        "Se han propuesto medidas correctivas para evitar la recurrencia del incidente.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado medidas de contención para limitar el impacto del incidente.",
        "Se han eliminado los artefactos maliciosos y cerrado los vectores de ataque.",
        "Se han aplicado parches y actualizaciones de seguridad en los sistemas afectados.",
        "Se han restaurado los sistemas afectados a un estado operativo seguro.",
        "Se han verificado los sistemas restaurados antes de volver a ponerlos en producción.",
        "Se han reforzado las medidas de seguridad para prevenir incidentes similares.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha elaborado el informe técnico del incidente con todos los detalles del análisis.",
        "Se ha notificado el incidente a los organismos competentes (INCIBE, CCN-CERT, AEPD).",
        "Se han cumplido los plazos de notificación establecidos por el RGPD y la normativa.",
        "Se han comunicado las conclusiones del incidente a los responsables de la organización.",
        "Se han archivado las evidencias y la documentación del incidente según los procedimientos.",
    ], start=1)],
}

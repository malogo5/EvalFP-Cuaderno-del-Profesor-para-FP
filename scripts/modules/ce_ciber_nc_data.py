"""EvalFP — Normativa de Ciberseguridad · 5026 · CE Ciberseguridad
RD 479/2020, de 7 de abril (BOE) · Decreto CLM 77/2022, de 12 de julio (DOCM)
"""
MODULO = {
    "nombre":"Normativa de Ciberseguridad","codigo":"5026","abrev":"NC",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 479/2020, de 7 de abril · Decreto CLM 77/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Legislación y cumplimiento en ciberseguridad","horas":20,"eval":1,"tags":"RGPD · LOPDGDD · Ley NIS2 · ENS · LSSI · Responsabilidad · DPO"},
    {"id":"UT2","nombre":"Marcos y estándares de ciberseguridad","horas":20,"eval":1,"tags":"ISO 27001 · NIST CSF · ENS · CIS Controls · PCI-DSS · SOC2"},
    {"id":"UT3","nombre":"Gestión de riesgos y cumplimiento","horas":20,"eval":2,"tags":"MAGERIT · Análisis de riesgos · GAP Analysis · Auditoría · Certificación"},
]
RAS = [
    {"id":"RA1","pond":35,"nombre":"Identifica la normativa legal e interna en materia de ciberseguridad, aplicando la legislación vigente."},
    {"id":"RA2","pond":35,"nombre":"Implanta políticas de seguridad de la información aplicando los marcos y estándares internacionales."},
    {"id":"RA3","pond":30,"nombre":"Realiza análisis de riesgos de ciberseguridad determinando su impacto y proponiendo medidas de control."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","examen"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las principales normas y leyes en materia de protección de datos: RGPD y LOPDGDD.",
        "Se ha analizado la Ley de Servicios de la Sociedad de la Información (LSSI) y el comercio electrónico.",
        "Se han descrito las obligaciones derivadas de la Directiva NIS2 para operadores esenciales e importantes.",
        "Se han identificado los requisitos del Esquema Nacional de Seguridad (ENS) y sus categorías.",
        "Se ha analizado la responsabilidad penal en materia de delitos informáticos.",
        "Se han identificado las obligaciones del Delegado de Protección de Datos (DPO).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los controles del estándar ISO 27001 y su estructura.",
        "Se ha descrito el proceso de certificación en ISO 27001.",
        "Se han aplicado los controles del NIST Cybersecurity Framework.",
        "Se han identificado los controles CIS y su relación con otros marcos.",
        "Se han elaborado políticas de seguridad de la información para una organización.",
        "Se ha realizado un análisis de brecha (GAP Analysis) respecto a un marco de referencia.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los activos de información y su valoración.",
        "Se han identificado las amenazas y vulnerabilidades de los activos.",
        "Se ha calculado el riesgo inherente y el riesgo residual de los activos.",
        "Se han propuesto medidas de tratamiento del riesgo: aceptar, mitigar, transferir o evitar.",
        "Se ha elaborado el plan de tratamiento de riesgos con las medidas priorizadas.",
        "Se ha documentado el proceso de análisis de riesgos según la metodología MAGERIT.",
    ], start=1)],
}

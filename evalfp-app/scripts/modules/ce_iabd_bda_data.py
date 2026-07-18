"""EvalFP — Big Data aplicado · 5075 · CE Inteligencia Artificial y Big Data
RD 279/2021, de 20 de abril (BOE) · Decreto CLM 69/2022, de 21 de junio (DOCM)
"""
MODULO = {
    "nombre":"Big Data aplicado","codigo":"5075","abrev":"BDA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IABD","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 279/2021, de 20 de abril · Decreto CLM 69/2022, de 21 de junio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Análisis y visualización avanzada de datos","horas":30,"eval":1,"tags":"Tableau · Power BI · Matplotlib · Seaborn · Plotly · Storytelling · KPIs"},
    {"id":"UT2","nombre":"Proyectos de Big Data e IA en producción","horas":45,"eval":1,"tags":"MLOps · Docker · Kubernetes · CI/CD · Monitorización · Drift · Feature Store"},
    {"id":"UT3","nombre":"Aplicaciones sectoriales de Big Data e IA","horas":45,"eval":2,"tags":"Salud · Finanzas · Industria 4.0 · Smart Cities · Recomendadores · NLP · Computer Vision"},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Realiza análisis y visualizaciones avanzadas de datos, extrayendo conclusiones de valor para la toma de decisiones."},
    {"id":"RA2","pond":35,"nombre":"Despliega y gestiona modelos de IA en producción aplicando técnicas de MLOps."},
    {"id":"RA3","pond":35,"nombre":"Diseña y desarrolla proyectos de Big Data e IA aplicados a sectores reales, integrando las tecnologías del ciclo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["proyecto","presentacion"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado visualizaciones avanzadas con librerías Python (Matplotlib, Seaborn, Plotly).",
        "Se han diseñado dashboards interactivos con herramientas como Power BI o Tableau.",
        "Se han aplicado técnicas de storytelling con datos para comunicar hallazgos a audiencias no técnicas.",
        "Se han definido y calculado KPIs relevantes para el negocio a partir de los datos analizados.",
        "Se ha realizado análisis exploratorio de datos (EDA) sobre conjuntos de datos reales.",
        "Se han identificado patrones, tendencias y anomalías en los datos que aporten valor al negocio.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los principios de MLOps y su ciclo de vida.",
        "Se han empaquetado modelos de ML en contenedores Docker para su despliegue.",
        "Se han implementado pipelines de CI/CD para la automatización del despliegue de modelos.",
        "Se han configurado sistemas de monitorización del rendimiento de los modelos en producción.",
        "Se han detectado y gestionado problemas de data drift y model drift.",
        "Se han utilizado plataformas MLOps (MLflow, Kubeflow) para la gestión del ciclo de vida del modelo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado oportunidades de aplicación del Big Data y la IA en diferentes sectores.",
        "Se ha diseñado la arquitectura de un proyecto de Big Data e IA de principio a fin.",
        "Se han implementado sistemas de recomendación aplicados a casos reales.",
        "Se han aplicado técnicas de NLP para el análisis de texto en entornos empresariales.",
        "Se han desarrollado aplicaciones de Computer Vision para la automatización de procesos.",
        "Se ha presentado un proyecto completo de Big Data e IA ante un público técnico y no técnico.",
        "Se han valorado los aspectos éticos, de privacidad y sesgo en las aplicaciones de IA.",
    ], start=1)],
}

"""EvalFP — Análisis de Datos con Python · CE Desarrollo de Aplicaciones en Python"""
MODULO = {
    "nombre":"Análisis de Datos con Python","codigo":"PYDATA","abrev":"PYDATA",
    "ciclo":"CE Desarrollo de Aplicaciones en Python","ciclo_clave":"CE_PYTHON","ciclo_nivel":"CE",
    "curso":"CE Python","horas_sem":5,"total_horas":150,"anno":"2026-2027","eval_count":2,
    "decreto":"CE Desarrollo de Aplicaciones en Python (Decreto CLM — Turno Diurno)",
}
UTS = [
    {"id":"UT1","nombre":"Manipulación de datos con NumPy y Pandas","horas":35,"eval":1,"tags":"NumPy · Arrays · Pandas · DataFrame · Series · Merging · GroupBy · Limpieza"},
    {"id":"UT2","nombre":"Visualización de datos","horas":25,"eval":1,"tags":"Matplotlib · Seaborn · Plotly · Gráficos · Dashboards · Storytelling"},
    {"id":"UT3","nombre":"Análisis estadístico y web scraping","horas":30,"eval":2,"tags":"Estadística · Scipy · Correlación · Regresión · BeautifulSoup · Selenium · APIs"},
    {"id":"UT4","nombre":"Introducción a Machine Learning con Python","horas":30,"eval":2,"tags":"Scikit-learn · Clasificación · Regresión · Clustering · Pipeline · Evaluación"},
    {"id":"UT5","nombre":"Proyecto de análisis de datos","horas":30,"eval":2,"tags":"EDA · Dataset real · Insights · Informe · Dashboard · Presentación"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Manipula y transforma conjuntos de datos con NumPy y Pandas para prepararlos para el análisis."},
    {"id":"RA2","pond":20,"nombre":"Crea visualizaciones de datos efectivas utilizando librerías Python especializadas."},
    {"id":"RA3","pond":20,"nombre":"Aplica técnicas de análisis estadístico y extrae datos de fuentes web y APIs."},
    {"id":"RA4","pond":25,"nombre":"Implementa modelos básicos de Machine Learning con Scikit-learn para la resolución de problemas de datos."},
    {"id":"RA5","pond":10,"nombre":"Desarrolla un proyecto completo de análisis de datos que aporte valor a un caso real."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {"RA1":["practica"],"RA2":["practica"],"RA3":["practica"],"RA4":["practica"],"RA5":["proyecto"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado y manipulado arrays multidimensionales con NumPy.",
        "Se han realizado operaciones vectorizadas y broadcasting sobre arrays NumPy.",
        "Se han creado y manipulado DataFrames y Series con Pandas.",
        "Se han limpiado y tratado datos: valores nulos, duplicados, tipos de datos y outliers.",
        "Se han realizado operaciones de filtrado, selección y transformación de datos.",
        "Se han combinado DataFrames mediante merge, join y concatenación.",
        "Se han aplicado operaciones de agrupación y agregación con groupby y pivot_table.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han creado gráficos estadísticos (histogramas, boxplots, scatter plots) con Matplotlib.",
        "Se han elaborado visualizaciones estadísticas avanzadas con Seaborn.",
        "Se han creado gráficos interactivos con Plotly.",
        "Se han diseñado dashboards básicos para la presentación de resultados.",
        "Se han aplicado principios de diseño visual y storytelling para comunicar hallazgos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han calculado estadísticos descriptivos y aplicado pruebas de hipótesis.",
        "Se ha analizado la correlación entre variables y se han identificado relaciones causales.",
        "Se han extraído datos de páginas web con BeautifulSoup y Selenium.",
        "Se han consumido datos de APIs públicas mediante requests.",
        "Se han automatizado la descarga y procesamiento de datos de fuentes externas.",
        "Se ha valorado la legalidad y ética del web scraping.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han preparado características (features) y etiquetas (labels) para el entrenamiento de modelos.",
        "Se han implementado modelos de clasificación y regresión con Scikit-learn.",
        "Se han evaluado modelos con métricas apropiadas y técnicas de validación cruzada.",
        "Se han aplicado técnicas de selección de características y preprocesamiento con Pipeline.",
        "Se han aplicado algoritmos de clustering sobre datos no etiquetados.",
        "Se han comparado distintos modelos seleccionando el más adecuado para el problema.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha seleccionado un dataset real y se ha planteado una pregunta de investigación.",
        "Se ha realizado un análisis exploratorio de datos (EDA) completo.",
        "Se han extraído conclusiones y recomendaciones a partir del análisis.",
        "Se ha elaborado un informe técnico documentando el proceso y los hallazgos.",
        "Se ha presentado el proyecto con un dashboard o notebook interactivo.",
    ], start=1)],
}

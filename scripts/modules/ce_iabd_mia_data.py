"""EvalFP — Modelos de Inteligencia Artificial · 5071 · CE Inteligencia Artificial y Big Data
RD 279/2021, de 20 de abril (BOE) · Decreto CLM 69/2022, de 21 de junio (DOCM)
"""
MODULO = {
    "nombre":"Modelos de Inteligencia Artificial","codigo":"5071","abrev":"MIA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IABD","horas_sem":2,"total_horas":60,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 279/2021, de 20 de abril · Decreto CLM 69/2022, de 21 de junio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Fundamentos de Inteligencia Artificial y aprendizaje automático","horas":15,"eval":1,"tags":"IA · ML · Tipos de aprendizaje · Scikit-learn · Python · Numpy · Pandas"},
    {"id":"UT2","nombre":"Modelos de aprendizaje supervisado","horas":25,"eval":1,"tags":"Regresión · Clasificación · SVM · Árboles de decisión · Random Forest · KNN"},
    {"id":"UT3","nombre":"Modelos de aprendizaje no supervisado y redes neuronales","horas":20,"eval":2,"tags":"Clustering · K-Means · PCA · Redes neuronales · TensorFlow · Keras"},
]
RAS = [
    {"id":"RA1","pond":30,"nombre":"Identifica los fundamentos del aprendizaje automático, diferenciando los tipos de algoritmos y sus aplicaciones."},
    {"id":"RA2","pond":40,"nombre":"Entrena y evalúa modelos de aprendizaje supervisado, seleccionando el algoritmo más adecuado al problema."},
    {"id":"RA3","pond":30,"nombre":"Aplica técnicas de aprendizaje no supervisado y redes neuronales para la extracción de patrones y clasificación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","proyecto"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales paradigmas de la Inteligencia Artificial.",
        "Se han diferenciado los tipos de aprendizaje automático: supervisado, no supervisado y por refuerzo.",
        "Se han descrito las fases del proceso de desarrollo de un modelo de ML.",
        "Se han preparado y preprocesado conjuntos de datos para el entrenamiento de modelos.",
        "Se han utilizado librerías Python (NumPy, Pandas, Scikit-learn) para el análisis de datos.",
        "Se ha evaluado la calidad de los datos identificando valores perdidos, outliers y sesgos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han implementado modelos de regresión lineal y logística para problemas de predicción.",
        "Se han aplicado algoritmos de clasificación: SVM, Árboles de decisión, Random Forest y KNN.",
        "Se han dividido los datos en conjuntos de entrenamiento y test, aplicando validación cruzada.",
        "Se han evaluado los modelos con métricas: precisión, recall, F1-score, RMSE y matriz de confusión.",
        "Se han aplicado técnicas de optimización de hiperparámetros (Grid Search, Random Search).",
        "Se han identificado y tratado problemas de sobreajuste y subajuste.",
        "Se ha seleccionado el modelo más adecuado para cada tipo de problema.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado algoritmos de clustering (K-Means, DBSCAN) para la agrupación de datos.",
        "Se ha aplicado PCA y otras técnicas de reducción de dimensionalidad.",
        "Se han descrito los fundamentos de las redes neuronales artificiales.",
        "Se han implementado redes neuronales con TensorFlow/Keras para clasificación.",
        "Se han descrito arquitecturas de Deep Learning: CNN, RNN y Transformers.",
        "Se ha evaluado el rendimiento de los modelos de redes neuronales y se ha ajustado la arquitectura.",
    ], start=1)],
}

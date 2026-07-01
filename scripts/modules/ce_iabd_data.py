"""EvalFP — Curso de Especialización en Inteligencia Artificial y Big Data
Módulo representativo: Sistemas de Aprendizaje Automático (5072)
RD 279/2021, de 20 de abril
"""
MODULO = {
    "nombre":"Sistemas de Aprendizaje Automático","codigo":"5072","abrev":"SAA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":6,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto": "RD 279/2021, de 20 de abril · Decreto CLM 69/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Caracterización de los sistemas de aprendizaje automático","horas":20,"eval":1,"tags":"ML · Supervised · Unsupervised · Reinforcement · scikit-learn"},
    {"id":"UT2","nombre":"Uso de algoritmos de aprendizaje supervisado","horas":25,"eval":1,"tags":"Regresión · Clasificación · SVM · Árboles · Random Forest"},
    {"id":"UT3","nombre":"Uso de algoritmos de aprendizaje no supervisado","horas":20,"eval":1,"tags":"Clustering · K-means · PCA · Reducción dimensionalidad"},
    {"id":"UT4","nombre":"Diseño y aplicación de redes neuronales","horas":30,"eval":2,"tags":"Deep Learning · TensorFlow · Keras · CNN · RNN · Transfer Learning"},
    {"id":"UT5","nombre":"Evaluación y optimización de modelos","horas":25,"eval":2,"tags":"Métricas · Cross-validation · Hyperparameter tuning · MLflow"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Caracteriza los sistemas de aprendizaje automático, reconociendo sus aplicaciones y describiendo las etapas del proceso de aprendizaje."},
    {"id":"RA2","pond":25,"nombre":"Aplica algoritmos de aprendizaje supervisado, configurando los parámetros y evaluando los modelos obtenidos."},
    {"id":"RA3","pond":20,"nombre":"Aplica algoritmos de aprendizaje no supervisado, configurando los parámetros y evaluando los modelos obtenidos."},
    {"id":"RA4","pond":20,"nombre":"Diseña y aplica redes neuronales artificiales, valorando su rendimiento en el aprendizaje profundo."},
    {"id":"RA5","pond":15,"nombre":"Evalúa modelos de aprendizaje automático, seleccionando las métricas adecuadas e interpretando los resultados."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","proyecto"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos paradigmas de aprendizaje automático.",
        "Se han descrito las fases del proceso de aprendizaje automático.",
        "Se han identificado los principales algoritmos de cada paradigma.",
        "Se han reconocido las aplicaciones del aprendizaje automático en distintos dominios.",
        "Se han preparado y limpiado conjuntos de datos para el entrenamiento.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado algoritmos de regresión adecuados al problema.",
        "Se han seleccionado algoritmos de clasificación adecuados al problema.",
        "Se han entrenado modelos supervisados con conjuntos de datos reales.",
        "Se han ajustado los hiperparámetros de los modelos.",
        "Se ha evaluado el rendimiento de los modelos con métricas adecuadas.",
        "Se han documentado los experimentos y resultados obtenidos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado algoritmos de clustering para agrupar datos.",
        "Se ha configurado y aplicado el algoritmo K-means.",
        "Se han aplicado técnicas de reducción de dimensionalidad (PCA).",
        "Se han interpretado los resultados del aprendizaje no supervisado.",
        "Se han documentado los experimentos de aprendizaje no supervisado.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los fundamentos de las redes neuronales artificiales.",
        "Se han diseñado arquitecturas de redes neuronales con frameworks.",
        "Se han entrenado redes neuronales con conjuntos de datos reales.",
        "Se han aplicado redes neuronales convolucionales para visión artificial.",
        "Se han aplicado técnicas de transfer learning.",
        "Se han evaluado y comparado distintas arquitecturas de redes neuronales.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han seleccionado las métricas de evaluación adecuadas al tipo de problema.",
        "Se ha aplicado la validación cruzada para estimar el rendimiento del modelo.",
        "Se han identificado y tratado problemas de sobreajuste y subajuste.",
        "Se ha optimizado el modelo mediante búsqueda de hiperparámetros.",
        "Se ha utilizado una herramienta de seguimiento de experimentos (MLflow).",
    ], start=1)],
}

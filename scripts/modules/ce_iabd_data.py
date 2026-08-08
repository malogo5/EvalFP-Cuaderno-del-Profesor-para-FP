"""EvalFP — Sistemas de Aprendizaje Automático · 5072 · CE Inteligencia Artificial y Big Data
Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 100 h · 3 h/semana · CE IA y Big Data.
"""
MODULO = {
    "nombre":"Sistemas de Aprendizaje Automático","codigo":"5072","abrev":"SAA",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IA y Big Data","horas_sem":3,"total_horas":100,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022, NID 2022/6683) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Caracteriza la Inteligencia Artificial fuerte y débil determinando…","horas":19,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Determina técnicas y herramientas de sistemas de aprendizaje…","horas":16,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Aplica algoritmos de aprendizaje supervisado","horas":25,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Aplica técnicas de aprendizaje no supervisado","horas":12,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica modelos computacionales de redes neuronales comparándolos con…","horas":12,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Valora la calidad de los resultados obtenidos en la práctica con…","horas":16,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":19,"nombre":"Caracteriza la Inteligencia Artificial fuerte y débil determinando usos y posibilidades."},
    {"id":"RA2","pond":16,"nombre":"Determina técnicas y herramientas de sistemas de aprendizaje automático (Machine Learning), testeando su aplicabilidad para la resolución de problemas."},
    {"id":"RA3","pond":25,"nombre":"Aplica algoritmos de aprendizaje supervisado, optimizando el resultado del modelo y minimizando los riesgos asociados."},
    {"id":"RA4","pond":12,"nombre":"Aplica técnicas de aprendizaje no supervisado relacionándolas con los tipos de problemas que tratan de resolver."},
    {"id":"RA5","pond":12,"nombre":"Aplica modelos computacionales de redes neuronales comparándolos con otros métodos de inteligencia artificial."},
    {"id":"RA6","pond":16,"nombre":"Valora la calidad de los resultados obtenidos en la práctica con sistemas de aprendizaje automático integrando principios fundamentales de la computación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","proyecto"],
    "RA2":["practica","proyecto"],
    "RA3":["practica","proyecto"],
    "RA4":["practica","proyecto"],
    "RA5":["practica","proyecto"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado las especificidades de Inteligencia Artificial fuerte y débil.",
        "Se han establecido las barreras entre la Inteligencia Artificial y el aprendizaje automático (Machine Learning).",
        "Se han diferenciado ámbitos de aplicación de la Inteligencia Artificial fuerte y débil.",
        "Se han identificado los problemas a los que puede hacer frente la Inteligencia Artificial débil.",
        "Se han identificado los problemas a los que puede hacer frente la Inteligencia Artificial fuerte.",
        "Se han reconocido las ventajas que proporciona cada tipo en la resolución de los problemas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principios de sistemas de aprendizaje automático.",
        "Se han determinado tipos y usos de sistemas de aprendizaje automático.",
        "Se han determinado técnicas y herramientas de sistemas de aprendizaje automático.",
        "Se han encontrado diferencias entre los tipos de sistemas de aprendizaje automático.",
        "Se han asociado técnicas y herramientas a cada tipo de sistemas de aprendizaje automático.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han proporcionado los datos etiquetados al modelo.",
        "Se han seleccionado los datos de entrada, ya sean para la fase de entrenamiento, fase de validación o fase de testeo de datos entre otras.",
        "Se han utilizado los datos en la fase de entrenamiento para la construcción del modelo aplicando características relevantes obtenidas.",
        "Se ha evaluado el modelo con los datos obtenidos en la fase de validación.",
        "Se han ajustado los datos de aprendizaje supervisado en la fase de ajuste para mejorar el rendimiento de las diferentes características o parámetros.",
        "Se ha implementado el modelo para realizar predicciones sobre nuevos datos.",
        "Se han detectado y minimizado los riesgos asociados al modelo.",
        "Se ha optimizado el modelo de aprendizaje supervisado validando datos de prueba.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han caracterizado los tipos de problemas que el aprendizaje no supervisado trata de resolver.",
        "Se han caracterizado las técnicas de aprendizaje no supervisado utilizadas para la resolución de dichos tipos de problemas.",
        "Se han aplicado algoritmos utilizados en el aprendizaje no supervisado.",
        "Se ha optimizado el modelo de aprendizaje no supervisado validando datos de prueba.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado los modelos neuronales para elegir el más adecuado para cada clase de problema.",
        "Se han aplicado técnicas de aprendizaje profundo (deep learning) para entrenar redes de neuronas.",
        "Se han comparado las redes de neuronas artificiales con otros métodos de inteligencia artificial.",
        "Se ha reconocido una red de neuronas entrenada a partir de un conjunto de datos.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la conveniencia de los algoritmos propuestos para dar solución a los problemas planteados.",
        "Se ha evaluado la aplicación práctica de los principios y técnicas básicas de los sistemas inteligentes.",
        "Se han integrado los principios fundamentales de la computación en la práctica para seleccionar, valorar y crear nuevos desarrollos tecnológicos.",
        "Se han desarrollado sistemas y aplicaciones informáticas que utilizan técnicas de los sistemas inteligentes.",
        "Se han desarrollado técnicas de aprendizaje computacional dedicadas a la extracción automática de información a partir de grandes volúmenes de datos.",
    ], start=1)],
}

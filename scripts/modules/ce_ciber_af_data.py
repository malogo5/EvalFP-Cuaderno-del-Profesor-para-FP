"""EvalFP — Análisis Forense Informático · 5024 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 120 h · 4 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Análisis Forense Informático","codigo":"5024","abrev":"AFI",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Aplica metodologías de análisis forense caracterizando las fases de…","horas":26,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Realiza análisis forenses en dispositivos móviles","horas":15,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Realiza análisis forenses en Cloud","horas":23,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Realiza análisis forense en dispositivos del IoT","horas":34,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Documenta análisis forenses elaborando informes que incluyan la…","horas":22,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":22,"nombre":"Aplica metodologías de análisis forense caracterizando las fases de preservación, adquisición, análisis y documentación."},
    {"id":"RA2","pond":12,"nombre":"Realiza análisis forenses en dispositivos móviles, aplicando metodologías establecidas, actualizadas y reconocidas."},
    {"id":"RA3","pond":19,"nombre":"Realiza análisis forenses en Cloud, aplicando metodologías establecidas, actualizadas y reconocidas."},
    {"id":"RA4","pond":28,"nombre":"Realiza análisis forense en dispositivos del IoT, aplicando metodologías establecidas, actualizadas y reconocidas."},
    {"id":"RA5","pond":19,"nombre":"Documenta análisis forenses elaborando informes que incluyan la normativa aplicable."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
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
        "Se han identificado los dispositivos a analizar para garantizar la preservación de evidencias.",
        "Se han utilizado los mecanismos y las herramientas adecuadas para la adquisición y extracción de las evidencias.",
        "Se ha asegurado la escena y conservado la cadena de custodia.",
        "Se ha documentado el proceso realizado de manera metódica.",
        "Se ha considerado la línea temporal de las evidencias.",
        "Se ha elaborado un informe de conclusiones a nivel técnico y ejecutivo.",
        "Se han presentado y expuesto las conclusiones del análisis forense realizado.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha realizado el proceso de toma de evidencias en un dispositivo móvil.",
        "Se han extraído, decodificado y analizado las pruebas conservando la cadena de custodia.",
        "Se han generado informes de datos móviles, cumpliendo con los requisitos de la industria forense de telefonía móvil.",
        "Se han presentado y expuesto las conclusiones del análisis forense realizado a quienes proceda.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha desarrollado una estrategia de análisis forense en Cloud, asegurando la disponibilidad de los recursos y capacidades necesarios una vez ocurrido el incidente.",
        "Se ha conseguido identificar las causas, el alcance y el impacto real causado por el incidente.",
        "Se han realizado las fases del análisis forense en Cloud.",
        "Se han identificado las características intrínsecas de la nube (elasticidad, ubicuidad, abstracción, volatilidad y compartición de recursos).",
        "Se han cumplido los requerimientos legales en vigor, RGPD (Reglamento general de protección de datos) y directiva NIS (Directiva de la UE sobre seguridad de redes y sistemas de información) o las que eventualmente pudieran sustituirlas.",
        "Se han presentado y expuesto las conclusiones del análisis forense realizado.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los dispositivos a analizar garantizando la preservación de las evidencias.",
        "Se han utilizado mecanismos y herramientas adecuadas para la adquisición y extracción de evidencias",
        "Se ha garantizado la autenticidad, completitud, fiabilidad y legalidad de las evidencias extraídas.",
        "Se han realizado análisis de evidencias de manera manual y mediante herramientas.",
        "Se ha documentado el proceso de manera metódica y detallada.",
        "Se ha considerado la línea temporal de las evidencias.",
        "Se ha mantenido la cadena de custodia",
        "Se ha elaborado un informe de conclusiones a nivel técnico y ejecutivo.",
        "Se han presentado y expuesto las conclusiones del análisis forense realizado.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido el objetivo del informe pericial y su justificación.",
        "Se ha definido el ámbito de aplicación del informe pericial.",
        "Se han documentado los antecedentes.",
        "Se han recopilado las normas legales y reglamentos cumplidos en el análisis forense realizado.",
        "Se han recogido los requisitos establecidos por el cliente.",
        "Se han incluido las conclusiones y su justificación.",
    ], start=1)],
}

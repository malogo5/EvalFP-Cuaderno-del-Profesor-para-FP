"""EvalFP — Digitalización aplicada a los sectores productivos (GM) · 1664 · Sistemas Microinformáticos y Redes
Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VI del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 50 h · 2 h/semana · 1º SMR.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Digitalización aplicada a los sectores productivos (GM)","codigo":"1664","abrev":"DIG",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":2,"total_horas":50,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo VI del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Establece las diferencias entre la Economía Lineal (EL) y la…","horas":9,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Caracteriza los principales aspectos de la 4.ª Revolución…","horas":9,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Identifica la estructura de los sistemas basados en…","horas":8,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Compara los sistemas de producción/prestación de servicios…","horas":12,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Elabora un plan de transformación de una empresa clásica del…","horas":12,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Establece las diferencias entre la Economía Lineal (EL) y la Economía Circular (EC), identificando las ventajas de la EC en relación con el medioambiente y el desarrollo sostenible."},
    {"id":"RA2","pond":18,"nombre":"Caracteriza los principales aspectos de la 4.ª Revolución Industrial indicando los cambios y las ventajas que se producen tanto desde el punto de vista de los clientes como de las empresas."},
    {"id":"RA3","pond":15,"nombre":"Identifica la estructura de los sistemas basados en cloud/nube describiendo su tipología y campo de aplicación."},
    {"id":"RA4","pond":25,"nombre":"Compara los sistemas de producción/prestación de servicios digitalizados con los sistemas clásicos identificando las mejoras introducidas."},
    {"id":"RA5","pond":24,"nombre":"Elabora un plan de transformación de una empresa clásica del sector en el que se enmarca el título, basada en una EL, al concepto 4.0, determinando los cambios a introducir en las principales fases del sistema e indicando como afectaría a los recursos humanos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
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
        "Se han identificado las etapas «típicas» de los modelos basados en EL y modelos basados en EC.",
        "Se ha analizado cada etapa de los modelos EL y EC y su repercusión en el medio ambiente.",
        "Se ha valorado la importancia del reciclaje en los modelos económicos.",
        "Se han identificado procesos reales basados en EL.",
        "Se han identificado procesos reales basados en EC.",
        "Se han comparado los modelos anteriores en relación con su impacto medioambiental y los ODS (Objetivos de Desarrollo Sostenible).",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han relacionado los sistemas ciber físicos con la evolución industrial.",
        "Se ha analizado el cambio producido en los sistemas automatizados.",
        "Se ha descrito la combinación de la parte física de las industrias con el software, IoT (Internet de las cosas), comunicaciones, entre otros.",
        "Se ha descrito la interrelación entre el mundo físico y el virtual.",
        "Se ha relacionado la migración a entornos 4.0 con la mejora de los resultados de las empresas.",
        "Se han identificado las ventajas para clientes y empresas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes niveles de la cloud/nube.",
        "Se han identificado las principales funciones de la cloud/nube (procesamiento de datos, intercambio de información, ejecución de aplicaciones, entre otros).",
        "Se ha descrito el concepto de edge computing y su relación con la cloud/nube.",
        "Se han definido los conceptos de fog y mist y sus zonas de aplicación en el conjunto.",
        "Se han identificado las ventajas que proporciona la utilización de la cloud/nube en los sistemas conectados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las tecnologías habilitadoras (THD) actuales que definen un sistema digitalizado.",
        "Se han descrito las características y aplicaciones del IoT, IA (Inteligencia Artificial), Big Data, tecnología 5G, la robótica colaborativa, Blockchain, Ciberseguridad, fabricación aditiva, realidad virtual, gemelos digitales, entre otras.",
        "Se ha descrito la contribución de las THD a la mejora de la productividad y la eficiencia de los sistemas productivos o de prestación de servicios.",
        "Se ha relacionado la alineación entre las unidades funcionales de las empresas que conforman el sistema y el objetivo del mismo.",
        "Se ha relacionado la implantación de las tecnologías habilitadoras (sensórica, tratamiento de datos, automatización y comunicaciones, entre otras) con la reducción de costes y la mejora de la competitividad.",
        "Se han relacionado las tecnologías disruptivas con aplicaciones concretas en los sectores productivos.",
        "Se han definido los sistemas de almacenamiento de datos no convencionales y el acceso a los mismos desde cada unidad.",
        "Se han descrito las mejoras producidas en el sistema y en cada una de sus etapas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido a nivel de bloques el diagrama de funcionamiento de la empresa clásica.",
        "Se han identificado las etapas susceptibles de ser digitalizadas.",
        "Se han definido las tecnologías implicadas en cada una de las etapas.",
        "Se ha establecido la conexión de las etapas digitalizadas con el resto del sistema.",
        "Se ha elaborado un diagrama de bloques del sistema digitalizado.",
        "Se ha elaborado un informe de viabilidad y de las mejoras introducidas.",
        "Se ha analizado la mejora en la producción y gestión de residuos, entre otras.",
        "Se ha elaborado un documento con la secuencia del plan de transformación y los recursos empleados.",
    ], start=1)],
}

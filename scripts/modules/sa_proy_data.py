"""EvalFP — Proyecto intermodular de aprendizaje colaborativo · 3160 · Servicios Administrativos
Horas, curso y h/semana: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo I del Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024) (por remisión expresa del Decreto 78/2024, Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024))
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 55 h · 1 h/semana · 2º SA.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Proyecto intermodular de aprendizaje colaborativo","codigo":"3160","abrev":"PROY",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"2º SA","horas_sem":1,"total_horas":55,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas, curso y h/semana: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo I del Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024) (por remisión expresa del Decreto 78/2024, Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024))",
}
UTS = [
    {"id":"UT1","nombre":"Busca información en internet sobre empresas «tipo» del…","horas":19,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Selecciona un servicio o producto de una empresa del sector…","horas":10,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Hace una propuesta de una empresa tipo «spin off» indicando…","horas":10,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Relaciona cada unidad de una empresa tipo con la prevención…","horas":8,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Transmite información con claridad de manera ordenada y…","horas":8,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":33,"nombre":"Busca información en internet sobre empresas «tipo» del sector/es relacionados con los estándares (unidades) de competencia incluidos en el ámbito profesional del título, elaborando un mapa de las mismas y los servicios o productos que ofrecen."},
    {"id":"RA2","pond":19,"nombre":"Selecciona un servicio o producto de una empresa del sector relacionándolo con su contribución a los ODS y sus destinatarios a nivel global."},
    {"id":"RA3","pond":18,"nombre":"Hace una propuesta de una empresa tipo «spin off» indicando los aspectos diferenciales con la empresa de referencia y elaborando un dossier con sus características."},
    {"id":"RA4","pond":15,"nombre":"Relaciona cada unidad de una empresa tipo con la prevención de riesgos profesionales identificando los equipos/sistemas de protección generales y los propios de cada actividad."},
    {"id":"RA5","pond":15,"nombre":"Transmite información con claridad de manera ordenada y estructurada."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4"]),
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
        "Se ha elaborado conjuntamente un esquema que contemple el conjunto de las empresas tipo del sector.",
        "Se han constituido equipos de trabajo y se han distribuido entre los grupos las empresas que se analizarán.",
        "Se ha identificado para la empresa seleccionada los productos o servicios que ofrece.",
        "Se han relacionado los productos o servicios ofertados con la consecución de los ODS (Objetivos de Desarrollo Sostenible).",
        "Se ha realizado un diagrama de bloques de los posibles departamentos que conforman la empresa.",
        "Se han tenido en cuenta las áreas transversales y su relación con las demás.",
        "Se ha presentado al gran grupo la configuración de la empresa y productos que ofrece.",
        "Se ha hecho una valoración de los recursos necesarios para cada unidad.",
        "Se ha elaborado un informe en un formato establecido con la información recabada, indicando al menos: el sector en el que se encuadra, los principales países donde opera, y las áreas de las que se compone.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha seleccionado un producto/servicio de la empresa a estudio.",
        "Se ha discutido en grupo con qué ODS pueda estar relacionado.",
        "Se han identificado las características del público objetivo al que está destinado.",
        "Se ha comparado el producto con otros de empresas similares.",
        "Se ha desarrollado una propuesta innovadora para potenciar el producto o servicio.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha planteado en el grupo el concepto de una empresa tipo «spin off», indicando sus ventajas e inconvenientes.",
        "Se ha discutido en grupo con qué ODS pueda estar relacionado.",
        "Se ha propuesto una posible organización de la empresa, atendiendo a una estructura lineal o circular.",
        "Se han indicado que tecnologías se incluirían para aumentar su competitividad.",
        "Se han propuesto aspectos innovadores sobre algún producto de la empresa de referencia.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado la responsabilidad de la empresa y los trabajadores en la consecución de entornos de trabajo seguros.",
        "Se han identificado los sistemas de protección generales e individuales de cada unidad en función de las actividades a realizar.",
        "Se ha estimado el coste de los elementos de protección individual.",
        "Se han propuesto posibles elementos de mejora en relación con la seguridad.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha mantenido una actitud ordenada y metódica en la transmisión de la información.",
        "Se ha transmitido información verbal tanto horizontal como verticalmente.",
        "Se ha transmitido información entre los miembros del grupo utilizando medios informáticos.",
        "Se han conocido los términos técnicos en otras lenguas que sean estándares del sector.",
    ], start=1)],
}

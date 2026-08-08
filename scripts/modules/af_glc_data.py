"""EvalFP — Gestión logística y comercial · 0655 · Administración y Finanzas
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 117 h · 3 h/semana · 2º AF.
"""
MODULO = {
    "nombre":"Gestión logística y comercial","codigo":"0655","abrev":"GLC",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"2º AF","horas_sem":3,"total_horas":117,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Planificación del aprovisionamiento","horas":27,"eval":1,"tags":"Previsión de demanda · Necesidades · Stocks · Costes"},
    {"id":"UT2","nombre":"Selección de proveedores","horas":22,"eval":1,"tags":"Solicitud de ofertas · Baremos · Cuadros comparativos · Homologación"},
    {"id":"UT3","nombre":"Negociación y relaciones con proveedores","horas":22,"eval":1,"tags":"Técnicas de negociación · Condiciones · Comunicación · Acuerdos"},
    {"id":"UT4","nombre":"Seguimiento y control del aprovisionamiento","horas":24,"eval":2,"tags":"Pedido · Recepción · Incidencias · Indicadores · Reclamaciones"},
    {"id":"UT5","nombre":"La cadena logística","horas":22,"eval":2,"tags":"Fases · Almacenaje · Transporte · Trazabilidad · Calidad y costes"},
]
RAS = [
    {"id":"RA1","pond":23,"nombre":"Elabora planes de aprovisionamiento, analizando información de las distintas áreas de la organización o empresa."},
    {"id":"RA2","pond":19,"nombre":"Realiza procesos de selección de proveedores, analizando las condiciones técnicas y los parámetros habituales."},
    {"id":"RA3","pond":19,"nombre":"Planifica la gestión de las relaciones con los proveedores, aplicando técnicas de negociación y comunicación."},
    {"id":"RA4","pond":21,"nombre":"Programa el seguimiento documental y los controles del proceso de aprovisionamiento, aplicando los mecanismos previstos en el programa y utilizando aplicaciones informáticas."},
    {"id":"RA5","pond":18,"nombre":"Define las fases y operaciones que deben realizarse dentro de la cadena logística, asegurándose la trazabilidad y calidad en el seguimiento de la mercancía."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","examen"],
    "RA3":["practica"],
    "RA4":["practica","examen"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido las fases que componen un programa de aprovisionamiento desde la detección de necesidades hasta la recepción de la mercancía.",
        "Se han determinado los principales parámetros que configuran un programa de aprovisionamiento que garantice la calidad y el cumplimiento del nivel de servicio establecido.",
        "Se han obtenido las previsiones de venta y/o demanda del periodo de cada departamento implicado.",
        "Se han contrastado los consumos históricos, lista de materiales y/o pedidos realizados, en función del cumplimiento de los objetivos del plan de ventas y/o producción previsto por la empresa/organización.",
        "Se ha calculado el coste del programa de aprovisionamiento, diferenciando los elementos que lo componen.",
        "Se ha determinado la capacidad óptima de almacenamiento de la organización, teniendo en cuenta la previsión de stocks.",
        "Se han elaborado las órdenes de suministro de materiales con fecha, cantidad y lotes, indicando el momento y destino/ubicación del suministro al almacén y/o a las unidades productivas precedentes.",
        "Se ha previsto con tiempo suficiente el reaprovisionamiento de la cadena de suministro para ajustar los volúmenes de stock al nivel de servicio, evitando los desabastecimientos.",
        "Se han realizado las operaciones anteriores mediante una aplicación informática de gestión de stocks y aprovisionamiento.",
        "Se ha asegurado la calidad del proceso de aprovisionamiento, estableciendo procedimientos normalizados de gestión de pedidos y control del proceso.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las fuentes de suministro y búsqueda de proveedores.",
        "Se ha confeccionado un fichero con los proveedores potenciales, de acuerdo con los criterios de búsqueda “online” y “off-line”.",
        "Se han realizado solicitudes de ofertas y pliego de condiciones de aprovisionamiento.",
        "Se han recopilado las ofertas de proveedores que cumplan con las condiciones establecidas, para su posterior evaluación.",
        "Se han definido los criterios esenciales en la selección de ofertas de proveedores: económicos, plazo de aprovisionamiento, calidad, condiciones de pago y servicio, entre otros.",
        "Se han comparado las ofertas de varios proveedores de acuerdo con los parámetros de precio, calidad y servicio.",
        "Se ha establecido un baremo de los criterios de selección en función del peso específico que, sobre el total, representa cada una de las variables consideradas.",
        "Se han realizado las operaciones anteriores mediante una aplicación informática de gestión de proveedores.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han relacionado las técnicas más utilizadas en la comunicación con proveedores.",
        "Se han detectado las ventajas, los costes y los requerimientos técnicos y comerciales de implantación de un sistema de intercambio electrónico de datos, en la gestión del aprovisionamiento.",
        "Se han elaborado escritos de forma clara y concisa de las solicitudes de información a los proveedores.",
        "Se han preparado previamente las conversaciones personales o telefónicas con los proveedores.",
        "Se han identificado los distintos tipos de documentos utilizados para el intercambio de información con proveedores.",
        "Se han explicado las diferentes etapas en un proceso de negociación de condiciones de aprovisionamiento.",
        "Se han descrito las técnicas de negociación más utilizadas en la compra, venta y aprovisionamiento.",
        "Se ha elaborado un informe que recoja los acuerdos de la negociación, mediante el uso de los programas informáticos adecuados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha secuenciado el proceso de control que deben seguir los pedidos realizados a un proveedor en el momento de recepción en el almacén.",
        "Se han definido los indicadores de calidad y eficacia operativa en la gestión de proveedores.",
        "Se han detectado las incidencias más frecuentes del proceso de aprovisionamiento.",
        "Se han establecido las posibles medidas que se deben adoptar ante las anomalías en la recepción de un pedido.",
        "Se han definido los aspectos que deben figurar en los documentos internos de registro y control del proceso de aprovisionamiento.",
        "Se han elaborado informes de evaluación de proveedores de manera clara y estructurada.",
        "Se ha elaborado la documentación relativa al control, registro e intercambio de información con proveedores, siguiendo los procedimientos de calidad y utilizando aplicaciones informáticas.",
        "Se han determinado los flujos de información, relacionando los departamentos de una empresa y los demás agentes logísticos que intervienen en la actividad de aprovisionamiento.",
        "Se han enlazado las informaciones de aprovisionamiento, logística y facturación con otras áreas de información de la empresa, como contabilidad y tesorería.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características básicas de la cadena logística, identificando las actividades, fases y agentes que participan y las relaciones entre ellos.",
        "Se han interpretado los diagramas de flujos físicos de mercancías, de información y económicos en las distintas fases de la cadena logística.",
        "Se han descrito los costes logísticos directos e indirectos, fijos y variables, considerando todos los elementos de una operación logística y las responsabilidades imputables a cada uno de los agentes de la cadena logística.",
        "Se han valorado las distintas alternativas en los diferentes modelos o estrategias de distribución de mercancías.",
        "Se han establecido las operaciones sujetas a la logística inversa y se ha determinado el tratamiento que se debe dar a las mercancías retornadas, para mejorar la eficiencia de la cadena logística.",
        "Se ha asegurado la satisfacción del cliente resolviendo imprevistos, incidencias y reclamaciones en la cadena logística.",
        "Se han realizado las operaciones anteriores mediante una aplicación informática de gestión de proveedores.",
        "Se ha valorado la responsabilidad corporativa en la gestión de residuos, desperdicios, devoluciones caducadas y embalajes, entre otros.",
    ], start=1)],
}

"""EvalFP — Preparación de pedidos y venta de productos · 3006 · Servicios Administrativos
Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 173 h · 4 h/semana · 2º SA.
"""
MODULO = {
    "nombre":"Preparación de pedidos y venta de productos","codigo":"3006","abrev":"PPVP",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"2º SA","horas_sem":4,"total_horas":173,"anno":"2026-2027","eval_count":3,
    "horas_aula":100,  # el resto hasta 173 h es formación en empresa
    "decreto":"Decreto 83/2014, de 01/08/2014 (DOCM, NID 2014/10286), Anexo II · distribución horaria LOFP vigente publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Asesoramiento y venta de productos","horas":23,"eval":1,"tags":"Características del producto · Argumentación · Cierre de la venta · Cobro"},
    {"id":"UT2","nombre":"Formación de pedidos","horas":27,"eval":2,"tags":"Documento de pedido · Medición y pesaje · Unidades · Comprobación"},
    {"id":"UT3","nombre":"Embalaje, etiquetado y expedición","horas":27,"eval":2,"tags":"Embalaje manual y automático · Etiquetado · Paletización · Documentación de transporte"},
    {"id":"UT4","nombre":"Atención de reclamaciones en la venta","horas":23,"eval":3,"tags":"Situaciones posibles · Protocolo de actuación · Devoluciones · Registro"},
]
RAS = [
    {"id":"RA1","pond":23,"nombre":"Atiende a posibles clientes asesorándoles sobre las características de los productos solicitados y seleccionando las mercancías requeridas de acuerdo con las instrucciones establecidas."},
    {"id":"RA2","pond":27,"nombre":"Conforma pedidos de acuerdo con los requerimientos de posibles clientes, aplicando técnicas de medición y pesado mediante herramientas manuales y terminales específicos."},
    {"id":"RA3","pond":27,"nombre":"Prepara pedidos para su expedición aplicando procedimientos manuales y automáticos de embalaje y etiquetado mediante equipos específicos."},
    {"id":"RA4","pond":23,"nombre":"Atiende reclamaciones de potenciales clientes identificando las situaciones posibles y aplicando los protocolos correspondientes."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1"], 2:["RA2","RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las fases del proceso de atención a clientes y preparación de pedidos en comercios, grandes superficies, almacenes y empresas o departamentos de logística.",
        "Se han aplicado técnicas de comunicación adecuadas al público objetivo del punto de venta, adaptando la actitud y discurso a la situación de la que se parte, obteniendo la información necesaria del posible cliente.",
        "Se han dado respuestas a preguntas de fácil solución, utilizando el léxico comercial adecuado.",
        "Se ha mantenido una actitud conciliadora y sensible con los demás, demostrando cordialidad y amabilidad en el trato, transmitiendo la información con claridad, de manera ordenada, estructurada y precisa.",
        "Se ha informado al posible cliente de las características de los productos, especialmente de las calidades esperables, formas de uso y consumo, argumentando sobre sus ventajas y comunicando el periodo de garantía.",
        "Se han relacionado las operaciones de cobro y devolución con la documentación de las posibles transacciones.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han aplicado las recomendaciones básicas de conservación y embalaje de pedidos de mercancías o productos interpretando la simbología relacionada.",
        "Se ha interpretado la información contenida en órdenes de pedido tipo, cumplimentando los documentos relacionados, tales como hojas de pedido, albaranes, órdenes de reparto, packing list, entre otras.",
        "Se han descrito los daños que pueden sufrir las mercancías/productos durante su manipulación para la conformación y preparación de pedidos.",
        "Se han descrito las características de un TPV y los procedimientos para la utilización de medios de pago electrónicos.",
        "Se han realizado operaciones de pesado y medido con los equipos y herramientas requeridos.",
        "Se han identificado los documentos de entrega asociados a la venta y a las devoluciones, realizando, en su caso, cierres de caja.",
        "Se han aplicado las normas básicas de prevención de riesgos laborales, relacionados con la manipulación de mercancías/productos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los pasos y procedimientos generales para la preparación de pedidos (selección, agrupamiento, etiquetado y presentación final).",
        "Se han identificado los principales tipos de envases y embalajes, relacionándolos con las características físicas y técnicas de los productos o mercancías que contienen.",
        "Se han utilizado los criterios de etiquetado establecidos, consignando, en su caso, el número de unidades, medida y/o peso de los productos o mercancías embaladas.",
        "Se han tomado las medidas oportunas para minimizar y reducir los residuos generados por los procesos de embalaje.",
        "Se ha manejado con la precisión requerida los equipos de pesaje y/o conteo manual y/o mecánico, utilizando las unidades de medida y peso especificadas en las órdenes de pedido.",
        "Se han aplicado las medidas y normas de seguridad, higiene y salud establecidas.",
        "Se han retirando los residuos generados en la preparación y embalaje.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las funciones del servicio de atención al cliente.",
        "Se han identificado los procedimientos para tratar las reclamaciones y los documentos asociados (formularios de reclamaciones, hojas de reclamaciones, cartas, entre otros)",
        "Se han reconocido los aspectos principales en los que incide la legislación vigente, en relación con las reclamaciones.",
        "Se han ofrecido alternativas al cliente ante reclamaciones fácilmente subsanables, exponiendo claramente los tiempos y condiciones de las operaciones a realizar, así como del nivel de probabilidad de modificación esperable.",
        "Se ha suministrado la información y la documentación necesaria al cliente para la presentación de una reclamación escrita, si éste fuera el caso.",
        "Se han recogido los formularios presentados por el cliente para la realización de una reclamación, clasificándolos y transmitiendo su información al responsable de su tratamiento.",
    ], start=1)],
}

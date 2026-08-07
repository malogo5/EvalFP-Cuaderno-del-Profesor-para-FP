"""EvalFP — Operaciones administrativas de compra-venta · 0438 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 135 h · 4 h/semana · 1º GA.
"""
MODULO = {
    "nombre":"Operaciones administrativas de compra-venta","codigo":"0438","abrev":"OACV",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"1º GA","horas_sem":4,"total_horas":135,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"Cálculo comercial","horas":28,"eval":1,"tags":"Precios de compra y venta · Márgenes · Descuentos · IVA · Recargo de equivalencia"},
    {"id":"UT2","nombre":"Documentación de compraventa","horas":32,"eval":1,"tags":"Pedido · Albarán · Factura · Factura electrónica · Facturas rectificativas · Archivo"},
    {"id":"UT3","nombre":"IVA y obligaciones fiscales","horas":22,"eval":2,"tags":"Regímenes de IVA · Libros registro · Modelos 303 y 390 · Presentación telemática"},
    {"id":"UT4","nombre":"Gestión de almacén y existencias","horas":28,"eval":2,"tags":"Fichas de almacén · PMP y FIFO · Inventario · Stock mínimo · Valoración de existencias"},
    {"id":"UT5","nombre":"Cobros y pagos","horas":25,"eval":3,"tags":"Efectivo · Transferencia · Cheque · Pagaré · Letra de cambio · Domiciliación"},
]
RAS = [
    {"id":"RA1","pond":21,"nombre":"Calcula precios de venta y compra y descuentos aplicando las normas y usos mercantiles y la legislación fiscal vigente."},
    {"id":"RA2","pond":23,"nombre":"Confecciona documentos administrativos de las operaciones de compraventa, relacionándolos con las transac - ciones comerciales de la empresa."},
    {"id":"RA3","pond":16,"nombre":"Liquida obligaciones fiscales ligadas a las operaciones de compra-venta aplicando la normativa fiscal vigente."},
    {"id":"RA4","pond":21,"nombre":"Controla existencias reconociendo y aplicando sistemas de gestión de almacén."},
    {"id":"RA5","pond":19,"nombre":"Tramita pagos y cobros reconociendo la documentación asociada y su flujo dentro de la empresa."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","examen"],
    "RA3":["examen","practica"],
    "RA4":["practica","examen"],
    "RA5":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las funciones del departamento de ventas o comercial y las del de compras.",
        "Se han reconocido los tipos de mercados, de clientela y de productos o servicios.",
        "Se han descrito los circuitos de los documentos de compraventa.",
        "Se han identificado los conceptos de precio de compra del producto, gastos, precio de venta, descuentos, interés comercial, recargos y márgenes comerciales.",
        "Se han distinguido los conceptos de comisiones y corretajes.",
        "Se han reconocido los porcentajes de IVA a aplicar en las operaciones de compraventa.",
        "Se han clasificado los tipos de descuento más habituales.",
        "Se han reconocido y cuantificado los gastos de compra o venta.",
        "Se han identificado los métodos para calcular el precio final de venta y los precios unitarios.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los documentos básicos de las operaciones de compraventa, precisando los requisitos forma - les que deben reunir.",
        "Se ha reconocido el contrato mercantil de compraventa.",
        "Se han descrito los flujos de documentación administrativa relacionados con la compra y venta, habituales en la empresa.",
        "Se ha identificado el proceso de recepción de pedidos y su posterior gestión.",
        "Se han cumplimentado los documentos relativos a la compra y venta en la empresa",
        "Se han comprobado la coherencia interna de los documentos, trasladando las copias a los departamentos corres - pondientes.",
        "Se han reconocido los procesos de expedición y entrega de mercancías.",
        "Se ha verificado que la documentación comercial, recibida y emitida, cumple con la legislación vigente y con los procedimientos internos de la empresa.",
        "Se han identificado los parámetros y la información que deben ser registrados en las operaciones de compraven - ta.",
        "Se ha valorado la necesidad de aplicar los sistemas de protección y salvaguarda de la información, así como cri - terios de calidad en el proceso administrativo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características básicas de las normas mercantiles y fiscales aplicables a las operaciones de compra-venta.",
        "Se han identificado las obligaciones de registro en relación con el Impuesto del Valor Añadido (IVA).",
        "Se han identificado los libros-registro obligatorios para las empresas.",
        "Se han identificado los libros-registro voluntarios para las empresas.",
        "Se ha identificado la obligación de presentar declaraciones trimestrales y resúmenes anuales en relación con el Impuesto del Valor Añadido (IVA).",
        "Se han identificado las obligaciones informativas a Hacienda en relación con las operaciones efectuadas periódi - camente.",
        "Se ha reconocido la normativa sobre la conservación de documentos e información.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado los diferentes tipos de existencias habituales en empresas de producción, comerciales y de servicios.",
        "Se han diferenciado los tipos de embalajes y envases que se utilizan.",
        "Se han descrito los procedimientos administrativos de recepción, almacenamiento, distribución interna y expedi - ción de existencias.",
        "Se han calculado los precios unitarios de coste de las existencias, teniendo en cuenta los gastos correspondien - tes.",
        "Se han identificado los métodos de control de existencias.",
        "Se han reconocido los conceptos de stock mínimo y stock óptimo.",
        "Se han identificado los procedimientos internos para el lanzamiento de pedidos a los proveedores.",
        "Se ha valorado la importancia de los inventarios periódicos.",
        "Se han utilizado las aplicaciones informáticas y procesos establecidos en la empresa para la gestión del alma - cén.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los medios de pago y cobro habituales en la empresa.",
        "Se han cumplimentado los documentos financieros utilizados y los impresos de cobro y pago.",
        "Se han valorado los procedimientos de autorización de los pagos.",
        "Se han valorado los procedimientos de gestión de los cobros.",
        "Se han reconocido los documentos de justificación del pago.",
        "Se han diferenciado el pago al contado y el pago aplazado.",
        "Se han identificado las características básicas y el funcionamiento de los pagos por Internet.",
        "Se han analizado las formas de financiación comercial más usuales.",
    ], start=1)],
}

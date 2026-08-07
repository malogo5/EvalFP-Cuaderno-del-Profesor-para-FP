"""EvalFP — Proceso integral de la actividad comercial · 0650 · Asistencia a la Dirección
Decreto 41/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9482), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 205 h · 6 h/semana · 1º AD.
"""
MODULO = {
    "nombre":"Proceso integral de la actividad comercial","codigo":"0650","abrev":"PIAC",
    "ciclo":"Asistencia a la Dirección","ciclo_clave":"AD","ciclo_nivel":"CFGS",
    "curso":"1º AD","horas_sem":6,"total_horas":205,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 41/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9482), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"El patrimonio empresarial","horas":24,"eval":1,"tags":"Activo · Pasivo · Patrimonio neto · Masas patrimoniales · Equilibrio"},
    {"id":"UT2","nombre":"Metodología contable y PGC de PYMES","horas":31,"eval":1,"tags":"Partida doble · Cuentas · Diario y mayor · Marco conceptual · Normas de valoración"},
    {"id":"UT3","nombre":"Tributación de la actividad comercial","horas":31,"eval":2,"tags":"IVA · IRPF · Impuesto de Sociedades · Modelos y plazos · Presentación telemática"},
    {"id":"UT4","nombre":"Documentación de compraventa","horas":31,"eval":2,"tags":"Pedido · Albarán · Factura · Facturación electrónica · Archivo"},
    {"id":"UT5","nombre":"Gestión de cobros y pagos","horas":20,"eval":2,"tags":"Medios de pago · Efectos comerciales · Vencimientos · Impagados"},
    {"id":"UT6","nombre":"Registro contable del ciclo comercial","horas":34,"eval":3,"tags":"Compras y ventas · Existencias · Gastos e ingresos · Regularización · Cierre"},
    {"id":"UT7","nombre":"Control de tesorería con aplicaciones informáticas","horas":34,"eval":3,"tags":"Previsión de tesorería · Conciliación bancaria · Software contable · Informes"},
]
RAS = [
    {"id":"RA1","pond":11,"nombre":"Determina los elementos patrimoniales de la empresa, analizando la actividad empresarial."},
    {"id":"RA2","pond":15,"nombre":"Integra la normativa contable y el método de la partida doble, analizando el PGC PYME y la metodología contable."},
    {"id":"RA3","pond":15,"nombre":"Gestiona la información sobre tributos que afectan o gravan la actividad comercial de la empresa, seleccionando y aplicando la normativa mercantil y fiscal vigente."},
    {"id":"RA4","pond":15,"nombre":"Elabora y organiza la documentación administrativa de las operaciones de compraventa, relacionándola con las transacciones comerciales de la empresa."},
    {"id":"RA5","pond":10,"nombre":"Determina los trámites de la gestión de cobros y pagos, analizando la documentación asociada y su flujo dentro de la empresa:"},
    {"id":"RA6","pond":17,"nombre":"Registra los hechos contables básicos derivados de la actividad comercial y dentro de un ciclo económico, aplicando la metodología contable y los principios y normas del PGC."},
    {"id":"RA7","pond":17,"nombre":"Efectúa la gestión y el control de la tesorería, utilizando aplicaciones informáticas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["practica","examen"],
    "RA5":["practica","examen"],
    "RA6":["examen","practica"],
    "RA7":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las fases del ciclo económico de la actividad empresarial.",
        "Se ha diferenciado entre inversión/financiación, inversión/gasto, gasto/pago e ingreso/cobro.",
        "Se han distinguido los distintos sectores económicos, basándose en la diversa tipología de actividades que se desarrollan en ellos.",
        "Se han definido los conceptos de patrimonio, elemento patrimonial y masa patrimonial.",
        "Se han identificado las masas patrimoniales que integran el activo, el pasivo exigible y el patrimonio neto.",
        "Se ha relacionado el patrimonio económico de la empresa con el patrimonio financiero y ambos con las fases del ciclo económico de la actividad empresarial.",
        "Se han clasificado un conjunto de elementos en masas patrimoniales.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han distinguido las fases del ciclo contable completo, adaptándolas a la legislación española.",
        "Se ha definido el concepto de cuenta como instrumento para representar los distintos elementos patrimoniales y hechos económicos de la empresa.",
        "Se han determinado las características más importantes del método de contabilización por partida doble.",
        "Se han reconocido los criterios de cargo y abono como método de registro de las modificaciones del valor de los elementos patrimoniales.",
        "Se ha definido el concepto de resultado contable, diferenciando las cuentas de ingresos y gastos.",
        "Se ha reconocido el PGC como instrumento de armonización contable.",
        "Se han relacionado las distintas partes del PGC, diferenciando las obligatorias de las no obligatorias.",
        "Se ha codificado un conjunto de elementos patrimoniales de acuerdo con los criterios del PGC, identificando su función en la asociación y desglose de la información contable.",
        "Se han identificado las cuentas anuales que establece el PGC, determinando la función que cumplen.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la normativa fiscal básica.",
        "Se han clasificado los tributos, identificando las características básicas de los más significativos.",
        "Se han identificado los elementos tributarios.",
        "Se han identificado las características básicas de las normas mercantiles y fiscales aplicables a las operaciones de compraventa.",
        "Se han distinguido y reconocido las operaciones sujetas, exentas y no sujetas a IVA.",
        "Se han diferenciado los regímenes especiales del IVA.",
        "Se han determinado las obligaciones de registro en relación con el Impuesto del Valor Añadido, así como los libros registros (voluntarios y obligatorios) para las empresas.",
        "Se han calculado las cuotas liquidables del impuesto y elaborado la documentación correspondiente a su declaración-liquidación.",
        "Se ha reconocido la normativa sobre la conservación de documentos e información.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado los elementos del contrato mercantil de compraventa.",
        "Se han establecido los flujos de documentación administrativa relacionados con la compraventa.",
        "Se han identificado y cumplimentado los documentos relativos a la compraventa en la empresa, precisando los requisitos formales que deben reunir.",
        "Se han reconocido los procesos de expedición y entrega de mercancías, así como la documentación administrativa asociada.",
        "Se ha verificado que la documentación comercial, recibida y emitida, cumple la legislación vigente y los procedimientos internos de una empresa.",
        "Se han identificado los parámetros y la información que deben ser registrados en las operaciones de compraventa.",
        "Se ha valorado la necesidad de aplicar los sistemas de protección y salvaguarda de la información, así como criterios de calidad en el proceso administrativo.",
        "Se ha gestionado la documentación, manifestando rigor y precisión.",
        "Se han utilizado aplicaciones informáticas específicas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los flujos de entrada y salida de tesorería, valorando los procedimientos de autorización de los pagos y gestión de los cobros.",
        "Se han identificado los medios de pago y cobro habituales en la empresa, así como sus documentos justificativos, diferenciando pago al contado y pago aplazado.",
        "Se han comparado las formas de financiación comercial más habituales.",
        "Se han aplicado las leyes financieras de capitalización simple o compuesta en función del tipo de operaciones.",
        "Se ha calculado la liquidación de efectos comerciales en operaciones de descuento.",
        "Se han calculado las comisiones y gastos en determinados productos y servicios bancarios relacionados con el aplazamiento del pago o el descuento comercial.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y codificado las cuentas que intervienen en las operaciones relacionadas con la actividad comercial conforme al PGC.",
        "Se han aplicado criterios de cargo y abono según el PGC.",
        "Se han efectuado los asientos correspondientes a los hechos contables más habituales del proceso comercial.",
        "Se han contabilizado las operaciones relativas a la liquidación de IVA.",
        "Se han registrado los hechos contables previos al cierre del ejercicio económico.",
        "Se ha calculado el resultado contable y el balance de situación final.",
        "Se ha preparado la información económica relevante para elaborar la memoria para un ejercicio económico concreto.",
        "Se han utilizado aplicaciones informáticas específicas.",
        "Se han realizado las copias de seguridad según el protocolo establecido para salvaguardar los datos registrados.",
        "Se ha gestionado la documentación, manifestando rigor y precisión.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han establecido la función y los métodos de control de la tesorería en la empresa.",
        "Se han cumplimentado los distintos libros y registros de tesorería.",
        "Se han ejecutado las operaciones del proceso de arqueo y cuadre de la caja y se han detectado las desviaciones.",
        "Se ha cotejado la información de los extractos bancarios con el libro de registro del banco.",
        "Se han descrito las utilidades de un calendario de vencimientos en términos de previsión financiera.",
        "Se ha relacionado el servicio de tesorería y el resto de departamentos con empresas y entidades externas.",
        "Se ha valorado la utilización de medios on-line, administración electrónica y otros sustitutivos de la presentación física de los documentos.",
        "Se han efectuado los procedimientos de acuerdo con los principios de responsabilidad, seguridad y confidencialidad de la información.",
        "Se ha utilizado la hoja de cálculo y otras herramientas informáticas para la gestión de tesorería.",
        "Se ha identificado el procedimiento para gestionar la presentación de documentos de cobro y pago ante las administraciones públicas.",
    ], start=1)],
}

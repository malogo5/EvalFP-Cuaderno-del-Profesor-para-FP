"""EvalFP — Operaciones Auxiliares de Gestión de Tesorería · 0448 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 165 h · 7 h/semana · 2º GA.
"""
MODULO = {
    "nombre":"Operaciones Auxiliares de Gestión de Tesorería","codigo":"0448","abrev":"OAGT",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"2º GA","horas_sem":7,"total_horas":165,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"Control de tesorería","horas":39,"eval":1,"tags":"Libro de caja y bancos · Previsión de tesorería · Arqueo · Conciliación bancaria"},
    {"id":"UT2","nombre":"Productos financieros de financiación e inversión","horas":39,"eval":1,"tags":"Préstamos · Créditos · Leasing · Descuento comercial · Depósitos · Renta fija y variable"},
    {"id":"UT3","nombre":"Cálculo financiero","horas":36,"eval":2,"tags":"Interés simple y compuesto · Descuento · Equivalencia de capitales · TAE · Hoja de cálculo"},
    {"id":"UT4","nombre":"Operaciones y documentación bancaria","horas":51,"eval":2,"tags":"Cuentas · Medios de pago · Banca electrónica · Extractos · Comisiones"},
]
RAS = [
    {"id":"RA1","pond":24,"nombre":"Aplica métodos de control de tesorería describiendo las fases del mismo."},
    {"id":"RA2","pond":24,"nombre":"Realiza los trámites de contratación, renovación y cancelación correspondientes a instrumentos financieros bási - cos de financiación, inversión y servicios de esta índole que se utilizan en la empresa, describiendo la finalidad de cada uno ellos."},
    {"id":"RA3","pond":21,"nombre":"Efectúa cálculos financieros básicos identificando y aplicando las leyes financieras correspondientes."},
    {"id":"RA4","pond":31,"nombre":"Efectúa las operaciones bancarias básicas interpretando la documentación asociada."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la función y los métodos del control de la tesorería en la empresa.",
        "Se ha confeccionado un presupuesto de tesorería y se han tomado decisiones para solucionar los desequilibrios",
        "Se ha diferenciado los flujos de entrada y salida de tesorería: cobros y pagos y la documentación relacionada con éstos.",
        "Se han cumplimentado los distintos libros y registros de tesorería.",
        "Se han ejecutado las operaciones del proceso de arqueo y cuadre de la caja y detectado las desviaciones.",
        "Se ha cotejado la información de los extractos bancarios con el libro de registro del banco.",
        "Se han descrito las utilidades de un calendario de vencimientos en términos de previsión financiera.",
        "Se ha relacionado el servicio de tesorería y el resto de departamentos, empresas y entidades externas.",
        "Se han utilizado medios telemáticos, de administración electrónica y otros sustitutivos de la presentación física de los documentos.",
        "Se han efectuado los procedimientos de acuerdo con los principios de responsabilidad, seguridad y confidencialidad de la información.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado las organizaciones, entidades y tipos de empresas que operan en el Sistema Financiero Español.",
        "Se han precisado las instituciones financieras bancarias y no bancarias y descrito sus principales características.",
        "Se han diferenciado los distintos mercados dentro del sistema financiero español relacionándolos con los diferentes productos financieros que se emplean habitualmente en la empresa.",
        "Se han relacionado las funciones principales de cada uno de los intermediarios financieros.",
        "Se han diferenciado los principales instrumentos financieros bancarios y no bancarios y descrito sus características.",
        "Se han clasificado los tipos de seguros de la empresa y los elementos que conforman un contrato de seguro.",
        "Se han identificado los servicios básicos que nos ofrecen los intermediarios financieros bancarios y los documentos necesarios para su contratación.",
        "Se ha calculado la rentabilidad y coste financiero de algunos instrumentos financieros de inversión.",
        "Se han operado medios telemáticos de banca on-line y afines.",
        "Se han cumplimentado diversos documentos relacionados con la contratación, renovación y cancelación de productos financieros habituales en la empresa.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha diferenciado entre las leyes financieras de capitalización simple y actualización simple.",
        "Se ha calculado el interés simple y compuesto de diversos instrumentos financieros.",
        "Se ha calculado el descuento simple de diversos instrumentos financieros.",
        "Se han descrito las implicaciones que tienen el tiempo y el tipo de interés en este tipo de operaciones.",
        "Se han diferenciado los conceptos del tanto nominal e interés efectivo o tasa anual equivalente.",
        "Se ha calculado la sustitución de uno o varios capitales por otro o por otros",
        "Se han diferenciado las características de los distintos tipos de comisiones de los productos financieros más habituales en la empresa.",
        "Se han identificado los servicios básicos que ofrecen los intermediarios financieros bancarios y los documentos necesarios para su contratación.",
        "Se ha calculado el valor actual y final de una renta constante en cualquiera de los planteamientos posibles",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han liquidado una cuenta bancaria y una de crédito por los métodos más habituales en la práctica bancaria",
        "Se ha calculado el líquido de una negociación de efectos.",
        "Se ha calculado los gastos que conlleva un efecto en gestión de cobro",
        "Se ha calculado el valor efectivo de una Letra del Tesoro",
        "Se ha realizado los cálculos para averiguar el TAE de cualquier operación financiera",
        "Se han diferenciado las variables que intervienen en las operaciones de préstamos.",
        "Se han relacionado los conceptos integrantes de la cuota del préstamo.",
        "Se han descrito las características del sistema de amortización de préstamos por los métodos más habituales utilizados en la práctica bancaria",
        "Se ha calculado el cuadro de amortización de préstamos sencillos por los métodos más habituales utilizados en la práctica bancaria",
        "Se han relacionado las operaciones financieras bancarias con la capitalización simple, compuesta y el descuento simple.",
        "Se han comparado productos financieros bajo las variables coste/rentabilidad.",
        "Se han utilizado herramientas informáticas específicas del sistema operativo bancario.",
        "Se ha analizado el funcionamiento de las operaciones de banca por Internet",
    ], start=1)],
}

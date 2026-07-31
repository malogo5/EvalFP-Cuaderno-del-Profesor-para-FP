"""EvalFP — Técnica Contable · 0441 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 165 h · 5 h/semana · 1º GA.
"""
MODULO = {
    "nombre":"Técnica Contable","codigo":"0441","abrev":"TC",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"1º GA","horas_sem":5,"total_horas":165,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"El patrimonio de la empresa","horas":26,"eval":1,"tags":"Activo · Pasivo · Patrimonio neto · Masas patrimoniales · Equilibrio patrimonial"},
    {"id":"UT2","nombre":"Metodología contable","horas":40,"eval":1,"tags":"La cuenta · Partida doble · Libro diario · Libro mayor · Balance de comprobación"},
    {"id":"UT3","nombre":"El Plan General de Contabilidad de PYMES","horas":40,"eval":2,"tags":"Marco conceptual · Cuadro de cuentas · Normas de registro y valoración · Cuentas anuales"},
    {"id":"UT4","nombre":"Registro de operaciones básicas","horas":26,"eval":3,"tags":"Compras y ventas · IVA soportado y repercutido · Gastos e ingresos · Nóminas"},
    {"id":"UT5","nombre":"Contabilidad informatizada","horas":33,"eval":3,"tags":"Plan de cuentas · Asientos predefinidos · Punteo · Libros oficiales · Copias de seguridad"},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Reconoce los elementos que integran el patrimonio de una organización económica clasificándolos en masas patrimoniales."},
    {"id":"RA2","pond":24,"nombre":"Reconoce la metodología contable analizando la terminología y los instrumentos contables utilizados en la em - presa."},
    {"id":"RA3","pond":24,"nombre":"Identifica el contenido básico del Plan General de Contabilidad PYME (PGC-PYME) interpretando su estructura."},
    {"id":"RA4","pond":16,"nombre":"Clasifica contablemente hechos económicos básicos, aplicando la metodología contable, el IVA y los criterios del Plan General de Contabilidad PYME."},
    {"id":"RA5","pond":20,"nombre":"Realiza operaciones de contabilización mediante del uso aplicaciones informáticas específicas valorando la efi - ciencia de éstas en la gestión del plan de cuentas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las fases del ciclo económico de la actividad empresarial.",
        "Se ha diferenciado entre inversión/financiación, inversión/gasto, gasto/pago e ingreso/cobro.",
        "Se han distinguido los distintos sectores económicos basándose en la diversa tipología de actividades que se desarrollan en ellos.",
        "Se han definido los conceptos de patrimonio, elemento patrimonial y masa patrimonial.",
        "Se han identificado las masas patrimoniales que integran el activo, el pasivo exigible y el patrimonio neto.",
        "Se ha relacionado cada masa patrimonial con las fases del ciclo económico de la actividad empresarial.",
        "Se han ordenado en masas patrimoniales un conjunto de elementos patrimoniales.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha distinguido las fases del ciclo contable completo adaptándolas a la legislación española.",
        "Se ha descrito el concepto de cuenta como instrumento para representar los distintos elementos patrimoniales y hechos económicos de la empresa.",
        "Se han descrito las características más importantes del método de contabilización por partida doble.",
        "Se han reconocido los criterios de cargo y abono como método de registro de las modificaciones del valor de los elementos patrimoniales.",
        "Se ha reconocido la importancia del balance de comprobación como instrumento básico para la identificación de errores y omisiones en las anotaciones de las cuentas.",
        "Se ha explicado la función del proceso de amortización contable.",
        "Se han diferenciando las cuentas de ingresos y gastos.",
        "Se ha analizado el proceso de regulación contable.",
        "Se ha definido el concepto de resultado contable.",
        "Se han descrito las funciones de los asientos de cierre y apertura.",
        "Se ha establecido la función del balance de situación, de las cuentas de pérdidas y ganancias y de la memoria.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha relacionado la normativa mercantil con el PGC.",
        "Se ha identificado la función contable de los documentos mercantiles",
        "Se ha reconocido el PGC como instrumento de armonización contable.",
        "Se han identificado las distintas partes del PGC-PYME.",
        "Se han identificado los principios contables establecidos en el marco conceptual del plan.",
        "Se han identificado los criterios de valoración en el marco conceptual del plan",
        "Se han diferenciado las partes del PGC-PYME que son obligatorias de las que no lo son.",
        "Se ha descrito el sistema de codificación establecido en el PGC-PYME y su función en la asociación y desglose de la información contable.",
        "Se han codificado un conjunto de elementos patrimoniales de acuerdo con los criterios del PGC-PYME.",
        "Se han identificado las cuentas anuales que establece el PGC-PYME.",
        "Se han identificado las cuentas que corresponden a los elementos patrimoniales.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las cuentas patrimoniales que intervienen en las operaciones básicas de las empresas.",
        "Se han identificado las cuentas de gestión que intervienen en las operaciones básicas de las empresas.",
        "Se han codificado las cuentas conforme al PGC-PYME.",
        "Se han determinado qué cuentas se cargan y cuáles se abonan, según el PGC-PYME.",
        "Se han efectuado los asientos correspondientes a los hechos contables teniendo en cuenta el IVA.",
        "Se han realizado las operaciones contables correspondientes a un ejercicio económico básico.",
        "Se ha efectuado el procedimiento de acuerdo con los principios de responsabilidad, seguridad y confidencialidad de la información.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han realizado las altas y bajas de las cuentas y subcuentas codificadas que proceden de la documentación soporte, siguiendo los procedimientos establecidos.",
        "Se han propuesto altas y bajas de códigos y conceptos en asientos predefinidos siguiendo los procedimientos establecidos.",
        "Se han introducido conceptos codificados en la aplicación informática siguiendo los procedimientos estableci - dos.",
        "Se han ejecutado las bajas de los conceptos codificados con la autorización correspondiente.",
        "Se han introducido los asientos predefinidos en la aplicación informática siguiendo los procedimientos establecidos.",
        "Se ha introducido la información que corresponde a cada campo en el asiento de acuerdo con la naturaleza eco - nómica de la operación.",
        "Se han resuelto los imprevistos que puedan surgir durante la utilización de la aplicación, recurriendo a la ayuda del programa, a la ayuda on-line o al servicio de atención al cliente de la empresa creadora del software.",
        "Se ha realizado copia de seguridad de las cuentas, saldos y sus movimientos respectivos, así como de la colec - ción de apuntes predefinidos.",
        "Se ha seguido el plan de acción para la custodia en lugar y soporte adecuado y la Gestión Administrativa de la copia de seguridad, en tiempo y con los métodos adecuados.",
    ], start=1)],
}

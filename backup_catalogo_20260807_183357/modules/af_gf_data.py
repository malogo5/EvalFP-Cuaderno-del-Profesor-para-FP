"""EvalFP — Gestión financiera · 0653 · Administración y Finanzas
Decreto 43/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9487), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 197 h · 5 h/semana · 2º AF.
"""
MODULO = {
    "nombre":"Gestión financiera","codigo":"0653","abrev":"GF",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"2º AF","horas_sem":5,"total_horas":197,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 43/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9487), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Necesidades financieras y ayudas públicas","horas":30,"eval":1,"tags":"Fuentes de financiación · Subvenciones · Coste del capital"},
    {"id":"UT2","nombre":"Productos y servicios financieros","horas":30,"eval":1,"tags":"Préstamos · Créditos · Leasing y renting · Descuento comercial · Contratación"},
    {"id":"UT3","nombre":"Cálculo y evaluación financiera","horas":39,"eval":1,"tags":"Interés simple y compuesto · Cuotas y amortización · TAE · Hoja de cálculo · Informes"},
    {"id":"UT4","nombre":"La actividad aseguradora","horas":34,"eval":2,"tags":"Tipos de seguros · Póliza · Prima · Siniestro · Indemnización"},
    {"id":"UT5","nombre":"Selección de inversiones","horas":30,"eval":2,"tags":"VAN y TIR · Plazo de recuperación · Renta fija y variable · Riesgo y rentabilidad"},
    {"id":"UT6","nombre":"Presupuestos y control presupuestario","horas":34,"eval":2,"tags":"Presupuestos por áreas · Presupuesto maestro · Desviaciones · Control"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Determina las necesidades financieras y las ayudas económicas óptimas para la empresa, identificando las alternativas posibles."},
    {"id":"RA2","pond":15,"nombre":"Clasifica los productos y servicios financieros, analizando sus características y formas de contratación."},
    {"id":"RA3","pond":20,"nombre":"Evalúa productos y servicios financieros del mercado, realizando los cálculos y elaborando los informes oportunos."},
    {"id":"RA4","pond":18,"nombre":"Caracteriza la tipología de seguros, analizando la actividad aseguradora."},
    {"id":"RA5","pond":15,"nombre":"Selecciona inversiones en activos financieros o económicos, analizando sus características y realizando los cálculos oportunos."},
    {"id":"RA6","pond":17,"nombre":"Integra los presupuestos parciales de las áreas funcionales y/o territoriales de la empresa/organización, verificando la información que contienen."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han comprobado los estados contables desde la óptica de las necesidades de financiación.",
        "Se han verificado informes económico-financieros y patrimoniales de los estados contables.",
        "Se han comparado los resultados de los análisis con los valores establecidos y se han calculado las desviaciones.",
        "Se han confeccionado informes de acuerdo con la estructura y los procedimientos, teniendo en cuenta los costes de oportunidad.",
        "Se han utilizado todos los canales de información y comunicación para identificar las ayudas públicas y/o privadas así como las fuentes a las que puede acceder la empresa.",
        "Se han identificado las características de las distintas formas de apoyo financiero a la empresa.",
        "Se ha contrastado la idoneidad y las incompatibilidades de las ayudas públicas y/o privadas estudiadas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las organizaciones, entidades y tipos de empresas que operan en el sistema financiero.",
        "Se han precisado las instituciones financieras bancarias y no bancarias y descrito sus principales características.",
        "Se han detallado los aspectos específicos de los productos y servicios existentes en el mercado.",
        "Se han reconocido las variables que intervienen en las operaciones que se realizan con cada producto/servicio financiero.",
        "Se han identificado los sujetos que intervienen en las operaciones que se realizan con cada producto/servicio financiero.",
        "Se han relacionado las ventajas e inconvenientes de los distintos productos y servicios.",
        "Se ha determinado la documentación necesaria exigida y generada con la gestión de los diferentes productos y servicios financieros.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha recogido información sobre productos y servicios financieros a través de los diferentes canales disponibles.",
        "Se han efectuado las operaciones matemáticas necesarias para valorar cada producto.",
        "Se han calculado los gastos y comisiones devengados en cada producto.",
        "Se ha determinado el tratamiento fiscal de cada producto.",
        "Se ha determinado el tipo de garantía exigido por cada producto.",
        "Se han realizado informes comparativos de los costes financieros de cada uno de los productos de financiación propuestos.",
        "Se han comparado los servicios y las contraprestaciones de las distintas entidades financieras, resaltando las diferencias, ventajas e inconvenientes.",
        "Se han comparado las rentabilidades, ventajas e inconvenientes de cada una de las formas de ahorro o inversión propuestas en productos financieros.",
        "Se han realizado los cálculos financieros necesarios utilizando aplicaciones informáticas específicas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la legislación básica que regula la actividad aseguradora.",
        "Se han relacionado los riesgos y las condiciones del asegurabilidad.",
        "Se han identificado los elementos que conforman un contrato de seguro.",
        "Se han clasificado los tipos de seguros.",
        "Se han establecido las obligaciones de las partes en un contrato de seguro.",
        "Se han determinado los procedimientos administrativos relativos a la contratación y seguimiento de los seguros.",
        "Se han identificado las primas y sus componentes.",
        "Se ha determinado el tratamiento fiscal de los seguros.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la función de los activos financieros como forma de inversión y como fuente de financiación.",
        "Se han clasificado los activos financieros utilizando como criterio el tipo de renta que generan, la clase de entidad emisora y los plazos de amortización.",
        "Se han distinguido el valor nominal, de emisión, de cotización, de reembolso y otros para efectuar los cálculos oportunos.",
        "Se ha determinado el importe resultante en operaciones de compraventa de activos financieros, calculando los gastos y las comisiones devengadas.",
        "Se han elaborado informes sobre las diversas alternativas de inversión en activos financieros que más se ajusten a las necesidades de la empresa.",
        "Se han identificado las variables que influyen en una inversión económica.",
        "Se ha calculado e interpretado el VAN, TIR y otros métodos de selección de distintas inversiones.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han integrado los presupuestos de las distintas áreas en un presupuesto común.",
        "Se ha comprobado que la información está completa y en la forma requerida.",
        "Se ha contrastado el contenido de los presupuestos parciales.",
        "Se han verificado los cálculos aritméticos, comprobando la corrección de los mismos.",
        "Se ha valorado la importancia de elaborar en tiempo y forma la documentación relacionada con los presupuestos.",
        "Se ha controlado la ejecución del presupuesto y se han detectado las desviaciones y sus causas.",
        "Se ha ordenado y archivado la información de forma que sea fácilmente localizable.",
        "Se han utilizado aplicaciones informáticas en la gestión de las tareas presupuestarias.",
    ], start=1)],
}

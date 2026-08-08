"""EvalFP — Contabilidad y fiscalidad · 0654 · Administración y Finanzas
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 236 h · 6 h/semana · 2º AF.
"""
MODULO = {
    "nombre":"Contabilidad y fiscalidad","codigo":"0654","abrev":"CF",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"2º AF","horas_sem":6,"total_horas":236,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Contabilización informatizada de operaciones","horas":34,"eval":1,"tags":"Software contable · Asientos · Inmovilizado · Existencias · Personal"},
    {"id":"UT2","nombre":"Impuesto de Sociedades e IRPF","horas":43,"eval":1,"tags":"Base imponible · Ajustes · Deducciones · Modelos 200 y 100 · Pagos fraccionados"},
    {"id":"UT3","nombre":"Operaciones de cierre del ejercicio","horas":43,"eval":1,"tags":"Periodificación · Amortizaciones · Deterioros · Regularización · Asiento de cierre"},
    {"id":"UT4","nombre":"Cuentas anuales y depósito en el Registro","horas":47,"eval":2,"tags":"Balance · Pérdidas y ganancias · Memoria · ECPN · Estado de flujos de efectivo"},
    {"id":"UT5","nombre":"Análisis de estados financieros","horas":30,"eval":2,"tags":"Ratios · Fondo de maniobra · Rentabilidad · Umbral de rentabilidad · Informes"},
    {"id":"UT6","nombre":"La auditoría de cuentas","horas":39,"eval":2,"tags":"Tipos de auditoría · Normas técnicas · Evidencia · Informe de auditoría"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Contabiliza en soporte informático los hechos contables derivados de las operaciones de trascendencia económicofinanciera de una empresa, cumpliendo con los criterios establecidos en el Plan General de Contabilidad (PGC)."},
    {"id":"RA2","pond":18,"nombre":"Realiza la tramitación de las obligaciones fiscales y contables relativas al Impuesto de Sociedades y el Impuesto sobre la Renta de las Personas Físicas, aplicando la normativa de carácter mercantil y fiscal vigente."},
    {"id":"RA3","pond":18,"nombre":"Registra contablemente las operaciones derivadas del fin del ejercicio económico a partir de la información y documentación de un ciclo económico completo, aplicando los criterios del PGC y la legislación vigente."},
    {"id":"RA4","pond":20,"nombre":"Confecciona las cuentas anuales y verifica los trámites para su depósito en el Registro Mercantil, aplicando la legislación mercantil vigente."},
    {"id":"RA5","pond":13,"nombre":"Elabora informes de análisis sobre la situación económica-financiera y patrimonial de una empresa, interpretando los estados contables."},
    {"id":"RA6","pond":16,"nombre":"Caracteriza el proceso de auditoría en la empresa, describiendo su propósito dentro del marco normativo español."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","examen"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["practica","examen"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha comprobado la correcta instalación de las aplicaciones informáticas y su funcionamiento.",
        "Se han seleccionado las prestaciones, funciones y procedimientos de las aplicaciones informáticas que se deben emplear para la contabilización.",
        "Se han caracterizado las definiciones y las relaciones contables fundamentales establecidas en los grupos, subgrupos y cuentas principales del PGC.",
        "Se han registrado, en asientos por partida doble, las operaciones más habituales relacionadas con los grupos de cuentas descritos anteriormente.",
        "Se han clasificado los diferentes tipos de documentos mercantiles que exige el PGC, indicando la clase de operación que representan.",
        "Se ha verificado el traspaso de la información entre las distintas fuentes de datos contables.",
        "Se ha identificado la estructura y forma de elaboración del balance de comprobación de sumas y saldos.",
        "Se han realizado copias de seguridad para la salvaguarda de los datos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado la normativa fiscal vigente y las normas aplicables en cada tipo de impuesto.",
        "Se han seleccionado los modelos establecidos por la Hacienda Pública para atender el procedimiento de declaración-liquidación de los distintos impuestos.",
        "Se han identificado los plazos establecidos por la Hacienda Pública para cumplir con las obligaciones fiscales.",
        "Se han realizado los cálculos oportunos para cuantificar los elementos tributarios de los impuestos que gravan la actividad económica.",
        "Se ha cumplimentado la documentación correspondiente a la declaración-liquidación de los distintos impuestos, utilizando aplicaciones informáticas de gestión fiscal.",
        "Se han generado los ficheros necesarios para la presentación telemática de los impuestos, valorando la eficiencia de esta vía.",
        "Se han relacionado los conceptos contables con los aspectos tributarios.",
        "Se ha diferenciado entre resultado contable y resultado fiscal y se han especificado los procedimientos para la conciliación de ambos.",
        "Se han contabilizado los hechos contables relacionados con el cumplimiento de las obligaciones fiscales, incluyendo los ajustes fiscales correspondientes.",
        "Se han descrito y cuantificado, en su caso, las consecuencias de la falta de rigor en el cumplimiento de las obligaciones fiscales.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han registrado en soporte informático los hechos contables y fiscales que se generan en un ciclo económico completo, contenidos en los documentos soportes.",
        "Se han calculado y contabilizado las correcciones de valor que procedan.",
        "Se han reconocido los métodos de amortización más habituales.",
        "Se han realizado los cálculos derivados de la amortización del inmovilizado.",
        "Se han dotado las amortizaciones que procedan según la amortización técnica propuesta.",
        "Se han realizado los asientos derivados de la periodificación contable.",
        "Se ha obtenido el resultado por medio del proceso de regularización.",
        "Se ha registrado la distribución del resultado según las normas y las indicaciones propuestas.",
        "Se han registrado en los libros obligatorios de la empresa todas las operaciones derivadas del ejercicio económico que sean necesarias.",
        "Se han realizado copias de seguridad para la salvaguarda de los datos.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha determinado la estructura de la cuenta de pérdidas y ganancias, diferenciando los distintos tipos de resultado que integran.",
        "Se ha determinado la estructura del balance de situación, indicando las relaciones entre los diferentes epígrafes.",
        "Se ha establecido la estructura de la memoria, estado de cambios en el patrimonio y estado de flujos de efectivo.",
        "Se han confeccionado las cuentas anuales aplicando los criterios del PGA.",
        "Se han determinado los libros contables objeto de legalización para su presentación ante los organismos correspondientes.",
        "Se han verificado los plazos de presentación legalmente establecidos en los organismos oficiales correspondientes.",
        "Se han cumplimentado los formularios de acuerdo con la legislación mercantil y se han utilizado aplicaciones informáticas.",
        "Se ha comprobado la veracidad e integridad de la información contenida en los ficheros generados por la aplicación informática.",
        "Se ha valorado la importancia de las cuentas anuales como instrumentos de comunicación interna y externa y de información pública.",
        "Se han realizado copias de seguridad para la salvaguarda de los datos.",
        "Se ha valorado la aplicación de las normas de protección de datos en el proceso contable.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido las funciones de los análisis económico-financiero, patrimonial y de tendencia y proyección, estableciendo sus diferencias.",
        "Se ha seleccionado la información relevante para el análisis de los estados contables que la proporcionan.",
        "Se han identificado los instrumentos de análisis más significativos y se ha descrito su función.",
        "Se han calculado las diferencias, porcentajes, índices y ratios más relevantes para el análisis económico, financiero y de tendencia y proyección.",
        "Se ha realizado un informe sobre la situación económica-financiera de la empresa, derivada de los cálculos realizados, comparándola con los ejercicios anteriores y con la media del sector.",
        "Se han obtenido conclusiones con respecto a la liquidez, solvencia, estructura financiera y rentabilidades de la empresa.",
        "Se ha valorado la importancia del análisis de los estados contables para la toma de decisiones en la empresa y su repercusión con respecto a los implicados en la misma (“stakeholders”).",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha delimitado el concepto de auditoría, sus clases (interna y externa) y el propósito de esta.",
        "Se han señalado los órganos y normativa vigente que atañe a la auditoría en España.",
        "Se han verificado las facultades y responsabilidades de los auditores.",
        "Se han secuenciado las diferentes fases de un proceso de auditoría y los flujos de información que se generan en cada uno de ellos.",
        "Se han determinado las partes de un informe de auditoría.",
        "Se ha valorado la importancia de la obligatoriedad de un proceso de auditoría.",
        "Se ha valorado la importancia de la colaboración del personal de la empresa en un proceso de auditoría.",
        "Se han reconocido las tareas que deben realizarse por parte de la empresa en un proceso de auditoría, tanto interna como externa.",
        "Se han contabilizado los ajustes y correcciones contables derivados de propuestas del informe de auditoría.",
    ], start=1)],
}

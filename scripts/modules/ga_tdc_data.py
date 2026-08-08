"""EvalFP — Tratamiento de la Documentación Contable · 0443 · Gestión Administrativa
Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IC-1. 1º · RA y CE: Decreto 251/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II
RA y CE literales del Anexo II del Decreto 251/2011 (DOCM); las horas y el curso son los del Decreto 79/2024, que modifica aquel currículo.
Duración: 195 h · 5 h/semana · 2º GA.
"""
MODULO = {
    "nombre":"Tratamiento de la Documentación Contable","codigo":"0443","abrev":"TDC",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"2º GA","horas_sem":5,"total_horas":195,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IC-1. 1º · RA y CE: Decreto 251/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Documentos soporte de la contabilidad","horas":41,"eval":1,"tags":"Facturas · Extractos bancarios · Nóminas · Justificantes · Archivo y conservación"},
    {"id":"UT2","nombre":"Registro contable de operaciones","horas":46,"eval":1,"tags":"Compras y ventas · Gastos e ingresos · Inmovilizado · Personal · IVA"},
    {"id":"UT3","nombre":"El ciclo contable completo","horas":51,"eval":2,"tags":"Apertura · Regularización · Amortizaciones · Cierre · Cuentas anuales"},
    {"id":"UT4","nombre":"Comprobación y control contable","horas":57,"eval":2,"tags":"Punteo · Conciliación bancaria · Balance de sumas y saldos · Detección y corrección de errores"},
]
RAS = [
    {"id":"RA1","pond":21,"nombre":"Prepara la documentación soporte de los hechos contables interpretando la información que contiene."},
    {"id":"RA2","pond":24,"nombre":"Registra contablemente hechos económicos habituales reconociendo y aplicando la metodología contable y los criterios del Plan General de Contabilidad PYME."},
    {"id":"RA3","pond":26,"nombre":"Contabiliza operaciones económicas habituales correspondientes a un ejercicio económico completo, reconocien - do y aplicando la metodología contable y los criterios del Plan de Contabilidad."},
    {"id":"RA4","pond":29,"nombre":"Comprueba las cuentas relacionando cada registro contable con los datos de los documentos soporte."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
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
        "Se han identificado los diferentes tipos de documentos soporte que son objeto de registro contable.",
        "Se ha comprobado que la documentación soporte recibida contiene todos los registros de control interno estable - cidos –firma, autorizaciones u otros– para su registro contable.",
        "Se han efectuado propuestas para la subsanación de errores.",
        "Se ha clasificado la documentación soporte de acuerdo a criterios previamente establecidos.",
        "Se ha efectuado el procedimiento de acuerdo con los principios de seguridad y confidencialidad de la informa - ción.",
        "Se ha archivado la documentación soporte de los asientos siguiendo procedimientos establecidos.",
        "Se ha mantenido un espacio de trabajo con el grado apropiado de orden y limpieza.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las cuentas que intervienen en las operaciones más habituales de las empresas.",
        "Se han codificado las cuentas conforme al PGC.",
        "Se han determinado qué cuentas se cargan y cuáles se abonan, según el PGC.",
        "Se han efectuado los asientos correspondientes a los hechos contables más habituales.",
        "Se han cumplimentado los distintos campos del libro de bienes de inversión por medios manuales y/o informáti - cos.",
        "Se han contabilizado las operaciones relativas a la liquidación de IVA.",
        "Se han realizado las copias de seguridad según el protocolo establecido para salvaguardar los datos registra - dos.",
        "Se ha efectuado el procedimiento de acuerdo con los principios de responsabilidad, seguridad y confidencialidad de la información.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los hechos económicos que originan una anotación contable.",
        "Se ha introducido correctamente la información derivada de cada hecho económico en la aplicación informática de forma cronológica.",
        "Se han obtenido periódicamente los balances de comprobación de sumas y saldos.",
        "Se han calculado las operaciones derivadas de los registros contables que se ha de realizar antes del cierre del ejercicio económico.",
        "Se ha introducido correctamente en la aplicación informática las amortizaciones correspondientes, las correccio - nes de valor reversibles y la regularización contable que corresponde a un ejercicio económico concreto.",
        "Se ha obtenido con medios informáticos el cálculo del resultado contable y el balance de situación final.",
        "Se ha preparado la información económica relevante para elaborar la memoria de la empresa para un ejercicio económico concreto.",
        "Se ha elaborado la memoria de la empresa para un ejercicio económico concreto.",
        "Se ha verificado el funcionamiento del proceso, contrastando los resultados con los datos introducidos.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han verificado los saldos de las cuentas deudoras y acreedoras de las administraciones públicas con la docu - mentación laboral y fiscal.",
        "Se han cotejado periódicamente los saldos de los préstamos y créditos con la documentación soporte.",
        "Se han circularizado los saldos de clientela y proveedores de acuerdo a las normas internas recibidas.",
        "Se han comprobado los saldos de la amortización acumulada de los elementos del inmovilizado acorde con el manual de procedimiento.",
        "Se han efectuado los punteos de las diversas partidas o asientos para efectuar las comprobaciones de movimien - tos o la integración de partidas.",
        "Se han efectuado las correcciones adecuadas a través de la conciliación bancaria para que, tanto los libros con - tables como el saldo de las cuentas, reflejen las mismas cantidades.",
        "Se ha comprobado el saldo de las cuentas como paso previo al inicio de las operaciones de cierre del ejercicio.",
        "Se han comunicado los errores detectados según el procedimiento establecido.",
        "Se han utilizado aplicaciones informáticas para la comprobación de los registros contables.",
        "Se ha efectuado el procedimiento de acuerdo con los principios de seguridad y confidencialidad de la informa - ción.",
    ], start=1)],
}

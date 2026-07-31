"""EvalFP — Simulación empresarial · 0656 · Administración y Finanzas
Decreto 43/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9487), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 156 h · 4 h/semana · 2º AF.
"""
MODULO = {
    "nombre":"Simulación empresarial","codigo":"0656","abrev":"SE",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"2º AF","horas_sem":4,"total_horas":156,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 43/2013, de 25/07/2013 (DOCM 01/08/2013, NID 2013/9487), Anexo I · distribución horaria LOFP publicada por la Consejería de Educación de CLM",
}
UTS = [
    {"id":"UT1","nombre":"Innovación y creación de empresas","horas":21,"eval":1,"tags":"Innovación · Emprendimiento · Detección de oportunidades · Casos reales"},
    {"id":"UT2","nombre":"Idea de negocio y estudio de mercado","horas":24,"eval":1,"tags":"Segmentación · Competencia · DAFO · Encuestas"},
    {"id":"UT3","nombre":"Organización, forma jurídica y recursos","horas":28,"eval":1,"tags":"Organigrama · Formas jurídicas · Recursos materiales y humanos"},
    {"id":"UT4","nombre":"Análisis de viabilidad","horas":24,"eval":2,"tags":"Plan de inversión · Previsión de tesorería · Umbral de rentabilidad · Escenarios"},
    {"id":"UT5","nombre":"Trámites de puesta en marcha","horas":28,"eval":2,"tags":"Registro Mercantil · Hacienda · Seguridad Social · Ayuntamiento · Licencias"},
    {"id":"UT6","nombre":"Gestión de la empresa-proyecto","horas":31,"eval":2,"tags":"Departamentos · Rotación de puestos · Documentación real · Reuniones · Memoria final"},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Determina los factores de la innovación empresarial, relacionándolos con la actividad de creación de empresas."},
    {"id":"RA2","pond":16,"nombre":"Selecciona una idea de negocio, analizando el mercado."},
    {"id":"RA3","pond":18,"nombre":"Determina la organización interna de la empresa, la forma jurídica y los recursos necesarios, analizando las alternativas disponibles y los objetivos marcados con el proyecto."},
    {"id":"RA4","pond":16,"nombre":"Comprueba la viabilidad de la empresa mediante diferentes tipos de análisis, verificando los diversos factores que pueden influir en la misma."},
    {"id":"RA5","pond":17,"nombre":"Gestiona la documentación necesaria para la puesta en marcha de una empresa, analizando los trámites legales y las actuaciones necesarias que conllevan la realización del proyecto empresarial."},
    {"id":"RA6","pond":19,"nombre":"Realiza la gestión de la empresa-proyecto en sus diversos departamentos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["proyecto","practica"],
    "RA3":["proyecto","practica"],
    "RA4":["proyecto","practica"],
    "RA5":["practica","proyecto"],
    "RA6":["proyecto","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han examinado las diversas facetas de la innovación empresarial (técnicas, materiales, de organización interna y externa, entre otras), relacionándolas como fuentes de desarrollo económico y creación de empleo.",
        "Se han relacionado la innovación y la iniciativa emprendedora con las implicaciones que tiene para la competitividad empresarial.",
        "Se han valorado los aspectos inherentes a la asunción de riesgo empresarial como motor económico y social.",
        "Se han determinado las diferentes facetas del carácter emprendedor desde el punto de vista empresarial.",
        "Se han seleccionado diferentes experiencias de innovación empresarial, describiendo y valorando los factores de riesgo asumidos en cada una de ellas.",
        "Se han propuesto posibilidades de internacionalización de algunas empresas como factor de innovación de las mismas.",
        "Se han definido ayudas y herramientas, públicas y privadas, para la innovación, creación e internacionalización de empresas, relacionándolas estructuradamente en un informe.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado las implicaciones que conlleva la elección de una idea de negocio.",
        "Se ha diferenciado entre lo que puede ser una simple idea de una idea de negocio factible.",
        "Se han señalado las ventajas e inconvenientes de las propuestas de negocio.",
        "Se ha determinado el producto o servicio que se quiere proporcionar con la idea de negocio.",
        "Se han concretado las necesidades que satisface y el valor añadido de la idea de negocio propuesta.",
        "Se han identificado los clientes potenciales, atendiendo a los objetivos del proyecto de empresa.",
        "Se ha efectuado un análisis de mercado para comprobar si existe un nicho en el mismo.",
        "Se ha efectuado un análisis de la competencia para posicionar nuestro producto.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las principales características del sector empresarial en el que se desenvuelve la idea de negocio.",
        "Se han reconocido los distintos tipos de empresas que existen.",
        "Se han establecido claramente los objetivos de la empresa.",
        "Se ha relacionado la organización establecida por la empresa con el tipo y fines de esta.",
        "Se han identificado las diferentes funciones dentro de la empresa.",
        "Se ha seleccionado la forma jurídica adecuada.",
        "Se ha efectuado una asignación eficiente de los recursos necesarios.",
        "Se han reconocido y seleccionado las posibles fuentes de financiación.",
        "Se ha valorado la importancia de dotar a la empresa de la estructura adecuada para su pervivencia.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha efectuado un estudio de la viabilidad técnica del negocio.",
        "Se ha contrastado el cumplimiento de la normativa legal del futuro negocio.",
        "Se ha comprobado la accesibilidad de las fuentes de financiación para la puesta en marcha del negocio.",
        "Se ha efectuado un análisis sobre la capacitación profesional para llevar a cabo las actividades derivadas del tipo de negocio elegido.",
        "Se ha realizado un análisis del impacto ambiental de proyecto de empresa.",
        "Se ha realizado un análisis de los riesgos laborales de proyecto de empresa.",
        "Se ha comprobado la viabilidad económica por medio del análisis de proyectos de inversión.",
        "Se ha elaborado un plan de viabilidad a largo plazo para poder efectuar una mejor planificación en la empresa.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la exigencia de la realización de diversos trámites legales exigibles antes de la puesta en marcha de un negocio.",
        "Se han diferenciado los trámites que se seguirían en función de la forma jurídica elegida.",
        "Se han identificado los organismos ante los cuales han de presentarse los trámites.",
        "Se ha cumplimentado la documentación necesaria para la constitución de la empresa.",
        "Se han realizado los trámites fiscales para la puesta en marcha.",
        "Se han realizado los trámites necesarios ante la autoridad laboral y la Seguridad Social.",
        "Se han realizado los trámites necesarios en otras administraciones públicas a la hora de abrir un negocio.",
        "Se ha reconocido la existencia de trámites de carácter específico para determinado tipos de negocios.",
        "Se ha valorado la importancia del cumplimiento de los plazos legales para la tramitación y puesta en marcha de un negocio.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha efectuado una planificación sobre las necesidades de aprovisionamiento de la empresa.",
        "Se ha gestionado el proceso de comercialización de los productos de la empresa.",
        "Se ha planificado la gestión de los recursos humanos.",
        "Se ha confeccionado y verificado la contabilidad de la empresa.",
        "Se han planificado las necesidades financieras de la empresa.",
        "Se ha analizado la normativa fiscal vigente y se ha cumplido con las obligaciones fiscales.",
        "Se ha valorado la organización de la propia tarea.",
        "Se ha realizado el trabajo entre los miembros del grupo.",
        "Se ha realizado cada tarea con rigurosidad y corrección para obtener un resultado global satisfactorio.",
        "Se ha materializado en un dossier el proyecto empresarial y se ha expuesto en público.",
    ], start=1)],
}

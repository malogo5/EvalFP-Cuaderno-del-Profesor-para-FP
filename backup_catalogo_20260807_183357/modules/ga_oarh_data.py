"""EvalFP — Operaciones Administrativas de Recursos Humanos · 0442 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 130 h · 6 h/semana · 2º GA.
"""
MODULO = {
    "nombre":"Operaciones Administrativas de Recursos Humanos","codigo":"0442","abrev":"OARH",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"2º GA","horas_sem":6,"total_horas":130,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"Selección de personal","horas":26,"eval":1,"tags":"Reclutamiento · Curriculum · Pruebas de selección · Entrevista · Protección de datos"},
    {"id":"UT2","nombre":"Formación y desarrollo de RRHH","horas":26,"eval":1,"tags":"Plan de formación · Promoción · Retribución variable · Beneficios sociales"},
    {"id":"UT3","nombre":"El contrato de trabajo","horas":26,"eval":1,"tags":"Modalidades · Alta y afiliación · Contrat@ · Modificaciones · Extinción y liquidación"},
    {"id":"UT4","nombre":"Nómina y seguros sociales","horas":23,"eval":2,"tags":"Bases de cotización · Deducciones · IRPF · RLC y RNT · Sistema de liquidación directa · Modelo 111"},
    {"id":"UT5","nombre":"Incidencias de la relación laboral","horas":16,"eval":2,"tags":"Incapacidad temporal · Nacimiento y cuidado de menor · Vacaciones · Permisos · Parte de accidente"},
    {"id":"UT6","nombre":"Calidad y prevención en la gestión de RRHH","horas":13,"eval":2,"tags":"Indicadores · Sistema integrado de gestión · Prevención de riesgos · Protección ambiental"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Realiza la tramitación administrativa de los procesos de captación y selección del personal describiendo la docu - mentación asociada."},
    {"id":"RA2","pond":20,"nombre":"Realiza la tramitación administrativa de los procesos de formación, desarrollo, compensación y beneficios de los trabajadores y las trabajadoras reconociendo la documentación que en ella se genera."},
    {"id":"RA3","pond":20,"nombre":"Confecciona la documentación relativa al proceso de contratación, variaciones de la situación laboral y finaliza - ción de contrato, identificando y aplicando la normativa laboral en vigor."},
    {"id":"RA4","pond":18,"nombre":"Elabora la documentación correspondiente al pago de retribuciones del personal, de cotización a la Seguridad Social e impuestos inherentes, reconociendo y aplicando la normativa en vigor."},
    {"id":"RA5","pond":12,"nombre":"Elabora la documentación relativa a las incidencias derivadas de la actividad laboral de los trabajadores, descri - biendo y aplicando las normas establecidas."},
    {"id":"RA6","pond":10,"nombre":"Aplica procedimientos de calidad, prevención de riesgos laborales y protección ambiental en las operaciones ad - ministrativas de recursos humanos reconociendo su incidencia en un sistema integrado de gestión administrativa."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["practica","examen"],
    "RA4":["practica","examen"],
    "RA5":["practica","examen"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los aspectos principales de la organización de las relaciones laborales.",
        "Se han relacionado las funciones y tareas del departamento de recursos humanos, así como las principales polí - ticas de gestión del capital humano de las organizaciones.",
        "Se han identificado las técnicas habituales de captación y selección.",
        "Se han caracterizado las labores de apoyo en la ejecución de pruebas y entrevistas en un proceso de selección, utilizado los canales convencionales o telemáticos.",
        "Se han identificado los recursos necesarios, tiempos y plazos, para realizar un proceso de selección de perso - nal.",
        "Se ha recopilado la información de las acciones formativas, junto con los informes cuantitativos –documental e informático– de cada una de las personas participantes y elaborado informes apropiados.",
        "Se ha mantenido actualizada la información sobre formación, desarrollo y compensación y beneficios, así como de interés general para los empleados en la base de datos creada para este fin.",
        "Se ha recopilado la información necesaria para facilitar la adaptación de los trabajadores y trabajadoras al nuevo empleo.",
        "Se han realizado consultas de las bases de datos con los filtros indicados, elaborando listados e informes sobre diversos datos de gestión de personal.",
        "Se han aplicado los criterios, normas y procesos de calidad establecidos, contribuyendo a una gestión eficaz.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características de los planes de formación continua así como las de los planes de carrera de los empleados y las empleadas.",
        "Se ha preparado la documentación necesaria para una actividad de formación, tal como manuales, listados, ho - rarios y hojas de control.",
        "Se han identificado y contactado las entidades de formación más cercanas o importantes, preferentemente por medios telemáticos, para proponer ofertas de formación en un caso empresarial dado.",
        "Se han clasificado las principales fuentes de subvención de la formación en función de su cuantía y requisitos.",
        "Se han organizado listados de actividades de formación y reciclaje en función de programas subvencionados.",
        "Se ha recopilado la información de las acciones formativas, junto con los informes cuantitativos –documental e informático– de cada uno de los participantes.",
        "Se ha actualizado la información sobre formación, desarrollo y compensación y beneficios, así como de interés general para los empleados en los canales de comunicación internos.",
        "Se han actualizado las bases de datos de gestión de personal.",
        "Se han realizado consultas básicas de las bases de datos con los filtros indicados, elaborando listados e informes.",
        "Se ha aplicado a su nivel la normativa vigente de protección de datos en cuanto a seguridad, confidencialidad, integridad, mantenimiento y accesibilidad a la información.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los aspectos más relevantes de las condiciones laborales establecidas en la Constitución, Esta - tuto de los Trabajadores, Convenios Colectivos y contratos.",
        "Se han reconocido las fases del proceso de contratación y los tipos de contratos laborales más habituales según la normativa laboral.",
        "Se han cumplimentado los contratos laborales.",
        "Se han obtenido documentos oficiales utilizando la página Web de los organismos públicos correspondientes.",
        "Se han definido los procesos de afiliación y alta en la Seguridad Social.",
        "Se han obtenido las tablas, baremos y referencias sobre las condiciones laborales: convenio colectivo, bases y tipos de cotización a la Seguridad Social y retenciones del IRPF.",
        "Se han aplicado las normas de cotización de la Seguridad Social referentes a condiciones laborales, plazos de pago y fórmulas de aplazamiento.",
        "Se han identificado las causas y procedimientos de modificación, suspensión y extinción del contrato de trabajo según la normativa vigente, así como identificado los elementos básicos del finiquito.",
        "Se ha registrado la información generada en los respectivos expedientes de personal.",
        "Se han seguido criterios de plazos, confidencialidad, seguridad y diligencia en la gestión y conservación de la información.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los conceptos de retribución y cotización del trabajador o trabajadora y diferenciado los tipos de retribución más comunes.",
        "Se ha identificado la estructura básica del salario y los distintos tipos de percepciones salariales, no salariales, las de periodicidad superior al mes y extraordinarias.",
        "Se ha calculado el importe de las bases de cotización en función de las percepciones salariales y las situaciones más comunes que las modifican.",
        "Se han calculado y cumplimentado el recibo de salario y documentos de cotización.",
        "Se han tenido en cuenta los plazos establecidos para el pago de cuotas a la Seguridad Social y retenciones, así como las fórmulas de aplazamiento según los casos.",
        "Se han obtenido los recibos de salario, documentos de cotización y listados de control.",
        "Se han creado los ficheros de remisión electrónica, tanto para entidades financieras como para la administración pública.",
        "Se han valorado las consecuencias de no cumplir con los plazos previstos en la presentación de documentación y pago.",
        "Se han realizado periódicamente copias de seguridad informáticas para garantizar la conservación de los datos en su integridad.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado los aspectos básicos de las relaciones laborales en cuanto a sus comunicaciones internas.",
        "Se han elaborado los formularios de recogida de datos sobre el control presencial, incapacidad temporal, permi - sos, vacaciones y similares.",
        "Se han realizado cálculos y estadísticas sobre los datos anteriores, utilizado hojas de cálculo y formatos de grá - ficos.",
        "Se han elaborado informes básicos del control de presencia, utilizando aplicaciones de proceso de texto y pre - sentaciones.",
        "Se ha realizado el seguimiento de control de presencia para conseguir la eficiencia de la empresa.",
        "Se han realizado periódicamente copias de seguridad de las bases de datos de empleados y empleadas.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los principios básicos de un modelo de gestión de calidad.",
        "Se ha valorado la integración de los procesos de recursos humanos con otros procesos administrativos de la empresa.",
        "Se han aplicado las normas de prevención de riesgos laborales en el sector.",
        "Se han aplicado los procesos para minimizar el impacto ambiental de su actividad.",
        "Se ha aplicado en la elaboración y conservación de la documentación las técnicas 3R –Reducir, Reutilizar, Reciclar.",
    ], start=1)],
}

"""EvalFP — Protocolo empresarial · 0661 · Asistencia a la Dirección
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.3º · RA y CE: Decreto 41/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 157 h · 4 h/semana · 2º AD.
"""
MODULO = {
    "nombre":"Protocolo empresarial","codigo":"0661","abrev":"PE",
    "ciclo":"Asistencia a la Dirección","ciclo_clave":"AD","ciclo_nivel":"CFGS",
    "curso":"2º AD","horas_sem":4,"total_horas":157,"anno":"2026-2027","eval_count":2,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.3º · RA y CE: Decreto 41/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Fundamentos de relaciones públicas","horas":19,"eval":1,"tags":"Comunicación corporativa · Públicos · Medios · Patrocinio y mecenazgo"},
    {"id":"UT2","nombre":"Protocolo empresarial","horas":30,"eval":1,"tags":"Precedencias · Presidencias · Tipos de mesa · Invitaciones · Regalos de empresa"},
    {"id":"UT3","nombre":"Protocolo institucional","horas":30,"eval":1,"tags":"Normativa de precedencias · Símbolos del Estado · Banderas · Actos oficiales"},
    {"id":"UT4","nombre":"Apoyo a la comunicación profesional","horas":28,"eval":2,"tags":"Comunicación interna y externa · Portavocía · Relación con medios · Redes sociales"},
    {"id":"UT5","nombre":"Cartas de servicios y compromisos de calidad","horas":22,"eval":2,"tags":"Compromisos · Indicadores · Garantías · Certificación"},
    {"id":"UT6","nombre":"Excelencia en la atención al cliente","horas":28,"eval":2,"tags":"Expectativas · Fidelización · Quejas · Mejora continua"},
]
RAS = [
    {"id":"RA1","pond":12,"nombre":"Caracteriza los fundamentos y elementos de relaciones públicas, relacionándolos con las distintas situaciones empresariales."},
    {"id":"RA2","pond":19,"nombre":"Selecciona las técnicas de protocolo empresarial aplicable, describiendo los diferentes elementos de diseño y organización, según la naturaleza y el tipo de acto, así como al público al que va dirigido."},
    {"id":"RA3","pond":19,"nombre":"Caracteriza el protocolo institucional, analizando los diferentes sistemas de organización y utilizando las normas establecidas."},
    {"id":"RA4","pond":18,"nombre":"Coordina actividades de apoyo a la comunicación y a las relaciones profesionales, internas y externas, asociando las técnicas empleadas con el tipo de usuario."},
    {"id":"RA5","pond":14,"nombre":"Elabora las cartas de servicios o los compromisos de calidad y garantía, ajustándose a los protocolos establecidos en la empresa/organización."},
    {"id":"RA6","pond":18,"nombre":"Promueve actitudes correctas de atención al cliente/usuario, analizando la importancia de superar las expectativas del mismo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","examen"],
    "RA3":["examen","practica"],
    "RA4":["practica"],
    "RA5":["practica","examen"],
    "RA6":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los fundamentos y principios de las relaciones públicas.",
        "Se ha identificado y clasificado el concepto de identidad corporativa, imagen corporativa y sus componentes.",
        "Se han reconocido distintos tipos de imagen proyectadas por empresas y organizaciones.",
        "Se han reconocido y valorado los diferentes recursos de las relaciones públicas.",
        "Se han seleccionado diferentes medios de comunicación, dependiendo del producto que hay que presentar y el público al que se dirige.",
        "Se ha valorado la importancia de la imagen, la identidad corporativa, la comunicación y las relaciones públicas en las empresas y organizaciones.",
        "Se ha analizado la conveniencia de contar con un servicio de protocolo y/o un gabinete de prensa o comunicación, según la dimensión de la empresa u organización.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la naturaleza y el tipo de actos que se deben organizar y se han aplicado las soluciones organizativas adecuadas.",
        "Se han descrito las fases de creación y diseño de un manual de protocolo y relaciones públicas según el público al que va dirigido.",
        "Se han diferenciado los requisitos y necesidades de los actos protocolarios nacionales de los internacionales.",
        "Se han identificado las técnicas de funcionamiento, planificación y organización de actos protocolarios empresariales.",
        "Se ha elaborado el programa y cronograma del acto que se va a organizar.",
        "Se ha definido y/o cumplimentado la documentación necesaria según el acto, para su correcto desarrollo.",
        "Se ha calculado el presupuesto económico del acto que hay que organizar.",
        "Se han definido los indicadores de calidad y puntos clave para el correcto desarrollo del acto.",
        "Se han comprobado las desviaciones producidas en los indicadores de calidad y puntos clave, y se han previsto las medidas de corrección correspondientes para ediciones posteriores.",
        "Se han valorado los actos protocolarios como medio coadyuvante a la estrategia en los negocios y en la mejora de las relaciones internas de la empresa.",
        "Se han analizado los aspectos de seguridad adecuados en función del tipo de acto y/o invitados y cómo pueden afectar a la organización.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los elementos que conforman el protocolo institucional y las clases de público al que puede dirigirse.",
        "Se ha valorado la importancia del conocimiento y seguimiento de los manuales de protocolo y relaciones públicas definidos en las instituciones.",
        "Se ha caracterizado el diseño, planificación y programación del acto protocolario en función del evento que se va a organizar.",
        "Se han descrito los principales elementos simbólicos y/o de representación en los actos institucionales (banderas, himnos y otros).",
        "Se han identificado las técnicas de funcionamiento, planificación y organización de actos protocolarios institucionales.",
        "Se ha definido y/o cumplimentado la documentación necesaria según el acto, para su correcto desarrollo.",
        "Se ha calculado el presupuesto económico del acto que se va a organizar.",
        "Se han comprobado las partidas presupuestarias reservadas para el acto, así como el cumplimento de procedimientos y plazos de los trámites necesarios.",
        "Se han definido los indicadores de calidad y puntos clave para el correcto desarrollo del acto.",
        "Se han valorado los actos protocolarios institucionales como el medio de comunicación y relación entre instituciones.",
        "Se han analizado los aspectos de seguridad adecuados y la correcta coordinación con los servicios de seguridad de las instituciones implicadas en un acto protocolario.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de las relaciones públicas como elemento estratégico en el trato con clientes, internos y externos, usuarios, proveedores y terceros relacionados con la empresa (“stakeholders”).",
        "Se han descrito los componentes de las relaciones públicas (saber estar, educación social, indumentaria, etiqueta, saludo, invitación formal, despedida y tiempos, entre otros).",
        "Se han analizado los objetivos y fases del protocolo interno atendiendo al organigrama funcional de la empresa/ departamento y las relaciones funcionales establecidas.",
        "Se han analizado y descrito los objetivos y fases del protocolo externo según el cliente/usuario.",
        "Se han especificado las modalidades de atención al cliente/usuario y los diferentes proveedores externos necesarios para su desarrollo.",
        "Se han analizado las técnicas de relaciones públicas y de protocolo relacionadas con los medios de comunicación.",
        "Se han aplicado las acciones del contacto directo y no directo, respetando las normas de deontología profesional.",
        "Se han demostrado las actitudes y aptitudes de profesionales en los procesos de atención al cliente.",
        "Se han definido las técnicas de dinamización e interacción grupal.",
        "Se ha mantenido la confidencialidad y privacidad, ajustando sus actuaciones al código deontológico de la profesión.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido los compromisos de calidad y garantía que ofrece la empresa a su usuario/cliente, y las normativas de consumo a las que está sujeto.",
        "Se han descrito las implicaciones de las políticas empresariales relativas a la responsabilidad social corporativa.",
        "Se han definido las características principales de los centros de atención al cliente y de las cartas de servicio.",
        "Se han definido y analizado los conceptos formales y no formales de quejas, reclamaciones y sugerencias.",
        "Se ha valorado la importancia de las quejas, reclamaciones y sugerencias como elemento de mejora continua.",
        "Se ha analizado la normativa legal vigente en materia de reclamaciones de clientes en establecimientos de empresas.",
        "Se han diseñado los puntos clave que debe contener un manual corporativo de atención al cliente/usuario y gestión de quejas y reclamaciones.",
        "Se ha valorado la importancia de tener una actitud empática hacia el cliente/usuario.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado las expectativas de los diferentes tipos de clientes/usuarios.",
        "Se han definido las fases para la implantación de un servicio o procedimiento de atención al cliente/usuario, incluyendo la faceta de control de calidad del mismo.",
        "Se han descrito las claves para lograr una actitud de empatía con el cliente/usuario.",
        "Se ha valorado la importancia de una actitud de simpatía.",
        "Se ha valorado en todo momento una actitud de respeto hacia los clientes, superiores y compañeros.",
        "Se han definido variables de diseño para todos a la hora de la planificación y desarrollo de la atención al cliente/ usuario.",
        "Se ha supervisado la atención al cliente en las instancias que dependan del asistente de dirección.",
        "Se han seguido procedimientos y actitudes conforme a la imagen corporativa.",
        "Se ha valorado la importancia de integrar la cultura de empresa en la atención al cliente/usuario para el logro de los objetivos establecidos en la organización.",
        "Se ha mantenido la confidencialidad y privacidad, ajustando sus actuaciones al código deontológico de la profesión.",
    ], start=1)],
}

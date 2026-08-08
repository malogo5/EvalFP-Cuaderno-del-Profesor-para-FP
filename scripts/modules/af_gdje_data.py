"""EvalFP — Gestión de la documentación jurídica y empresarial · 0647 · Administración y Finanzas
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 67 h · 2 h/semana · 1º AF.
"""
MODULO = {
    "nombre":"Gestión de la documentación jurídica y empresarial","codigo":"0647","abrev":"GDJE",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"1º AF","horas_sem":2,"total_horas":67,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Las administraciones públicas y el Derecho","horas":10,"eval":1,"tags":"Constitución · Poderes del Estado · Unión Europea · Jerarquía normativa · Boletines oficiales"},
    {"id":"UT2","nombre":"Búsqueda y actualización de información jurídica","horas":12,"eval":1,"tags":"Bases de datos jurídicas · Boletines oficiales · Legislación aplicable · Archivo de normativa"},
    {"id":"UT3","nombre":"Documentación jurídica de la empresa","horas":13,"eval":2,"tags":"Escritura de constitución · Estatutos · Libros societarios · Registro Mercantil · Poderes"},
    {"id":"UT4","nombre":"Contratos privados y documentos de fe pública","horas":13,"eval":2,"tags":"Compraventa · Arrendamiento · Notaría · Registro de la Propiedad · Contratos mercantiles"},
    {"id":"UT5","nombre":"Trámites ante organismos públicos","horas":19,"eval":3,"tags":"Procedimiento administrativo · Plazos · Recursos · Sede electrónica · Certificado digital"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Caracteriza la estructura y organización de las administraciones públicas establecidas en la Constitución española y la UE, reconociendo los organismos, instituciones y personas que las integran."},
    {"id":"RA2","pond":18,"nombre":"Actualiza periódicamente la información jurídica requerida por la actividad empresarial, seleccionando la legislación y jurisprudencia relacionada con la organización."},
    {"id":"RA3","pond":20,"nombre":"Organiza los documentos jurídicos relativos a la constitución y funcionamiento de las entidades, cumpliendo la normativa civil y mercantil vigente según las directrices definidas."},
    {"id":"RA4","pond":20,"nombre":"Cumplimenta los modelos de contratación privados más habituales en el ámbito empresarial o documentos de fe pública, aplicando la normativa vigente y los medios informáticos disponibles para su presentación y firma."},
    {"id":"RA5","pond":27,"nombre":"Elabora la documentación requerida por los organismos públicos relativos a los distintos procedimientos administrativos, cumpliendo con la legislación vigente y las directrices definidas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","examen"],
    "RA3":["practica","examen"],
    "RA4":["practica","examen"],
    "RA5":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los poderes públicos establecidos en la Constitución española y sus respectivas funciones.",
        "Se han determinado los órganos de gobierno de cada uno de los poderes públicos así como sus funciones, conforme a su legislación específica.",
        "Se han identificado los principales órganos de gobierno del poder ejecutivo de las administraciones autonómicas y locales así como sus funciones.",
        "Se han definido la estructura y funciones básicas de las principales instituciones de la Unión Europea.",
        "Se han descrito las funciones o competencias de los órganos y la normativa aplicable a los mismos.",
        "Se han descrito las relaciones entre los diferentes órganos de la Unión Europea y el resto de las Administraciones nacionales, así como la incidencia de la normativa europea en la nacional.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las fuentes del Derecho de acuerdo con el ordenamiento jurídico.",
        "Se han precisado las características de las normas jurídicas y de los órganos que las elaboran, dictan, aprueban y publican.",
        "Se han relacionado las leyes con el resto de normas que las desarrollan, identificando los órganos responsables de su aprobación y tramitación.",
        "Se ha identificado la estructura de los boletines oficiales, incluido el diario oficial de la Unión Europea, como medio de publicidad de las normas.",
        "Se han seleccionado distintas fuentes o bases de datos de documentación jurídica tradicionales y/o en Internet, estableciendo accesos directos a las mismas para agilizar los procesos de búsqueda y localización de información.",
        "Se ha detectado la aparición de nueva normativa, jurisprudencia, notificaciones, etc., consultando habitualmente las bases de datos jurídicas que puedan afectar a la entidad.",
        "Se ha archivado la información encontrada en los soportes o formatos establecidos, para posteriormente trasmitirla a los departamentos correspondientes de la organización.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las diferencias y similitudes entre las distintas formas jurídicas de empresa.",
        "Se ha determinado el proceso de constitución de una sociedad mercantil y se ha indicado la normativa mercantil aplicable y los documentos jurídicos que se generan.",
        "Se han precisado las funciones de los fedatarios y los registros públicos, y la estructura y características de los documentos públicos habituales en el ámbito de los negocios.",
        "Se han descrito y analizado las características y los aspectos más significativos de los modelos de documentos más habituales en la vida societaria: estatutos, escrituras y actas, entre otros.",
        "Se han elaborado documentos societarios a partir de los datos aportados, modificando y adaptando los modelos disponibles.",
        "Se ha reconocido la importancia de la actuación de los fedatarios en la elevación a público de los documentos, estimando las consecuencias de no realizar los trámites oportunos.",
        "Se han determinado las peculiaridades de la documentación mercantil acorde al objeto social de la empresa.",
        "Se ha verificado el cumplimiento de las características y requisitos formales de los libros de la sociedad exigidos por la normativa mercantil.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito el concepto de contrato y la capacidad para contratar según la normativa española.",
        "Se han identificado las distintas modalidades de contratación y sus características.",
        "Se han identificado las normas relacionadas con los distintos tipos de contratos del ámbito empresarial.",
        "Se ha recopilado y cotejado la información y documentación necesaria para la cumplimentación de cada contrato, de acuerdo con las instrucciones recibidas.",
        "Se han cumplimentado los modelos normalizados, utilizando aplicaciones informáticas, de acuerdo con la información recopilada y las instrucciones recibidas.",
        "Se han verificado los datos de cada documento, comprobando el cumplimiento y exactitud de los requisitos contractuales y legales.",
        "Se ha valorado la utilización de la firma digital y certificados de autenticidad en la elaboración de los documentos que lo permitan.",
        "Se han aplicado las normas de seguridad y confidencialidad de la información en el uso y la custodia de los documentos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido el concepto y fases del procedimiento administrativo común de acuerdo con la normativa aplicable.",
        "Se han determinado las características, requisitos legales y de formato de los documentos oficiales más habituales, generados en cada una de las fases del procedimiento administrativo y recursos ante lo contencioso-administrativo.",
        "Se ha recopilado la información necesaria para la elaboración de la documentación administrativa o judicial, de acuerdo con los objetivos del documento.",
        "Se han cumplimentado los impresos, modelos o documentación tipo, de acuerdo con los datos e información disponible y los requisitos legales establecidos.",
        "Se ha valorado la importancia de los plazos de formulación de la documentación.",
        "Se han preparado las renovaciones o acciones periódicas derivadas de las obligaciones con las administraciones públicas, para su presentación al organismo correspondiente.",
        "Se han descrito las características de la firma electrónica, sus efectos jurídicos, el proceso para su obtención y la normativa estatal y europea que la regula.",
        "Se ha establecido el procedimiento para la solicitud de la certificación electrónica para la presentación de los modelos oficiales por vía telemática.",
        "Se han descrito los derechos de las corporaciones y los ciudadanos en relación con la presentación de documentos ante la Administración.",
        "Se han determinado los trámites y presentación de documentos tipo en los procesos y procedimientos de contratación pública y concesión de subvenciones, según las bases de las convocatorias y la normativa de aplicación.",
        "Se han determinado las condiciones de custodia de los documentos y expedientes relacionados con las administraciones públicas, garantizando su conservación e integridad.",
    ], start=1)],
}

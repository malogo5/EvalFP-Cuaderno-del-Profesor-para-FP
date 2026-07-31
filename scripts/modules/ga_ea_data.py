"""EvalFP — Empresa y Administración · 0439 · Gestión Administrativa
Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 105 h · 3 h/semana · 1º GA.
"""
MODULO = {
    "nombre":"Empresa y Administración","codigo":"0439","abrev":"EA",
    "ciclo":"Gestión Administrativa","ciclo_clave":"GA","ciclo_nivel":"CFGM",
    "curso":"1º GA","horas_sem":3,"total_horas":105,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 251/2011, de 12/08/2011, por el que se establece el currículo del ciclo formativo de grado medio de Gestión Administrativa en Castilla-La Mancha (DOCM 22/08/2011)",
}
UTS = [
    {"id":"UT1","nombre":"Innovación y creación de empresas","horas":15,"eval":1,"tags":"Innovación empresarial · Emprendimiento · Plan de empresa · Ayudas y subvenciones"},
    {"id":"UT2","nombre":"La empresa y su forma jurídica","horas":13,"eval":1,"tags":"Empresario individual · Sociedades · Trámites de constitución · Registro Mercantil"},
    {"id":"UT3","nombre":"El sistema tributario español","horas":15,"eval":2,"tags":"Tributos, tasas y contribuciones · LGT · Elementos del tributo · Hecho imponible"},
    {"id":"UT4","nombre":"Obligaciones fiscales de la empresa","horas":17,"eval":2,"tags":"Censo · IAE · IRPF · Impuesto de Sociedades · IVA · Calendario fiscal"},
    {"id":"UT5","nombre":"La Administración Pública","horas":12,"eval":3,"tags":"Administración General, autonómica y local · Poderes del Estado · Personal al servicio"},
    {"id":"UT6","nombre":"El procedimiento administrativo","horas":21,"eval":3,"tags":"Acto administrativo · Fases · Silencio administrativo · Recursos · Notificaciones"},
    {"id":"UT7","nombre":"Registros y Administración electrónica","horas":12,"eval":3,"tags":"Registro de entrada y salida · Certificado digital · Sede electrónica · Compulsas"},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Describe las características inherentes a la innovación empresarial relacionándolas con la actividad de creación de empresas."},
    {"id":"RA2","pond":12,"nombre":"Identifica el concepto de empresa y empresario o empresaria analizando su forma jurídica y la normativa a la que está sujeto."},
    {"id":"RA3","pond":14,"nombre":"Analiza el sistema tributario español reconociendo sus finalidades básicas así como las de los principales tribu - tos."},
    {"id":"RA4","pond":16,"nombre":"Identifica las obligaciones fiscales de la empresa diferenciando los tributos a los que está sujeta."},
    {"id":"RA5","pond":12,"nombre":"Identifica la estructura funcional y jurídica de la Administración Pública, reconociendo los diferentes organismos y personas que la integran."},
    {"id":"RA6","pond":20,"nombre":"Describe los diferentes tipos de relaciones entre los administrados y la Administración y sus características com - pletando documentación que de éstas surge."},
    {"id":"RA7","pond":12,"nombre":"Realiza gestiones de obtención de información y presentación de documentos ante las Administraciones Públicas identificando los distintos tipos de registros públicos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado las diversas posibilidades de innovación empresarial (técnicas, materiales, de organización interna y externa, entre otras), relacionándolas como fuentes de desarrollo económico y creación de empleo.",
        "Se han descrito las implicaciones que tiene para la competitividad empresarial la innovación y la iniciativa em - prendedora.",
        "Se han comparado y documentado diferentes experiencias de innovación empresarial, describiendo y valorando los factores de riesgo asumidos en cada una de ellas.",
        "Se han definido las características de empresas de base tecnológica, relacionándolas con los distintos sectores económicos.",
        "Se han enumerado algunas iniciativas innovadoras que puedan aplicarse a empresas u organizaciones ya exis - tentes para su mejora.",
        "Se han analizado posibilidades de internacionalización de algunas empresas como factor de innovación de las mismas.",
        "Se han buscado ayudas y herramientas, públicas y privadas, para la innovación, creación e internacionalización de empresas, relacionándolas estructuradamente en un informe.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido el concepto de empresa.",
        "Se ha distinguido entre personalidad física y jurídica.",
        "Se ha diferenciado la empresa según su constitución legal.",
        "Se han reconocido las características de la empresaria o empresario autónomo.",
        "Se han precisado las características de los diferentes tipos de sociedades.",
        "Se ha identificado la forma jurídica más adecuada para cada tipo de empresa.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha relacionado la obligación tributaria con su finalidad socioeconómica.",
        "Se ha reconocido la jerarquía normativa tributaria.",
        "Se han identificado los diferentes tipos de tributos.",
        "Se han discriminado sus principales características.",
        "Se ha diferenciado entre impuestos directos e indirectos.",
        "Se han identificado los elementos de la declaración-liquidación.",
        "Se han reconocido las formas de extinción de las deudas tributarias.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido las obligaciones fiscales de la empresa.",
        "Se ha precisado la necesidad de alta en el censo.",
        "Se han reconocido las empresas sujetas al pago del Impuesto de Actividades Económicas.",
        "Se han reconocido las características generales del Impuesto sobre el Valor Añadido y sus diferentes regímenes.",
        "Se han interpretado los modelos de liquidación del IVA, reconociendo los plazos de declaración-liquidación.",
        "Se ha reconocido la naturaleza y ámbito de aplicación del Impuesto sobre la Renta de las Personas Físicas.",
        "Se han cumplimentado los modelos de liquidación de IRPF, reconociendo los plazos de declaración-liquidación.",
        "Se ha identificado la naturaleza y los elementos del impuesto de sociedades.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado el marco jurídico en el que se integran las Administraciones Públicas.",
        "Se han reconocido las organizaciones que componen las diferentes Administraciones Públicas.",
        "Se han interpretado las relaciones entre las diferentes Administraciones Públicas.",
        "Se han obtenido diversas informaciones de las Administraciones Públicas por las diversas vías de acceso a las mismas y relacionado éstas en un informe.",
        "Se han precisado las distintas formas de relación laboral en la Administración Pública.",
        "Se han utilizado las fuentes de información relacionadas con la oferta de empleo público para reunir datos signi - ficativos sobre ésta.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido el concepto de acto administrativo.",
        "Se han clasificado los diferentes actos administrativos.",
        "Se ha definido el proceso administrativo, sus tipos, fases y tipos de silencio.",
        "Se han precisado los diferentes tipos de contratos administrativos.",
        "Se ha definido el concepto de recurso administrativo y diferenciado sus tipos.",
        "Se han identificado los actos recurribles y no recurribles.",
        "Se han diferenciado los diferentes tipos de recursos administrativos.",
        "Se han verificado las condiciones para la interposición de un recurso administrativo.",
        "Se ha precisado los diferentes órganos de la jurisdicción contencioso-administrativa y su ámbito de aplicación.",
        "Se han relacionado las fases el procedimiento contencioso-administrativo.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han observado las normas de presentación de documentos ante la Administración.",
        "Se han reconocido las funciones de los Archivos Públicos.",
        "Se ha solicitado determinada información en un Registro Público.",
        "Se ha reconocido el derecho a la información, atención y participación de la ciudadanía.",
        "Se ha accedido a las oficinas de información y atención a la ciudadanía por vías como las páginas Web, ventani - llas únicas y atención telefónica para obtener información relevante y relacionarla en un informe tipo.",
        "Se han identificado y descrito los límites al derecho a la información relacionados con los datos en poder de las Administraciones Públicas sobre las personas administradas.",
    ], start=1)],
}

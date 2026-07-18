"""EvalFP — Lenguajes de Marcas y Sistemas de Gestión de Información · 0483 · 1º DAM
RD 450/2010, de 16 de abril (BOE) · Decreto CLM 252/2011, de 17 de noviembre (DOCM)
"""
MODULO = {
    "nombre":"Lenguajes de Marcas y Sistemas de Gestión de Información","codigo":"0483","abrev":"LMSGI",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"1º DAM","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 450/2010, de 16 de abril · Decreto CLM 252/2011, de 17 de noviembre (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de las características del lenguaje XML","horas":25,"eval":1,"tags":"XML · DTD · XSD · Validación · Namespaces · Parsers SAX/DOM"},
    {"id":"UT2","nombre":"Utilización de lenguajes de marcas en entornos web","horas":35,"eval":1,"tags":"HTML5 · CSS3 · Accesibilidad · SEO · Semántica · Responsive"},
    {"id":"UT3","nombre":"Aplicación en la transmisión de información","horas":30,"eval":2,"tags":"JSON · YAML · RSS · Atom · XSLT · XPath · API REST"},
    {"id":"UT4","nombre":"Definición de esquemas y vocabularios XML","horas":20,"eval":2,"tags":"XSD · RelaxNG · Namespaces · Validación · Herramientas"},
    {"id":"UT5","nombre":"Conversión y transformación de documentos XML","horas":18,"eval":3,"tags":"XSLT · XPath · Plantillas · Saxon · Procesadores XSLT"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce las características de los lenguajes de marcas analizando e interpretando fragmentos de código."},
    {"id":"RA2","pond":20,"nombre":"Utiliza lenguajes de marcas para la transmisión y presentación de información a través de la web evaluando su funcionalidad."},
    {"id":"RA3","pond":20,"nombre":"Accede y manipula documentos web utilizando lenguajes de script de cliente."},
    {"id":"RA4","pond":25,"nombre":"Establece mecanismos de validación de documentos XML utilizando técnicas y herramientas específicas."},
    {"id":"RA5","pond":20,"nombre":"Realiza conversiones sobre documentos XML utilizando técnicas y herramientas de procesamiento."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características generales de los lenguajes de marcas.",
        "Se han reconocido las ventajas que proporcionan en el tratamiento de la información.",
        "Se han clasificado los lenguajes de marcas e identificado los más relevantes.",
        "Se han diferenciado sus ámbitos de aplicación.",
        "Se ha reconocido la necesidad y los ámbitos específicos de aplicación de XML.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y clasificado los lenguajes de marcas relacionados con la web y sus versiones.",
        "Se ha analizado la estructura de un documento HTML e identificado las secciones que lo componen.",
        "Se ha reconocido la funcionalidad de las principales etiquetas y atributos del lenguaje HTML.",
        "Se han establecido las semejanzas y diferencias entre los lenguajes HTML y XHTML.",
        "Se han utilizado hojas de estilo CSS para dar formato y presentación a los documentos web.",
        "Se han utilizado herramientas en la creación de documentos web.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las tecnologías y lenguajes de script de cliente relacionados con la web.",
        "Se ha identificado la sintaxis básica del lenguaje de script de cliente.",
        "Se han utilizado métodos para la selección y acceso a elementos de documentos web.",
        "Se han creado y modificado elementos de documentos web mediante scripting.",
        "Se han eliminado elementos de documentos web y gestionado eventos básicos.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la necesidad de describir la información en documentos XML.",
        "Se han identificado las tecnologías relacionadas con la definición de documentos XML.",
        "Se ha analizado la estructura de una definición de tipo de documento (DTD).",
        "Se ha creado y asociado una DTD a un documento XML.",
        "Se han creado esquemas XML (XSD) como alternativa a los DTD.",
        "Se han utilizado herramientas específicas de validación de documentos XML.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la necesidad de la conversión de documentos XML.",
        "Se han establecido ámbitos de aplicación de las transformaciones XSLT.",
        "Se han analizado las tecnologías implicadas y su modo de funcionamiento.",
        "Se ha descrito la sintaxis de las hojas de estilo XSL y sus elementos.",
        "Se han utilizado plantillas y se han aplicado transformaciones XSLT sobre documentos XML.",
    ], start=1)],
}

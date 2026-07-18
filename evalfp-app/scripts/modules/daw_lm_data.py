"""EvalFP — Lenguajes de Marcas y Sistemas de Gestión de Información · 0373 · 1º DAW
RD 686/2010, de 20 de mayo (BOE) · Decreto CLM 230/2011, de 28 de julio (DOCM)
"""
MODULO = {
    "nombre":"Lenguajes de Marcas y Sistemas de Gestión de Información","codigo":"0373","abrev":"LMSGI",
    "ciclo":"Desarrollo de Aplicaciones Web","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"1º DAW","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 686/2010, de 20 de mayo · Decreto CLM 230/2011, de 28 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de las características del lenguaje XML","horas":25,"eval":1,"tags":"XML · DTD · XSD · Validación · Namespaces · Parsers SAX/DOM"},
    {"id":"UT2","nombre":"Utilización de lenguajes de marcas en entornos web","horas":35,"eval":1,"tags":"HTML5 · CSS3 · Accesibilidad · SEO · Semántica · Responsive"},
    {"id":"UT3","nombre":"Aplicación de los lenguajes de marcas en la transmisión de información","horas":30,"eval":2,"tags":"JSON · YAML · RSS · Atom · XSLT · XPath · API REST"},
    {"id":"UT4","nombre":"Gestión de la información en el sistema ERP-CRM","horas":20,"eval":3,"tags":"ERP · CRM · Exportar/Importar · Formularios · Informes · Integración"},
    {"id":"UT5","nombre":"Sistemas de gestión empresarial","horas":18,"eval":3,"tags":"Odoo · SugarCRM · Módulos · Workflow · Usuarios · Configuración"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce las características de los lenguajes de marcas analizando e interpretando fragmentos de código."},
    {"id":"RA2","pond":20,"nombre":"Utiliza lenguajes de marcas para la transmisión y presentación de información a través de la web evaluando su funcionalidad."},
    {"id":"RA3","pond":20,"nombre":"Accede y manipula documentos web utilizando lenguajes de script de cliente."},
    {"id":"RA4","pond":20,"nombre":"Establece mecanismos de validación de documentos XML utilizando técnicas y herramientas específicas."},
    {"id":"RA5","pond":15,"nombre":"Realiza conversiones sobre documentos XML utilizando técnicas y herramientas de procesamiento."},
    {"id":"RA6","pond":10,"nombre":"Gestiona información en sistemas ERP/CRM evaluando y utilizando módulos relevantes."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT1","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA5",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA6",["CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características generales de los lenguajes de marcas.",
        "Se han reconocido las ventajas que proporcionan en el tratamiento de la información.",
        "Se han clasificado los lenguajes de marcas e identificado los más relevantes.",
        "Se han diferenciado sus ámbitos de aplicación.",
        "Se ha reconocido la necesidad y los ámbitos específicos de aplicación de un lenguaje de marcas de propósito general.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y clasificado los lenguajes de marcas relacionados con la web y sus diferentes versiones.",
        "Se ha analizado la estructura de un documento HTML e identificado las secciones que lo componen.",
        "Se ha reconocido la funcionalidad de las principales etiquetas y atributos del lenguaje HTML.",
        "Se han establecido las semejanzas y diferencias entre los lenguajes HTML y XHTML.",
        "Se han utilizado herramientas en la creación de documentos web.",
        "Se han identificado las ventajas que aporta la utilización de hojas de estilo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las tecnologías y los lenguajes de script de cliente relacionados con los lenguajes de marcas para la web.",
        "Se ha identificado la sintaxis básica del lenguaje de script de cliente.",
        "Se han utilizado métodos para la selección y acceso a elementos de documentos web.",
        "Se han creado y modificado elementos de documentos web.",
        "Se han eliminado elementos de documentos web.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la necesidad de describir la información transmitida en los documentos XML y sus reglas.",
        "Se han identificado las tecnologías relacionadas con la definición de documentos XML.",
        "Se ha analizado la estructura de una definición de tipo de documento (DTD).",
        "Se ha creado y asociado una definición de tipo de documento (DTD) a un documento XML.",
        "Se han identificado los tipos de elementos y atributos en una definición de tipo de documento (DTD).",
        "Se han utilizado herramientas específicas de validación de documentos XML.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la necesidad de la conversión de documentos XML.",
        "Se han establecido ámbitos de aplicación.",
        "Se han analizado las tecnologías implicadas y su modo de funcionamiento.",
        "Se ha descrito la sintaxis de las hojas de estilo XSL y sus elementos.",
        "Se han utilizado plantillas y se ha aplicado transformaciones XSLT.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las principales funciones de los sistemas ERP-CRM.",
        "Se han reconocido las ventajas de los sistemas ERP-CRM frente a aplicaciones aisladas.",
        "Se han evaluado las funcionalidades y los módulos más habituales de los sistemas ERP-CRM.",
        "Se han instalado, configurado y administrado un sistema ERP-CRM.",
        "Se han importado y exportado datos en el sistema ERP-CRM desde y hacia documentos XML.",
        "Se han diseñado e implementado formularios e informes en el sistema ERP-CRM.",
        "Se ha realizado la integración de módulos y funcionalidades del sistema ERP-CRM.",
    ], start=1)],
}

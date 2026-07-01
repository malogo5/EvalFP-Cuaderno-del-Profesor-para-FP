"""
EvalFP — Lenguajes de Marcas y Sistemas de Gestión de Información (LMSGI)
Módulo: 0373 · 1º ASIR / 1º DAM / 1º DAW · Ciclos: ASIR, DAM, DAW
Decreto: RD 1629/2009 (ASIR), RD 450/2010 (DAM), RD 686/2010 (DAW)
"""

MODULO = {
    "nombre":      "Lenguajes de Marcas y Sistemas de Gestión de Información",
    "codigo":      "0373",
    "abrev":       "LMSGI",
    "ciclo":       "ASIR / DAM / DAW",
    "curso":       "1º",
    "horas_sem":   3,
    "total_horas": 96,
    "anno":        "2026-2027",
    "eval_count":  3,
    "ciclo_clave": "ASIR",
    "ciclo_nivel": "CFGS",
    "decreto": "RD 1629/2009 / RD 450/2010 / RD 686/2010 · Decreto CLM 200/2010, 252/2011, 230/2011 (DOCM)",
}

UTS = [
    {"id":"UT1","nombre":"Reconocimiento de las características de los lenguajes de marcas","horas":12,"eval":1,"tags":"HTML · XML · SGML · Markdown"},
    {"id":"UT2","nombre":"Utilización de lenguajes de marcas en entornos web (HTML/CSS)","horas":25,"eval":1,"tags":"HTML5 · CSS3 · Semántica · Accesibilidad"},
    {"id":"UT3","nombre":"Manipulación de documentos XML","horas":20,"eval":2,"tags":"DTD · XML Schema · XPath · XSLT"},
    {"id":"UT4","nombre":"Definición de esquemas y vocabularios XML","horas":15,"eval":2,"tags":"XML Schema · RelaxNG · Namespaces"},
    {"id":"UT5","nombre":"Conversión y adaptación de documentos XML","horas":12,"eval":3,"tags":"XSLT · XQuery · Saxon"},
    {"id":"UT6","nombre":"Almacenamiento y gestión de la información en XML/JSON","horas":12,"eval":3,"tags":"BBDD nativas XML · JSON · REST"},
]

RAS = [
    {"id":"RA1","pond":10,"nombre":"Reconoce las características de los lenguajes de marcas analizando e interpretando fragmentos de código."},
    {"id":"RA2","pond":25,"nombre":"Utiliza lenguajes de marcas para la transmisión y presentación de información a través de la web, evaluando su utilidad e interoperabilidad."},
    {"id":"RA3","pond":20,"nombre":"Establece mecanismos de validación de documentos XML utilizando técnicas y herramientas de validación."},
    {"id":"RA4","pond":15,"nombre":"Identifica la estructura de un documento XML y crea definiciones de tipo de documento (DTD) y esquemas XML."},
    {"id":"RA5","pond":15,"nombre":"Realiza conversiones sobre documentos XML utilizando técnicas y herramientas de transformación de documentos."},
    {"id":"RA6","pond":15,"nombre":"Gestiona la información en formato XML, utilizando técnicas de almacenamiento y consulta de información en bases de datos nativas XML y relacionales."},
]

ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]

EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}

CES = {
    "RA1": [
        {"id":"CR1","texto":"Se han identificado las características generales de los lenguajes de marcas."},
        {"id":"CR2","texto":"Se han reconocido las ventajas que proporcionan en el tratamiento de la información."},
        {"id":"CR3","texto":"Se han clasificado los lenguajes de marcas e identificado los más relevantes."},
        {"id":"CR4","texto":"Se han diferenciado sus ámbitos de aplicación."},
        {"id":"CR5","texto":"Se ha reconocido la necesidad de la estandarización y los organismos que la promueven."},
        {"id":"CR6","texto":"Se han identificado las tecnologías relacionadas con los lenguajes de marcas para el tratamiento de la información."},
    ],
    "RA2": [
        {"id":"CR1","texto":"Se han identificado y utilizado las etiquetas y los atributos de HTML."},
        {"id":"CR2","texto":"Se han creado páginas web bien formadas y con significado semántico."},
        {"id":"CR3","texto":"Se ha reconocido la funcionalidad de los estilos CSS."},
        {"id":"CR4","texto":"Se han enlazado estilos con páginas web."},
        {"id":"CR5","texto":"Se han creado y vinculado hojas de estilos."},
        {"id":"CR6","texto":"Se han utilizado herramientas de validación de documentos HTML y CSS."},
        {"id":"CR7","texto":"Se han identificado las ventajas que aporta la utilización de hojas de estilos."},
    ],
    "RA3": [
        {"id":"CR1","texto":"Se ha establecido la necesidad de describir la información transmitida en los documentos XML y sus reglas."},
        {"id":"CR2","texto":"Se han identificado las tecnologías relacionadas con la definición de documentos XML (DTD y XML Schema)."},
        {"id":"CR3","texto":"Se ha analizado la estructura de un documento XML."},
        {"id":"CR4","texto":"Se han creado definiciones de tipo de documento."},
        {"id":"CR5","texto":"Se ha creado el vocabulario XML aplicando una definición de tipo de documento."},
        {"id":"CR6","texto":"Se han utilizado herramientas de validación de documentos XML."},
    ],
    "RA4": [
        {"id":"CR1","texto":"Se han establecido las tecnologías de definición de documentos XML."},
        {"id":"CR2","texto":"Se ha analizado la estructura de un esquema XML."},
        {"id":"CR3","texto":"Se han creado esquemas XML."},
        {"id":"CR4","texto":"Se han utilizado esquemas XML para la validación de documentos."},
        {"id":"CR5","texto":"Se ha valorado la necesidad de los esquemas XML en el intercambio de información."},
        {"id":"CR6","texto":"Se han utilizado herramientas de creación y validación de esquemas XML."},
        {"id":"CR7","texto":"Se han documentado esquemas XML."},
    ],
    "RA5": [
        {"id":"CR1","texto":"Se ha reconocido la necesidad de la conversión de documentos XML."},
        {"id":"CR2","texto":"Se han establecido ámbitos de aplicación."},
        {"id":"CR3","texto":"Se han analizado las tecnologías de transformación de documentos XML en uso."},
        {"id":"CR4","texto":"Se ha descrito la sintaxis de XSLT."},
        {"id":"CR5","texto":"Se han creado hojas de estilo XSLT."},
        {"id":"CR6","texto":"Se han utilizado herramientas de procesado XSLT."},
    ],
    "RA6": [
        {"id":"CR1","texto":"Se han identificado los principales métodos de almacenamiento de la información usados en XML."},
        {"id":"CR2","texto":"Se han identificado los inconvenientes de almacenar información en formato XML."},
        {"id":"CR3","texto":"Se han establecido tecnologías de almacenamiento nativo de XML."},
        {"id":"CR4","texto":"Se han utilizado sistemas gestores de bases de datos relacionales en el almacenamiento de información en formato XML."},
        {"id":"CR5","texto":"Se han utilizado técnicas específicas para crear documentos XML a partir de información almacenada en bases de datos relacionales."},
        {"id":"CR6","texto":"Se han identificado las características de los sistemas gestores de bases de datos nativas XML."},
    ],
}

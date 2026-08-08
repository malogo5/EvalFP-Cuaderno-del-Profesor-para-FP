"""EvalFP — Lenguajes de Marcas y Sistemas de Gestión de Información · 0373 · ASIR / DAM / DAW
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 116 h · 3 h/semana · 1º ASIR.
"""
MODULO = {
    "nombre":"Lenguajes de Marcas y Sistemas de Gestión de Información","codigo":"0373","abrev":"LMSGI",
    "ciclo":"ASIR / DAM / DAW","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":3,"total_horas":116,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Reconocimiento de las características de los lenguajes de marcas","horas":20,"eval":1,"tags":"HTML · XML · SGML · Markdown"},
    {"id":"UT2","nombre":"Utiliza lenguajes de marcas para la transmisión de información a…","horas":14,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Genera canales de contenidos","horas":14,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Establece mecanismos de validación para documentos XML","horas":14,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Conversión y adaptación de documentos XML","horas":18,"eval":2,"tags":"XSLT · XQuery · Saxon"},
    {"id":"UT6","nombre":"Gestiona información en formato XML","horas":16,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Trabaja con sistemas empresariales de gestión de información…","horas":20,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":17,"nombre":"Reconoce las características de lenguajes de marcas analizando e interpretando fragmentos de código."},
    {"id":"RA2","pond":12,"nombre":"Utiliza lenguajes de marcas para la transmisión de información a través de la Web analizando la estructura de los documentos e identificando sus elementos."},
    {"id":"RA3","pond":12,"nombre":"Genera canales de contenidos analizando y utilizando tecnologías de sindicación."},
    {"id":"RA4","pond":12,"nombre":"Establece mecanismos de validación para documentos XML utilizando métodos para definir su sintaxis y estructura."},
    {"id":"RA5","pond":16,"nombre":"Realiza conversiones sobre documentos XML utilizando técnicas y herramientas de procesamiento."},
    {"id":"RA6","pond":14,"nombre":"Gestiona información en formato XML analizando y utilizando tecnologías de almacenamiento y lenguajes de consulta."},
    {"id":"RA7","pond":17,"nombre":"Trabaja con sistemas empresariales de gestión de información realizando tareas de importación, integración, aseguramiento y extracción de la información."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características generales de los lenguajes de marcas.",
        "Se han reconocido las ventajas que proporcionan en el tratamiento de la información.",
        "Se han clasificado los lenguajes de marcas e identificado los más relevantes.",
        "Se han diferenciado sus ámbitos de aplicación.",
        "Se ha reconocido la necesidad y los ámbitos específicos de aplicación de un lenguaje de marcas de propósito general.",
        "Se han analizado las características propias del lenguaje XML.",
        "Se ha identificado la estructura de un documento XML y sus reglas sintácticas.",
        "Se ha contrastado la necesidad de crear documentos XML bien formados y la influencia en su procesamiento.",
        "Se han identificado las ventajas que aportan los espacios de nombres.",
        "Se conocen los mecanismos de codificación XML propios de cada idioma.",
        "Se conocen los fundamentos básicos de programación",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y clasificado los lenguajes de marcas relacionados con la Web y sus diferentes versiones.",
        "Se ha analizado la estructura de un documento HTML e identificado las secciones que lo componen.",
        "Se ha reconocido la funcionalidad de las principales etiquetas y atributos del lenguaje HTML.",
        "Se han establecido las semejanzas y diferencias entre los lenguajes HTML y XHTML.",
        "Se ha reconocido la utilidad de XHTML en los sistemas de gestión de información.",
        "Se han utilizado herramientas en la creación documentos Web.",
        "Se han identificado las ventajas que aporta la utilización de hojas de estilo.",
        "Se han aplicado hojas de estilo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las ventajas que aporta la sindicación de contenidos en la gestión y transmisión de la información.",
        "Se han definido sus ámbitos de aplicación.",
        "Se han analizado las tecnologías en que se basa la sindicación de contenidos.",
        "Se ha identificado la estructura y la sintaxis de un canal de contenidos.",
        "Se han creado y validado canales de contenidos.",
        "Se ha comprobado la funcionalidad y el acceso a los canales.",
        "Se han utilizado herramientas específicas como agregadores y directorios de canales.",
        "Se conocen las características distintivas de distintos formatos de agregación en XML.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la necesidad de describir la información transmitida en los documentos XML y sus reglas.",
        "Se han identificado las tecnologías relacionadas con la definición de documentos XML.",
        "Se ha analizado la estructura y sintaxis específica utilizada en la descripción.",
        "Se han creado descripciones de documentos XML.",
        "Se han utilizado descripciones en la elaboración y validación de documentos XML.",
        "Se han asociado las descripciones con los documentos.",
        "Se han utilizado herramientas específicas.",
        "Se han documentado las descripciones.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la necesidad de la conversión de documentos XML.",
        "Se han establecido ámbitos de aplicación.",
        "Se han analizado las tecnologías implicadas y su modo de funcionamiento.",
        "Se ha descrito la sintaxis específica utilizada en la conversión y adaptación de documentos XML.",
        "Se han creado especificaciones de conversión.",
        "Se han identificado y caracterizado herramientas específicas relacionadas con la conversión de documentos XML.",
        "Se han realizado conversiones con distintos formatos de salida.",
        "Se han documentado y depurado las especificaciones de conversión.",
        "Se ha utilizado el modelo DOM para extraer información de un documento XML.",
        "Se reconoce la importancia del uso de estándares abiertos",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales métodos de almacenamiento de la información usada en documentos XML.",
        "Se han identificado los inconvenientes de almacenar información en formato XML.",
        "Se han establecido tecnologías eficientes de almacenamiento de información en función de sus características.",
        "Se han utilizado sistemas gestores de bases de datos relacionales en el almacenamiento de información en formato XML.",
        "Se han utilizado técnicas específicas para crear documentos XML a partir de información almacenada en bases de datos relacionales.",
        "Se han identificado las características de los sistemas gestores de bases de datos nativas XML.",
        "Se han instalado y analizado sistemas gestores de bases de datos nativas XML.",
        "Se han utilizado técnicas para gestionar la información almacenada en bases de datos nativas XML.",
        "Se han identificado lenguajes y herramientas para el tratamiento y almacenamiento de información y su inclusión en documentos XML.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las ventajas de los sistemas de gestión y planificación de recursos empresariales.",
        "Se han evaluado las características de las principales aplicaciones de gestión empresarial.",
        "Se han instalado aplicaciones de gestión empresarial.",
        "Se han configurado y adaptado las aplicaciones.",
        "Se ha establecido y verificado el acceso seguro a la información.",
        "Se han generado informes.",
        "Se han realizado tareas de integración con aplicaciones ofimáticas.",
        "Se han realizado procedimientos de extracción de información para su tratamiento e incorporación a diversos sistemas.",
        "Se han realizado tareas de asistencia y resolución de incidencias.",
        "Se han elaborado documentos relativos a la explotación de la aplicación.",
        "Se ha procesado información XML procedente una aplicación de gestión empresarial",
    ], start=1)],
}

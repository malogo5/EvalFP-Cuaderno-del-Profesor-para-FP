"""EvalFP — Implantación de Aplicaciones Web · 0376 · Administración de Sistemas Informáticos en Red (ASIR)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 158 h · 4 h/semana · 2º ASIR.
"""
MODULO = {
    "nombre":"Implantación de Aplicaciones Web","codigo":"0376","abrev":"IAW",
    "ciclo":"Administración de Sistemas Informáticos en Red (ASIR)","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"2º ASIR","horas_sem":4,"total_horas":158,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 1º · RA y CE: Decreto 200/2010, de 03/08/2010 (DOCM núm. 151, de 06/08/2010), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Prepara el entorno de desarrollo y los servidores de aplicaciones…","horas":34,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Implanta gestores de contenidos seleccionándolos y estableciendo la…","horas":21,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Administra gestores de contenidos adaptándolos a los requerimientos…","horas":23,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Gestiona aplicaciones de ofimática Web integrando funcionalidades y","horas":21,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Genera documentos Web","horas":23,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Genera documentos Web con acceso a bases de datos","horas":18,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Realiza modificaciones en gestores de contenidos adaptando su…","horas":18,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":21,"nombre":"Prepara el entorno de desarrollo y los servidores de aplicaciones Web instalando e integrando las funcionalidades necesarias."},
    {"id":"RA2","pond":13,"nombre":"Implanta gestores de contenidos seleccionándolos y estableciendo la configuración de sus parámetros."},
    {"id":"RA3","pond":15,"nombre":"Administra gestores de contenidos adaptándolos a los requerimientos y garantizando la integridad de la información."},
    {"id":"RA4","pond":13,"nombre":"Gestiona aplicaciones de ofimática Web integrando funcionalidades y asegurando el acceso a la información."},
    {"id":"RA5","pond":15,"nombre":"Genera documentos Web utilizando lenguajes de guiones de servidor."},
    {"id":"RA6","pond":12,"nombre":"Genera documentos Web con acceso a bases de datos utilizando lenguajes de guiones de servidor."},
    {"id":"RA7","pond":11,"nombre":"Realiza modificaciones en gestores de contenidos adaptando su apariencia y funcionalidades."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
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
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado el software necesario para su funcionamiento.",
        "Se han identificado las diferentes tecnologías empleadas.",
        "Se han instalado y configurado servidores Web y de bases de datos.",
        "Se han reconocido las posibilidades de procesamiento en los entornos cliente y servidor.",
        "Se han añadido y configurado los componentes y módulos necesarios para el procesamiento de código en el servidor.",
        "Se ha instalado y configurado el acceso a bases de datos.",
        "Se ha establecido y verificado la seguridad en los accesos al servidor.",
        "Se han utilizado plataformas integradas orientadas a la prueba y desarrollo de aplicaciones Web.",
        "Se han creado procedimientos para realizar copia de seguridad de la plataforma web.",
        "Se han documentado los procedimientos realizados.",
        "Se han instalado y configurado aplicaciones Web de comercio electrónico (e-commerce).",
        "Se han instalado y configurado aplicaciones Web de educación a distancia (e-learning).",
        "Se han identificado las aplicaciones Web más utilizadas en las Tecnologías de la Información y Comunicación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado el uso y utilidad de los gestores de contenidos.",
        "Se han clasificado según la funcionalidad principal del sitio Web que permiten gestionar.",
        "Se han instalado diferentes tipos de gestores de contenidos.",
        "Se han diferenciado sus características (uso, licencia, entre otras).",
        "Se han personalizado y configurado los gestores de contenidos.",
        "Se han activado y configurado los mecanismos de seguridad proporcionados por los propios gestores de contenidos.",
        "Se han realizado pruebas de funcionamiento.",
        "Se han publicado los gestores de contenidos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han adaptado y configurado los módulos del gestor de contenidos.",
        "Se han creado y gestionado usuarios con distintos perfiles.",
        "Se han integrado módulos atendiendo a requerimientos de funcionalidad.",
        "Se han realizado copias de seguridad de los contenidos.",
        "Se han importado y exportado contenidos en distintos formatos.",
        "Se han gestionado plantillas.",
        "Se han integrado funcionalidades de sindicación.",
        "Se han realizado actualizaciones.",
        "Se han obtenido informes de acceso.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la utilidad de las aplicaciones de ofimática Web.",
        "Se han clasificado según su funcionalidad y prestaciones específicas.",
        "Se han instalado aplicaciones de ofimática Web.",
        "Se han configurado las aplicaciones para integrarlas en una intranet.",
        "Se han gestionado las cuentas de usuario.",
        "Se han aplicado criterios de seguridad en el acceso de los usuarios.",
        "Se han utilizado las aplicaciones de forma cooperativa.",
        "Se ha elaborado documentación relativa al uso y gestión de las aplicaciones.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los lenguajes de guiones de servidor más relevantes.",
        "Se ha reconocido la relación entre los lenguajes de guiones de servidor y los lenguajes de marcas utilizados en los clientes.",
        "Se ha reconocido la sintaxis básica de un lenguaje de guiones concreto.",
        "Se han utilizado estructuras de control del lenguaje.",
        "Se han definido y utilizado funciones.",
        "Se han utilizado formularios para introducir información.",
        "Se han establecido y utilizado mecanismos para asegurar la persistencia de la información entre distintos documentos Web relacionados.",
        "Se ha identificado y asegurado a los usuarios que acceden al documento Web.",
        "Se ha verificado el aislamiento del entorno específico de cada usuario.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los sistemas gestores de bases de datos más utilizados en entornos Web.",
        "Se ha verificado la integración de los sistemas gestores de bases de datos con el lenguaje de guiones de servidor.",
        "Se ha configurado en el lenguaje de guiones la conexión para el acceso al sistema gestor de base de datos.",
        "Se han creado bases de datos y tablas en el gestor utilizando el lenguaje de guiones.",
        "Se ha obtenido y actualizado la información almacenada en bases de datos.",
        "Se han aplicado criterios de seguridad en el acceso de los usuarios.",
        "Se ha verificado el funcionamiento y el rendimiento del sistema.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la estructura de directorios del gestor de contenidos.",
        "Se ha reconocido la funcionalidad de los ficheros que utiliza y su naturaleza (código, imágenes, configuración, entre otros).",
        "Se han seleccionado las funcionalidades que hay que adaptar e incorporar.",
        "Se han identificado los recursos afectados por las modificaciones.",
        "Se ha modificado el código de la aplicación para incorporar nuevas funcionalidades y adaptar otras existentes.",
        "Se ha verificado el correcto funcionamiento de los cambios realizados.",
        "Se han documentado los cambios realizados.",
    ], start=1)],
}

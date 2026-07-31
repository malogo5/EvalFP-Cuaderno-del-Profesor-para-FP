"""EvalFP — Aplicaciones Web · 0228 · Sistemas Microinformáticos y Redes
Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 169 h · 5 h/semana · 1º SMR.
"""
MODULO = {
    "nombre":"Aplicaciones Web","codigo":"0228","abrev":"AW",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":5,"total_horas":169,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Conoce los conceptos básicos de Internet","horas":14,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Elabora páginas web con lenguajes de marcas mediante herramientas…","horas":30,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Instala gestores de contenidos","horas":38,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Instala sistemas de gestión de aprendizaje a distancia","horas":22,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Instala servicios de gestión de archivos web","horas":24,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Instala aplicaciones de ofimática web","horas":22,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Instala aplicaciones web de escritorio","horas":19,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":8,"nombre":"Conoce los conceptos básicos de Internet, sus características, su evolución y sus tendencias."},
    {"id":"RA2","pond":18,"nombre":"Elabora páginas web con lenguajes de marcas mediante herramientas editoras de textos y específicas de desarrollo web, incluyendo scripts de navegador."},
    {"id":"RA3","pond":23,"nombre":"Instala gestores de contenidos, identificando sus aplicaciones y configurándolos según requerimientos."},
    {"id":"RA4","pond":13,"nombre":"Instala sistemas de gestión de aprendizaje a distancia, describiendo la estructura del sitio y la jerarquía de directorios generada."},
    {"id":"RA5","pond":14,"nombre":"Instala servicios de gestión de archivos web, identificando sus aplicaciones y verificando su integridad."},
    {"id":"RA6","pond":13,"nombre":"Instala aplicaciones de ofimática web, describiendo sus características y entornos de uso."},
    {"id":"RA7","pond":11,"nombre":"Instala aplicaciones web de escritorio, describiendo sus características y entornos de uso."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13","CR14"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los conceptos básicos de Internet.",
        "Se ha descrito el esquema de funcionamiento básico de un servicio web.",
        "Se ha descrito la estructura de almacenamiento de la información relacionada con un servicio web.",
        "Se han identificado los conceptos básicos de una base de datos asociada a un servicio web.",
        "Se han descrito las últimas tendencias en Internet, el significado de las redes sociales en Internet y se han analizado sus características y evolución.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características generales de los lenguajes de marcas.",
        "Se ha realizado la estructura de un documento HTML identificado las secciones que lo componen.",
        "Se ha reconocido la funcionalidad de las principales etiquetas y atributos del lenguaje HTML.",
        "Se han establecido las semejanzas y diferencias entre los lenguajes HTML y XHTML.",
        "Se ha reconocido la utilidad de XHTML en los sistemas de gestión de información.",
        "Se han utilizado herramientas en la creación de documentos web.",
        "Se han incluido elementos multimedia en documentos web.",
        "Se han identificado las ventajas que aporta la utilización de hojas de estilo.",
        "Se han aplicado hojas de estilo.",
        "Se han identificado las ventajas que aporta la integración de scritps de navegador en documentos web.",
        "Se han integrado distintos tipos de scripts en documentos web.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los requerimientos necesarios para instalar gestores de contenidos.",
        "Se han instalado diferentes tipos de gestores de contenidos.",
        "Se han gestionado usuarios con roles diferentes.",
        "Se ha personalizado la interfaz del gestor de contenidos.",
        "Se han creado contenidos.",
        "Se han publicado los contenidos.",
        "Se han realizado pruebas de funcionamiento.",
        "Se han realizado tareas de actualización del gestor de contenidos, especialmente las de seguridad.",
        "Se han instalado y configurado los módulos y menús necesarios.",
        "Se han gestionado plantillas.",
        "Se han activado y configurado los mecanismos de seguridad proporcionados por el propio gestor de contenidos.",
        "Se han habilitado foros y establecido reglas de acceso.",
        "Se han realizado pruebas de funcionamiento.",
        "Se han realizado copias de seguridad de los contenidos del gestor.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la estructura del sitio y la jerarquía de directorios generada.",
        "Se han realizado modificaciones en la estética o aspecto del sitio.",
        "Se han manipulado y generado perfiles personalizados.",
        "Se ha comprobado la funcionalidad de las comunicaciones mediante foros, consultas, entre otros.",
        "Se han importado y exportado contenidos en distintos formatos.",
        "Se han realizado copias de seguridad y restauraciones.",
        "Se han realizado informes de acceso y utilización del sitio.",
        "Se ha comprobado la seguridad del sitio.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la utilidad de un servicio de gestión de archivos web.",
        "Se han descrito diferentes aplicaciones de gestión de archivos web.",
        "Se ha instalado y adaptado una herramienta de gestión de archivos web.",
        "Se han creado y clasificado cuentas de persona usuaria en función de sus permisos.",
        "Se han creado grupos de gestión de personas usuarias.",
        "Se han gestionado archivos y directorios.",
        "Se han utilizado archivos de información adicional.",
        "Se han aplicado criterios de indexación sobre los archivos y directorios.",
        "Se ha comprobado la seguridad del gestor de archivos.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la utilidad de las aplicaciones de ofimática web.",
        "Se han descrito diferentes aplicaciones de ofimática web (procesador de textos, hoja de cálculo, entre otras).",
        "Se han instalado aplicaciones de ofimática web.",
        "Se han gestionado las cuentas de usuario.",
        "Se han gestionado grupos de usuarios.",
        "Se han aplicado criterios de seguridad en el acceso de los usuarios y grupos.",
        "Se han reconocido las prestaciones específicas de cada una de las aplicaciones instaladas.",
        "Se han utilizado las aplicaciones de forma colaborativa.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito diferentes aplicaciones web de escritorio.",
        "Se han instalado aplicaciones para proveer de acceso web al servicio de correo electrónico.",
        "Se han configurado las aplicaciones para integrarlas con un servidor de correo.",
        "Se han gestionado las cuentas de usuario.",
        "Se ha verificado el acceso al correo electrónico.",
        "Se han instalado aplicaciones de calendario web.",
        "Se han reconocido las prestaciones específicas de las aplicaciones instaladas (citas, tareas, entre otras).",
    ], start=1)],
}

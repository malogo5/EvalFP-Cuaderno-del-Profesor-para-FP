"""EvalFP — Aplicaciones Ofimáticas · 0223 · 1º SMR
RD 1691/2007, de 14 de diciembre (BOE) · Decreto CLM 107/2009, de 4 de agosto (DOCM)
"""
MODULO = {
    "nombre":"Aplicaciones Ofimáticas","codigo":"0223","abrev":"OFIM",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":6,"total_horas":192,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Sistema operativo: interfaz gráfica y gestión de archivos","horas":28,"eval":1,"tags":"Windows · Linux · Explorador · Archivos · Personalización · Accesorios"},
    {"id":"UT2","nombre":"Procesador de textos","horas":40,"eval":1,"tags":"Word · Formato · Estilos · Tablas · Imágenes · Plantillas · Combinación de correspondencia"},
    {"id":"UT3","nombre":"Hoja de cálculo","horas":40,"eval":2,"tags":"Excel · Fórmulas · Funciones · Gráficos · Tablas dinámicas · Macros básicas"},
    {"id":"UT4","nombre":"Presentaciones multimedia","horas":28,"eval":2,"tags":"PowerPoint · Diseño · Animaciones · Multimedia · Exportar"},
    {"id":"UT5","nombre":"Base de datos ofimática","horas":28,"eval":3,"tags":"Access · Tablas · Consultas · Formularios · Informes · Relaciones"},
    {"id":"UT6","nombre":"Integración de aplicaciones ofimáticas","horas":28,"eval":3,"tags":"OLE · Incrustación · Vinculación · PDF · Exportar/Importar"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Utiliza las funciones básicas del sistema operativo, describiendo sus características y ajustando su configuración."},
    {"id":"RA2","pond":25,"nombre":"Escribe textos con un procesador de textos aplicando las posibilidades de edición y formato del documento."},
    {"id":"RA3","pond":20,"nombre":"Elabora hojas de cálculo con datos y fórmulas, utilizando las funciones básicas de la aplicación."},
    {"id":"RA4","pond":15,"nombre":"Crea presentaciones con aplicaciones informáticas, relacionando los elementos de diseño con las posibilidades del software."},
    {"id":"RA5","pond":15,"nombre":"Utiliza bases de datos ofimáticas, describiendo su funcionamiento e identificando sus elementos."},
    {"id":"RA6","pond":10,"nombre":"Integra datos en documentos de distintas aplicaciones ofimáticas, relacionando las utilidades de cada aplicación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las funciones básicas del sistema operativo.",
        "Se ha gestionado el sistema de archivos desde la interfaz gráfica y desde la línea de comandos.",
        "Se han personalizado los entornos de escritorio del sistema operativo.",
        "Se han utilizado aplicaciones de gestión del sistema operativo.",
        "Se han aplicado medidas de seguridad básicas: usuarios, contraseñas y permisos.",
        "Se han utilizado los periféricos del sistema (impresoras, escáneres, etc.).",
        "Se ha comprobado el correcto funcionamiento del sistema tras las modificaciones realizadas.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las funciones y posibilidades del procesador de textos.",
        "Se ha configurado la página: márgenes, orientación, tamaño y encabezados y pies.",
        "Se han aplicado formatos de carácter, párrafo y página.",
        "Se han utilizado estilos y plantillas para dar formato al documento.",
        "Se han insertado imágenes, tablas, gráficos y otros objetos.",
        "Se ha utilizado el corrector ortográfico y gramatical.",
        "Se han combinado documentos para generar correspondencia en serie.",
        "Se han generado documentos en distintos formatos, incluido PDF.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las funciones y posibilidades de la hoja de cálculo.",
        "Se ha introducido y editado información en celdas: textos, números y fechas.",
        "Se han utilizado los distintos tipos de referencias a celdas y rangos.",
        "Se han aplicado fórmulas y funciones básicas: matemáticas, estadísticas, de texto y de fecha.",
        "Se han creado y modificado gráficos de distintos tipos.",
        "Se han utilizado listas y tablas de datos: filtros, ordenación y subtotales.",
        "Se ha protegido el libro y las hojas con contraseñas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las funciones y posibilidades de la aplicación de presentaciones.",
        "Se han creado presentaciones con distintos diseños y plantillas.",
        "Se han insertado y editado texto, imágenes, formas y elementos multimedia.",
        "Se han aplicado animaciones a los objetos y transiciones entre diapositivas.",
        "Se ha configurado la presentación para su proyección.",
        "Se han exportado las presentaciones en distintos formatos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos de una base de datos: tablas, consultas, formularios e informes.",
        "Se han creado tablas definiendo los campos y estableciendo la clave principal.",
        "Se han establecido relaciones entre tablas.",
        "Se han creado consultas de selección para filtrar y ordenar información.",
        "Se han creado formularios para introducir y visualizar datos.",
        "Se han generado informes para presentar los datos de forma estructurada.",
        "Se han importado y exportado datos entre la base de datos y otras aplicaciones.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las posibilidades de integración entre aplicaciones ofimáticas.",
        "Se han insertado objetos vinculados e incrustados entre aplicaciones.",
        "Se han importado y exportado datos entre las distintas aplicaciones ofimáticas.",
        "Se han combinado datos de hojas de cálculo con documentos de texto.",
        "Se han creado documentos compuestos que integran elementos de varias aplicaciones.",
        "Se han generado documentos en formato PDF desde distintas aplicaciones ofimáticas.",
    ], start=1)],
}

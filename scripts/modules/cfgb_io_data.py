"""EvalFP — Ofimática y Archivo de Documentos · 3031 · FPB Informática de Oficina
RD 356/2014, de 16 de mayo (BOE) · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])
"""
MODULO = {
    "nombre":"Ofimática y Archivo de Documentos","codigo":"3031","abrev":"OFIM",
    "ciclo":"","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"","horas_sem":7,"total_horas":208,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 356/2014, de 16 de mayo · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])",
}
UTS = [
    {"id":"UT1","nombre":"Tramitación de información en línea","horas":30,"eval":1,"tags":"Internet · Intranet · Búsqueda · Nube · Páginas institucionales"},
    {"id":"UT2","nombre":"Comunicaciones por correo electrónico","horas":28,"eval":1,"tags":"Correo electrónico · Agenda · Seguridad · Listas de distribución"},
    {"id":"UT3","nombre":"Procesador de textos","horas":40,"eval":1,"tags":"Word · Formato · Tablas · Plantillas · Impresión · Objetos"},
    {"id":"UT4","nombre":"Hoja de cálculo","horas":35,"eval":2,"tags":"Excel · Fórmulas · Funciones · Gráficos · Bases de datos · Ergonomía"},
    {"id":"UT5","nombre":"Elaboración de presentaciones","horas":30,"eval":2,"tags":"PowerPoint · Diapositivas · Animaciones · Proyector · Diseño"},
    {"id":"UT6","nombre":"Equipos de reprografía y encuadernación","horas":45,"eval":3,"tags":"Fotocopiadoras · Impresoras · Escáneres · Encuadernadoras · Guillotina · Reciclaje"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Tramita información en línea aplicando herramientas de Internet, intranet y otras redes."},
    {"id":"RA2","pond":15,"nombre":"Realiza comunicaciones internas y externas mediante las utilidades de correo electrónico siguiendo las pautas marcadas."},
    {"id":"RA3","pond":20,"nombre":"Elabora documentos utilizando las funciones básicas del procesador de texto."},
    {"id":"RA4","pond":20,"nombre":"Elabora documentos utilizando las aplicaciones básicas de hojas de cálculo."},
    {"id":"RA5","pond":15,"nombre":"Elabora presentaciones gráficas utilizando aplicaciones informáticas."},
    {"id":"RA6","pond":10,"nombre":"Utiliza los equipos de reproducción, informáticos y de encuadernación funcional en función del trabajo a realizar."},
    {"id":"RA7","pond":5,"nombre":"Obtiene encuadernaciones funcionales utilizando los útiles y medios apropiados en función de las características de los documentos tipo."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6","RA7"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las distintas redes informáticas a las que podemos acceder.",
        "Se han diferenciado distintos métodos de búsqueda de información en redes informáticas.",
        "Se ha accedido a información a través de Internet, intranet y otras redes de área local.",
        "Se han localizado documentos utilizando herramientas de Internet.",
        "Se han situado y recuperado archivos almacenados en servicios de alojamiento compartidos (la nube).",
        "Se ha comprobado la veracidad de la información localizada.",
        "Se ha valorado la utilidad de páginas institucionales y de Internet para la realización de trámites administrativos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los diferentes procedimientos de transmisión y recepción de mensajes internos y externos.",
        "Se ha utilizado el correo electrónico para enviar y recibir mensajes, tanto internos como externos.",
        "Se han anexado documentos, vínculos, entre otros en mensajes de correo electrónico.",
        "Se han empleado las utilidades del correo electrónico para clasificar contactos y listas de distribución.",
        "Se han aplicado criterios de prioridad, importancia y seguimiento en el envío de mensajes.",
        "Se han comprobado las medidas de seguridad y confidencialidad en la custodia o envío de información.",
        "Se ha organizado la agenda incluyendo tareas, avisos y otras herramientas de planificación del trabajo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las funciones básicas, prestaciones y procedimientos simples de los procesadores de textos y autoedición.",
        "Se han identificado las funciones y utilidades que garanticen las normas de seguridad, integridad y confidencialidad de la información.",
        "Se ha localizado, abierto y guardado el documento en el formato y dirección facilitados, nombrándolos significativamente.",
        "Se han configurado las distintas páginas del documento: márgenes, dimensiones y orientación, tablas, encabezados y pies de página, encolumnados, bordes y sombreados.",
        "Se ha trabajado con la opción de tablas y se han elaborado documentos con exactitud, aplicando los formatos y estilos indicados.",
        "Se han corregido los posibles errores cometidos al reutilizar o introducir la información.",
        "Se han integrado objetos simples en el texto, en el lugar y forma adecuados.",
        "Se han configurado las diferentes opciones de impresión en función de la información facilitada.",
        "Se han utilizado las funciones y utilidades del procesador de textos que garanticen la seguridad, integridad y confidencialidad de la información.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han utilizado los diversos tipos de datos y referencia para celdas, rangos, hojas y libros.",
        "Se han aplicado fórmulas y funciones básicas.",
        "Se han generado y modificado gráficos de diferentes tipos.",
        "Se ha utilizado la hoja de cálculo como base de datos sencilla.",
        "Se ha utilizado aplicaciones y periféricos para introducir textos, números, códigos e imágenes.",
        "Se han aplicado las reglas de ergonomía y salud en el desarrollo de las actividades.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las opciones básicas de las aplicaciones de presentaciones.",
        "Se reconocen los distintos tipos de vista asociados a una presentación.",
        "Se han aplicado y reconocido las distintas tipografías y normas básicas de composición, diseño y utilización del color.",
        "Se han creado presentaciones sencillas incorporando texto, gráficos, objetos y archivos multimedia.",
        "Se han diseñado plantillas de presentaciones.",
        "Se han utilizado periféricos para ejecutar presentaciones asegurando el correcto funcionamiento.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los principales componentes y necesidades de mantenimiento de los equipos de reproducción, identificando las incidencias elementales.",
        "Se ha descrito el funcionamiento de las fotocopiadoras, impresoras, escáneres, reproductoras, perforadoras y encuadernadoras.",
        "Se han identificado las posibles incidencias básicas de equipos de reproducción e informáticos, describiendo posibles actuaciones.",
        "Se han realizado las tareas de limpieza y mantenimiento de útiles de encuadernación y los ajustes pertinentes.",
        "Se han identificado los distintos recursos consumibles —tintas, papel, cintas, cartuchos, tóner— relacionándolos con los equipos.",
        "Se ha manejado los equipos asumiendo el compromiso de mantenerlos y cuidarlos, evitando costes y desgastes innecesarios.",
        "Se han realizado las pruebas de funcionamiento básico de los equipos informáticos y de reproducción.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la documentación a encuadernar describiendo sus características y los criterios de ordenación más apropiados.",
        "Se han identificado los distintos útiles y herramientas empleados en las operaciones de encuadernación funcional —guillotina, perforadora, cizalla—.",
        "Se han identificado los distintos tipos de materiales —canutillos, grapas, espirales, anillas, cubiertas— utilizados en la encuadernación.",
        "Se han descrito los sistemas de reciclaje en función de la naturaleza de los residuos producidos.",
        "Se han identificado y descrito los riesgos profesionales derivados del uso de las máquinas y herramientas y sus equipos de protección.",
        "Se ha identificado y comprobado el estado de funcionamiento de las herramientas de encuadernación funcional.",
        "Se ha organizado la documentación a encuadernar, ordenándola de acuerdo con los criterios establecidos.",
        "Se ha utilizado la cizalla u otros útiles análogos realizando distintos cortes de papel con precisión, observando las medidas de seguridad.",
        "Se ha utilizado la máquina de perforar papel de forma correcta.",
        "Se han realizado encuadernaciones —encanutado, grapado, espiralado, anillado— asignando el tipo de cubiertas en función del documento.",
        "Se han desechado los residuos en distintos envases de reciclado conforme a su naturaleza.",
        "Se han aplicado las precauciones y equipos de protección necesarios para realizar con seguridad la encuadernación funcional.",
        "Se ha comprobado que la encuadernación funcional realizada cumple con los criterios de calidad facilitados.",
    ], start=1)],
}

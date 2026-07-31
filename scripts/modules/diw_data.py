"""EvalFP — Diseño de Interfaces Web · 0615 · Desarrollo de Aplicaciones Web (DAW)
Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 186 h · 5 h/semana · 2º DAW.
"""
MODULO = {
    "nombre":"Diseño de Interfaces Web","codigo":"0615","abrev":"DIW",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":5,"total_horas":186,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Planificación de interfaces gráficas","horas":30,"eval":1,"tags":"UX · Arquitectura de información · Personas · User Journey"},
    {"id":"UT2","nombre":"Uso de estilos CSS avanzados","horas":38,"eval":1,"tags":"Flexbox · Grid · Variables CSS · Animaciones · Media Queries"},
    {"id":"UT3","nombre":"Prepara archivos multimedia para la Web","horas":34,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Integra contenido multimedia en documentos Web","horas":30,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Accesibilidad y usabilidad web","horas":29,"eval":3,"tags":"WCAG 2.1 · WAI-ARIA · Contraste · Teclado · Screen readers"},
    {"id":"UT6","nombre":"Desarrolla interfaces Web amigables","horas":25,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Planifica la creación de una interfaz web valorando y aplicando especificaciones de diseño."},
    {"id":"RA2","pond":20,"nombre":"Crea interfaces Web homogéneos definiendo y aplicando estilos."},
    {"id":"RA3","pond":18,"nombre":"Prepara archivos multimedia para la Web, analizando sus características y manejando herramientas especificas."},
    {"id":"RA4","pond":16,"nombre":"Integra contenido multimedia en documentos Web valorando su aportación y seleccionando adecuadamente los elementos interactivos."},
    {"id":"RA5","pond":16,"nombre":"Desarrolla interfaces Web accesibles, analizando las pautas establecidas y aplicando técnicas de verificación."},
    {"id":"RA6","pond":14,"nombre":"Desarrolla interfaces Web amigables analizando y aplicando las pautas de usabilidad establecidas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la importancia de la comunicación visual y sus principios básicos.",
        "Se han analizado y seleccionado los colores y tipografías adecuados para su visualización en pantalla.",
        "Se han analizado alternativas para la presentación de la información en documentos Web.",
        "Se ha valorado la importancia de definir y aplicar la guía de estilo en el desarrollo de una aplicación Web.",
        "Se han utilizado y valorado distintas aplicaciones para el diseño de documentos Web.",
        "Se han utilizado marcos, tablas y capas para presentar la información de manera ordenada.",
        "Se han creado y utilizado plantillas de diseño.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las posibilidades de modificar las etiquetas HTML.",
        "Se han definido estilos de forma directa.",
        "Se han definido y asociado estilos globales en hojas externas.",
        "Se han definido hojas de estilos alternativas.",
        "Se han redefinido estilos.",
        "Se han identificado las distintas propiedades de cada elemento.",
        "Se han creado clases de estilos.",
        "Se han utilizado herramientas de validación de hojas de estilos.",
        "Se ha utilizado y actualizado la guía de estilo.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las implicaciones de las licencias y los derechos de autor en el uso de material multimedia.",
        "Se han identificado los formatos de imagen, audio y vídeo a utilizar.",
        "Se han analizado las herramientas disponibles para generar contenido multimedia.",
        "Se han empleado herramientas para el tratamiento digital de la imagen.",
        "Se han utilizado herramientas para manipular audio y vídeo.",
        "Se han realizado animaciones a partir de imágenes fijas.",
        "Se han importado y exportado imágenes, audio y vídeo en diversos formatos según su finalidad.",
        "Se ha aplicado la guía de estilo.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido y analizado las tecnologías relacionadas con la inclusión de contenido multimedia e interactivo.",
        "Se han identificado las necesidades específicas de configuración de los navegadores Web para soportar contenido multimedia e interactivo.",
        "Se han utilizado herramientas gráficas para el desarrollo de contenido multimedia interactivo.",
        "Se ha analizado el código generado por las herramientas de desarrollo de contenido interactivo.",
        "Se han agregado elementos multimedia a documentos Web.",
        "Se ha añadido interactividad a elementos de un documento Web.",
        "Se ha verificado el funcionamiento de los elementos multimedia e interactivos en distintos navegadores.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la necesidad de diseñar webs accesibles.",
        "Se ha analizado la accesibilidad de diferentes documentos Web.",
        "Se han identificado las principales pautas de accesibilidad al contenido.",
        "Se han analizado los posibles errores según los puntos de verificación de prioridad.",
        "Se ha alcanzado el nivel de conformidad deseado.",
        "Se han verificado los niveles alcanzados mediante el uso de test externos.",
        "Se ha verificado la visualización del interfaz con diferentes navegadores y tecnologías.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha analizado la usabilidad de diferentes documentos Web.",
        "Se ha valorado la importancia del uso de estándares en la creación de documentos Web.",
        "Se ha modificado el interfaz Web para adecuarlo al objetivo que persigue y a los usuarios a los que va dirigido.",
        "Se ha verificado la facilidad de navegación de un documento Web mediante distintos periféricos.",
        "Se han analizado diferentes técnicas para verificar la usabilidad de un documento Web.",
        "Se ha verificado la usabilidad del interfaz Web creado en diferentes navegadores y tecnologías.",
    ], start=1)],
}

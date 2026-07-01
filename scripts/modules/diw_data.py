"""EvalFP — Diseño de Interfaces Web (DIW) · 0615 · 2º DAW · RD 686/2010 (actualizado RD 405/2023)"""
MODULO = {
    "nombre":"Diseño de Interfaces Web","codigo":"0615","abrev":"DIW",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 686/2010, de 20 de mayo · Decreto CLM 230/2011, de 28 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Planificación de interfaces gráficas","horas":20,"eval":1,"tags":"UX · Arquitectura de información · Personas · User Journey"},
    {"id":"UT2","nombre":"Uso de estilos CSS avanzados","horas":30,"eval":1,"tags":"Flexbox · Grid · Variables CSS · Animaciones · Media Queries"},
    {"id":"UT3","nombre":"Implantación de contenido multimedia","horas":18,"eval":2,"tags":"SVG · Canvas · WebP · Vídeo HTML5 · Lazy loading"},
    {"id":"UT4","nombre":"Diseño de webs adaptables (Responsive)","horas":22,"eval":2,"tags":"Responsive · Mobile first · Bootstrap · Tailwind · Frameworks CSS"},
    {"id":"UT5","nombre":"Accesibilidad y usabilidad web","horas":18,"eval":3,"tags":"WCAG 2.1 · WAI-ARIA · Contraste · Teclado · Screen readers"},
    {"id":"UT6","nombre":"Herramientas y metodologías de diseño","horas":20,"eval":3,"tags":"Figma · Adobe XD · Design Systems · Atomic Design · Storybook"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Planifica la creación de una interfaz web valorando y aplicando especificaciones de diseño."},
    {"id":"RA2","pond":25,"nombre":"Crea interfaces web homogéneas definiendo y aplicando estilos."},
    {"id":"RA3","pond":15,"nombre":"Prepara archivos multimedia para la web, analizando las posibilidades de los distintos formatos y su inclusión en páginas web."},
    {"id":"RA4","pond":20,"nombre":"Integra contenido interactivo en la interfaz web valorando y aplicando las posibilidades que ofrecen los lenguajes de guiones del lado del cliente y el marcado."},
    {"id":"RA5","pond":20,"nombre":"Desarrolla interfaces web accesibles, analizando las pautas establecidas y aplicando técnicas de verificación."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA1",["CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y aplicado los fundamentos del diseño visual.",
        "Se han analizado y aplicado las guías de estilo de las interfaces gráficas.",
        "Se han utilizado colores, tipografías e iconografía de forma coherente.",
        "Se han creado wireframes y prototipos de interfaz de usuario.",
        "Se han valorado e incorporado los principios de diseño centrado en el usuario.",
        "Se han analizado y aplicado principios de diseño de experiencia de usuario (UX).",
        "Se han utilizado herramientas de diseño vectorial y prototipado.",
        "Se han creado sistemas de diseño reutilizables.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las posibilidades de las hojas de estilo para el diseño web.",
        "Se han creado hojas de estilo con selectores complejos.",
        "Se ha aplicado el modelo de cajas (box model) de CSS.",
        "Se han creado layouts con Flexbox y CSS Grid.",
        "Se han aplicado transiciones y animaciones CSS.",
        "Se han definido variables CSS y temas.",
        "Se han utilizado preprocesadores CSS (Sass, Less).",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las implicaciones de los distintos formatos de imagen para la web.",
        "Se han optimizado imágenes para su visualización en web.",
        "Se han incluido elementos de vídeo y audio en páginas web.",
        "Se han utilizado formatos de imagen vectorial (SVG).",
        "Se han aplicado técnicas para mejorar el rendimiento en la carga de recursos multimedia.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido y aplicado técnicas de diseño responsive.",
        "Se ha aplicado la metodología mobile-first en el diseño.",
        "Se han utilizado frameworks CSS para el desarrollo responsive.",
        "Se han adaptado los contenidos multimedia a distintas resoluciones.",
        "Se han utilizado media queries para adaptar el diseño a distintos dispositivos.",
        "Se han validado los diseños en múltiples dispositivos y navegadores.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha reconocido la necesidad de diseñar webs accesibles.",
        "Se han analizado los niveles de accesibilidad WCAG y su aplicación.",
        "Se han aplicado atributos WAI-ARIA en componentes de interfaz.",
        "Se han verificado los niveles de accesibilidad de las páginas usando herramientas.",
        "Se ha comprobado la navegabilidad mediante teclado y lectores de pantalla.",
        "Se ha analizado la normativa legal sobre accesibilidad web.",
    ], start=1)],
}

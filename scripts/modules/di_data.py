"""EvalFP — Desarrollo de Interfaces (DI) · 0492 · 2º DAM · RD 450/2010"""
MODULO = {
    "nombre":"Desarrollo de Interfaces","codigo":"0490","abrev":"DI",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":6,"total_horas":192,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Diseño de la interfaz gráfica de usuario","horas":30,"eval":1,"tags":"Principios UX/UI · Usabilidad · Accesibilidad · Wireframes · Figma"},
    {"id":"UT2","nombre":"Creación de interfaces con componentes gráficos","horas":40,"eval":1,"tags":"JavaFX · FXML · SceneBuilder · Swing · CSS"},
    {"id":"UT3","nombre":"Creación de informes y documentos","horas":30,"eval":2,"tags":"JasperReports · iReport · PDF · Excel · Crystal Reports"},
    {"id":"UT4","nombre":"Internacionalización y accesibilidad","horas":24,"eval":2,"tags":"i18n · L10n · WCAG · ResourceBundle · Locale"},
    {"id":"UT5","nombre":"Preparación y distribución de aplicaciones","horas":36,"eval":3,"tags":"Maven · Gradle · JAR · Instaladores · CI/CD · App stores"},
    {"id":"UT6","nombre":"Desarrollo de interfaces web con tecnologías actuales","horas":32,"eval":3,"tags":"React · Vue.js · Electron · Tailwind · Componentes"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Genera interfaces gráficas de usuario mediante el uso de herramientas visuales, reconociendo los criterios de diseño."},
    {"id":"RA2","pond":25,"nombre":"Crea componentes visuales valorando y aplicando las características del lenguaje de programación."},
    {"id":"RA3","pond":20,"nombre":"Diseña y crea informes valorando y empleando las herramientas gráficas."},
    {"id":"RA4","pond":15,"nombre":"Prepara aplicaciones para su distribución valorando los requerimientos de instalación."},
    {"id":"RA5","pond":20,"nombre":"Elabora ayudas generales y contextuales para aplicaciones reconociendo la utilidad de los sistemas de ayuda."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA5",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA2",["CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA5"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[
        {"id":"CR1","texto":"Se han analizado y aplicado las guías de estilo de las interfaces gráficas."},
        {"id":"CR2","texto":"Se han generado interfaces gráficas de usuario mediante herramientas visuales."},
        {"id":"CR3","texto":"Se han creado controles y componentes visuales."},
        {"id":"CR4","texto":"Se han manejado eventos del ratón y del teclado."},
        {"id":"CR5","texto":"Se han aplicado los fundamentos del diseño centrado en el usuario."},
        {"id":"CR6","texto":"Se han diseñado prototipos de interfaces de usuario (wireframes y mockups)."},
    ],
    "RA2":[
        {"id":"CR1","texto":"Se han creado clases que heredan de clases de la librería gráfica."},
        {"id":"CR2","texto":"Se han creado nuevos componentes visuales."},
        {"id":"CR3","texto":"Se ha modificado el comportamiento de los componentes."},
        {"id":"CR4","texto":"Se han programado componentes de tablas y listas."},
        {"id":"CR5","texto":"Se han aplicado estilos a los componentes."},
        {"id":"CR6","texto":"Se han programado menús y barras de herramientas."},
        {"id":"CR7","texto":"Se han creado aplicaciones con interfaz gráfica usando JavaFX y FXML."},
        {"id":"CR8","texto":"Se han creado interfaces web con frameworks modernos (React/Vue)."},
        {"id":"CR9","texto":"Se han aplicado principios de diseño responsive."},
    ],
    "RA3":[
        {"id":"CR1","texto":"Se han descrito las características y tipos de informes."},
        {"id":"CR2","texto":"Se han creado informes mediante herramientas de generación de informes."},
        {"id":"CR3","texto":"Se han diseñado plantillas de informes."},
        {"id":"CR4","texto":"Se han integrado los informes en la aplicación."},
        {"id":"CR5","texto":"Se han exportado informes a distintos formatos."},
        {"id":"CR6","texto":"Se han parametrizado los informes."},
    ],
    "RA4":[
        {"id":"CR1","texto":"Se han identificado las fases del proceso de instalación de aplicaciones."},
        {"id":"CR2","texto":"Se han creado paquetes de instalación de aplicaciones."},
        {"id":"CR3","texto":"Se han instalado y desinstalado aplicaciones."},
        {"id":"CR4","texto":"Se han creado archivos ejecutables (JAR, EXE, DMG)."},
        {"id":"CR5","texto":"Se han utilizado gestores de dependencias y compilación (Maven, Gradle)."},
        {"id":"CR6","texto":"Se han configurado pipelines básicos de CI/CD."},
    ],
    "RA5":[
        {"id":"CR1","texto":"Se han identificado los sistemas de ayuda disponibles."},
        {"id":"CR2","texto":"Se han utilizado herramientas de creación de sistemas de ayuda."},
        {"id":"CR3","texto":"Se han creado sistemas de ayuda contextuales y generales."},
        {"id":"CR4","texto":"Se han integrado los sistemas de ayuda en las aplicaciones."},
        {"id":"CR5","texto":"Se han elaborado manuales de usuario de las aplicaciones."},
    ],
}

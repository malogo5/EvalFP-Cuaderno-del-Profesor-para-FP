"""EvalFP — Programación Multimedia y Dispositivos Móviles (PMDM) · 0493 · 2º DAM · RD 450/2010"""
MODULO = {
    "nombre":"Programación Multimedia y Dispositivos Móviles","codigo":"0493","abrev":"PMDM",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":5,"total_horas":160,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 450/2010, de 16 de abril · Decreto CLM 252/2011 (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Programación de contenidos multimedia","horas":30,"eval":1,"tags":"Imagen · Audio · Vídeo · Animaciones · JavaFX Media · HTML5 Media"},
    {"id":"UT2","nombre":"Desarrollo de aplicaciones para dispositivos móviles (Android)","horas":50,"eval":1,"tags":"Android Studio · Kotlin · Activities · Intents · Layouts · Jetpack"},
    {"id":"UT3","nombre":"Almacenamiento de información en dispositivos móviles","horas":30,"eval":2,"tags":"SQLite · Room · SharedPreferences · Firebase · ContentProviders"},
    {"id":"UT4","nombre":"Aplicaciones con acceso a servicios en la red","horas":30,"eval":2,"tags":"Retrofit · OkHttp · REST · JSON · Coroutines · Glide"},
    {"id":"UT5","nombre":"Publicación de aplicaciones móviles","horas":20,"eval":3,"tags":"Google Play · TestFlight · APK · Firma · Monetización · Analíticas"},
    {"id":"UT6","nombre":"Frameworks multiplataforma","horas":20,"eval":3,"tags":"Flutter · React Native · Kotlin Multiplatform · Ionic"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Programa aplicaciones que integran contenido multimedia, reconociendo e integrando los diferentes tipos."},
    {"id":"RA2","pond":35,"nombre":"Desarrolla aplicaciones para dispositivos móviles, analizando y empleando las tecnologías específicas."},
    {"id":"RA3","pond":20,"nombre":"Desarrolla aplicaciones para dispositivos móviles que gestionan bases de datos, analizando y empleando las herramientas específicas."},
    {"id":"RA4","pond":20,"nombre":"Desarrolla aplicaciones para dispositivos móviles con acceso a servicios en la red, analizando y empleando las tecnologías específicas."},
    {"id":"RA5","pond":10,"nombre":"Publica aplicaciones desarrolladas para dispositivos móviles analizando y empleando las tecnologías específicas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT6","RA2",["CR8","CR9"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los formatos de imagen, audio y vídeo más utilizados.",
        "Se han creado y manipulado imágenes mediante librerías especializadas.",
        "Se ha implementado la reproducción de audio y vídeo en aplicaciones.",
        "Se han creado animaciones y transiciones de interfaz.",
        "Se han optimizado los recursos multimedia para su uso en dispositivos móviles.",
        "Se han integrado elementos multimedia en una aplicación de escritorio y web.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las arquitecturas de los sistemas operativos móviles más utilizados.",
        "Se ha instalado y configurado el entorno de desarrollo para aplicaciones móviles.",
        "Se han creado y ejecutado proyectos de desarrollo de aplicaciones móviles.",
        "Se han programado interfaces de usuario adaptadas a la resolución del dispositivo.",
        "Se han utilizado los sensores y hardware del dispositivo.",
        "Se ha implementado la navegación entre pantallas (Activities y Fragments).",
        "Se han utilizado los ciclos de vida de los componentes de la aplicación.",
        "Se han desarrollado aplicaciones con arquitectura MVVM.",
        "Se han utilizado frameworks multiplataforma para el desarrollo móvil.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las posibilidades de almacenamiento en los dispositivos móviles.",
        "Se han utilizado ficheros para el almacenamiento y recuperación de información.",
        "Se han creado y utilizado bases de datos en aplicaciones móviles (SQLite/Room).",
        "Se han utilizado proveedores de contenidos para compartir información entre aplicaciones.",
        "Se han utilizado servicios de almacenamiento en la nube (Firebase Firestore).",
        "Se han implementado sincronización de datos online/offline.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han valorado las ventajas e inconvenientes de las distintas tecnologías de acceso a servicios en la red.",
        "Se han programado clientes de servicios en la red.",
        "Se han utilizado librerías específicas para el acceso a servicios HTTP (Retrofit, OkHttp).",
        "Se han desarrollado aplicaciones que consumen APIs REST.",
        "Se han procesado respuestas en formato JSON.",
        "Se han gestionado tareas asíncronas con Coroutines.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado las condiciones y requisitos de publicación en tiendas de aplicaciones.",
        "Se han creado certificados digitales y se han firmado las aplicaciones.",
        "Se han publicado aplicaciones en Google Play Store.",
        "Se han analizado las técnicas de monetización y analítica de aplicaciones.",
        "Se han actualizado aplicaciones publicadas y gestionado las versiones.",
    ], start=1)],
}

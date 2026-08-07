"""EvalFP — Programación Multimedia y Dispositivos Móviles · 0489 · Desarrollo de Aplicaciones Multiplataforma (DAM)
Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 158 h · 4 h/semana · 2º DAM.
"""
MODULO = {
    "nombre":"Programación Multimedia y Dispositivos Móviles","codigo":"0489","abrev":"PMDM",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":4,"total_horas":158,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Aplica tecnologías de desarrollo para dispositivos móviles","horas":29,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Desarrollo de aplicaciones para dispositivos móviles (Android)","horas":44,"eval":1,"tags":"Android Studio · Kotlin · Activities · Intents · Layouts · Jetpack"},
    {"id":"UT3","nombre":"Desarrolla programas que integran contenidos multimedia","horas":25,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Selecciona y prueba motores de juegos","horas":22,"eval":3,"tags":""},
    {"id":"UT5","nombre":"Desarrolla juegos 2D y 3D sencillos","horas":25,"eval":3,"tags":""},
    {"id":"UT6","nombre":"Desarrolla aplicaciones basadas en la localización","horas":13,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":18,"nombre":"Aplica tecnologías de desarrollo para dispositivos móviles evaluando sus características y capacidades."},
    {"id":"RA2","pond":28,"nombre":"Desarrolla aplicaciones para dispositivos móviles analizando y empleando las tecnologías y librerías específicas."},
    {"id":"RA3","pond":16,"nombre":"Desarrolla programas que integran contenidos multimedia analizando y empleando las tecnologías y librerías específicas."},
    {"id":"RA4","pond":14,"nombre":"Selecciona y prueba motores de juegos analizando la arquitectura de juegos 2D y 3D."},
    {"id":"RA5","pond":16,"nombre":"Desarrolla juegos 2D y 3D sencillos utilizando motores de juegos."},
    {"id":"RA6","pond":8,"nombre":"Desarrolla aplicaciones basadas en la localización."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12","CR13","CR14"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4","RA5","RA6"]}
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
        "Se han analizado las limitaciones que plantea la ejecución de aplicaciones en los dispositivos móviles.",
        "Se han identificado los distintos sistemas operativos existentes para dispositivos móviles y sus características principales.",
        "Se han identificado las tecnologías de desarrollo de aplicaciones para dispositivos móviles.",
        "Se han instalado, configurado y utilizado entornos de trabajo para el desarrollo de aplicaciones para dispositivos móviles.",
        "Se han identificado configuraciones que clasifican los dispositivos móviles en base a sus características.",
        "Se han descrito perfiles que establecen la relación entre el dispositivo y la aplicación.",
        "Se ha analizado la estructura de aplicaciones existentes para dispositivos móviles identificando las clases utilizadas.",
        "Se han realizado modificaciones sobre aplicaciones existentes.",
        "Se han utilizado emuladores para comprobar el funcionamiento de las aplicaciones.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha generado la estructura de clases necesaria para la aplicación.",
        "Se han analizado y utilizado las clases que modelan ventanas, menús, alertas y controles para el desarrollo de aplicaciones gráficas sencillas.",
        "Se han analizado cómo funcionan los servicios disponibles en los dispositivos móviles y su utilidad en el desarrollo de las aplicaciones.",
        "Se han identificado los proveedores de contenido.",
        "Se han utilizado las clases necesarias para la conexión y comunicación con dispositivos inalámbricos.",
        "Se han utilizado las clases necesarias para el intercambio de mensajes de texto y multimedia.",
        "Se han utilizado las clases necesarias para establecer conexiones y comunicaciones HTTP y HTTPS.",
        "Se han utilizado las clases necesarias para establecer conexiones con almacenes de datos garantizando la persistencia.",
        "Se ha recuperado y utilizado la información proporcionada por la red.",
        "Se han definido distintos requerimientos de seguridad en las aplicaciones.",
        "Se han realizado pruebas de interacción usuario-aplicación para optimizar las aplicaciones desarrolladas a partir de emuladores.",
        "Se han empaquetado y desplegado las aplicaciones desarrolladas en dispositivos móviles reales.",
        "Se han registrado las aplicaciones en centros de distribución autorizados.",
        "Se han documentado los procesos necesarios para el desarrollo de las aplicaciones.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado entornos de desarrollo multimedia.",
        "Se han reconocido las clases que permiten la captura, procesamiento y almacenamiento de datos multimedia.",
        "Se han utilizado clases para la conversión de datos multimedia de un formato a otro.",
        "Se han utilizado clases para construir procesadores para la transformación de las fuentes de datos multimedia.",
        "Se han utilizado clases para el control de eventos, tipos de media y excepciones, entre otros.",
        "Se han utilizado clases para la creación y control de animaciones.",
        "Se han utilizado clases para construir reproductores de contenidos multimedia.",
        "Se han depurado y documentado los programas desarrollados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos que componen la arquitectura de un juego 2D y 3D.",
        "Se han analizado los componentes de un motor de juegos.",
        "Se han analizado entornos de desarrollo de juegos.",
        "Se han analizado diferentes motores de juegos, sus características y funcionalidades.",
        "Se han identificado los bloques funcionales de un juego existente.",
        "Se han definido y ejecutado procesos de render.",
        "Se ha reconocido la representación lógica y espacial de una escena gráfica sobre un juego existente.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la lógica de un nuevo juego.",
        "Se han creado objetos y definido los fondos.",
        "Se han instalado y utilizado extensiones para el manejo de escenas.",
        "Se han utilizado instrucciones gráficas para determinar las propiedades finales de la superficie de un objeto o imagen.",
        "Se ha incorporado sonido a los diferentes eventos del juego.",
        "Se han desarrollado e implantado juegos para dispositivos móviles.",
        "Se han realizado pruebas de funcionamiento y optimización de los juegos desarrollados.",
        "Se han documentado las fases de diseño y desarrollo de los juegos creados.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado las distintas tecnologías de localización (GPS, A-GPS,...).",
        "Se han utilizado mapas para localizar una serie de ubicaciones concretas.",
        "Se han utilizado datos de localización en distintas aplicaciones móviles.",
        "Se han documentado los procesos necesarios para el desarrollo de las aplicaciones de localización.",
    ], start=1)],
}

"""EvalFP — Hacking Ético · 5025 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 120 h · 4 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Hacking Ético","codigo":"5025","abrev":"HE",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Determina herramientas de monitorización para detectar vulnerabilidades","horas":35,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Ataca y defiende en entornos de prueba","horas":27,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Ataca y defiende en entornos de prueba","horas":19,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Análisis forense digital","horas":16,"eval":2,"tags":"Adquisición de evidencias · Volatility · Autopsy · Cadena de custodia"},
    {"id":"UT5","nombre":"Ataca y defiende en entornos de prueba","horas":23,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":29,"nombre":"Determina herramientas de monitorización para detectar vulnerabilidades aplicando técnicas de hacking ético."},
    {"id":"RA2","pond":23,"nombre":"Ataca y defiende en entornos de prueba, comunicaciones inalámbricas consiguiendo acceso a redes para demostrar sus vulnerabilidades."},
    {"id":"RA3","pond":16,"nombre":"Ataca y defiende en entornos de prueba, redes y sistemas consiguiendo acceso a información y sistemas de terceros."},
    {"id":"RA4","pond":13,"nombre":"Consolida y utiliza sistemas comprometidos garantizando accesos futuros."},
    {"id":"RA5","pond":19,"nombre":"Ataca y defiende en entornos de prueba, aplicaciones web consiguiendo acceso a datos o funcionalidades no autorizadas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica","informe"],
    "RA2":["practica","informe"],
    "RA3":["practica","informe"],
    "RA4":["practica","informe"],
    "RA5":["practica","informe"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido la terminología esencial del hacking ético.",
        "Se han identificado los conceptos éticos y legales frente al ciberdelito.",
        "Se ha definido el alcance y condiciones de un test de intrusión.",
        "Se han identificado los elementos esenciales de seguridad: confidencialidad, autenticidad, integridad y disponibilidad.",
        "Se han identificado las fases de un ataque seguidas por un atacante.",
        "Se han analizado y definido los tipos vulnerabilidades.",
        "Se han analizado y definido los tipos de ataque.",
        "Se han determinado y caracterizado las diferentes vulnerabilidades existentes.",
        "Se han determinado las herramientas de monitorización disponibles en el mercado adecuadas en función del tipo de organización.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado los distintos modos de funcionamiento de las tarjetas de red inalámbricas.",
        "Se han descrito las técnicas de encriptación de las redes inalámbricas y sus puntos vulnerables.",
        "Se han detectado redes inalámbricas y se ha capturado tráfico de red como paso previo a su ataque.",
        "Se ha accedido a redes inalámbricas vulnerables.",
        "Se han caracterizado otros sistemas de comunicación inalámbricos y sus vulnerabilidades.",
        "Se han utilizado técnicas de “Equipo Rojo y Azul”.",
        "Se han realizado informes sobre las vulnerabilidades detectadas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha recopilado información sobre la red y sistemas objetivo mediante técnicas pasivas.",
        "Se ha creado un inventario de equipos, cuentas de usuario y potenciales vulnerabilidades de la red y sistemas objetivo mediante técnicas activas.",
        "Se ha interceptado tráfico de red de terceros para buscar información sensible.",
        "Se ha realizado un ataque de intermediario, leyendo, insertando y modificando, a voluntad, el tráfico intercambiado por dos extremos remotos.",
        "Se han comprometido sistemas remotos explotando sus vulnerabilidades.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han administrado sistemas remotos a través de herramientas de línea de comandos.",
        "Se han comprometido contraseñas a través de ataques de diccionario, tablas rainbow y fuerza bruta contra sus versiones encriptadas.",
        "Se ha accedido a sistemas adicionales a través de sistemas comprometidos.",
        "Se han instalado puertas traseras para garantizar accesos futuros a los sistemas comprometidos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos sistemas de autenticación web, destacando sus debilidades y fortalezas.",
        "Se ha realizado un inventario de equipos, protocolos, servicios y sistemas operativos que proporcionan el servicio de una aplicación web.",
        "Se ha analizado el flujo de las interacciones realizadas entre el navegador y la aplicación web durante su uso normal.",
        "Se han examinado manualmente aplicaciones web en busca de las vulnerabilidades más habituales.",
        "Se han usado herramientas de búsquedas y explotación de vulnerabilidades web.",
        "Se ha realizado la búsqueda y explotación de vulnerabilidades web mediante herramientas software.",
    ], start=1)],
}

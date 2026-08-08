"""EvalFP — Bastionado de Redes y Sistemas · 5022 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 185 h · 6 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Bastionado de Redes y Sistemas","codigo":"5022","abrev":"BRS",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":6,"total_horas":185,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM núm. 136, de 18/07/2022) · Horas: Anexo I · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Diseño de planes de securización","horas":31,"eval":1,"tags":"CIS Controls · NIST · ISO 27001 · Plan director · Análisis de riesgos · MAGERIT"},
    {"id":"UT2","nombre":"Configura sistemas de control de acceso y autenticación de personas…","horas":26,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Administra credenciales de acceso a sistemas informáticos","horas":26,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Diseña redes de computadores contemplando los requisitos de seguridad","horas":26,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Configura dispositivos y sistemas informáticos cumpliendo los…","horas":26,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Configura dispositivos para la instalación de sistemas informáticos…","horas":25,"eval":2,"tags":""},
    {"id":"UT7","nombre":"Configura sistemas informáticos minimizando las probabilidades de…","horas":25,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Diseña planes de securización incorporando buenas prácticas para el bastionado de sistemas y redes."},
    {"id":"RA2","pond":14,"nombre":"Configura sistemas de control de acceso y autenticación de personas preservando la confidencialidad y privacidad de los datos."},
    {"id":"RA3","pond":14,"nombre":"Administra credenciales de acceso a sistemas informáticos aplicando los requisitos de funcionamiento y seguridad establecidos."},
    {"id":"RA4","pond":14,"nombre":"Diseña redes de computadores contemplando los requisitos de seguridad."},
    {"id":"RA5","pond":14,"nombre":"Configura dispositivos y sistemas informáticos cumpliendo los requisitos de seguridad."},
    {"id":"RA6","pond":14,"nombre":"Configura dispositivos para la instalación de sistemas informáticos minimizando las probabilidades de exposición a ataques."},
    {"id":"RA7","pond":14,"nombre":"Configura sistemas informáticos minimizando las probabilidades de exposición a ataques."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6","RA7"]}
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
        "Se han identificado los activos, las amenazas y vulnerabilidades de la organización.",
        "Se ha evaluado las medidas de seguridad actuales.",
        "Se ha elaborado un análisis de riesgo de la situación actual en ciberseguridad de la organización",
        "Se ha priorizado las medidas técnicas de seguridad a implantar en la organización teniendo también en cuenta los principios de la economía circular.",
        "Se ha diseñado y elaborado un plan de medidas técnicas de seguridad a implantar en la organización, apropiadas para garantizar un nivel de seguridad adecuado en función de los riesgos de la organización.",
        "Se han identificado las mejores prácticas en base a estándares, guías y políticas de securización adecuadas para el bastionado de los sistemas y redes de la organización.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los mecanismos de autenticación en base a distintos / múltiples factores (físicos, inherentes y basados en el conocimiento), existentes.",
        "Se han definido protocolos y políticas de autenticación basados en contraseñas y frases de paso, en base a las principales vulnerabilidades y tipos de ataques.",
        "Se han definido protocolos y políticas de autenticación basados en certificados digitales y tarjetas inteligentes, en base a las principales vulnerabilidades y tipos de ataques.",
        "Se han definido protocolos y políticas de autenticación basados en tokens, OTPs, etc., en base a las principales vulnerabilidades y tipos de ataques.",
        "Se han definido protocolos y políticas de autenticación basados en características biométricas, según las principales vulnerabilidades y tipos de ataques.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de credenciales más utilizados.",
        "Se han generado y utilizado diferentes certificados digitales como medio de acceso a un servidor remoto.",
        "Se ha comprobado la validez y la autenticidad de un certificado digital de un servicio web.",
        "Se han comparado certificados digitales válidos e inválidos por diferentes motivos.",
        "Se ha instalado y configurado un servidor seguro para la administración de credenciales (tipo RADIUS - Remote Access Dial In User Service).",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha incrementado el nivel de seguridad de una red local plana segmentándola físicamente y utilizando técnicas y dispositivos de enrutamiento.",
        "Se ha optimizado una red local plana utilizando técnicas de segmentación lógica (VLANs).",
        "Se ha adaptado un segmento de una red local ya operativa utilizando técnicas de subnetting para incrementar su segmentación respetando los direccionamientos existentes.",
        "Se han configurado las medidas de seguridad adecuadas en los dispositivos que dan acceso a una red inalámbrica (routers, puntos de acceso, etc.).",
        "Se ha establecido un túnel seguro de comunicaciones entre dos sedes geográficamente separadas.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado dispositivos de seguridad perimetral acorde a una serie de requisitos de seguridad.",
        "Se han detectado errores de configuración de dispositivos de red mediante el análisis de tráfico.",
        "Se han identificado comportamientos no deseados en una red a través del análisis de los registros (Logs), de un cortafuego.",
        "Se han implementado contramedidas frente a comportamientos no deseados en una red.",
        "Se han caracterizado, instalado y configurado diferentes herramientas de monitorización.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado la BIOS para incrementar la seguridad del dispositivo y su contenido minimizando las probabilidades de exposición a ataques.",
        "Se ha preparado un sistema informático para su primera instalación teniendo en cuenta las medidas de seguridad necesarias.",
        "Se ha configurado un sistema informático para que un actor malicioso no pueda alterar la secuencia de arranque con fines de acceso ilegítimo.",
        "Se ha instalado un sistema informático utilizando sus capacidades de cifrado del sistema de ficheros para evitar la extracción física de datos.",
        "Se ha particionado el sistema de ficheros del sistema informático para minimizar riesgos de seguridad.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han enumerado y eliminado los programas, servicios y protocolos innecesarios que hayan sido instalados por defecto en el sistema.",
        "Se han configurado las características propias del sistema informático para imposibilitar el acceso ilegítimo mediante técnicas de explotación de procesos.",
        "Se ha incrementado la seguridad del sistema de administración remoto SSH y otros.",
        "Se ha instalado y configurado un Sistema de detección de intrusos en un Host (HIDS) en el sistema informático.",
        "Se han instalado y configurado sistemas de copias de seguridad.",
    ], start=1)],
}

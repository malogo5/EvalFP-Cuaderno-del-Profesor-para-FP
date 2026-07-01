"""EvalFP — Análisis Forense Informático · 5024 · CE Ciberseguridad
RD 479/2020, de 7 de abril (BOE) · Decreto CLM 77/2022, de 12 de julio (DOCM)
"""
MODULO = {
    "nombre":"Análisis Forense Informático","codigo":"5024","abrev":"AFI",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 479/2020, de 7 de abril · Decreto CLM 77/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Aplicación de metodologías forenses","horas":25,"eval":1,"tags":"Cadena de custodia · RFC 3227 · Metodología · Fases · Perito · Informe pericial"},
    {"id":"UT2","nombre":"Análisis forense en sistemas operativos","horas":35,"eval":1,"tags":"Autopsy · Volatility · Registro Windows · Linux · Artefactos · Línea de tiempo"},
    {"id":"UT3","nombre":"Análisis forense en redes","horas":30,"eval":2,"tags":"Wireshark · NetworkMiner · PCAP · DNS · HTTP · Flujos de red"},
    {"id":"UT4","nombre":"Análisis forense en dispositivos móviles","horas":15,"eval":2,"tags":"Android · iOS · Cellebrite · Extracción · Apps · GPS · Borrado seguro"},
    {"id":"UT5","nombre":"Análisis forense en Cloud y entornos virtuales","horas":15,"eval":2,"tags":"AWS · Azure · Logs cloud · Contenedores · VMs · API logs"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Aplica metodologías de análisis forense adecuando los procedimientos a las características del incidente."},
    {"id":"RA2","pond":30,"nombre":"Realiza análisis forenses en sistemas operativos recopilando y analizando evidencias digitales."},
    {"id":"RA3","pond":25,"nombre":"Realiza análisis forenses en redes identificando y analizando evidencias en el tráfico de red."},
    {"id":"RA4","pond":15,"nombre":"Realiza análisis forenses en dispositivos móviles, obteniendo evidencias de manera forense."},
    {"id":"RA5","pond":10,"nombre":"Realiza análisis forenses en Cloud, identificando evidencias en entornos virtualizados y servicios en la nube."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de análisis forense y sus características.",
        "Se han descrito las fases del análisis forense: identificación, preservación, análisis y presentación.",
        "Se han aplicado los principios de la cadena de custodia en la gestión de evidencias.",
        "Se han identificado los requisitos legales del análisis forense en España.",
        "Se han documentado los procedimientos de recogida y preservación de evidencias.",
        "Se han elaborado informes periciales con los hallazgos del análisis.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han adquirido imágenes forenses de discos y memorias manteniendo la integridad mediante hash.",
        "Se han recuperado archivos borrados y datos de espacios no asignados.",
        "Se han analizado los artefactos del sistema de archivos y los metadatos.",
        "Se han examinado los registros del sistema operativo Windows (Registro, Event Logs, Prefetch).",
        "Se han analizado los artefactos de actividad del usuario (historial, accesos recientes, papelera).",
        "Se ha realizado análisis de memoria volátil para identificar procesos y conexiones activas.",
        "Se ha construido una línea de tiempo de la actividad del sistema.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han capturado y analizado trazas de tráfico de red.",
        "Se han identificado protocolos de red relevantes para la investigación.",
        "Se han reconstruido sesiones de comunicación a partir del tráfico capturado.",
        "Se han identificado exfiltraciones de datos en el tráfico de red.",
        "Se han analizado logs de dispositivos de red (firewalls, routers, proxies).",
        "Se han identificado indicadores de compromiso en el tráfico de red.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de extracción forense en dispositivos móviles.",
        "Se han adquirido datos de dispositivos Android e iOS mediante herramientas forenses.",
        "Se han analizado aplicaciones, mensajes, contactos y registros de llamadas.",
        "Se ha analizado la información de geolocalización almacenada en el dispositivo.",
        "Se han identificado artefactos de aplicaciones de mensajería instantánea.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de evidencias disponibles en entornos cloud.",
        "Se han obtenido y analizado los logs de servicios cloud (AWS CloudTrail, Azure Monitor).",
        "Se han analizado evidencias en entornos de contenedores y máquinas virtuales.",
        "Se han identificado las limitaciones legales y técnicas del análisis forense en la nube.",
        "Se ha documentado el proceso y los hallazgos del análisis forense en cloud.",
    ], start=1)],
}

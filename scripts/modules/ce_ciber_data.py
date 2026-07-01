"""EvalFP — Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información
Módulos: 0484+/CE · RD 479/2020, de 7 de abril
Módulo representativo: Hacking Ético (0487CE)
"""
MODULO = {
    "nombre":"Hacking Ético","codigo":"5025","abrev":"HE",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":6,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto": "RD 479/2020, de 7 de abril · Decreto CLM 77/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Determinación de las herramientas de hacking ético","horas":20,"eval":1,"tags":"Kali Linux · Metasploit · Nmap · Burp Suite · Recon"},
    {"id":"UT2","nombre":"Ataque a sistemas y redes","horas":25,"eval":1,"tags":"Explotación · Escalada de privilegios · Post-explotación · Pivoting"},
    {"id":"UT3","nombre":"Ataque a aplicaciones web","horas":25,"eval":1,"tags":"OWASP Top 10 · SQLi · XSS · CSRF · LFI/RFI"},
    {"id":"UT4","nombre":"Análisis forense digital","horas":25,"eval":2,"tags":"Adquisición de evidencias · Volatility · Autopsy · Cadena de custodia"},
    {"id":"UT5","nombre":"Elaboración de informes de auditoría","horas":25,"eval":2,"tags":"CVSS · CVE · Informe técnico · Informe ejecutivo · Remediación"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Determina las herramientas de hacking ético necesarias, analizando las características de cada tarea."},
    {"id":"RA2","pond":25,"nombre":"Ataca y defiende en entornos de laboratorio, analizando las vulnerabilidades de sistemas operativos y redes."},
    {"id":"RA3","pond":25,"nombre":"Ataca y defiende en entornos de laboratorio, analizando las vulnerabilidades de aplicaciones web."},
    {"id":"RA4","pond":15,"nombre":"Consolida y utiliza sistemas comprometidos, garantizando accesos futuros."},
    {"id":"RA5","pond":15,"nombre":"Ataca y defiende en entornos de laboratorio, analizando las vulnerabilidades de las comunicaciones inalámbricas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","informe"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las características de las principales herramientas de hacking ético.",
        "Se han instalado y configurado entornos de laboratorio de pruebas.",
        "Se han clasificado las herramientas según su función en el proceso de auditoría.",
        "Se han utilizado distribuciones especializadas en seguridad ofensiva.",
        "Se han descrito los marcos legales del hacking ético.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha realizado reconocimiento de sistemas objetivo (footprinting).",
        "Se han identificado puertos y servicios mediante escaneo.",
        "Se han detectado vulnerabilidades con herramientas automatizadas.",
        "Se han explotado vulnerabilidades en sistemas operativos.",
        "Se ha escalado privilegios en sistemas comprometidos.",
        "Se han documentado las vulnerabilidades encontradas y sus evidencias.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los vectores de ataque a aplicaciones web del OWASP Top 10.",
        "Se han realizado ataques de inyección SQL.",
        "Se han realizado ataques XSS y CSRF.",
        "Se han explotado vulnerabilidades en la gestión de sesiones.",
        "Se han utilizado proxies de intercepción para analizar peticiones.",
        "Se han documentado los hallazgos en aplicaciones web.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han establecido mecanismos de persistencia en sistemas comprometidos.",
        "Se han utilizado técnicas de pivoting para acceder a redes internas.",
        "Se han cubierto huellas de la intrusión.",
        "Se ha documentado la cadena de explotación completa.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han elaborado informes técnicos de las vulnerabilidades encontradas.",
        "Se han elaborado informes ejecutivos con el resumen de riesgos.",
        "Se han clasificado las vulnerabilidades mediante CVSS.",
        "Se han propuesto medidas de remediación para cada hallazgo.",
        "Se han presentado los resultados de la auditoría.",
    ], start=1)],
}

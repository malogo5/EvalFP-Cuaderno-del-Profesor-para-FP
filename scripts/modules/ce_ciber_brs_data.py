"""EvalFP — Bastionado de Redes y Sistemas · 5022 · CE Ciberseguridad
RD 479/2020, de 7 de abril (BOE) · Decreto CLM 77/2022, de 12 de julio (DOCM)
"""
MODULO = {
    "nombre":"Bastionado de Redes y Sistemas","codigo":"5022","abrev":"BRS",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":6,"total_horas":180,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 479/2020, de 7 de abril · Decreto CLM 77/2022, de 12 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Diseño de planes de securización","horas":35,"eval":1,"tags":"CIS Controls · NIST · ISO 27001 · Plan director · Análisis de riesgos · MAGERIT"},
    {"id":"UT2","nombre":"Configuración de sistemas operativos seguros","horas":40,"eval":1,"tags":"Hardening Windows · Linux · CIS Benchmarks · GPO · SELinux · AppArmor"},
    {"id":"UT3","nombre":"Bastionado de redes","horas":40,"eval":2,"tags":"Firewall · VLAN · VPN · DMZ · IDS/IPS · Zero Trust · Segmentación"},
    {"id":"UT4","nombre":"Bastionado de aplicaciones y servicios","horas":35,"eval":2,"tags":"Servidores web · BBDD · Docker · Kubernetes · WAF · API Security"},
    {"id":"UT5","nombre":"Monitorización y auditoría","horas":30,"eval":2,"tags":"SIEM · Wazuh · Nagios · Auditoría · Cumplimiento · Reporting"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Diseña planes de securización incorporando buenas prácticas para el bastionado de sistemas y redes."},
    {"id":"RA2","pond":25,"nombre":"Configura sistemas operativos eliminando configuraciones por defecto e implantando medidas de protección."},
    {"id":"RA3","pond":25,"nombre":"Configura redes seguras para el bastionado de sistemas, previniendo intrusiones y accesos no autorizados."},
    {"id":"RA4","pond":20,"nombre":"Configura aplicaciones y servicios con los criterios de seguridad adecuados eliminando vulnerabilidades."},
    {"id":"RA5","pond":10,"nombre":"Establece sistemas de monitorización y auditoría comprobando la implementación de las medidas de seguridad."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los activos, las amenazas y los riesgos de la organización.",
        "Se ha elaborado un análisis de riesgos de los sistemas y redes de la organización.",
        "Se han identificado los controles de seguridad aplicables según marcos de referencia (CIS, NIST, ISO 27001).",
        "Se ha elaborado un plan de securización con las medidas técnicas priorizadas.",
        "Se han definido procedimientos de bastionado para los distintos activos.",
        "Se ha documentado el plan de securización para su aprobación e implantación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han eliminado cuentas y servicios innecesarios del sistema operativo.",
        "Se han aplicado políticas de contraseñas y bloqueo de cuentas.",
        "Se ha configurado el control de acceso basado en el principio de mínimo privilegio.",
        "Se han aplicado actualizaciones y parches de seguridad del sistema operativo.",
        "Se ha configurado el firewall del sistema operativo con reglas restrictivas.",
        "Se han aplicado las guías de bastionado del CIS Benchmark para el sistema operativo.",
        "Se ha verificado el bastionado mediante herramientas de auditoría de configuración.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha segmentado la red utilizando VLANs y zonas de seguridad (DMZ, LAN, WAN).",
        "Se han configurado firewalls con políticas de denegación por defecto.",
        "Se ha implementado un sistema de detección y prevención de intrusiones (IDS/IPS).",
        "Se han configurado redes privadas virtuales (VPN) para el acceso remoto seguro.",
        "Se han aplicado filtros de contenido y proxies de seguridad.",
        "Se ha implementado el modelo Zero Trust en el acceso a los recursos de red.",
        "Se ha verificado la seguridad de la red mediante pruebas de penetración controladas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y eliminado los módulos y características innecesarias de las aplicaciones.",
        "Se han configurado los servidores web con cabeceras de seguridad y TLS.",
        "Se han aplicado medidas de seguridad en bases de datos: cifrado, control de acceso y auditoría.",
        "Se han bastionado los entornos de contenedores (Docker, Kubernetes).",
        "Se han configurado WAF para proteger las aplicaciones web de ataques.",
        "Se han aplicado medidas de seguridad en el ciclo de desarrollo (DevSecOps).",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado un sistema SIEM para la monitorización centralizada.",
        "Se han definido alertas y dashboards para la detección temprana de anomalías.",
        "Se han programado auditorías periódicas de la configuración de seguridad.",
        "Se ha verificado el cumplimiento de las medidas de bastionado implantadas.",
        "Se ha elaborado un informe de estado de seguridad con métricas e indicadores.",
    ], start=1)],
}

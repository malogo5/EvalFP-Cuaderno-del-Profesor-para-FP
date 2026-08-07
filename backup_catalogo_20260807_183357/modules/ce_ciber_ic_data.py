"""EvalFP — Incidentes de Ciberseguridad · 5021 · CE Ciberseguridad en Entornos de las TI
Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 120 h · 4 h/semana · CE Ciberseguridad.
"""
MODULO = {
    "nombre":"Incidentes de Ciberseguridad","codigo":"5021","abrev":"IC",
    "ciclo":"CE Ciberseguridad en Entornos de las TI","ciclo_clave":"CE_CIBER","ciclo_nivel":"CE",
    "curso":"CE Ciberseguridad","horas_sem":4,"total_horas":120,"anno":"2026-2027","eval_count":2,
    "decreto":"Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha (DOCM) · RA y CE literales del Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Desarrollo de planes de prevención y concienciación","horas":23,"eval":1,"tags":"Plan de seguridad · Políticas · Concienciación · Normativa · ISO 27001"},
    {"id":"UT2","nombre":"Auditoría de incidentes de ciberseguridad","horas":23,"eval":1,"tags":"SIEM · Logs · Correlación · Alertas · IDS/IPS · SOC"},
    {"id":"UT3","nombre":"Investigación de los incidentes de ciberseguridad","horas":23,"eval":1,"tags":"Análisis · Evidencias · Cadena de custodia · Herramientas forenses"},
    {"id":"UT4","nombre":"Implementación de medidas de ciberseguridad","horas":28,"eval":2,"tags":"Hardening · Parches · Firewall · WAF · Cifrado · Bastionado"},
    {"id":"UT5","nombre":"Documentación y notificación de incidentes","horas":23,"eval":2,"tags":"ENISA · INCIBE · CCN-CERT · Notificación RGPD · Informes"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Desarrolla planes de prevención y concienciación en ciberseguridad, estableciendo normas y medidas de protección."},
    {"id":"RA2","pond":19,"nombre":"Analiza incidentes de ciberseguridad utilizando herramientas, mecanismos de detección y alertas de seguridad."},
    {"id":"RA3","pond":19,"nombre":"Investiga incidentes de ciberseguridad analizando los riesgos implicados y definiendo las posibles medidas a adoptar."},
    {"id":"RA4","pond":23,"nombre":"Implementa medidas de ciberseguridad en redes y sistemas respondiendo a los incidentes detectados y aplicando las técnicas de protección adecuadas."},
    {"id":"RA5","pond":19,"nombre":"Detecta y documenta incidentes de ciberseguridad siguiendo procedimientos de actuación establecidos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han definido los principios generales de la organización en materia de ciberseguridad, que deben ser conocidos y apoyados por la dirección de la misma.",
        "Se ha establecido una normativa de protección del puesto de trabajo.",
        "Se ha definido un plan de concienciación de ciberseguridad dirigido a los empleados.",
        "Se ha desarrollado el material necesario para llevar a cabo las acciones de concienciación dirigidas a los empleados.",
        "Se ha realizado una auditoría para verificar el cumplimiento del plan de prevención y concienciación de la organización.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha clasificado y definido la taxonomía de incidentes de ciberseguridad que pueden afectar a la organización.",
        "Se han establecido controles, herramientas y mecanismos de monitorización, identificación, detección y alerta de incidentes",
        "Se han establecido controles y mecanismos de detección e identificación de incidentes de seguridad física.",
        "Se han establecido controles, herramientas y mecanismos de monitorización, identificación, detección y alerta de incidentes a través de la investigación en fuentes abiertas (OSINT: Open Source Intelligence).",
        "Se ha realizado una clasificación, valoración, documentación y seguimiento de los incidentes detectados dentro de la organización.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han recopilado y almacenado de forma segura evidencias de incidentes de ciberseguridad que afectan a la organización.",
        "Se ha realizado un análisis de evidencias.",
        "Se ha realizado la investigación de incidentes de ciberseguridad.",
        "Se ha intercambiado información de incidentes, con proveedores y/o organismos competentes que podrían hacer aportaciones al respecto.",
        "Se han iniciado las primeras medidas de contención de los incidentes para limitar los posibles daños causados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han desarrollado procedimientos de actuación detallados para dar respuesta, mitigar, eliminar o contener los tipos de incidentes de ciberseguridad más habituales.",
        "Se han preparado respuestas ciberresilientes ante incidentes que permitan seguir prestando los servicios de la organización y fortaleciendo las capacidades de identificación, detección, prevención, contención, recuperación y cooperación con terceros.",
        "Se ha establecido un flujo de toma de decisiones y escalado de incidentes interno y/o externo adecuados.",
        "Se han llevado a cabo las tareas de restablecimiento de los servicios afectados por un incidente hasta confirmar la vuelta a la normalidad.",
        "Se han documentado las acciones realizadas y las conclusiones que permitan mantener un registro de “lecciones aprendidas”.",
        "Se ha realizado un seguimiento adecuado del incidente para evitar que una situación similar se vuelva a repetir.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha desarrollado un procedimiento de actuación detallado para la notificación de incidentes de ciberseguridad en los tiempos adecuados.",
        "Se ha notificado el incidente de manera adecuada al personal interno de la organización responsable de la toma de decisiones.",
        "Se ha notificado el incidente de manera adecuada a las autoridades competentes en el ámbito de la gestión de incidentes de ciberseguridad en caso de ser necesario.",
        "Se ha notificado formalmente el incidente a los afectados, personal interno, clientes, proveedores, etc., en caso de ser necesario.",
        "Se ha notificado el incidente a los medios de comunicación en caso de ser necesario.",
    ], start=1)],
}

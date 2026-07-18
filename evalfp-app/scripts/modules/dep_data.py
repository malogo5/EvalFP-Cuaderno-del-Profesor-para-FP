"""EvalFP — Despliegue de Aplicaciones Web (DEP) · 0614 · 2º DAW · RD 686/2010 (actualizado RD 405/2023)"""
MODULO = {
    "nombre":"Despliegue de Aplicaciones Web","codigo":"0614","abrev":"DAW-Depl",
    "ciclo":"Desarrollo de Aplicaciones Web (DAW)","ciclo_clave":"DAW","ciclo_nivel":"CFGS",
    "curso":"2º DAW","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 686/2010, de 20 de mayo · Decreto CLM 230/2011, de 28 de julio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Implantación de arquitecturas web","horas":22,"eval":1,"tags":"DNS · Dominios · Hosting · VPS · CDN · HTTPS"},
    {"id":"UT2","nombre":"Administración de servidores web","horas":26,"eval":1,"tags":"Nginx · Apache · Virtualhost · SSL/TLS · WAF"},
    {"id":"UT3","nombre":"Control de versiones y repositorios","horas":20,"eval":2,"tags":"Git · GitHub · GitLab · Ramas · Pull Requests · Gitflow"},
    {"id":"UT4","nombre":"Integración y despliegue continuos (CI/CD)","horas":28,"eval":2,"tags":"GitHub Actions · GitLab CI · Jenkins · Pipelines · Automatización"},
    {"id":"UT5","nombre":"Contenedores y orquestación","horas":32,"eval":3,"tags":"Docker · Docker Compose · Kubernetes · Registro de imágenes"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Implanta arquitecturas web analizando y aplicando criterios de funcionalidad y disponibilidad."},
    {"id":"RA2","pond":20,"nombre":"Gestiona servidores web evaluando y aplicando criterios de configuración para el acceso seguro a los servicios."},
    {"id":"RA3","pond":20,"nombre":"Implanta aplicaciones web en servidores de aplicaciones aplicando criterios de seguridad y disponibilidad."},
    {"id":"RA4","pond":20,"nombre":"Aplica mecanismos de control de versiones integrando su uso en el proceso de despliegue de aplicaciones web."},
    {"id":"RA5","pond":20,"nombre":"Implanta y gestiona infraestructuras mediante contenedores valorando sus características y posibilidades."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los fundamentos del alojamiento web y tipos de hospedaje.",
        "Se han configurado dominios y registros DNS.",
        "Se ha implantado un certificado SSL/TLS con Let's Encrypt.",
        "Se han configurado redirecciones HTTP/HTTPS.",
        "Se han utilizado servicios de CDN para la distribución de contenido.",
        "Se ha configurado y verificado la disponibilidad del servicio.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha instalado y configurado un servidor web Nginx.",
        "Se han creado y configurado hosts virtuales.",
        "Se han configurado reglas de reescritura de URL.",
        "Se ha configurado la compresión y caché de recursos.",
        "Se han aplicado medidas de seguridad en el servidor web.",
        "Se han interpretado los logs del servidor para detectar incidencias.",
        "Se ha implementado un balanceador de carga básico.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las fases de un proceso de despliegue.",
        "Se han configurado variables de entorno para distintos entornos.",
        "Se han automatizado pruebas de integración antes del despliegue.",
        "Se han configurado pipelines de CI/CD.",
        "Se ha implantado una estrategia de despliegue (blue-green, rolling).",
        "Se han monitorizado los despliegues y configurado alertas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y aplicado los conceptos de control de versiones distribuido.",
        "Se han gestionado ramas y fusiones en repositorios Git.",
        "Se han utilizado plataformas de alojamiento de código (GitHub/GitLab).",
        "Se han aplicado flujos de trabajo de desarrollo (Gitflow, trunk-based).",
        "Se han revisado y aprobado cambios mediante pull/merge requests.",
        "Se han resuelto conflictos de fusión.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la utilidad de los contenedores en el despliegue de aplicaciones.",
        "Se han creado imágenes Docker a partir de Dockerfiles.",
        "Se han ejecutado y gestionado contenedores.",
        "Se han definido entornos multi-contenedor con Docker Compose.",
        "Se han publicado imágenes en un registro de contenedores.",
        "Se han descrito las características básicas de la orquestación con Kubernetes.",
    ], start=1)],
}

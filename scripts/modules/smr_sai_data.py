"""EvalFP — Seguridad Informática (SAI) · 0226 · 2º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Seguridad Informática","codigo":"0226","abrev":"SAI",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":4,"total_horas":128,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Criterios generales de seguridad","horas":20,"eval":1,"tags":"Amenazas · Vulnerabilidades · Riesgos · Políticas de seguridad"},
    {"id":"UT2","nombre":"Seguridad pasiva","horas":22,"eval":1,"tags":"CPD · SAI · RAID · Copias de seguridad · Control de acceso físico"},
    {"id":"UT3","nombre":"Seguridad lógica","horas":24,"eval":1,"tags":"Contraseñas · Cifrado · Certificados · Antivirus · Actualizaciones"},
    {"id":"UT4","nombre":"Seguridad en redes corporativas","horas":30,"eval":2,"tags":"Cortafuegos · IDS · IPS · DMZ · VPN"},
    {"id":"UT5","nombre":"Criptografía","horas":16,"eval":2,"tags":"Simétrica · Asimétrica · Hash · PKI · TLS/SSL"},
    {"id":"UT6","nombre":"Normativa de seguridad","horas":16,"eval":3,"tags":"RGPD · LOPD · ENS · ISO 27001 · Auditoría"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Adopta pautas y prácticas de tratamiento seguro de la información, reconociendo las vulnerabilidades de un sistema informático."},
    {"id":"RA2","pond":20,"nombre":"Implanta mecanismos de seguridad activa, seleccionando y ejecutando contramedidas ante amenazas o ataques al sistema."},
    {"id":"RA3","pond":20,"nombre":"Implanta técnicas de seguridad remota, eligiendo algoritmos criptográficos y protocolos seguros."},
    {"id":"RA4","pond":20,"nombre":"Implanta cortafuegos para asegurar un sistema informático, analizando sus prestaciones y controlando el tráfico hacia la red interna."},
    {"id":"RA5","pond":15,"nombre":"Implanta servidores proxy, aplicando criterios de administración y configuración que garanticen el funcionamiento seguro del servicio."},
    {"id":"RA6","pond":10,"nombre":"Implanta soluciones de alta disponibilidad analizando las distintas opciones y asegurando la continuidad de los servicios."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA1",["CR7","CR8"]),
    ("UT3","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los problemas de seguridad más habituales en los sistemas informáticos.",
        "Se han descrito las amenazas a la seguridad de la información.",
        "Se han identificado las vulnerabilidades de sistemas informáticos.",
        "Se han descrito las técnicas de seguridad más habituales.",
        "Se han aplicado políticas de contraseñas seguras.",
        "Se han descrito los principios de seguridad de la información.",
        "Se han clasificado los tipos de copias de seguridad.",
        "Se han implantado procedimientos de copias de seguridad.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de software malicioso.",
        "Se han instalado y configurado sistemas antivirus.",
        "Se ha comprobado el correcto funcionamiento del antivirus.",
        "Se han aplicado actualizaciones del sistema operativo y aplicaciones.",
        "Se han configurado sistemas de autenticación segura.",
        "Se ha configurado el cifrado de sistemas de ficheros.",
        "Se han documentado las medidas de seguridad aplicadas.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los métodos de criptografía simétrica y asimétrica.",
        "Se ha descrito la infraestructura de clave pública (PKI).",
        "Se han generado certificados digitales.",
        "Se ha configurado el protocolo HTTPS en servidores web.",
        "Se han configurado VPN para el acceso remoto seguro.",
        "Se han descrito los protocolos de seguridad en redes inalámbricas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los tipos de cortafuegos y sus características.",
        "Se ha instalado y configurado un cortafuegos.",
        "Se han definido reglas de filtrado de paquetes.",
        "Se ha configurado una DMZ.",
        "Se han monitoriado los logs del cortafuegos.",
        "Se han documentado las reglas del cortafuegos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los tipos de proxy y sus funciones.",
        "Se ha instalado y configurado un proxy.",
        "Se han configurado los clientes para usar el proxy.",
        "Se han establecido filtros de contenido.",
        "Se han analizado los logs del proxy.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los conceptos de disponibilidad y continuidad del servicio.",
        "Se ha descrito la normativa sobre protección de datos (RGPD).",
        "Se han identificado las obligaciones legales relativas a la seguridad.",
        "Se ha descrito el Esquema Nacional de Seguridad (ENS).",
        "Se han identificado las fases de una auditoría de seguridad.",
    ], start=1)],
}

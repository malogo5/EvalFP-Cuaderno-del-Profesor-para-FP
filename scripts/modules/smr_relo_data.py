"""EvalFP — Redes Locales (RELO) · 0224 · 1º SMR · RD 1691/2007"""
MODULO = {
    "nombre":"Redes Locales","codigo":"0224","abrev":"RELO",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"1º SMR","horas_sem":6,"total_horas":192,"anno":"2026-2027","eval_count":3,
    "decreto": "RD 1691/2007, de 14 de diciembre · Decreto CLM 107/2009, de 4 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Caracterización de redes locales","horas":28,"eval":1,"tags":"Topologías · Medios de transmisión · OSI · TCP/IP"},
    {"id":"UT2","nombre":"Instalación física de una red","horas":35,"eval":1,"tags":"Cableado · RJ45 · Fibra óptica · Wi-Fi · Rack"},
    {"id":"UT3","nombre":"Configuración y administración de conmutadores","horas":35,"eval":1,"tags":"Switch · VLANs · STP · Trunking · CDP/LLDP"},
    {"id":"UT4","nombre":"Configuración y administración de routers","horas":35,"eval":2,"tags":"Router · Enrutamiento estático · RIP · NAT · ACLs"},
    {"id":"UT5","nombre":"Configuración de redes inalámbricas","horas":28,"eval":2,"tags":"Wi-Fi · WPA2/3 · AP · SSID · Canales · QoS"},
    {"id":"UT6","nombre":"Resolución de incidencias en redes locales","horas":31,"eval":3,"tags":"Ping · Traceroute · Wireshark · Nmap · Incidencias"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Reconoce la estructura de las redes de datos identificando sus elementos y principios de funcionamiento."},
    {"id":"RA2","pond":20,"nombre":"Despliega el cableado de una red de datos con criterios de calidad y seguridad."},
    {"id":"RA3","pond":20,"nombre":"Interconecta equipos en redes cableadas e inalámbricas identificando y usando los dispositivos de interconexión."},
    {"id":"RA4","pond":20,"nombre":"Gestiona dispositivos de interconexión de redes, administrando sus prestaciones y configuraciones."},
    {"id":"RA5","pond":25,"nombre":"Mantiene una red de área local interpretando la información obtenida con las herramientas de monitorización y diagnóstico."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT5","RA3",["CR7","CR8","CR9"]),
    ("UT6","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["examen","practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los principios de las redes de comunicaciones y su evolución.",
        "Se han identificado los tipos de redes y sus topologías.",
        "Se han descrito los protocolos de comunicaciones de las redes locales.",
        "Se han identificado los medios de transmisión y sus características.",
        "Se han descrito los modelos de referencia OSI y TCP/IP.",
        "Se han identificado y descrito los protocolos de la familia TCP/IP.",
        "Se ha descrito la estructura y el direccionamiento IP.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido los tipos de cableado estructurado y sus categorías.",
        "Se han crimpado conectores RJ45 en los cables de red.",
        "Se han montado rosetas y paneles de parcheo.",
        "Se han instalado y etiquetado el cableado en racks.",
        "Se han realizado pruebas de verificación del cableado.",
        "Se han reconocido las características y ventajas de la fibra óptica.",
        "Se ha documentado la instalación del cableado.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los dispositivos de interconexión de redes.",
        "Se han instalado y configurado concentradores y conmutadores.",
        "Se han configurado VLANs en conmutadores.",
        "Se ha configurado el protocolo Spanning Tree (STP).",
        "Se han instalado puntos de acceso inalámbricos.",
        "Se han configurado redes Wi-Fi con los parámetros adecuados.",
        "Se han configurado protocolos de seguridad inalámbrica (WPA2/3).",
        "Se han realizado pruebas de conectividad.",
        "Se han documentado las configuraciones realizadas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado routers con interfaces LAN y WAN.",
        "Se han configurado tablas de enrutamiento estático.",
        "Se ha configurado el protocolo de enrutamiento dinámico RIP.",
        "Se ha configurado NAT para el acceso a Internet.",
        "Se han configurado listas de control de acceso (ACLs).",
        "Se han configurado servidores DHCP en el router.",
        "Se ha verificado el funcionamiento del enrutamiento.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los síntomas y causas de las averías más habituales en redes.",
        "Se han utilizado los comandos de diagnóstico básico de redes.",
        "Se ha utilizado un analizador de protocolos para inspeccionar el tráfico.",
        "Se han identificado y resuelto incidencias en la capa física.",
        "Se han identificado y resuelto incidencias en la configuración IP.",
        "Se han registrado y documentado las incidencias y sus soluciones.",
        "Se han realizado pruebas de rendimiento de la red.",
    ], start=1)],
}

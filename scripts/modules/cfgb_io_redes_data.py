"""EvalFP — Instalación y Mantenimiento de Redes para Transmisión de Datos · 3016 · FPB Informática de Oficina
RD 356/2014, de 16 de mayo (BOE) · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])
"""
MODULO = {
    "nombre":"Instalación y Mantenimiento de Redes para Transmisión de Datos","codigo":"3016","abrev":"REDES",
    "ciclo":"","ciclo_clave":"CFGB","ciclo_nivel":"CFGB",
    "curso":"2º IO","horas_sem":7,"total_horas":210,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 356/2014, de 16 de mayo · Decreto CLM 80/2014, de 1 de agosto (DOCM [2014/10283])",
}
UTS = [
    {"id":"UT1","nombre":"Elementos de redes de voz y datos","horas":35,"eval":1,"tags":"Cableado · Conectores · Canaletas · Armarios · Equipos activos · Topologías"},
    {"id":"UT2","nombre":"Canalización y soportes","horas":35,"eval":1,"tags":"Bandejas · Canaletas · Tubos · Soportes · Armarios de distribución"},
    {"id":"UT3","nombre":"Despliegue del cableado estructurado","horas":35,"eval":2,"tags":"Cable UTP · Fibra óptica · Trazado · Crimpado · Conectores RJ-45"},
    {"id":"UT4","nombre":"Instalación de elementos y sistemas","horas":35,"eval":2,"tags":"Rosetas · Patch panel · Switch · Access point · Tomas de red"},
    {"id":"UT5","nombre":"Configuración básica de redes locales","horas":35,"eval":3,"tags":"TCP/IP · Ping · Ipconfig · Switch · DHCP básico · Verificación"},
    {"id":"UT6","nombre":"Prevención de riesgos laborales y medioambiente","horas":35,"eval":3,"tags":"EPI · Escaleras · Herramientas eléctricas · Residuos · Normativa"},
]
RAS = [
    {"id":"RA1","pond":15,"nombre":"Selecciona los elementos que configuran las redes para la transmisión de voz y datos, identificando sus características y aplicaciones."},
    {"id":"RA2","pond":18,"nombre":"Monta canalizaciones, soportes y armarios en redes de transmisión de voz y datos, interpretando la documentación técnica."},
    {"id":"RA3","pond":18,"nombre":"Despliega el cableado de una red de voz y datos analizando su trazado e interpretando la simbología y documentación técnica."},
    {"id":"RA4","pond":18,"nombre":"Instala elementos y sistemas de transmisión de voz y datos, interpretando la documentación técnica y verificando su funcionamiento."},
    {"id":"RA5","pond":18,"nombre":"Realiza operaciones básicas de configuración en redes locales cableadas e inalámbricas, interpretando el diseño de red facilitado."},
    {"id":"RA6","pond":13,"nombre":"Cumple las normas de prevención de riesgos laborales y de protección ambiental, identificando los riesgos asociados y las medidas y equipos para prevenirlos."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5","RA6"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5","RA6"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de red según su extensión y tecnología.",
        "Se han identificado los medios de transmisión más habituales en redes de área local —par trenzado, fibra óptica, inalámbrico—.",
        "Se han descrito las características de los equipos activos de red —switch, router, punto de acceso Wi-Fi—.",
        "Se han identificado los conectores y elementos pasivos de red —rosetas, latiguillos, patch panel—.",
        "Se han descrito los principales estándares de cableado estructurado y sus características.",
        "Se ha valorado la importancia de cumplir con los estándares en la instalación de redes.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos tipos de canalizaciones y soportes utilizados en redes de voz y datos.",
        "Se han interpretado planos y esquemas de instalación de redes.",
        "Se han montado canaletas y bandejas portacables siguiendo el trazado indicado.",
        "Se han instalado tubos y conductos de protección del cableado.",
        "Se han montado cajas de registro y cajas de toma de red.",
        "Se han instalado y rack y armarios de distribución, verificando su nivelado y fijación.",
        "Se han aplicado las medidas de seguridad en el trabajo con herramientas y en altura.",
        "Se ha comprobado la solidez y corrección del montaje realizado.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado el trazado del cableado estructurado indicado en la documentación técnica.",
        "Se ha tendido el cable de red por los soportes y canalizaciones instalados, respetando los radios de curvatura.",
        "Se han confeccionado latiguillos RJ-45 utilizando la herramienta de crimpar y verificando su continuidad.",
        "Se han realizado conexiones en rosetas, patch panel y cajas de toma siguiendo el estándar indicado.",
        "Se han identificado y etiquetado los cables tendidos siguiendo el esquema de la instalación.",
        "Se ha comprobado la continuidad y ausencia de cruces en el cableado mediante comprobador.",
        "Se han aplicado técnicas de protección del cableado frente a interferencias electromagnéticas.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han instalado rosetas y tomas de red en las cajas de registro.",
        "Se ha realizado el parcheo en el patch panel, conectando los cables al puerto correspondiente.",
        "Se ha instalado el switch y el router en el armario de distribución, conectando los latiguillos de red.",
        "Se han instalado puntos de acceso inalámbricos siguiendo las instrucciones del fabricante.",
        "Se ha verificado la conectividad de cada puesto de trabajo con el switch mediante comprobador de red.",
        "Se han documentado las conexiones realizadas actualizando el esquema de la instalación.",
        "Se han realizado pruebas de funcionamiento del servicio de telefonía IP básico.",
        "Se han detectado y resuelto incidencias básicas de la instalación.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han configurado los parámetros IP básicos de los equipos de usuario conectados a la red.",
        "Se han verificado la conectividad entre equipos mediante las herramientas ping e ipconfig/ifconfig.",
        "Se han configurado los parámetros básicos de un switch —VLAN de gestión, contraseña— siguiendo las instrucciones facilitadas.",
        "Se ha configurado la red inalámbrica —SSID, canal, cifrado WPA2— en el punto de acceso.",
        "Se ha comprobado la conectividad inalámbrica verificando la asociación de los equipos al punto de acceso.",
        "Se han identificado y resuelto incidencias básicas de configuración de red.",
        "Se ha documentado la configuración realizada completando la ficha de la instalación.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los riesgos profesionales más frecuentes en la instalación de redes —caídas, cortes, descargas eléctricas—.",
        "Se han descrito las medidas preventivas y los equipos de protección individual (EPI) aplicables.",
        "Se han identificado las zonas de peligro en el uso de escaleras de mano y andamios.",
        "Se han manejado con seguridad las herramientas eléctricas y manuales utilizadas en la instalación.",
        "Se ha reconocido la señalización de seguridad de las zonas de trabajo.",
        "Se han identificado los residuos generados clasificándolos según su naturaleza y las normas de gestión.",
        "Se han depositado los residuos en los contenedores adecuados conforme a la normativa medioambiental.",
        "Se ha valorado la importancia de respetar las normas de prevención de riesgos laborales y protección del medio ambiente.",
    ], start=1)],
}

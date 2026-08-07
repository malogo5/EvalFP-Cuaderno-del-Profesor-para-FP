"""EvalFP — Seguridad y Alta Disponibilidad · 0378 · Administración de Sistemas Informáticos en Red (ASIR)
Decreto 200/2010, de 03/08/2010, currículo del ciclo de Administración de Sistemas Informáticos en Red en Castilla-La Mancha (DOCM, NID 2010/13389) · RA y CE literales del Anexo I
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 159 h · 4 h/semana · 2º ASIR.
"""
MODULO = {
    "nombre":"Seguridad y Alta Disponibilidad","codigo":"0378","abrev":"SAD",
    "ciclo":"Administración de Sistemas Informáticos en Red (ASIR)","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"2º ASIR","horas_sem":4,"total_horas":159,"anno":"2026-2027","eval_count":3,
    "decreto":"Decreto 200/2010, de 03/08/2010, currículo del ciclo de Administración de Sistemas Informáticos en Red en Castilla-La Mancha (DOCM, NID 2010/13389) · RA y CE literales del Anexo I",
}
UTS = [
    {"id":"UT1","nombre":"Adopta pautas y prácticas de tratamiento seguro de la información","horas":27,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Implanta mecanismos de seguridad activa","horas":24,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Implanta técnicas seguras de acceso remoto a un sistema informático","horas":19,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Implanta cortafuegos para asegurar un sistema informático","horas":22,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Implantación de servidores proxy","horas":24,"eval":2,"tags":"Squid · HAProxy · Reverse Proxy · WAF"},
    {"id":"UT6","nombre":"Implanta soluciones de alta disponibilidad empleando técnicas de…","horas":24,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Reconoce la legislación y normativa sobre seguridad y protección de…","horas":19,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":17,"nombre":"Adopta pautas y prácticas de tratamiento seguro de la información, reconociendo las vulnerabilidades de un sistema informático y la necesidad de asegurarlo."},
    {"id":"RA2","pond":15,"nombre":"Implanta mecanismos de seguridad activa, seleccionando y ejecutando contramedidas ante amenazas o ataques al sistema."},
    {"id":"RA3","pond":12,"nombre":"Implanta técnicas seguras de acceso remoto a un sistema informático, interpretando y aplicando el plan de seguridad."},
    {"id":"RA4","pond":14,"nombre":"Implanta cortafuegos para asegurar un sistema informático, analizando sus prestaciones y controlando el tráfico hacia la red interna."},
    {"id":"RA5","pond":15,"nombre":"Implanta servidores «proxy», aplicando criterios de configuración que garanticen el funcionamiento seguro del servicio."},
    {"id":"RA6","pond":15,"nombre":"Implanta soluciones de alta disponibilidad empleando técnicas de vitalización y configurando los entornos de prueba."},
    {"id":"RA7","pond":12,"nombre":"Reconoce la legislación y normativa sobre seguridad y protección de datos valorando su importancia."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4","RA5"], 3:["RA6","RA7"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de asegurar la privacidad, coherencia y disponibilidad de la información en los sistemas informáticos.",
        "Se han descrito las diferencias entre seguridad física y lógica.",
        "Se han clasificado las principales vulnerabilidades de un sistema informático, según su tipología y origen.",
        "Se ha contrastado la incidencia de las técnicas de ingeniería social en los fraudes informáticos.",
        "Se han adoptado políticas de contraseñas.",
        "Se han valorado las ventajas que supone la utilización de sistemas biométricos.",
        "Se han aplicado técnicas criptográficas en el almacenamiento y transmisión de la información.",
        "Se ha reconocido la necesidad de establecer un plan integral de protección perimetral, especialmente en sistemas conectados a redes públicas.",
        "Se han identificado las fases del análisis forense ante ataques a un sistema.",
        "Se han identificado las herramientas hardware y software para realizar un análisis forense.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado los principales tipos de amenazas lógicas contra un sistema informático.",
        "Se ha verificado el origen y la autenticidad de las aplicaciones instaladas en un equipo, así como el estado de actualización del sistema operativo.",
        "Se han identificado la anatomía de los ataques más habituales, así como las medidas preventivas y paliativas disponibles.",
        "Se han analizado diversos tipos de amenazas, ataques y software malicioso, en entornos de ejecución controlados.",
        "Se han implantado aplicaciones específicas para la detección de amenazas y la eliminación de software malicioso.",
        "Se han utilizado técnicas de cifrado, firmas y certificados digitales en un entorno de trabajo basado en el uso de redes públicas.",
        "Se han evaluado las medidas de seguridad de los protocolos usados en redes inalámbricas.",
        "Se ha reconocido la necesidad de inventariar y controlar los servicios de red que se ejecutan en un sistema.",
        "Se han descrito los tipos y características de los sistemas de detección de intrusiones.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito escenarios típicos de sistemas con conexión a redes públicas en los que se precisa fortificar la red interna.",
        "Se han clasificado las zonas de riesgo de un sistema, según criterios de seguridad perimetral.",
        "Se han identificado los protocolos seguros de comunicación y sus ámbitos de utilización.",
        "Se han configurado redes privadas virtuales mediante protocolos seguros a distintos niveles.",
        "Se ha implantado un servidor como pasarela de acceso a la red interna desde ubicaciones remotas.",
        "Se han identificado y configurado los posibles métodos de autenticación en el acceso de usuarios remotos a través de la pasarela.",
        "Se ha instalado, configurado e integrado en la pasarela un servidor remoto de autenticación.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características, tipos y funciones de los cortafuegos.",
        "Se han clasificado los niveles en los que se realiza el filtrado de tráfico.",
        "Se ha planificado la instalación de cortafuegos para limitar los accesos a determinadas zonas de la red.",
        "Se han configurado filtros en un cortafuegos a partir de un listado de reglas de filtrado.",
        "Se han revisado los registros de sucesos de cortafuegos, para verificar que las reglas se aplican correctamente.",
        "Se han probado distintas opciones para implementar cortafuegos, tanto software como hardware.",
        "Se han diagnosticado problemas de conectividad en los clientes provocados por los cortafuegos.",
        "Se ha elaborado documentación relativa a la instalación, configuración y uso de cortafuegos.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los tipos de «proxy», sus características y funciones principales.",
        "Se ha instalado y configurado un servidor «proxy-cache».",
        "Se han configurado los métodos de autenticación en el «proxy».",
        "Se ha configurado un «proxy» en modo transparente.",
        "Se ha utilizado el servidor «proxy» para establecer restricciones de acceso Web.",
        "Se han solucionado problemas de acceso desde los clientes al «proxy».",
        "Se han realizado pruebas de funcionamiento del «proxy», monitorizando su actividad con herramientas gráficas.",
        "Se ha configurado un servidor «proxy» en modo inverso.",
        "Se ha elaborado documentación relativa a la instalación, configuración y uso de servidores «proxy».",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado supuestos y situaciones en las que se hace necesario implementar soluciones de alta disponibilidad.",
        "Se han identificado soluciones hardware para asegurar la continuidad en el funcionamiento de un sistema.",
        "Se han evaluado las posibilidades de la vitalización de sistemas para implementar soluciones de alta disponibilidad.",
        "Se ha implantado un servidor redundante que garantice la continuidad de servicios en casos de caída del servidor principal.",
        "Se ha implantado un balanceador de carga a la entrada de la red interna.",
        "Se han implantado sistemas de almacenamiento redundante sobre servidores y dispositivos específicos.",
        "Se ha evaluado la utilidad de los sistemas de «clúster» para aumentar la fiabilidad y productividad del sistema.",
        "Se han analizado soluciones de futuro para un sistema con demanda creciente.",
        "Se han esquematizado y documentado soluciones para diferentes supuestos con necesidades de alta disponibilidad.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la legislación sobre protección de datos de carácter personal.",
        "Se ha determinado la necesidad de controlar el acceso a la información personal almacenada.",
        "Se han identificado las figuras legales que intervienen en el tratamiento y mantenimiento de los ficheros de datos.",
        "Se ha contrastado el deber de poner a disposición de las personas los datos personales que les conciernen.",
        "Se ha descrito la legislación actual sobre los servicios de la sociedad de la información y comercio electrónico.",
        "Se han contrastado las normas sobre gestión de seguridad de la información.",
        "Se ha comprendido la necesidad de conocer y respetar la normativa legal aplicable.",
    ], start=1)],
}

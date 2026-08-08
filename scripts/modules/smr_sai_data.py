"""EvalFP — Seguridad Informática · 0226 · Sistemas Microinformáticos y Redes (SMR)
Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 167 h · 4 h/semana · 2º SMR.
"""
MODULO = {
    "nombre":"Seguridad Informática","codigo":"0226","abrev":"SI",
    "ciclo":"Sistemas Microinformáticos y Redes (SMR)","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":4,"total_horas":167,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Aplica medidas de seguridad pasiva en sistemas informáticos","horas":33,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Gestiona dispositivos de almacenamiento","horas":43,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Aplica mecanismos de seguridad activa","horas":33,"eval":2,"tags":""},
    {"id":"UT4","nombre":"Asegura la privacidad de la información transmitida en redes…","horas":36,"eval":3,"tags":""},
    {"id":"UT5","nombre":"Reconoce la legislación y normativa sobre seguridad y protección de…","horas":22,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Aplica medidas de seguridad pasiva en sistemas informáticos describiendo características de entornos y relacionándolas con sus necesidades."},
    {"id":"RA2","pond":26,"nombre":"Gestiona dispositivos de almacenamiento describiendo los procedimientos efectuados y aplicando técnicas para asegurar la integridad de la información."},
    {"id":"RA3","pond":19,"nombre":"Aplica mecanismos de seguridad activa describiendo sus características y relacionándolas con las necesidades de uso del sistema informático."},
    {"id":"RA4","pond":22,"nombre":"Asegura la privacidad de la información transmitida en redes informáticas describiendo vulnerabilidades e instalando software especifico."},
    {"id":"RA5","pond":13,"nombre":"Reconoce la legislación y normativa sobre seguridad y protección de datos analizando las repercusiones de su incumplimiento."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11","CR12"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4","RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de mantener la información segura.",
        "Se han descrito las diferencias entre seguridad física y lógica.",
        "Se han definido las características de la ubicación física y condiciones ambientales de los equipos y servidores.",
        "Se ha identificado la necesidad de proteger físicamente los sistemas informáticos.",
        "Se ha verificado el funcionamiento de los sistemas de alimentación ininterrumpida.",
        "Se han seleccionado los puntos de aplicación de los sistemas de alimentación ininterrumpida.",
        "Se han esquematizado las características de una política de seguridad basada en listas de control de acceso.",
        "Se ha valorado la importancia de establecer una política de contraseñas.",
        "Se han valorado las ventajas que supone la utilización de sistemas biométricos.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado la documentación técnica relativa a la política de almacenamiento.",
        "Se han tenido en cuenta factores inherentes al almacenamiento de la información (rendimiento, disponibilidad, accesibilidad, entre otros).",
        "Se han clasificado y enumerado los principales métodos de almacenamiento incluidos los sistemas de almacenamiento en red.",
        "Se han descrito las tecnologías de almacenamiento redundante y distribuido.",
        "Se han clasificado los principales tipos de criptografía.",
        "Se han seleccionado estrategias para la realización de copias de seguridad.",
        "Se ha tenido en cuenta la frecuencia y el esquema de rotación.",
        "Se han realizado copias de seguridad con distintas estrategias.",
        "Se han identificado las características de los medios de almacenamiento remotos y extraíbles.",
        "Se han utilizado medios de almacenamiento remotos y extraíbles.",
        "Se han creado y restaurado imágenes de respaldo de sistemas en funcionamiento.",
        "Se han utilizado herramientas de chequeo de discos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han clasificado y enumerado los tipos de amenazas.",
        "Se han descrito los principales tipos de ataques.",
        "Se han aplicado técnicas de auditoría de sistemas.",
        "Se han seguido planes de contingencia para actuar ante fallos de seguridad.",
        "Se han clasificado los principales tipos de software malicioso.",
        "Se han realizado actualizaciones periódicas de los sistemas para corregir posibles vulnerabilidades.",
        "Se ha verificado el origen y la autenticidad de las aplicaciones que se instalan en los sistemas.",
        "Se han instalado, probado y actualizado aplicaciones específicas para la detección y eliminación de software malicioso.",
        "Se han aplicado técnicas de recuperación de datos.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha identificado la necesidad de inventariar y controlar los servicios de red.",
        "Se ha contrastado la incidencia de las técnicas de ingeniería social en los fraudes informáticos y robos de información.",
        "Se ha deducido la importancia de minimizar el volumen de tráfico generado por la publicidad y el correo no deseado.",
        "Se han aplicado medidas para evitar la monitorización de redes cableadas.",
        "Se han clasificado y valorado las propiedades de seguridad de los protocolos usados en redes inalámbricas.",
        "Se han descrito sistemas de identificación como la firma electrónica, certificado digital, entre otros.",
        "Se han utilizado sistemas de identificación como la firma electrónica, certificado digital, entre otros.",
        "Se han instalado, configurado y utilizado herramientas de cifrado.",
        "Se han descrito el uso de la tecnología de tarjetas inteligentes.",
        "Se ha instalado y configurado un cortafuegos en un equipo o servidor.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la legislación sobre protección de datos de carácter personal.",
        "Se ha determinado la necesidad de controlar el acceso a la información personal almacenada.",
        "Se han identificado las figuras legales que intervienen en el tratamiento y mantenimiento de los ficheros de datos.",
        "Se ha contrastado la obligación de poner a disposición de las personas los datos personales que les conciernen.",
        "Se ha descrito la legislación actual sobre los servicios de la sociedad de la información y comercio electrónico.",
        "Se han contrastado las normas sobre gestión de seguridad de la información.",
    ], start=1)],
}

"""EvalFP — Aplicaciones Ofimáticas · 0223 · Sistemas Microinformáticos y Redes
Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 270 h · 7 h/semana · 2º SMR.
"""
MODULO = {
    "nombre":"Aplicaciones Ofimáticas","codigo":"0223","abrev":"AO",
    "ciclo":"Sistemas Microinformáticos y Redes","ciclo_clave":"SMR","ciclo_nivel":"CFGM",
    "curso":"2º SMR","horas_sem":7,"total_horas":270,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3 2º · RA y CE: Decreto 107/2009, de 04/08/2009 (DOCM núm. 153, de 07/08/2009), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Instala y actualiza aplicaciones ofimáticas","horas":38,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Elabora documentos y plantillas","horas":29,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Elabora documentos y plantillas de cálculo","horas":33,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Elabora documentos con bases de datos ofimáticas","horas":33,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Elabora documentos haciendo uso de herramientas y plataformas que…","horas":8,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Manipula imágenes digitales","horas":21,"eval":2,"tags":""},
    {"id":"UT7","nombre":"Manipula secuencias de video","horas":21,"eval":2,"tags":""},
    {"id":"UT8","nombre":"Elabora presentaciones multimedia","horas":25,"eval":3,"tags":""},
    {"id":"UT9","nombre":"Realiza operaciones de gestión del correo y la agenda electrónica","horas":29,"eval":3,"tags":""},
    {"id":"UT10","nombre":"Aplica técnicas de soporte en el uso de aplicaciones","horas":33,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":14,"nombre":"Instala y actualiza aplicaciones ofimáticas, interpretando especificaciones y describiendo los pasos a seguir en el proceso."},
    {"id":"RA2","pond":11,"nombre":"Elabora documentos y plantillas, describiendo y aplicando las opciones avanzadas de procesadores de textos."},
    {"id":"RA3","pond":12,"nombre":"Elabora documentos y plantillas de cálculo, describiendo y aplicando opciones avanzadas de hojas de cálculo."},
    {"id":"RA4","pond":12,"nombre":"Elabora documentos con bases de datos ofimáticas describiendo y aplicando operaciones de manipulación de datos."},
    {"id":"RA5","pond":3,"nombre":"Elabora documentos haciendo uso de herramientas y plataformas que permiten compartir un espacio de información y de trabajo común."},
    {"id":"RA6","pond":8,"nombre":"Manipula imágenes digitales analizando las posibilidades de distintos programas y aplicando técnicas de captura y edición básicas."},
    {"id":"RA7","pond":8,"nombre":"Manipula secuencias de video analizando las posibilidades de distintos programas y aplicando técnicas de captura y edición básicas."},
    {"id":"RA8","pond":9,"nombre":"Elabora presentaciones multimedia describiendo y aplicando normas básicas de composición y diseño."},
    {"id":"RA9","pond":11,"nombre":"Realiza operaciones de gestión del correo y la agenda electrónica, relacionando necesidades de uso con su configuración."},
    {"id":"RA10","pond":12,"nombre":"Aplica técnicas de soporte en el uso de aplicaciones, identificando y resolviendo incidencias."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT8","RA8",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT9","RA9",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT10","RA10",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5","RA6","RA7"], 3:["RA8","RA9","RA10"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["practica"],
    "RA2":["practica"],
    "RA3":["practica"],
    "RA4":["practica"],
    "RA5":["practica"],
    "RA6":["practica"],
    "RA7":["examen","practica"],
    "RA8":["examen","practica"],
    "RA9":["examen","practica"],
    "RA10":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado y establecido las fases del proceso de instalación.",
        "Se han respetado las especificaciones técnicas del proceso de instalación.",
        "Se han configurado las aplicaciones según los criterios establecidos.",
        "Se han documentado las incidencias.",
        "Se han solucionado problemas en la instalación o integración con el sistema informático.",
        "Se han eliminado y/o añadido componentes de la instalación en el equipo.",
        "Se han actualizado las aplicaciones.",
        "Se han respetado las licencias software.",
        "Se han propuesto soluciones software para entornos de aplicación.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha personalizado las opciones de software y barra de herramientas.",
        "Se han diseñado plantillas.",
        "Se han utilizado aplicaciones y periféricos para introducir textos e imágenes.",
        "Se han importado y exportado documentos creados con otras aplicaciones y en otros formatos.",
        "Se han creado y utilizado macros en la realización de documentos.",
        "Se han elaborado manuales específicos.",
        "Se han generando versiones de un documento o haciendo uso del control de cambios de forma coordinada y grupal.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha personalizado las opciones de software y barra de herramientas.",
        "Se han utilizado los diversos tipos de datos y referencia para celdas, rangos, hojas y libros.",
        "Se han aplicado fórmulas y funciones.",
        "Se han generado y modificado gráficos de diferentes tipos.",
        "Se han empleado macros para la realización de documentos y plantillas.",
        "Se han importado y exportado hojas de cálculo creadas con otras aplicaciones y en otros formatos.",
        "Se ha utilizado la hoja de cálculo como base de datos: formularios, creación de listas, filtrado, protección y ordenación de datos.",
        "Se han utilizado aplicaciones y periféricos para introducir textos, números, códigos e imágenes.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los elementos de las bases de datos relacionales.",
        "Se han creado bases de datos ofimáticas.",
        "Se han utilizado las tablas de la base de datos (insertar, modificar y eliminar registros).",
        "Se han utilizado asistentes en la creación de consultas.",
        "Se han utilizado asistentes en la creación de formularios.",
        "Se han utilizado asistentes en la creación de informes.",
        "Se ha realizado búsqueda y filtrado sobre la información almacenada.",
        "Se han creado y utilizado macros.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos métodos que permiten el trabajo colaborativo.",
        "Se han utilizado herramientas sincrónicas y asíncronas para la creación de documentos de forma coordinada y grupal.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los distintos formatos de imágenes.",
        "Se ha realizado la adquisición de imágenes con periféricos.",
        "Se ha trabajado con imágenes a diferentes resoluciones, según su finalidad.",
        "Se han empleado herramientas para la edición de imagen digital.",
        "Se han importado y exportado imágenes en diversos formatos.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido los elementos que componen una secuencia de video.",
        "Se han estudiado los tipos de formatos y codecs más empleados.",
        "Se han importado y exportado secuencias de video.",
        "Se han capturado secuencias de video con recursos adecuados.",
        "Se han elaborado video tutoriales.",
    ], start=1)],
    "RA8":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las opciones básicas de las aplicaciones de presentaciones.",
        "Se han reconocido los distintos tipos de vista asociados a una presentación.",
        "Se han aplicado y reconocido las distintas tipografías y normas básicas de composición, diseño y utilización del color.",
        "Se han diseñado plantillas de presentaciones.",
        "Se han creado presentaciones.",
        "Se han utilizado periféricos para ejecutar presentaciones.",
    ], start=1)],
    "RA9":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los elementos que componen un correo electrónico.",
        "Se han analizado las necesidades básicas de gestión de correo y agenda electrónica.",
        "Se han configurado distintos tipos de cuentas de correo electrónico.",
        "Se han conectado y sincronizado agendas del equipo informático con dispositivos móviles.",
        "Se ha operado con la libreta de direcciones.",
        "Se ha trabajado con todas las opciones de gestión de correo electrónico (etiquetas, filtros, carpetas, entre otros).",
        "Se han utilizado opciones de agenda electrónica.",
    ], start=1)],
    "RA10":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han elaborado guías visuales con los conceptos básicos de uso de una aplicación.",
        "Se han identificado problemas relacionados con el uso de aplicaciones ofimáticas.",
        "Se han utilizado manuales de usuario para instruir en el uso de aplicaciones.",
        "Se han aplicado técnicas de asesoramiento en el uso de aplicaciones.",
        "Se han realizado informes de incidencias.",
        "Se han aplicado los procedimientos necesarios para salvaguardar la información y su recuperación.",
        "Se han utilizado los recursos disponibles (documentación técnica, ayudas en línea, soporte técnico, entre otros) para solventar incidencias.",
        "Se han solventando las incidencias en el tiempo adecuado y con el nivel de calidad esperado.",
    ], start=1)],
}

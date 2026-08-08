"""EvalFP — Recursos humanos y responsabilidad social corporativa · 0648 · Administración y Finanzas
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 68 h · 2 h/semana · 1º AF.
"""
MODULO = {
    "nombre":"Recursos humanos y responsabilidad social corporativa","codigo":"0648","abrev":"RHRSC",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"1º AF","horas_sem":2,"total_horas":68,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I-C.4º · RA y CE: Decreto 43/2013, de 25/07/2013 (DOCM núm. 148, de 01/08/2013), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Ética empresarial y cultura de empresa","horas":11,"eval":1,"tags":"Valores · Códigos éticos · Clima laboral · Comportamiento responsable"},
    {"id":"UT2","nombre":"Responsabilidad social corporativa","horas":9,"eval":1,"tags":"Grupos de interés · Memorias de sostenibilidad · ODS · Auditoría social"},
    {"id":"UT3","nombre":"Comunicación en el departamento de recursos humanos","horas":15,"eval":2,"tags":"Habilidades sociales · Motivación · Liderazgo · Trabajo en equipo · Gestión de conflictos"},
    {"id":"UT4","nombre":"Selección de personal","horas":15,"eval":2,"tags":"Perfil del puesto · Reclutamiento · Pruebas · Entrevista · Protección de datos"},
    {"id":"UT5","nombre":"Formación y desarrollo profesional","horas":18,"eval":3,"tags":"Plan de formación · Detección de necesidades · Promoción · Evaluación del desempeño"},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Caracteriza la empresa como una comunidad de personas, distinguiendo las implicaciones éticas de su comportamiento con respecto a los implicados en la misma."},
    {"id":"RA2","pond":13,"nombre":"Contrasta la aplicación de los principios de responsabilidad social corporativa en las políticas de desarrollo de los recursos humanos de las empresas, valorando su adecuación a las buenas prácticas validadas internacionalmente."},
    {"id":"RA3","pond":22,"nombre":"Coordina los flujos de información del departamento de recursos humanos a través de la organización, aplicando habilidades personales y sociales en procesos de gestión de recursos humanos."},
    {"id":"RA4","pond":22,"nombre":"Aplica los procedimientos administrativos relativos a la selección de recursos humanos, eligiendo los métodos e instrumentos más adecuados a la política de cada organización."},
    {"id":"RA5","pond":27,"nombre":"Gestiona los procedimientos administrativos relativos a la formación, promoción y desarrollo de recursos humanos, designando los métodos e instrumentos más adecuados."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["practica","examen"],
    "RA4":["practica","examen"],
    "RA5":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han determinado las diferentes actividades realizadas en la empresa, las personas implicadas y su responsabilidad en las mismas.",
        "Se han identificado claramente las variables éticas y culturales de las organizaciones.",
        "Se han evaluado las implicaciones entre competitividad empresarial y comportamiento ético.",
        "Se han definido estilos éticos de adaptación a los cambios empresariales, a la globalización y a la cultura social presente.",
        "Se han seleccionado indicadores para el diagnóstico de las relaciones de las empresas y los interesados (stakeholders).",
        "Se han determinado elementos de mejora de las comunicaciones de las organizaciones externas e internas que promuevan la transparencia, la cooperación y la confianza.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido el concepto de responsabilidad social corporativa (RSC).",
        "Se han analizado las políticas de recursos humanos en cuanto a motivación, mejora continua, promoción y recompensa, entre otros factores.",
        "Se han analizado las recomendaciones y la normativa europea, de organizaciones intergubernamentales, así como la nacional con respecto a RSC y desarrollo de los recursos humanos.",
        "Se han descrito las buenas prácticas e iniciativas en cuanto a códigos de conducta relacionados con los derechos de los trabajadores.",
        "Se han programado puntos de control para el contraste del cumplimiento de las políticas de RSC y códigos de conducta en la gestión de los recursos humanos.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las funciones que se deben desarrollar en el área de la empresa que se encarga de la gestión de recursos humanos.",
        "Se han caracterizado habilidades de comunicación efectiva en los diferentes roles laborales.",
        "Se han establecido los canales de comunicación interna entre los distintos departamentos de la empresa, así como entre el personal y los departamentos.",
        "Se ha analizado la información que proporcionan los sistemas de control de personal para la mejora de la gestión de la empresa.",
        "Se ha mantenido actualizada la información precisa para el desarrollo de las funciones del departamento de recursos humanos.",
        "Se ha establecido la manera de organizar y conservar la documentación del departamento de recursos humanos en soporte convencional e informático.",
        "Se ha utilizado un sistema informático para el almacenamiento y tratamiento de la información en la gestión de los recursos humanos.",
        "Se ha valorado la importancia de la aplicación de criterios de seguridad, confidencialidad, integridad y accesibilidad en la tramitación de la información derivada de la administración de recursos humanos.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los organismos y empresas relevantes en el mercado laboral, dedicados a la selección y formación de recursos humanos.",
        "Se han secuenciado las fases de un proceso de selección de personal y sus características fundamentales.",
        "Se ha identificado la información que se genera en cada una de las fases de un proceso de selección de personal.",
        "Se ha valorado la importancia del reconocimiento del concepto de perfil del puesto de trabajo para seleccionar los currículos.",
        "Se han establecidos las características de los métodos e instrumentos de selección de personal más utilizados en función del perfil del puesto de trabajo.",
        "Se ha elaborado la documentación necesaria para llevar a cabo el proceso de selección.",
        "Se han establecido las vías de comunicación orales y escritas con las personas que intervienen en el proceso de selección.",
        "Se ha registrado y archivado la información y documentación relevante del proceso de selección.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han planificado las fases de los procesos de formación y promoción de personal.",
        "Se han establecido las características de los métodos e instrumentos de los procesos de formación.",
        "Se ha identificado la información que se genera en cada una de las fases de los procesos de formación y promoción de personal.",
        "Se ha elaborado la documentación necesaria para efectuar los procesos de formación y promoción de personal.",
        "Se han establecido los métodos de valoración del trabajo y de incentivos.",
        "Se ha recabado información sobre las necesidades formativas de la empresa.",
        "Se han detectado las necesidades de recursos materiales y humanos en el proceso de formación.",
        "Se han establecido las vías de comunicación orales y escritas con las personas que intervienen en los procesos de formación y promoción.",
        "Se ha registrado y archivado la información y documentación relevante de los procesos de formación y promoción de personal.",
        "Se han aplicado los procedimientos administrativos de seguimiento y evaluación de la formación.",
    ], start=1)],
}

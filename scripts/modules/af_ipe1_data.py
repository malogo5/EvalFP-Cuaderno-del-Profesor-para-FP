"""EvalFP — Itinerario personal para la empleabilidad I · 1709 · Administración y Finanzas
Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo V del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)
Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,
remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.
Duración: 80 h · 3 h/semana · 1º AF.
UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.
"""
MODULO = {
    "nombre":"Itinerario personal para la empleabilidad I","codigo":"1709","abrev":"IPE1",
    "ciclo":"Administración y Finanzas","ciclo_clave":"AF","ciclo_nivel":"CFGS",
    "curso":"1º AF","horas_sem":3,"total_horas":80,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas, curso y h/semana: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Anexo V del RD 659/2023 (por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto consolidado)",
}
UTS = [
    {"id":"UT1","nombre":"Distingue las características del sector productivo y define…","horas":6,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Adquiere las competencias necesarias para el desempeño de…","horas":19,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Analiza sus condiciones laborales como persona trabajadora…","horas":14,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Analiza y evalúa su potencial profesional y sus intereses…","horas":23,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Aplica las estrategias para el aprendizaje autónomo…","horas":18,"eval":2,"tags":""},
]
RAS = [
    {"id":"RA1","pond":8,"nombre":"Distingue las características del sector productivo y define los puestos de trabajo relacionándolos con las competencias profesionales expresadas en el título."},
    {"id":"RA2","pond":23,"nombre":"Adquiere las competencias necesarias para el desempeño de las funciones de nivel básico en Prevención de Riesgos Laborales."},
    {"id":"RA3","pond":18,"nombre":"Analiza sus condiciones laborales como persona trabajadora por cuenta ajena identificándolas en los principales tipos de cambios y vicisitudes relevantes que se pueden presentar en la relación laboral en la normativa laboral y especialmente en el convenio colectivo del sector."},
    {"id":"RA4","pond":28,"nombre":"Analiza y evalúa su potencial profesional y sus intereses para guiarse en el proceso de autoorientación y elabora una hoja de ruta para la inserción profesional en base al análisis de las competencias, intereses y destrezas personales."},
    {"id":"RA5","pond":23,"nombre":"Aplica las estrategias para el aprendizaje autónomo reconociendo su valor profesionalizador, diseñando y optimizando su propio entorno de aprendizaje haciendo uso de las tecnologías digitales como herramientas de aprendizaje autónomo, siendo coherente con su identidad digital y sus propios objetivos profesionales planteados en su plan de desarrollo individual."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CR10","CR11"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
]
EVAL_RAS = {1:["RA1", "RA2", "RA3"], 2:["RA4", "RA5"]}
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
        "Se han analizado las principales oportunidades de empleo y de inserción laboral en el sector profesional, identificando las posibilidades de empleo y analizado sus requerimientos actuales para el perfil profesional.",
        "Se ha comparado los diferentes requerimientos exigidos por el mercado laboral con las exigencias para el trabajo en la función pública relacionados con el sector privado.",
        "Se ha reflexionado sobre las actitudes y aptitudes requeridas actualmente para la actividad profesional relacionadas con el título, así como las competencias personales y sociales más relevantes para el sector identificando nuestra zona de desarrollo próximo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha valorado la importancia de la cultura preventiva en todos los ámbitos actividades de la empresa u organismo equiparado relacionado las condiciones laborales con la salud de la persona trabajadora identificando y clasificando los factores de riesgo en la actividad y los daños derivados de los mismos, especialmente las situaciones de riesgo más habituales en los entornos de trabajo del sector profesional relacionado con el título.",
        "Se han clasificado y descrito los tipos de daños profesionales, con especial referencia a accidentes de trabajo y enfermedades profesionales, relacionados con el perfil profesional del título.",
        "Se ha determinado la evaluación de riesgos en la empresa u organismo equiparado y definido las técnicas de prevención y de protección que deben aplicarse para evitar los daños en su origen y minimizar sus consecuencias.",
        "Se han analizado los protocolos de actuación en caso de emergencia.",
        "Se han determinado los principales derechos y deberes en materia de prevención de riesgos laborales.",
        "Se han clasificado las distintas formas de gestión de la prevención en la empresa u organismo equiparado, en función de los distintos criterios establecidos en la normativa sobre prevención de riesgos laborales y determinado las formas de representación de las personas trabajadoras en la empresa u organismo equiparado en materia de prevención de riesgos.",
        "Se ha valorado la importancia de la existencia de un plan preventivo en la empresa u organismo equiparado que incluya la secuenciación de actuaciones a realizar en caso de emergencia y reflexionado sobre el contenido del mismo.",
        "Se han determinado los requisitos y condiciones para la vigilancia de la salud de la persona trabajadora y su importancia como medida de prevención.",
        "Se han identificado las técnicas básicas de primeros auxilios que han de ser aplicadas en el lugar del accidente ante distintos tipos de daños y la composición y uso del botiquín.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han analizado los derechos y obligaciones derivados de la relación laboral, así como las condiciones de trabajo pactadas en un convenio colectivo aplicable al sector profesional relacionado con el título.",
        "Se han comparado las principales modalidades de contratación, localizando los diferentes modelos en las fuentes oficiales.",
        "Se han identificado las características definitorias de los nuevos entornos de organización del trabajo y los derechos que conlleva.",
        "Se han identificado los diferentes componentes del recibo de salario.",
        "Se han identificado los recursos laborales existentes ante las diferentes vicisitudes que se pueden dar en la relación laboral.",
        "Se ha valorado el papel de la Seguridad Social como pilar esencial para la mejora de la calidad de vida de los ciudadanos.",
        "Se han analizado las principales prestaciones derivadas de la suspensión y extinción de la relación laboral.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han evaluado los propios intereses, motivaciones, habilidades y destrezas en el marco de un proceso de autoconocimiento.",
        "Se han analizado las cualidades y competencias personales afines a la actividad profesional relacionada con el perfil del título.",
        "Se han determinado las competencias personales y sociales con valor para el empleo.",
        "Se han señalado las preferencias profesionales, intereses y metas en el marco de un proyecto profesional.",
        "Se ha valorado el concepto de autoestima en el proceso de búsqueda de empleo.",
        "Se han identificado las fortalezas, debilidades, amenazas y oportunidades propias para la inserción profesional.",
        "Se han identificado expectativas de futuro para inserción profesional analizando competencias, intereses y destrezas personales.",
        "Se han valorado hitos importantes en la trayectoria vital con valor profesionalizador.",
        "Se han identificado los itinerarios formativos profesionales relacionados con el perfil profesional.",
        "Se han formulado objetivos profesionales y se ha determinado metas personales y profesionales para la mejora de la empleabilidad y las condiciones de inserción laboral.",
        "Se ha trazado un plan de acción para desarrollar las áreas de mejora y potenciar las fortalezas personales con valor para el empleo.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha tomado conciencia de la responsabilidad individual en el desarrollo profesional valorando la actitud de aprendizaje permanente para el desarrollo de propias y nuevas competencias.",
        "Se ha identificado la empleabilidad como capacidad de adaptación al entorno laboral.",
        "Se han conocido y utilizado herramientas, fuentes de información, conexiones y actividades para la configuración de un entorno personal de aprendizaje para la empleabilidad.",
        "Se ha puesto en práctica la competencia digital para configurar un entorno personal de aprendizaje para la empleabilidad.",
        "Se ha analizado el concepto de identidad digital y su impacto en la empleabilidad.",
        "Se ha justificado el diseño de su entorno de aprendizaje basado en cómo este mejora la empleabilidad.",
        "Se ha elaborado su plan de desarrollo individual como herramienta para la mejora de la empleabilidad.",
        "Se han aplicado las herramientas de aprendizaje autónomo para su desarrollo personal y profesional.",
        "Se ha diseñado el entorno de aprendizaje que permite alcanzar el plan de desarrollo individual.",
    ], start=1)],
}

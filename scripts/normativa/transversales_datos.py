#!/usr/bin/env python3
"""Resultados de aprendizaje y criterios de evaluación de los módulos transversales.

FUENTE: Real Decreto 659/2023, de 18 de julio, por el que se desarrolla la ordenación
del Sistema de Formación Profesional (BOE núm. 174, de 22 de julio de 2023).
Texto consolidado, con las modificaciones del Real Decreto 658/2024, de 9 de julio
(BOE-A-2024-14079). Recuperado el 7 de agosto de 2026 de
https://www.boe.es/buscar/act.php?id=BOE-A-2023-16889

POR QUÉ SE COPIA DEL REAL DECRETO Y NO DEL DECRETO DE CLM:
Los Decretos 79/2024 (grado medio) y 80/2024 (grado superior) de Castilla-La Mancha
NO redactan RA ni CE propios para estos módulos: remiten expresamente al Real Decreto.

  Decreto 80/2024, artículo undécimo:
    «Los resultados de aprendizaje y criterios de evaluación de los módulos
     profesionales de Itinerario personal para la empleabilidad I y II, son los
     establecidos en el anexo V del Real Decreto 659/2023, de 18 de julio.»
    (y equivalentes para Digitalización, Sostenibilidad e Inglés profesional)

  Decreto 79/2024, artículo duodécimo: idéntico, con Digitalización en el anexo VI
  e Inglés profesional en el anexo IX.

Copiar de aquí ES cumplir el decreto de Castilla-La Mancha. Las HORAS, en cambio,
salen siempre del anexo del decreto autonómico, no de este Real Decreto (que fija
duraciones de referencia distintas: 50 h para el IPE I, 30 h para Digitalización
y Sostenibilidad, 50 h para Inglés profesional).

ERRATAS DEL BOE que se transcriben tal cual:
  - Anexo VIII, RA 4: «Propón productos y servicios responsables…» (por «Propone»).
  - Anexo IX, RA 2 a): «diccionarios técnicos. para la comprensión del texto.»
"""

FUENTE = ("Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), "
          "texto consolidado tras el Real Decreto 658/2024, de 9 de julio")

# ---------------------------------------------------------------------------
# ANEXO V · Itinerario personal para la empleabilidad I y II (grado medio y superior)
# ---------------------------------------------------------------------------

IPE_I = {
 "codigo": "1709", "nombre": "Itinerario personal para la empleabilidad I",
 "anexo": "Anexo V", "ects": 5,
 "ras": [
  ("Distingue las características del sector productivo y define los puestos de trabajo relacionándolos con las competencias profesionales expresadas en el título.", [
   "Se han analizado las principales oportunidades de empleo y de inserción laboral en el sector profesional, identificando las posibilidades de empleo y analizado sus requerimientos actuales para el perfil profesional.",
   "Se ha comparado los diferentes requerimientos exigidos por el mercado laboral con las exigencias para el trabajo en la función pública relacionados con el sector privado.",
   "Se ha reflexionado sobre las actitudes y aptitudes requeridas actualmente para la actividad profesional relacionadas con el título, así como las competencias personales y sociales más relevantes para el sector identificando nuestra zona de desarrollo próximo.",
  ]),
  ("Adquiere las competencias necesarias para el desempeño de las funciones de nivel básico en Prevención de Riesgos Laborales.", [
   "Se ha valorado la importancia de la cultura preventiva en todos los ámbitos actividades de la empresa u organismo equiparado relacionado las condiciones laborales con la salud de la persona trabajadora identificando y clasificando los factores de riesgo en la actividad y los daños derivados de los mismos, especialmente las situaciones de riesgo más habituales en los entornos de trabajo del sector profesional relacionado con el título.",
   "Se han clasificado y descrito los tipos de daños profesionales, con especial referencia a accidentes de trabajo y enfermedades profesionales, relacionados con el perfil profesional del título.",
   "Se ha determinado la evaluación de riesgos en la empresa u organismo equiparado y definido las técnicas de prevención y de protección que deben aplicarse para evitar los daños en su origen y minimizar sus consecuencias.",
   "Se han analizado los protocolos de actuación en caso de emergencia.",
   "Se han determinado los principales derechos y deberes en materia de prevención de riesgos laborales.",
   "Se han clasificado las distintas formas de gestión de la prevención en la empresa u organismo equiparado, en función de los distintos criterios establecidos en la normativa sobre prevención de riesgos laborales y determinado las formas de representación de las personas trabajadoras en la empresa u organismo equiparado en materia de prevención de riesgos.",
   "Se ha valorado la importancia de la existencia de un plan preventivo en la empresa u organismo equiparado que incluya la secuenciación de actuaciones a realizar en caso de emergencia y reflexionado sobre el contenido del mismo.",
   "Se han determinado los requisitos y condiciones para la vigilancia de la salud de la persona trabajadora y su importancia como medida de prevención.",
   "Se han identificado las técnicas básicas de primeros auxilios que han de ser aplicadas en el lugar del accidente ante distintos tipos de daños y la composición y uso del botiquín.",
  ]),
  ("Analiza sus condiciones laborales como persona trabajadora por cuenta ajena identificándolas en los principales tipos de cambios y vicisitudes relevantes que se pueden presentar en la relación laboral en la normativa laboral y especialmente en el convenio colectivo del sector.", [
   "Se han analizado los derechos y obligaciones derivados de la relación laboral, así como las condiciones de trabajo pactadas en un convenio colectivo aplicable al sector profesional relacionado con el título.",
   "Se han comparado las principales modalidades de contratación, localizando los diferentes modelos en las fuentes oficiales.",
   "Se han identificado las características definitorias de los nuevos entornos de organización del trabajo y los derechos que conlleva.",
   "Se han identificado los diferentes componentes del recibo de salario.",
   "Se han identificado los recursos laborales existentes ante las diferentes vicisitudes que se pueden dar en la relación laboral.",
   "Se ha valorado el papel de la Seguridad Social como pilar esencial para la mejora de la calidad de vida de los ciudadanos.",
   "Se han analizado las principales prestaciones derivadas de la suspensión y extinción de la relación laboral.",
  ]),
  ("Analiza y evalúa su potencial profesional y sus intereses para guiarse en el proceso de autoorientación y elabora una hoja de ruta para la inserción profesional en base al análisis de las competencias, intereses y destrezas personales.", [
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
  ]),
  ("Aplica las estrategias para el aprendizaje autónomo reconociendo su valor profesionalizador, diseñando y optimizando su propio entorno de aprendizaje haciendo uso de las tecnologías digitales como herramientas de aprendizaje autónomo, siendo coherente con su identidad digital y sus propios objetivos profesionales planteados en su plan de desarrollo individual.", [
   "Se ha tomado conciencia de la responsabilidad individual en el desarrollo profesional valorando la actitud de aprendizaje permanente para el desarrollo de propias y nuevas competencias.",
   "Se ha identificado la empleabilidad como capacidad de adaptación al entorno laboral.",
   "Se han conocido y utilizado herramientas, fuentes de información, conexiones y actividades para la configuración de un entorno personal de aprendizaje para la empleabilidad.",
   "Se ha puesto en práctica la competencia digital para configurar un entorno personal de aprendizaje para la empleabilidad.",
   "Se ha analizado el concepto de identidad digital y su impacto en la empleabilidad.",
   "Se ha justificado el diseño de su entorno de aprendizaje basado en cómo este mejora la empleabilidad.",
   "Se ha elaborado su plan de desarrollo individual como herramienta para la mejora de la empleabilidad.",
   "Se han aplicado las herramientas de aprendizaje autónomo para su desarrollo personal y profesional.",
   "Se ha diseñado el entorno de aprendizaje que permite alcanzar el plan de desarrollo individual.",
  ]),
 ],
}

IPE_II = {
 "codigo": "1710", "nombre": "Itinerario personal para la empleabilidad II",
 "anexo": "Anexo V", "ects": 5,
 "ras": [
  ("Planifica y pone en marcha estrategias en los diferentes procesos selectivos de empleo que le permiten mejorar sus posibilidades de inserción laboral.", [
   "Se han determinado las técnicas utilizadas actualmente en el sector para el proceso de selección de personal.",
   "Se han desarrollado estrategias para la búsqueda de empleo relacionadas con las técnicas actuales más utilizadas contextualizadas al sector.",
   "Se han valorado las actitudes y aptitudes que permiten superar procesos selectivos en el sector privado y en el sector público.",
   "Se ha construido una marca personal identificando las necesidades del mercado actual, sus habilidades, destrezas y su aporte de valor.",
  ]),
  ("Aplica estrategias relacionadas con las competencias personales, sociales y emocionales para el empleo en búsqueda de la mejora de su empleabilidad.", [
   "Se ha valorado la importancia de las competencias personales y sociales en la empleabilidad en el sector de referencia.",
   "Se ha participado activamente en el establecimiento de los objetivos del equipo y en la toma de decisiones del mismo y asumido la responsabilidad de las acciones y decisiones del grupo, participando activamente en el logro de unos objetivos compartidos cooperando con otras personas y compartiendo el liderazgo.",
   "Se han incorporado al propio proceso de aprendizaje las técnicas y recursos de presentación y comunicación, tanto orales como escritos, adecuados para una comunicación efectiva y afectiva siendo capaz de adaptarlos a cada situación y circunstancias, valorando las oportunidades y dificultades que ofrece cada una de ellas.",
   "Se han aplicado técnicas y estrategias para la gestión del tiempo disponible para alcanzar los objetivos tanto individuales como del equipo y programado las actividades necesarias.",
   "Se han aplicado estrategias para canalizar las emociones mostrando una actitud flexible en las relaciones con otras personas.",
   "Se han desarrollado estrategias para la programación de actividades atendiendo a criterios de organización eficiente y previendo las posibles dificultades.",
   "Se ha reaccionado de forma flexible y positiva ante conflictos y situaciones nuevas, aprovechando las oportunidades y gestionando las dificultades haciendo uso de estrategias relacionadas con la inteligencia emocional.",
  ]),
  ("Pone en práctica las habilidades emprendedoras necesarias para el desarrollo de procesos de innovación e investigación aplicadas que promuevan la modernización del sector productivo hacia un modelo sostenible.", [
   "Se ha identificado el concepto de innovación y su relación con la construcción de una sociedad más sostenible que mejore en el bienestar de los individuos.",
   "Se han analizado las distintas metodologías para emprender y su importancia para favorecer la innovación y como fuente de creación de empleo y bienestar social.",
   "Se han aplicado las habilidades emprendedoras necesarias para promover el emprendimiento y el intraemprendimiento.",
   "Se ha puesto en práctica el trabajo colaborativo como requisito para el desarrollo de procesos de innovación.",
   "Se ha desarrollado la competencia digital necesaria para la mejora de los procesos de innovación e investigación aplicadas que promuevan la modernización del sector productivo.",
   "Se han incorporado los objetivos de las políticas e iniciativas relacionadas con la sostenibilidad y el medio ambiente a la estrategia empresarial enfocada al desarrollo de un modelo económico y social sostenible.",
  ]),
  ("Identifica, define y valida ideas de emprendimiento generadoras de nuevas oportunidades a partir de estrategias de análisis del entorno socio productivo utilizando metodologías ágiles para el emprendimiento.", [
   "Se han identificado los problemas de las personas destinatarias potenciales del proyecto emprendedor como paso previo a la propuesta de soluciones que se conviertan en oportunidades.",
   "Se ha puesto en práctica el proceso creativo con el fin de conseguir una idea emprendedora que aporte valor económico, social y/o cultural.",
   "Se ha diseñado un modelo de negocio y/o gestión derivado de la idea emprendedora.",
   "Se han incorporado valores éticos y sociales a la idea emprendedora analizando modelos de balance social.",
   "Se ha analizado la contribución de la Economía Circular y la Economía del Bien Común al desarrollo de un modelo económico y social basado en la equidad, la justicia social y la sostenibilidad.",
   "Se han analizado los principales componentes del entorno general y específico, y su impacto en la idea emprendedora.",
   "Se han realizado entrevistas de problema para validar el perfil y el problema de las personas destinatarias de la idea emprendedora.",
   "Se ha validado la solución mediante la creación de prototipos buscando el encaje problema-solución.",
   "Se ha experimentado con la puesta en práctica de estrategias de marketing para desarrollar destrezas en técnicas de comunicación y venta.",
  ]),
  ("Desarrolla un proyecto emprendedor de innovación social y/o tecnológica aplicada en colaboración con el entorno.", [
   "Se han analizado los conceptos básicos del emprendimiento y la innovación social.",
   "Se ha reflexionado sobre la necesidad del liderazgo ético y sostenible en las organizaciones.",
   "Se ha reflexionado sobre la tecnología como base para el cambio del modelo productivo.",
   "Se han puesto en marcha las estrategias propias del pensamiento de diseño para detectar necesidades sociales y medioambientales.",
   "Se han analizado los elementos del diseño de modelos de negocio ecosociales y/o de base tecnológica.",
   "Se han alineado metas de desarrollo sostenible con el diseño de modelos de negocio ecosociales y/o de base tecnológica.",
   "Se han aplicado las estrategias necesarias para analizar la viabilidad del proyecto emprendedor.",
   "Se han investigado las opciones financieras socialmente responsables.",
   "Se han definido los agentes implicados en el proyecto, así como su participación en el mismo.",
  ]),
 ],
}

# ---------------------------------------------------------------------------
# ANEXO VIII · Sostenibilidad aplicada al sistema productivo (medio y superior)
# ---------------------------------------------------------------------------

SOSTENIBILIDAD = {
 "codigo": "1708", "nombre": "Sostenibilidad aplicada al sistema productivo",
 "anexo": "Anexo VIII", "ects": 3,
 "ras": [
  ("Identifica los aspectos ambientales, sociales y de gobernanza (ASG) relativos a la sostenibilidad teniendo en cuenta el concepto de desarrollo sostenible y los marcos internacionales que contribuyen a su consecución.", [
   "Se ha descrito el concepto de sostenibilidad, estableciendo los marcos internacionales asociados al desarrollo sostenible.",
   "Se han identificado los asuntos ambientales, sociales y de gobernanza que influyen en el desarrollo sostenible de las organizaciones empresariales.",
   "Se han relacionado los Objetivos de Desarrollo Sostenible (ODS) con su importancia para la consecución de la Agenda 2030.",
   "Se ha analizado la importancia de identificar los aspectos ASG más relevantes para los grupos de interés de las organizaciones relacionándolos con los riesgos y oportunidades que suponen para la propia organización.",
   "Se han identificado los principales estándares de métricas para la evaluación del desempeño en sostenibilidad y su papel en la rendición de cuentas que marca la legislación vigente y las futuras regulaciones en desarrollo.",
   "Se ha descrito la inversión socialmente responsable y el papel de los analistas, inversores, agencias e índices de sostenibilidad en el fomento de la sostenibilidad.",
  ]),
  ("Caracteriza los retos ambientales y sociales a los que se enfrenta la sociedad, describiendo los impactos sobre las personas y los sectores productivos y proponiendo acciones para minimizarlos.", [
   "Se han identificado los principales retos ambientales y sociales.",
   "Se han relacionado los retos ambientales y sociales con el desarrollo de la actividad económica.",
   "Se ha analizado el efecto de los impactos ambientales y sociales sobre las personas y los sectores productivos.",
   "Se han identificado las medidas y acciones encaminadas a minimizar los impactos ambientales y sociales.",
   "Se ha analizado la importancia de establecer alianzas y trabajar de manera transversal y coordinada para abordar con éxito los retos ambientales y sociales.",
  ]),
  ("Establece la aplicación de criterios de sostenibilidad en el desempeño profesional y personal, identificando los elementos necesarios.", [
   "Se han identificado los ODS más relevantes para la actividad profesional que realiza.",
   "Se han analizado los riesgos y oportunidades que representan los ODS.",
   "Se han identificado las acciones necesarias para atender algunos de los retos ambientales y sociales desde la actividad profesional y el entorno personal.",
  ]),
  ("Propón productos y servicios responsables teniendo en cuenta los principios de la economía circular.", [
   "Se ha caracterizado el modelo de producción y consumo actual.",
   "Se han identificado los principios de la economía verde y circular.",
   "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción.",
   "Se han aplicado principios de ecodiseño.",
   "Se ha analizado el ciclo de vida del producto.",
   "Se han identificado los procesos de producción y los criterios de sostenibilidad aplicados.",
  ]),
  ("Realiza actividades sostenibles minimizando el impacto de las mismas en el medio ambiente.", [
   "Se ha caracterizado el modelo de producción y consumo actual.",
   "Se han identificado los principios de la economía verde y circular.",
   "Se han contrastado los beneficios de la economía verde y circular frente al modelo clásico de producción.",
   "Se ha evaluado el impacto de las actividades personales y profesionales.",
   "Se han aplicado principios de ecodiseño.",
   "Se han aplicado estrategias sostenibles.",
   "Se ha analizado el ciclo de vida del producto.",
   "Se han identificado los procesos de producción y los criterios de sostenibilidad aplicados.",
   "Se ha aplicado la normativa ambiental.",
  ]),
  ("Analiza un plan de sostenibilidad de una empresa del sector, identificando sus grupos de interés, los aspectos ASG materiales y justificando acciones para su gestión y medición.", [
   "Se han identificado los principales grupos de interés de la empresa.",
   "Se han analizado los aspectos ASG materiales, las expectativas de los grupos de interés y la importancia de los aspectos ASG en relación con los objetivos empresariales.",
   "Se han definido acciones encaminadas a minimizar los impactos negativos y aprovechar las oportunidades que plantean los principales aspectos ASG identificados.",
   "Se han determinado las métricas de evaluación del desempeño de la empresa de acuerdo con los estándares de sostenibilidad más ampliamente utilizados.",
   "Se ha elaborado un informe de sostenibilidad con el plan y los indicadores propuestos.",
  ]),
 ],
}

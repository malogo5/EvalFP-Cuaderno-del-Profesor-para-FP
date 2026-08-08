#!/usr/bin/env python3
"""Segunda parte de los transversales: Digitalización e Inglés profesional.

Misma fuente y mismas advertencias que transversales_datos.py:
Real Decreto 659/2023, de 18 de julio (BOE núm. 174, de 22/07/2023), texto
consolidado tras el Real Decreto 658/2024, de 9 de julio.

Ojo: Digitalización e Inglés profesional tienen currículo DISTINTO en grado medio
y en grado superior. No son intercambiables.
  - Digitalización: anexo VI (grado medio, 1664) y anexo VII (grado superior, 1665)
  - Inglés profesional: anexo IX (grado medio, 0156) y anexo X (grado superior, 0179)
"""

# ---------------------------------------------------------------------------
# ANEXO VI · Digitalización aplicada a los sectores productivos (GRADO MEDIO)
# ---------------------------------------------------------------------------

DIGITALIZACION_GM = {
 "codigo": "1664", "nombre": "Digitalización aplicada a los sectores productivos (GM)",
 "anexo": "Anexo VI", "ects": None,
 "ras": [
  ("Establece las diferencias entre la Economía Lineal (EL) y la Economía Circular (EC), identificando las ventajas de la EC en relación con el medioambiente y el desarrollo sostenible.", [
   "Se han identificado las etapas «típicas» de los modelos basados en EL y modelos basados en EC.",
   "Se ha analizado cada etapa de los modelos EL y EC y su repercusión en el medio ambiente.",
   "Se ha valorado la importancia del reciclaje en los modelos económicos.",
   "Se han identificado procesos reales basados en EL.",
   "Se han identificado procesos reales basados en EC.",
   "Se han comparado los modelos anteriores en relación con su impacto medioambiental y los ODS (Objetivos de Desarrollo Sostenible).",
  ]),
  ("Caracteriza los principales aspectos de la 4.ª Revolución Industrial indicando los cambios y las ventajas que se producen tanto desde el punto de vista de los clientes como de las empresas.", [
   "Se han relacionado los sistemas ciber físicos con la evolución industrial.",
   "Se ha analizado el cambio producido en los sistemas automatizados.",
   "Se ha descrito la combinación de la parte física de las industrias con el software, IoT (Internet de las cosas), comunicaciones, entre otros.",
   "Se ha descrito la interrelación entre el mundo físico y el virtual.",
   "Se ha relacionado la migración a entornos 4.0 con la mejora de los resultados de las empresas.",
   "Se han identificado las ventajas para clientes y empresas.",
  ]),
  ("Identifica la estructura de los sistemas basados en cloud/nube describiendo su tipología y campo de aplicación.", [
   "Se han identificado los diferentes niveles de la cloud/nube.",
   "Se han identificado las principales funciones de la cloud/nube (procesamiento de datos, intercambio de información, ejecución de aplicaciones, entre otros).",
   "Se ha descrito el concepto de edge computing y su relación con la cloud/nube.",
   "Se han definido los conceptos de fog y mist y sus zonas de aplicación en el conjunto.",
   "Se han identificado las ventajas que proporciona la utilización de la cloud/nube en los sistemas conectados.",
  ]),
  ("Compara los sistemas de producción/prestación de servicios digitalizados con los sistemas clásicos identificando las mejoras introducidas.", [
   "Se han identificado las tecnologías habilitadoras (THD) actuales que definen un sistema digitalizado.",
   "Se han descrito las características y aplicaciones del IoT, IA (Inteligencia Artificial), Big Data, tecnología 5G, la robótica colaborativa, Blockchain, Ciberseguridad, fabricación aditiva, realidad virtual, gemelos digitales, entre otras.",
   "Se ha descrito la contribución de las THD a la mejora de la productividad y la eficiencia de los sistemas productivos o de prestación de servicios.",
   "Se ha relacionado la alineación entre las unidades funcionales de las empresas que conforman el sistema y el objetivo del mismo.",
   "Se ha relacionado la implantación de las tecnologías habilitadoras (sensórica, tratamiento de datos, automatización y comunicaciones, entre otras) con la reducción de costes y la mejora de la competitividad.",
   "Se han relacionado las tecnologías disruptivas con aplicaciones concretas en los sectores productivos.",
   "Se han definido los sistemas de almacenamiento de datos no convencionales y el acceso a los mismos desde cada unidad.",
   "Se han descrito las mejoras producidas en el sistema y en cada una de sus etapas.",
  ]),
  ("Elabora un plan de transformación de una empresa clásica del sector en el que se enmarca el título, basada en una EL, al concepto 4.0, determinando los cambios a introducir en las principales fases del sistema e indicando como afectaría a los recursos humanos.", [
   "Se ha definido a nivel de bloques el diagrama de funcionamiento de la empresa clásica.",
   "Se han identificado las etapas susceptibles de ser digitalizadas.",
   "Se han definido las tecnologías implicadas en cada una de las etapas.",
   "Se ha establecido la conexión de las etapas digitalizadas con el resto del sistema.",
   "Se ha elaborado un diagrama de bloques del sistema digitalizado.",
   "Se ha elaborado un informe de viabilidad y de las mejoras introducidas.",
   "Se ha analizado la mejora en la producción y gestión de residuos, entre otras.",
   "Se ha elaborado un documento con la secuencia del plan de transformación y los recursos empleados.",
  ]),
 ],
}

# ---------------------------------------------------------------------------
# ANEXO VII · Digitalización aplicada a los sectores productivos (GRADO SUPERIOR)
# ---------------------------------------------------------------------------

DIGITALIZACION_GS = {
 "codigo": "1665", "nombre": "Digitalización aplicada a los sectores productivos (GS)",
 "anexo": "Anexo VII", "ects": 3,
 "ras": [
  ("Analiza el concepto de digitalización y su repercusión en los sectores productivos teniendo en cuenta la actividad de la empresa e identificando entornos IT (Information Technology: tecnología de la información) y OT (Operation Technology: tecnología de operación) característicos.", [
   "Se ha descrito en qué consiste el concepto de digitalización.",
   "Se ha relacionado la implantación de la tecnología digital con la organización de las empresas.",
   "Se han establecido las diferencias y similitudes entre los entornos IT y OT.",
   "Se han identificado los departamentos típicos de las empresas que pueden constituir entornos IT.",
   "Se han seleccionado las tecnologías típicas de la digitalización en planta y en negocio.",
   "Se ha analizado la importancia de la conexión entre entornos IT y OT.",
   "Se han analizado las ventajas de digitalizar una empresa industrial de extremo a extremo.",
  ]),
  ("Caracteriza las tecnologías habilitadoras digitales necesarias para la adecuación/transformación de las empresas a entornos digitales describiendo sus características y aplicaciones.", [
   "Se han identificado las principales tecnologías habilitadoras digitales.",
   "Se han relacionado las THD con el desarrollo de productos y servicios.",
   "Se ha relacionado la importancia de las THD con la economía sostenible y eficiente.",
   "Se han identificado nuevos mercados generados por las THD.",
   "Se ha analizado la implicación de THD tanto en la parte de negocio como en la parte de planta.",
   "Se han identificado las mejoras producidas debido a la implantación de las tecnologías habilitadoras en relación con los entornos IT y OT.",
   "Se ha elaborado un informe que relacione, las tecnologías con sus características y áreas de aplicación.",
  ]),
  ("Identifica sistemas basados en cloud/nube y su influencia en el desarrollo de los sistemas digitales.", [
   "Se han identificado los diferentes niveles de la cloud/nube.",
   "Se han identificado las principales funciones de la cloud/nube (procesamiento de datos, intercambio de información, ejecución de aplicaciones, entre otros).",
   "Se ha descrito el concepto de edge computing y su relación con la cloud/nube.",
   "Se han definido los conceptos de fog y mist y sus zonas de aplicación en el conjunto.",
   "Se han identificado las ventajas que proporciona la utilización de la cloud/nube en los sistemas conectados.",
  ]),
  ("Identifica aplicaciones de la IA (inteligencia artificial) en entornos del sector donde está enmarcado el título describiendo las mejoras implícitas en su implementación.", [
   "Se ha identificado la importancia de la IA en la automatización de procesos y su optimización.",
   "Se ha relacionado la IA con la recogida masiva de datos (Big Data) y su tratamiento (análisis) con la rentabilidad de las empresas.",
   "Se ha valorado la importancia presente y futura de la IA.",
   "Se han identificado los sectores con implantación más relevante de IA.",
   "Se han identificado los lenguajes de programación en IA.",
   "Se ha descrito como influye la IA en el sector del título.",
  ]),
  ("Evalúa la importancia de los datos, así como su protección en una economía digital globalizada, definiendo sistemas de seguridad y ciberseguridad tanto a nivel de equipo/sistema, como globales.", [
   "Se ha establecido la diferencia entre dato e información.",
   "Se ha descrito el ciclo de vida del dato.",
   "Se ha identificado la relación entre Big Data, análisis de datos, machine/ deep learning e inteligencia artificial.",
   "Se han descrito las características que definen Big Data.",
   "Se han descrito las etapas típicas de la ciencia de datos y su relación en el proceso.",
   "Se han descrito los procedimientos de almacenaje de datos en la cloud/nube.",
   "Se ha descrito la importancia del cloud computing.",
   "Se han identificado los principales objetivos de la ciencia de datos en las diferentes empresas.",
   "Se ha valorado la importancia de la seguridad y su regulación en relación con los datos.",
  ]),
  ("Desarrolla un proyecto de transformación digital de una empresa de un sector relacionado con el título, teniendo en cuenta los cambios que se deben producir en función de los objetivos de la empresa.", [
   "Se han identificado los objetivos estratégicos de la empresa.",
   "Se han identificado y alineado las áreas de producción/negocio y de comunicaciones.",
   "Se han identificado las áreas susceptibles de ser digitalizadas.",
   "Se ha analizado el encaje de AD (áreas digitalizadas) entre sí y con las que no lo están.",
   "Se han tenido en cuenta las necesidades presentes y futuras de la empresa.",
   "Se han relacionado cada una de las áreas con la implantación de las tecnologías.",
   "Se han analizado las posibles brechas de seguridad en cada una de las áreas.",
   "Se ha definido el tratamiento de los datos y su análisis.",
   "Se ha tenido en cuenta la integración entre datos, aplicaciones, plataformas que los soportan, entre otros.",
   "Se han documentado los cambios realizados en función de la estrategia.",
   "Se han tenido en cuenta la idoneidad de los recursos humanos.",
  ]),
 ],
}

# ---------------------------------------------------------------------------
# ANEXO IX · Inglés profesional (GRADO MEDIO)
# ---------------------------------------------------------------------------

INGLES_GM = {
 "codigo": "0156", "nombre": "Inglés profesional (GM)",
 "anexo": "Anexo IX", "ects": None,
 "ras": [
  ("Comprende información, de índole profesional y cotidiana, contenida en discursos orales sencillos, emitidos en lengua estándar, descifrando el contenido global del mensaje, y relacionándolo con los recursos lingüísticos correspondientes.", [
   "Se ha situado el mensaje en su contexto por medio del análisis de sus características textuales y contextuales.",
   "Se ha identificado el hilo argumental de mensajes orales y determinado los roles que aparecen en los mismos.",
   "Se ha reconocido la finalidad del mensaje, ya se trate de un mensaje directo, telefónico o en cualquier otro medio auditivo.",
   "Se ha extraído información específica contenida en discursos orales, en lengua estándar, relacionados con la vida social, profesional o académica.",
   "Se han secuenciado los elementos constituyentes del mensaje.",
   "Se han identificado y resumido con claridad las ideas principales de un discurso sobre temas conocidos, transmitido por los medios de comunicación y emitido en lengua estándar.",
   "Se han reconocido las instrucciones orales y se han seguido las indicaciones siendo capaz de concluir si precisan de una respuesta verbal o de una no verbal.",
   "Se ha tomado conciencia de la importancia de comprender globalmente un mensaje, sin necesidad de entender todos y cada uno de los elementos del mismo.",
   "Se ha servido del análisis de la entonación y de los elementos visuales para identificar los diversos significados e intenciones comunicativas del emisor.",
  ]),
  ("Comprende información profesional contenida en textos escritos sencillos, analizando de forma comprensiva su contenido.", [
   "Se han seleccionado los materiales de consulta y diccionarios técnicos. para la comprensión del texto.",
   "Se han leído de forma comprensiva textos claros en lengua estándar.",
   "Se ha relacionado el texto con el ámbito del sector a que se refiere.",
   "Se han reconocido las ideas principales de un texto escrito identificando la información relevante, sin necesidad de entender todos y cada uno de los elementos de dicho texto.",
   "Se ha identificado la terminología utilizada, así como las estructuras gramaticales y demás elementos característicos de cada tipología discursiva.",
   "Se han realizado traducciones de textos en lengua estándar utilizando material de apoyo en caso necesario.",
   "Se ha interpretado el mensaje recibido a través de soportes telemáticos o cualquier otro tipo de soporte.",
   "Se ha reconocido la finalidad de distintos textos escritos en cualquier soporte, en lengua estándar y relacionados con la actividad profesional.",
   "Se ha extraído información específica de textos de diferente naturaleza, relativos a su profesión y contenidos en distintos soportes.",
  ]),
  ("Produce mensajes orales sencillos, claros y estructurados, participando como agente activo en conversaciones profesionales.", [
   "Se han determinado los registros más adecuados para la emisión del mensaje.",
   "Se ha comunicado utilizando fórmulas, nexos de unión, marcadores discursivos y estrategias de interacción acordes a la situación de comunicación.",
   "Se han descrito hechos breves e imprevistos relacionados con su profesión.",
   "Se ha utilizado correctamente la terminología de la profesión.",
   "Se han expresado sentimientos, ideas u opiniones.",
   "Se han enumerado las actividades propias de la tarea profesional.",
   "Se ha descrito y secuenciado un proceso de trabajo de su competencia.",
   "Se ha justificado la aceptación o no de propuestas realizadas haciendo uso de normas de cortesía y de modales apropiados.",
   "Se ha intercambiado, con relativa fluidez, información específica y detallada utilizando frases de estructura sencilla y diferentes soportes telemáticos.",
   "Se han realizado, de manera clara, presentaciones breves y preparadas sobre un tema dentro de su especialidad, haciendo uso de los protocolos adecuados.",
   "Se ha comunicado espontáneamente adoptando un nivel de formalidad adecuado a las circunstancias.",
   "Se han respondido preguntas relativas a su vida socio-profesional, incluidas las propias de una entrevista de trabajo.",
   "Se ha solicitado la reformulación del discurso o la aclaración de parte del mismo cuando se ha considerado necesario para una mejor comprensión.",
  ]),
  ("Redacta textos sencillos en lengua estándar, relacionando las reglas gramaticales con la finalidad de los mismos.", [
   "Se han seleccionado las estrategias, estructuras, vocabulario y convenciones más adecuadas para el tipo de texto que se va a crear (fax, nota, carta o correo electrónico, entre otros).",
   "Se han redactado textos breves relacionados con aspectos cotidianos y/o profesionales.",
   "Se ha organizado la información de manera coherente y cohesionada.",
   "Se han realizado resúmenes de textos relacionados con su entorno profesional, identificando las ideas principales de los mismos.",
   "Se ha cumplimentado documentación específica de su campo profesional, aplicando las fórmulas establecidas y el vocabulario específico.",
   "Se ha cumplimentado un texto dado con apoyos visuales y claves lingüísticas aportadas.",
   "Se han utilizado las fórmulas de cortesía propias del documento que se va a elaborar.",
   "Se ha escrito correspondencia formal básica en formato físico o digital destinada principalmente a pedir información, solicitar un servicio o llevar a cabo una reclamación u otra gestión sencilla, siempre atendiendo a las convenciones de la tipología textual.",
   "Se han tomado notas, y mensajes, con información sencilla sobre aspectos propios de su labor profesional.",
   "Se ha solicitado, de forma escrita, información referente a aspectos relacionados con su campo profesional (página web y correo electrónico, entre otros).",
  ]),
  ("Aplica actitudes y comportamientos profesionales en situaciones de comunicación, describiendo las relaciones típicas características del país de la lengua extranjera.", [
   "Se han definido los rasgos más significativos de las costumbres y usos de la comunidad donde se habla la lengua extranjera.",
   "Se han descrito los protocolos y normas de relación social propios del país.",
   "Se han identificado los valores y creencias propios de la comunidad donde se habla la lengua extranjera.",
   "Se han identificado los aspectos socio-profesionales propios del sector, en cualquier tipo de texto.",
   "Se han aplicado los protocolos y normas de relación social propios del país de la lengua extranjera.",
  ]),
 ],
}

# ---------------------------------------------------------------------------
# ANEXO X · Inglés profesional (GRADO SUPERIOR)
# ---------------------------------------------------------------------------

INGLES_GS = {
 "codigo": "0179", "nombre": "Inglés profesional (GS)",
 "anexo": "Anexo X", "ects": 5,
 "ras": [
  ("Comprende información, de índole profesional, académica y cotidiana, contenida en todo tipo de discursos orales, emitidos por cualquier medio de comunicación en lengua estándar, interpretando con precisión el contenido del mensaje.", [
   "Se ha identificado la idea principal de mensajes en lengua estándar relacionados con la vida social, profesional o académica.",
   "Se ha reconocido la finalidad de mensajes directos o emitidos en cualquier soporte en lengua estándar.",
   "Se ha extraído información específica contenida en distintos discursos orales en lengua estándar, relacionada con la vida social, profesional o académica.",
   "Se ha identificado el punto de vista y la actitud del hablante.",
   "Se ha identificado el hilo argumental de mensajes orales y determinado los roles que aparecen en dichos mensajes.",
   "Se han comprendido adecuadamente mensajes en lengua estándar en ambientes con contaminación acústica.",
   "Se han extraído las ideas principales de conferencias, charlas e informes, y otras formas de presentación académica y profesional, lingüísticamente complejas.",
   "Se ha tomado conciencia de la importancia de comprender globalmente un mensaje sin entender todos y cada uno de los elementos del mismo.",
  ]),
  ("Comprende mensajes escritos, de naturaleza profesional, académica y cotidiana, de relativa dificultad, analizando de forma comprensiva su contenido.", [
   "Se ha identificado la idea principal de textos específicos de su ámbito social, profesional o académico.",
   "Se ha reconocido la finalidad de distintos textos escritos en cualquier soporte, en lengua estándar y relacionados con la actividad profesional.",
   "Se ha extraído información específica de textos, de diferente naturaleza, relativos a su profesión, y contenidos en distintos soportes.",
   "Se ha tomado conciencia de la importancia de comprender globalmente un texto sin entender todos y cada uno de los elementos del mismo.",
   "Se han leído y comprendido, de manera autónoma, textos relacionados con el sector con la velocidad y estilo de lectura propia del nivel competencial.",
   "Se ha interpretado la correspondencia relativa a su especialidad, captando fácilmente el significado esencial.",
   "Se han interpretado textos extensos, y de cierta complejidad, relacionados o no con su especialidad, pudiendo realizar varias lecturas del mismo.",
   "Se ha identificado con rapidez el contenido y la importancia de noticias, artículos e informes sobre una amplia serie de temas profesionales.",
   "Se han interpretado instrucciones, con distintos niveles de dificultad, y mensajes técnicos recibidos a través de soportes digitales.",
   "Se han traducido textos de cierta complejidad, utilizando material de apoyo en caso necesario.",
  ]),
  ("Produce mensajes orales claros y bien estructurados, analizando el contenido de la situación y adaptándose al registro lingüístico del interlocutor.", [
   "Se han emitido mensajes generales propios de sector y de la vida cotidiana, utilizando nexos y estrategias de interacción.",
   "Se ha intercambiado con fluidez información específica y detallada utilizando estructuras de una complejidad acorde al nivel competencial.",
   "Se han seleccionado y aplicado los registros adecuados para la emisión del mensaje, así como protocolos y normas de relación social propios del país.",
   "Se han realizado presentaciones, bien estructuradas, sobre temas de su ámbito profesional, haciendo uso de los protocolos establecidos.",
   "Se ha utilizado correctamente la terminología de la profesión.",
   "Se ha descrito y secuenciado oralmente un proceso de trabajo de su competencia.",
   "Se ha solicitado la reformulación del discurso o parte del mismo cuando se ha considerado necesario.",
   "Se ha interaccionado espontáneamente, adoptando un nivel de formalidad adecuado a las circunstancias.",
   "Se ha expresado con fluidez, precisión y eficacia sobre una amplia serie de temas generales, académicos, profesionales o de ocio, marcando con claridad la relación entre las ideas.",
   "Se han expresado y defendido puntos de vista con claridad, proporcionando explicaciones y argumentos adecuados.",
   "Se ha respondido a preguntas relativas a su vida socio-profesional, incluidas las propias de una entrevista de trabajo.",
  ]),
  ("Redacta documentos e informes, propios del sector o de la vida académica y cotidiana, relacionando los recursos lingüísticos con el propósito de los mismos.", [
   "Se han escrito textos claros y detallados sobre una variedad de temas relacionados con su profesión, sintetizando y evaluando información y argumentos procedentes de varias fuentes.",
   "Se ha cumplimentado documentación específica de su campo profesional, utilizando vocabulario específico y protocolos y normas de relación social propios del país.",
   "Se ha organizado la información con corrección, precisión, con cohesión y coherencia, solicitando y/o facilitando información de tipo general o detallada.",
   "Se han cumplimentado textos mediante apoyos visuales y claves lingüísticas.",
   "Se han elaborado informes, destacando los aspectos significativos y ofreciendo detalles relevantes que sirvan de apoyo.",
   "Se han escrito cartas, formales e informales, empleando las fórmulas de cortesía establecidas y el vocabulario específico para la elaboración de las mismas.",
   "Se han resumido diferentes tipos de documentos escritos, utilizando sus propios recursos lingüísticos.",
   "Se han utilizado las fórmulas de cortesía propias del documento que se va a elaborar.",
  ]),
  ("Aplica actitudes y comportamientos profesionales en situaciones de comunicación, describiendo las relaciones típicas características del país de la lengua extranjera.", [
   "Se han definido los rasgos más significativos de las costumbres y usos de la comunidad donde se habla la lengua extranjera.",
   "Se han descrito los protocolos y normas de relación social propios del país.",
   "Se han identificado los valores y creencias propios de la comunidad donde se habla la lengua extranjera.",
   "Se ha identificado los aspectos socio-profesionales propios del sector, en cualquier tipo de texto.",
   "Se han aplicado los protocolos y normas de relación social propios del país de la lengua extranjera.",
   "Se han reconocido los marcadores lingüísticos de la procedencia regional.",
  ]),
 ],
}

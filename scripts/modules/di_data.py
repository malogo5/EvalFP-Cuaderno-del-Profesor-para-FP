"""EvalFP — Desarrollo de Interfaces · 0488 · Desarrollo de Aplicaciones Multiplataforma (DAM)
Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 233 h · 6 h/semana · 2º DAM.
"""
MODULO = {
    "nombre":"Desarrollo de Interfaces","codigo":"0488","abrev":"DI",
    "ciclo":"Desarrollo de Aplicaciones Multiplataforma (DAM)","ciclo_clave":"DAM","ciclo_nivel":"CFGS",
    "curso":"2º DAM","horas_sem":6,"total_horas":233,"anno":"2026-2027","eval_count":3,
    "decreto":"Horas y curso: Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo IA-3. 6º · RA y CE: Decreto 252/2011, de 12/08/2011 (DOCM núm. 164, de 22/08/2011), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"Genera interfaces gráficos de usuario mediante editores visuales","horas":29,"eval":1,"tags":""},
    {"id":"UT2","nombre":"Genera interfaces gráficos de usuario basados en XML","horas":29,"eval":1,"tags":""},
    {"id":"UT3","nombre":"Crea componentes visuales","horas":32,"eval":1,"tags":""},
    {"id":"UT4","nombre":"Diseña interfaces gráficos","horas":32,"eval":2,"tags":""},
    {"id":"UT5","nombre":"Crea informes","horas":29,"eval":2,"tags":""},
    {"id":"UT6","nombre":"Documenta aplicaciones","horas":25,"eval":3,"tags":""},
    {"id":"UT7","nombre":"Prepara aplicaciones para su distribución","horas":29,"eval":3,"tags":""},
    {"id":"UT8","nombre":"Evalúa el funcionamiento de aplicaciones diseñando y ejecutando pruebas","horas":28,"eval":3,"tags":""},
]
RAS = [
    {"id":"RA1","pond":13,"nombre":"Genera interfaces gráficos de usuario mediante editores visuales utilizando las funcionalidades del editor y adaptando el código generado."},
    {"id":"RA2","pond":12,"nombre":"Genera interfaces gráficos de usuario basados en XML utilizando herramientas específicas y adaptando el documento XML generado."},
    {"id":"RA3","pond":14,"nombre":"Crea componentes visuales valorando y empleando herramientas específicas."},
    {"id":"RA4","pond":14,"nombre":"Diseña interfaces gráficos identificando y aplicando criterios de usabilidad."},
    {"id":"RA5","pond":12,"nombre":"Crea informes evaluando y utilizando herramientas gráficas."},
    {"id":"RA6","pond":11,"nombre":"Documenta aplicaciones seleccionando y utilizando herramientas específicas."},
    {"id":"RA7","pond":12,"nombre":"Prepara aplicaciones para su distribución evaluando y utilizando herramientas específicas."},
    {"id":"RA8","pond":12,"nombre":"Evalúa el funcionamiento de aplicaciones diseñando y ejecutando pruebas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT6","RA6",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT7","RA7",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
    ("UT8","RA8",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2","RA3"], 2:["RA4","RA5"], 3:["RA6","RA7","RA8"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["examen","practica"],
    "RA3":["examen","practica"],
    "RA4":["examen","practica"],
    "RA5":["examen","practica"],
    "RA6":["examen","practica"],
    "RA7":["examen","practica"],
    "RA8":["examen","practica"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha creado un interfaz gráfico utilizando los asistentes de un editor visual.",
        "Se han utilizado las funciones del editor para ubicar los componentes del interfaz.",
        "Se han modificado las propiedades de los componentes para adecuarlas a las necesidades de la aplicación.",
        "Se ha analizado el código generado por el editor visual.",
        "Se ha modificado el código generado por el editor visual.",
        "Se han enlazado componentes a orígenes de datos.",
        "Se han asociado a los eventos las acciones correspondientes.",
        "Se ha desarrollado una aplicación que incluye el interfaz gráfico obtenido.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las ventajas de generar interfaces de usuario a partir de su descripción en XML.",
        "Se ha generado la descripción del interfaz en XML usando un editor gráfico.",
        "Se ha analizado el documento XML generado.",
        "Se ha modificado el documento XML.",
        "Se han asignado acciones a los eventos.",
        "Se ha depurado el documento XML.",
        "Se ha generado el código correspondiente al interfaz a partir del documento XML.",
        "Se ha programado una aplicación que incluye el interfaz generado.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las herramientas para diseño y prueba de componentes.",
        "Se han creado componentes visuales.",
        "Se han definido sus propiedades y asignado valores por defecto.",
        "Se han modificado las propiedades de los componentes.",
        "Se han determinado los eventos a los que debe responder el componente y se les han asociado las acciones correspondientes.",
        "Se han realizado pruebas unitarias sobre los componentes desarrollados.",
        "Se han documentado los componentes creados.",
        "Se han empaquetado componentes.",
        "Se han programado aplicaciones cuyo interfaz gráfico utiliza los componentes creados.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han reconocido las normas ISO para la usabilidad.",
        "Se han creado menús que se ajustan a los estándares.",
        "Se han creado menús contextuales cuya estructura y contenido siguen los estándares establecidos.",
        "Se han distribuido las acciones en menús, barras de herramientas, botones de comando, entre otros, siguiendo un criterio coherente.",
        "Se han distribuido adecuadamente los controles en la interfaz de usuario.",
        "Se ha utilizado el tipo de control más apropiado en cada caso",
        "Se ha diseñado el aspecto de la interfaz de usuario (colores y fuentes entre otros) atendiendo a su legibilidad.",
        "Se ha verificado que los mensajes generados por la aplicación son adecuados en extensión y claridad.",
        "Se han realizado pruebas para evaluar la usabilidad de la aplicación.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido la estructura del informe.",
        "Se han generado informes básicos a partir de una fuente de datos mediante asistentes.",
        "Se han establecido filtros sobre los valores a presentar en los informes.",
        "Se han incluido valores calculados, recuentos y totales.",
        "Se han incluido gráficos generados a partir de los datos.",
        "Se han utilizado herramientas para generar el código correspondiente a los informes de una aplicación.",
        "Se ha modificado el código correspondiente a los informes.",
        "Se ha desarrollado una aplicación que incluye informes incrustados.",
    ], start=1)],
    "RA6":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado sistemas de generación de ayudas.",
        "Se han generado ayudas en los formatos habituales.",
        "Se han generado ayudas sensibles al contexto.",
        "Se ha documentado la estructura de la información persistente.",
        "Se ha confeccionado el manual de usuario y la guía de referencia.",
        "Se han confeccionado los manuales de instalación, configuración y administración.",
        "Se han confeccionado tutoriales.",
    ], start=1)],
    "RA7":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han empaquetado los componentes que requiere la aplicación.",
        "Se ha personalizado el asistente de instalación",
        "Se ha empaquetado la aplicación para ser instalada de forma típica, completa o personalizada.",
        "Se han generado paquetes de instalación utilizando el entorno de desarrollo.",
        "Se han generado paquetes de instalación utilizando herramientas externas.",
        "Se han generado paquetes instalables en modo desatendido.",
        "Se ha preparado el paquete de instalación para que la aplicación pueda ser correctamente desinstalada.",
        "Se ha preparado la aplicación para ser descargada desde un servidor web y ejecutada.",
    ], start=1)],
    "RA8":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha establecido una estrategia de pruebas.",
        "Se han realizado pruebas de integración de los distintos elementos.",
        "Se han realizado pruebas de regresión.",
        "Se han realizado pruebas de volumen y estrés.",
        "Se han realizado pruebas de seguridad.",
        "Se han realizado pruebas de uso de recursos por parte de la aplicación.",
        "Se ha documentado la estrategia de pruebas y los resultados obtenidos.",
        "Se han realizado pruebas de usuario.",
    ], start=1)],
}

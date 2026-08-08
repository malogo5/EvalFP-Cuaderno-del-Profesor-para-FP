"""EvalFP — Técnicas administrativas básicas · 3003 · Servicios Administrativos
Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 83/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II
RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).
Duración: 197 h · 6 h/semana · 1º SA.
"""
MODULO = {
    "nombre":"Técnicas administrativas básicas","codigo":"3003","abrev":"TAB",
    "ciclo":"Servicios Administrativos","ciclo_clave":"SA","ciclo_nivel":"CFGB",
    "curso":"1º SA","horas_sem":6,"total_horas":197,"anno":"2026-2027","eval_count":3,
    "horas_aula":180,  # el resto hasta 197 h es formación en empresa
    "decreto":"Horas y curso: Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I · RA y CE: Decreto 83/2014, de 01/08/2014 (DOCM núm. 151, de 07/08/2014), Anexo II",
}
UTS = [
    {"id":"UT1","nombre":"La empresa y sus áreas funcionales","horas":29,"eval":1,"tags":"Tipos de empresa · Organigrama · Departamentos · Tareas administrativas"},
    {"id":"UT2","nombre":"Correspondencia y paquetería","horas":52,"eval":1,"tags":"Registro de entrada y salida · Servicios postales · Franqueo · Embalaje · Envíos"},
    {"id":"UT3","nombre":"Almacén de material de oficina","horas":52,"eval":2,"tags":"Fichas de almacén · Inventario · Punto de pedido · Recepción · Consumibles"},
    {"id":"UT4","nombre":"Operaciones básicas de tesorería","horas":47,"eval":3,"tags":"Libro de caja · Arqueo · Medios de pago · Cheque y transferencia · Justificantes"},
]
RAS = [
    {"id":"RA1","pond":16,"nombre":"Clasifica las tareas administrativas de una empresa identificando las áreas funcionales de la misma."},
    {"id":"RA2","pond":29,"nombre":"Tramita correspondencia y paquetería identificando las fases del proceso."},
    {"id":"RA3","pond":29,"nombre":"Controla el almacén de material de oficina relacionando el nivel de existencias con el aseguramiento de la continuidad de los servicios."},
    {"id":"RA4","pond":26,"nombre":"Realiza operaciones básicas de tesorería identificando los diferentes documentos utilizados."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6","CR7","CR8"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"], 3:["RA4"]}
DUAL_RA = None
RA_INSTRUMENTOS = {
    "RA1":["examen","practica"],
    "RA2":["practica","examen"],
    "RA3":["practica","examen"],
    "RA4":["practica","examen"],
}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha definido la organización de una empresa.",
        "Se han descrito las tareas administrativas de una empresa.",
        "Se han identificado las áreas funcionales de una empresa.",
        "Se ha definido el organigrama elemental de una organización privada y pública.",
        "Se ha identificado la ubicación física de las distintas áreas de trabajo.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las distintas fases a realizar en la gestión de la correspondencia.",
        "Se ha realizado la recepción del correo físico y de la paquetería, cumplimentando los documentos internos y externos asociados.",
        "Se ha clasificado el correo utilizando distintos criterios.",
        "Se ha distribuido el correo, tanto el interno como el externo.",
        "Se ha anotado en los libros registro el correo y los paquetes recibidos y distribuidos.",
        "Se ha utilizado el fax para el envío y recepción de documentos por este medio.",
        "Se ha preparado para su envío la correspondencia y paquetería saliente, tanto la normal como la urgente.",
        "Se ha puesto especial interés en no extraviar la correspondencia.",
        "Se ha mantenido en todo momento limpio y en orden el espacio de trabajo",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los materiales de oficina en relación con sus características y aplicaciones.",
        "Se han reconocido las funciones de los inventarios de material.",
        "Se han identificado los diferentes tipos de valoración de existencias.",
        "Se han definido los diferentes tipos de estocaje.",
        "Se ha calculado el volumen de existencias.",
        "Se han empleado aplicaciones informáticas en el control de almacén",
        "Se han descrito los procedimientos administrativos de aprovisionamiento de material",
        "Se han realizado pedidos garantizando unas existencias mínimas.",
        "Se ha valorado la importancia de un estocaje mínimo.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado los distintos medios de cobro y pago.",
        "Se han reconocido los diferentes justificantes de las operaciones de tesorería.",
        "Se han relacionado los requisitos básicos de los medios de pago más habituales.",
        "Se han realizado pagos y cobros al contado simulados, calculando el importe a devolver en cada caso.",
        "Se han realizado operaciones de tesorería simuladas, utilizando para ello los documentos más habituales en este tipo de operaciones.",
        "Se ha cumplimentado un libro registro de movimientos de caja.",
        "Se ha realizado el cálculo el importe a pagar/cobrar en distintas hipótesis de trabajo.",
        "Se ha demostrado responsabilidad tanto en el manejo del dinero en efectivo como en el de los documentos utilizados.",
    ], start=1)],
}

"""EvalFP — Fundamentos de Hardware · 0369 · 1º ASIR
RD 1629/2009, de 30 de octubre (BOE) · Decreto CLM 200/2010, de 3 de agosto (DOCM)
"""
MODULO = {
    "nombre":"Fundamentos de Hardware","codigo":"0371","abrev":"FHW",
    "ciclo":"Administración de Sistemas Informáticos en Red","ciclo_clave":"ASIR","ciclo_nivel":"CFGS",
    "curso":"1º ASIR","horas_sem":3,"total_horas":96,"anno":"2026-2027","eval_count":3,
    "decreto":"RD 1629/2009, de 30 de octubre · Decreto CLM 200/2010, de 3 de agosto (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Arquitectura y componentes del ordenador","horas":20,"eval":1,"tags":"CPU · RAM · Placa base · Bus · Chipset · Arquitectura von Neumann"},
    {"id":"UT2","nombre":"Dispositivos de almacenamiento y periféricos","horas":20,"eval":1,"tags":"HDD · SSD · NVMe · RAID · USB · Interfaces · E/S"},
    {"id":"UT3","nombre":"Ensamblaje y verificación de equipos","horas":20,"eval":2,"tags":"Montaje · BIOS/UEFI · POST · Diagnóstico · Benchmarking · Carga térmica"},
    {"id":"UT4","nombre":"Sistemas de alimentación y refrigeración","horas":18,"eval":2,"tags":"SAI · Fuente de alimentación · Refrigeración líquida · Consumo · PUE"},
    {"id":"UT5","nombre":"Mantenimiento preventivo y correctivo","horas":18,"eval":3,"tags":"Planes de mantenimiento · Diagnóstico de fallos · Herramientas · Inventario · PRL"},
]
RAS = [
    {"id":"RA1","pond":20,"nombre":"Analiza la arquitectura de los equipos y sistemas identificando la función de los componentes hardware."},
    {"id":"RA2","pond":20,"nombre":"Analiza los dispositivos de almacenamiento y periféricos, describiendo sus características y criterios de selección."},
    {"id":"RA3","pond":20,"nombre":"Ensambla equipos hardware, interpretando el esquema de montaje e identificando los elementos que lo integran."},
    {"id":"RA4","pond":20,"nombre":"Analiza los sistemas de alimentación y refrigeración, describiendo sus características y criterios de selección."},
    {"id":"RA5","pond":20,"nombre":"Elabora planes de mantenimiento de equipos hardware, identificando las acciones preventivas y correctivas."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT4","RA4",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT5","RA5",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3","RA4"], 3:["RA5"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica"] for ra in ["RA1","RA2","RA3","RA4","RA5"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha descrito la arquitectura de los equipos informáticos: modelo von Neumann y evolución.",
        "Se han identificado los distintos tipos de microprocesadores, relacionando sus características con sus prestaciones.",
        "Se han descrito las características y tipos de memoria RAM, caché y ROM.",
        "Se ha analizado la función de la placa base y su chipset.",
        "Se han descrito los buses del sistema y los estándares de interconexión.",
        "Se han comparado distintas arquitecturas de equipos para seleccionar el más adecuado a cada uso.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características y tipos de discos duros magnéticos y de estado sólido.",
        "Se han analizado los interfaces de conexión de almacenamiento: SATA, NVMe, SAS.",
        "Se han descrito las configuraciones RAID y su impacto en el rendimiento y la fiabilidad.",
        "Se han identificado los distintos tipos de periféricos y sus interfaces de conexión.",
        "Se han descrito los estándares de conectividad externa: USB, Thunderbolt, HDMI, DisplayPort.",
        "Se han comparado distintas soluciones de almacenamiento para seleccionar la más adecuada.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha interpretado el esquema de montaje de un equipo informático.",
        "Se han instalado el microprocesador, la memoria RAM y el sistema de refrigeración en la placa base.",
        "Se han conectado los dispositivos de almacenamiento y los periféricos internos.",
        "Se han realizado las conexiones eléctricas y de datos del equipo.",
        "Se han configurado los parámetros básicos de la BIOS/UEFI.",
        "Se ha verificado el correcto arranque del equipo y se han identificado errores POST.",
        "Se han aplicado las medidas de prevención de riesgos laborales durante el montaje.",
    ], start=1)],
    "RA4":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito los distintos tipos de fuentes de alimentación y sus características.",
        "Se ha calculado la potencia necesaria de la fuente de alimentación para un sistema dado.",
        "Se han descrito los sistemas de alimentación ininterrumpida (SAI/UPS) y sus tipos.",
        "Se han descrito los sistemas de refrigeración por aire y líquida.",
        "Se han calculado las necesidades de refrigeración en función del TDP de los componentes.",
        "Se ha analizado el PUE (Power Usage Effectiveness) como indicador de eficiencia energética.",
    ], start=1)],
    "RA5":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han identificado las acciones preventivas y correctivas de mantenimiento de equipos.",
        "Se ha elaborado un plan de mantenimiento preventivo para un parque de equipos.",
        "Se han utilizado herramientas hardware y software de diagnóstico.",
        "Se ha gestionado el inventario de equipos y sus componentes.",
        "Se han identificado los residuos generados y los procedimientos de gestión según normativa RAEE.",
        "Se han aplicado las normas de seguridad y PRL en las tareas de mantenimiento.",
    ], start=1)],
}

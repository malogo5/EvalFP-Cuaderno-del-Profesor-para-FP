"""EvalFP — Sistemas de Big Data · 5074 · CE Inteligencia Artificial y Big Data
RD 279/2021, de 20 de abril (BOE) · Decreto CLM 69/2022, de 21 de junio (DOCM)
"""
MODULO = {
    "nombre":"Sistemas de Big Data","codigo":"5074","abrev":"SBD",
    "ciclo":"CE Inteligencia Artificial y Big Data","ciclo_clave":"CE_IABD","ciclo_nivel":"CE",
    "curso":"CE IABD","horas_sem":3,"total_horas":90,"anno":"2026-2027","eval_count":2,
    "decreto":"RD 279/2021, de 20 de abril · Decreto CLM 69/2022, de 21 de junio (DOCM)",
}
UTS = [
    {"id":"UT1","nombre":"Fundamentos y ecosistema Big Data","horas":20,"eval":1,"tags":"Las 5 V · Hadoop · HDFS · MapReduce · YARN · Cloud · Data Lake · Data Warehouse"},
    {"id":"UT2","nombre":"Procesamiento distribuido con Apache Spark","horas":35,"eval":1,"tags":"RDD · DataFrame · Spark SQL · PySpark · SparkStreaming · MLlib"},
    {"id":"UT3","nombre":"Almacenamiento y gestión de datos masivos","horas":35,"eval":2,"tags":"NoSQL · MongoDB · Cassandra · HBase · Kafka · Data pipelines · ETL"},
]
RAS = [
    {"id":"RA1","pond":25,"nombre":"Identifica los sistemas y tecnologías Big Data, describiendo su arquitectura y los casos de uso habituales."},
    {"id":"RA2","pond":45,"nombre":"Gestiona sistemas de procesamiento distribuido utilizando Apache Spark para el análisis de grandes volúmenes de datos."},
    {"id":"RA3","pond":30,"nombre":"Implementa soluciones de almacenamiento y procesamiento de datos masivos utilizando tecnologías NoSQL y plataformas cloud."},
]
ASIGNACIONES = [
    ("UT1","RA1",["CR1","CR2","CR3","CR4","CR5","CR6"]),
    ("UT2","RA2",["CR1","CR2","CR3","CR4","CR5","CR6","CR7"]),
    ("UT3","RA3",["CR1","CR2","CR3","CR4","CR5","CR6"]),
]
EVAL_RAS = {1:["RA1","RA2"], 2:["RA3"]}
DUAL_RA = None
RA_INSTRUMENTOS = {ra:["practica","proyecto"] for ra in ["RA1","RA2","RA3"]}
CES = {
    "RA1":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han descrito las características del Big Data (volumen, velocidad, variedad, veracidad y valor).",
        "Se han identificado los componentes del ecosistema Hadoop (HDFS, MapReduce, YARN).",
        "Se han comparado las arquitecturas Lambda y Kappa para el procesamiento de datos.",
        "Se han diferenciado Data Lake, Data Warehouse y Data Lakehouse.",
        "Se han identificado los principales proveedores cloud de servicios Big Data.",
        "Se ha valorado el impacto del Big Data en los procesos de toma de decisiones empresariales.",
    ], start=1)],
    "RA2":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se ha configurado un entorno Apache Spark local y distribuido.",
        "Se han realizado operaciones con RDDs y DataFrames en PySpark.",
        "Se han ejecutado consultas SQL sobre datos distribuidos con Spark SQL.",
        "Se han implementado transformaciones y acciones sobre grandes conjuntos de datos.",
        "Se ha aplicado MLlib para el entrenamiento de modelos de ML sobre datos distribuidos.",
        "Se ha procesado flujos de datos en tiempo real con Spark Streaming.",
        "Se ha optimizado el rendimiento de los jobs Spark ajustando la configuración del clúster.",
    ], start=1)],
    "RA3":[{"id":f"CR{i}","texto":t} for i,t in enumerate([
        "Se han diferenciado los tipos de bases de datos NoSQL y sus casos de uso.",
        "Se han realizado operaciones CRUD en MongoDB y Cassandra.",
        "Se han diseñado e implementado pipelines de datos con Apache Kafka.",
        "Se han implementado procesos ETL para la ingestión y transformación de datos masivos.",
        "Se han utilizado servicios cloud (AWS S3, Azure Data Lake, Google BigQuery) para el almacenamiento de datos.",
        "Se han monitorizado y gestionado los clústeres de Big Data asegurando su disponibilidad.",
    ], start=1)],
}

#!/usr/bin/env python3
"""Genera los módulos transversales de todos los ciclos del catálogo.

HORAS, CURSO Y HORAS SEMANALES: del anexo del decreto de Castilla-La Mancha
(78/2024, 79/2024 u 80/2024), leídos de normativa/anexos_2024_horas.json.

RESULTADOS DE APRENDIZAJE Y CRITERIOS DE EVALUACIÓN: literales del Real Decreto
al que remiten expresamente los decretos de CLM (ver transversales_datos.py).

  1709/1710 Itinerario personal I y II  → RD 659/2023, anexo V
  1664 Digitalización (GM)              → RD 659/2023, anexo VI
  1665 Digitalización (GS)              → RD 659/2023, anexo VII
  1708 Sostenibilidad                   → RD 659/2023, anexo VIII
  0156 Inglés profesional (GM)          → RD 659/2023, anexo IX
  0179 Inglés profesional (GS)          → RD 659/2023, anexo X
  1713 Proyecto intermodular (GM)       → RD 499/2024, anexo II
  3160 Proyecto intermodular (básico)   → RD 498/2024, anexo I

La capa didáctica (unidades de trabajo, ponderaciones, reparto por evaluación e
instrumentos) es propuesta, no normativa: se ajusta desde Programación.

    python3 scripts/normativa/gen_transversales.py
"""
import json
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
RAIZ = AQUI.parent.parent
MODS = RAIZ / "scripts" / "modules"

from transversales_datos import IPE_I, IPE_II, SOSTENIBILIDAD          # noqa: E402
from transversales_datos2 import (DIGITALIZACION_GM, DIGITALIZACION_GS,  # noqa: E402
                                  INGLES_GM, INGLES_GS)

# ---------------------------------------------------------------------------
# Proyecto intermodular
# ---------------------------------------------------------------------------

PROYECTO_GM = {
 "codigo": "1713", "nombre": "Proyecto intermodular",
 "anexo": "Anexo II del Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024)",
 "ras": [
  ("Caracteriza las empresas del sector atendiendo a su organización y al tipo de producto o servicio que ofrecen.", [
   "Se han identificado las empresas tipo más representativas del sector.",
   "Se ha descrito la estructura organizativa de las empresas.",
   "Se han caracterizado los principales departamentos.",
   "Se han determinado las funciones de cada departamento.",
   "Se ha evaluado el volumen de negocio de acuerdo a las necesidades de los clientes.",
   "Se ha definido la estrategia para dar respuesta a las demandas.",
   "Se han valorado los recursos humanos y materiales necesarios.",
   "Se ha realizado el seguimiento de los resultados de acuerdo a la estrategia aplicada.",
   "Se han relacionado los productos o servicios con su posible contribución a los ODS (Objetivos de Desarrollo Sostenible).",
  ]),
  ("Plantea soluciones a las necesidades del sector teniendo en cuenta la viabilidad de las mismas, los costes asociados y elaborando un pequeño proyecto.", [
   "Se han identificado las necesidades.",
   "Se han planteado en grupo posibles soluciones.",
   "Se ha obtenido la información relativa a las soluciones planteadas.",
   "Se han identificado aspectos innovadores que puedan ser de aplicación.",
   "Se ha realizado el estudio de viabilidad técnica.",
   "Se han identificado las partes que componen el proyecto.",
   "Se han previsto los recursos materiales y humanos para realizarlo.",
   "Se ha realizado el presupuesto económico correspondiente.",
   "Se ha definido y elaborado la documentación para su diseño.",
   "Se han identificado los aspectos relacionados con la calidad del proyecto.",
   "Se han presentado en público las ideas más relevantes de los proyectos propuestos.",
  ]),
  ("Planifica la ejecución de las actividades propuestas a la solución planteada, determinando el plan de intervención y elaborando la documentación correspondiente.", [
   "Se han temporizado las secuencias de las actividades.",
   "Se han determinado los recursos y la logística de cada actividad.",
   "Se han identificado permisos y autorizaciones en caso de ser necesarios.",
   "Se han identificado las actividades que implican riesgos en su ejecución.",
   "Se ha tenido en cuenta el plan de prevención de riesgos y los medios y equipos necesarios.",
   "Se han asignado recursos materiales y humanos a cada actividad.",
   "Se han tenido en cuenta posibles imprevistos.",
   "Se han propuesto soluciones a los posibles imprevistos.",
   "Se ha elaborado la documentación necesaria.",
  ]),
  ("Realiza el seguimiento de la ejecución de las actividades planteadas, verificando que se cumple con la planificación.", [
   "Se ha definido el procedimiento de seguimiento de las actividades.",
   "Se ha verificado la calidad de los resultados de las actividades.",
   "Se han identificado posibles desviaciones de la planificación y/o los resultados esperados.",
   "Se ha informado de las desviaciones en caso de ser necesario.",
   "Se han solucionado las desviaciones y se han documentado las intervenciones.",
   "Se ha definido y elaborado la documentación necesaria para la evaluación de las actividades y del proyecto en su conjunto.",
  ]),
  # Errata del BOE: el anexo II numera dos veces la letra a) en este RA.
  ("Transmite información con claridad, de manera ordenada y estructurada.", [
   "Se ha mantenido una actitud ordenada y metódica en la transmisión de la información.",
   "Se ha transmitido información verbal tanto horizontal como verticalmente.",
   "Se ha transmitido información entre los miembros del grupo utilizando medios informáticos.",
   "Se han conocido los términos técnicos en otras lenguas que sean estándares del sector.",
  ]),
 ],
}

PROYECTO_GB = {
 "codigo": "3160", "nombre": "Proyecto intermodular de aprendizaje colaborativo",
 "anexo": "Anexo I del Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024)",
 "ras": [
  ("Busca información en internet sobre empresas «tipo» del sector/es relacionados con los estándares (unidades) de competencia incluidos en el ámbito profesional del título, elaborando un mapa de las mismas y los servicios o productos que ofrecen.", [
   "Se ha elaborado conjuntamente un esquema que contemple el conjunto de las empresas tipo del sector.",
   "Se han constituido equipos de trabajo y se han distribuido entre los grupos las empresas que se analizarán.",
   "Se ha identificado para la empresa seleccionada los productos o servicios que ofrece.",
   "Se han relacionado los productos o servicios ofertados con la consecución de los ODS (Objetivos de Desarrollo Sostenible).",
   "Se ha realizado un diagrama de bloques de los posibles departamentos que conforman la empresa.",
   "Se han tenido en cuenta las áreas transversales y su relación con las demás.",
   "Se ha presentado al gran grupo la configuración de la empresa y productos que ofrece.",
   "Se ha hecho una valoración de los recursos necesarios para cada unidad.",
   "Se ha elaborado un informe en un formato establecido con la información recabada, indicando al menos: el sector en el que se encuadra, los principales países donde opera, y las áreas de las que se compone.",
  ]),
  ("Selecciona un servicio o producto de una empresa del sector relacionándolo con su contribución a los ODS y sus destinatarios a nivel global.", [
   "Se ha seleccionado un producto/servicio de la empresa a estudio.",
   "Se ha discutido en grupo con qué ODS pueda estar relacionado.",
   "Se han identificado las características del público objetivo al que está destinado.",
   "Se ha comparado el producto con otros de empresas similares.",
   "Se ha desarrollado una propuesta innovadora para potenciar el producto o servicio.",
  ]),
  ("Hace una propuesta de una empresa tipo «spin off» indicando los aspectos diferenciales con la empresa de referencia y elaborando un dossier con sus características.", [
   "Se ha planteado en el grupo el concepto de una empresa tipo «spin off», indicando sus ventajas e inconvenientes.",
   "Se ha discutido en grupo con qué ODS pueda estar relacionado.",
   "Se ha propuesto una posible organización de la empresa, atendiendo a una estructura lineal o circular.",
   "Se han indicado que tecnologías se incluirían para aumentar su competitividad.",
   "Se han propuesto aspectos innovadores sobre algún producto de la empresa de referencia.",
  ]),
  ("Relaciona cada unidad de una empresa tipo con la prevención de riesgos profesionales identificando los equipos/sistemas de protección generales y los propios de cada actividad.", [
   "Se ha analizado la responsabilidad de la empresa y los trabajadores en la consecución de entornos de trabajo seguros.",
   "Se han identificado los sistemas de protección generales e individuales de cada unidad en función de las actividades a realizar.",
   "Se ha estimado el coste de los elementos de protección individual.",
   "Se han propuesto posibles elementos de mejora en relación con la seguridad.",
  ]),
  ("Transmite información con claridad de manera ordenada y estructurada.", [
   "Se ha mantenido una actitud ordenada y metódica en la transmisión de la información.",
   "Se ha transmitido información verbal tanto horizontal como verticalmente.",
   "Se ha transmitido información entre los miembros del grupo utilizando medios informáticos.",
   "Se han conocido los términos técnicos en otras lenguas que sean estándares del sector.",
  ]),
 ],
}

RD659 = ("por remisión expresa del decreto de CLM, Real Decreto 659/2023, de 18 de "
         "julio (BOE núm. 174, de 22/07/2023), texto consolidado")

# código -> (datos, abreviatura, sufijo de fichero, remisión)
CATALOGO = {
 "1709": (IPE_I,            "IPE1",  "ipe1",  RD659),
 "1710": (IPE_II,           "IPE2",  "ipe2",  RD659),
 "1708": (SOSTENIBILIDAD,   "SOST",  "sost",  RD659),
 "1664": (DIGITALIZACION_GM, "DIG",  "dig",   RD659),
 "1665": (DIGITALIZACION_GS, "DIG",  "dig",   RD659),
 "0156": (INGLES_GM,        "INGP",  "ing",   RD659),
 "0179": (INGLES_GS,        "INGP",  "ing",   RD659),
 "1713": (PROYECTO_GM,      "PROY",  "proy",
          "por remisión expresa del Decreto 79/2024, Real Decreto 499/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024)"),
 "3160": (PROYECTO_GB,      "PROY",  "proy",
          "por remisión expresa del Decreto 78/2024, Real Decreto 498/2024, de 21 de mayo (BOE núm. 129, de 28/05/2024)"),
}

# ciclo_clave -> (decreto CLM, texto del ciclo en el anexo, prefijo de fichero,
#                 nombre del ciclo en el catálogo, nivel)
CICLOS = {
 "ASIR": ("80/2024", "Administración de Sistemas Informáticos en Red", "asir",
          "Administración de Sistemas Informáticos en Red", "CFGS"),
 "DAW":  ("80/2024", "Desarrollo de Aplicaciones Web", "daw",
          "Desarrollo de Aplicaciones Web", "CFGS"),
 "DAM":  ("80/2024", "Desarrollo de Aplicaciones Multiplataforma", "dam",
          "Desarrollo de Aplicaciones Multiplataforma", "CFGS"),
 "AD":   ("80/2024", "Asistencia a la Dirección", "ad",
          "Asistencia a la Dirección", "CFGS"),
 "AF":   ("80/2024", "Administración y Finanzas", "af",
          "Administración y Finanzas", "CFGS"),
 "GA":   ("79/2024", "Gestión Administrativa", "ga",
          "Gestión Administrativa", "CFGM"),
 "SMR":  ("79/2024", "Sistemas Microinformáticos y Redes", "smr",
          "Sistemas Microinformáticos y Redes", "CFGM"),
 "CFGB": ("78/2024", "Informática de Oficina", "cfgb_io",
          "Informática de Oficina", "CFGB"),
 "SA":   ("78/2024", "Servicios Administrativos", "sa",
          "Servicios Administrativos", "CFGB"),
}

SIGLA = {"ASIR": "ASIR", "DAW": "DAW", "DAM": "DAM", "AD": "AD", "AF": "AF",
         "GA": "GA", "SMR": "SMR", "CFGB": "IO", "SA": "SA"}

DEC_CLM = {
 "78/2024": "Decreto 78/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I",
 "79/2024": "Decreto 79/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I",
 "80/2024": "Decreto 80/2024, de 05/11/2024 (DOCM núm. 218, de 11/11/2024), Anexo I",
}


def reparte(pesos, total):
    s = sum(pesos)
    ex = [p * total / s for p in pesos]
    base = [int(x) for x in ex]
    orden = sorted(range(len(pesos)), key=lambda i: ex[i] - base[i], reverse=True)
    for i in orden[:total - sum(base)]:
        base[i] += 1
    return base


def corta(t, n=62):
    t = t.rstrip(".")
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"


def genera(clave, cod, fila, bloque):
    datos, abrev, suf, remision = CATALOGO[cod]
    dec, _, pref, nombre_ciclo, nivel = CICLOS[clave]
    horas = fila["horas"]
    sem = [s for s in fila["semanales"] if s]
    # el proyecto intermodular reparte 1 h en cada curso: se ancla en 2.º
    if len(sem) > 1:
        curso_n, hsem = 2, sem[-1]
    else:
        curso_n = 1 if fila["semanales"][0] else 2
        hsem = sem[0] if sem else 1
    curso = f"{curso_n}º {SIGLA[clave]}"
    evalc = 2 if curso_n == 2 else 3

    n = len(datos["ras"])
    n_ces = [len(c) for _, c in datos["ras"]]
    h_ut = reparte(n_ces, horas)
    ponds = reparte(n_ces, 100)
    corte = (n + 1) // 2
    evals = [1 if i < corte else 2 for i in range(n)]
    if evalc == 2:
        evals = [min(e, 2) for e in evals]

    procedencia = (f"Horas, curso y h/semana: {DEC_CLM[dec]} · "
                   f"RA y CE: {datos['anexo'] if cod in ('1713', '3160') else datos['anexo'] + ' del RD 659/2023'} "
                   f"({remision})")

    L = [f'"""EvalFP — {datos["nombre"]} · {cod} · {nombre_ciclo}',
         procedencia,
         "Módulo transversal: Castilla-La Mancha no redacta RA ni CE propios para él,",
         "remite al Real Decreto. Las horas sí son las del anexo del decreto autonómico.",
         f'Duración: {horas} h · {hsem} h/semana · {curso}.',
         "UT, ponderaciones y reparto por evaluación: propuesta didáctica, no normativa.",
         '"""',
         "MODULO = {",
         f'    "nombre":"{datos["nombre"]}","codigo":"{cod}","abrev":"{abrev}",',
         f'    "ciclo":"{nombre_ciclo}","ciclo_clave":"{clave}","ciclo_nivel":"{nivel}",',
         f'    "curso":"{curso}","horas_sem":{hsem},"total_horas":{horas},'
         f'"anno":"2026-2027","eval_count":{evalc},',
         f'    "decreto":"{procedencia}",',
         "}",
         "UTS = ["]
    for i, (ra, _) in enumerate(datos["ras"], 1):
        L.append(f'    {{"id":"UT{i}","nombre":"{corta(ra)}","horas":{h_ut[i-1]},'
                 f'"eval":{evals[i-1]},"tags":""}},')
    L.append("]")
    L.append("RAS = [")
    for i, (ra, _) in enumerate(datos["ras"], 1):
        L.append(f'    {{"id":"RA{i}","pond":{ponds[i-1]},"nombre":"{ra}"}},')
    L.append("]")
    L.append("ASIGNACIONES = [")
    for i, (_, ces) in enumerate(datos["ras"], 1):
        ids = ",".join(f'"CR{j}"' for j in range(1, len(ces) + 1))
        L.append(f'    ("UT{i}","RA{i}",[{ids}]),')
    L.append("]")
    e1 = [f'"RA{i}"' for i in range(1, n + 1) if evals[i - 1] == 1]
    e2 = [f'"RA{i}"' for i in range(1, n + 1) if evals[i - 1] == 2]
    L.append(f'EVAL_RAS = {{1:[{", ".join(e1)}], 2:[{", ".join(e2)}]}}')
    L.append("DUAL_RA = None")
    L.append("RA_INSTRUMENTOS = {")
    for i in range(1, n + 1):
        L.append(f'    "RA{i}":["practica"],')
    L.append("}")
    L.append("CES = {")
    for i, (_, ces) in enumerate(datos["ras"], 1):
        L.append(f'    "RA{i}":[{{"id":f"CR{{i}}","texto":t}} for i,t in enumerate([')
        for c in ces:
            L.append(f'        "{c}",')
        L.append("    ], start=1)],")
    L.append("}")
    return f"{pref}_{suf}_data.py", "\n".join(L) + "\n"


def main():
    anexos = json.load(open(RAIZ / "normativa" / "anexos_2024_horas.json"))
    creados = 0
    for clave, (dec, texto, pref, _, _) in CICLOS.items():
        bloque = next(b for b in anexos
                      if b["decreto"] == dec and b["n_cursos"] == 2 and texto in b["ciclo"])
        for fila in bloque["modulos"]:
            cod = fila["codigo"]
            if cod not in CATALOGO:
                continue
            nombre, contenido = genera(clave, cod, fila, bloque)
            (MODS / nombre).write_text(contenido, encoding="utf-8")
            creados += 1
            print(f"  {nombre:26} {cod}  {fila['horas']:>3} h  {clave}")
    print(f"\n{creados} módulos transversales generados")


if __name__ == "__main__":
    main()

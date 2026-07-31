#!/usr/bin/env python3
"""
gen_modulo.py — genera scripts/modules/<archivo>_data.py a partir de un JSON
con los RA y CE **literales del DOCM**.

Uso:
    python3 scripts/gen_modulo.py normativa/docm_json/GA_0437.json

Formato del JSON de entrada (ver normativa/docm_json/_PLANTILLA.json):
{
  "archivo": "ga_ceac",                 # nombre del _data.py (sin sufijo)
  "modulo": {
    "nombre": "...", "codigo": "0437", "abrev": "CEAC",
    "ciclo": "Gestión Administrativa", "ciclo_clave": "GA", "ciclo_nivel": "CFGM",
    "curso": "1º GA", "horas_sem": 4, "total_horas": 130,
    "anno": "2026-2027", "eval_count": 3,
    "decreto": "Decreto 251/2011, de 12/08/2011 (DOCM 22/08/2011)"
  },
  "ras": [
    {"enunciado": "...", "ut": "Nombre corto de la UT", "eval": 1,
     "tags": "a · b · c", "instrumentos": ["examen","practica"],
     "ces": ["texto literal CE1", "texto literal CE2"]}
  ],
  "dual_ra": null
}

Reglas que aplica el generador (las mismas verificadas en los módulos ya buenos):
  · Una UT por RA, en el orden del decreto.
  · Horas de cada UT proporcionales a su nº de CE, ajustadas para sumar total_horas.
  · Ponderación de cada RA proporcional a su nº de CE, ajustada para sumar 100.
  · Todos los CE de un RA quedan asignados a su UT (ninguno suelto).
  · eval por RA: la del JSON si viene; si no, reparto secuencial equilibrado en horas.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "modules")


def reparto_entero(pesos, total):
    """Reparte `total` en enteros proporcionalmente a `pesos` (restos mayores)."""
    suma = sum(pesos) or 1
    brutos = [p * total / suma for p in pesos]
    base = [int(b) for b in brutos]
    resto = total - sum(base)
    orden = sorted(range(len(pesos)), key=lambda i: brutos[i] - base[i], reverse=True)
    for i in range(resto):
        base[orden[i % len(orden)]] += 1
    return base


def reparto_evals(horas, n_evals):
    """Asigna cada RA a una evaluación buscando bloques de horas equilibrados."""
    total = sum(horas)
    objetivo = total / n_evals
    evals, acum, ev = [], 0, 1
    for i, h in enumerate(horas):
        restantes_ra = len(horas) - i
        restantes_ev = n_evals - ev + 1
        # Deja siempre al menos un RA por evaluación pendiente
        if ev < n_evals and acum + h / 2 > objetivo * ev and restantes_ra > restantes_ev - 1:
            ev += 1
        evals.append(ev)
        acum += h
    # Garantiza que ninguna evaluación queda vacía
    for e in range(1, n_evals + 1):
        if e not in evals:
            for i in range(len(evals) - 1, -1, -1):
                if evals.count(evals[i]) > 1:
                    evals[i] = e
                    break
            evals.sort()
    return evals


def py(s):
    """Literal Python de una cadena, en una sola línea."""
    return json.dumps(" ".join(str(s).split()), ensure_ascii=False)


def generar(cfg):
    m = cfg["modulo"]
    ras = cfg["ras"]
    n = len(ras)
    n_ces = [len(r["ces"]) for r in ras]
    total = int(m["total_horas"])
    n_ev = int(m.get("eval_count", 3))

    # En los ciclos con fase de formación en empresa, la duración oficial del módulo
    # incluye esas horas. Las UT sólo pueden repartir las horas de aula.
    aula = int(m.get('horas_aula') or total)
    horas = reparto_entero(n_ces, aula)
    ponds = reparto_entero(n_ces, 100)
    evals = [r["eval"] for r in ras] if all("eval" in r for r in ras) else reparto_evals(horas, n_ev)

    L = []
    A = L.append
    A('"""EvalFP — %s · %s · %s' % (m["nombre"], m["codigo"], m["ciclo"]))
    A(m["decreto"])
    A("RA y CE literales del anexo de currículo del decreto de Castilla-La Mancha (DOCM).")
    A("Duración: %d h · %s h/semana · %s." % (total, m.get("horas_sem", "?"), m.get("curso", "")))
    A('"""')
    A("MODULO = {")
    A('    "nombre":%s,"codigo":%s,"abrev":%s,' % (py(m["nombre"]), py(m["codigo"]), py(m["abrev"])))
    A('    "ciclo":%s,"ciclo_clave":%s,"ciclo_nivel":%s,'
      % (py(m["ciclo"]), py(m["ciclo_clave"]), py(m["ciclo_nivel"])))
    A('    "curso":%s,"horas_sem":%d,"total_horas":%d,"anno":%s,"eval_count":%d,'
      % (py(m["curso"]), int(m.get("horas_sem", 0)), total, py(m.get("anno", "2026-2027")), n_ev))
    if m.get('horas_aula') and aula != total:
        A('    "horas_aula":%d,  # el resto hasta %d h es formación en empresa' % (aula, total))
    A('    "decreto":%s,' % py(m["decreto"]))
    A("}")

    A("UTS = [")
    for i, r in enumerate(ras):
        A('    {"id":"UT%d","nombre":%s,"horas":%d,"eval":%d,"tags":%s},'
          % (i + 1, py(r.get("ut") or r["enunciado"][:60]), horas[i], evals[i], py(r.get("tags", ""))))
    A("]")

    A("RAS = [")
    for i, r in enumerate(ras):
        A('    {"id":"RA%d","pond":%d,"nombre":%s},' % (i + 1, ponds[i], py(r["enunciado"])))
    A("]")

    A("ASIGNACIONES = [")
    for i, r in enumerate(ras):
        ces = ",".join('"CR%d"' % (j + 1) for j in range(len(r["ces"])))
        A('    ("UT%d","RA%d",[%s]),' % (i + 1, i + 1, ces))
    A("]")

    porev = {}
    for i, e in enumerate(evals):
        porev.setdefault(e, []).append("RA%d" % (i + 1))
    A("EVAL_RAS = {%s}" % ", ".join(
        "%d:[%s]" % (e, ",".join('"%s"' % x for x in v)) for e, v in sorted(porev.items())))
    A("DUAL_RA = %s" % (py(cfg["dual_ra"]) if cfg.get("dual_ra") else "None"))

    A("RA_INSTRUMENTOS = {")
    for i, r in enumerate(ras):
        ins = r.get("instrumentos") or ["examen", "practica"]
        A('    "RA%d":[%s],' % (i + 1, ",".join('"%s"' % x for x in ins)))
    A("}")

    A("CES = {")
    for i, r in enumerate(ras):
        A('    "RA%d":[{"id":f"CR{i}","texto":t} for i,t in enumerate([' % (i + 1))
        for ce in r["ces"]:
            A("        %s," % py(ce))
        A("    ], start=1)],")
    A("}")

    # ---- verificaciones ----
    errores = []
    if sum(horas) != aula:
        errores.append("las horas de las UT suman %d y las de aula son %d" % (sum(horas), aula))
    if sum(ponds) != 100:
        errores.append("las ponderaciones suman %d%%" % sum(ponds))
    if 0 in n_ces:
        errores.append("hay algún RA sin criterios de evaluación")
    if sorted(set(evals)) != list(range(1, n_ev + 1)):
        errores.append("evaluaciones asignadas %s con eval_count=%d" % (sorted(set(evals)), n_ev))
    if min(horas) <= 0:
        errores.append("alguna UT se queda con 0 horas")
    return "\n".join(L) + "\n", errores, {"ras": n, "ces": sum(n_ces), "horas": horas, "ponds": ponds, "evals": evals}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    fallos = 0
    for ruta in sys.argv[1:]:
        with open(ruta, encoding="utf-8") as f:
            cfg = json.load(f)
        codigo, errores, info = generar(cfg)
        destino = os.path.join(DEST, "%s_data.py" % cfg["archivo"])
        with open(destino, "w", encoding="utf-8") as f:
            f.write(codigo)
        estado = "OK " if not errores else "AVISO"
        print("%s %-24s %s · %d RA · %d CE · horas %s · pond %s · ev %s"
              % (estado, cfg["modulo"]["abrev"], cfg["modulo"]["codigo"], info["ras"], info["ces"],
                 info["horas"], info["ponds"], info["evals"]))
        for e in errores:
            fallos += 1
            print("      ! %s" % e)
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
prebake_modules.py
Genera renderer/modules_data.json con TODOS los módulos.
Ejecutar antes de npm run build:
    python3 scripts/prebake_modules.py
"""
import sys, json, os, importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
MODS = os.path.join(ROOT, "modules")
OUT  = os.path.join(ROOT, "..", "renderer", "modules_data.json")

sys.path.insert(0, ROOT)

def export_module(name):
    mod = importlib.import_module(f"modules.{name}")
    m   = dict(mod.MODULO)

    # ── Evaluaciones parciales del módulo ───────────────────────────────────
    #
    # En 2º curso solo hay DOS evaluaciones parciales: el tercer trimestre se
    # dedica a la formación en centros de trabajo. El catálogo lo tenía a medias
    # —AD, AF y GA con dos; DAM, ASIR, IO, DAW, SA y SMR con tres—, así que la
    # aplicación ofrecía una 3ª evaluación que no existe en el calendario.
    #
    # Las unidades que estuvieran colocadas en un tercer trimestre pasan al
    # segundo, y lo mismo el mapa de RA por evaluación.
    uts = [dict(u) for u in mod.UTS]
    eval_ras = {str(k): list(v) for k, v in (getattr(mod, "EVAL_RAS", {}) or {}).items()}
    if str(m.get("curso", "")).strip().startswith("2"):
        m["eval_count"] = 2
        for u in uts:
            if int(u.get("eval", 1) or 1) > 2:
                u["eval"] = 2
        if "3" in eval_ras:
            eval_ras["2"] = list(dict.fromkeys(eval_ras.get("2", []) + eval_ras.pop("3")))

    # ── Actividades de partida ──────────────────────────────────────────────
    #
    # Tres reglas, aprendidas auditando la aplicación en uso:
    #
    #  1. Cada actividad nace con SUS CRITERIOS marcados. Una actividad sin
    #     criterios no entra en la nota de ningún RA: se podía calificar el
    #     examen de una evaluación entera y que no moviera la calificación del
    #     módulo, mientras la parrilla sí mostraba su nota.
    #  2. El examen de cada evaluación cuelga de las UT de esa evaluación. Sin
    #     UT ni RA, la fila decía «sin RA» y no computaba.
    #  3. Los pesos de cada evaluación suman 100: las prácticas se reparten el
    #     30 % y el examen se lleva el 70 %. Antes cada práctica llevaba un 30
    #     fijo y la suma salía 130 % o 160 %, con la aplicación avisando de un
    #     error que ella misma había creado.
    #
    # Todo esto es un punto de partida razonable, no una imposición: se cambia
    # en Programación.
    PESO_PRACTICAS = 30
    PESO_EXAMEN    = 70

    ut_por_id = {u["id"]: u for u in uts}

    def _eval_de(ut_id):
        return ut_por_id.get(ut_id, {}).get("eval", 1)

    # Criterios de cada UT, con la clave compuesta RA|CE que usa el motor
    # (el id del criterio se repite en todos los RA del módulo).
    ces_por_ut = {}
    for ut_id, ra_id, ces in mod.ASIGNACIONES:
        ces_por_ut.setdefault(ut_id, []).extend(f"{ra_id}|{ce}" for ce in ces)

    actividades = []
    orden = 1
    # una práctica por cada par UT–RA: si una UT trabaja criterios de dos RA,
    # cada RA necesita su propia actividad para poder calificarse
    vistas = set()
    ras_por_ut = {}
    for ut_id, ra_id, _ in mod.ASIGNACIONES:
        ras_por_ut.setdefault(ut_id, []).append(ra_id)
    for ut_id, ra_id, ces in mod.ASIGNACIONES:
        if (ut_id, ra_id) in vistas:
            continue
        vistas.add((ut_id, ra_id))
        ut = ut_por_id.get(ut_id, {})
        sufijo = f" ({ra_id})" if len(set(ras_por_ut.get(ut_id, []))) > 1 else ""
        actividades.append({
            "ut_id": ut_id, "ra_id": ra_id,
            "descripcion": f"Práctica {ut_id}{sufijo} — {ut.get('nombre','')}",
            "instrumento": "Práctica", "tipo": "practica",
            "peso": PESO_PRACTICAS, "nota_max": 10,
            "eval": ut.get("eval", 1), "orden": orden,
            "ces": [f"{ra_id}|{ce}" for ce in ces],
        })
        orden += 1

    evals_con_uts = sorted(set(u.get("eval", 1) for u in uts))
    for ev in evals_con_uts:
        uts_ev = [u["id"] for u in uts if u.get("eval", 1) == ev]
        ces_ev, vistos = [], set()
        for ut_id in uts_ev:
            for clave in ces_por_ut.get(ut_id, []):
                if clave not in vistos:
                    vistos.add(clave)
                    ces_ev.append(clave)
        actividades.append({
            "ut_id": ",".join(uts_ev) or None, "ra_id": None,
            "descripcion": f"Examen Evaluación {ev}",
            "instrumento": "Examen", "tipo": "examen",
            "peso": PESO_EXAMEN, "nota_max": 10,
            "eval": ev, "orden": orden,
            "ces": ces_ev,
        })
        orden += 1

    # Repartir el 30 % de las prácticas dentro de cada evaluación, cuadrando a
    # 100 con el examen. El resto de la división se suma a la primera, para que
    # la suma sea exacta y no 29 ni 31.
    for ev in evals_con_uts:
        practicas_ev = [a for a in actividades if a["eval"] == ev and a["tipo"] == "practica"]
        if not practicas_ev:
            continue
        base = PESO_PRACTICAS // len(practicas_ev)
        resto = PESO_PRACTICAS - base * len(practicas_ev)
        for i, a in enumerate(practicas_ev):
            a["peso"] = base + (resto if i == 0 else 0)

    return {
        "modulo":          m,
        "ras":             mod.RAS,
        "uts":             uts,
        "ces":             getattr(mod, "CES", {}),
        "asignaciones":    [{"ut": ut, "ra": ra, "ces": ces} for ut, ra, ces in mod.ASIGNACIONES],
        "eval_ras":        eval_ras,
        "ra_instrumentos": getattr(mod, "RA_INSTRUMENTOS", {}),
        "actividades":     actividades,
    }

def main():
    names = sorted(
        f[:-3] for f in os.listdir(MODS)
        if f.endswith(".py") and not f.startswith("_")
    )

    index   = []
    details = {}
    errors  = []

    for name in names:
        try:
            data = export_module(name)
            m    = data["modulo"]
            index.append({
                "key":         name,
                "codigo":      m.get("codigo", ""),
                "abrev":       m.get("abrev", name),
                "nombre":      m.get("nombre", name),
                "ciclo_clave": m.get("ciclo_clave", "OTRO"),
                "ciclo_nivel": m.get("ciclo_nivel", ""),
                "ciclo":       m.get("ciclo", ""),
                "curso":       m.get("curso", ""),
                "horas_sem":   m.get("horas_sem", 0),
                "total_horas": m.get("total_horas", 0),
                "horas_aula":  m.get("horas_aula", 0),
            })
            details[name] = data
            print(f"  ✅  {name}")
        except Exception as e:
            errors.append(name)
            print(f"  ❌  {name}: {e}", file=sys.stderr)

    payload = {"index": index, "modules": details}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUT) // 1024
    print(f"\n✅  {len(index)} módulos → {OUT}  ({size_kb} KB)")
    if errors:
        print(f"⚠️  {len(errors)} errores: {errors}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

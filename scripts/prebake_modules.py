#!/usr/bin/env python3
"""
prebake_modules.py
Genera evalfp-app/renderer/modules_data.json con TODOS los módulos.
Ejecutar antes de npm run build:
    python3 scripts/prebake_modules.py
"""
import sys, json, os, importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
MODS = os.path.join(ROOT, "modules")
OUT  = os.path.join(ROOT, "..", "evalfp-app", "renderer", "modules_data.json")

sys.path.insert(0, ROOT)

def export_module(name):
    mod = importlib.import_module(f"modules.{name}")
    m   = mod.MODULO

    actividades = []
    orden = 1
    uts_vistas = set()
    for ut_id, ra_id, ces in mod.ASIGNACIONES:
        if ut_id in uts_vistas:
            continue
        uts_vistas.add(ut_id)
        ut = next((u for u in mod.UTS if u["id"] == ut_id), {})
        actividades.append({
            "ut_id": ut_id, "ra_id": ra_id,
            "descripcion": f"Práctica {ut_id} — {ut.get('nombre','')}",
            "instrumento": "Práctica", "tipo": "practica",
            "peso": 30, "nota_max": 10,
            "eval": ut.get("eval", 1), "orden": orden
        })
        orden += 1

    evals_con_uts = sorted(set(u.get("eval", 1) for u in mod.UTS))
    for ev in evals_con_uts:
        actividades.append({
            "ut_id": None, "ra_id": None,
            "descripcion": f"Examen Evaluación {ev}",
            "instrumento": "Examen", "tipo": "examen",
            "peso": 70, "nota_max": 10,
            "eval": ev, "orden": orden
        })
        orden += 1

    return {
        "modulo":          m,
        "ras":             mod.RAS,
        "uts":             mod.UTS,
        "ces":             getattr(mod, "CES", {}),
        "asignaciones":    [{"ut": ut, "ra": ra, "ces": ces} for ut, ra, ces in mod.ASIGNACIONES],
        "eval_ras":        getattr(mod, "EVAL_RAS", {}),
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

#!/usr/bin/env python3
"""Exporta un módulo de datos a JSON para la app Electron standalone."""
import sys, json, importlib, os

sys.path.insert(0, os.path.dirname(__file__))

def export(mod_name):
    mod = importlib.import_module(f"modules.{mod_name}")
    m   = mod.MODULO

    # Derivar actividades (igual que build_template)
    actividades = []
    orden = 1
    
    # Una práctica por UT
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

    # Un examen por evaluación (donde haya UTs)
    evals_con_uts = sorted(set(u.get("eval",1) for u in mod.UTS))
    for ev in evals_con_uts:
        actividades.append({
            "ut_id": None, "ra_id": None,
            "descripcion": f"Examen Evaluación {ev}",
            "instrumento": "Examen", "tipo": "examen",
            "peso": 70, "nota_max": 10,
            "eval": ev, "orden": orden
        })
        orden += 1

    data = {
        "modulo":        m,
        "ras":           mod.RAS,
        "uts":           mod.UTS,
        "ces":           getattr(mod, "CES", []),
        "asignaciones":  [{"ut": ut, "ra": ra, "ces": ces} for ut, ra, ces in mod.ASIGNACIONES],
        "ra_instrumentos": getattr(mod, "RA_INSTRUMENTOS", {}),
        "actividades":   actividades,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Listar módulos disponibles con metadatos para agrupación
        mods_dir = os.path.join(os.path.dirname(__file__), "modules")
        mod_names = sorted(f[:-3] for f in os.listdir(mods_dir)
                           if f.endswith(".py") and not f.startswith("_"))
        result = []
        for name in mod_names:
            try:
                mod = importlib.import_module(f"modules.{name}")
                m = mod.MODULO
                result.append({
                    "key": name,
                    "abrev": m.get("abrev", name),
                    "nombre": m.get("nombre", name),
                    "ciclo_clave": m.get("ciclo_clave", "OTRO"),
                    "ciclo_nivel": m.get("ciclo_nivel", ""),
                    "ciclo": m.get("ciclo", ""),
                    "curso": m.get("curso", ""),
                })
            except Exception as e:
                result.append({"key": name, "abrev": name, "nombre": name,
                                "ciclo_clave": "OTRO", "ciclo_nivel": "", "ciclo": "", "curso": ""})
        print(json.dumps(result))
    else:
        export(sys.argv[1])

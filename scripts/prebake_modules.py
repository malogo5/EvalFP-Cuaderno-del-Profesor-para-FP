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
    # Los cursos de especialización van igual: duran menos de un curso completo
    # y se organizan en dos trimestres. Dos módulos se habían quedado con tres
    # —uno de Ciberseguridad y otro de IA y Big Data— mientras sus compañeros de
    # curso tenían dos, así que el boletín de un mismo alumno no cuadraba de un
    # módulo a otro.
    #
    # Las unidades que estuvieran colocadas en un tercer trimestre pasan al
    # segundo, y lo mismo el mapa de RA por evaluación.
    uts = [dict(u) for u in mod.UTS]
    eval_ras = {str(k): list(v) for k, v in (getattr(mod, "EVAL_RAS", {}) or {}).items()}
    curso = str(m.get("curso", "")).strip()
    if curso.startswith("2") or curso.upper().startswith("CE"):
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

    # Criterios que se adquieren y se acreditan en la fase de formación en
    # empresa. El módulo los declara en DUAL_CES = {"RA8": ["CR1", ...]}. No
    # llevan peso en el aula: su nota sale del informe de la tutoría de empresa,
    # igual que cualquier otra actividad, para que el motor de calificación no
    # tenga que saber nada especial.
    # DUAL_CES declara los criterios que se trabajan también en la fase de
    # formación en empresa. Se califican al 50 % en el centro y al 50 % con el
    # informe de la tutoría: para que el motor lo calcule exactamente así, cada
    # criterio dualizado queda cubierto por DOS actividades del mismo peso, la
    # práctica de aula de su unidad y el informe de empresa de su RA, y se
    # excluye del examen, que tiene otro peso y rompería el reparto.
    dual_ces = getattr(mod, "DUAL_CES", {}) or {}
    # DUAL_CES admite dos formas: la lista de criterios que se acreditan
    # íntegramente en la empresa, o el diccionario {criterio: puntos sobre 100
    # del RA} cuando el criterio se evalúa en los dos sitios, como hace la
    # programación del departamento.
    dual_peso = {}
    for ra, lista in dual_ces.items():
        if isinstance(lista, dict):
            for ce, w in lista.items():
                dual_peso[f"{ra}|{ce}"] = float(w)
        else:
            for ce in lista:
                dual_peso[f"{ra}|{ce}"] = None   # 100 % en la empresa
    dual_claves = set(dual_peso)
    # Con el modelo del 50 % ningún criterio sale del aula: se evalúa en los dos
    # ámbitos. Solo saldría si el módulo lo declarase al 100 % en la empresa.
    solo_empresa = {k for k, v in dual_peso.items() if v == 100}

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
            "ces": [f"{ra_id}|{ce}" for ce in ces if f"{ra_id}|{ce}" not in solo_empresa],
        })
        orden += 1
    # Una práctica que se ha quedado sin criterios (todos son de empresa) no
    # califica nada: sobra.
    actividades = [a for a in actividades if a["ces"]]

    evals_con_uts = sorted(set(u.get("eval", 1) for u in uts))
    for ev in evals_con_uts:
        uts_ev = [u["id"] for u in uts if u.get("eval", 1) == ev]
        ces_ev, vistos = [], set()
        for ut_id in uts_ev:
            for clave in ces_por_ut.get(ut_id, []):
                if clave not in vistos and clave not in dual_claves:
                    vistos.add(clave)
                    ces_ev.append(clave)
        # Una UT cuyos criterios se acreditan todos en la empresa no entra en el
        # examen: nombrarla haría creer que se examina de algo que no evalúa.
        uts_examen = [u for u in uts_ev
                      if any(c not in dual_claves for c in ces_por_ut.get(u, []))]
        actividades.append({
            "ut_id": ",".join(uts_examen) or None, "ra_id": None,
            "descripcion": f"Examen Evaluación {ev}",
            "instrumento": "Examen", "tipo": "examen",
            "peso": PESO_EXAMEN, "nota_max": 10,
            "eval": ev, "orden": orden,
            "ces": ces_ev,
        })
        orden += 1

    # ── Fase de formación en empresa ────────────────────────────────────────
    # Una actividad por RA dualizado, con los mismos criterios y el MISMO peso
    # que la práctica de aula que los trabaja: así la nota de cada criterio es
    # exactamente la media del centro y de la empresa. Van en la evaluación en
    # la que se puede calificar la estancia, que es la última del módulo.
    empresa_acts = []
    if dual_claves:
        for ra_id, lista in dual_ces.items():
            claves = [f"{ra_id}|{ce}" for ce in (lista.keys() if isinstance(lista, dict) else lista)]
            hermana = next((a for a in actividades
                            if a["tipo"] == "practica" and a["ra_id"] == ra_id
                            and any(c in a["ces"] for c in claves)), None)
            if hermana is None:
                continue
            empresa_acts.append({
                "ut_id": hermana["ut_id"], "ra_id": ra_id,
                "descripcion": f"Informe del periodo de formación en empresa — {ra_id}",
                "instrumento": "Empresa", "tipo": "practica",
                "peso": hermana["peso"], "nota_max": 10,
                "eval": hermana["eval"], "orden": orden,
                "ces": sorted(claves),
                "_gemela": hermana["descripcion"],
            })
            orden += 1
        actividades.extend(empresa_acts)

    # Repartir el 30 % de las prácticas dentro de cada evaluación, cuadrando a
    # 100 con el examen. El resto de la división se suma a la primera, para que
    # la suma sea exacta y no 29 ni 31.
    for ev in evals_con_uts:
        practicas_ev = [a for a in actividades if a["eval"] == ev
                        and a["tipo"] == "practica" and a["instrumento"] != "Empresa"]
        if practicas_ev:
            base = PESO_PRACTICAS // len(practicas_ev)
            resto = PESO_PRACTICAS - base * len(practicas_ev)
            for i, a in enumerate(practicas_ev):
                a["peso"] = base + (resto if i == 0 else 0)
        for a in actividades:
            if a["eval"] == ev and a["tipo"] == "examen":
                a["peso"] = PESO_EXAMEN

    # Cada actividad de empresa toma el peso de su práctica gemela: es lo que
    # hace que la nota del criterio sea la media exacta del centro y de la
    # empresa. Después se reescala la evaluación entera —examen incluido— para
    # que vuelva a sumar 100 sin romper esa igualdad.
    if dual_claves:
        gemela_de = {}
        for a in actividades:
            if a.get("instrumento") == "Empresa":
                g = next((x for x in actividades if x["descripcion"] == a.get("_gemela")), None)
                if g:
                    a["peso"] = g["peso"]
                    gemela_de[a["descripcion"]] = g["descripcion"]
                a.pop("_gemela", None)
        for ev in evals_con_uts:
            acts_ev = [a for a in actividades if a["eval"] == ev]
            total = sum(a["peso"] for a in acts_ev)
            if not total or total == 100:
                continue
            for a in acts_ev:
                a["peso"] = int(round(a["peso"] * 100.0 / total))
            # Reponer la igualdad que el redondeo haya podido romper y cuadrar
            # el 100 con el examen, que es el instrumento de mayor peso.
            for a in acts_ev:
                if a.get("instrumento") == "Empresa" and a["descripcion"] in gemela_de:
                    g = next((x for x in acts_ev if x["descripcion"] == gemela_de[a["descripcion"]]), None)
                    if g:
                        a["peso"] = g["peso"]
            dif = 100 - sum(a["peso"] for a in acts_ev)
            if dif:
                ex = [a for a in acts_ev if a["tipo"] == "examen"]
                (ex[0] if ex else max(acts_ev, key=lambda x: x["peso"]))["peso"] += dif

    # El porcentaje dualizado de cada RA se deriva de sus criterios: es lo que
    # lee la pestaña de Programación para avisar si el módulo se sale del 10-20 %
    # de resultados que debe cubrir la fase de formación en empresa.
    ras_out = []
    for r in mod.RAS:
        r2 = dict(r)
        lista = dual_ces.get(r2["id"], [])
        total = len(getattr(mod, "CES", {}).get(r2["id"], [])) or 0
        if isinstance(lista, dict) and lista:
            r2["dual"] = round(sum(lista.values()))
        elif lista and total:
            # Cada criterio dualizado aporta la mitad de su peso dentro del RA.
            r2["dual"] = round(50.0 * len(lista) / total)
        ras_out.append(r2)

    # Peso de cada criterio dentro de su RA, si el módulo lo declara.
    ce_pesos = getattr(mod, "CE_PESOS", {}) or {}
    ces_out = {}
    for ra_id, lista in (getattr(mod, "CES", {}) or {}).items():
        nuevos = []
        for c in lista:
            c2 = dict(c)
            w = ce_pesos.get(ra_id, {}).get(c2.get("id"))
            if w is not None:
                c2["peso"] = w
            nuevos.append(c2)
        ces_out[ra_id] = nuevos

    return {
        "modulo":          m,
        "ras":             ras_out,
        "uts":             uts,
        "ces":             ces_out or getattr(mod, "CES", {}),
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

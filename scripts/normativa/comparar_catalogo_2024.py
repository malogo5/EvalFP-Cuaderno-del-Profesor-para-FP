#!/usr/bin/env python3
"""Compara el catálogo de EvalFP con los anexos de los Decretos 78/79/80 de 2024.

No modifica nada: sólo produce el informe de discrepancias.
"""
import json
import sys

CAT = "/sessions/friendly-jolly-hawking/mnt/evalfp/renderer/modules_data.json"
ANEXOS = "/tmp/dec/anexos.json"

# ciclo del catálogo -> (decreto, anexo, texto del ciclo en el decreto)
MAPA = {
    "ASIR": ("80/2024", "IA-3. 1º", "Administración de Sistemas Informáticos en Red"),
    "DAW":  ("80/2024", "IA-3. 2º", "Desarrollo de Aplicaciones Web"),
    "DAM":  ("80/2024", "IA-3. 6º", "Desarrollo de Aplicaciones Multiplataforma"),
    "AD":   ("80/2024", "I-C.3º",   "Asistencia a la Dirección"),
    "AF":   ("80/2024", "I-C.4º",   "Administración y Finanzas"),
    "GA":   ("79/2024", "IC-1. 1º", "Gestión Administrativa"),
    "SMR":  ("79/2024", "IA-3 2º",  "Sistemas Microinformáticos y Redes"),
    "CFGB": ("78/2024", "I",        "Informática de Oficina"),
    "SA":   ("78/2024", "I",        "Servicios Administrativos"),
}
# ciclos del catálogo fuera del ámbito de estos tres decretos
FUERA = {"CE_CIBER", "CE_IABD", "CE_PYTHON"}


def carga_anexos():
    d = json.load(open(ANEXOS))
    out = {}
    for clave, (dec, anexo, ciclo) in MAPA.items():
        cand = [b for b in d
                if b["decreto"] == dec and b["n_cursos"] == 2
                and ciclo in b["ciclo"]]
        if anexo:
            exact = [b for b in cand if b["anexo"] == anexo]
            cand = exact or cand
        if not cand:
            print(f"!! sin anexo para {clave}", file=sys.stderr)
            continue
        out[clave] = cand[0]
    return out


def main():
    cat = json.load(open(CAT))
    anexos = carga_anexos()

    filas, sin_fuente, no_en_catalogo = [], [], []
    for m in cat["index"]:
        ck = m["ciclo_clave"]
        if ck in FUERA:
            sin_fuente.append((m, "curso de especialización: no lo modifican "
                                  "los Decretos 78/79/80 de 2024"))
            continue
        b = anexos.get(ck)
        if not b:
            sin_fuente.append((m, "ciclo sin anexo localizado"))
            continue
        fila = next((x for x in b["modulos"] if x["codigo"] == m["codigo"]), None)
        if fila is None:
            sin_fuente.append((m, f"código {m['codigo']} no aparece en el "
                                  f"anexo {b['anexo']} del Decreto {b['decreto']}"))
            continue
        h_dec = fila["horas"]
        sem_dec = [s for s in fila["semanales"] if s]
        # el módulo puede repartirse entre los dos cursos (proyecto intermodular)
        sem_dec_val = sum(sem_dec) if len(sem_dec) > 1 else (
            sem_dec[0] if sem_dec else None)
        filas.append({
            "key": m["key"], "codigo": m["codigo"], "abrev": m["abrev"],
            "nombre": m["nombre"], "ciclo": ck,
            "cat_horas": m["total_horas"], "cat_sem": m["horas_sem"],
            "dec_horas": h_dec, "dec_sem": sem_dec_val,
            "dec_sem_detalle": fila["semanales"],
            "decreto": b["decreto"], "anexo": b["anexo"],
            "nombre_decreto": fila["nombre"],
            "dif_horas": (h_dec - m["total_horas"]) if h_dec is not None else None,
            "dif_sem": (sem_dec_val - m["horas_sem"]) if sem_dec_val is not None else None,
        })

    # módulos del decreto que faltan en el catálogo
    codigos_cat = {(m["ciclo_clave"], m["codigo"]) for m in cat["index"]}
    for ck, b in anexos.items():
        for x in b["modulos"]:
            if x["codigo"] and (ck, x["codigo"]) not in codigos_cat:
                no_en_catalogo.append({
                    "ciclo": ck, "codigo": x["codigo"], "nombre": x["nombre"],
                    "horas": x["horas"], "semanales": x["semanales"],
                    "decreto": b["decreto"], "anexo": b["anexo"]})

    json.dump({"comparados": filas, "sin_fuente": [
        {"key": m["key"], "codigo": m["codigo"], "abrev": m["abrev"],
         "nombre": m["nombre"], "ciclo": m["ciclo_clave"],
         "cat_horas": m["total_horas"], "cat_sem": m["horas_sem"],
         "motivo": motivo} for m, motivo in sin_fuente],
        "faltan_en_catalogo": no_en_catalogo},
        sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

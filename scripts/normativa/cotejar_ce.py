#!/usr/bin/env python3
"""Coteja cada criterio de evaluación del catálogo con el texto del decreto.

Comprueba, uno a uno, que el texto de cada CE que guarda EvalFP aparece
literalmente en el anexo del decreto del que dice proceder. Es la comprobación que
sostiene la afirmación «RA y CE literales del DOCM» ante una inspección.

Cómo compara: normaliza ambos textos quitando todo lo que no sea letra o número y
pasando a minúsculas. Así son irrelevantes los guiones de partición de palabra que
mete el PDF («in - formación»), los dobles espacios, las comillas tipográficas y los
saltos de línea. Lo que sí detecta es una palabra distinta, una frase cambiada o un
criterio que no está en el decreto.

    python3 scripts/normativa/cotejar_ce.py            # resumen
    python3 scripts/normativa/cotejar_ce.py --detalle  # lista los que no casan
"""
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
NORM = RAIZ / "normativa"
CACHE = pathlib.Path("/tmp/cotejo_textos")

# ciclo_clave -> fichero de la fuente (PDF o texto ya extraído)
FUENTES = {
    "ASIR": NORM / "CLM_ASIR_200_2010.pdf",
    "SMR":  NORM / "CLM_SMR_107_2009.pdf",
    "DAM":  NORM / "CLM_DAM_252_2011.pdf",
    "DAW":  NORM / "CLM_DAW_230_2011.pdf",
    "AD":   NORM / "CLM_Decreto_41_2013_AD.pdf",
    "AF":   NORM / "CLM_Decreto_43_2013_AF.pdf",
    "CFGB": NORM / "CLM_CFGB_IO_80_2014.pdf",
    "SA":   NORM / "CLM_Decreto_83_2014_Servicios_Administrativos.pdf",
    "GA":   NORM / "texto" / "DOCM_GA_251_2011.txt",
    "CE_CIBER": NORM / "CLM_CE_CIBER_77_2022.pdf",
    "CE_IABD":  NORM / "CLM_CE_IABD_69_2022.pdf",
}

# Excepciones por código de módulo: su fuente no es el decreto de currículo del
# ciclo. El Itinerario personal para la empleabilidad de grado básico (3159) es el
# único transversal con RA y CE redactados por Castilla-La Mancha, en el Anexo II
# del Decreto 78/2024.
POR_CODIGO = {
    "3159": NORM / "texto" / "DOCM_78_2024.txt",
}

# Los transversales y el CE de Python se transcribieron en esta misma sesión desde
# su fuente; se cotejan aparte, contra el fichero de datos literales.
GENERADOS = ("_ipe1_", "_ipe2_", "_ing_", "_dig_", "_sost_", "_proy_", "ce_python")


def normaliza(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace("«", "").replace("»", "").replace("“", "").replace("”", "")
    return re.sub(r"[^0-9a-záéíóúüñ]+", "", t.lower())


def texto_fuente(ruta):
    CACHE.mkdir(exist_ok=True)
    if ruta.suffix == ".txt":
        crudo = ruta.read_text(encoding="utf-8", errors="replace")
    else:
        destino = CACHE / (ruta.stem + ".txt")
        if not destino.exists():
            subprocess.run(["pdftotext", "-enc", "UTF-8", "-nopgbrk",
                            str(ruta), str(destino)], check=True)
        crudo = destino.read_text(encoding="utf-8", errors="replace")
    return normaliza(crudo)


def main():
    detalle = "--detalle" in sys.argv
    cat = json.load(open(RAIZ / "renderer" / "modules_data.json"))
    fuentes = {}
    filas, fallos = [], []

    for key, mod in sorted(cat["modules"].items()):
        if any(g in key for g in GENERADOS):
            continue
        ck = mod["modulo"]["ciclo_clave"]
        cod = str(mod["modulo"]["codigo"])
        ruta = POR_CODIGO.get(cod) or FUENTES.get(ck)
        if ruta is None:
            continue
        if ruta not in fuentes:
            fuentes[ruta] = texto_fuente(ruta)
        texto = fuentes[ruta]

        total = malos = 0
        for ra, ces in (mod.get("ces") or {}).items():
            for ce in ces:
                total += 1
                if normaliza(ce["texto"]) not in texto:
                    malos += 1
                    fallos.append((ck, key, mod["modulo"]["codigo"], ra,
                                   ce["id"], ce["texto"]))
        filas.append((ck, key, mod["modulo"]["codigo"], total, malos))

    filas.sort()
    print(f"{'ciclo':10} {'módulo':24} {'cód':6} {'CE':>4} {'no casan':>9}")
    print("-" * 60)
    por_ciclo = {}
    for ck, key, cod, total, malos in filas:
        print(f"{ck:10} {key:24} {cod:6} {total:>4} {malos:>9}"
              + ("" if malos == 0 else "   <<<"))
        t, m = por_ciclo.get(ck, (0, 0))
        por_ciclo[ck] = (t + total, m + malos)

    print("\n" + "=" * 60)
    print(f"{'RESUMEN POR CICLO':30} {'CE':>8} {'no casan':>10}")
    for ck in sorted(por_ciclo):
        t, m = por_ciclo[ck]
        print(f"  {ck:28} {t:>8} {m:>10}" + ("   OK" if m == 0 else ""))
    T = sum(t for t, _ in por_ciclo.values())
    M = sum(m for _, m in por_ciclo.values())
    print(f"  {'TOTAL':28} {T:>8} {M:>10}")
    print(f"\nCoinciden literalmente: {T - M} de {T}  ({100 * (T - M) / T:.2f} %)")

    if detalle and fallos:
        print("\n" + "=" * 60)
        print("CRITERIOS QUE NO SE LOCALIZAN EN EL DECRETO\n")
        for ck, key, cod, ra, ceid, txt in fallos:
            print(f"[{ck} · {cod} · {ra}.{ceid}] {txt}")
    return 0 if M == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

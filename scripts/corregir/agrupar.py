#!/usr/bin/env python3
"""
agrupar.py — reparte las fotos de una tanda entre el alumnado, ANTES de gastar
una sola llamada a la IA.

Mezclar producciones de dos alumnos es el peor error posible al corregir, así que
aquí no se adivina nada en silencio: se propone un reparto, se marca lo que no
cuadra y la última palabra la tiene el profesorado.

Dos formas de agrupar, en este orden:
  1. Por prefijo del nombre del archivo: 01_p1.jpg, 01_p2.jpg, 02_p1.jpg…
     También valen «alumno01-1.jpg», «03 pagina 2.jpg» o «A07_2.png».
  2. Por número fijo de páginas: las N primeras son del primero, y así.

    python3 agrupar.py --imagenes a.jpg,b.jpg --paginas 2
    python3 agrupar.py --imagenes ... --modo prefijo
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

RE_PREFIJO = re.compile(r'^[A-Za-z]{0,3}[_\- ]?(\d{1,3})')


def _clave_orden(ruta: str):
    """Ordena de forma natural: 2 antes que 10."""
    nombre = Path(ruta).name
    trozos = re.split(r'(\d+)', nombre)
    return [int(t) if t.isdigit() else t.lower() for t in trozos]


def por_prefijo(imagenes: list[str]) -> tuple[dict[str, list[str]], list[str]]:
    grupos: dict[str, list[str]] = {}
    sueltas: list[str] = []
    for ruta in imagenes:
        m = RE_PREFIJO.match(Path(ruta).name)
        if not m:
            sueltas.append(ruta)
            continue
        grupos.setdefault(m.group(1).zfill(2), []).append(ruta)
    for k in grupos:
        grupos[k].sort(key=_clave_orden)
    return dict(sorted(grupos.items())), sueltas


def por_paginas(imagenes: list[str], paginas: int) -> tuple[dict[str, list[str]], list[str]]:
    ordenadas = sorted(imagenes, key=_clave_orden)
    grupos: dict[str, list[str]] = {}
    for i in range(0, len(ordenadas), paginas):
        grupos[str(len(grupos) + 1).zfill(2)] = ordenadas[i:i + paginas]
    sueltas = []
    # el último grupo incompleto se señala, no se descarta
    if grupos and len(list(grupos.values())[-1]) != paginas:
        sueltas = list(grupos.values())[-1]
    return grupos, sueltas


def agrupar(imagenes: list[str], modo: str = "auto", paginas: int = 0) -> dict:
    imagenes = [i for i in imagenes if i.strip()]
    grupos, sueltas = {}, []

    if modo in ("auto", "prefijo"):
        grupos, sueltas = por_prefijo(imagenes)
        # si el prefijo no reparte nada creíble, se cae a páginas fijas
        util = len(grupos) > 1 and not sueltas
        if modo == "auto" and not util and paginas:
            grupos, sueltas = por_paginas(imagenes, paginas)
    elif modo == "paginas":
        if paginas < 1:
            return {"error": "Indica cuántas páginas tiene cada examen."}
        grupos, sueltas = por_paginas(imagenes, paginas)

    if not grupos:
        return {"error": "No he sabido repartir las fotos. Dime cuántas páginas tiene cada examen."}

    esperadas = paginas or (max((len(v) for v in grupos.values()), default=0))
    filas = []
    for clave, rutas in grupos.items():
        aviso = ""
        if esperadas and len(rutas) != esperadas:
            aviso = f"esperaba {esperadas} páginas y veo {len(rutas)}"
        filas.append({"numero": clave, "paginas": len(rutas),
                      "archivos": [Path(r).name for r in rutas],
                      "rutas": rutas, "aviso": aviso})

    return {
        "modo": modo, "paginas_por_examen": esperadas,
        "total_examenes": len(filas), "total_fotos": len(imagenes),
        "grupos": filas,
        "incidencias": [f["numero"] for f in filas if f["aviso"]],
        "sin_agrupar": [Path(r).name for r in sueltas],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--imagenes', required=True)
    ap.add_argument('--modo', default='auto', choices=['auto', 'prefijo', 'paginas'])
    ap.add_argument('--paginas', type=int, default=0)
    args = ap.parse_args()
    print(json.dumps(agrupar([r.strip() for r in args.imagenes.split(',')],
                             args.modo, args.paginas), ensure_ascii=False))


if __name__ == '__main__':
    main()

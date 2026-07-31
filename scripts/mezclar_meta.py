#!/usr/bin/env python3
"""
mezclar_meta.py — une el texto **literal** del DOCM con los metadatos didácticos
(siglas, curso, horas semanales, nombre de UT, evaluación e instrumentos) y deja
un JSON por módulo listo para gen_modulo.py.

    python3 scripts/mezclar_meta.py --crudo normativa/docm_json/_crudo_GA.json \
                                    --meta  normativa/docm_json/_meta_GA.json \
                                    --salida normativa/docm_json

El fichero de metadatos es una lista de objetos con la misma forma que espera
gen_modulo.py, pero **sin** enunciados ni criterios: esos se toman siempre del
decreto, emparejando por código de módulo y por orden de RA.
"""
import argparse
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--crudo', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--salida', required=True)
    ap.add_argument('--prefijo', default='')
    args = ap.parse_args()

    crudo = {m['codigo']: m for m in json.load(open(args.crudo, encoding='utf-8'))}
    metas = json.load(open(args.meta, encoding='utf-8'))
    fallos = 0

    for meta in metas:
        cod = meta['modulo']['codigo']
        if cod not in crudo:
            print('! %s no aparece en el decreto' % cod)
            fallos += 1
            continue
        oficial = crudo[cod]
        if len(meta['ras']) != len(oficial['ras']):
            print('! %s: el decreto tiene %d RA y los metadatos %d'
                  % (cod, len(oficial['ras']), len(meta['ras'])))
            fallos += 1
            continue
        for destino, fuente in zip(meta['ras'], oficial['ras']):
            destino['enunciado'] = fuente['enunciado']
            destino['ces'] = fuente['ces']
        meta['modulo'].setdefault('nombre', oficial['nombre'])
        ruta = os.path.join(args.salida, '%s%s.json' % (args.prefijo, cod))
        json.dump(meta, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('OK %-5s %-6s %d RA · %d CE · %s'
              % (cod, meta['modulo']['abrev'], len(meta['ras']),
                 sum(len(r['ces']) for r in meta['ras']), os.path.basename(ruta)))
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()

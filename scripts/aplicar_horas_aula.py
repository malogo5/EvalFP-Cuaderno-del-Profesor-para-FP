#!/usr/bin/env python3
"""
aplicar_horas_aula.py — separa, en los ciclos de Grado Básico, la duración oficial
del módulo (que incluye la fase de formación en empresa) de las horas que se
imparten realmente en el aula, que son las que reparten las UT.

    python3 scripts/aplicar_horas_aula.py --aplicar

De dónde salen las semanas: los ámbitos del ciclo no tienen fase de empresa, así que
su duración dividida entre sus horas semanales da las semanas lectivas reales.
    1º · Ciencias aplicadas I 120 h ÷ 4 h/sem = 30 · Comunicación y CCSS I 120 ÷ 4 = 30
    2º · Ciencias aplicadas II 152 h ÷ 6 h/sem ≈ 25 · Comunicación y CCSS II 152 ÷ 6 ≈ 25
Por tanto horas de aula = horas semanales × 30 (1º) o × 25 (2º).
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from corregir_catalogo import campo, fijar, reparto_entero  # noqa: E402

MODS = os.path.join(ROOT, 'modules')
SEMANAS = {'1': 30, '2': 25}
CICLOS = ('CFGB', 'SA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    args = ap.parse_args()
    tocados = 0

    for fichero in sorted(os.listdir(MODS)):
        if not fichero.endswith('_data.py'):
            continue
        ruta = os.path.join(MODS, fichero)
        texto = open(ruta, encoding='utf-8').read()
        if campo(texto, 'ciclo_clave') not in CICLOS:
            continue
        curso = str(campo(texto, 'curso') or '')
        semanas = SEMANAS.get(curso[:1])
        hsem = campo(texto, 'horas_sem')
        total = campo(texto, 'total_horas')
        if not (semanas and hsem and total):
            print('! %s: faltan curso u horas semanales' % fichero)
            continue

        aula = hsem * semanas
        if aula >= total:
            print('=  %-24s %3d h · sin fase de empresa (%d h/sem × %d sem)'
                  % (fichero, total, hsem, semanas))
            continue
        if campo(texto, 'horas_aula') == aula:
            continue

        if 'horas_aula' in texto:
            texto = fijar(texto, 'horas_aula', aula)
        else:
            texto = texto.replace('"decreto":',
                                  '"horas_aula":%d,\n    "decreto":' % aula, 1)
        m = re.search(r'UTS\s*=\s*\[(.*?)\n\]', texto, re.S)
        pesos = [int(x) for x in re.findall(r'"horas"\s*:\s*(\d+)', m.group(1))]
        nuevos = reparto_entero(pesos, aula)
        it = iter(nuevos)
        bloque = re.sub(r'"horas"\s*:\s*\d+', lambda _: '"horas":%d' % next(it), m.group(1))
        texto = texto[:m.start(1)] + bloque + texto[m.end(1):]

        tocados += 1
        print('OK %-24s oficial %3d h = %3d h de aula (%d h/sem × %d sem) + %3d h en empresa · UT %s → %s'
              % (fichero, total, aula, hsem, semanas, total - aula, pesos, nuevos))
        if args.aplicar:
            open(ruta, 'w', encoding='utf-8').write(texto)

    print('\n%d módulos %s' % (tocados, 'actualizados' if args.aplicar else 'por actualizar (usa --aplicar)'))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
corregir_catalogo.py — alinea los módulos ya existentes con la normativa vigente
de Castilla-La Mancha: código oficial del módulo, duración total, horas semanales
y curso, según la tabla «Duración y distribución horaria semanal» que publica la
Consejería de Educación para cada ciclo (normativa/oficial_informatica.json).

Las horas de las UT se reescalan de forma proporcional para que sigan sumando
exactamente la duración del módulo. Los RA y CE **no se tocan**.

    python3 scripts/corregir_catalogo.py            # muestra lo que haría
    python3 scripts/corregir_catalogo.py --aplicar  # escribe los cambios
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MODS = os.path.join(ROOT, 'modules')
TABLA = os.path.join(ROOT, '..', 'normativa', 'oficial_informatica.json')


def reparto_entero(pesos, total):
    suma = sum(pesos) or 1
    brutos = [p * total / suma for p in pesos]
    base = [max(1, int(b)) for b in brutos]
    # ajusta hasta cuadrar el total
    while sum(base) > total:
        i = base.index(max(base))
        base[i] -= 1
    orden = sorted(range(len(pesos)), key=lambda i: brutos[i] - base[i], reverse=True)
    i = 0
    while sum(base) < total:
        base[orden[i % len(orden)]] += 1
        i += 1
    return base


def campo(texto, clave):
    m = re.search(r'"%s"\s*:\s*("([^"]*)"|\d+)' % clave, texto)
    if not m:
        return None
    return m.group(2) if m.group(2) is not None else int(m.group(1))


def fijar(texto, clave, valor):
    if isinstance(valor, str):
        nuevo = '"%s":"%s"' % (clave, valor)
    else:
        nuevo = '"%s":%d' % (clave, valor)
    pat = re.compile(r'"%s"\s*:\s*(?:"[^"]*"|\d+)' % clave)
    if pat.search(texto):
        return pat.sub(nuevo, texto, count=1)
    return texto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    args = ap.parse_args()

    oficial = json.load(open(TABLA, encoding='utf-8'))
    tocados = 0

    for fichero in sorted(os.listdir(MODS)):
        if not fichero.endswith('_data.py'):
            continue
        ruta = os.path.join(MODS, fichero)
        texto = open(ruta, encoding='utf-8').read()
        ck = campo(texto, 'ciclo_clave')
        ab = campo(texto, 'abrev')
        if ck not in oficial or ab not in oficial.get(ck, {}):
            continue
        cod, horas, hsem, curso = oficial[ck][ab]

        cambios = []
        if campo(texto, 'codigo') != cod:
            cambios.append('código %s → %s' % (campo(texto, 'codigo'), cod))
            texto = fijar(texto, 'codigo', cod)
        if campo(texto, 'horas_sem') != hsem:
            cambios.append('h/sem %s → %s' % (campo(texto, 'horas_sem'), hsem))
            texto = fijar(texto, 'horas_sem', hsem)
        if campo(texto, 'curso') != curso:
            cambios.append('curso %r → %r' % (campo(texto, 'curso'), curso))
            texto = fijar(texto, 'curso', curso)

        total_viejo = campo(texto, 'total_horas')
        if total_viejo != horas:
            cambios.append('duración %s → %s h' % (total_viejo, horas))
            texto = fijar(texto, 'total_horas', horas)
            # reescala las horas de las UT
            m = re.search(r'UTS\s*=\s*\[(.*?)\n\]', texto, re.S)
            if m:
                bloque = m.group(1)
                valores = [int(x) for x in re.findall(r'"horas"\s*:\s*(\d+)', bloque)]
                if valores:
                    nuevos = reparto_entero(valores, horas)
                    it = iter(nuevos)
                    bloque2 = re.sub(r'"horas"\s*:\s*\d+',
                                     lambda _: '"horas":%d' % next(it), bloque)
                    texto = texto[:m.start(1)] + bloque2 + texto[m.end(1):]
                    cambios.append('UT %s → %s' % (valores, nuevos))

        if cambios:
            tocados += 1
            print('%-26s %-5s %-6s %s' % (fichero, ck, ab, ' · '.join(cambios)))
            if args.aplicar:
                open(ruta, 'w', encoding='utf-8').write(texto)

    print('\n%d módulos %s' % (tocados, 'corregidos' if args.aplicar else 'por corregir (usa --aplicar)'))


if __name__ == '__main__':
    main()

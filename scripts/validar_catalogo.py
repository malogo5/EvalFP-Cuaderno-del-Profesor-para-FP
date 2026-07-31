#!/usr/bin/env python3
"""
validar_catalogo.py — comprueba la coherencia de todo el catálogo prebakeado.

    python3 scripts/validar_catalogo.py

Verifica, módulo a módulo:
  1. las horas de las UT suman exactamente la duración del módulo
  2. las ponderaciones de los RA suman 100 %
  3. cada RA tiene criterios de evaluación
  4. todos los CE están asignados a alguna UT (ninguno suelto)
  5. no hay UT repetidas ni CE asignados dos veces
  6. EVAL_RAS cubre todos los RA y no usa evaluaciones fuera de eval_count
  7. cada RA tiene instrumentos de evaluación asignados
  8. dentro de cada ciclo no se repiten código ni siglas
"""
import collections
import json
import os
import sys

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renderer', 'modules_data.json')


def main():
    d = json.load(open(RUTA, encoding='utf-8'))
    mods = d['modules']
    fallos = []
    avisos = []

    for clave, m in sorted(mods.items()):
        mm = m['modulo']
        et = '%s/%s' % (mm.get('ciclo_clave'), mm.get('abrev'))

        # en los ciclos con formación en empresa las UT reparten sólo las horas de aula
        referencia = mm.get('horas_aula') or mm.get('total_horas')
        horas = sum(u.get('horas', 0) for u in m['uts'])
        if horas != referencia:
            fallos.append('%s · las UT suman %d h y las de aula son %s' % (et, horas, referencia))
        if mm.get('horas_aula') and mm['horas_aula'] > (mm.get('total_horas') or 0):
            fallos.append('%s · horas de aula (%s) mayores que la duración oficial (%s)'
                          % (et, mm['horas_aula'], mm.get('total_horas')))

        pond = sum(r.get('pond', 0) for r in m['ras'])
        if pond != 100:
            fallos.append('%s · las ponderaciones de RA suman %s %%' % (et, pond))

        ces = m.get('ces', {})
        for r in m['ras']:
            if not ces.get(r['id']):
                fallos.append('%s · %s sin criterios de evaluación' % (et, r['id']))
            if r['id'] not in (m.get('ra_instrumentos') or {}):
                fallos.append('%s · %s sin instrumentos de evaluación' % (et, r['id']))

        asignados = collections.Counter()
        uts_vistas = collections.Counter()
        for a in m['asignaciones']:
            uts_vistas[a['ut']] += 1
            for ce in a['ces']:
                asignados['%s|%s' % (a['ra'], ce)] += 1
        for ut, n in uts_vistas.items():
            if n > 1:
                avisos.append('%s · la UT %s trabaja criterios de %d RA distintos' % (et, ut, n))
        for k, n in asignados.items():
            if n > 1:
                avisos.append('%s · el criterio %s se trabaja en %d UT' % (et, k, n))

        # cada RA debe tener al menos una actividad con la que calificarse
        con_actividad = {a.get('ra_id') for a in m.get('actividades', []) if a.get('ra_id')}
        for r in m['ras']:
            if r['id'] not in con_actividad:
                fallos.append('%s · %s no tiene ninguna actividad de partida' % (et, r['id']))
        for ra, lista in ces.items():
            for ce in lista:
                if asignados.get('%s|%s' % (ra, ce['id']), 0) == 0:
                    fallos.append('%s · %s %s no está asignado a ninguna UT' % (et, ra, ce['id']))

        ev = m.get('eval_ras') or {}
        cubiertos = {x for v in ev.values() for x in v}
        for r in m['ras']:
            if r['id'] not in cubiertos:
                fallos.append('%s · %s no está en ninguna evaluación' % (et, r['id']))
        n_ev = int(mm.get('eval_count', 3))
        for k in ev:
            if not (1 <= int(k) <= n_ev):
                fallos.append('%s · evaluación %s fuera de rango (eval_count=%d)' % (et, k, n_ev))

    ciclos = collections.defaultdict(list)
    for m in d['index']:
        ciclos[m['ciclo_clave']].append(m)
    for ck, lista in ciclos.items():
        for campo in ('codigo', 'abrev'):
            c = collections.Counter(x.get(campo) for x in lista)
            for k, n in c.items():
                if n > 1:
                    fallos.append('%s · %s repetido %d veces: %s' % (ck, campo, n, k))

    print('módulos verificados: %d' % len(mods))
    print('ciclos: %s' % ', '.join('%s(%d)' % (k, len(v)) for k, v in sorted(ciclos.items())))
    print('horas totales del catálogo: %d h · RA: %d · CE: %d'
          % (sum(x.get('total_horas', 0) for x in d['index']),
             sum(len(m['ras']) for m in mods.values()),
             sum(len(v) for m in mods.values() for v in (m.get('ces') or {}).values())))
    if avisos:
        print('\n%d avisos (revisables, no bloquean):' % len(avisos))
        for a in avisos:
            print('  ·', a)
    if fallos:
        print('\n%d PROBLEMAS:' % len(fallos))
        for f in fallos:
            print('  ✗', f)
        sys.exit(1)
    print('\n✅ sin errores')


if __name__ == '__main__':
    main()

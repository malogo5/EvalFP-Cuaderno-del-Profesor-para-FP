#!/usr/bin/env python3
"""
regenerar_desde_clm.py — rehace los módulos ya existentes con los RA y CE
**literales del decreto de currículo de Castilla-La Mancha**, sustituyendo el
texto adaptado del Real Decreto que tenían.

    python3 scripts/regenerar_desde_clm.py --ciclos SMR ASIR CFGB DAM DAW

Conserva del módulo anterior todo lo que no es normativo: sigla, código, curso,
horas semanales, duración, número de evaluaciones y los instrumentos por RA.
El nombre de cada UT se reutiliza cuando el RA del decreto dice esencialmente lo
mismo que el que había (parecido >= 0.8); si no, se deriva del propio enunciado
del RA para que el nombre nunca contradiga a la normativa.

Genera el JSON de entrada en normativa/docm_json/ y llama a gen_modulo.py, de
modo que las horas de las UT y las ponderaciones vuelven a cuadrar solas.
"""
import argparse
import difflib
import importlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import gen_modulo  # noqa: E402

CRUDO = {'SMR': 'SMR', 'ASIR': 'ASIR', 'CFGB': 'CFGBIO', 'DAM': 'DAM', 'DAW': 'DAW',
         'CE_CIBER': 'CE_CIBER', 'CE_IABD': 'CE_IABD'}
DECRETO = {
    'SMR':  'Decreto 107/2009, de 04/08/2009, currículo del ciclo de Sistemas Microinformáticos y '
            'Redes en Castilla-La Mancha (DOCM, NID 2009/11413) · RA y CE literales del Anexo I',
    'ASIR': 'Decreto 200/2010, de 03/08/2010, currículo del ciclo de Administración de Sistemas '
            'Informáticos en Red en Castilla-La Mancha (DOCM, NID 2010/13389) · RA y CE literales del Anexo I',
    'CFGB': 'Decreto 80/2014, de 01/08/2014, currículo del ciclo de Formación Profesional Básica de '
            'Informática de Oficina en Castilla-La Mancha (DOCM, NID 2014/10283) · RA y CE literales del Anexo II',
    'DAM':  'Decreto 252/2011, de 12/08/2011, currículo del ciclo de Desarrollo de Aplicaciones '
            'Multiplataforma en Castilla-La Mancha (DOCM, NID 2011/11916) · RA y CE literales del Anexo I',
    'CE_CIBER': 'Decreto 77/2022, de 12/07/2022, currículo del Curso de Especialización en '
                'Ciberseguridad en Entornos de las Tecnologías de la Información en Castilla-La Mancha '
                '(DOCM) · RA y CE literales del Anexo II',
    'CE_IABD': 'Decreto 69/2022, de 12/07/2022, currículo del Curso de Especialización en '
               'Inteligencia Artificial y Big Data en Castilla-La Mancha (DOCM, NID 2022/6683) '
               '· RA y CE literales del Anexo II',
    'DAW':  'Decreto 230/2011, de 28/07/2011, currículo del ciclo de Desarrollo de Aplicaciones Web '
            'en Castilla-La Mancha (DOCM, NID 2011/11276) · RA y CE literales del Anexo I',
}


def nombre_ut(enunciado):
    """Nombre corto de UT derivado del propio enunciado del RA."""
    t = re.split(r',\s|\s+(?:analizando|aplicando|identificando|describiendo|relacionándol|'
                 r'reconociendo|utilizando|valorando|interpretando|siguiendo|justificando|'
                 r'evaluando|verificando|asegurando|teniendo|atendiendo|seleccionando)', enunciado)[0]
    t = t.strip(' .;:')
    if len(t) > 72:
        t = t[:69].rsplit(' ', 1)[0] + '…'
    return t[0].upper() + t[1:] if t else enunciado[:60]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ciclos', nargs='+', default=list(CRUDO))
    ap.add_argument('--salida', default=os.path.join(ROOT, '..', 'normativa', 'docm_json'))
    args = ap.parse_args()

    crudos = {}
    for ck in args.ciclos:
        ruta = os.path.join(args.salida, '_crudo_%s.json' % CRUDO[ck])
        crudos[ck] = {m['codigo']: m for m in json.load(open(ruta, encoding='utf-8'))}

    hechos, saltados = [], []
    for fichero in sorted(os.listdir(os.path.join(ROOT, 'modules'))):
        if not fichero.endswith('_data.py'):
            continue
        base = fichero[:-8]
        mod = importlib.import_module('modules.' + fichero[:-3])
        ck = mod.MODULO.get('ciclo_clave')
        if ck not in crudos:
            continue
        oficial = crudos[ck].get(mod.MODULO.get('codigo'))
        if not oficial:
            saltados.append((mod.MODULO['abrev'], 'no aparece en el decreto'))
            continue

        viejos = mod.RAS
        instr_viejos = getattr(mod, 'RA_INSTRUMENTOS', {}) or {}
        uts_por_ra = {}
        for ut_id, ra_id, _ in mod.ASIGNACIONES:
            uts_por_ra.setdefault(ra_id, ut_id)
        nombre_por_ra, tags_por_ra = {}, {}
        for ra_id, ut_id in uts_por_ra.items():
            ut = next((u for u in mod.UTS if u['id'] == ut_id), {})
            nombre_por_ra[ra_id] = ut.get('nombre', '')
            tags_por_ra[ra_id] = ut.get('tags', '')

        ras, reutilizadas = [], 0
        for i, r in enumerate(oficial['ras']):
            viejo = viejos[i] if i < len(viejos) else None
            ut, tags = nombre_ut(r['enunciado']), ''
            if viejo:
                parecido = difflib.SequenceMatcher(
                    None, viejo['nombre'].lower(), r['enunciado'].lower()).ratio()
                if parecido >= 0.8 and nombre_por_ra.get(viejo['id']):
                    ut = nombre_por_ra[viejo['id']]
                    tags = tags_por_ra.get(viejo['id'], '')
                    reutilizadas += 1
            ras.append({
                'ut': ut, 'tags': tags,
                'instrumentos': (instr_viejos.get('RA%d' % (i + 1)) or ['examen', 'practica']),
                'enunciado': r['enunciado'], 'ces': r['ces'],
            })

        m = dict(mod.MODULO)
        m['decreto'] = DECRETO[ck]
        cfg = {'archivo': base, 'modulo': m, 'ras': ras, 'dual_ra': getattr(mod, 'DUAL_RA', None)}
        ruta_json = os.path.join(args.salida, '%s_%s.json' % (ck, m['codigo']))
        json.dump(cfg, open(ruta_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

        codigo, errores, info = gen_modulo.generar(cfg)
        open(os.path.join(ROOT, 'modules', fichero), 'w', encoding='utf-8').write(codigo)
        hechos.append((ck, m['abrev'], len(viejos), info['ras'],
                       sum(len(v) for v in mod.CES.values()), info['ces'], reutilizadas, errores))

    print('%-5s %-6s %-11s %-11s %-9s %s' % ('ciclo', 'sigla', 'RA antes→CLM', 'CE antes→CLM',
                                             'UT reutil.', 'avisos'))
    for ck, ab, ra0, ra1, ce0, ce1, reut, errores in hechos:
        print('%-5s %-6s %5d → %-4d %5d → %-4d %6d/%-3d %s'
              % (ck, ab, ra0, ra1, ce0, ce1, reut, ra1, '; '.join(errores) or 'ok'))
    print('\n%d módulos regenerados desde el decreto de CLM' % len(hechos))
    for ab, motivo in saltados:
        print('  · %s omitido: %s' % (ab, motivo))


if __name__ == '__main__':
    main()

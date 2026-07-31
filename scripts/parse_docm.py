#!/usr/bin/env python3
"""
parse_docm.py — extrae los módulos profesionales (RA y CE **literales**) del texto
de un decreto de currículo del DOCM.

    python3 scripts/parse_docm.py normativa/texto/DOCM_GA_251_2011.txt --json normativa/docm_json/_crudo_GA.json

Trabaja sobre el texto plano extraído del PDF oficial. No inventa ni reescribe nada:
solo localiza los bloques, corta por los marcadores del alfabeto español y deshace
el guionado de fin de línea que introduce el PDF ("pre - senciales" -> "presenciales").
"""
import argparse
import json
import re
import unicodedata

# Marcadores tal y como los usa el DOCM: alfabeto español, con dígrafos, y luego dobles
ALFABETO = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "ll", "m",
            "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
MARCADORES = ALFABETO + [x + x for x in ALFABETO]

CORTES = ("Duración:", "Contenidos:", "Orientaciones pedagógicas", "Módulo Profesional:",
          "Módulo profesional:", "Anexo", "ANEXO")


def limpiar(t):
    t = ' '.join(str(t).split())
    t = re.sub(r'<<PAG\d+>>', ' ', t)
    # cabeceras y pies del boletín intercalados
    t = re.sub(r'AÑO [IVXL]+\s+Núm\.\s*\d+\s+\d+ de \w+ de \d{4}', ' ', t)
    t = re.sub(r'\bNúm\.\s*\d+\b', ' ', t)
    t = re.sub(r'\bAÑO [IVXL]+\b', ' ', t)
    t = re.sub(r'\b\d+ de (?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|'
               r'septiembre|octubre|noviembre|diciembre) de \d{4}\b', ' ', t)
    t = re.sub(r'(?<![\d,.])\d{5}(?![\d,.])', ' ', t)  # nº de página del boletín
    # Partición de palabra a final de línea. En el texto que da pdf.js aparece como
    # «pre -  senciales»: guion con UN espacio delante y DOS o más detrás. Un guion con
    # un solo espacio a cada lado es un inciso del propio decreto («consumibles - tintas
    # y líquidos - relacionándoles…») y no debe unirse.
    t = re.sub(r'([a-záéíóúüñ])\s-\s{2,}([a-záéíóúüñ])', r'\1\2', t)
    t = re.sub(r'\s+([,.;:])', r'\1', t)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()


def sin_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')


def trocear_modulos(texto):
    """Devuelve [(nombre, codigo, bloque)] por cada módulo profesional del decreto."""
    # entre el código y los RA algunos decretos intercalan los créditos ECTS
    pat = re.compile(r'M[óo]dulo\s+[Pp]rofesional:\s*(.+?)\.?\s*C[óo]digo:\s*([A-Z]{0,4}\d{4})\.?\s*'
                     r'(?:[^.]{0,60}\.\s*)?Resultados\s+de\s+[Aa]prendizaje', re.S)
    marcas = list(pat.finditer(texto))
    salida = []
    for i, m in enumerate(marcas):
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
        bloque = texto[m.end():fin]
        # el bloque de RA acaba donde empieza duración, contenidos u orientaciones
        for c in ('Duración:', 'Contenidos:', 'Contenidos básicos:', 'Orientaciones pedagógicas'):
            p = bloque.find(c)
            if p > 200:
                bloque = bloque[:p]
        nombre = limpiar(m.group(1))
        nombre = re.split(r'\s*Equivalencia en cr[ée]ditos|\s*Duraci[óo]n', nombre)[0].strip(' .')
        salida.append((nombre, m.group(2), bloque))
    return salida


def trocear_ras(bloque):
    """Corta el bloque de un módulo en sus RA siguiendo la numeración 1., 2., 3., ..."""
    tramos, pos, n = [], 0, 1
    while True:
        # el punto tras el número falta en algunos PDF del DOCM ("4 Determina...")
        pat = re.compile(r'(?<![\d.,])%d\.?\s+(?=[A-ZÁÉÍÓÚÑ][a-záéíóúüñ])' % n)
        elegido = None
        for m in pat.finditer(bloque, pos):
            # un RA de verdad va seguido de sus criterios de evaluación
            if re.search(r'Criterios\s+de\s+[Ee]valuaci[óo]n', bloque[m.end():m.end() + 900]):
                elegido = m
                break
        if not elegido:
            break
        tramos.append((n, elegido.start(), elegido.end()))
        pos = elegido.end()
        n += 1
    ras = []
    for i, (num, ini_marca, ini) in enumerate(tramos):
        fin = tramos[i + 1][0 + 1] if i + 1 < len(tramos) else len(bloque)
        ras.append((num, bloque[ini:fin]))
    return ras


def trocear_ces(tramo):
    """Separa enunciado del RA y sus CE, siguiendo el orden de los marcadores."""
    m = re.search(r'Criterios\s+de\s+[Ee]valuaci[óo]n:?\s*', tramo)
    if not m:
        return limpiar(tramo), []
    enunciado = limpiar(tramo[:m.start()])
    resto = tramo[m.end():]

    # recorta el tramo en cuanto aparece una sección posterior
    corte = len(resto)
    for c in CORTES:
        p = resto.find(c)
        if p != -1:
            corte = min(corte, p)
    resto = resto[:corte]

    posiciones, pos, fallos = [], 0, 0
    for marca in MARCADORES:
        p = resto.find(marca + ')', pos)
        # el marcador tiene que ir precedido de espacio o principio de tramo
        while p > 0 and not resto[p - 1].isspace():
            p = resto.find(marca + ')', p + 1)
        if p == -1:
            # algún decreto se salta una letra (p. ej. va de e) a g) en el 80/2014);
            # se toleran hasta dos huecos antes de dar por terminada la lista
            fallos += 1
            if fallos > 2 or not posiciones:
                break
            continue
        fallos = 0
        posiciones.append((marca, p))
        pos = p + len(marca) + 1

    ces = []
    for i, (marca, p) in enumerate(posiciones):
        ini = p + len(marca) + 1
        fin = posiciones[i + 1][1] if i + 1 < len(posiciones) else len(resto)
        texto = limpiar(resto[ini:fin])
        if texto:
            ces.append(texto)
    return enunciado, ces


def horas_por_codigo(texto):
    """Lee la tabla de duraciones del anexo (código ... horas)."""
    horas = {}
    for m in re.finditer(r'\b(0\d{3}|\d{4})\b[^\d\n]{5,90}?\b(\d{2,3})\s*(?:horas)?\b', texto):
        pass
    return horas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichero')
    ap.add_argument('--json', required=True)
    ap.add_argument('--solo', nargs='*', help='códigos a incluir')
    args = ap.parse_args()

    texto = open(args.fichero, encoding='utf-8').read()
    modulos = []
    for nombre, codigo, bloque in trocear_modulos(texto):
        if args.solo and codigo not in args.solo:
            continue
        ras = []
        for num, tramo in trocear_ras(bloque):
            enun, ces = trocear_ces(tramo)
            if not ces:
                continue
            ras.append({'ra': num, 'enunciado': enun, 'ces': ces})
        modulos.append({'codigo': codigo, 'nombre': nombre, 'ras': ras})

    json.dump(modulos, open(args.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print('%-6s %-58s %3s RA  %3s CE   reparto' % ('cód', 'módulo', '', ''))
    for m in modulos:
        print('%-6s %-58s %3d     %3d     %s'
              % (m['codigo'], m['nombre'][:58], len(m['ras']),
                 sum(len(r['ces']) for r in m['ras']),
                 '/'.join(str(len(r['ces'])) for r in m['ras'])))
    avisos = []
    for m in modulos:
        for r in m['ras']:
            for c in r['ces']:
                if len(c) > 700:
                    avisos.append((m['codigo'], 'RA%d' % r['ra'], 'CE muy largo (%d)' % len(c), c[:90]))
                if len(c) < 25:
                    avisos.append((m['codigo'], 'RA%d' % r['ra'], 'CE muy corto', c))
                if re.search(r'\b\d{5}\b', c):
                    avisos.append((m['codigo'], 'RA%d' % r['ra'], 'posible nº de página', c[:90]))
    print('\navisos: %d' % len(avisos))
    for a in avisos[:20]:
        print('  ', ' · '.join(a))


if __name__ == '__main__':
    main()

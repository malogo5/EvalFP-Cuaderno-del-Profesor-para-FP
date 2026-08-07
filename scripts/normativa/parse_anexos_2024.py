#!/usr/bin/env python3
"""Extrae los anexos de duración y distribución horaria semanal de los
Decretos 78/2024, 79/2024 y 80/2024 de Castilla-La Mancha
(DOCM núm. 218, de 11 de noviembre de 2024).

Estrategia: anclar en la línea de cabecera "Duración y distribución horaria
semanal ... del ciclo formativo ..." y leer hasta la fila "Total", que fija
las posiciones de columna reales de cada tabla.

Salida: JSON [{decreto, anexo, ciclo, n_cursos, modulos[], total}]
"""
import json
import re
import sys

ANEXO_RE = re.compile(
    r"^\s*Anexo\s+((?:I{1,3}|IV|VI{0,3}|IX|X|V)[-.]?\s*[ABC]?[-.]?\s*"
    r"\d*\.?\s*\d*\s*º?)\s*$")
CAB_RE = re.compile(r"Duración y distribución horaria semanal")
PAGINA_RE = re.compile(r"AÑO\s+XLIII\s+Núm\.\s+\d+")
TOTAL_RE = re.compile(r"^\s*Total\b")
NUM_RE = re.compile(r"\d+")
CODIGO_RE = re.compile(r"^\s*(\d{4})\s*[.,]?\s*")
# vocabulario que sólo aparece en las cabeceras de las tablas; una línea
# compuesta EXCLUSIVAMENTE por estas palabras es cabecera, no un módulo.
VOCAB_CAB = re.compile(
    r"(Distribución|Módulos?|Ámbitos?|Horas?|Semanales?|Totales?|Cursos?|"
    r"[123]\s*º|\bde\b|\bdel\b|\by\b|\bs\b)",
    re.IGNORECASE)


def es_ruido(l):
    s = l.strip()
    if not s:
        return True
    if PAGINA_RE.search(s):
        return True
    if re.fullmatch(r"\d{4,6}", s):          # número de página suelto
        return True
    if re.match(r"^\s*\d{4}\s*[.,]", s):     # fila real: empieza por código
        return False
    return not VOCAB_CAB.sub("", s).strip(" /·.-")


def toks(linea):
    return [(int(m.group(0)), m.start()) for m in NUM_RE.finditer(linea)]


def parse_fichero(path, decreto):
    lineas = open(path, encoding="utf-8").read().split("\n")
    bloques, anexo_actual = [], None
    i = 0
    while i < len(lineas):
        m = ANEXO_RE.match(lineas[i])
        if m:
            anexo_actual = re.sub(r"\s+", " ", m.group(1)).strip()
            i += 1
            continue
        if not CAB_RE.search(lineas[i]):
            i += 1
            continue

        # --- cabecera: puede ocupar varias líneas hasta el nombre del ciclo ---
        cab, j = [lineas[i].strip()], i + 1
        while j < len(lineas) and j < i + 6:
            s = lineas[j].strip()
            if not s or es_ruido(lineas[j]) or CODIGO_RE.match(lineas[j]):
                break
            cab.append(s)
            j += 1
            if cab[-1].endswith("."):
                break
        cabtxt = re.sub(r"\s+", " ", " ".join(cab))
        cm = re.search(r"ciclo formativo(?:\s+de)?\s+(.*)$", cabtxt)
        ciclo = (cm.group(1) if cm else cabtxt).strip(" .")
        ciclo = re.sub(r"\s*/\s*a\b", "/a", ciclo)

        # --- cuerpo: hasta la fila Total ---
        crudo, k = [], j
        while k < len(lineas):
            if TOTAL_RE.match(lineas[k]):
                crudo.append(lineas[k])
                k += 1
                break
            if CAB_RE.search(lineas[k]) or ANEXO_RE.match(lineas[k]):
                break
            crudo.append(lineas[k])
            k += 1
        if not crudo or not TOTAL_RE.match(crudo[-1]):
            i = j
            continue

        total_toks = toks(crudo[-1])
        if len(total_toks) < 2:
            i = k
            continue
        col0 = total_toks[0][1]              # x de "Horas totales"
        cols_sem = [p for _, p in total_toks[1:]]
        zona = col0 - 8                      # margen izquierdo de la zona numérica

        filas, buf = [], ""
        for raw in crudo[:-1]:
            if es_ruido(raw):
                continue
            t = [(v, p) for v, p in toks(raw) if p >= zona]
            texto_izq = raw[:t[0][1]].strip() if t else raw.strip()
            if t:
                nombre = (buf + " " + texto_izq).strip()
                filas.append({"nombre": re.sub(r"\s+", " ", nombre), "cols": t})
                buf = ""
            else:
                s = raw.strip()
                if CODIGO_RE.match(s) or s in ("Tutoría", "Optatividad") or buf:
                    buf = (buf + " " + s).strip()
                elif filas:                  # continuación posterior del nombre
                    filas[-1]["nombre"] = re.sub(
                        r"\s+", " ", filas[-1]["nombre"] + " " + s)
                else:
                    buf = s

        bloques.append({"decreto": decreto, "anexo": anexo_actual,
                        "ciclo": ciclo, "filas": filas,
                        "col0": col0, "cols_sem": cols_sem,
                        "total": [v for v, _ in total_toks]})
        i = k
    return bloques


def columnas_semanales(b):
    """Devuelve la función posición->índice de curso.

    Las columnas de la fila Total no siempre coinciden en x con las de los
    datos (los números van centrados y varían de anchura), así que se agrupan
    las posiciones observadas en los propios datos y, si salen tantos grupos
    como cursos, se usan esos; si no, se cae a la fila Total.
    """
    n = len(b["cols_sem"])
    obs = sorted(p for f in b["filas"] for _, p in f["cols"][1:])
    grupos = []
    for p in obs:
        if grupos and p - grupos[-1][-1] <= 5:
            grupos[-1].append(p)
        else:
            grupos.append([p])
    if len(grupos) == n:
        centros = [sum(g) / len(g) for g in grupos]
    else:
        centros = [float(x) for x in b["cols_sem"]]
    return lambda p: min(range(n), key=lambda i: abs(centros[i] - p))


def normaliza(b):
    asigna = columnas_semanales(b)
    n = len(b["cols_sem"])
    mods = []
    for f in b["filas"]:
        nombre, cols = f["nombre"], f["cols"]
        cm = CODIGO_RE.match(nombre)
        codigo = cm.group(1) if cm else None
        if cm:
            nombre = nombre[cm.end():]
        nombre = nombre.strip(" .,·")
        horas = cols[0][0] if cols else None
        sem = [None] * n
        for v, p in cols[1:]:
            sem[asigna(p)] = v
        mods.append({"codigo": codigo, "nombre": nombre, "horas": horas,
                     "semanales": sem})
    return {"decreto": b["decreto"], "anexo": b["anexo"], "ciclo": b["ciclo"],
            "n_cursos": n, "modulos": mods, "total": b["total"]}


def valida(b):
    """Cuadre aritmético contra la fila Total del propio decreto."""
    s = sum(m["horas"] or 0 for m in b["modulos"])
    sems = [sum(m["semanales"][i] or 0 for m in b["modulos"])
            for i in range(b["n_cursos"])]
    ok = s == b["total"][0] and sems == b["total"][1:]
    return ok, s, sems


if __name__ == "__main__":
    salida = []
    for path, dec in [("/tmp/dec/d78.txt", "78/2024"),
                      ("/tmp/dec/d79.txt", "79/2024"),
                      ("/tmp/dec/d80.txt", "80/2024")]:
        for b in parse_fichero(path, dec):
            n = normaliza(b)
            ok, s, sems = valida(n)
            n["_cuadra"] = ok
            n["_suma"] = [s] + sems
            salida.append(n)
    json.dump(salida, sys.stdout, ensure_ascii=False, indent=1)

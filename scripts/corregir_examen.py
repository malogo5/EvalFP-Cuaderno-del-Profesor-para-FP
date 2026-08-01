#!/usr/bin/env python3
"""
corregir_examen.py — corrige exámenes manuscritos a partir de fotos, contra los
criterios de evaluación literales del decreto.

    python3 corregir_examen.py --modulo iso_data --ra RA3 \
        --alumno "Carrasco Nieto, Marta" --numero 03 \
        --imagenes foto1.jpg,foto2.jpg --salida ~/Documents/EvalFP/correcciones

Sigue los principios del prompt maestro de corrección de ProfeLibre:
  · La rúbrica —aquí, los criterios de evaluación del RA— es la única referencia.
  · Un examen es de UN alumno y se corrige aislado: nunca se mezclan producciones.
  · Nada de inventar: lo que no se lee es [ilegible] y lo dudoso, [dudoso].
  · Anonimización por número de lista salvo que se pida lo contrario.
  · Las fotos que se entregan son SIEMPRE las originales en color; el preprocesado
    en gris y alto contraste es solo para leer mejor y no sale en la entrega.
  · Feedback específico y accionable, sin frases vacías y sin infantilizar.
  · Transcripción mínima: se cita al alumno solo cuando la cita es la evidencia.

Devuelve por pantalla un resumen compacto y deja en la carpeta de salida:
  correccion_<alumno>.json   la corrección estructurada, criterio a criterio
  correccion_<alumno>.md     el documento de entrega
  <foto>_corregida.jpg       las fotos originales con las marcas superpuestas
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_asistente import (  # noqa: E402
    IAAsistente, MODELO_CLAUDE_CALIDAD, MODELO_OPENAI_CALIDAD, TIMEOUT_CALIDAD,
    _agrupar_ces_por_ra, _cargar_modulo, _emit_ia_code, _parse_opts,
)

AQUI = Path(__file__).resolve().parent
PREPROCESAR = AQUI / "corregir" / "preprocesar_imagen.py"
ANOTAR = AQUI / "corregir" / "anotar_examen.py"

MAX_IMAGENES = 12
MAX_BYTES_IMG = 5 * 1024 * 1024


# ─── Preprocesado ────────────────────────────────────────────────────────────

def _recortar_cabecera(ruta: str, destino: Path, porcentaje: int) -> str:
    """Corta la franja superior de la foto, donde va el nombre escrito a mano.

    Anonimizar el identificador no anonimiza la imagen: en la hoja está el nombre
    del alumno de su puño y letra. Esto recorta solo la copia que se envía al
    proveedor de IA; la entrega sigue usando la foto original completa.
    """
    magick = shutil.which("magick") or shutil.which("convert")
    if not magick:
        return ruta
    out = destino / f"sincabecera_{Path(ruta).name}"
    try:
        subprocess.run(
            [magick, ruta, "-gravity", "north", "-chop", f"0x{porcentaje}%", str(out)],
            check=True, capture_output=True, timeout=120)
        return str(out) if out.exists() else ruta
    except Exception:
        return ruta


def _preprocesar(rutas: list[str], destino: Path, recorte: int = 0) -> list[str]:
    """Gris, contraste y enfoque: solo para leer. La entrega usa el original."""
    destino.mkdir(parents=True, exist_ok=True)
    salidas = []
    for i, r in enumerate(rutas, 1):
        origen = _recortar_cabecera(r, destino, recorte) if recorte > 0 else r
        out = destino / f"lectura_{i:02d}.jpg"
        try:
            subprocess.run([sys.executable, str(PREPROCESAR), origen, str(out)],
                           check=True, capture_output=True, timeout=120)
            salidas.append(str(out) if out.exists() else origen)
        except Exception:
            salidas.append(origen)     # sin ImageMagick se lee el original
    return salidas


def _b64(ruta: str) -> tuple[str, str]:
    datos = Path(ruta).read_bytes()
    if len(datos) > MAX_BYTES_IMG:
        _emit_ia_code("IMAGEN_GRANDE",
                      f"La imagen {Path(ruta).name} pesa más de 5 MB. Redúcela antes de corregir.")
    ext = Path(ruta).suffix.lower()
    tipo = "image/png" if ext == ".png" else "image/jpeg"
    return tipo, base64.b64encode(datos).decode("ascii")


# ─── Llamada con visión ──────────────────────────────────────────────────────

def _llamar_vision(ia: IAAsistente, system: str, user: str, imagenes: list[str]) -> str:
    prov = getattr(ia, "_proveedor", "demo")
    if prov == "demo":
        return json.dumps({
            "alumno": "(demo)",
            "legibilidad": "buena",
            "preguntas": [{"numero": 1, "transcripcion": "(modo demo)", "valoracion": "correcta",
                           "criterios": [], "puntos": 1, "sobre": 1,
                           "comentario": "Texto de ejemplo: configura una clave de API para corregir de verdad."}],
            "puntos_fuertes": "(demo)", "aspecto_mejora": "(demo)",
            "feedforward": ["(demo)"], "nota": 5.0,
            "anotaciones": [],
        }, ensure_ascii=False)

    if prov == "claude":
        bloques = []
        for ruta in imagenes:
            tipo, dato = _b64(ruta)
            bloques.append({"type": "image",
                            "source": {"type": "base64", "media_type": tipo, "data": dato}})
        bloques.append({"type": "text", "text": user})
        msg = ia._cliente.messages.create(
            model=MODELO_CLAUDE_CALIDAD, max_tokens=4000, temperature=0.2,
            system=system, messages=[{"role": "user", "content": bloques}],
            timeout=TIMEOUT_CALIDAD,
        )
        return msg.content[0].text

    if prov == "openai":
        contenido = []
        for ruta in imagenes:
            tipo, dato = _b64(ruta)
            contenido.append({"type": "image_url",
                              "image_url": {"url": f"data:{tipo};base64,{dato}"}})
        contenido.append({"type": "text", "text": user})
        resp = ia._cliente.chat.completions.create(
            model=MODELO_OPENAI_CALIDAD, max_tokens=4000, temperature=0.2,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": contenido}],
            timeout=TIMEOUT_CALIDAD,
        )
        return resp.choices[0].message.content

    _emit_ia_code("ERROR_RED", f"Proveedor sin visión: {prov}")
    return ""


# ─── Prompts ─────────────────────────────────────────────────────────────────

SYSTEM = textwrap.dedent("""\
    Actúas a la vez como especialista en la materia del módulo de Formación Profesional
    que se te indica, corrector riguroso con la rúbrica y experto en evaluación
    competencial. Corriges un examen manuscrito a partir de fotografías.

    PRINCIPIOS INNEGOCIABLES

    1. Los criterios de evaluación que se te dan son tu ÚNICA referencia. No añades
       criterios propios ni valoras nada que no esté en ellos.
    2. El examen pertenece a UN alumno o alumna. No mencionas ni comparas con nadie más.
    3. No inventas. Lo que no puedas leer con confianza razonable va como [ilegible];
       lo que se lea pero admita dos lecturas, [dudoso]. Distingues «no respondido»
       (en blanco) de «no legible» (escrito pero indescifrable): no es lo mismo.
    4. Transcripción mínima: citas literalmente al alumno solo cuando la cita es la
       evidencia de un acierto o de un error. El resto lo parafraseas.
    5. Feedback específico y accionable. Prohibidas las frases vacías: «muy bien»,
       «sigue así», «ánimo», «buen trabajo en general». Nada de infantilizar.
    6. Riguroso pero justo: si el razonamiento es correcto y falla el cálculo, lo
       reconoces; si el resultado es correcto con proceso incorrecto, lo señalas.

    CÓMO LEER LETRA MANUSCRITA
    · El contexto manda sobre los píxeles: usa lo que sabes del módulo para
      desambiguar trazos dudosos.
    · Lee en bloques, no letra a letra.
    · Ojo con los pares clásicos en español: u/v, a/o cerradas, 1/l, y con los
      subíndices y superíndices, que se escriben pequeños.

    FORMATO DE SALIDA
    Respondes ÚNICAMENTE con un objeto JSON válido, sin texto antes ni después y sin
    vallas de código. Este esquema exacto:

    {
      "alumno": "identificador que se te ha dado",
      "legibilidad": "buena | regular | mala",
      "preguntas": [
        {"numero": 1,
         "transcripcion": "solo lo imprescindible, o [ilegible] / [en blanco]",
         "valoracion": "correcta | parcial | incorrecta | en blanco | ilegible",
         "criterios": ["CE1", "CE4"],
         "puntos": 1.5, "sobre": 2,
         "comentario": "qué falla o qué acierta, y la forma correcta"}
      ],
      "criterios_alcanzados": ["CE1"],
      "criterios_no_alcanzados": ["CE4"],
      "puntos_fuertes": "2-3 frases específicas de ESTE examen",
      "aspecto_mejora": "UN solo aspecto, con el ejemplo concreto de su examen y la forma correcta",
      "feedforward": ["2 a 4 acciones concretas y realizables esta semana"],
      "nota": 6.5,
      "dudas_para_el_docente": ["lo que no has podido resolver y afecta a la nota"],
      "anotaciones": [
        {"pagina": 1, "y_percent": 35, "type": "correct|incorrect|partial|comment",
         "text": "texto de la marca, o null si es solo un visto"}
      ]
    }

    Para las anotaciones: y_percent es la altura donde cae la respuesta en la foto,
    de 0 (arriba) a 100 (abajo). Deja al menos 5 puntos entre marcas para que no se
    solapen y prioriza señalar los errores por encima de los vistos.
""")


def _prompt_usuario(mod, ra, ces, alumno, n_imgs, baremo, enunciado, ajustes=""):
    ces_txt = "\n".join(f"  CE{i}. {c}" for i, c in enumerate(ces, 1)) or "  (sin criterios)"
    extra = ""
    if enunciado:
        extra += f"\n\nENUNCIADO / SOLUCIONARIO QUE APORTA EL DOCENTE\n{enunciado[:4000]}"
    if baremo:
        extra += f"\n\nBAREMO\n{baremo[:1000]}"
    if ajustes:
        extra += ("\n\nAJUSTES DE CRITERIO ACORDADOS CON EL DOCENTE\n"
                  "Se han aplicado ya a los exámenes anteriores de esta tanda; aplícalos también aquí "
                  "para que todo el grupo se corrija con la misma vara de medir:\n"
                  f"{ajustes[:1200]}")
    return textwrap.dedent(f"""\
        Módulo: {mod['nombre']} ({mod.get('codigo','')}) — {mod.get('ciclo','')} {mod.get('curso','')}
        Resultado de aprendizaje evaluado: {ra['id']} — {ra.get('nombre','')}

        CRITERIOS DE EVALUACIÓN (rúbrica única; numéralos así en tu respuesta)
        {ces_txt}{extra}

        Vas a corregir el examen de {alumno}. Son {n_imgs} página(s), todas suyas y en orden.

        Corrige pregunta a pregunta contra esos criterios, decide qué criterios queda
        acreditados y cuáles no, y propón una nota sobre 10 con su desglose implícito
        en los puntos por pregunta. Devuelve solo el JSON del esquema.
    """)


# ─── Salidas ─────────────────────────────────────────────────────────────────

def _json_de(texto: str) -> dict:
    t = (texto or "").strip()
    if t.startswith("```"):
        t = t.split("```")[1] if len(t.split("```")) > 1 else t
        t = t[t.find("{"):] if "{" in t else t
    ini, fin = t.find("{"), t.rfind("}")
    if ini == -1 or fin == -1:
        _emit_ia_code("RESPUESTA_NO_VALIDA",
                      "El modelo no ha devuelto una corrección en el formato esperado.")
    try:
        return json.loads(t[ini:fin + 1])
    except json.JSONDecodeError as e:
        _emit_ia_code("RESPUESTA_NO_VALIDA", f"No he podido leer la corrección: {e}")
    return {}


def _markdown(datos: dict, mod, ra, alumno: str, imagenes: list[str]) -> str:
    L = [f"# Corrección · {alumno}", "",
         f"**{mod['nombre']}** ({mod.get('codigo','')}) · {mod.get('ciclo','')} {mod.get('curso','')}  ",
         f"**{ra['id']}** — {ra.get('nombre','')}  ",
         f"**Nota propuesta: {datos.get('nota','—')}/10** · legibilidad de la letra: {datos.get('legibilidad','—')}",
         "", "> Corrección asistida por IA sobre los criterios de evaluación del decreto.",
         "> Revísala antes de entregarla: la nota es una propuesta, no una calificación.", "",
         "## Pregunta a pregunta", ""]
    for p in datos.get("preguntas", []):
        crit = ", ".join(p.get("criterios", []))
        L.append(f"**{p.get('numero','·')}. {p.get('valoracion','')}** "
                 f"— {p.get('puntos','?')}/{p.get('sobre','?')} puntos"
                 + (f" · criterios {crit}" if crit else ""))
        if p.get("transcripcion"):
            L.append(f"> {p['transcripcion']}")
        if p.get("comentario"):
            L.append(f"{p['comentario']}")
        L.append("")
    alc, noalc = datos.get("criterios_alcanzados", []), datos.get("criterios_no_alcanzados", [])
    L += ["## Criterios de evaluación", "",
          f"- Acreditados: {', '.join(alc) or '—'}",
          f"- Sin acreditar: {', '.join(noalc) or '—'}", "",
          "## Qué has hecho bien", "", datos.get("puntos_fuertes", "—"), "",
          "## Qué mejorar", "", datos.get("aspecto_mejora", "—"), "",
          "## Para la próxima", ""]
    L += [f"{i}. {a}" for i, a in enumerate(datos.get("feedforward", []), 1)] or ["—"]
    dudas = datos.get("dudas_para_el_docente") or []
    if dudas:
        L += ["", "## Dudas que debes resolver tú", ""] + [f"- {d}" for d in dudas]
    if imagenes:
        L += ["", "## Examen corregido", ""] + [f"![Página {i}]({Path(p).name})"
                                                for i, p in enumerate(imagenes, 1)]
    return "\n".join(L) + "\n"


def _anotar(datos: dict, originales: list[str], salida: Path, alumno: str, mod) -> list[str]:
    """Marca sobre las fotos ORIGINALES en color, nunca sobre las preprocesadas."""
    anots = datos.get("anotaciones") or []
    if not anots or not ANOTAR.exists():
        return []
    paginas = []
    for i in range(1, len(originales) + 1):
        dela = [{"y_percent": a.get("y_percent", 50), "type": a.get("type", "comment"),
                 "text": a.get("text")} for a in anots if int(a.get("pagina", 1)) == i]
        paginas.append({"page_number": i, "annotations": dela})
    doc = {"student_name": alumno, "student_group": mod.get("curso", ""),
           "subject": mod.get("nombre", ""), "total_grade": f"{datos.get('nota','—')} / 10",
           "pages": paginas}
    tmp = salida / "_anotaciones.json"
    tmp.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    try:
        subprocess.run([sys.executable, str(ANOTAR), ",".join(originales), str(tmp), str(salida)],
                       check=True, capture_output=True, timeout=180)
    except Exception as e:
        print(f"[aviso] no he podido anotar las fotos: {e}", file=sys.stderr)
        return []
    finally:
        tmp.unlink(missing_ok=True)
    return sorted(str(p) for p in salida.glob("*corregida*"))


# ─── Comando ─────────────────────────────────────────────────────────────────

def main(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--ra", "--alumno", "--numero", "--imagenes",
                              "--salida", "--proveedor", "--anonimizar", "--baremo", "--recorte-cabecera",
                              "--enunciado", "--ajustes"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        _emit_ia_code("RA_NO_ENCONTRADO", f"El RA '{ra_id}' no existe en este módulo.")

    rutas = [r.strip() for r in str(opts.get("--imagenes", "")).split(",") if r.strip()]
    rutas = [r for r in rutas if Path(r).is_file()]
    if not rutas:
        _emit_ia_code("SIN_IMAGENES", "No he recibido ninguna foto del examen.")
    if len(rutas) > MAX_IMAGENES:
        _emit_ia_code("DEMASIADAS_IMAGENES",
                      f"Máximo {MAX_IMAGENES} páginas por examen; me has pasado {len(rutas)}.")

    anonimizar = str(opts.get("--anonimizar", "true")).lower() not in ("0", "false", "no", "off")
    numero = str(opts.get("--numero", "") or "").strip()
    nombre_real = opts.get("--alumno", "Alumno")
    alumno = f"Alumno_{numero.zfill(2)}" if (anonimizar and numero) else (
        "Alumno_01" if anonimizar else nombre_real)

    salida = Path(opts.get("--salida") or (AQUI.parent / "correcciones"))
    salida = salida / f"{mod.MODULO['abrev']}_{ra_id}"
    salida.mkdir(parents=True, exist_ok=True)

    ces = _agrupar_ces_por_ra(mod).get(ra_id, [])
    ia = IAAsistente(proveedor=opts.get("--proveedor", "auto"))

    with tempfile.TemporaryDirectory(prefix="evalfp-lectura-") as tmp:
        # Recorte de la cabecera para no enviar el nombre manuscrito (privacidad)
        try:
            recorte = int(opts.get("--recorte-cabecera") or 0)
        except ValueError:
            recorte = 0
        recorte = max(0, min(40, recorte))
        legibles = _preprocesar(rutas, Path(tmp), recorte)
        print(f"Leyendo {len(legibles)} página(s) de {alumno}…", flush=True)
        bruto = _llamar_vision(
            ia, SYSTEM,
            _prompt_usuario(mod.MODULO, ra, ces, alumno, len(legibles),
                            opts.get("--baremo"), opts.get("--enunciado"),
                            opts.get("--ajustes", "")),
            legibles)

    datos = _json_de(bruto)
    datos["alumno"] = alumno

    base = alumno.replace(" ", "_").replace(",", "")
    (salida / f"correccion_{base}.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    anotadas = _anotar(datos, rutas, salida, alumno, mod.MODULO)
    (salida / f"correccion_{base}.md").write_text(
        _markdown(datos, mod.MODULO, ra, alumno, anotadas), encoding="utf-8")

    # Resumen compacto en pantalla
    print(f"\n{'='*60}")
    print(f"CORRECCIÓN · {alumno} · {ra_id}")
    print(f"{'='*60}\n")
    print(f"Nota propuesta: {datos.get('nota','—')}/10 · letra {datos.get('legibilidad','—')}")
    for p in datos.get("preguntas", []):
        print(f"  {p.get('numero','·')}. {p.get('valoracion','')} "
              f"({p.get('puntos','?')}/{p.get('sobre','?')}) {str(p.get('comentario',''))[:90]}")
    print(f"\nFuerte  · {datos.get('puntos_fuertes','—')}")
    print(f"Mejorar · {datos.get('aspecto_mejora','—')}")
    for a in datos.get("feedforward", []):
        print(f"  → {a}")
    for d in datos.get("dudas_para_el_docente") or []:
        print(f"  ⚠ {d}")
    if anotadas:
        print(f"\nFotos corregidas: {len(anotadas)}")
    print(f"Guardado en: {salida}")
    print("\nNOTA_PROPUESTA:" + str(datos.get("nota", "")))


if __name__ == "__main__":
    if not sys.argv[1:] or sys.argv[1] in ("-h", "--help", "--ayuda"):
        print(__doc__)
        sys.exit(0)
    main(sys.argv[1:])

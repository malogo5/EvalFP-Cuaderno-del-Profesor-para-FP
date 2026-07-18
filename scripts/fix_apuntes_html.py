#!/usr/bin/env python3
"""
Fix rápido para apuntes ya generados — aplica los mismos parches que _limpiar_html_ia():

  Fix 1: <ul class="list-disc"> cuyas <li> empiezan por a)/b)/c)/d)
          → elimina list-disc para que las opciones de test no tengan bullet visual.

  Fix 2: <pre/div class="code-block"> dentro de <p>
          → extrae el bloque fuera del párrafo (HTML inválido que causa texto flotante).

Uso:
  python3 fix_apuntes_html.py                          # busca en ~/Documents/EvalFP/apuntes
  python3 fix_apuntes_html.py /ruta/personalizada      # carpeta alternativa
"""

import re
import sys
from pathlib import Path

# ── Fix 1 ──────────────────────────────────────────────────────────────────────
def _fix_test_ul(m: re.Match) -> str:
    ul = m.group(0)
    if not re.search(r'<li[^>]*>\s*[a-dA-D]\)', ul):
        return ul
    ul = re.sub(r'\blist-disc\b\s*', '', ul)
    ul = re.sub(r'(<ul\b[^>]*?)(>)',
                r'\1 style="list-style:none;padding-left:0"\2', ul, count=1)
    return ul

# ── Fix 2 ──────────────────────────────────────────────────────────────────────
_code_in_p = re.compile(
    r'<p([^>]*)>'
    r'((?:(?!<(?:pre|div)\b)[\s\S])*?)'
    r'(<(?:pre|div)\b[^>]*class="[^"]*code-block[^"]*"[^>]*>'
    r'[\s\S]*?</(?:pre|div)>)'
    r'([\s\S]*?)</p>',
    re.DOTALL | re.IGNORECASE
)

def _split_code_from_p(m: re.Match) -> str:
    p_attrs, before, code_block, after = m.group(1), m.group(2), m.group(3), m.group(4)
    result = ''
    if before.strip():
        result += f'<p{p_attrs}>{before.strip()}</p>'
    result += code_block
    if after.strip():
        result += f'<p{p_attrs}>{after.strip()}</p>'
    return result

# ── Función de extracción: el HTML real está en JSON dentro de <script> ────────
def _extract_sections_json(html: str):
    """Devuelve (json_str, start_pos, end_pos) del array sections: [...].
    Itera TODOS los <script> porque los primeros son CDN externos (vacíos)."""
    for script_m in re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE):
        script    = script_m.group(1)
        sec_start = script.find('sections: [')
        if sec_start < 0:
            continue  # Este script no tiene sections, probar el siguiente
        # Buscar el corchete de cierre balanceado
        depth = 0
        i = sec_start + len('sections: ')
        start_i = i
        while i < len(script):
            c = script[i]
            if c in '[{':
                depth += 1
            elif c in ']}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        # Posiciones en el HTML original
        json_in_script = script[start_i:i + 1]
        html_offset = script_m.start(1)
        abs_start = html_offset + start_i
        abs_end   = html_offset + i + 1
        return json_in_script, abs_start, abs_end
    return None  # Ningún script tenía sections:


def fix_html_file(fpath: Path) -> tuple[bool, list]:
    import json

    html = fpath.read_text(encoding='utf-8')
    result = _extract_sections_json(html)
    if result is None:
        return False, ["  ⚠️  No se encontró el array sections: en el script"]

    json_str, abs_start, abs_end = result
    try:
        sections = json.loads(json_str.replace('\\/', '/'))
    except json.JSONDecodeError as e:
        return False, [f"  ⚠️  JSON parse error: {e}"]

    changes = []
    for sec in sections:
        sec_html = sec.get('html', '')
        if not sec_html:
            continue

        original = sec_html

        # Fix 1: listas de test sin bullets
        sec_html = re.sub(
            r'<ul\b[^>]*>.*?</ul>',
            _fix_test_ul,
            sec_html,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Fix 2: code-block fuera de <p> (dos pasadas)
        for _ in range(2):
            sec_html = _code_in_p.sub(_split_code_from_p, sec_html)

        if sec_html != original:
            changes.append(f"  • [{sec.get('id','?')}] modificado")
            sec['html'] = sec_html

    if not changes:
        return False, []

    # Re-serializar el JSON y sustituir en el HTML
    new_json = json.dumps(sections, ensure_ascii=False, indent=2).replace('</', '\\/')
    new_html = html[:abs_start] + new_json + html[abs_end:]
    fpath.write_text(new_html, encoding='utf-8')
    return True, changes


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / 'Documents' / 'EvalFP' / 'apuntes'
    if not base.exists():
        print(f"❌  Carpeta no encontrada: {base}")
        sys.exit(1)

    files = sorted(base.rglob('index.html'))
    print(f"Archivos encontrados: {len(files)}  en  {base}\n")

    total_ok = 0
    for fpath in files:
        rel = fpath.relative_to(base)
        changed, msgs = fix_html_file(fpath)
        if changed:
            print(f"✅  {rel}")
            for m in msgs:
                print(m)
            total_ok += 1
        elif msgs:
            print(f"⚠️  {rel}")
            for m in msgs:
                print(m)
        else:
            print(f"—   {rel}  (sin cambios)")

    print(f"\nTotal modificados: {total_ok}/{len(files)}")


if __name__ == '__main__':
    main()

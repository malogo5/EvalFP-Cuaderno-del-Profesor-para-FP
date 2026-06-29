#!/usr/bin/env python3
"""
EvalFP — Generador de Apuntes HTML (integración con CLAUDE.md)
===============================================================
Genera un index.html autocontenido por cada UT del módulo,
siguiendo la plantilla Vue 3 del proyecto Generador de Apuntes.

Con ANTHROPIC_API_KEY: genera contenido pedagógico real via Claude.
Sin API key: genera un skeleton HTML editable con secciones estructuradas.

Uso:
    python build_apuntes.py                        # todas las UTs del módulo por defecto
    python build_apuntes.py --modulo par_data      # módulo PAR
    python build_apuntes.py --modulo iso_data --ut UT1   # una sola UT
    python build_apuntes.py --salida ../apuntes    # directorio de salida personalizado
    python build_apuntes.py --ayuda

Salida por defecto:
    apuntes/04-FP/{MOD}/{CURSO}/{ut-kebab}/index.html
"""

from __future__ import annotations

import importlib
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

# ─── Helpers ─────────────────────────────────────────────────────────────────

def kebab(text: str) -> str:
    """Convierte 'Administración de software base' → 'administracion-de-software-base'."""
    # Normalizar acentos
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
        "ñ": "n", "Ñ": "n", "ü": "u", "Ü": "u",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Minúsculas, solo alfanum y guion
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def apunte_path(mod, ut: dict, base: Path) -> Path:
    """Ruta de salida: base/04-FP/{ABREV}/{CURSO-KEBAB}/{ut-kebab}/index.html"""
    curso_k = kebab(mod.MODULO.get("curso", "1-asir"))
    ut_k    = kebab(ut["nombre"])
    return base / "04-FP" / mod.MODULO["abrev"] / curso_k / ut_k / "index.html"


def apunte_rel_path(mod, ut: dict) -> str:
    """
    Ruta relativa desde src/EvalFP.xlsx hasta el index.html del apunte.
    Ej: '../apuntes/04-FP/ISO/1-asir/instalacion-software-libre/index.html'
    """
    curso_k = kebab(mod.MODULO.get("curso", "1-asir"))
    ut_k    = kebab(ut["nombre"])
    return f"../apuntes/04-FP/{mod.MODULO['abrev']}/{curso_k}/{ut_k}/index.html"


def _ces_por_ra_modulo(mod) -> dict[str, list[str]]:
    ces: dict[str, list[str]] = {}
    for _ut, ra_id, celist in mod.ASIGNACIONES:
        ces.setdefault(ra_id, [])
        for ce in celist:
            if ce not in ces[ra_id]:
                ces[ra_id].append(ce)
    return ces


def _ras_de_ut(mod, ut_id: str) -> list[str]:
    """RAs asociados a una UT (en orden de aparición en ASIGNACIONES)."""
    vistos = []
    for uid, ra_id, _ in mod.ASIGNACIONES:
        if uid == ut_id and ra_id not in vistos:
            vistos.append(ra_id)
    return vistos

# ─── Plantilla HTML ──────────────────────────────────────────────────────────

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {ut_label} · {abrev} · {curso}</title>
<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --sidebar-width: 300px;
    --header-height: 72px;
    --bg-main: #ffffff;
    --bg-subtle: #f8fafc;
    --border: #e2e8f0;
    --text-main: #0f172a;
    --text-muted: #64748b;
  }}
  [v-cloak] {{ display: none; }}
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg-subtle); }}
  code, .code-block {{ font-family: 'JetBrains Mono', monospace; }}
  .sidebar {{ width: var(--sidebar-width); min-height: 100vh; background: #0f172a;
              position: fixed; left: 0; top: 0; overflow-y: auto; z-index: 40;
              transition: transform .3s; }}
  .sidebar-hidden {{ transform: translateX(-100%); }}
  .main-content {{ margin-left: var(--sidebar-width); transition: margin .3s; }}
  .main-content.full {{ margin-left: 0; }}
  .header {{ height: var(--header-height); background: white; border-bottom: 1px solid var(--border);
             position: sticky; top: 0; z-index: 30; display: flex; align-items: center;
             padding: 0 1.5rem; gap: 1rem; }}
  .nav-item {{ display: block; padding: .5rem 1rem; border-radius: .5rem; color: #94a3b8;
               font-size: .8rem; font-weight: 500; cursor: pointer; transition: all .2s;
               text-decoration: none; margin-bottom: .25rem; }}
  .nav-item:hover, .nav-item.active {{ background: #1e293b; color: white; }}
  .nav-item.active {{ color: #60a5fa; }}
  .callout {{ border-radius: .75rem; padding: 1rem 1.25rem; border-left: 4px solid; }}
  .callout-info    {{ background: #eff6ff; border-color: #3b82f6; }}
  .callout-warning {{ background: #fffbeb; border-color: #f59e0b; }}
  .callout-success {{ background: #f0fdf4; border-color: #22c55e; }}
  .callout-danger  {{ background: #fef2f2; border-color: #ef4444; }}
  .callout-title   {{ font-weight: 700; font-size: .9rem; margin-bottom: .35rem; }}
  .callout-info .callout-title    {{ color: #1d4ed8; }}
  .callout-warning .callout-title {{ color: #b45309; }}
  .callout-success .callout-title {{ color: #15803d; }}
  .callout-danger .callout-title  {{ color: #b91c1c; }}
  .code-block {{ background: #1e293b; color: #e2e8f0; padding: 1rem 1.25rem;
                border-radius: .75rem; font-size: .82rem; line-height: 1.6;
                overflow-x: auto; }}
  .code-block .comment {{ color: #64748b; }}
  .code-block .keyword {{ color: #7dd3fc; }}
  .code-block .string  {{ color: #86efac; }}
  .code-block .number  {{ color: #fca5a5; }}
  @media print {{
    .sidebar, .header, .no-print {{ display: none !important; }}
    .main-content {{ margin-left: 0 !important; }}
    body {{ background: white; }}
  }}
  @media (max-width: 1023px) {{
    .main-content {{ margin-left: 0; }}
  }}
</style>
</head>
<body>
<div id="app" v-cloak>

  <!-- Sidebar -->
  <aside class="sidebar" :class="{{ 'sidebar-hidden': !sidebarOpen }}">
    <div class="p-5">
      <div class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{abrev}</div>
      <div class="text-white font-bold text-sm mb-1">{ut_label}</div>
      <div class="text-slate-400 text-xs mb-5">{modulo_nombre}</div>
      <nav>
        <a v-for="s in sections" :key="s.id"
           class="nav-item"
           :class="{{ active: activeSection === s.id }}"
           @click="activeSection = s.id; $nextTick(() => document.getElementById(s.id)?.scrollIntoView({{behavior:'smooth'}}))"
        >{{{{ s.icon }}}} {{{{ s.title }}}}</a>
      </nav>
      <div class="mt-6 p-3 bg-slate-800 rounded-xl text-xs text-slate-400">
        <div class="font-bold text-slate-300 mb-1">Autora</div>
        <div>{autora}</div>
        <div class="mt-2 font-bold text-slate-300 mb-1">Licencia</div>
        <div>CC BY 4.0</div>
      </div>
    </div>
  </aside>

  <!-- Header -->
  <header class="header" :class="{{ 'full': !sidebarOpen }}" style="padding-left: calc(var(--sidebar-width) + 1.5rem)" :style="{{ 'padding-left': sidebarOpen ? '' : '1.5rem' }}">
    <button @click="sidebarOpen = !sidebarOpen"
            class="p-2 rounded-lg hover:bg-slate-100 text-slate-500 no-print">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>
    <div class="flex-1">
      <h1 class="font-bold text-slate-800 text-sm">{title}</h1>
      <p class="text-xs text-slate-400">{ut_label} · {abrev} · {curso} · {anno}</p>
    </div>
    <button onclick="window.print()" class="no-print flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-1.5 rounded-lg">
      📄 Imprimir / PDF
    </button>
  </header>

  <!-- CC BY banner -->
  <div class="main-content" :class="{{ 'full': !sidebarOpen }}">
    <div class="bg-green-50 border-b border-green-200 px-6 py-2 text-xs text-green-700 font-medium no-print">
      📄 Licencia <strong>CC BY 4.0</strong> — Puedes compartir y adaptar este material citando a la autora.
    </div>

    <!-- Contenido -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <section v-for="s in sections" :key="s.id" :id="s.id" class="mb-16 scroll-mt-24">
        <div v-html="s.html"></div>
      </section>
    </main>

    <footer class="text-center py-8 text-xs text-slate-400 border-t border-slate-200">
      {modulo_nombre} · {ut_label} · {autora} · CC BY 4.0 · {anno}
    </footer>
  </div>

</div>
<script>
const {{ createApp }} = Vue;
createApp({{
  data() {{
    return {{
      activeSection: 'inicio',
      sidebarOpen: window.innerWidth >= 1024,
      sections: {sections_json}
    }};
  }},
  mounted() {{
    document.title = '{title} — {ut_label} · {abrev} · {curso}';
    const obs = new IntersectionObserver(e => {{
      e.forEach(x => {{ if (x.isIntersecting) this.activeSection = x.target.id; }});
    }}, {{ rootMargin: '-20% 0px -70% 0px' }});
    this.$nextTick(() => {{
      document.querySelectorAll('section[id]').forEach(s => obs.observe(s));
    }});
  }}
}}).mount('#app');
</script>
</body>
</html>"""

# ─── Secciones demo (sin API) ─────────────────────────────────────────────────

def _secciones_demo(mod, ut: dict) -> list[dict]:
    """Genera secciones estructuradas con contenido de ejemplo."""
    ras = _ras_de_ut(mod, ut["id"])
    ras_str = " · ".join(ras)
    nombre = ut["nombre"]
    tags   = ut.get("tags", "")

    portada = f"""
<section id="inicio" class="text-center py-8 mb-4 flex flex-col justify-center min-h-[55vh]">
  <div class="inline-block bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full mb-4 mx-auto">FP Grado Superior · ASIR</div>
  <h1 class="text-4xl font-extrabold text-slate-900 leading-tight mb-2">{nombre}</h1>
  <p class="text-base text-slate-400 font-medium max-w-2xl mx-auto italic mb-6">{ut['id']} · {mod.MODULO['abrev']} — {mod.MODULO['nombre']} · {mod.MODULO['curso']} · {mod.MODULO['anno']}</p>
  <div class="grid grid-cols-2 gap-3 text-left max-w-sm mx-auto mb-6">
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Autora</span>
      <span class="text-sm font-bold text-slate-800">Isabel López</span>
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">RAs</span>
      <span class="text-sm font-bold text-slate-800">{ras_str}</span>
    </div>
  </div>
  <div class="inline-flex items-center gap-2 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5 mx-auto">
    <span class="text-xs font-bold text-green-800">📄 Licencia CC BY 4.0</span>
  </div>
</section>"""

    secciones = [
        {"id": "inicio",      "icon": "👋", "title": "Portada", "html": portada},
        {
            "id": "introduccion", "icon": "📌", "title": "1. Introducción",
            "html": f"""
<h2 class="text-2xl font-bold text-slate-800 mb-4">Introducción a {nombre}</h2>
<div class="callout callout-info my-5">
  <div class="callout-title">📐 Contexto</div>
  <p class="text-sm">RAs trabajados: <strong>{ras_str}</strong>. Horas: <strong>{ut.get('horas', '—')}</strong>. Tags: {tags}</p>
</div>
<p class="text-slate-600 leading-relaxed mb-4">
  [Añade aquí la introducción al tema. Explica el contexto, por qué es importante y qué aprenderá el alumnado.]
</p>"""
        },
        {
            "id": "conceptos",  "icon": "📖", "title": "2. Conceptos clave",
            "html": f"""
<h2 class="text-2xl font-bold text-slate-800 mb-4">Conceptos clave</h2>
<p class="text-slate-600 leading-relaxed mb-4">[Desarrolla los conceptos teóricos principales de {nombre}.]</p>
<div class="callout callout-warning my-5">
  <div class="callout-title">⚠️ Importante</div>
  <p class="text-sm">[Añade un punto clave o advertencia importante.]</p>
</div>"""
        },
        {
            "id": "practica",   "icon": "🔧", "title": "3. Práctica",
            "html": f"""
<h2 class="text-2xl font-bold text-slate-800 mb-4">Aplicación práctica</h2>
<p class="text-slate-600 leading-relaxed mb-4">[Describe el procedimiento práctico para GNU/Linux y Windows Server cuando aplique.]</p>
<div class="code-block my-4">
  <span class="comment"># Ejemplo de comando (Linux)</span><br>
  <span class="keyword">comando</span> <span class="string">"argumento"</span>
</div>
<div class="callout callout-success my-5">
  <div class="callout-title">✅ Buena práctica</div>
  <p class="text-sm">[Añade una recomendación profesional.]</p>
</div>"""
        },
        {
            "id": "ejercicios", "icon": "📝", "title": "Ejercicios",
            "html": """
<h2 class="text-2xl font-bold text-slate-800 mb-4">Ejercicios prácticos</h2>
<div class="space-y-4">
  <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
    <div class="flex items-center gap-2 mb-2">
      <span class="bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded">EJ 1</span>
      <h4 class="font-bold text-slate-800">[Título del ejercicio]</h4>
    </div>
    <p class="text-sm text-slate-600">[Descripción del ejercicio.]</p>
  </div>
  <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
    <div class="flex items-center gap-2 mb-2">
      <span class="bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded">EJ 2</span>
      <h4 class="font-bold text-slate-800">[Título del ejercicio]</h4>
    </div>
    <p class="text-sm text-slate-600">[Descripción del ejercicio.]</p>
  </div>
</div>"""
        },
        {
            "id": "autoevaluacion", "icon": "✅", "title": "Autoevaluación",
            "html": """
<h2 class="text-2xl font-bold text-slate-800 mb-4">Autoevaluación</h2>
<div class="space-y-4">
  <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
    <p class="font-semibold text-slate-700 mb-2">1. [Pregunta de autoevaluación]</p>
    <p class="text-sm text-slate-500 italic">[Respuesta corta o pista]</p>
  </div>
  <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
    <p class="font-semibold text-slate-700 mb-2">2. [Pregunta de autoevaluación]</p>
    <p class="text-sm text-slate-500 italic">[Respuesta corta o pista]</p>
  </div>
</div>"""
        },
        {
            "id": "glosario",   "icon": "📚", "title": "Glosario",
            "html": f"""
<h2 class="text-2xl font-bold text-slate-800 mb-4">Glosario</h2>
<div class="space-y-2">
  {''.join(f'<div class="flex gap-3 p-3 bg-white border border-slate-100 rounded-lg"><span class="font-bold text-blue-700 min-w-[120px] text-sm">{tag}</span><span class="text-sm text-slate-600">[Definición de {tag}]</span></div>' for tag in (tags.split(' · ') if tags else ["[Término]"]))}
</div>"""
        },
    ]
    return secciones


# ─── Generador IA ─────────────────────────────────────────────────────────────

_SYSTEM_IA = textwrap.dedent("""\
    Eres un experto docente de FP (Formación Profesional) española especializado en ASIR.
    Generas contenido HTML para apuntes didácticos usando Vue 3 + Tailwind CSS.

    REGLAS CRÍTICAS:
    - Responde ÚNICAMENTE con el array JSON de secciones: [{...}, {...}, ...]
    - Cada objeto tiene: id (slug), icon (emoji), title (str), html (str con HTML)
    - El HTML usa clases Tailwind y los componentes callout/code-block definidos
    - NO uses backticks dentro del HTML (rompen el template literal de Vue)
    - Usa comillas simples o entidades HTML (&apos;) en lugar de backticks
    - Cubre siempre GNU/Linux Y Windows Server cuando aplique
    - Idioma: castellano técnico, nivel CFGS, tono explicativo y narrativo
    - Incluye siempre: introduccion, 2-4 secciones de contenido, ejercicios, autoevaluacion, glosario

    Componentes disponibles:
    <!-- Callout info/warning/success/danger -->
    <div class="callout callout-info my-5"><div class="callout-title">📐 Título</div><p class="text-sm">...</p></div>

    <!-- Bloque de código -->
    <div class="code-block my-4"><span class="comment"># comentario</span><br><span class="keyword">cmd</span> <span class="string">'arg'</span></div>

    <!-- Tabla -->
    <table class="w-full text-sm border-collapse my-4"><thead><tr class="bg-slate-700 text-white"><th class="p-3 text-left">Col</th></tr></thead><tbody><tr class="border-b bg-white"><td class="p-3">...</td></tr></tbody></table>

    <!-- Cards grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4"><div class="bg-blue-50 border border-blue-200 rounded-xl p-4"><h4 class="font-bold text-blue-800 mb-2">Título</h4><p class="text-xs text-slate-600">...</p></div></div>

    La sección 'inicio' SIEMPRE tiene id='inicio' y contiene la portada del tema (ver ejemplo en instrucciones).
""")


def _secciones_ia(mod, ut: dict, ia) -> list[dict]:
    """Genera secciones con contenido real via IA."""
    import json

    ras = _ras_de_ut(mod, ut["id"])
    ras_str = " · ".join(ras)

    portada_html = f"""<section id="inicio" class="text-center py-8 mb-4 flex flex-col justify-center min-h-[55vh]">
  <div class="inline-block bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full mb-4 mx-auto">FP Grado Superior · ASIR</div>
  <h1 class="text-4xl font-extrabold text-slate-900 leading-tight mb-2">{ut['nombre']}</h1>
  <p class="text-base text-slate-400 font-medium max-w-2xl mx-auto italic mb-6">{ut['id']} · {mod.MODULO['abrev']} — {mod.MODULO['nombre']} · {mod.MODULO['curso']} · {mod.MODULO['anno']}</p>
  <div class="grid grid-cols-2 gap-3 text-left max-w-sm mx-auto mb-6">
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Autora</span>
      <span class="text-sm font-bold text-slate-800">Isabel López</span>
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">RAs</span>
      <span class="text-sm font-bold text-slate-800">{ras_str}</span>
    </div>
  </div>
  <div class="inline-flex items-center gap-2 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5 mx-auto">
    <span class="text-xs font-bold text-green-800">📄 Licencia CC BY 4.0</span>
  </div>
</section>"""

    user = textwrap.dedent(f"""\
        Módulo: {mod.MODULO['nombre']} ({mod.MODULO['ciclo']} — {mod.MODULO['curso']})
        UT: {ut['id']} — {ut['nombre']}
        Horas: {ut.get('horas', '—')}  · Evaluación: EV{ut.get('eval', '?')}
        RAs que trabaja: {ras_str}
        Tags/conceptos clave: {ut.get('tags', '(no especificados)')}

        Genera el array JSON de secciones para esta UT.
        La primera sección DEBE ser exactamente:
        {{"id": "inicio", "icon": "👋", "title": "Portada", "html": {json.dumps(portada_html)}}}

        Luego añade: introduccion, 3-4 secciones de contenido técnico profundo (con analogías y ejemplos),
        ejercicios (mínimo 3), autoevaluacion (mínimo 5 preguntas), glosario (mínimo 10 términos clave).

        Responde SOLO con el array JSON, sin markdown, sin explicaciones, sin ```json.
    """)

    raw = ia._llamar(_SYSTEM_IA, user)

    # Intentar parsear JSON
    try:
        # Limpiar posibles bloques markdown
        raw_clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        secciones = json.loads(raw_clean)
        return secciones
    except Exception:
        print(f"  ⚠️  Error parseando JSON de IA, usando modo DEMO para esta UT.")
        return _secciones_demo(mod, ut)


# ─── Generador principal ──────────────────────────────────────────────────────

def generar_apunte(mod, ut: dict, ia, output_base: Path) -> Path:
    """Genera index.html para una UT. Devuelve el path del archivo creado."""
    import json

    print(f"  📄 {ut['id']}: {ut['nombre']}")

    if ia._proveedor == "demo":
        secciones = _secciones_demo(mod, ut)
    else:
        secciones = _secciones_ia(mod, ut, ia)

    # Serializar secciones a JSON válido para insertar en el script Vue
    sections_json = json.dumps(secciones, ensure_ascii=False, indent=2)

    html = _TEMPLATE.format(
        title        = ut["nombre"],
        ut_label     = ut["id"],
        abrev        = mod.MODULO["abrev"],
        modulo_nombre= mod.MODULO["nombre"],
        curso        = mod.MODULO["curso"],
        anno         = mod.MODULO.get("anno", "2026-2027"),
        autora       = "Isabel López",
        sections_json= sections_json,
    )

    out_path = apunte_path(mod, ut, output_base)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def generar_modulo(mod, ia, output_base: Path, ut_filtro: str | None = None) -> list[Path]:
    """Genera apuntes para todas (o una) las UTs del módulo. Devuelve paths creados."""
    generados = []
    for ut in mod.UTS:
        if ut_filtro and ut["id"] != ut_filtro:
            continue
        path = generar_apunte(mod, ut, ia, output_base)
        generados.append(path)
    return generados


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _cargar_modulo(nombre: str):
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    nombre_limpio = nombre.replace("scripts/modules/", "").replace(".py", "")
    try:
        return importlib.import_module(f"modules.{nombre_limpio}")
    except ModuleNotFoundError:
        print(f"❌ Módulo '{nombre_limpio}' no encontrado en scripts/modules/")
        sys.exit(1)


def _parse_opts(args: list[str], keys: list[str]) -> dict[str, str]:
    opts: dict[str, str] = {}
    i = 0
    while i < len(args):
        if args[i] in keys and i + 1 < len(args):
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    return opts


AYUDA = textwrap.dedent("""\
    EvalFP — Generador de Apuntes HTML
    ====================================
    Uso: python build_apuntes.py [opciones]

    Opciones:
      --modulo  <nombre>  Módulo a generar (iso_data, par_data, …) [default: iso_data]
      --ut      <UT_ID>   Generar solo esta UT (p.ej. UT1). Sin esta opción → todas las UTs.
      --salida  <dir>     Directorio base de salida [default: ../apuntes]
      --proveedor <p>     claude | openai | demo | auto [default: auto]
      --ayuda             Muestra esta ayuda

    Variables de entorno:
      ANTHROPIC_API_KEY   Para generar contenido con Claude (recomendado)
      OPENAI_API_KEY      Para generar contenido con OpenAI (alternativa)

    Sin API key → modo DEMO: genera HTML estructurado con secciones de ejemplo editables.

    Ejemplos:
      python build_apuntes.py --modulo iso_data
      python build_apuntes.py --modulo iso_data --ut UT1
      python build_apuntes.py --modulo par_data --proveedor demo --salida ../apuntes
""")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or "--ayuda" in args or "-h" in args:
        print(AYUDA)
        sys.exit(0)

    opts    = _parse_opts(args, ["--modulo", "--ut", "--salida", "--proveedor"])
    mod     = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ut_id   = opts.get("--ut")
    salida  = Path(opts.get("--salida", str(Path(__file__).parent.parent / "apuntes")))
    proveedor = opts.get("--proveedor", "auto")

    from ai_asistente import IAAsistente
    ia = IAAsistente(proveedor=proveedor)

    print(f"Generando apuntes — {mod.MODULO['abrev']} · {mod.MODULO['nombre']}")
    print(f"Proveedor IA: {ia._proveedor}  |  Salida: {salida}")
    print()

    archivos = generar_modulo(mod, ia, salida, ut_id)

    print(f"\n✅ {len(archivos)} apunte(s) generado(s):")
    for p in archivos:
        print(f"   📄 {p}")

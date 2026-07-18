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
import json as _json
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Any


# ─── Adaptador JSON → interfaz de módulo ─────────────────────────────────────

class _ModFromJson:
    """
    Adapta un dict JSON (exportado desde SQLite por Electron) a la misma
    interfaz que los módulos Python estáticos (iso_data.py, par_data.py…):
      mod.MODULO       → {nombre, abrev, ciclo, curso, anno}
      mod.UTS          → [{id, nombre, horas, eval, tags}, …]
      mod.RAS          → [{id, nombre, pond}, …]
      mod.CES          → {"RA1": [{id, texto}, …], …}
      mod.ASIGNACIONES → [(ut_id, ra_id, [ce_ids]), …]
    """
    def __init__(self, data: dict):
        self.MODULO = {
            'nombre': data.get('nombre', data.get('abrev', '?')),
            'abrev':  data.get('abrev', '?'),
            'ciclo':  data.get('ciclo', 'FP'),
            'curso':  data.get('curso', ''),
            'anno':   data.get('anno', '2026-2027'),
        }
        self.UTS  = data.get('uts', [])
        self.RAS  = data.get('ras', [])
        self.CES  = data.get('ces', {})
        # SQLite guarda [{ut, ra, ces:[...]}, …] → convertir a tuplas
        self.ASIGNACIONES = [
            (a['ut'], a['ra'], a.get('ces', []))
            for a in data.get('asignaciones', [])
        ]


def _cargar_desde_json(json_path: str) -> '_ModFromJson':
    with open(json_path, encoding='utf-8') as f:
        return _ModFromJson(_json.load(f))

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


def _ciclo_badge(mod) -> str:
    """
    Crea etiqueta corta para la portada: 'FP Grado Superior · ASIR'
    Extrae el grado del ciclo y la sigla del campo curso (ej: '1º ASIR' → 'ASIR').
    Funciona para cualquier familia profesional.
    """
    ciclo = mod.MODULO.get('ciclo', '')
    curso = mod.MODULO.get('curso', '')
    ciclo_lower = ciclo.lower()

    # Siglas de Grado Superior de todas las familias profesionales
    _gs_siglas = {
        # Informática y Comunicaciones
        'ASIR', 'DAM', 'DAW', 'ASIX', 'SYSNET', 'SMIX', 'IABD', 'CIB',
        # Administración y Gestión
        'ADGF', 'AF', 'ADE', 'RR.HH.',
        # Comercio y Marketing
        'MK', 'COM',
        # Hostelería y Turismo
        'AGT', 'TSRH', 'TD',
        # Sanidad
        'TAFAD', 'TES',
        # Electricidad y Electrónica
        'ASEA', 'SEI',
        # Fabricación Mecánica / Automoción
        'TSAFAR', 'TASEA',
        # Edificación / Civil
        'PCI',
        # marcador genérico
        'CFGS',
    }
    # Siglas de Grado Medio
    _gm_siglas = {
        'SMR', 'CFGM',
        # Admin
        'GEA',
        # Comercio
        'AF2',
        # Hostelería
        'TCM',
    }

    grado = 'FP'
    if 'superior' in ciclo_lower or any(s in ciclo for s in _gs_siglas):
        grado = 'FP Grado Superior'
    elif 'medio' in ciclo_lower or any(s in ciclo for s in _gm_siglas):
        grado = 'FP Grado Medio'

    # Extraer sigla del curso: '1º ASIR' → 'ASIR', '2º DAM' → 'DAM'
    sigla = re.sub(r'^\d+[ºª]?\s*', '', curso).strip()

    return f"{grado} · {sigla}" if sigla else (f"{grado} · {curso}" if curso else grado)

# ─── Plantilla HTML ──────────────────────────────────────────────────────────

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · {ut_label} · {abrev} · {curso}</title>
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
  * {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg-main); color: var(--text-main); line-height: 1.7; overflow-x: hidden; }}
  h1,h2,h3,h4,h5,h6 {{ font-weight: 800 !important; color: #0f172a; letter-spacing: -0.02em; }}
  h2 {{ font-size: 1.75rem; margin-top: 0.75rem; margin-bottom: 0.5rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 0.5rem; color: var(--primary); }}
  h3 {{ font-size: 1.25rem; margin-top: 0.5rem; margin-bottom: 0.5rem; color: #1e293b; display: flex; align-items: center; gap: 0.5rem; }}
  h3::before {{ content: ''; width: 4px; height: 1rem; background: var(--primary); border-radius: 4px; display: inline-block; flex-shrink: 0; }}
  h4 {{ font-size: 1rem; margin-top: 0.5rem; margin-bottom: 0.25rem; }}
  p {{ margin-bottom: 0.5rem; color: #475569; text-align: justify; }}
  code {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85em; }}
  ul, ol {{ margin-bottom: 0.5rem; }}
  .callout {{ padding: 1rem; border-radius: 1rem; margin: 0.75rem 0; border: 1px solid transparent; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
  .callout-title {{ display: flex; align-items: center; gap: 0.75rem; font-weight: 700; margin-bottom: 0.75rem; font-size: 1rem; }}
  .callout-info    {{ background-color: #eff6ff; border-color: #bfdbfe; color: #1e40af; }}
  .callout-warning {{ background-color: #fffbeb; border-color: #fef3c7; color: #92400e; }}
  .callout-success {{ background-color: #f0fdf4; border-color: #bbf7d0; color: #166534; }}
  .callout-danger  {{ background-color: #fef2f2; border-color: #fecaca; color: #991b1b; }}
  .sidebar {{ width: var(--sidebar-width); background: var(--bg-subtle); border-right: 1px solid var(--border);
              position: fixed; height: 100vh; z-index: 40;
              transition: all 0.4s cubic-bezier(0.4,0,0.2,1); left: 0; overflow-y: auto; }}
  .sidebar-collapsed {{ transform: translateX(-100%); }}
  .nav-item {{ display: flex; align-items: center; padding: 0.65rem 1.25rem; margin: 0.2rem 1rem;
               font-size: 0.85rem; font-weight: 600; color: var(--text-muted); border-radius: 0.75rem;
               transition: all 0.2s; text-decoration: none; }}
  .nav-item:hover {{ background-color: #f1f5f9; color: var(--text-main); transform: translateX(4px); }}
  .nav-item.active {{ background-color: white; color: var(--primary); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
  .main-container {{ margin-left: var(--sidebar-width); transition: margin-left 0.4s cubic-bezier(0.4,0,0.2,1); min-height: 100vh; }}
  .main-container-expanded {{ margin-left: 0; }}
  @media (max-width: 1024px) {{
    .sidebar {{ transform: translateX(-100%); }}
    .sidebar:not(.sidebar-collapsed) {{ transform: translateX(0); box-shadow: 20px 0 50px rgba(0,0,0,0.1); }}
    .main-container {{ margin-left: 0 !important; }}
  }}
  header {{ height: var(--header-height); background: rgba(255,255,255,0.8); backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 30;
            display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; }}
  .toggle-btn {{ padding: 0.5rem; border-radius: 0.5rem; color: var(--text-muted); transition: all 0.2s; background: none; border: none; cursor: pointer; }}
  .toggle-btn:hover {{ background: #f1f5f9; color: var(--primary); }}
  .content-area {{ max-width: 900px; margin: 0 auto; padding: 1rem 1.5rem; }}
  section {{ margin-bottom: 0.5rem; padding-top: 0; }}
  .code-block {{ background: #0f172a; color: #e2e8f0; font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem; padding: 1rem 1.25rem; border-radius: 0.75rem;
                line-height: 1.6; overflow-x: auto; }}
  .code-block .comment {{ color: #64748b; }}
  .code-block .keyword {{ color: #93c5fd; }}
  .code-block .string  {{ color: #86efac; }}
  .code-block .number  {{ color: #fca5a5; }}
  @media print {{
    @page {{ margin: 2cm; size: a4; }}
    .sidebar, header, .no-print {{ display: none !important; }}
    .main-container {{ margin-left: 0 !important; padding: 0 !important; }}
    .content-area {{ max-width: 100% !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }}
    body {{ background: white !important; font-size: 11pt; }}
    * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
    h2 {{ border-bottom: 2px solid #eee !important; }}
    .callout, .code-block {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div id="app" v-cloak>

  <!-- Sidebar -->
  <aside class="sidebar no-print" :class="{{ 'sidebar-collapsed': !sidebarOpen }}">
    <div class="h-20 flex items-center px-5 border-b border-slate-200 bg-white">
      <div>
        <div class="font-extrabold text-sm leading-tight text-slate-800">{abrev} · {curso}</div>
        <div class="text-[10px] text-slate-400 mt-0.5 uppercase tracking-wider font-bold">{modulo_nombre}</div>
      </div>
    </div>
    <nav class="py-4">
      <a v-for="s in sections" :key="s.id"
         :href="'#' + s.id"
         class="nav-item"
         :class="{{ active: activeSection === s.id }}"
         @click="activeSection = s.id"
      ><span class="text-base mr-2">{{{{ s.icon }}}}</span><span class="leading-tight">{{{{ s.title }}}}</span></a>
    </nav>
  </aside>

  <!-- Main -->
  <div class="main-container" :class="{{ 'main-container-expanded': !sidebarOpen }}">

    <!-- CC BY Banner -->
    <div class="no-print bg-gradient-to-r from-green-50 to-emerald-50 border-b border-green-200 px-6 py-2">
      <div class="max-w-5xl mx-auto flex items-center gap-3">
        <span class="text-xs font-bold text-green-800">📄 Licencia <strong>CC BY 4.0</strong> — Material educativo de libre uso con atribución</span>
      </div>
    </div>

    <!-- Header -->
    <header class="no-print">
      <div class="flex items-center gap-3">
        <button @click="sidebarOpen = !sidebarOpen" class="toggle-btn">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <span class="text-sm font-bold text-slate-700 truncate max-w-md">{ut_label} — {title}</span>
      </div>
      <button onclick="window.print()"
              class="inline-flex items-center gap-2 bg-white border border-slate-200 text-slate-600 text-sm font-bold px-4 py-2 rounded-xl hover:bg-slate-50 transition-all no-print">
        🖨️ Imprimir / PDF
      </button>
    </header>

    <!-- Contenido -->
    <main class="content-area">
      <section v-for="s in sections" :key="s.id" :id="s.id" class="mb-6 scroll-mt-24">
        <div v-html="s.html"></div>
      </section>
    </main>

    <footer class="bg-slate-50 border-t border-slate-200 py-8 no-print">
      <div class="max-w-4xl mx-auto px-8 flex justify-between items-center text-xs text-slate-400">
        <span>{modulo_nombre} · {ut_label} · {autora} · CC BY 4.0 · {anno}</span>
        <span>Licencia CC BY 4.0</span>
      </div>
    </footer>
  </div>

</div>
<script>
const {{ createApp }} = Vue;
createApp({{
  data() {{
    return {{
      activeSection: 'inicio',
      sidebarOpen: true,
      sections: {sections_json}
    }};
  }},
  mounted() {{
    if (window.innerWidth < 1024) this.sidebarOpen = false;
    document.title = '{title} · {ut_label} · {abrev} · {curso}';
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

    portada = f"""<div class="text-center py-8 mb-4 flex flex-col justify-center min-h-[55vh]">
  <div class="inline-block bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full mb-4 mx-auto">{_ciclo_badge(mod)}</div>
  <h1 class="text-4xl text-slate-900 leading-tight mb-2">{nombre}</h1>
  <p class="text-base text-slate-400 font-medium max-w-2xl mx-auto italic mb-6">{ut['id']} · {mod.MODULO['abrev']} — {mod.MODULO['nombre']} · {mod.MODULO['curso']} · {mod.MODULO['anno']}</p>
  <div class="grid grid-cols-2 gap-3 text-left max-w-sm mx-auto mb-6">
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Autora</span>
      <span class="text-sm font-bold text-slate-800">Isabel López</span>
    </div>
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Curso</span>
      <span class="text-sm font-bold text-slate-800">{mod.MODULO['anno']}</span>
    </div>
  </div>
  <div class="inline-flex items-center gap-2 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5 mx-auto">
    <span class="text-xs font-bold text-green-800">📄 Licencia CC BY 4.0</span>
  </div>
</div>"""

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

def _familia_tipo(ciclo: str) -> str:
    """
    Detecta la familia profesional del ciclo para adaptar el estilo del contenido.
    Devuelve: 'informatica' | 'admin_gestion' | 'comercio' | 'sanidad' | 'hosteleria' | 'general'
    """
    c = ciclo.lower()
    if any(k in c for k in ('informátic', 'informatica', 'sistemas', 'comunicacion', 'comunicación',
                             'asir', 'dam', 'daw', 'red', 'ciberseguridad')):
        return 'informatica'
    if any(k in c for k in ('administrac', 'gestión', 'gestion', 'finanz', 'contabil',
                             'recursos humanos', 'fiscal')):
        return 'admin_gestion'
    if any(k in c for k in ('comercio', 'marketing', 'ventas', 'actividades comerciales')):
        return 'comercio'
    if any(k in c for k in ('sanidad', 'enfermer', 'farmac', 'laboratori', 'salud')):
        return 'sanidad'
    if any(k in c for k in ('hostelería', 'hosteleria', 'turismo', 'restaur', 'alojamiento')):
        return 'hosteleria'
    return 'general'


def _profundidad_hint(familia: str) -> str:
    """Devuelve el hint de profundidad apropiado para cada familia profesional."""
    hints = {
        'informatica': (
            "Profundidad técnica real: versiones actuales de software, comandos reales "
            "con flags y su efecto, valores numéricos de rendimiento, comparativas de "
            "protocolos con métricas reales"
        ),
        'admin_gestion': (
            "Profundidad real: artículos de ley o reglamento con número y fecha, "
            "ejemplos numéricos con cifras reales (asientos contables, cálculos fiscales, "
            "nóminas), casos prácticos basados en situaciones empresariales verosímiles"
        ),
        'comercio': (
            "Profundidad real: datos de mercado actuales, ejemplos de campañas o "
            "estrategias reales, cálculos de márgenes/ratios con cifras concretas, "
            "referencias a normativa de comercio y consumo"
        ),
        'sanidad': (
            "Profundidad real: nomenclatura clínica correcta, protocolos con pasos "
            "exactos, dosis o parámetros con unidades, referencias a guías clínicas "
            "y normativa sanitaria vigente"
        ),
        'hosteleria': (
            "Profundidad real: temperaturas, tiempos y gramajes precisos, referencias "
            "a normativa APPCC y de higiene alimentaria, ejemplos de fichas técnicas "
            "y escandallos reales"
        ),
        'general': (
            "Profundidad real: ejemplos concretos del sector con datos numéricos, "
            "referencias a normativa o estándares aplicables, casos prácticos verosímiles"
        ),
    }
    return hints.get(familia, hints['general'])


def _make_system_ia(ciclo: str, curso: str) -> str:
    """Genera el system prompt adaptado al ciclo y curso reales del módulo."""
    nivel   = f"{ciclo} — {curso}" if curso else ciclo
    familia = _familia_tipo(ciclo)
    prof    = _profundidad_hint(familia)

    # El bloque de código solo se incluye en familias donde tiene sentido
    componente_codigo = ""
    if familia in ('informatica', 'admin_gestion', 'general'):
        componente_codigo = (
            "\n        <!-- Bloque de código / fórmula / ejemplo técnico -->"
            "\n        <div class=\"code-block my-4\">"
            "<span class=\"comment\"># comentario / descripción</span><br>"
            "<span class=\"keyword\">instruccion</span> "
            "<span class=\"string\">'valor'</span> "
            "<span class=\"number\">42</span></div>"
        )

    return textwrap.dedent(f"""\
        Eres un experto docente de Formación Profesional española, especializado en {ciclo}.
        Generas apuntes didácticos de alta calidad en HTML (Vue 3 + Tailwind CSS) para {nivel}.

        FILOSOFÍA DEL CONTENIDO:
        - Cada concepto merece 3-5 párrafos explicativos con desarrollo real, no listas de bullets
        - Empieza los conceptos clave explicando "qué pasaría sin este concepto" antes de definirlo
        - Usa analogías del mundo cotidiano o del sector para conceptos abstractos
        - Incluye siempre el "por qué importa profesionalmente" y conexiones con otros módulos del ciclo
        - {prof}
        - Para evolución histórica: tarjetas de cronología con badges de año
        - Para procedimientos: pasos numerados con justificación del porqué de cada uno
        - Para comparativas: tablas con descripción, ventajas/limitaciones y caso de uso real
        - Para flujos de proceso: pasos con borde lateral de color

        REGLAS CRÍTICAS:
        - Responde ÚNICAMENTE con el array JSON: [{{"id":"...","icon":"...","title":"...","html":"..."}}]
        - NO uses backticks en el HTML (rompen el template literal de Vue); usa comillas simples o &apos;
        - Idioma: castellano técnico para {nivel}, tono explicativo narrativo (como libro de texto de calidad)
        - El JSON debe ser válido: escapa las comillas dobles dentro de atributos HTML como &quot;

        COMPONENTES DISPONIBLES (úsalos activamente en combinación):

        <!-- Callout (info/warning/success/danger) -->
        <div class="callout callout-info my-5"><div class="callout-title">📐 Título</div><p class="text-sm">Contenido.</p></div>
{componente_codigo}
        <!-- Tabla con cabecera oscura (alterna bg-white / bg-slate-50 en filas) -->
        <table class="w-full text-sm border-collapse my-4"><thead><tr class="bg-slate-700 text-white"><th class="p-3 text-left">Col A</th><th class="p-3 text-left">Col B</th></tr></thead><tbody><tr class="border-b bg-white"><td class="p-3 font-semibold">...</td><td class="p-3 text-slate-600 text-xs">...</td></tr><tr class="border-b bg-slate-50"><td class="p-3 font-semibold">...</td><td class="p-3 text-slate-600 text-xs">...</td></tr></tbody></table>

        <!-- Tarjetas de cronología (evolución histórica, hitos) -->
        <div class="space-y-3 my-4"><div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm"><div class="flex items-start gap-3"><span class="bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded-lg flex-shrink-0">1970</span><div><h4 class="font-bold text-slate-800 text-sm">Título del hito</h4><p class="text-sm text-slate-600 mt-1">Descripción detallada del hito y su relevancia.</p></div></div></div></div>

        <!-- Pasos numerados (procedimientos, procesos, protocolos) -->
        <div class="space-y-3 my-4"><div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm"><div class="flex items-center gap-2 mb-2"><span class="bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded">1</span><h4 class="font-bold text-slate-800">Nombre del paso</h4></div><p class="text-sm text-slate-600">Descripción y justificación del paso.</p></div></div>

        <!-- Grid de tarjetas coloreadas (clasificaciones, comparativas, tipos) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 my-4"><div class="bg-blue-50 border border-blue-200 rounded-xl p-4"><h4 class="font-bold text-blue-800 mb-2">Categoría A</h4><p class="text-xs text-slate-600">Descripción.</p></div><div class="bg-green-50 border border-green-200 rounded-xl p-4"><h4 class="font-bold text-green-800 mb-2">Categoría B</h4><p class="text-xs text-slate-600">Descripción.</p></div><div class="bg-purple-50 border border-purple-200 rounded-xl p-4"><h4 class="font-bold text-purple-800 mb-2">Categoría C</h4><p class="text-xs text-slate-600">Descripción.</p></div></div>

        <!-- Flujo de proceso (pasos con borde lateral de color) -->
        <div class="space-y-3 my-4"><div class="bg-white border-l-4 border-blue-500 rounded-r-xl p-4 shadow-sm"><h4 class="font-bold text-blue-800 text-sm mb-2">Paso 1 — Nombre</h4><p class="text-xs text-slate-600">Qué ocurre en este paso y por qué.</p></div><div class="bg-white border-l-4 border-green-500 rounded-r-xl p-4 shadow-sm"><h4 class="font-bold text-green-800 text-sm mb-2">Paso 2 — Nombre</h4><p class="text-xs text-slate-600">...</p></div></div>

        <!-- Diagrama de capas / jerarquía (divs apilados con flechas) -->
        <div class="space-y-1 my-5 text-sm"><div class="bg-purple-50 border border-purple-200 rounded-xl p-3 text-purple-800 font-semibold">Nivel superior</div><div class="flex justify-center"><div class="w-0.5 h-4 bg-slate-300"></div></div><div class="bg-blue-50 border border-blue-200 rounded-xl p-3 text-blue-800 font-semibold">Nivel intermedio</div><div class="flex justify-center"><div class="w-0.5 h-4 bg-slate-300"></div></div><div class="bg-green-50 border border-green-200 rounded-xl p-3 text-green-800 font-semibold">Nivel base</div></div>

        <!-- Tarjeta de glosario con barra lateral azul -->
        <div class="bg-white border border-slate-200 rounded-xl p-3 flex gap-3 shadow-sm"><div class="w-1 bg-blue-500 rounded-full flex-shrink-0"></div><div><strong class="text-slate-800 text-sm">Término</strong><p class="text-xs text-slate-600 mt-0.5">Definición completa y precisa.</p></div></div>

        La primera sección SIEMPRE tiene id='inicio' y su html es la portada proporcionada.
    """)


def _fix_json_escapes(s: str) -> str:
    """Reemplaza \\X inválidos en JSON (ej: \\s, \\d, \\w) con \\\\X."""
    return re.sub(r'\\([^"\\/bfnrtu\n\r])', lambda m: '\\\\' + m.group(1), s)


def _limpiar_html_ia(html: str) -> str:
    """
    Limpia artefactos que la IA suele meter en el HTML de las secciones:
    - Bloques de markdown (``` html  ```)
    - Etiquetas <script> completas (no queremos JS en el HTML de contenido)
    - Expresiones de template literal JS tipo ${...} y ` backtick
    - Preambles JSON que la IA añade antes del HTML (ej: 'on [{"id":...,"html":"')
    - Sufijos JSON que la IA añade tras el HTML (ej: '"}]')
    """
    # 0. Convertir secuencias literales \n y \t a caracteres reales
    #    El AI a veces emite \n como texto (backslash + n) en lugar de
    #    un salto de línea real. En HTML esto se muestra como texto visible.
    html = html.replace('\\n', '\n').replace('\\t', '  ')

    # 1. Quitar bloques markdown residuales
    html = re.sub(r"```(?:html|javascript|js)?", "", html)

    # 2. Quitar bloques <script>...</script> completos
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 3. Quitar expresiones ${...} (template literals de JS que se cuelan en el HTML)
    html = re.sub(r'\$\{[^}]*\}', '', html)

    # 4. Quitar backticks sueltos que romperían template literals (legado)
    html = html.replace('`', "'")

    # 5. Strip JSON preamble: si hay texto antes del primer '<' que parezca JSON
    #    (p.ej. 'on [{"id":"sec","icon":"...","html":"') eliminarlo.
    first_tag = html.find('<')
    if first_tag > 0:
        before = html[:first_tag]
        # Si el prefijo contiene comillas/llaves/corchetes → es artefacto JSON, no contenido
        if '{' in before or '[' in before or '"html"' in before or len(before.strip()) > 80:
            html = html[first_tag:]

    # 5b. Strip ctx_base preamble si el AI lo incluyó en el HTML.
    #     Ocurre cuando la IA repite el bloque de contexto del módulo
    #     (Módulo:, Ciclo /, UT:…) antes del primer <h2>.
    _mh = re.search(r'<h[1-4][\s>]', html, re.IGNORECASE)
    if _mh and _mh.start() > 0:
        _bh = html[:_mh.start()]
        if re.search(r'Módulo\s*:|Ciclo\s*/|^\s*UT\s*:|Curso\s*/|Tags\s*:', _bh,
                     re.IGNORECASE | re.MULTILINE):
            html = html[_mh.start():]

    # 5c. Truncar en artefactos JSON de sección INCRUSTADOS en el HTML.
    #
    #  El AI a veces mezcla el HTML de contenido con JSON de sección, en dos patrones:
    #   · "},{"id":"siguiente","html":"   → transición entre elementos del array
    #   · on [{"id":"inicio","html":"     → el AI añade el array completo de secciones
    #   · [{"id":"inicio","html":"        → idem sin el "on"
    #
    #  En todos los casos: si hay HTML válido ANTES del artefacto, truncamos ahí.
    _m5b = re.search(
        r'(?:'
        r'"\s*\}\s*,\s*\{\s*'          # "},{ — transición de array
        r'|on\s+\[?\s*\{\s*'           # on [{ — narración + array
        r'|\[\s*\{\s*'                  # [{ — array directo
        r')'
        r'"(?:id|icon|title|html)"\s*:',
        html, re.DOTALL
    )
    if _m5b:
        _before5b = html[:_m5b.start()].rstrip('"').strip()
        if '<' in _before5b:           # Solo si hay HTML válido antes → truncar
            html = _before5b

    # 6. Strip todo lo que aparece después del último '>'.
    #    Las respuestas HTML válidas no tienen texto tras el cierre del último elemento;
    #    cualquier texto posterior es un artefacto JSON ("},{"id":"..."...).
    last_gt = html.rfind('>')
    if last_gt >= 0:
        html = html[:last_gt + 1]

    # 7. Convertir encabezados markdown residuales a HTML
    #    El AI a veces escribe "# Título" en lugar de <h3>Título</h3>
    html = re.sub(r'^#{3,}\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^#{2}\s+(.+)$',  r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.+)$',     r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # 7b. Convertir listas markdown (* item / - item) a HTML <ul><li>
    #     Evita que los asteriscos aparezcan como texto visible en el navegador.
    #     Caso especial: si los items empiezan por a)/b)/c)/d) (opciones de test),
    #     suprimimos el bullet visual para no mostrar "• a) chmod" (dos sistemas de listado).
    def _md_list_to_ul(match: re.Match) -> str:
        raw = match.group(0).rstrip()
        is_test = bool(re.search(r'^[ \t]*[*\-]\s+[a-d]\)', raw, re.MULTILINE))
        items = re.sub(
            r'^[ \t]*[*\-]\s+(.+)$',
            r'  <li>\1</li>',
            raw,
            flags=re.MULTILINE
        )
        if is_test:
            # Opciones a/b/c/d: sin bullets (el prefijo ya identifica la opción)
            return (
                '<ul class="space-y-1 my-2 ml-4" style="list-style:none;padding-left:0">'
                f'\n{items}\n</ul>'
            )
        return f'<ul class="list-disc space-y-1 my-3 ml-5">\n{items}\n</ul>'

    html = re.sub(
        r'(?:^[ \t]*[*\-]\s+.+$\n?)+',
        _md_list_to_ul,
        html,
        flags=re.MULTILINE
    )

    # 7c. Convertir listas numeradas markdown (1. item) a HTML <ol><li>
    def _md_list_to_ol(match: re.Match) -> str:
        items = re.sub(
            r'^[ \t]*\d+\.\s+(.+)$',
            r'  <li>\1</li>',
            match.group(0).rstrip(),
            flags=re.MULTILINE
        )
        return f'<ol class="list-decimal space-y-1 my-3 ml-5">\n{items}\n</ol>'

    html = re.sub(
        r'(?:^[ \t]*\d+\.\s+.+$\n?)+',
        _md_list_to_ol,
        html,
        flags=re.MULTILINE
    )

    # 7d. Fixear <ul class="list-disc..."> cuyas <li> empiezan por a)/b)/c)/d).
    #     La IA a veces genera HTML directo con list-disc para opciones de test,
    #     produciendo "• a) opción" (bullet + letra = doble identificador visual).
    def _fix_test_ul(m: re.Match) -> str:
        ul = m.group(0)
        if not re.search(r'<li[^>]*>\s*[a-dA-D]\)', ul):
            return ul  # No es lista de test → dejar intacta
        ul = re.sub(r'\blist-disc\b\s*', '', ul)           # Quitar list-disc del class
        ul = re.sub(r'(<ul\b[^>]*?)(>)',                   # Añadir style inline
                    r'\1 style="list-style:none;padding-left:0"\2', ul, count=1)
        return ul

    html = re.sub(r'<ul\b[^>]*>.*?</ul>', _fix_test_ul, html, flags=re.DOTALL | re.IGNORECASE)

    # 7e. Extraer <pre class="code-block"> / <div class="code-block"> de dentro de <p>.
    #     HTML inválido: los navegadores auto-cierran el <p> al encontrar un elemento de
    #     bloque, produciendo texto que "flota" encima del bloque de código.
    #     Solución: dividir el <p> en tres partes — texto previo | bloque | texto posterior.
    _code_in_p = re.compile(
        r'<p([^>]*)>'
        r'((?:(?!<(?:pre|div)\b)[\s\S])*?)'               # texto antes del bloque
        r'(<(?:pre|div)\b[^>]*class="[^"]*code-block[^"]*"[^>]*>'
        r'[\s\S]*?</(?:pre|div)>)'                         # bloque de código completo
        r'([\s\S]*?)</p>',                                 # texto después del bloque
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

    # Dos pasadas por si hay más de un bloque de código en el mismo <p>
    for _ in range(2):
        html = _code_in_p.sub(_split_code_from_p, html)

    # 8. Limpiar espacios sobrantes al principio y final
    return html.strip()


def _parsear_json_ia(raw: str, contexto: str = "") -> list | dict | None:
    """
    Intenta parsear JSON de la respuesta IA con múltiples estrategias de recuperación.
    Devuelve el objeto parseado o None si todos los intentos fallan.
    """
    import json
    raw_clean = re.sub(r"```(?:json)?|```", "", raw).strip()

    for intento, texto in [
        ("directo",        raw_clean),
        ("fix_escapes",    _fix_json_escapes(raw_clean)),
    ]:
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            pass

    # Extraer el primer array o dict de la respuesta
    for patron in [r'(\[.*\])', r'(\{.*\})']:
        m = re.search(patron, raw_clean, re.DOTALL)
        if m:
            for texto in [m.group(1), _fix_json_escapes(m.group(1))]:
                try:
                    return json.loads(texto)
                except json.JSONDecodeError:
                    pass

    # Intentar cerrar JSON truncado
    truncated = raw_clean.rstrip().rstrip(',')
    if not truncated.endswith(']'):
        depth_obj = truncated.count('{') - truncated.count('}')
        depth_arr = truncated.count('[') - truncated.count(']')
        truncated += '}' * max(0, depth_obj) + ']' * max(0, depth_arr)
    try:
        result = json.loads(truncated)
        print(f"  ⚠️  JSON truncado recuperado parcialmente{' (' + contexto + ')' if contexto else ''}.")
        return result
    except Exception:
        pass

    return None


# ─── Helpers para bloques pedagógicos (HTML generado desde Python) ────────────

def _html_ces(ces_ids: list) -> str:
    """Chips de criterios de evaluación — generado en Python para garantizar estilo."""
    if not ces_ids:
        return ""
    chips = "".join(
        f'<span class="bg-blue-50 border border-blue-200 text-blue-700 '
        f'text-xs font-bold px-2.5 py-0.5 rounded-full">{c}</span>'
        for c in ces_ids
    )
    return (
        '<div class="flex flex-wrap gap-2 mb-5 mt-1">'
        '<span class="text-[10px] font-bold text-slate-400 uppercase '
        'tracking-widest mr-1 self-center">Criterios:</span>'
        f'{chips}</div>'
    )


def _html_errores(errores: list) -> str:
    """Tarjetas de errores frecuentes — generado en Python para garantizar estilo."""
    if not errores:
        return ""
    cards = ""
    for e in errores:
        cards += (
            '<div class="bg-red-50 border border-red-200 rounded-xl p-4">'
            '<div class="flex items-start gap-3">'
            '<span class="bg-red-600 text-white text-xs font-bold px-2 py-0.5 '
            'rounded flex-shrink-0 mt-0.5">!</span>'
            '<div>'
            f'<h4 class="font-bold text-red-800 text-sm">{e.get("sintoma","")}</h4>'
            f'<p class="text-xs text-slate-600 mt-1"><strong>Causa:</strong> {e.get("causa","")}</p>'
            f'<p class="text-xs text-slate-600 mt-0.5"><strong>Solución:</strong> {e.get("solucion","")}</p>'
            '</div></div></div>'
        )
    return (
        '<h3 class="mt-10" style="color:#7f1d1d">⚠️ Errores frecuentes</h3>'
        '<div class="space-y-3 my-4">'
        f'{cards}</div>'
    )


def _html_reflexion(preguntas: list) -> str:
    """Mini-reflexión formativa — generado en Python para garantizar estilo."""
    if not preguntas:
        return ""
    ps = "".join(
        f'<p class="text-sm text-amber-700 mb-2">{i + 1}. {p}</p>'
        for i, p in enumerate(preguntas[:3])
    )
    return (
        '<div class="bg-amber-50 border border-amber-200 rounded-xl p-5 my-6">'
        '<h4 class="font-bold text-amber-800 mb-3">🤔 Reflexiona</h4>'
        f'{ps}</div>'
    )


def _meta_pedagogica(ia, system_ia: str, ctx_base: str,
                     sec_title: str, modelo: str) -> dict:
    """
    Llama a la IA con un prompt ligero para obtener metadatos pedagógicos
    de una sección como JSON limpio: CEs relevantes, errores frecuentes,
    preguntas de reflexión.
    Devuelve el dict parseado, o {} si falla.
    """
    meta_prompt = textwrap.dedent(f"""\
        {ctx_base}

        Para la sección "{sec_title}", devuelve ÚNICAMENTE el siguiente objeto JSON
        (sin texto adicional, sin markdown, sin backticks):

        {{
          "ces": ["CE1.a", "CE1.b"],
          "errores": [
            {{"sintoma": "...", "causa": "...", "solucion": "..."}},
            {{"sintoma": "...", "causa": "...", "solucion": "..."}}
          ],
          "reflexion": [
            "¿...?",
            "¿...?",
            "¿...?"
          ]
        }}

        Normas:
        - ces: 2-4 IDs exactos de los CEs del contexto más relevantes para esta sección
        - errores: 3-5 errores reales y específicos de ESTE tema (no genéricos):
            síntoma = lo que observa el alumno/técnico
            causa   = por qué ocurre (explicación técnica)
            solucion = cómo corregirlo (con comando o paso exacto si aplica)
        - reflexion: exactamente 3 preguntas abiertas y específicas de esta sección:
            1. ¿Qué harías si...? (situación técnica realista)
            2. Conectada con un error típico en empresa/FCT
            3. Que relacione con otro módulo del ciclo o con FCT
        Solo JSON válido, sin texto extra.
    """)
    try:
        raw = ia._llamar(system_ia, meta_prompt,
                         max_tokens=1000, modelo=modelo, temperatura=0.3)
        return _parsear_json_ia(raw, f"meta:{sec_title}") or {}
    except Exception as exc:
        print(f"  ⚠️  meta_pedagogica({sec_title}): {exc}")
        return {}


def _secciones_ia(mod, ut: dict, ia) -> list[dict]:
    """
    Genera secciones con contenido real via IA.

    Arquitectura en DOS FASES para máxima calidad:
      Fase 1 — Outline: una llamada pequeña planifica las secciones de contenido
               (IDs, títulos, emoji, 2-3 frases de qué debe cubrir cada una)
      Fase 2 — Contenido: una llamada por sección con 8 000 tokens completos
               → cada sección recibe presupuesto total, sin competir con las demás
    Resultado: 10-12 secciones ricas en lugar de 7 secciones superficiales.
    """
    import json

    # ── Preparar contexto del módulo / UT ────────────────────────────────────
    ras = _ras_de_ut(mod, ut["id"])
    ras_full = []
    for ra_id in ras:
        ra_obj = next((r for r in mod.RAS if r["id"] == ra_id), None)
        ras_full.append(
            f"{ra_id}: {ra_obj.get('nombre','')}" if ra_obj else ra_id
        )

    ces_por_ra = _ces_por_ra_modulo(mod)
    ces_ut: list[str] = []
    for ra_id in ras:
        for ce_id in ces_por_ra.get(ra_id, []):
            ce_texto = ''
            ces_dict = mod.CES if hasattr(mod, 'CES') else {}
            for ce in ces_dict.get(ra_id, []):
                if (ce if isinstance(ce, str) else ce.get('id', '')) == ce_id:
                    ce_texto = ce if isinstance(ce, str) else ce.get('texto', '')
            ces_ut.append(f"{ce_id}: {ce_texto}" if ce_texto else ce_id)

    ces_str     = "\n".join(f"  - {c}" for c in ces_ut) if ces_ut else "  (sin CEs especificados)"
    ras_full_str = "\n".join(f"  - {r}" for r in ras_full)

    portada_html = (
        f'<div class="text-center py-8 mb-4 flex flex-col justify-center min-h-[55vh]">\n'
        f'  <div class="inline-block bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full mb-4 mx-auto">{_ciclo_badge(mod)}</div>\n'
        f'  <h1 class="text-4xl text-slate-900 leading-tight mb-2">{ut["nombre"]}</h1>\n'
        f'  <p class="text-base text-slate-400 font-medium max-w-2xl mx-auto italic mb-6">'
        f'{ut["id"]} · {mod.MODULO["abrev"]} — {mod.MODULO["nombre"]} · {mod.MODULO["curso"]} · {mod.MODULO["anno"]}</p>\n'
        f'  <div class="grid grid-cols-2 gap-3 text-left max-w-sm mx-auto mb-6">\n'
        f'    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">\n'
        f'      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Autora</span>\n'
        f'      <span class="text-sm font-bold text-slate-800">Isabel López</span>\n'
        f'    </div>\n'
        f'    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">\n'
        f'      <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Curso</span>\n'
        f'      <span class="text-sm font-bold text-slate-800">{mod.MODULO["anno"]}</span>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'  <div class="inline-flex items-center gap-2 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5 mx-auto">\n'
        f'    <span class="text-xs font-bold text-green-800">📄 Licencia CC BY 4.0</span>\n'
        f'  </div>\n'
        f'</div>'
    )

    ctx_base = textwrap.dedent(f"""\
        Módulo: {mod.MODULO['nombre']}
        Ciclo / Familia profesional: {mod.MODULO['ciclo']}
        Curso / Nivel: {mod.MODULO['curso']}
        UT: {ut['id']} — {ut['nombre']}
        Horas: {ut.get('horas','—')} · Eval: EV{ut.get('eval','?')}
        Tags: {ut.get('tags','(sin especificar)')}
        RAs:
{ras_full_str}
        CEs:
{ces_str}""")

    import time as _time
    system_ia  = _make_system_ia(mod.MODULO['ciclo'], mod.MODULO['curso'])
    _t0        = _time.time()

    def _elapsed() -> str:
        s = int(_time.time() - _t0)
        return f"{s//60}m {s%60:02d}s" if s >= 60 else f"{s}s"

    def _fase(msg: str):
        print(f"EVALFP_FASE: {msg}", flush=True)

    def _paso(msg: str):
        print(f"EVALFP_PASO:   {msg}", flush=True)

    def _ok(msg: str):
        print(f"EVALFP_OK: {msg}", flush=True)

    def _cont(msg: str):
        print(f"EVALFP_CONT:   {msg}", flush=True)

    # ── Selección de modelos según proveedor ─────────────────────────────────
    _MODELOS_APUNTES = {
        "claude": "claude-sonnet-4-6",
        "openai": "gpt-4o",
    }
    MODELO_APUNTES = _MODELOS_APUNTES.get(ia._proveedor)

    # Temperatura baja para apuntes: más densidad técnica, menos variación creativa
    TEMP_APUNTES = 0.4

    _fase(f"Iniciando generación — {ut['nombre']}")
    if MODELO_APUNTES:
        _paso(f"Proveedor: {ia._proveedor.upper()} · Modelo: {MODELO_APUNTES} · Temp: {TEMP_APUNTES}")
    else:
        _paso("Modo DEMO — sin llamadas a API")

    # ── FASE 1: Outline ───────────────────────────────────────────────────────
    _fase("Fase 1 — Planificando estructura del documento…")
    outline_prompt = textwrap.dedent(f"""\
        {ctx_base}

        Tu tarea: planificar las secciones de contenido de estos apuntes (NO generes el HTML todavía).

        Devuelve ÚNICAMENTE un array JSON con 8-12 secciones de CONTENIDO (sin portada, sin ejercicios,
        sin autoevaluación, sin glosario — esas se generan aparte).

        Cada elemento del array debe tener:
          - "id": string en kebab-case descriptivo del subtema (ej: "tipos-kernel", "instalacion-ubuntu")
          - "icon": emoji relevante
          - "title": título corto con número (ej: "2. Tipos y arquitectura del kernel")
          - "scope": lista de 5-8 puntos concretos que la sección DEBE cubrir para agotar
                     completamente los RAs y CEs indicados (cada punto = un concepto, procedimiento
                     o comparativa específica, con valores reales, versiones o comandos exactos)

        Reglas:
        - Secciones ordenadas de menor a mayor complejidad (contexto → conceptos → procedimientos → diagnóstico)
        - Cada sección debe cubrir UN tema bien acotado, no varios temas mezclados
        - Las secciones deben ser suficientemente distintas entre sí (no duplicar contenido)
        - Cubre TODO lo necesario para que un alumno pueda superar los CEs listados

        Responde SOLO con el array JSON, sin markdown ni explicaciones.
    """)

    raw_outline = ia._llamar(system_ia, outline_prompt, max_tokens=2500, modelo=MODELO_APUNTES, temperatura=TEMP_APUNTES)
    outline = _parsear_json_ia(raw_outline, "outline")

    if not outline or not isinstance(outline, list):
        _paso("⚠️  No se pudo generar el outline. Usando modo DEMO.")
        return _secciones_demo(mod, ut)

    _ok(f"Estructura lista — {len(outline)} secciones de contenido ({_elapsed()})")
    for s in outline:
        _paso(f"{s.get('icon','·')} {s.get('title', s.get('id','?'))}")

    # ── FASE 2: Contenido sección a sección ──────────────────────────────────
    outline_resumen = "\n".join(
        f"  - {s.get('id','?')}: {s.get('title','')}" for s in outline
    )

    secciones: list[dict] = [
        {"id": "inicio", "icon": "🏠", "title": "Portada", "html": portada_html}
    ]

    # Secciones especiales fijas al final
    SECCIONES_FIJAS = ["ejercicios", "autoevaluacion", "glosario"]
    specs_fijas = {
        "ejercicios": {
            "id": "ejercicios", "icon": "📝", "title": "Ejercicios prácticos",
            "scope": (
                "4 bloques: "
                "(1) Análisis conceptual: 3 preguntas abiertas con área de respuesta punteada (min-h-12); "
                "(2) Cálculo/Comparativa: tabla de datos + espacio de resolución; "
                "(3) Práctica terminal: comandos reales con preguntas de reflexión sobre la salida; "
                "(4) Caso de diseño: callout-warning con escenario empresarial real y tarea de diseño."
            ),
        },
        "autoevaluacion": {
            "id": "autoevaluacion", "icon": "✅", "title": "Autoevaluación",
            "scope": (
                "14-16 preguntas tipo test, 4 opciones cada una (a/b/c/d), "
                "cada pregunta en bg-yellow-50 con pista breve, "
                "clave de respuestas al final en grid de 4 columnas."
            ),
        },
        "glosario": {
            "id": "glosario", "icon": "📖", "title": "Glosario",
            "scope": (
                "20+ términos técnicos clave de la UT, cada uno como tarjeta con barra azul lateral: "
                '<div class="bg-white border border-slate-200 rounded-xl p-3 flex gap-3 shadow-sm">'
                '<div class="w-1 bg-blue-500 rounded-full flex-shrink-0"></div>'
                '<div><strong class="text-slate-800 text-sm">Término</strong>'
                '<p class="text-xs text-slate-600 mt-0.5">Definición completa.</p></div></div>'
            ),
        },
    }

    todas_secciones = list(outline) + [specs_fijas[k] for k in SECCIONES_FIJAS]
    n_total = len(todas_secciones)

    _fase(f"Fase 2 — Generando {n_total} secciones (esto puede tardar varios minutos)…")

    for i, spec in enumerate(todas_secciones, 1):
        sec_id    = spec.get("id", f"seccion{i}")
        sec_title = spec.get("title", sec_id)
        sec_scope = spec.get("scope", "")
        es_fija   = sec_id in SECCIONES_FIJAS

        _paso(f"[{i}/{n_total}] {spec.get('icon','📄')} {sec_title}  ({_elapsed()} transcurridos)")

        # Convertir scope a lista de puntos si viene como string
        if isinstance(sec_scope, list):
            scope_str = "\n".join(f"  • {p}" for p in sec_scope)
        else:
            scope_str = str(sec_scope)

        # (Los bloques pedagógicos CE chips / errores / reflexión se generan
        #  DESPUÉS de obtener el HTML, mediante _meta_pedagogica() + helpers Python,
        #  para garantizar el estilo correcto sin depender del formato del AI.)

        instrucciones_visuales = textwrap.dedent("""\
            COMPONENTES OBLIGATORIOS en el cuerpo de la sección (usa al menos 4 tipos):
            - <h3> subsecciones (mínimo 3-4 por cada <h2>) con párrafos explicativos
            - Párrafos narrativos (3-5 párrafos por concepto clave, SIN listas de bullets)
            - Callout info/warning/success/danger (bg-blue-50/yellow-50/green-50/red-50) para avisos
            - Bloque de código comentado línea a línea: <div class="code-block my-4">...</div> — SIEMPRE elemento standalone, NUNCA dentro de un <p>
            - Tabla con cabecera oscura (bg-slate-700 text-white) para comparativas
            - Tarjetas cronología (badge año + título + párrafo) para evolución histórica
            - Pasos numerados (span redondeado bg-blue-600 + h4 + párrafo) para procedimientos
            - Grid tarjetas coloreadas (bg-blue-50/green-50/purple-50/orange-50) para clasificaciones
            - Diagrama capas (divs apilados + flecha) para arquitecturas
            - Flujo borde lateral (border-l-4) para resolución de problemas paso a paso
        """)

        sec_prompt = textwrap.dedent(f"""\
            {ctx_base}

            Secciones de estos apuntes (para referencias cruzadas):
            {outline_resumen}

            ═══════════════════════════════════════════════════════
            GENERA LA SECCIÓN: "{sec_title}" (id="{sec_id}")
            ═══════════════════════════════════════════════════════

            Puntos que DEBES cubrir (NO omitas ninguno — desarrolla cada uno en profundidad):
{scope_str}

            {instrucciones_visuales}

            REQUISITOS DE LONGITUD Y CALIDAD (OBLIGATORIOS):
            ─────────────────────────────────────────────────
            • MÍNIMO 2000 palabras de texto explicativo (sin contar etiquetas HTML)
            • Al menos 4 subsecciones <h3> dentro de esta sección
            • Para cada concepto clave: párrafo "sin esto no existiría X porque...",
              luego definición técnica exacta, luego analogía cotidiana, luego implicación profesional
            • Valores numéricos concretos, versiones reales, comandos con flags exactos
            • Si hay procedimientos: pasos detallados con justificación de cada paso
            • Si hay comparativas: tabla completa con ≥4 opciones y criterios reales
            • Conexiones explícitas con otros módulos del ciclo cuando sean relevantes
            • NO resumir — desarrollar. Cada punto del scope merece al menos
              3-4 párrafos de explicación más un componente visual diferente

            NO pares hasta haber cubierto TODOS los puntos del scope con esa profundidad.
            Nivel: libro de texto universitario adaptado a {mod.MODULO['ciclo']}.

            FORMATO DE RESPUESTA (MUY IMPORTANTE):
            • Solo HTML estático — CERO JavaScript, CERO <script>, CERO expresiones ${"{...}"}
            • CERO backticks (`), CERO bloques markdown (```), CERO JSON
            • CERO comentarios del tipo "Aquí va..." o "Continuación de..."
            • NO reproduzcas el bloque de contexto (Módulo:, Ciclo:, UT:…) — es solo para tu referencia
            • Empieza directamente con el <h2> del título de la sección, sin ningún texto previo
        """)

        max_tok  = 8000 if es_fija else 12000
        raw_html = ia._llamar(system_ia, sec_prompt, max_tokens=max_tok, modelo=MODELO_APUNTES, temperatura=TEMP_APUNTES)
        html_limpio = _limpiar_html_ia(raw_html)

        _ok(f"[{i}/{n_total}] ✓ {sec_title} — {len(html_limpio):,} caracteres")

        # Continuación: hasta 2 rondas si la sección queda corta
        # Umbral: 8 000 chars para fijas, 10 000 para contenido
        # Las secciones fijas solo hacen 1 ronda
        max_cont = 1 if es_fija else 2
        umbral   = 8000 if es_fija else 10000
        for ronda in range(1, max_cont + 1):
            if len(html_limpio) >= umbral:
                break
            _cont(f"Sección corta ({len(html_limpio):,} chars) — continuación {ronda}/{max_cont}…")
            cont_prompt = textwrap.dedent(f"""\
                {ctx_base}

                Estás generando la sección "{sec_title}" de los apuntes.
                Ya generaste este HTML (continúa desde aquí, NO lo repitas):

                --- ÚLTIMO FRAGMENTO GENERADO ---
                {html_limpio[-1200:]}
                --- FIN ---

                Puntos del scope que DEBES cubrir aún con detalle real:
{scope_str}

                Continúa el HTML directamente desde donde quedaste.
                NO repitas lo ya escrito. NO escribas comentarios introductorios.
                Mínimo 1 500 palabras adicionales con componentes visuales variados.
                SIN markdown, SIN ```, SIN backticks.
            """)
            cont_html = ia._llamar(system_ia, cont_prompt, max_tokens=max_tok, modelo=MODELO_APUNTES, temperatura=TEMP_APUNTES)
            cont_html = _limpiar_html_ia(cont_html)
            html_limpio = html_limpio + "\n" + cont_html
            _cont(f"  ↪ Total tras continuación {ronda}: {len(html_limpio):,} caracteres")

        # ── Bloques pedagógicos (Python genera el HTML estilizado, IA aporta contenido JSON) ──
        if not es_fija:
            _paso(f"  🎓 Metadatos pedagógicos: CEs · errores · reflexión…")
            meta = _meta_pedagogica(ia, system_ia, ctx_base, sec_title, MODELO_APUNTES)
            # 1. CE chips: inyectar justo después del primer <h2>
            ces_html = _html_ces(meta.get("ces", []))
            if ces_html:
                html_limpio = re.sub(
                    r'(<h2[^>]*>.*?</h2>)',
                    lambda m: m.group(1) + ces_html,
                    html_limpio, count=1, flags=re.DOTALL | re.IGNORECASE
                )
            # 2. Errores frecuentes + mini-reflexión: añadir al final de la sección
            html_limpio += (
                "\n" + _html_errores(meta.get("errores", []))
                + "\n" + _html_reflexion(meta.get("reflexion", []))
            )

        secciones.append({
            "id":    sec_id,
            "icon":  spec.get("icon", "📄"),
            "title": sec_title,
            "html":  html_limpio,
        })

    return secciones


# ─── Generador principal ──────────────────────────────────────────────────────

def generar_apunte(mod, ut: dict, ia, output_base: Path) -> Path:
    """Genera index.html para una UT. Devuelve el path del archivo creado."""
    import json

    print(f"  📄 {ut['id']}: {ut['nombre']}")

    if ia._proveedor == "demo":
        secciones = _secciones_demo(mod, ut)
    else:
        secciones = _secciones_ia(mod, ut, ia)

    # Serializar secciones a JSON válido para insertar en el script Vue.
    # Escapar '</' → '<\/' para que ningún '</script>' dentro del HTML de
    # una sección pueda cerrar prematuramente el bloque <script> del template.
    sections_json = json.dumps(secciones, ensure_ascii=False, indent=2)
    sections_json = sections_json.replace('</', '<\\/')

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

    opts    = _parse_opts(args, ["--modulo", "--datos", "--ut", "--salida", "--proveedor"])
    ut_id   = opts.get("--ut")
    salida  = Path(opts.get("--salida", str(Path(__file__).parent.parent / "apuntes")))
    proveedor = opts.get("--proveedor", "auto")

    # --datos (JSON de SQLite) tiene prioridad sobre --modulo (módulo Python estático)
    if opts.get("--datos"):
        mod = _cargar_desde_json(opts["--datos"])
    else:
        mod = _cargar_modulo(opts.get("--modulo", "iso_data"))

    from ai_asistente import IAAsistente
    ia = IAAsistente(proveedor=proveedor)

    # Aviso explícito si se pidió IA real pero no hay clave configurada
    if ia._proveedor == "demo" and proveedor in ("auto", "claude", "openai"):
        print("EVALFP_NO_KEY: Sin API key detectada. El contenido generado será de ejemplo (modo DEMO).")
        print("EVALFP_NO_KEY: Ve a Ajustes → API Keys y configura ANTHROPIC_API_KEY o OPENAI_API_KEY.")

    print(f"EVALFP_FASE: ▶  {mod.MODULO['abrev']} · {mod.MODULO['nombre']}", flush=True)
    print(f"EVALFP_PASO:   Proveedor: {ia._proveedor.upper()}  |  Destino: {salida}", flush=True)
    print(flush=True)

    import time as _time_cli
    _t_cli = _time_cli.time()
    archivos = generar_modulo(mod, ia, salida, ut_id)
    _dur = int(_time_cli.time() - _t_cli)
    _dur_str = f"{_dur//60}m {_dur%60:02d}s" if _dur >= 60 else f"{_dur}s"

    print(f"EVALFP_FASE: ✅  {len(archivos)} apunte(s) generado(s) en {_dur_str}", flush=True)
    for p in archivos:
        print(f"EVALFP_OK: 📄 {p}", flush=True)

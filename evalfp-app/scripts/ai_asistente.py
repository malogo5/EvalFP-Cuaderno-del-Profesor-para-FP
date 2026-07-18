"""
EvalFP — Asistente IA
=====================
Genera material didáctico profesional para módulos de FP, alineado con los
RA/CE del currículo oficial y con la programación real del profesor/a:

  1. Rúbricas de evaluación (4 niveles × CE, con descriptores observables)
  2. Situaciones de aprendizaje / actividades prácticas por RA
  3. Informes individuales de progreso del alumnado
  4. `todo`: rúbricas + actividades + apuntes de un módulo completo

Todo el material se guarda en una carpeta única organizada en subcarpetas:
    Material IA/<ABREV>/rubricas/     rubrica_RA1_20260708-1830.md
    Material IA/<ABREV>/actividades/  actividades_RA1_20260708-1830.md
    Material IA/<ABREV>/informes/     informe_Apellidos_Nombre_20260708.md
    Material IA/<ABREV>/apuntes/      04-FP/<ABREV>/.../index.html

Fuente de datos (por orden de prioridad):
    --datos <ruta.json>   Programación REAL del profesor exportada desde SQLite
                          (RAs con ponderaciones editadas, UTs, CEs, actividades)
    --modulo <clave>      Módulo estático scripts/modules/<clave>.py (legado)

Uso como CLI:
    python ai_asistente.py rubrica   --datos mod.json --ra RA1 --salida "Material IA/ISO"
    python ai_asistente.py actividad --datos mod.json --ra RA2 --n 3 --salida ...
    python ai_asistente.py informe   --datos mod.json --alumno "García, M." --notas "RA1:7,RA2:5" --salida ...
    python ai_asistente.py todo      --datos mod.json --salida ...

Dependencias opcionales: pip install anthropic | openai
Sin API key ni SDK → modo DEMO (texto de ejemplo sin llamada a API).
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

# ─── Constantes ──────────────────────────────────────────────────────────────

MODELO_CLAUDE  = os.environ.get("EVALFP_MODEL_CLAUDE", "claude-haiku-4-5-20251001")
MODELO_OPENAI  = os.environ.get("EVALFP_MODEL_OPENAI", "gpt-4o-mini")
MAX_TOKENS     = 4096          # las rúbricas de RAs con muchos CEs necesitan espacio
TEMPERATURA    = 0.6

NIVELES_RUBRICA = [
    ("No Alcanzado",  "0-4",  "NO demuestra el criterio o lo hace con errores graves."),
    ("En Proceso",    "5-6",  "Demuestra el criterio de forma básica o con apoyo."),
    ("Alcanzado",     "7-8",  "Demuestra el criterio de forma autónoma y correcta."),
    ("Sobresaliente", "9-10", "Demuestra el criterio con precisión, criterio propio y profundidad."),
]

SYSTEM_BASE = textwrap.dedent("""\
    Eres un/a docente experto/a de Formación Profesional del sistema educativo
    español, especialista en programación didáctica y evaluación por Resultados
    de Aprendizaje (RA) y Criterios de Evaluación (CE) conforme a la LOE/LOFP y
    a los Reales Decretos de título. Trabajas con rigor curricular:
    - Nunca inventas RA, CE ni contenidos ajenos al currículo facilitado.
    - Citas los CE SIEMPRE por su código oficial (p. ej. "CE b)" o "CR2").
    - Adaptas el nivel de exigencia y el lenguaje técnico al ciclo indicado
      (CFGB básico / CFGM medio / CFGS superior / CE curso de especialización).
    - Redactas en español de España, con precisión terminológica del sector.
    Responde SOLO con el contenido solicitado en Markdown, sin introducciones,
    disculpas ni metacomentarios.
""")


# ─── Motor IA ─────────────────────────────────────────────────────────────────

class IAAsistente:
    """Interfaz unificada Claude / OpenAI / Demo para generación de contenido FP."""

    def __init__(self, api_key: str | None = None, proveedor: str = "auto"):
        """proveedor: "claude" | "openai" | "demo" | "auto"."""
        self._proveedor, self._cliente = self._init_cliente(api_key, proveedor)

    # ── Inicialización ────────────────────────────────────────────────────────

    def _init_cliente(self, api_key: str | None, proveedor: str):
        if proveedor in ("demo",):
            return "demo", None

        if proveedor in ("claude", "auto"):
            key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if key:
                try:
                    import anthropic  # noqa: PLC0415
                    return "claude", anthropic.Anthropic(api_key=key)
                except ImportError:
                    if proveedor == "claude":
                        raise RuntimeError(
                            "SDK anthropic no instalado. Ejecuta: pip install anthropic"
                        )

        if proveedor in ("openai", "auto"):
            key = api_key or os.environ.get("OPENAI_API_KEY")
            if key:
                try:
                    import openai  # noqa: PLC0415
                    return "openai", openai.OpenAI(api_key=key)
                except ImportError:
                    if proveedor == "openai":
                        raise RuntimeError(
                            "SDK openai no instalado. Ejecuta: pip install openai"
                        )

        print(
            "[EvalFP IA] ⚠️  Sin API key ni SDK detectado → modo DEMO (texto de ejemplo).",
            file=sys.stderr,
        )
        return "demo", None

    # ── Llamada genérica ──────────────────────────────────────────────────────

    def _llamar(
        self,
        system: str,
        user: str,
        max_tokens: int | None = None,
        modelo: str | None = None,
        temperatura: float | None = None,
    ) -> str:
        if self._proveedor == "demo":
            return self._demo_response(user)

        _max   = max_tokens or MAX_TOKENS
        _temp  = temperatura if temperatura is not None else TEMPERATURA

        if self._proveedor == "claude":
            msg = self._cliente.messages.create(
                model=modelo or MODELO_CLAUDE,
                max_tokens=_max,
                temperature=_temp,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return msg.content[0].text

        if self._proveedor == "openai":
            resp = self._cliente.chat.completions.create(
                model=modelo or MODELO_OPENAI,
                max_tokens=_max,
                temperature=_temp,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
            )
            return resp.choices[0].message.content

        raise RuntimeError(f"Proveedor desconocido: {self._proveedor}")

    @staticmethod
    def _demo_response(prompt: str) -> str:
        return (
            "[DEMO — sin API key] Este es un texto de ejemplo generado localmente.\n"
            "Para obtener contenido real, configura tu API key en Ajustes "
            "y vuelve a ejecutar el asistente.\n\n"
            f"Prompt recibido (primeros 300 chars):\n{prompt[:300]}…"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # FUNCIONES PÚBLICAS
    # ══════════════════════════════════════════════════════════════════════════

    def descriptores_rubrica(
        self,
        ra: dict[str, Any],
        ces_detalle: list[dict[str, str]],
        modulo: dict[str, Any],
        instrumentos: list[str] | None = None,
    ) -> str:
        """
        Rúbrica profesional para un RA: descriptores observables y medibles
        por CE (texto oficial completo) en 4 niveles de logro.
        """
        system = SYSTEM_BASE + textwrap.dedent("""\

            Especialización de esta tarea: RÚBRICAS DE EVALUACIÓN.
            - Cada descriptor debe ser OBSERVABLE y MEDIBLE (verbos de acción,
              evidencias concretas), no vago ("entiende", "conoce" ✗).
            - Los 4 niveles de cada CE deben ser claramente discriminables
              entre sí y progresivos.
            - Usa temperatura baja: precisión antes que creatividad.
        """)

        ces_lista = "\n".join(
            f"  - {ce['id']}: {ce.get('texto', '(sin texto)')}" for ce in ces_detalle
        ) or "  (El currículo no detalla CEs para este RA: deriva 4-6 indicadores del enunciado del RA.)"
        instr = f"\nInstrumentos previstos en la programación: {', '.join(instrumentos)}." if instrumentos else ""

        user = textwrap.dedent(f"""\
            CONTEXTO CURRICULAR
            Módulo: {modulo.get('nombre','?')} ({modulo.get('abrev','')})
            Ciclo: {modulo.get('ciclo','')} — {modulo.get('curso','')} · {modulo.get('horas','?')} h
            {('Normativa: ' + modulo['decreto']) if modulo.get('decreto') else ''}
            Resultado de Aprendizaje: {ra['id']} — {ra['nombre']}
            Ponderación en la nota final: {ra.get('pond','?')}%{instr}

            Criterios de Evaluación oficiales (código: texto):
{ces_lista}

            TAREA
            Genera una rúbrica de evaluación completa en Markdown:

            1. Tabla con una fila por CE y estas columnas:
               | CE | Criterio (resumen ≤12 palabras) | No Alcanzado (0-4) | En Proceso (5-6) | Alcanzado (7-8) | Sobresaliente (9-10) |
               Cada celda de nivel: 1-2 frases con descriptores OBSERVABLES
               (qué hace, produce o demuestra el alumno/a, con qué calidad).
            2. Fila final "**RA global**" con la descripción general de cada nivel.
            3. Sección "**Evidencias de evaluación**": para cada CE, qué evidencia
               concreta recoger (entregable, observación, pregunta de examen…).
            4. Sección "**Instrucciones de aplicación**": cómo puntuar (nota del CE
               = nivel alcanzado; nota del RA = media de CEs), qué hacer con CEs
               no evaluables en el trimestre y recordatorio de que el RA se supera
               con nota ≥5.

            No inventes CEs: usa exactamente los códigos facilitados.
        """)

        return self._llamar(system, user, max_tokens=MAX_TOKENS, temperatura=0.3)

    def propuesta_actividades(
        self,
        ra: dict[str, Any],
        ces_detalle: list[dict[str, str]],
        modulo: dict[str, Any],
        n_actividades: int = 3,
        uts_ra: list[dict] | None = None,
        plan_existente: list[str] | None = None,
    ) -> str:
        """
        Situaciones de aprendizaje / actividades profesionales para un RA,
        coherentes con las UTs reales (nombre y horas) y el plan del profesor.
        """
        system = SYSTEM_BASE + textwrap.dedent("""\

            Especialización de esta tarea: DISEÑO DE SITUACIONES DE APRENDIZAJE.
            - Contextualiza SIEMPRE en un escenario laboral realista del sector.
            - Cada actividad debe poder evaluarse con los CE indicados: no
              propongas nada que no genere evidencias de esos CE.
            - La duración debe ser coherente con las horas de las UTs indicadas.
            - Incluye atención a la diversidad (refuerzo y ampliación) y, si
              procede, prevención de riesgos y uso responsable de la tecnología.
        """)

        ces_lista = "\n".join(
            f"  - {ce['id']}: {ce.get('texto', '(sin texto)')}" for ce in ces_detalle
        ) or "  (Sin CEs detallados: alinea con el enunciado del RA.)"
        uts_str = ""
        if uts_ra:
            uts_str = "\nUnidades de trabajo que desarrollan este RA:\n" + "\n".join(
                f"  - {u.get('id','?')}: {u.get('nombre','')} ({u.get('horas','?')} h, {int(u.get('eval',1))}ª evaluación)"
                for u in uts_ra
            )
        plan_str = ""
        if plan_existente:
            plan_str = "\nInstrumentos ya previstos en la programación (NO los dupliques, complétalos):\n" + \
                       "\n".join(f"  - {p}" for p in plan_existente)

        user = textwrap.dedent(f"""\
            CONTEXTO CURRICULAR
            Módulo: {modulo.get('nombre','?')} ({modulo.get('abrev','')})
            Ciclo: {modulo.get('ciclo','')} — {modulo.get('curso','')} · {modulo.get('horas','?')} h
            {('Normativa: ' + modulo['decreto']) if modulo.get('decreto') else ''}
            Resultado de Aprendizaje: {ra['id']} — {ra['nombre']} (pondera {ra.get('pond','?')}% de la nota final)

            Criterios de Evaluación oficiales:
{ces_lista}{uts_str}{plan_str}

            TAREA
            Diseña {n_actividades} actividades/situaciones de aprendizaje. Para CADA una:

            ## A{{n}}. {{Título profesional y descriptivo}}
            - **Escenario profesional**: contexto laboral realista (empresa/encargo) del sector.
            - **Objetivo didáctico**: qué evidencia el alumnado, vinculado a los CE por código.
            - **CE evaluados**: lista de códigos + cómo lo evidencia cada uno.
            - **Desarrollo por sesiones**: pasos numerados con tiempos (sesiones de 55 min).
            - **Entregables**: qué se entrega, formato y condiciones.
            - **Criterios de corrección**: reparto de puntos sobre 10 ligado a los CE.
            - **Recursos**: software (versiones), hardware, material.
            - **Atención a la diversidad**: 1 adaptación de refuerzo + 1 de ampliación.
            - **Duración total**: horas (coherente con las UTs indicadas).

            Las {n_actividades} actividades deben ser complementarias entre sí
            (no variantes de la misma) y cubrir entre todas el máximo de CEs.
        """)

        return self._llamar(system, user, max_tokens=MAX_TOKENS, temperatura=0.6)

    def borrador_informe_alumno(
        self,
        alumno: str,
        modulo: dict[str, Any],
        notas_ra: dict[str, float],
        ras_modulo: list[dict] | None = None,
        observaciones: str = "",
    ) -> str:
        """
        Informe individual de progreso. Riguroso con la normativa:
        - Solo usa los RA con nota real (NUNCA inventa calificaciones).
        - Nota media reponderada sobre los RA evaluados.
        - Regla de oro: el módulo solo se supera con TODOS los RA ≥5.
        """
        system = SYSTEM_BASE + textwrap.dedent("""\

            Especialización de esta tarea: INFORMES DE PROGRESO AL ALUMNADO Y FAMILIAS.
            - Tono profesional, constructivo y respetuoso; sin jerga innecesaria.
            - Sé específico: referencia los RA por su código y nombre corto.
            - No inventes datos: si un RA no tiene nota, es "pendiente de evaluar".
            - El feedforward debe ser accionable (qué hacer, cómo y para cuándo).
        """)

        ras_modulo = ras_modulo or []
        pond = {r["id"]: r.get("pond", 0) for r in ras_modulo}
        nombre_ra = {r["id"]: r.get("nombre", "") for r in ras_modulo}

        # Media reponderada sobre los RA con nota (H10) — jamás inventar notas
        con_nota = [(ra, n) for ra, n in notas_ra.items()]
        pond_sum = sum(pond.get(ra, 0) for ra, _ in con_nota)
        if con_nota and pond_sum > 0:
            media = sum(n * pond.get(ra, 0) for ra, n in con_nota) / pond_sum
        elif con_nota:
            media = sum(n for _, n in con_nota) / len(con_nota)
        else:
            media = None

        suspensos   = sorted(ra for ra, n in con_nota if n < 5)
        aprobados   = sorted(ra for ra, n in con_nota if n >= 5)
        sin_evaluar = sorted(r["id"] for r in ras_modulo if r["id"] not in notas_ra)

        if media is None:
            estado = "SIN CALIFICACIONES REGISTRADAS"
        elif sin_evaluar:
            estado = f"EVALUACIÓN PARCIAL — pendientes de evaluar: {', '.join(sin_evaluar)}"
        elif suspensos:
            estado = f"NO SUPERADO — RA pendientes: {', '.join(suspensos)} (la media no compensa un RA suspenso)"
        else:
            estado = "SUPERADO — todos los RA ≥ 5"

        notas_str = "\n".join(
            f"  {ra}: {n:.1f}/10 — {nombre_ra.get(ra, '')[:70]}"
            for ra, n in sorted(con_nota)
        ) or "  (sin notas registradas)"
        obs_str = f"\nObservaciones del profesor/a:\n{observaciones}" if observaciones else ""

        user = textwrap.dedent(f"""\
            DATOS DEL INFORME (usa EXCLUSIVAMENTE estos datos)
            Alumno/a: {alumno}
            Módulo: {modulo.get('nombre','?')} ({modulo.get('abrev','')})
            Ciclo: {modulo.get('ciclo','')} — {modulo.get('curso','')} — Curso {modulo.get('anno','')}

            Calificaciones por Resultado de Aprendizaje (0-10):
{notas_str}

            Media ponderada de los RA evaluados: {f'{media:.2f}' if media is not None else '—'}
            RA aprobados: {', '.join(aprobados) or '—'}
            RA suspensos: {', '.join(suspensos) or '—'}
            RA aún sin evaluar: {', '.join(sin_evaluar) or '—'}
            Situación del módulo: {estado}{obs_str}

            TAREA
            Redacta el informe individual (4-5 párrafos, Markdown, encabezado con
            los datos identificativos):
            1. Contexto: módulo, periodo y alcance de la evaluación.
            2. Logros: qué competencias demuestran los RA aprobados (por código).
            3. Dificultades: análisis de los RA suspensos y posibles causas observables.
            4. Plan de mejora (feedforward): 3-4 acciones CONCRETAS con plazo, ligadas
               a la recuperación de los RA pendientes.
            5. Cierre: situación normativa del módulo ({estado}) explicada con claridad
               —incluida, si procede, la regla de que la media no compensa un RA
               suspenso— y mensaje de ánimo realista.
        """)

        return self._llamar(system, user, max_tokens=2048, temperatura=0.5)

    def generar_todo_modulo(
        self,
        mod,
        output_dir: str | Path = ".",
    ) -> list[Path]:
        """
        Genera para un módulo completo, en subcarpetas organizadas:
          <salida>/rubricas/rubrica_RA1_<fecha>.md
          <salida>/actividades/actividades_RA1_<fecha>.md
        Devuelve la lista de paths generados.
        """
        out = Path(output_dir)
        archivos: list[Path] = []
        modulo = mod.MODULO
        ces_por_ra = _ces_detalle_por_ra(mod)
        uts_por_ra = _uts_por_ra(mod)

        for ra in mod.RAS:
            ra_id = ra["id"]
            ces   = ces_por_ra.get(ra_id, [])

            print(f"EVALFP_PASO: ✏️  Rúbrica {ra_id}…")
            rubrica = self.descriptores_rubrica(ra, ces, modulo, _instrumentos_ra(mod, ra_id))
            archivos.append(_guardar(
                out, "rubricas", f"rubrica_{ra_id.lower()}",
                _cabecera("Rúbrica de evaluación", ra_id, ra, modulo) + rubrica,
            ))

            print(f"EVALFP_PASO: 🔧 Actividades {ra_id}…")
            actividades = self.propuesta_actividades(
                ra, ces, modulo, 3, uts_por_ra.get(ra_id, []), _plan_ra(mod, ra_id))
            archivos.append(_guardar(
                out, "actividades", f"actividades_{ra_id.lower()}",
                _cabecera("Situaciones de aprendizaje", ra_id, ra, modulo) + actividades,
            ))

        return archivos


# ─── Datos del módulo ─────────────────────────────────────────────────────────

class _ModDesdeJson:
    """
    Adapta el JSON exportado desde SQLite (programación real del profesor)
    a la interfaz de los módulos Python estáticos:
      MODULO, UTS, RAS, CES, ASIGNACIONES (+ ACTIVIDADES, EVAL_RAS, MINEXAM)
    """
    def __init__(self, data: dict):
        self.MODULO = {
            "nombre":  data.get("nombre", data.get("abrev", "?")),
            "abrev":   data.get("abrev", "?"),
            "ciclo":   data.get("ciclo", "FP"),
            "curso":   data.get("curso", ""),
            "anno":    data.get("anno", ""),
            "horas":   data.get("horas", 0),
            "decreto": data.get("decreto", ""),
        }
        self.UTS  = data.get("uts", [])
        self.RAS  = data.get("ras", [])
        self.CES  = data.get("ces", {})
        self.ASIGNACIONES = [
            (a["ut"], a["ra"], a.get("ces", []))
            for a in data.get("asignaciones", [])
        ]
        self.ACTIVIDADES = data.get("actividades", [])
        self.EVAL_RAS    = data.get("eval_ras", {})
        self.MINEXAM     = data.get("minexam")


def _cargar_datos_o_modulo(opts: dict[str, str]):
    """--datos (JSON real, prioridad) o --modulo (estático legado)."""
    if opts.get("--datos"):
        with open(opts["--datos"], encoding="utf-8") as f:
            return _ModDesdeJson(json.load(f))
    return _cargar_modulo(opts.get("--modulo", "iso_data"))


def _cargar_modulo(nombre: str):
    """Importa un módulo de datos estático por nombre (iso_data, par_data, …)."""
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    import importlib
    nombre_limpio = nombre.replace("scripts/modules/", "").replace(".py", "")
    try:
        return importlib.import_module(f"modules.{nombre_limpio}")
    except ModuleNotFoundError:
        print(f"❌ No se encontró el módulo '{nombre_limpio}' en scripts/modules/")
        sys.exit(1)


def _ces_detalle_por_ra(mod) -> dict[str, list[dict]]:
    """
    {ra_id: [{id, texto}, …]} con el TEXTO oficial de cada CE.
    Prioriza mod.CES (textos completos); si no, los códigos de ASIGNACIONES.
    """
    detalle: dict[str, list[dict]] = {}
    ces_map = getattr(mod, "CES", {}) or {}

    # Códigos cubiertos por asignaciones (respetan la selección del profesor)
    codigos: dict[str, list[str]] = {}
    for _ut, ra_id, ces in getattr(mod, "ASIGNACIONES", []):
        codigos.setdefault(ra_id, [])
        for ce in ces:
            if ce not in codigos[ra_id]:
                codigos[ra_id].append(ce)

    for ra in getattr(mod, "RAS", []):
        ra_id = ra["id"]
        completos = ces_map.get(ra_id, [])
        if completos:
            sel = codigos.get(ra_id)
            detalle[ra_id] = (
                [ce for ce in completos if ce["id"] in sel] if sel else list(completos)
            ) or list(completos)
        else:
            detalle[ra_id] = [{"id": c, "texto": ""} for c in codigos.get(ra_id, [])]
    return detalle


def _uts_por_ra(mod) -> dict[str, list[dict]]:
    """{ra_id: [ut, …]} — UTs que desarrollan cada RA según asignaciones."""
    ut_map = {u.get("id"): u for u in getattr(mod, "UTS", [])}
    res: dict[str, list[dict]] = {}
    for ut_id, ra_id, _ces in getattr(mod, "ASIGNACIONES", []):
        u = ut_map.get(ut_id)
        if u and u not in res.setdefault(ra_id, []):
            res[ra_id].append(u)
    return res


def _plan_ra(mod, ra_id: str) -> list[str]:
    """Instrumentos ya planificados para un RA en la programación real."""
    return [
        f"{a.get('instrumento', a.get('tipo','?'))} · «{a.get('descripcion','')}» (peso {a.get('peso',0)}%, {int(a.get('eval',1))}ª ev.)"
        for a in getattr(mod, "ACTIVIDADES", [])
        if str(a.get("ra_id")) == str(ra_id)
    ]


def _instrumentos_ra(mod, ra_id: str) -> list[str]:
    tipos = {a.get("instrumento", a.get("tipo")) for a in getattr(mod, "ACTIVIDADES", [])
             if str(a.get("ra_id")) == str(ra_id)}
    return sorted(t for t in tipos if t)


# ─── Guardado organizado ──────────────────────────────────────────────────────

def _slug(texto: str, maxlen: int = 60) -> str:
    t = texto.strip()
    for a, b in zip("áéíóúÁÉÍÓÚñÑüÜ", "aeiouAEIOUnNuU"):
        t = t.replace(a, b)
    t = re.sub(r"[^\w\-. ]", "", t).strip().replace(" ", "_")
    return t[:maxlen] or "documento"


def _guardar(base: Path, subcarpeta: str, nombre: str, contenido: str) -> Path:
    """Guarda en <base>/<subcarpeta>/<nombre>_<fecha>.md y anuncia la ruta."""
    carpeta = Path(base) / subcarpeta
    carpeta.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    destino = carpeta / f"{_slug(nombre)}_{stamp}.md"
    destino.write_text(contenido, encoding="utf-8")
    print(f"💾 Guardado: {destino}")
    return destino


def _cabecera(tipo: str, ra_id: str, ra: dict, modulo: dict) -> str:
    return (
        f"# {tipo} — {ra_id}: {ra.get('nombre','')}\n\n"
        f"**Módulo:** {modulo.get('nombre','')} ({modulo.get('abrev','')})  \n"
        f"**Ciclo:** {modulo.get('ciclo','')} — {modulo.get('curso','')}  \n"
        f"**Ponderación del RA:** {ra.get('pond','?')}%  \n"
        + (f"**Normativa:** {modulo['decreto']}  \n" if modulo.get('decreto') else "")
        + f"**Generado:** {datetime.now().strftime('%d/%m/%Y %H:%M')} · EvalFP Asistente IA (borrador para revisión docente)\n\n---\n\n"
    )


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _parse_notas(notas_str: str) -> dict[str, float]:
    """Parsea "RA1:7,RA2:5.5" → {"RA1": 7.0, "RA2": 5.5} (ignora entradas malformadas)."""
    resultado = {}
    for parte in notas_str.split(","):
        if ":" not in parte:
            continue
        ra, _, nota = parte.strip().partition(":")
        try:
            resultado[ra.strip()] = float(nota.strip())
        except ValueError:
            continue
    return resultado


def _cmd_rubrica(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--datos", "--ra", "--proveedor", "--salida"])
    mod = _cargar_datos_o_modulo(opts)
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    ces = _ces_detalle_por_ra(mod).get(ra_id, [])
    out = ia.descriptores_rubrica(ra, ces, mod.MODULO, _instrumentos_ra(mod, ra_id))
    print(f"\n{'='*60}\nRÚBRICA — {ra_id}: {ra['nombre']}\n{'='*60}\n")
    print(out)
    if opts.get("--salida"):
        _guardar(Path(opts["--salida"]), "rubricas", f"rubrica_{ra_id.lower()}",
                 _cabecera("Rúbrica de evaluación", ra_id, ra, mod.MODULO) + out)


def _cmd_actividad(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--datos", "--ra", "--n", "--proveedor", "--salida"])
    mod = _cargar_datos_o_modulo(opts)
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    n = max(1, min(10, int(opts.get("--n", "3"))))
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    ces = _ces_detalle_por_ra(mod).get(ra_id, [])
    out = ia.propuesta_actividades(ra, ces, mod.MODULO, n,
                                   _uts_por_ra(mod).get(ra_id, []), _plan_ra(mod, ra_id))
    print(f"\n{'='*60}\nACTIVIDADES — {ra_id}: {ra['nombre']}\n{'='*60}\n")
    print(out)
    if opts.get("--salida"):
        _guardar(Path(opts["--salida"]), "actividades", f"actividades_{ra_id.lower()}",
                 _cabecera("Situaciones de aprendizaje", ra_id, ra, mod.MODULO) + out)


def _cmd_informe(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--datos", "--alumno", "--notas", "--proveedor", "--salida", "--observaciones"])
    mod    = _cargar_datos_o_modulo(opts)
    alumno = opts.get("--alumno", "Alumno/a")
    notas  = _parse_notas(opts.get("--notas", ""))
    if not notas:
        print("❌ Sin notas por RA (--notas \"RA1:7,RA2:5\"). No se genera informe sin datos reales.")
        sys.exit(1)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.borrador_informe_alumno(alumno, mod.MODULO, notas, mod.RAS,
                                     opts.get("--observaciones", ""))
    print(f"\n{'='*60}\nINFORME INDIVIDUAL — {alumno}\n{'='*60}\n")
    print(out)
    if opts.get("--salida"):
        _guardar(Path(opts["--salida"]), "informes", f"informe_{_slug(alumno)}", out)


def _cmd_generar_todo(args: list[str]):
    opts      = _parse_opts(args, ["--modulo", "--datos", "--salida", "--proveedor"])
    mod       = _cargar_datos_o_modulo(opts)
    abrev     = mod.MODULO["abrev"]
    salida    = Path(opts.get("--salida", f"Material IA/{abrev}"))
    ia        = IAAsistente(proveedor=opts.get("--proveedor", "auto"))

    print(f"EVALFP_FASE: Generando material completo del módulo {abrev} → {salida}")
    archivos = ia.generar_todo_modulo(mod, salida)

    # Apuntes HTML por UT
    print("EVALFP_FASE: 📄 Apuntes HTML por unidad de trabajo")
    try:
        from build_apuntes import generar_apunte
        apuntes_base = salida / "apuntes"
        for ut in mod.UTS:
            print(f"EVALFP_PASO: 📄 {ut['id']}: {ut['nombre']}")
            try:
                out_path = generar_apunte(mod, ut, ia, apuntes_base)
                archivos.append(out_path)
                print(f"EVALFP_OK: {out_path.name}")
            except Exception as e:
                print(f"⚠️  Error en {ut['id']}: {e}")
    except ImportError as e:
        print(f"⚠️  No se pudo importar build_apuntes.py: {e}")

    print(f"\n✅ {len(archivos)} archivos generados en {salida}/")
    for f in archivos:
        print(f"   📄 {f if isinstance(f, str) else f.name}")


def _parse_opts(args: list[str], keys: list[str]) -> dict[str, str]:
    """Parsea una lista de args ["--key", "value", …] → dict."""
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
    EvalFP — Asistente IA
    =====================
    Uso: python ai_asistente.py <comando> [opciones]

    Comandos:
      rubrica    Rúbrica de evaluación (4 niveles × CE) para un RA
      actividad  Situaciones de aprendizaje / prácticas para un RA
      informe    Informe individual de progreso de un alumno/a
      todo       Rúbricas + actividades + apuntes de todo el módulo

    Fuente de datos:
      --datos <ruta.json>   Programación real exportada desde EvalFP (prioridad)
      --modulo <nombre>     Módulo estático (iso_data, par_data, …) [legado]

    Opciones comunes:
      --proveedor <p>       claude | openai | demo | auto [default: auto]
      --salida <directorio> Carpeta de material; crea subcarpetas
                            rubricas/ actividades/ informes/ apuntes/

    Opciones por comando:
      rubrica   --ra <RA_ID>
      actividad --ra <RA_ID>  --n <num_propuestas 1-10>
      informe   --alumno "<Apellidos, Nombre>"  --notas "RA1:7,RA2:5.5"
                [--observaciones "texto libre del profesor"]

    Variables de entorno:
      ANTHROPIC_API_KEY / OPENAI_API_KEY   claves de API
      EVALFP_MODEL_CLAUDE / EVALFP_MODEL_OPENAI   modelo a usar (opcional)

    Sin clave configurada → modo DEMO (texto de ejemplo local).
""")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("--ayuda", "-h", "--help", "ayuda"):
        print(AYUDA)
        sys.exit(0)

    cmd = args[0]
    resto = args[1:]

    if cmd == "rubrica":
        _cmd_rubrica(resto)
    elif cmd == "actividad":
        _cmd_actividad(resto)
    elif cmd == "informe":
        _cmd_informe(resto)
    elif cmd == "todo":
        _cmd_generar_todo(resto)
    else:
        print(f"❌ Comando desconocido: '{cmd}'. Usa --ayuda para ver opciones.")
        sys.exit(1)

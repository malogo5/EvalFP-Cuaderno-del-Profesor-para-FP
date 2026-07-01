"""
EvalFP — Asistente IA (Sprint 2.6)
====================================
Genera contenido pedagógico asistido por IA para módulos de FP:

  1. Descriptores de rúbricas (4 niveles × CE) para un RA
  2. Propuestas de actividades/prácticas para un RA
  3. Borrador de informe individual de alumno/a

Uso como módulo:
    from ai_asistente import IAAsistente
    ia = IAAsistente()               # usa ANTHROPIC_API_KEY del entorno, si existe
    texto = ia.descriptores_rubrica(ra, ces, modulo)

Uso como CLI:
    python ai_asistente.py --ayuda
    python ai_asistente.py rubrica   --modulo iso_data --ra RA1
    python ai_asistente.py actividad --modulo iso_data --ra RA2
    python ai_asistente.py informe   --modulo iso_data --alumno "García López, Marta" --notas "RA1:7,RA2:5,RA3:8"

Dependencias opcionales:
    pip install anthropic            # para Claude (recomendado)
    pip install openai               # alternativa GPT
Si no hay ninguna instalada → modo DEMO (texto de ejemplo sin llamada a API).
"""

from __future__ import annotations

import json
import os
import sys
import textwrap
from pathlib import Path
from typing import Any

# ─── Constantes ──────────────────────────────────────────────────────────────

MODELO_CLAUDE  = "claude-haiku-4-5-20251001"   # rápido y económico
MODELO_OPENAI  = "gpt-4o-mini"
MAX_TOKENS     = 1024
TEMPERATURA    = 0.7

NIVELES_RUBRICA = [
    ("No Alcanzado",  "0-4",  "El alumno/a NO demuestra el criterio o lo hace con errores graves."),
    ("En Proceso",    "5-6",  "El alumno/a demuestra el criterio de forma básica o con apoyo."),
    ("Alcanzado",     "7-8",  "El alumno/a demuestra el criterio de forma autónoma y correcta."),
    ("Sobresaliente", "9-10", "El alumno/a demuestra el criterio con precisión y profundidad."),
]

# ─── Motor IA ─────────────────────────────────────────────────────────────────

class IAAsistente:
    """Interfaz unificada Claude / OpenAI / Demo para generación de contenido FP."""

    def __init__(self, api_key: str | None = None, proveedor: str = "auto"):
        """
        proveedor: "claude" | "openai" | "demo" | "auto"
        "auto" detecta el primer SDK disponible con clave configurada.
        """
        self._proveedor, self._cliente = self._init_cliente(api_key, proveedor)

    # ── Inicialización ────────────────────────────────────────────────────────

    def _init_cliente(self, api_key: str | None, proveedor: str):
        if proveedor in ("demo",):
            return "demo", None

        # Intentar Claude
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

        # Intentar OpenAI
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

        # Fallback demo
        print(
            "[EvalFP IA] ⚠️  Sin API key ni SDK detectado → modo DEMO (texto de ejemplo).",
            file=sys.stderr,
        )
        return "demo", None

    # ── Llamada genérica ──────────────────────────────────────────────────────

    def _llamar(self, system: str, user: str, max_tokens: int | None = None) -> str:
        if self._proveedor == "demo":
            return self._demo_response(user)

        _max = max_tokens or MAX_TOKENS

        if self._proveedor == "claude":
            msg = self._cliente.messages.create(
                model=MODELO_CLAUDE,
                max_tokens=_max,
                temperature=TEMPERATURA,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return msg.content[0].text

        if self._proveedor == "openai":
            resp = self._cliente.chat.completions.create(
                model=MODELO_OPENAI,
                max_tokens=_max,
                temperature=TEMPERATURA,
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
            "Para obtener contenido real, configura ANTHROPIC_API_KEY o OPENAI_API_KEY "
            "en tu entorno y vuelve a ejecutar el asistente.\n\n"
            f"Prompt recibido (primeros 200 chars):\n{prompt[:200]}…"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # FUNCIONES PÚBLICAS
    # ══════════════════════════════════════════════════════════════════════════

    def descriptores_rubrica(
        self,
        ra: dict[str, Any],
        ces: list[str],
        modulo: dict[str, Any],
    ) -> str:
        """
        Genera descriptores de rúbrica para un RA completo.

        Parámetros:
            ra     — dict con claves 'id', 'nombre', 'pond'
            ces    — lista de códigos de criterios (["CE1","CE2",...])
            modulo — dict con claves 'nombre', 'ciclo', 'curso'

        Devuelve texto formateado Markdown con la tabla de descriptores.
        """
        system = textwrap.dedent("""\
            Eres un experto en evaluación de Formación Profesional española.
            Generas descriptores de rúbricas claros, concretos y adecuados al nivel del ciclo.
            Usa lenguaje técnico apropiado para el módulo, pero comprensible para el alumnado.
            Responde SOLO con el contenido solicitado, sin introducciones ni cierres.
        """)

        ces_lista = "\n".join(f"  - {ce}" for ce in ces)
        user = textwrap.dedent(f"""\
            Módulo: {modulo['nombre']} ({modulo['ciclo']} — {modulo['curso']})
            Resultado de Aprendizaje: {ra['id']} — {ra['nombre']}
            Ponderación: {ra['pond']}%
            Criterios de Evaluación:
{ces_lista}

            Genera una rúbrica en formato Markdown con 4 columnas:
            | Criterio | No Alcanzado (0-4) | En Proceso (5-6) | Alcanzado (7-8) | Sobresaliente (9-10) |

            Para cada criterio, escribe descriptores CONCRETOS y OBSERVABLES (1-2 frases).
            Adapta el lenguaje técnico a {modulo['ciclo']}.
            Al final añade una fila "NOTA GLOBAL" con la descripción general de cada nivel para este RA.
        """)

        return self._llamar(system, user)

    def propuesta_actividades(
        self,
        ra: dict[str, Any],
        ces: list[str],
        modulo: dict[str, Any],
        n_actividades: int = 3,
    ) -> str:
        """
        Propone actividades/prácticas para trabajar un RA concreto.

        Parámetros:
            ra             — dict con claves 'id', 'nombre'
            ces            — lista de códigos de criterios
            modulo         — dict con claves 'nombre', 'ciclo', 'curso'
            n_actividades  — número de propuestas a generar (default 3)

        Devuelve texto formateado con las propuestas de actividades.
        """
        system = textwrap.dedent("""\
            Eres un docente experto en FP con años de experiencia diseñando actividades
            de aprendizaje prácticas y motivadoras.
            Propones actividades contextualizadas en entornos laborales reales,
            alineadas con los criterios de evaluación del currículo español de FP.
            Responde SOLO con las propuestas, sin introducciones ni cierres.
        """)

        ces_lista = "\n".join(f"  - {ce}" for ce in ces)
        user = textwrap.dedent(f"""\
            Módulo: {modulo['nombre']} ({modulo['ciclo']} — {modulo['curso']})
            Resultado de Aprendizaje: {ra['id']} — {ra['nombre']}
            Criterios de Evaluación:
{ces_lista}

            Propón {n_actividades} actividades/prácticas para trabajar este RA.
            Para cada actividad incluye:
            1. **Nombre** (breve y descriptivo)
            2. **Objetivo** (qué aprende el alumnado)
            3. **Descripción** (2-3 párrafos: contexto, desarrollo, entregable)
            4. **Criterios cubiertos** (qué CEs de la lista trabaja)
            5. **Instrumento de evaluación** (práctica / examen / proyecto / empresa)
            6. **Duración estimada** (horas)
            7. **Recursos necesarios** (software, hardware, materiales)

            Usa contextos laborales reales del sector {modulo['ciclo']}.
        """)

        return self._llamar(system, user)

    def borrador_informe_alumno(
        self,
        alumno: str,
        modulo: dict[str, Any],
        notas_ra: dict[str, float],
        nota_final: float,
        resultado: str,
        observaciones: str = "",
    ) -> str:
        """
        Genera un borrador de informe individual para un alumno/a.

        Parámetros:
            alumno        — nombre completo del alumno/a
            modulo        — dict con claves 'nombre', 'ciclo', 'curso', 'anno'
            notas_ra      — {"RA1": 7.5, "RA2": 4.0, ...}
            nota_final    — nota numérica final del módulo
            resultado     — "APTO" | "NO APTO"
            observaciones — texto libre del profesor (opcional)

        Devuelve borrador de informe en texto para revisar y personalizar.
        """
        system = textwrap.dedent("""\
            Eres un tutor/a de FP redactando informes individuales de progreso del alumnado.
            Usas un tono profesional, constructivo y respetuoso.
            Destacas logros y señalas áreas de mejora con propuestas concretas.
            El informe está dirigido al alumno/a y a su familia.
            Responde SOLO con el texto del informe, sin instrucciones ni metacomentarios.
        """)

        # Calcular puntos fuertes y débiles
        notas_ordenadas = sorted(notas_ra.items(), key=lambda x: x[1], reverse=True)
        puntos_fuertes  = [f"{ra}: {nota:.1f}" for ra, nota in notas_ordenadas if nota >= 5]
        puntos_mejora   = [f"{ra}: {nota:.1f}" for ra, nota in notas_ordenadas if nota < 5]

        notas_str = "\n".join(f"  {ra}: {nota:.1f}/10" for ra, nota in notas_ordenadas)
        obs_str   = f"\nObservaciones del profesor/a:\n{observaciones}" if observaciones else ""

        user = textwrap.dedent(f"""\
            Alumno/a: {alumno}
            Módulo: {modulo['nombre']}
            Ciclo: {modulo['ciclo']} — {modulo['curso']} — Curso {modulo.get('anno','2026-2027')}

            Notas por Resultado de Aprendizaje:
{notas_str}

            Nota final del módulo: {nota_final:.2f}/10
            Resultado: {resultado}

            Puntos fuertes (RAs aprobados): {', '.join(puntos_fuertes) or 'Ninguno'}
            RAs con dificultades: {', '.join(puntos_mejora) or 'Ninguno'}{obs_str}

            Redacta un informe individual de 3-4 párrafos con:
            1. Saludo e introducción (módulo, curso, periodo evaluado)
            2. Valoración del progreso: logros concretos en los RAs con mejor rendimiento
            3. Áreas de mejora: indicaciones específicas y constructivas para los RAs con dificultades
            4. Conclusión con nota final, resultado y ánimo/orientación para la próxima evaluación

            Tono: profesional, empático, constructivo. No uses jerga técnica excesiva.
        """)

        return self._llamar(system, user)

    def generar_todo_modulo(
        self,
        mod,
        output_dir: str | Path = ".",
    ) -> list[Path]:
        """
        Genera para un módulo completo:
         - Una rúbrica por RA (archivo rubrica_{ra_id}.md)
         - Propuestas de actividades por RA (actividades_{ra_id}.md)

        mod: módulo importado (iso_data, par_data, …)
        output_dir: directorio donde guardar los archivos .md

        Devuelve lista de paths generados.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        archivos: list[Path] = []

        modulo = mod.MODULO

        # Construir CES_POR_RA desde ASIGNACIONES del módulo (sin depender de build_template)
        ces_por_ra: dict[str, list[str]] = {}
        for _ut, ra_id, ces in mod.ASIGNACIONES:
            ces_por_ra.setdefault(ra_id, [])
            for ce in ces:
                if ce not in ces_por_ra[ra_id]:
                    ces_por_ra[ra_id].append(ce)

        for ra in mod.RAS:
            ra_id = ra["id"]
            ces   = ces_por_ra.get(ra_id, [])

            # Rúbrica
            print(f"  ✏️  Generando rúbrica {ra_id}…")
            rubrica = self.descriptores_rubrica(ra, ces, modulo)
            path_r  = out / f"rubrica_{ra_id.lower()}.md"
            path_r.write_text(
                f"# Rúbrica — {ra_id}: {ra['nombre']}\n\n"
                f"**Módulo:** {modulo['nombre']}  \n"
                f"**Ponderación:** {ra['pond']}%\n\n"
                f"{rubrica}\n",
                encoding="utf-8",
            )
            archivos.append(path_r)

            # Actividades
            print(f"  🔧 Generando propuestas de actividades {ra_id}…")
            actividades = self.propuesta_actividades(ra, ces, modulo)
            path_a      = out / f"actividades_{ra_id.lower()}.md"
            path_a.write_text(
                f"# Propuestas de Actividades — {ra_id}: {ra['nombre']}\n\n"
                f"**Módulo:** {modulo['nombre']}\n\n"
                f"{actividades}\n",
                encoding="utf-8",
            )
            archivos.append(path_a)

        return archivos


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _cargar_modulo(nombre: str):
    """Importa un módulo de datos por nombre (iso_data, par_data, …)."""
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    import importlib
    nombre_limpio = nombre.replace("scripts/modules/", "").replace(".py", "")
    try:
        return importlib.import_module(f"modules.{nombre_limpio}")
    except ModuleNotFoundError:
        print(f"❌ No se encontró el módulo '{nombre_limpio}' en scripts/modules/")
        sys.exit(1)


def _parse_notas(notas_str: str) -> dict[str, float]:
    """Parsea "RA1:7,RA2:5.5,RA3:8" → {"RA1": 7.0, "RA2": 5.5, "RA3": 8.0}"""
    resultado = {}
    for parte in notas_str.split(","):
        ra, nota = parte.strip().split(":")
        resultado[ra.strip()] = float(nota.strip())
    return resultado


def _cmd_rubrica(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--ra", "--proveedor"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ces_por_ra: dict[str, list[str]] = {}
    for _ut, rid, ces in mod.ASIGNACIONES:
        ces_por_ra.setdefault(rid, [])
        for ce in ces:
            if ce not in ces_por_ra[rid]:
                ces_por_ra[rid].append(ce)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.descriptores_rubrica(ra, ces_por_ra.get(ra_id, []), mod.MODULO)
    print(f"\n{'='*60}")
    print(f"RÚBRICA — {ra_id}: {ra['nombre']}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_actividad(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--ra", "--n", "--proveedor"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    n = int(opts.get("--n", "3"))
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ces_por_ra: dict[str, list[str]] = {}
    for _ut, rid, ces in mod.ASIGNACIONES:
        ces_por_ra.setdefault(rid, [])
        for ce in ces:
            if ce not in ces_por_ra[rid]:
                ces_por_ra[rid].append(ce)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.propuesta_actividades(ra, ces_por_ra.get(ra_id, []), mod.MODULO, n)
    print(f"\n{'='*60}")
    print(f"ACTIVIDADES — {ra_id}: {ra['nombre']}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_informe(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--alumno", "--notas", "--proveedor"])
    mod    = _cargar_modulo(opts.get("--modulo", "iso_data"))
    alumno = opts.get("--alumno", "Alumno Ejemplo")
    notas  = _parse_notas(opts.get("--notas", ",".join(
        f"{r['id']}:5" for r in mod.RAS
    )))
    nota_final = sum(
        notas.get(r["id"], 5) * r["pond"] / 100 for r in mod.RAS
    )
    resultado = "APTO" if nota_final >= 5 else "NO APTO"

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.borrador_informe_alumno(alumno, mod.MODULO, notas, nota_final, resultado)
    print(f"\n{'='*60}")
    print(f"INFORME INDIVIDUAL — {alumno}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_generar_todo(args: list[str]):
    opts      = _parse_opts(args, ["--modulo", "--salida", "--proveedor"])
    mod_name  = opts.get("--modulo", "iso_data")
    mod       = _cargar_modulo(mod_name)
    abrev     = mod.MODULO['abrev'].lower()
    salida    = Path(opts.get("--salida", f"ia_output/{abrev}"))
    proveedor = opts.get("--proveedor", "auto")
    ia        = IAAsistente(proveedor=proveedor)

    # ── 1. Rúbricas + actividades ────────────────────────────────────────────
    print(f"Generando contenido IA para módulo {mod.MODULO['abrev']}…")
    archivos = ia.generar_todo_modulo(mod, salida)

    # ── 2. Apuntes HTML ──────────────────────────────────────────────────────
    print(f"\n📄 Generando apuntes HTML…")
    try:
        from build_apuntes import generar_apunte, apunte_path
        from pathlib import Path as _Path
        apuntes_base = salida / "apuntes"
        apuntes_generados: list[Path] = []
        for ut in mod.UTS:
            print(f"  📄 {ut['id']}: {ut['nombre']}")
            try:
                out_path = generar_apunte(mod, ut, ia, apuntes_base)
                apuntes_generados.append(out_path)
                archivos.append(out_path)
                print(f"     ✅ {out_path.name}")
            except Exception as e:
                print(f"     ⚠️  Error en {ut['id']}: {e}")
        print(f"  → {len(apuntes_generados)} apunte(s) generado(s) en {apuntes_base}/")
    except ImportError as e:
        print(f"  ⚠️  No se pudo importar build_apuntes.py: {e}")

    # ── Resumen ──────────────────────────────────────────────────────────────
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
    EvalFP — Asistente IA (Sprint 2.6)
    ===================================
    Uso: python ai_asistente.py <comando> [opciones]

    Comandos:
      rubrica    Genera descriptores de rúbrica para un RA
      actividad  Propone actividades/prácticas para un RA
      informe    Redacta borrador de informe individual de alumno/a
      todo       Genera rúbricas + actividades para todos los RAs de un módulo

    Opciones comunes:
      --modulo   <nombre>   Nombre del módulo (iso_data, par_data, …) [default: iso_data]
      --proveedor <p>       claude | openai | demo | auto [default: auto]

    Opciones por comando:
      rubrica   --ra <RA_ID>
      actividad --ra <RA_ID>  --n <num_propuestas>
      informe   --alumno "<Nombre Apellidos>"  --notas "RA1:7,RA2:5.5"
      todo      --salida <directorio>

    Variables de entorno:
      ANTHROPIC_API_KEY   Clave de API para Claude (recomendado)
      OPENAI_API_KEY      Clave de API para OpenAI (alternativa)

    Si no se configura ninguna clave → modo DEMO (texto de ejemplo local).

    Ejemplos:
      python ai_asistente.py rubrica --modulo iso_data --ra RA1
      python ai_asistente.py actividad --modulo par_data --ra RA3 --n 2
      python ai_asistente.py informe --alumno "García López, Marta" --notas "RA1:7,RA2:4,RA3:8"
      python ai_asistente.py todo --modulo iso_data --salida ia_output/iso
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

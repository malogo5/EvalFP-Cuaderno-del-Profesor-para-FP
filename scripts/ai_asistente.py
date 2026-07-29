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
        timeout_s = 15.0

        def _emit_red_error(exc: Exception):
            _emit_ia_code(
                "ERROR_RED",
                "No se ha podido conectar con el servidor de IA. Revisa tu conexión a internet o inténtalo más tarde.",
            )

        if self._proveedor == "claude":
            try:
                import anthropic  # noqa: PLC0415
                try:
                    msg = self._cliente.messages.create(
                        model=MODELO_CLAUDE,
                        max_tokens=_max,
                        temperature=TEMPERATURA,
                        system=system,
                        messages=[{"role": "user", "content": user}],
                        timeout=timeout_s,
                    )
                    return msg.content[0].text
                except (
                    anthropic.APIConnectionError,
                    anthropic.APITimeoutError,
                    anthropic.RateLimitError,
                    anthropic.APIError,
                    TimeoutError,
                    OSError,
                ) as exc:
                    _emit_red_error(exc)
                except Exception as exc:
                    _emit_red_error(exc)
            except ImportError:
                _emit_ia_code("ERROR_RED", "No se ha podido cargar el SDK de Claude.")

        if self._proveedor == "openai":
            try:
                import openai  # noqa: PLC0415
                try:
                    resp = self._cliente.chat.completions.create(
                        model=MODELO_OPENAI,
                        max_tokens=_max,
                        temperature=TEMPERATURA,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user",   "content": user},
                        ],
                        timeout=timeout_s,
                    )
                    return resp.choices[0].message.content
                except (
                    openai.APIConnectionError,
                    openai.APITimeoutError,
                    openai.RateLimitError,
                    openai.APIError,
                    TimeoutError,
                    OSError,
                ) as exc:
                    _emit_red_error(exc)
                except Exception as exc:
                    _emit_red_error(exc)
            except ImportError:
                _emit_ia_code("ERROR_RED", "No se ha podido cargar el SDK de OpenAI.")

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
        ces_por_ra = _agrupar_ces_por_ra(mod)

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
    """Parsea "RA1:7,RA2:5.5,RA3:8" → {"RA1": 7.0, "RA2": 5.5, "RA3": 8.0}

    Reglas:
    - ignora espacios alrededor de separadores
    - permite separadores "," o ";" entre pares
    - valida formato y rango 0..10
    """
    s = (notas_str or "").strip()
    if not s:
        raise ValueError("notas vacías")

    resultado: dict[str, float] = {}
    partes = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    for parte in partes:
        if ":" not in parte:
            raise ValueError(f"formato inválido: '{parte}' (usa RA1:7,RA2:5.5)")
        ra, nota = parte.split(":", 1)
        ra = ra.strip()
        if not ra:
            raise ValueError(f"RA vacío en '{parte}'")
        try:
            n = float(nota.strip())
        except Exception:
            raise ValueError(f"nota inválida en '{parte}'")
        if n < 0 or n > 10:
            raise ValueError(f"nota fuera de rango 0-10 en '{parte}'")
        resultado[ra] = n
    return resultado


def _parse_min_exam(val: str | None) -> float | None:
    if val is None:
        return None
    s = str(val).strip()
    if s == "":
        return None
    try:
        n = float(s)
    except Exception:
        raise ValueError("mínimo de examen inválido")
    if n < 0 or n > 10:
        raise ValueError("mínimo de examen fuera de rango 0-10")
    return n


def _emit_ia_code(code: str, msg: str, exit_code: int = 1):
    print(f"{code}: {msg}")
    if exit_code is not None:
        sys.exit(exit_code)


def _agrupar_ces_por_ra(mod) -> dict[str, list[str]]:
    """Agrupa los Criterios de Evaluación (CE) correspondientes a cada RA."""
    ces_por_ra: dict[str, list[str]] = {}
    for _ut, ra_id, ces in mod.ASIGNACIONES:
        ces_por_ra.setdefault(ra_id, [])
        for ce in ces:
            if ce not in ces_por_ra[ra_id]:
                ces_por_ra[ra_id].append(ce)
    return ces_por_ra


def _anonimizar_alumno_nombre(alumno: str, activo: bool = True) -> str:
    """Devuelve un identificador opaco si la anonimización está activa."""
    nombre = (alumno or "").strip()
    if not activo or not nombre:
        return nombre
    piezas = [p for p in nombre.replace(",", " ").split() if p]
    if not piezas:
        return "Alumno_ANON"
    iniciales = "".join(p[0] for p in piezas[:3]).upper()
    return f"Alumno_ANON_{iniciales or 'X'}"


def _parse_ponderaciones(pond_str: str | None) -> dict[str, float]:
    """Parsea "--ponderaciones" tipo "RA1:20,RA2:30,RA3:50" → {"RA1": 20.0, ...}

    Reglas:
    - tolera espacios y separadores "," o ";"
    - ignora pares corruptos de forma segura (no revienta el comando)
    - valida que el peso sea >= 0 (valores negativos se ignoran)
    """
    s = (pond_str or "").strip()
    if not s:
        return {}

    res: dict[str, float] = {}
    partes = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    for parte in partes:
        if ":" not in parte:
            continue
        ra, valor = parte.split(":", 1)
        ra = ra.strip()
        if not ra:
            continue
        try:
            n = float(valor.strip())
        except Exception:
            continue
        if n < 0:
            continue
        res[ra] = n
    return res


def _parse_json_list(raw: str | None) -> list[dict]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _norm_ponds(ras: list[dict]) -> dict[str, float]:
    """Devuelve ponderaciones normalizadas por RA.

    - Si la suma es 0: devuelve vacío; el llamador debe tratarlo como error.
    - Si la suma != 100: normaliza proporcionalmente.
    """
    p = {r["id"]: float(r.get("pond") or 0) for r in ras}
    total = sum(p.values())
    if total <= 0:
        return {}
    return {k: (v * 100.0 / total) for k, v in p.items()}


def _calc_informe_estado(mod, notas: dict[str, float], min_exam: float | None, pond_overrides: dict[str, float] | None = None):
    """Criterio de informe alineado con la app:
    - Nota final: media ponderada reponderada SOLO sobre RA evaluados (notas presentes)
    - Regla de oro: APTO ⇔ todos los RA calificados >=5 y sin mínimos KO
    - Si faltan RA sin nota: resultado PENDIENTE
    """
    ras = list(mod.RAS)
    if not ras:
        return {"nota_final": None, "resultado": "PENDIENTE", "pendientes": [], "sin_nota": []}

    pond_overrides = pond_overrides or {}
    # Consolidar ponderaciones (prioriza overrides dinámicos; fallback al estático del módulo)
    ras_pond = [{"id": r["id"], "pond": pond_overrides.get(r["id"], float(r.get("pond") or 0))} for r in ras]
    raw_total = sum(float(r.get("pond") or 0) for r in ras_pond)
    if raw_total <= 0:
        return {
            "nota_final": None,
            "resultado": "ERROR",
            "pendientes": [],
            "sin_nota": [],
            "alerta": ("PONDERACION_CERO", "La suma de ponderaciones es cero."),
        }
    ponds = _norm_ponds(ras_pond)
    if not ponds:
        return {
            "nota_final": None,
            "resultado": "ERROR",
            "pendientes": [],
            "sin_nota": [],
            "alerta": ("PONDERACION_CERO", "La suma de ponderaciones es cero."),
        }

    sin_nota: list[str] = []
    pendientes: list[str] = []
    alerta_absentismo: tuple[str, str] | None = None
    alerta_ra_llave: tuple[str, str] | None = None
    sum_w = 0.0
    sum_wn = 0.0

    # Para el mínimo de examen en Python solo podemos aplicarlo si llega una nota
    # específica de examen por RA; en el flujo actual no existe. Permitimos
    # pasar claves tipo "RA1_EX" o "RA1_EXAM" como nota de examen.
    def _ex_for(ra_id: str) -> float | None:
        for k in (f"{ra_id}_EX", f"{ra_id}_EXAM", f"{ra_id}_EXAMEN"):
            if k in notas:
                return notas.get(k)
        return None

    for ra in ras:
        ra_id = ra["id"]
        n = notas.get(ra_id)
        if n is None:
            sin_nota.append(ra_id)
            continue
        if n < 0 or n > 10:
            return {
                "nota_final": None,
                "resultado": "ERROR",
                "pendientes": [],
                "sin_nota": [],
                "alerta": ("NOTA_INVALIDA", f"Rango incorrecto en {ra_id}. Debe estar entre 0 y 10."),
            }
        w = float(ponds.get(ra_id, 0))
        sum_w += w
        sum_wn += n * w

        min_ko = False
        if min_exam is not None:
            ex = _ex_for(ra_id)
            if ex is not None and ex < min_exam:
                min_ko = True

        if n < 5 or min_ko:
            pendientes.append(ra_id)

    faltas_pct = getattr(mod, "_faltas_porcentaje", None)
    if faltas_pct is not None:
        try:
            faltas_num = float(faltas_pct)
            if faltas_num >= 15:
                alerta_absentismo = (
                    "ABSENTISMO_CRITICO",
                    f"Absentismo crítico detectado ({faltas_num:.1f}%). Puede implicar pérdida del derecho a la evaluación continua.",
                )
        except Exception:
            pass

    ras_llave = set(getattr(mod, "_ras_llave", []) or [])
    if ras_llave and pendientes:
        criticos = sorted(r for r in pendientes if r in ras_llave)
        if criticos:
            alerta_ra_llave = (
                "RA_LLAVE_SUSPENDIDO",
                f"Ha suspendido un RA crítico obligatorio: {', '.join(criticos)}.",
            )
            resultado = "NO APTO"
        else:
            resultado = None
    else:
        resultado = None

    if sum_w > 0:
        nota_final = sum_wn / sum_w
    else:
        # No debería pasar si hay notas presentes, pero por seguridad:
        nota_final = None

    if sin_nota:
        resultado = "PENDIENTE"
        alerta = ("RA_NO_EVALUADO", f"Faltan notas para el RA: {', '.join(sin_nota)}.")
    else:
        resultado = "APTO" if (nota_final is not None and nota_final >= 5 and not pendientes) else "NO APTO"
        alerta = None

    if not sin_nota and pendientes:
        alerta = ("RA_SUSPENDIDO", f"El alumno tiene suspendido el RA: {', '.join(pendientes)}.")
    if alerta_absentismo:
        alerta = alerta_absentismo
    if alerta_ra_llave:
        alerta = alerta_ra_llave
        resultado = "NO APTO"

    nota_final_2 = None if nota_final is None else round(nota_final + 1e-12, 2)
    return {
        "nota_final": nota_final_2,
        "resultado": resultado,
        "pendientes": pendientes,
        "sin_nota": sin_nota,
        "alerta": alerta,
    }


def _cmd_rubrica(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--ra", "--proveedor"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ces_por_ra = _agrupar_ces_por_ra(mod)

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
    try:
        n = int(str(opts.get("--n", "3")).strip())
    except Exception:
        print("❌ --n debe ser un entero (1-10).")
        sys.exit(1)
    if n < 1 or n > 10:
        print("❌ --n fuera de rango (1-10).")
        sys.exit(1)
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        print(f"❌ RA '{ra_id}' no encontrado en el módulo.")
        sys.exit(1)

    ces_por_ra = _agrupar_ces_por_ra(mod)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.propuesta_actividades(ra, ces_por_ra.get(ra_id, []), mod.MODULO, n)
    print(f"\n{'='*60}")
    print(f"ACTIVIDADES — {ra_id}: {ra['nombre']}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_informe(args: list[str]):
    opts = _parse_opts(args, ["--modulo", "--alumno", "--notas", "--proveedor", "--min-exam", "--ponderaciones", "--anonimizar", "--faltas-porcentaje", "--ras-llave"])
    mod    = _cargar_modulo(opts.get("--modulo", "iso_data"))
    alumno_raw = opts.get("--alumno", "Alumno Ejemplo")
    anonimizar = True
    if "--anonimizar" in opts:
        anonimizar = opts["--anonimizar"].strip().lower() not in ("0", "false", "no", "off")
    alumno = _anonimizar_alumno_nombre(alumno_raw, activo=anonimizar)
    try:
        notas = _parse_notas(opts.get("--notas", ""))
    except ValueError as e:
        _emit_ia_code("NOTA_INVALIDA", f"Formato o rango de nota incorrecto: {e}")

    try:
        min_exam = _parse_min_exam(opts.get("--min-exam"))
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    pond_dinamicas = _parse_ponderaciones(opts.get("--ponderaciones"))
    faltas_porcentaje = None
    if "--faltas-porcentaje" in opts:
        try:
            faltas_porcentaje = float(str(opts.get("--faltas-porcentaje", "")).strip())
        except Exception:
            print("❌ --faltas-porcentaje debe ser numérico.")
            sys.exit(1)
    ras_llave = [r.strip() for r in str(opts.get("--ras-llave", "")).split(",") if r.strip()]
    setattr(mod, "_faltas_porcentaje", faltas_porcentaje)
    setattr(mod, "_ras_llave", ras_llave)
    st = _calc_informe_estado(mod, notas, min_exam, pond_dinamicas)
    alerta = st.get("alerta")
    if alerta:
        code, msg = alerta
        if code == "RA_NO_EVALUADO" or code == "PONDERACION_CERO" or code == "NOTA_INVALIDA":
            _emit_ia_code(code, msg)
        if code == "RA_SUSPENDIDO":
            print(f"{code}: {msg}")
    nota_final = st["nota_final"]
    resultado = st["resultado"]

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.borrador_informe_alumno(alumno, mod.MODULO, notas, nota_final, resultado)
    print(f"\n{'='*60}")
    print(f"INFORME INDIVIDUAL — {alumno}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_generar_todo(args: list[str]):
    opts      = _parse_opts(args, ["--modulo", "--salida", "--proveedor", "--alumnos-json", "--notas-grid-json", "--actividades-json"])
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
    except Exception:
        print("EVALFP_WARN_APUNTES: Error al generar los apuntes HTML del módulo.")

    alumnos = _parse_json_list(opts.get("--alumnos-json"))
    notas_grid = _parse_json_list(opts.get("--notas-grid-json"))
    actividades = _parse_json_list(opts.get("--actividades-json"))

    if alumnos:
        print(f"\n🧾 Generando informes individuales…")
        for alumno in alumnos:
            try:
                nombre = f"{alumno.get('apellidos','')}{', ' if alumno.get('apellidos') and alumno.get('nombre') else ''}{alumno.get('nombre','')}".strip()
                notas = {}
                ra_map: dict[str, list[tuple[float, float]]] = {}
                act_by_id = {str(a.get("id")): a for a in actividades if a.get("id") is not None}
                for row in notas_grid:
                    if row.get('alumno_id') != alumno.get('id'):
                        continue
                    act = act_by_id.get(str(row.get('actividad_id')))
                    ra_id = str((act or {}).get('ra_id') or row.get('ra_id') or '').strip()
                    if not ra_id:
                        continue
                    nota_val = row.get('nota_rec') if row.get('nota_rec') is not None else row.get('nota')
                    try:
                        nota_num = float(nota_val)
                    except Exception:
                        continue
                    peso = float((act or {}).get('peso') or 1)
                    ra_map.setdefault(ra_id, []).append((nota_num, peso))
                for ra_id, vals in ra_map.items():
                    den = sum(p for _, p in vals) or len(vals)
                    num = sum(n * p for n, p in vals)
                    notas[ra_id] = num / den if den else 0.0
                setattr(mod, "_faltas_porcentaje", None)
                setattr(mod, "_ras_llave", [])
                st = _calc_informe_estado(mod, notas, None, None)
                out_txt = ia.borrador_informe_alumno(nombre, mod.MODULO, notas, st["nota_final"] or 0.0, st["resultado"])
                out_path = salida / f"informe_{alumno.get('id','alumno')}.md"
                out_path.write_text(out_txt, encoding="utf-8")
                archivos.append(out_path)
                print(f"  ✅ {out_path.name}")
            except Exception as e:
                print(f"  ⚠️  Error en informe de {alumno.get('id','?')}: {e}")

    # ── Resumen ──────────────────────────────────────────────────────────────
    print(f"\n✅ {len(archivos)} archivos generados en {salida}/")
    for f in archivos:
        print(f"   📄 {f if isinstance(f, str) else f.name}")


def _parse_opts(args: list[str], valid_flags: list[str] | None = None) -> dict[str, str]:
    """Parsea una lista de args ["--key", "value", …] → dict.

    Si se proporciona valid_flags, rechaza flags desconocidos y exige valor
    para cada flag reconocido.
    """
    opts: dict[str, str] = {}
    valid_set = set(valid_flags or [])
    i = 0
    while i < len(args):
        tok = args[i]
        if not isinstance(tok, str) or not tok.startswith("--"):
            i += 1
            continue

        if valid_flags is not None and tok not in valid_set:
            print(f"❌ Flag desconocido detectado: {tok}")
            sys.exit(1)

        if i + 1 >= len(args) or (isinstance(args[i + 1], str) and args[i + 1].startswith("--")):
            print(f"❌ Falta el valor obligatorio para el flag: {tok}")
            sys.exit(1)

        opts[tok] = args[i + 1]
        i += 2

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
      informe   --alumno "<Nombre Apellidos>"  --notas "RA1:7,RA2:5.5"  [--min-exam 5]  [--ponderaciones "RA1:20,RA2:30,RA3:50"]
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

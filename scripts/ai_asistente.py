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

# Dos niveles de modelo. Lo que va a leer una familia o sostiene una reclamación
# —informes y planes de recuperación— se genera con el modelo capaz; lo repetitivo
# —rúbricas, listados de actividades— con el económico, que va sobrado.
MODELO_CLAUDE  = "claude-haiku-4-5-20251001"   # rápido y económico
MODELO_OPENAI  = "gpt-4o-mini"
MODELO_CLAUDE_CALIDAD = "claude-sonnet-5"
MODELO_OPENAI_CALIDAD = "gpt-4o"
MAX_TOKENS     = 1024
TEMPERATURA    = 0.7

# Un texto largo y cuidado no cabe en 15 s: se da margen y un reintento.
TIMEOUT_NORMAL  = 30.0
TIMEOUT_CALIDAD = 90.0

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

    def _llamar(self, system: str, user: str, max_tokens: int | None = None,
                calidad: bool = False) -> str:
        if self._proveedor == "demo":
            return self._demo_response(user)

        _max = max_tokens or MAX_TOKENS
        timeout_s = TIMEOUT_CALIDAD if calidad else TIMEOUT_NORMAL
        modelo_claude = MODELO_CLAUDE_CALIDAD if calidad else MODELO_CLAUDE
        modelo_openai = MODELO_OPENAI_CALIDAD if calidad else MODELO_OPENAI

        def _emit_red_error(exc: Exception):
            _emit_ia_code(
                "ERROR_RED",
                "No se ha podido conectar con el servidor de IA. Revisa tu conexión a internet o inténtalo más tarde.",
            )

        def _con_reintento(fn):
            """Un corte de red o un pico de latencia no deberían perder el trabajo."""
            import time  # noqa: PLC0415
            ultimo = None
            for intento in range(2):
                try:
                    return fn()
                except Exception as exc:            # noqa: BLE001 — se reemite abajo
                    ultimo = exc
                    if intento == 0:
                        print("[EvalFP IA] reintentando tras un fallo de conexión…", file=sys.stderr)
                        time.sleep(1.5)
            raise ultimo

        if self._proveedor == "claude":
            try:
                import anthropic  # noqa: PLC0415
                try:
                    msg = _con_reintento(lambda: self._cliente.messages.create(
                        model=modelo_claude,
                        max_tokens=_max,
                        temperature=TEMPERATURA,
                        system=system,
                        messages=[{"role": "user", "content": user}],
                        timeout=timeout_s,
                    ))
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
                    resp = _con_reintento(lambda: self._cliente.chat.completions.create(
                        model=modelo_openai,
                        max_tokens=_max,
                        temperature=TEMPERATURA,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user",   "content": user},
                        ],
                        timeout=timeout_s,
                    ))
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
        contexto: dict[str, Any] | None = None,
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
        ctx = contexto or {}
        ra_texto   = ctx.get("ra_texto", {})      # {"RA1": "Instala sistemas operativos…"}
        ces_por_ra = ctx.get("ces_por_ra", {})    # {"RA1": ["Se ha…", …]}
        uts_por_ra = ctx.get("uts_por_ra", {})    # {"RA1": ["UT1 · Instalación…"]}
        evidencias = ctx.get("evidencias", [])    # actividades con nota, la del alumno

        system = textwrap.dedent("""\
            Eres profesor o profesora de Formación Profesional redactando el informe individual
            de evaluación de un alumno o alumna. El informe lo van a leer el alumnado y su familia,
            y puede acompañar a una reclamación, así que cada afirmación debe poder sostenerse en
            los criterios de evaluación del módulo.

            Cómo escribes:
            · Hablas de lo que el alumno o alumna sabe hacer y de lo que todavía no, en lenguaje
              claro, nunca en clave («RA3», «CE b») salvo entre paréntesis como referencia.
            · Cada área de mejora va acompañada de una propuesta concreta y realizable: qué tarea,
              sobre qué contenido, con qué finalidad.
            · No inventas datos, notas, fechas, actitudes ni comportamientos: solo usas lo que se
              te da. Si no hay evidencia de algo, no lo mencionas.
            · No juzgas a la persona («es vago», «no se esfuerza»): describes desempeño.
            · Tono profesional y cercano, en español de España, sin florituras ni frases de relleno.

            Responde SOLO con el texto del informe, sin encabezados de sistema ni metacomentarios.
        """)

        # Puntos fuertes y débiles, con el enunciado real de cada RA
        notas_ordenadas = sorted(notas_ra.items(), key=lambda x: x[1], reverse=True)

        def _bloque_ra(ra_id: str, nota: float) -> str:
            enun = ra_texto.get(ra_id, "")
            lineas = [f"  {ra_id} — {nota:.1f}/10" + (f": {enun}" if enun else "")]
            uts = uts_por_ra.get(ra_id) or []
            if uts:
                lineas.append(f"      Se trabaja en: {'; '.join(uts)}")
            ces = ces_por_ra.get(ra_id) or []
            if ces and nota < 5:
                lineas.append("      Criterios de evaluación que quedan por alcanzar:")
                lineas += [f"        · {c}" for c in ces[:12]]
            return "\n".join(lineas)

        superados  = [(ra, n) for ra, n in notas_ordenadas if n >= 5]
        pendientes = [(ra, n) for ra, n in notas_ordenadas if n < 5]

        bloque_sup = "\n".join(_bloque_ra(ra, n) for ra, n in superados) or "  (ninguno)"
        bloque_pen = "\n".join(_bloque_ra(ra, n) for ra, n in pendientes) or "  (ninguno)"

        # Los RA que todavía no se han trabajado. Sin esto, un informe de
        # trimestre daba a entender que el módulo estaba entero y que lo no
        # citado estaba suspenso.
        sin_evaluar = [ra for ra in ra_texto if ra not in notas_ra]
        bloque_sin = ""
        if sin_evaluar:
            filas = [f"  {ra} — sin calificar todavía" +
                     (f": {ra_texto.get(ra, '')}" if ra_texto.get(ra) else "")
                     for ra in sin_evaluar]
            bloque_sin = ("\n\n            RESULTADOS DE APRENDIZAJE QUE AÚN NO SE HAN TRABAJADO\n"
                          + "\n".join(filas) +
                          "\n            (El módulo está en curso: no digas que están suspensos ni "
                          "que le faltan; di que se verán más adelante.)")

        ev_str = ""
        if evidencias:
            filas = [f"  · {e.get('descripcion','(actividad)')}: {e.get('nota')}/10"
                     + (f" — {e.get('ut')}" if e.get("ut") else "")
                     for e in evidencias[:20]]
            ev_str = "\n\nCalificaciones de las actividades del alumno/a:\n" + "\n".join(filas)

        obs_str = f"\n\nObservaciones del profesor/a:\n{observaciones}" if observaciones else ""
        nota_txt = "sin calificación todavía" if nota_final is None else f"{nota_final:.2f}/10"
        if sin_evaluar and nota_final is not None:
            nota_txt += " (parcial: solo con lo evaluado hasta ahora)"

        user = textwrap.dedent(f"""\
            Alumno/a: {alumno}
            Módulo: {modulo['nombre']} ({modulo.get('codigo','')})
            Ciclo: {modulo['ciclo']} — {modulo.get('curso','')} — Curso {modulo.get('anno','2026-2027')}
            Normativa del módulo: {modulo.get('decreto','')}

            RESULTADOS DE APRENDIZAJE SUPERADOS
{bloque_sup}

            RESULTADOS DE APRENDIZAJE NO SUPERADOS
{bloque_pen}{bloque_sin}

            Nota final del módulo: {nota_txt} · Resultado: {resultado}{ev_str}{obs_str}

            Redacta el informe con esta estructura, sin numerarla ni poner títulos:

            1. Una frase de situación: módulo, ciclo y periodo evaluado.
            2. Qué ha conseguido: describe en lenguaje llano las capacidades de los resultados de
               aprendizaje superados, citando lo que sabe hacer, no la nota.
            3. Qué le falta: para CADA resultado de aprendizaje no superado, explica qué se
               esperaba —apoyándote en sus criterios de evaluación, dichos con tus palabras— y qué
               no ha demostrado todavía.
            4. Cómo recuperarlo: una propuesta concreta por cada resultado no superado (tarea,
               contenido y unidad de trabajo donde repasarlo).
            5. Cierre con la nota final, el resultado y una orientación realista.

            Si el resultado es NO APTO con la media igual o superior a 5, explica con naturalidad
            que en Formación Profesional hay que superar todos los resultados de aprendizaje y que
            la media no compensa uno suspenso.

            Extensión: entre 250 y 400 palabras. Nada de listas con viñetas: prosa.
        """)

        return self._llamar(system, user, max_tokens=1800, calidad=True)

    def plan_recuperacion(
        self,
        alumno: str,
        modulo: dict[str, Any],
        pendientes: list[dict[str, Any]],
        contexto: dict[str, Any] | None = None,
        semanas: int = 4,
    ) -> str:
        """Plan de recuperación centrado SOLO en los RA que le quedan."""
        ctx = contexto or {}
        ces_por_ra = ctx.get("ces_por_ra", {})
        uts_por_ra = ctx.get("uts_por_ra", {})

        system = textwrap.dedent("""\
            Eres profesor o profesora de Formación Profesional preparando el plan de recuperación
            que se entrega al alumnado con resultados de aprendizaje pendientes.

            El plan tiene que ser algo que el alumno o alumna pueda seguir solo: qué estudiar, qué
            hacer, en qué orden y cómo se le va a evaluar. Nada de buenas intenciones genéricas.

            Reglas:
            · Solo hablas de los resultados de aprendizaje que se te dan como pendientes.
            · Cada tarea que propones se puede hacer con medios de aula y en el tiempo indicado.
            · Dices con qué se va a evaluar cada resultado y qué hay que demostrar para superarlo.
            · No inventas fechas concretas ni notas: usas «semana 1», «semana 2»…
            · Español de España, tono directo y respetuoso, sin infantilizar.

            Responde SOLO con el plan, en texto con encabezados simples.
        """)

        bloques = []
        for p in pendientes:
            ra_id = p.get("ra")
            ces = ces_por_ra.get(ra_id) or []
            uts = uts_por_ra.get(ra_id) or []
            bloques.append(
                f"\n{ra_id} — nota actual {p.get('nota')}/10\n"
                f"  Enunciado: {p.get('enunciado','')}\n"
                + (f"  Unidades donde se trabaja: {'; '.join(uts)}\n" if uts else "")
                + ("  Criterios de evaluación pendientes:\n"
                   + "\n".join(f"    · {c}" for c in ces[:12]) if ces else "")
            )

        user = textwrap.dedent(f"""\
            Alumno/a: {alumno}
            Módulo: {modulo['nombre']} ({modulo.get('codigo','')}) — {modulo.get('ciclo','')} {modulo.get('curso','')}
            Tiempo disponible hasta la prueba de recuperación: {semanas} semanas

            RESULTADOS DE APRENDIZAJE PENDIENTES
            {''.join(bloques)}

            Escribe el plan con esta forma:

            · Un párrafo breve de situación: qué le queda y qué supone superarlo.
            · Un apartado por cada resultado de aprendizaje pendiente, con: qué tiene que llegar a
              hacer (en lenguaje llano), qué repasar y dónde, dos o tres tareas concretas de
              práctica, y cómo se le evaluará.
            · Un calendario por semanas repartiendo esas tareas en las {semanas} semanas.
            · Una última línea recordando que hay que superar TODOS los resultados de aprendizaje.
        """)
        return self._llamar(system, user, max_tokens=2000, calidad=True)

    def radiografia_grupo(
        self,
        modulo: dict[str, Any],
        estadisticas: dict[str, Any],
    ) -> str:
        """Lee los números del grupo (ya calculados) y propone refuerzo."""
        system = textwrap.dedent("""\
            Eres jefe o jefa de departamento de Formación Profesional analizando cómo ha ido un
            módulo con un grupo, para decidir qué reforzar y qué cambiar en la programación.

            Trabajas SOLO con los datos que se te dan, que ya vienen calculados: no recalculas
            medias ni porcentajes, no inventas cifras y no supones causas que no estén en los datos.
            Cuando algo puede tener varias explicaciones, lo dices como hipótesis a comprobar.

            Escribes para el propio profesorado: directo, sin adornos, accionable.
        """)

        filas = []
        for ra in estadisticas.get("ras", []):
            filas.append(
                f"  {ra['id']} ({ra.get('pond','?')}%) — media {ra['media']} · "
                f"aprueban {ra['aprobados']}/{ra['total']} ({ra['porcentaje']}%)\n"
                f"      {ra.get('enunciado','')}"
            )
        acts = []
        for a in estadisticas.get("actividades", [])[:15]:
            acts.append(f"  · {a['descripcion']}: media {a['media']} · "
                        f"aprueban {a['aprobados']}/{a['total']} ({a['porcentaje']}%)")

        user = textwrap.dedent(f"""\
            Módulo: {modulo['nombre']} ({modulo.get('codigo','')}) — {modulo.get('ciclo','')} {modulo.get('curso','')}
            Alumnado con calificaciones: {estadisticas.get('n_alumnos', 0)}
            Media del grupo: {estadisticas.get('media_grupo', '—')}/10 ·
            Superan el módulo: {estadisticas.get('superan', 0)} de {estadisticas.get('n_alumnos', 0)}

            RESULTADOS DE APRENDIZAJE
{chr(10).join(filas) or '  (sin datos)'}

            ACTIVIDADES DE PEOR A MEJOR RESULTADO
{chr(10).join(acts) or '  (sin datos)'}

            Redacta un análisis con:

            · Cómo ha ido el grupo en dos o tres frases.
            · Dónde está el problema: los resultados de aprendizaje y las actividades con peores
              datos, diciendo qué contenido concreto hay detrás.
            · Qué reforzar y cómo: propuestas de aula para los puntos débiles, ordenadas por
              urgencia, indicando a cuántos alumnos afectaría.
            · Qué revisar de la programación de cara al curso que viene: si alguna actividad puede
              estar mal planteada, mal situada en el tiempo o mal ponderada, dilo como hipótesis.
        """)
        return self._llamar(system, user, max_tokens=2000, calidad=True)

    def examen_con_solucionario(
        self,
        modulo: dict[str, Any],
        ra: dict[str, Any],
        ces: list[str],
        n_preguntas: int = 8,
        tipo: str = "mixto",
        duracion: int = 50,
    ) -> str:
        """Prueba escrita a partir de los CE literales del decreto, con solucionario."""
        system = textwrap.dedent("""\
            Eres profesor o profesora de Formación Profesional que redacta pruebas escritas.

            Reglas que no te saltas:
            · Cada pregunta evalúa uno o varios criterios de evaluación concretos, y lo indicas.
            · Preguntas inequívocas: un enunciado, una tarea, una respuesta esperable.
            · El solucionario dice qué se considera correcto y qué errores son frecuentes.
            · El baremo reparte los puntos entre las preguntas y suma exactamente 10.
            · Nada de preguntas trampa, de cultura general ni ajenas a los criterios dados.
            · Español de España, registro claro para el nivel del ciclo.
        """)

        ces_txt = "\n".join(f"  {i}. {c}" for i, c in enumerate(ces, 1)) or "  (sin criterios)"
        formato = {
            "test": "preguntas tipo test de 4 opciones con una sola correcta",
            "desarrollo": "preguntas de desarrollo, de respuesta razonada",
            "practico": "supuestos prácticos con tareas a resolver paso a paso",
        }.get(tipo, "una mezcla equilibrada de test, respuesta corta y un supuesto práctico")

        user = textwrap.dedent(f"""\
            Módulo: {modulo['nombre']} ({modulo.get('codigo','')}) — {modulo.get('ciclo','')} {modulo.get('curso','')}
            Resultado de aprendizaje evaluado:
              {ra.get('id')} — {ra.get('nombre','')}

            Criterios de evaluación del decreto que hay que cubrir:
{ces_txt}

            Prepara una prueba de {n_preguntas} preguntas, {formato}, para {duracion} minutos.

            Devuelve, en este orden y con estos títulos:

            ENUNCIADO DE LA PRUEBA
            (cabecera con módulo, RA, duración y puntuación total, y las preguntas numeradas;
            cada pregunta indica entre corchetes los criterios que evalúa y sus puntos)

            SOLUCIONARIO
            (respuesta esperada de cada pregunta, qué se admite como válido y los errores
            frecuentes que conviene vigilar al corregir)

            BAREMO POR CRITERIO
            (tabla de texto: criterio de evaluación, preguntas que lo evalúan y puntos que suma)
        """)
        return self._llamar(system, user, max_tokens=3000, calidad=True)

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
    scripts_dir = Path(__file__).resolve().parent
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


def _contexto_didactico(mod, notas: dict[str, float], detalle: list[dict] | None = None) -> dict:
    """
    Reúne lo que la IA necesita para hablar del módulo con propiedad: el enunciado
    literal de cada RA, sus criterios de evaluación tal y como los redacta el
    decreto, en qué unidades de trabajo se tocan y, si se ha pasado, las notas de
    las actividades concretas del alumno o alumna.
    """
    ra_texto = {r["id"]: r.get("nombre", "") for r in getattr(mod, "RAS", [])}

    ces_por_ra: dict[str, list[str]] = {}
    for ra_id, lista in (getattr(mod, "CES", {}) or {}).items():
        ces_por_ra[ra_id] = [c.get("texto", "") for c in lista if c.get("texto")]

    uts = {u["id"]: u.get("nombre", "") for u in getattr(mod, "UTS", [])}
    uts_por_ra: dict[str, list[str]] = {}
    for ut_id, ra_id, _ces in getattr(mod, "ASIGNACIONES", []):
        etiqueta = f"{ut_id} · {uts.get(ut_id, '')}".strip(" ·")
        uts_por_ra.setdefault(ra_id, [])
        if etiqueta not in uts_por_ra[ra_id]:
            uts_por_ra[ra_id].append(etiqueta)

    evidencias = []
    for act in (detalle or []):
        nota = act.get("nota")
        if nota is None or nota == "":
            continue
        evidencias.append({
            "descripcion": str(act.get("descripcion", ""))[:120],
            "nota": nota,
            "ut": f"{act.get('ut_id','')} · {uts.get(act.get('ut_id'), '')}".strip(" ·"),
            "ra": act.get("ra_id"),
        })
    # primero lo suspenso: es de lo que hay que hablar
    evidencias.sort(key=lambda e: float(e["nota"]) if str(e["nota"]).replace('.', '', 1).isdigit() else 10)

    return {"ra_texto": ra_texto, "ces_por_ra": ces_por_ra,
            "uts_por_ra": uts_por_ra, "evidencias": evidencias}


# Códigos que impiden seguir (falta información o los datos son inválidos) frente a
# los que solo advierten. Antes solo salían los primeros y algún aviso normativo se
# quedaba dentro de Python sin llegar nunca al profesorado.
#
# Que falten RA por evaluar NO es un error: en diciembre o en marzo faltan casi
# todos, y el informe de trimestre es justo el que más se pide. Se avisa y se
# redacta el informe con lo que hay, diciendo qué queda por trabajar.
CODIGOS_BLOQUEANTES = {"PONDERACION_CERO", "NOTA_INVALIDA"}


def _emitir_alertas(estado: dict):
    """Saca por pantalla todas las alertas del estado, no solo la primera.

    Los avisos se imprimen y la ejecución continúa; un código bloqueante corta,
    pero solo después de haber mostrado los avisos que ya se habían detectado.
    """
    alertas = estado.get("alertas")
    if not alertas:
        alerta = estado.get("alerta")
        alertas = [alerta] if alerta else []

    bloqueantes = [a for a in alertas if a[0] in CODIGOS_BLOQUEANTES]
    avisos = [a for a in alertas if a[0] not in CODIGOS_BLOQUEANTES]

    for code, msg in avisos:
        print(f"{code}: {msg}")
    if bloqueantes:
        code, msg = bloqueantes[0]
        _emit_ia_code(code, msg)


def _agrupar_ces_por_ra(mod) -> dict[str, list[str]]:
    """Agrupa los Criterios de Evaluación (CE) correspondientes a cada RA."""
    ces_por_ra: dict[str, list[str]] = {}
    for _ut, ra_id, ces in mod.ASIGNACIONES:
        ces_por_ra.setdefault(ra_id, [])
        for ce in ces:
            if ce not in ces_por_ra[ra_id]:
                ces_por_ra[ra_id].append(ce)
    return ces_por_ra


def _es_de_recuperacion(act: dict | None) -> bool:
    """¿Es una actividad de la 2ª convocatoria? (Orden 201/2024, art. 21.5)

    Los informes y las estadísticas hablan del curso: meter en ellos la prueba de
    recuperación de junio mezclaría dos convocatorias distintas en la misma media.
    """
    try:
        return int((act or {}).get("convocatoria") or 1) == 2
    except (TypeError, ValueError):
        return False


def _ras_de_actividad(act: dict | None) -> list[str]:
    """RA que califica una actividad.

    Primero el suyo propio; si no lo tiene —caso del examen que cubre varias
    unidades— los que digan sus criterios, que van guardados como "RA4|CR1"
    porque el id del criterio se repite en todos los RA del módulo.
    """
    ra = str((act or {}).get("ra_id") or "").strip()
    if ra:
        return [ra]
    ces = (act or {}).get("ces")
    if isinstance(ces, str):
        try:
            ces = json.loads(ces or "[]")
        except Exception:
            ces = []
    salida: list[str] = []
    for clave in (ces or []):
        if "|" in str(clave):
            r = str(clave).split("|", 1)[0].strip()
            if r and r not in salida:
                salida.append(r)
    return salida


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


def _parse_notas_ra(raw: str | None) -> dict[str, dict[str, float]]:
    """{ alumno_id: { "RA1": 7.0, … } } tal y como lo calcula el motor del renderer.

    Aquí no se pueden replicar los pesos de cada actividad, la escala de cada
    instrumento, los RA cerrados en una sesión anterior ni las pruebas de la 2ª
    convocatoria: la aplicación manda las notas por RA ya hechas y este script
    solo las interpreta.
    """
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    salida: dict[str, dict[str, float]] = {}
    for aid, filas in data.items():
        if not isinstance(filas, dict):
            continue
        limpias = {}
        for ra_id, nota in filas.items():
            try:
                limpias[str(ra_id)] = float(nota)
            except (TypeError, ValueError):
                continue
        if limpias:
            salida[str(aid)] = limpias
    return salida


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
        alerta = ("RA_NO_EVALUADO", f"Módulo aún en curso: sin calificar todavía {', '.join(sin_nota)}.")
    else:
        resultado = "APTO" if (nota_final is not None and nota_final >= 5 and not pendientes) else "NO APTO"
        alerta = None

    if not sin_nota and pendientes:
        alerta = ("RA_SUSPENDIDO", f"El alumno tiene suspendido el RA: {', '.join(pendientes)}.")

    # Varias condiciones pueden darse a la vez (RA suspenso + absentismo, por
    # ejemplo). Antes cada una pisaba a la anterior y el diagnóstico salía
    # incompleto: ahora se acumulan todas y el informe las cuenta enteras.
    alertas: list[tuple[str, str]] = []
    if alerta:
        alertas.append(alerta)
    if alerta_absentismo:
        alertas.append(alerta_absentismo)
    if alerta_ra_llave:
        alertas.append(alerta_ra_llave)
        resultado = "NO APTO"
    alerta = alertas[0] if alertas else None

    nota_final_2 = None if nota_final is None else round(nota_final + 1e-12, 2)
    return {
        "nota_final": nota_final_2,
        "resultado": resultado,
        "pendientes": pendientes,
        "sin_nota": sin_nota,
        "alerta": alerta,      # la primera, por compatibilidad
        "alertas": alertas,    # todas las que se han dado a la vez
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
    opts = _parse_opts(args, ["--modulo", "--alumno", "--notas", "--proveedor", "--min-exam",
                              "--ponderaciones", "--anonimizar", "--faltas-porcentaje",
                              "--ras-llave", "--detalle-json"])
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
    _emitir_alertas(st)
    nota_final = st["nota_final"]
    resultado = st["resultado"]

    detalle = _parse_json_list(opts.get("--detalle-json"))
    contexto = _contexto_didactico(mod, notas, detalle)

    ia  = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.borrador_informe_alumno(alumno, mod.MODULO, notas, nota_final, resultado,
                                     contexto=contexto)
    print(f"\n{'='*60}")
    print(f"INFORME INDIVIDUAL — {alumno}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_plan(args: list[str]):
    """Plan de recuperación para el alumnado con RA pendientes."""
    opts = _parse_opts(args, ["--modulo", "--alumno", "--notas", "--proveedor", "--anonimizar",
                              "--detalle-json", "--semanas", "--min-exam", "--ponderaciones"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    anonimizar = str(opts.get("--anonimizar", "true")).lower() not in ("0", "false", "no", "off")
    alumno = _anonimizar_alumno_nombre(opts.get("--alumno", "Alumno Ejemplo"), activo=anonimizar)
    try:
        notas = _parse_notas(opts.get("--notas", ""))
    except ValueError as e:
        _emit_ia_code("NOTA_INVALIDA", f"Formato o rango de nota incorrecto: {e}")
    try:
        semanas = max(1, min(12, int(str(opts.get("--semanas", "4")).strip())))
    except Exception:
        semanas = 4

    ra_texto = {r["id"]: r.get("nombre", "") for r in mod.RAS}
    pendientes = [{"ra": ra, "nota": f"{n:.1f}", "enunciado": ra_texto.get(ra, "")}
                  for ra, n in sorted(notas.items()) if n < 5]
    if not pendientes:
        print("Este alumno o alumna no tiene resultados de aprendizaje pendientes: "
              "no hace falta plan de recuperación.")
        return

    contexto = _contexto_didactico(mod, notas, _parse_json_list(opts.get("--detalle-json")))
    ia = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.plan_recuperacion(alumno, mod.MODULO, pendientes, contexto, semanas)
    print(f"\n{'='*60}")
    print(f"PLAN DE RECUPERACIÓN — {alumno} · {len(pendientes)} RA pendientes")
    print(f"{'='*60}\n")
    print(out)


def _cmd_grupo(args: list[str]):
    """Radiografía del grupo: los números se calculan aquí, la IA solo interpreta."""
    opts = _parse_opts(args, ["--modulo", "--proveedor", "--alumnos-json",
                              "--notas-grid-json", "--actividades-json",
                              "--notas-ra-json"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    alumnos = _parse_json_list(opts.get("--alumnos-json"))
    grid    = _parse_json_list(opts.get("--notas-grid-json"))
    acts    = [a for a in _parse_json_list(opts.get("--actividades-json"))
               if not _es_de_recuperacion(a)]
    if not alumnos or not grid or not acts:
        _emit_ia_code("SIN_DATOS",
                      "Faltan datos del grupo. Necesito alumnado, actividades y notas guardadas.")

    act_por_id = {a.get("id"): a for a in acts}
    ra_texto = {r["id"]: r.get("nombre", "") for r in mod.RAS}
    ra_pond  = {r["id"]: r.get("pond") for r in mod.RAS}

    def _nota(fila):
        n = fila.get("nota_rec") if fila.get("nota_rec") is not None else fila.get("nota")
        try:
            return float(n)
        except (TypeError, ValueError):
            return None

    # Notas por alumno y RA. Las manda calculadas la aplicación; solo si no
    # llegan (versión antigua) se recurre a la media de las notas crudas.
    notas_ra_app = _parse_notas_ra(opts.get("--notas-ra-json"))
    por_alumno_ra: dict[Any, dict[str, list[float]]] = {}
    por_actividad: dict[Any, list[float]] = {}
    for fila in grid:
        n = _nota(fila)
        if n is None:
            continue
        act = act_por_id.get(fila.get("actividad_id")) or {}
        # Cada instrumento tiene su escala: un 7 sobre 20 no es un aprobado.
        try:
            nota_max = float(act.get("nota_max") or 10) or 10
        except (TypeError, ValueError):
            nota_max = 10
        por_actividad.setdefault(fila.get("actividad_id"), []).append(n * 10 / nota_max)
        if notas_ra_app:
            continue
        for ra in _ras_de_actividad(act):
            por_alumno_ra.setdefault(fila.get("alumno_id"), {}).setdefault(ra, []).append(n)
    for aid, filas in notas_ra_app.items():
        por_alumno_ra[aid] = {ra_id: [nota] for ra_id, nota in filas.items()}

    def _media(xs):
        return round(sum(xs) / len(xs), 2) if xs else None

    ras_stats = []
    for r in mod.RAS:
        notas_ra = [_media(v.get(r["id"], [])) for v in por_alumno_ra.values()]
        notas_ra = [x for x in notas_ra if x is not None]
        if not notas_ra:
            continue
        aprob = sum(1 for x in notas_ra if x >= 5)
        ras_stats.append({
            "id": r["id"], "pond": ra_pond.get(r["id"]), "enunciado": ra_texto.get(r["id"], ""),
            "media": _media(notas_ra), "aprobados": aprob, "total": len(notas_ra),
            "porcentaje": round(100 * aprob / len(notas_ra)),
        })

    acts_stats = []
    for aid, notas_act in por_actividad.items():
        act = act_por_id.get(aid) or {}
        aprob = sum(1 for x in notas_act if x >= 5)
        acts_stats.append({
            "descripcion": str(act.get("descripcion", "(actividad)"))[:90],
            "media": _media(notas_act), "aprobados": aprob, "total": len(notas_act),
            "porcentaje": round(100 * aprob / len(notas_act)),
        })
    acts_stats.sort(key=lambda a: (a["porcentaje"], a["media"] or 0))

    medias_alumno = []
    superan = 0
    for _aid, ras_al in por_alumno_ra.items():
        medias = {ra: _media(v) for ra, v in ras_al.items()}
        vals = [v for v in medias.values() if v is not None]
        if not vals:
            continue
        medias_alumno.append(_media(vals))
        if len(medias) == len(ras_stats) and all(v >= 5 for v in vals):
            superan += 1

    stats = {
        "n_alumnos": len(medias_alumno),
        "media_grupo": _media(medias_alumno),
        "superan": superan,
        "ras": ras_stats,
        "actividades": acts_stats,
    }

    ia = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.radiografia_grupo(mod.MODULO, stats)
    print(f"\n{'='*60}")
    print(f"RADIOGRAFÍA DEL GRUPO — {mod.MODULO['abrev']} · {stats['n_alumnos']} alumnos/as")
    print(f"{'='*60}\n")
    for r in ras_stats:
        print(f"  {r['id']}: media {r['media']} · aprueban {r['aprobados']}/{r['total']} ({r['porcentaje']}%)")
    print()
    print(out)


def _cmd_examen(args: list[str]):
    """Prueba escrita + solucionario a partir de los CE del decreto."""
    opts = _parse_opts(args, ["--modulo", "--ra", "--n", "--tipo", "--duracion", "--proveedor"])
    mod = _cargar_modulo(opts.get("--modulo", "iso_data"))
    ra_id = opts.get("--ra", mod.RAS[0]["id"])
    ra = next((r for r in mod.RAS if r["id"] == ra_id), None)
    if not ra:
        _emit_ia_code("RA_NO_ENCONTRADO", f"El RA '{ra_id}' no existe en este módulo.")
    try:
        n = max(3, min(20, int(str(opts.get("--n", "8")).strip())))
    except Exception:
        n = 8
    try:
        duracion = max(15, min(180, int(str(opts.get("--duracion", "50")).strip())))
    except Exception:
        duracion = 50
    tipo = str(opts.get("--tipo", "mixto")).strip().lower()
    if tipo not in ("mixto", "test", "desarrollo", "practico"):
        tipo = "mixto"

    ces = _agrupar_ces_por_ra(mod).get(ra_id, [])
    ia = IAAsistente(proveedor=opts.get("--proveedor", "auto"))
    out = ia.examen_con_solucionario(mod.MODULO, ra, ces, n, tipo, duracion)
    print(f"\n{'='*60}")
    print(f"PRUEBA ESCRITA — {ra_id}: {ra['nombre'][:70]}")
    print(f"{'='*60}\n")
    print(out)


def _cmd_generar_todo(args: list[str]):
    opts      = _parse_opts(args, ["--modulo", "--salida", "--proveedor", "--alumnos-json",
                                   "--notas-grid-json", "--actividades-json", "--notas-ra-json"])
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
    actividades = [a for a in _parse_json_list(opts.get("--actividades-json"))
                   if not _es_de_recuperacion(a)]

    notas_ra = _parse_notas_ra(opts.get("--notas-ra-json"))

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
                    ras_act = _ras_de_actividad(act) or (
                        [str(row.get('ra_id')).strip()] if row.get('ra_id') else [])
                    if not ras_act:
                        continue
                    nota_val = row.get('nota_rec') if row.get('nota_rec') is not None else row.get('nota')
                    try:
                        nota_num = float(nota_val)
                    except Exception:
                        continue
                    # Si la actividad cubre varios RA, su peso se reparte entre ellos
                    peso = float((act or {}).get('peso') or 1) / len(ras_act)
                    for ra_id in ras_act:
                        ra_map.setdefault(ra_id, []).append((nota_num, peso))
                for ra_id, vals in ra_map.items():
                    den = sum(p for _, p in vals) or len(vals)
                    num = sum(n * p for n, p in vals)
                    notas[ra_id] = num / den if den else 0.0
                # Si la aplicación ha mandado las notas por RA calculadas con su
                # motor, mandan ellas: son las que figuran en Evaluaciones.
                if str(alumno.get("id")) in notas_ra:
                    notas = dict(notas_ra[str(alumno.get("id"))])
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
      plan      --alumno "<Nombre Apellidos>"  --notas "RA1:7,RA3:3"  [--semanas 4]
      grupo     --alumnos-json <json>  --notas-grid-json <json>  --actividades-json <json>
      examen    --ra <RA_ID>  [--n 8]  [--tipo mixto|test|desarrollo|practico]  [--duracion 50]
      todo      --salida <directorio>

    Variables de entorno:
      ANTHROPIC_API_KEY   Clave de API para Claude (recomendado)
      OPENAI_API_KEY      Clave de API para OpenAI (alternativa)

    Si no se configura ninguna clave → modo DEMO (texto de ejemplo local).

    Ejemplos:
      python ai_asistente.py rubrica --modulo iso_data --ra RA1
      python ai_asistente.py actividad --modulo par_data --ra RA3 --n 2
      python ai_asistente.py informe --alumno "García López, Marta" --notas "RA1:7,RA2:4,RA3:8"
      python ai_asistente.py plan --modulo iso_data --alumno "García, Marta" --notas "RA1:7,RA3:3"
      python ai_asistente.py examen --modulo iso_data --ra RA3 --n 8 --tipo mixto
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
    elif cmd == "plan":
        _cmd_plan(resto)
    elif cmd == "grupo":
        _cmd_grupo(resto)
    elif cmd == "examen":
        _cmd_examen(resto)
    elif cmd == "todo":
        _cmd_generar_todo(resto)
    else:
        print(f"❌ Comando desconocido: '{cmd}'. Usa --ayuda para ver opciones.")
        sys.exit(1)

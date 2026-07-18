# AGENTS.md — EvalFP (Cuaderno del Profesor para FP)

## Qué es este proyecto

Aplicación de escritorio Electron para que el profesorado de Formación Profesional en España gestione programación didáctica, registro de notas y evaluación por Resultados de Aprendizaje (RA). Base de datos SQLite local (`better-sqlite3`), sin backend remoto.

## Stack

- **App**: Electron (`main.js`, `preload.js`, `db.js`) + `renderer/` (frontend)
- **Generación de materiales**: scripts Python en `scripts/` (`build_apuntes.py`, `build_template.py`, `ai_asistente.py`)
- **Config del profesor/módulos**: `scripts/teacher_config.py`, `scripts/modules/*_data.py`
- **Build**: `electron-builder` (ver `build-mac.sh`, `entitlements.mac.plist`)

## Comandos

```bash
npm start              # arrancar la app en desarrollo
npm run prebake        # regenerar datos de módulos antes de build
npm run build:mac      # build macOS (incluye prebake)
npm run build:win      # build Windows (incluye prebake)
pip install -r requirements.txt   # dependencias Python de scripts/
```

## Reglas del proyecto (ver `docs/guia_desarrollo.md` y `docs/decisiones_arquitectura.md`)

- Cada sprint debe dejar el programa completamente funcional — nunca commitear a medias.
- No romper compatibilidad hacia atrás.
- Nunca usar referencias de celda fijas de Excel; todo mediante tablas estructuradas (ADR-003).
- Un archivo = un curso académico; un profesor por archivo (ADR-001, ADR-002).
- Sin dependencias de Microsoft Access (ADR-004).
- Compatibilidad obligatoria Windows y macOS (ADR-005).
- Sin complementos externos obligatorios (ADR-006).
- Añadir un nuevo módulo de FP: crear `*_data.py` en `scripts/modules/` y registrarlo en `teacher_config.py`.

## Datos sensibles

Este proyecto maneja datos de alumnado (nombre, NIA, fecha de nacimiento, notas). **Nunca** commitear `evalfp.db` con datos reales, ni incluir nombres/datos de alumnos reales en ejemplos, tests o documentación. El `.gitignore` ya excluye `*.db`, pero revisa siempre antes de un `git add -A`.

## Licencia

GPLv3 — cualquier código añadido debe ser compatible con esta licencia.

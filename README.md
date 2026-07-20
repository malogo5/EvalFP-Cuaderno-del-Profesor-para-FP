# EvalFP — Cuaderno del Profesor para FP

[![Licencia: GPL-3.0-or-later](https://img.shields.io/badge/Licencia-GPL--3.0--or--later-blue.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/versión-3.0.0-orange.svg)](CHANGELOG.md)

EvalFP es una aplicación de escritorio Electron para profesorado de Formación Profesional en España. Gestiona programación didáctica, alumnado, notas, evaluaciones, informes y materiales de apoyo en una base de datos SQLite local, sin backend remoto.

**Versión actual:** 3.0.0 · Consulta el [CHANGELOG](CHANGELOG.md) y la [ruta del proyecto](docs/refactor/03_ROADMAP.md) para el historial y la evolución.

## Lo esencial

- Funcionamiento local en macOS y Windows.
- Datos de alumnado guardados solo en tu equipo.
- Motor de módulos ampliable con archivos `*_data.py`.
- Generación opcional de materiales con Python e IA.

## Primeros pasos

1. Instala dependencias.
2. Arranca la app en local.
3. Selecciona o crea un módulo.
4. Importa tu alumnado.
5. Empieza a registrar actividades y notas.

```bash
npm install
npm start
```

Si quieres el flujo completo de instalación y uso, abre [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md).

## Funcionalidades

- Gestión de módulos y grupos.
- Alumnado con edición rápida.
- Registro de notas por actividades y evaluaciones.
- Dashboard y boletines.
- Asistente IA opcional para rúbricas, actividades e informes.
- Generación de instaladores para macOS y Windows.

## Desarrollo y pruebas

```bash
npm run prebake
npm test
npm run test:e2e
npm run lint
npm run build:mac
npm run build:win
```

## Estructura principal

- `main.js`, `preload.js`, `db.js`: núcleo de Electron.
- `renderer/`: interfaz de usuario.
- `scripts/`: generación de módulos, plantilla y asistente IA.
- `docs/`: decisiones, guía de desarrollo y notas técnicas.

## Añadir un módulo

1. Crea un archivo nuevo en `scripts/modules/` siguiendo el patrón de `iso_data.py`.
2. Regístralo en `scripts/teacher_config.py`.
3. Ejecuta `npm run prebake`.
4. Vuelve a abrir la app o genera el instalador.

## Documentación útil

- [docs/guia_desarrollo.md](docs/guia_desarrollo.md)
- [docs/decisiones_arquitectura.md](docs/decisiones_arquitectura.md)
- [docs/version_2.md](docs/version_2.md)
- [docs/casos_uso.md](docs/casos_uso.md)

## Licencia

EvalFP se distribuye bajo [GNU GPL v3.0 o posterior](LICENSE).

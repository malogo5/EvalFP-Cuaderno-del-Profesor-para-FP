# Instalación y uso de EvalFP

Este documento resume cómo instalar y usar la aplicación en macOS y Windows.

## Qué necesitas

- Un equipo con macOS o Windows.
- El instalador de EvalFP o el proyecto en local si vas a desarrollarlo.
- Python 3.10+ solo si vas a regenerar módulos o usar las funciones de IA desde scripts.
- Node.js 22+ solo si vas a ejecutar la app o construirla desde el código fuente.

## Instalación en macOS

1. Abre el archivo `.dmg`.
2. Arrastra `EvalFP` a `Applications`.
3. Abre la app desde `Applications` o con Spotlight.
4. Si macOS muestra una advertencia de seguridad, ve a `Ajustes del sistema > Privacidad y seguridad` y permite la apertura.

## Instalación en Windows

1. Ejecuta el instalador `.exe`.
2. Sigue el asistente de instalación.
3. Si lo prefieres, deja marcada la opción de acceso directo en el escritorio.
4. Abre EvalFP desde el menú Inicio o el acceso directo creado.

## Primer arranque

1. Abre EvalFP.
2. Crea o selecciona tu módulo.
3. Importa el alumnado.
4. Empieza a registrar actividades y notas.
5. Revisa el dashboard y los boletines al terminar la evaluación.

## Uso básico

- `Inicio`: guía rápida para empezar.
- `Módulos`: alta, selección y gestión de módulos.
- `Alumnos`: edición del alumnado.
- `Notas`: registro de calificaciones.
- `Evaluaciones`: resultados parciales y finales.
- `Dashboard`: resumen visual del módulo.
- `Asistente IA`: generación opcional de contenidos.
- `Ajustes`: configuración general.

## Buenas prácticas

- Haz copias de seguridad periódicas de tu carpeta de datos del usuario.
- No compartas la base de datos con datos reales de alumnado.
- Mantén actualizada la versión instalada.
- Si vas a usar IA, configura primero tus claves API de forma segura.

## Si trabajas desde el repositorio

```bash
npm install
npm start
```

Para generar instaladores:

```bash
npm run prebake
npm run build:mac
npm run build:win
```

## Asistente IA

El asistente es opcional. Si no configuras API keys, funciona en modo demo.

## Licencia

EvalFP se distribuye bajo licencia GPLv3 o posterior.

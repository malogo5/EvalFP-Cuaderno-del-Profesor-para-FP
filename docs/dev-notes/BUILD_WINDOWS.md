# EvalFP — Build para Windows

## Requisitos

- **Node.js 22+** → https://nodejs.org (descargar el instalador LTS)
- **Python 3.10+** → https://www.python.org (marcar "Add to PATH" durante la instalación)

## Pasos

Abre una terminal (PowerShell o CMD) en la carpeta `evalfp-app/`:

```powershell
# 1. Instalar dependencias (solo la primera vez)
npm install

# 2. Pre-hornear módulos (genera renderer/modules_data.json)
python ..\scripts\prebake_modules.py

# 3. Generar el instalador .exe
npm run build:win
```

El instalador quedará en `evalfp-app\dist\EvalFP Setup 3.0.0.exe`.

## Notas

- El icono `assets\icon.ico` debe existir antes de hacer el build.
  Si no lo tienes, puedes omitirlo quitando las líneas `"icon"` del `package.json` o generándolo con:
  ```
  magick assets\icon.png -resize 256x256 assets\icon.ico
  ```

- El instalador NSIS creará accesos directos en el Escritorio y en el Menú Inicio.

- La app **no necesita Python instalado** para su uso normal.
  Python solo es necesario si se usan las funciones de IA (Asistente IA / Apuntes).

## Cross-compile desde Mac (avanzado)

Para generar el `.exe` desde macOS sin una VM Windows:

```bash
# Instalar Wine + Mono (solo la primera vez, vía Homebrew)
brew install --cask wine-crossover

# Luego desde evalfp-app/
npm run prebake
npx electron-builder --win --x64
```

> ⚠️ La firma de código (.exe con certificado) requiere un certificado EV y
> solo es posible ejecutándolo en una máquina Windows real o en un CI Windows
> (GitHub Actions, por ejemplo).

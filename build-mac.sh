#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# build-mac.sh — Genera EvalFP.dmg (arm64 + x64) para macOS
#
# Uso:
#   cd evalfp
#   bash build-mac.sh
#
# Requisitos:
#   • Node.js 22+  (node --version)
#   • Python 3.10+ (python3 --version)
#   • npm install  (ejecutar una vez si node_modules no existe)
#
# Para firmar y notarizar (opcional, necesario para distribución pública):
#   export APPLE_ID="tu@email.com"
#   export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
#   export APPLE_TEAM_ID="XXXXXXXXXX"
#   bash build-mac.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   EvalFP — Build Mac  🍎                 ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 0. Comprobaciones ─────────────────────────────────────────────────────────
command -v node    >/dev/null 2>&1 || { echo "❌  node no encontrado. Instala Node.js 22+"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌  python3 no encontrado. Instala Python 3.10+"; exit 1; }

NODE_VER=$(node -e "process.stdout.write(process.versions.node)")
echo "✅  Node  $NODE_VER"
echo "✅  Python $(python3 --version)"
echo ""

# ── 1. Dependencias npm ───────────────────────────────────────────────────────
if [ ! -d "node_modules" ]; then
  echo "📦  Instalando dependencias npm…"
  npm install
fi

# ── 2. Pre-hornear módulos → renderer/modules_data.json ──────────────────────
echo "🐍  Pre-horneando módulos Python → modules_data.json…"
python3 scripts/prebake_modules.py

# ── 3. Limpiar dist anterior ──────────────────────────────────────────────────
if [ -d "dist" ]; then
  echo "🧹  Limpiando dist/ anterior…"
  rm -rf dist
fi

# ── 4. Electron Builder ───────────────────────────────────────────────────────
echo ""
echo "🔨  Construyendo .app y .dmg…"
echo ""
npx electron-builder --mac --config.mac.identity=null

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   ✅  Build completado                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📂  Salida:  dist/"
ls -lh dist/*.dmg 2>/dev/null || true
echo ""

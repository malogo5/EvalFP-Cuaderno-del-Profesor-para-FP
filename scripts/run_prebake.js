'use strict'

const { spawnSync } = require('child_process')
const path = require('path')

const python = process.platform === 'win32' ? 'python' : 'python3'
const script = path.join(__dirname, 'prebake_modules.py')
// Windows usa cp1252 en muchas consolas por defecto. El catálogo informa de
// módulos con símbolos Unicode, así que forzamos UTF-8 en todas las plataformas.
const result = spawnSync(python, [script], {
  stdio: 'inherit',
  env: {
    ...process.env,
    PYTHONUTF8: '1',
    PYTHONIOENCODING: 'utf-8',
  },
})

if (result.error) {
  console.error(`No se pudo ejecutar ${python}: ${result.error.message}`)
  process.exit(1)
}
process.exit(result.status ?? 1)

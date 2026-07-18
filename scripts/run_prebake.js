'use strict'

const { spawnSync } = require('child_process')
const path = require('path')

const python = process.platform === 'win32' ? 'python' : 'python3'
const script = path.join(__dirname, 'prebake_modules.py')
const result = spawnSync(python, [script], { stdio: 'inherit' })

if (result.error) {
  console.error(`No se pudo ejecutar ${python}: ${result.error.message}`)
  process.exit(1)
}
process.exit(result.status ?? 1)

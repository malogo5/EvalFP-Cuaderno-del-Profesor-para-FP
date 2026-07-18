/**
 * Setup global para tests unitarios — inyecta el mock de Electron
 * directamente en require.cache de Node.js ANTES de que db.js cargue.
 *
 * Por qué es necesario:
 *   db.js usa require('electron') en CommonJS (CJS). Vitest intercepta
 *   imports ESM, pero NO los require() de Node. La única forma fiable de
 *   mockar un módulo CJS sin modificar el código fuente es precargar el
 *   mock en require.cache antes de que el módulo lo llame.
 */

import { createRequire } from 'module'
import os   from 'os'
import path from 'path'
import fs   from 'fs'

const _require = createRequire(import.meta.url)

const TEST_DB_DIR = path.join(os.tmpdir(), `evalfp-test-${process.pid}`)

// Crear el directorio de la DB de test si no existe
fs.mkdirSync(TEST_DB_DIR, { recursive: true })

// Inyectar el mock de Electron en el cache de require()
_require.cache[_require.resolve('electron')] = {
  id:       _require.resolve('electron'),
  filename: _require.resolve('electron'),
  loaded:   true,
  exports: {
    app: {
      getPath: (name) => name === 'userData' ? TEST_DB_DIR : os.tmpdir(),
    },
  },
}

import { defineConfig } from 'vitest/config'

// db.js usa `node:sqlite`, que Electron trae habilitado pero Node sólo expone
// con --experimental-sqlite entre 22.5 y 23.3 (a partir de 23.4 va sin flag).
// La detección se hace por número de versión y no cargando el módulo, porque
// cargarlo aquí ya imprimiría el ExperimentalWarning en el proceso principal.
const [may, men] = process.versions.node.split('.').map(Number)
const version = may + men / 1000
const execArgv = []
if (version >= 22.005 && version < 23.004) execArgv.push('--experimental-sqlite')
if (version >= 21.003) execArgv.push('--disable-warning=ExperimentalWarning')

export default defineConfig({
  test: {
    environment: 'node',
    globals: false,
    // Parchea require.cache para que require('electron') en db.js (CJS)
    // devuelva el mock antes de que el módulo se cargue.
    setupFiles: ['./tests/unit/setup.js'],
    // Excluir tests E2E de Playwright — los ejecuta `npm run test:e2e`
    exclude: ['tests/e2e/**', 'node_modules/**'],
    // forks (no threads) para poder pasar flags de Node al proceso de test.
    // En Vitest 4 execArgv es opción de primer nivel (ya no va en poolOptions).
    pool: 'forks',
    execArgv,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['db.js', 'renderer/js/modules/evaluaciones.js'],
    },
  },
})

import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
    globals: false,
    // Parchea require.cache para que require('electron') en db.js (CJS)
    // devuelva el mock antes de que el módulo se cargue.
    setupFiles: ['./tests/unit/setup.js'],
    // Excluir tests E2E de Playwright — los ejecuta `npm run test:e2e`
    exclude: ['tests/e2e/**', 'node_modules/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['db.js', 'renderer/js/modules/evaluaciones.js'],
    },
  },
})

'use strict'
/**
 * Playwright — Configuración para tests E2E de EvalFP (Electron)
 *
 * Documentación: https://playwright.dev/docs/api/class-electron
 *
 * Ejecutar:
 *   npm run test:e2e         → todos los tests
 *   npm run test:e2e:ui      → modo interactivo con interfaz visual
 *   npx playwright test --headed  → con ventana visible (debug)
 */

const { defineConfig } = require('@playwright/test')

module.exports = defineConfig({
  testDir:  './tests/e2e',
  timeout:  45_000,           // Electron tarda en arrancar

  // Reintentar una vez en CI si falla (flakiness de UI)
  retries: process.env.CI ? 1 : 0,

  // En local: mostrar solo los fallos; en CI: verbose
  reporter: process.env.CI
    ? [['github'], ['html', { outputFolder: 'playwright-report', open: 'never' }]]
    : 'list',

  use: {
    // Capturas automáticas de pantalla al fallar
    screenshot: 'only-on-failure',
    screenshotPath: './tests/e2e/screenshots',

    // Vídeo del fallo para debug
    video: 'retain-on-failure',

    // Traza completa en el primer reintento
    trace: 'on-first-retry',
  },

  // No hay proyectos de browsers — Electron usa su propio Chromium embebido
})

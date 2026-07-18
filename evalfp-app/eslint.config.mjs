/**
 * ESLint Flat Config — EvalFP
 * Documentación: https://eslint.org/docs/latest/use/configure/configuration-files
 *
 * Instalación (una sola vez):
 *   npm install --save-dev eslint @eslint/js globals
 *
 * Uso:
 *   npm run lint          → revisar todo el proyecto
 *   npm run lint:fix      → corregir automáticamente lo que se pueda
 */

import js      from '@eslint/js'
import globals from 'globals'

export default [
  // ── Ignorar carpetas que no son código fuente ──────────────────────────
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      'dist-staging/**',
      'playwright-report/**',
    ],
  },

  // ── Reglas base recomendadas ───────────────────────────────────────────
  js.configs.recommended,

  // ── Proceso principal Electron y utilidades Node (CommonJS) ───────────
  // main.js, preload.js, db.js, main/*.js
  {
    files: ['main.js', 'preload.js', 'db.js', 'main/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType:  'commonjs',
      globals: {
        ...globals.node,
      },
    },
    rules: {
      'no-unused-vars':    ['warn', { argsIgnorePattern: '^_' }],
      'no-console':        'off',
      'semi':              ['warn', 'never'],
      'no-var':            'error',
      'prefer-const':      'warn',
      'eqeqeq':            ['warn', 'always'],   // warn (no error) para legacy !=
      'no-throw-literal':  'error',
    },
  },

  // ── Mocks y configuración Playwright (CommonJS) ───────────────────────
  {
    files: ['__mocks__/**/*.js', 'playwright.config.js'],
    languageOptions: {
      ecmaVersion:  2022,
      sourceType:   'commonjs',
      globals: {
        ...globals.node,
      },
    },
  },

  // ── Módulos del renderer (scripts del navegador, multi-archivo) ────────
  // Electron carga estos archivos como <script> en el renderer process.
  // Las funciones definidas en otros archivos (renderModulos, esc…)
  // son globals legítimas del entorno multi-script; desactivamos no-undef.
  {
    files: ['renderer/js/app.js', 'renderer/js/modules/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType:  'script',
      globals: {
        ...globals.browser,
        // setTimeout / clearTimeout / setInterval también en renderer
        setTimeout:   'readonly',
        clearTimeout: 'readonly',
        setInterval:  'readonly',
      },
    },
    rules: {
      'no-undef':       'off',   // Cross-file globals en arquitectura multi-script
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-console':     'off',
      'no-var':         'warn',
      'prefer-const':   'warn',
    },
  },

  // ── Utils del renderer (module.exports condicional) ───────────────────
  // Estos archivos exportan con module.exports para poder usarse
  // tanto en el renderer (inyectados como script) como en tests Node.
  {
    files: ['renderer/js/utils/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType:  'script',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      'no-unused-vars':          ['warn', { argsIgnorePattern: '^_' }],
      'no-console':              'off',
      'no-prototype-builtins':   'warn',
    },
  },

  // ── Tests unitarios (ESM + Vitest globals) ────────────────────────────
  {
    files: ['tests/unit/**/*.{js,mjs}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType:  'module',
      globals: {
        ...globals.node,
        describe:   'readonly',
        it:         'readonly',
        expect:     'readonly',
        beforeEach: 'readonly',
        afterEach:  'readonly',
        vi:         'readonly',
      },
    },
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-empty':       'warn',
    },
  },

  // ── Tests E2E (Playwright, CommonJS) ─────────────────────────────────
  // Incluye globals del navegador y del renderer multi-script porque el
  // código dentro de page.evaluate() se ejecuta en el renderer de Electron.
  {
    files: ['tests/e2e/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType:  'commonjs',
      globals: {
        ...globals.node,
        ...globals.browser,
        test:           'readonly',
        expect:         'readonly',
        _modulos:       'writable',
        _curMod:        'writable',
        updateModBadge: 'readonly',
        selectMod:      'readonly',
      },
    },
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    },
  },
]

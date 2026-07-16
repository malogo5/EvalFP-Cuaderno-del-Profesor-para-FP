# 🐛 Issues Encontrados - EvalFP

**Total de issues**: 28  
**Críticos**: 4  
**Importantes**: 8  
**Menores**: 16

---

## 🔴 CRÍTICOS (Resolver ASAP)

### SEC-001: XSS en renderModulos()
**Archivo**: `renderer/js/modules/modulos.js` líneas 11-22  
**Severidad**: 🔴 CRÍTICA  
**Tipo**: Cross-Site Scripting (XSS)

**Código vulnerable**:
```javascript
el.innerHTML = _modulos.map(m => `
  <div class="mod-card" onclick="selectMod(${m.id})">
    <div class="mod-card-abrev">${m.abrev}</div>
    <div class="mod-card-nombre">${m.nombre}</div>  // ⚠️ NO ESCAPADO
    <div class="mod-card-meta">
      ${m.ciclo||''} · ${m.curso||''} · ${m.anno||''}
      ${m.decreto ? `<br><span>${m.decreto}</span>` : ''}  // ⚠️ NO ESCAPADO
    </div>
  </div>
`).join('')
```

**Ataque posible**:
- Nombre del módulo: `<img src=x onerror="alert('Hacked')">`
- Decreto: `<script>alert('XSS')</script>`

**Fix**:
```javascript
el.innerHTML = _modulos.map(m => `
  <div class="mod-card" onclick="selectMod(${m.id})">
    <div class="mod-card-abrev">${esc(m.abrev)}</div>
    <div class="mod-card-nombre">${esc(m.nombre)}</div>
    <div class="mod-card-meta">
      ${esc(m.ciclo||'')} · ${esc(m.curso||'')} · ${esc(m.anno||'')}
      ${m.decreto ? `<br><span>${esc(m.decreto)}</span>` : ''}
    </div>
  </div>
`).join('')
```

**Tiempo estimado**: 30 minutos

---

### SEC-002: XSS en renderModRasPanel()
**Archivo**: `renderer/js/modules/modulos.js` líneas 76-100+  
**Severidad**: 🔴 CRÍTICA  
**Tipo**: Cross-Site Scripting (XSS)

**Código vulnerable**:
```javascript
html += `
  <div class="card">
    <span>${ra.nombre}</span>  // ⚠️ NO ESCAPADO
    ${raCes.length ? `<div>${raCes.map(ce => `
      <span>${ce.texto}</span>  // ⚠️ NO ESCAPADO
    `).join('')}</div>` : ''}
  </div>
`
```

**Fix**:
```javascript
html += `
  <div class="card">
    <span>${esc(ra.nombre)}</span>
    ${raCes.length ? `<div>${raCes.map(ce => `
      <span>${esc(ce.texto)}</span>
    `).join('')}</div>` : ''}
  </div>
`
```

**Tiempo estimado**: 30 minutos

---

### SEC-003: Claves API sin encripción
**Archivo**: `main.js` líneas 48-53  
**Severidad**: 🔴 CRÍTICA  
**Tipo**: Almacenamiento inseguro de secretos

**Código vulnerable**:
```javascript
const cfg = db.getAllConfig()
if (cfg.openaiKey)    process.env.OPENAI_API_KEY    = cfg.openaiKey
if (cfg.anthropicKey) process.env.ANTHROPIC_API_KEY = cfg.anthropicKey
```

**Problemas**:
- Las claves se guardan en **texto plano** en SQLite
- Se cargan en `process.env` (visible en memory dumps)
- No hay encriptación

**Fix**:
```javascript
// Instalar keytar
// npm install keytar

const keytar = require('keytar')
const SERVICE_NAME = 'EvalFP'

async function loadApiKeys() {
  const openaiKey = await keytar.getPassword(SERVICE_NAME, 'openai-key')
  const anthropicKey = await keytar.getPassword(SERVICE_NAME, 'anthropic-key')
  
  if (openaiKey) process.env.OPENAI_API_KEY = openaiKey
  if (anthropicKey) process.env.ANTHROPIC_API_KEY = anthropicKey
}

// En ajustes.js:
async function saveAjustes() {
  const openaiKey = document.getElementById('cfg-openai').value
  const anthropicKey = document.getElementById('cfg-anthropic').value
  
  if (openaiKey) {
    await keytar.setPassword(SERVICE_NAME, 'openai-key', openaiKey)
  }
  if (anthropicKey) {
    await keytar.setPassword(SERVICE_NAME, 'anthropic-key', anthropicKey)
  }
}
```

**Tiempo estimado**: 1-2 horas (incluye testing)

---

### SEC-004: Sin respaldo de base de datos
**Archivo**: `main.js`  
**Severidad**: 🔴 CRÍTICA  
**Tipo**: Pérdida de datos

**Problema**:
- No hay backups automáticos
- Si se corrompe la DB, se pierden **todos los datos**
- Sin historial de cambios

**Fix**:
```javascript
// Instalar node-schedule
// npm install node-schedule

const schedule = require('node-schedule')

function setupBackups() {
  const dbPath = path.join(app.getPath('userData'), 'evalfp.db')
  const backupDir = path.join(app.getPath('userData'), 'backups')
  
  // Crear backup diario a las 2 AM
  schedule.scheduleJob('0 2 * * *', () => {
    try {
      fs.mkdirSync(backupDir, { recursive: true })
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
      const backupPath = path.join(backupDir, `evalfp_${timestamp}.db`)
      fs.copyFileSync(dbPath, backupPath)
      
      // Limpiar backups > 30 días
      const files = fs.readdirSync(backupDir)
      const now = Date.now()
      files.forEach(f => {
        const fPath = path.join(backupDir, f)
        const stats = fs.statSync(fPath)
        if (now - stats.mtimeMs > 30 * 24 * 60 * 60 * 1000) {
          fs.unlinkSync(fPath)
        }
      })
    } catch (err) {
      console.error('Backup failed:', err)
    }
  })
}

app.whenReady().then(() => {
  setupBackups()
  // ... resto del código
})
```

**Tiempo estimado**: 1 hora

---

## 🟡 IMPORTANTES (Próximas 2 semanas)

### SEC-005: Falta validación en preload
**Archivo**: `preload.js`  
**Severidad**: 🟡 IMPORTANTE

**Problema**:
```javascript
contextBridge.exposeInMainWorld('api', {
  saveAlumno: a => ipcRenderer.invoke('db:saveAlumno', a)  // ⚠️ Sin validar
})
```

**Fix**:
```javascript
function validateAlumno(a) {
  if (!Number.isInteger(a.modulo_id)) throw new Error('modulo_id inválido')
  if (a.apellidos && a.apellidos.length > 100) throw new Error('apellidos muy largo')
  if (a.nombre && a.nombre.length > 100) throw new Error('nombre muy largo')
  if (a.num && (!Number.isInteger(a.num) || a.num < 1)) throw new Error('num inválido')
  return true
}

contextBridge.exposeInMainWorld('api', {
  saveAlumno: a => {
    validateAlumno(a)
    return ipcRenderer.invoke('db:saveAlumno', a)
  }
})
```

---

### SEC-006: Sin logging de errores
**Archivo**: `main.js` múltiples ubicaciones  
**Severidad**: 🟡 IMPORTANTE

**Problema**:
```javascript
try {
  const db = require('./db')
  const cfg = db.getAllConfig()
  if (cfg.openaiKey) process.env.OPENAI_API_KEY = cfg.openaiKey
} catch {}  // ❌ ERROR SILENCIOSO
```

**Fix**:
```javascript
// Crear logger.js
const fs = require('fs')
const path = require('path')

class Logger {
  constructor(logDir) {
    this.logDir = logDir
    fs.mkdirSync(logDir, { recursive: true })
  }

  error(msg, err) {
    const log = `[${new Date().toISOString()}] ERROR: ${msg}\n${err?.stack || ''}\n`
    fs.appendFileSync(path.join(this.logDir, 'error.log'), log)
    console.error(msg, err)
  }

  warn(msg) {
    const log = `[${new Date().toISOString()}] WARN: ${msg}\n`
    fs.appendFileSync(path.join(this.logDir, 'warn.log'), log)
    console.warn(msg)
  }

  info(msg) {
    const log = `[${new Date().toISOString()}] INFO: ${msg}\n`
    fs.appendFileSync(path.join(this.logDir, 'info.log'), log)
  }
}

module.exports = Logger
```

---

### SEC-007: HTML injection en notas.js
**Archivo**: `renderer/js/modules/notas.js` línea 42  
**Severidad**: 🟡 IMPORTANTE

**Código vulnerable**:
```javascript
<th title="${a.descripcion}" style="text-align:center">
  <div>${a.instrumento}</div>  // ⚠️ NO ESCAPADO en content
</th>
```

**Fix**:
```javascript
<th title="${esc(a.descripcion)}" style="text-align:center">
  <div>${esc(a.instrumento)}</div>
</th>
```

---

### SEC-008: Sin validación de notas
**Archivo**: `renderer/js/modules/notas.js`  
**Severidad**: 🟡 IMPORTANTE

**Problema**:
```javascript
const val = nota === '' || nota === null ? null : parseFloat(nota)
// ❌ No valida rango 0-10
```

**Fix**:
```javascript
function validateNota(nota) {
  if (nota === '' || nota === null) return null
  const num = parseFloat(nota)
  if (isNaN(num)) throw new Error('Nota debe ser un número')
  if (num < 0 || num > 10) throw new Error('Nota debe estar entre 0-10')
  return num
}
```

---

### SEC-009: Race condition en saveAlumno
**Archivo**: `renderer/js/modules/alumnos.js` línea 39-45  
**Severidad**: 🟡 IMPORTANTE

**Código vulnerable**:
```javascript
clearTimeout(_updateTimers[id+field])
_updateTimers[id+field] = setTimeout(async () => {
  const a = _alumnos.find(x => x.id === id)
  if (!a) return
  a[field] = field === 'num' ? (parseInt(val)||null) : val  // ⚠️ Modifica estado
  await window.api.saveAlumno(a)
}, 400)
```

**Problema**: Si hay múltiples cambios rápidos, pueden guardar estados inconsistentes.

**Fix**:
```javascript
// Usar un Map de cambios pending
const _pendingChanges = new Map()

function updateAlumno(id, field, val) {
  const key = `${id}:${field}`
  
  clearTimeout(_pendingChanges.get(key)?.timeout)
  
  _pendingChanges.set(key, {
    id, field, val,
    timeout: setTimeout(async () => {
      const a = _alumnos.find(x => x.id === id)
      if (!a) return
      
      a[field] = field === 'num' ? (parseInt(val)||null) : val
      try {
        await window.api.saveAlumno(a)
      } catch (err) {
        console.error('Error saving alumno:', err)
        // Revertir cambio
        location.reload()
      } finally {
        _pendingChanges.delete(key)
      }
    }, 400)
  })
}
```

---

### SEC-010: Spawn sin sanitizar argumentos
**Archivo**: `main.js` línea 63  
**Severidad**: 🟡 IMPORTANTE

**Código vulnerable**:
```javascript
const proc = spawn(python(), [path.join(sd, scriptName), ...args], { cwd: sd, env })
```

**Problema**: Los argumentos `args` vienen directamente del renderer sin sanitizar.

**Fix**:
```javascript
function sanitizeArg(arg) {
  if (typeof arg !== 'string') throw new Error('Argumento debe ser string')
  if (arg.length > 10000) throw new Error('Argumento muy largo')
  // Whitelist de caracteres seguros
  if (!arg.match(/^[a-zA-Z0-9\-_.,\s]*$/)) {
    throw new Error('Argumento contiene caracteres peligrosos')
  }
  return arg
}

ipcMain.on('gen-ia', (event, { comando, modulo, ra, n, alumno, notas, proveedor }) => {
  // Validar todos los argumentos
  [comando, modulo, ra, n, alumno, notas, proveedor].forEach(arg => {
    if (arg !== null && arg !== undefined) sanitizeArg(String(arg))
  })
  
  // ... resto del código
})
```

---

### SEC-011: Sin límite en campos de configuración
**Archivo**: `renderer/js/modules/ajustes.js`  
**Severidad**: 🟡 IMPORTANTE

**Problema**:
```javascript
await window.api.setConfig(k, document.getElementById(id).value)
// ❌ Sin límite de tamaño
```

**Fix**:
```javascript
async function saveAjustes() {
  const keys = { 
    openaiKey:'cfg-openai', 
    anthropicKey:'cfg-anthropic', 
    proveedor:'cfg-prov' 
  }
  
  for (const [k, id] of Object.entries(keys)) {
    const value = document.getElementById(id).value
    
    // Validar
    if (value && value.length > 10000) {
      alert('Valor demasiado largo para ' + k)
      return
    }
    
    await window.api.setConfig(k, value)
  }
  
  // Mostrar confirmación
  const st = document.getElementById('ajustes-ok')
  st.textContent = '✅ Guardado'
  setTimeout(() => st.textContent = '', 2500)
}
```

---

### SEC-012: No hay validación de nombre de archivo PDF
**Archivo**: `main.js` línea 157  
**Severidad**: 🟡 IMPORTANTE

**Código vulnerable**:
```javascript
const filename = `boletin_${alumnoNombre.replace(/[^a-zA-Z0-9]/g,'_')}_${Date.now()}.pdf`
```

**Problema**: `alumnoNombre` viene del usuario sin validar longitud.

**Fix**:
```javascript
const filename = `boletin_${alumnoNombre
  .slice(0, 50)  // Limitar
  .replace(/[^a-zA-Z0-9]/g,'_')}_${Date.now()}.pdf`
```

---

## 🟢 MENORES (Próximo mes)

### MNT-001: Módulo programacion.js muy grande
**Archivo**: `renderer/js/modules/programacion.js`  
**Líneas**: 729  
**Recomendación**: Refactorizar en 4 módulos

```
programacion.js (729) →
  ├─ ut-section.js (200)
  ├─ ra-section.js (200) 
  ├─ ce-section.js (150)
  └─ programacion-main.js (180)
```

---

### MNT-002: Variables globales contaminan window
**Archivo**: `renderer/js/app.js` línea 95-111  
**Problema**: 40+ funciones expuestas al window

**Fix**:
```javascript
// Crear namespace
window.EvalFP = {
  go, goSection, initModSelect,
  renderModulos, selectMod, // ... etc
}

// Actualizar HTML: onclick="EvalFP.go(this)"
```

---

### MNT-003: Sin ESLint
**Recomendación**: Agregar eslint

```bash
npm install --save-dev eslint eslint-config-airbnb-base
npx eslint . --fix
```

---

### MNT-004: Sin Prettier
**Recomendación**: Agregar formater

```bash
npm install --save-dev prettier
npx prettier . --write
```

---

### MNT-005: Sin pre-commit hooks
**Recomendación**: Agregar husky

```bash
npm install --save-dev husky
npx husky install
```

---

### MNT-006: Sin CONTRIBUTING.md
**Recomendación**: Crear documento

---

### MNT-007: Sin LICENSE file
**Recomendación**: Agregar LICENSE

---

### MNT-008: Comments en inglés para mejor colaboración
**Recomendación**: Traducir/bilingüe JSDoc

---

### MNT-009: Sin archivo .env.example
**Recomendación**: Documentar variables necesarias

---

### MNT-010: Sin package.json scripts más complejos
**Recomendación**: Agregar scripts útiles

```json
{
  "scripts": {
    "dev": "electron .",
    "build": "npm run build:mac && npm run build:win",
    "build:mac": "electron-builder --mac",
    "build:win": "electron-builder --win",
    "test": "vitest",
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

---

### QA-001: Sin tests unitarios para db.js
**Recomendación**: Agregar tests

```javascript
// tests/unit/db.test.js
import { describe, it, expect } from 'vitest'
import * as db from '../../db'

describe('Database', () => {
  it('should create modulo', () => {
    const id = db.addModulo({...})
    expect(id).toBeGreaterThan(0)
  })
})
```

---

### QA-002: Sin tests E2E
**Recomendación**: Agregar Playwright

---

### QA-003: Sin validación de campos de formulario en tiempo real
**Recomendación**: Agregar validación mientras se escribe

---

### QA-004: UI muy oscura (accesibilidad)
**Recomendación**: Revisar contraste (WCAG AA)

---

### QA-005: Sin modo claro/oscuro explícito
**Recomendación**: Agregar toggle de tema

---

### UX-001: Sin confirmación antes de eliminar módulo
**Archivo**: `renderer/js/modules/modulos.js`  
**Recomendación**: Agregar modal de confirmación

```javascript
async function delModulo(id) {
  if (!confirm('¿Estás seguro? Se eliminarán TODOS los datos de este módulo.')) return
  await window.api.deleteModulo(id)
  // ...
}
```

---

### UX-002: Sin indicador de carga
**Recomendación**: Mostrar spinner cuando se cargan datos

---

## 📊 Resumen de Issues

| Severidad | Count | Ejemplos |
|-----------|-------|----------|
| 🔴 Crítico | 4 | XSS, API Keys, Backups, Errores |
| 🟡 Importante | 8 | Validación, Logging, Race conditions |
| 🟢 Menor | 16 | Refactoring, Testing, Docs |

---

## 🎯 Plan de Ejecución

### Semana 1
- [ ] SEC-001: Fix XSS en modulos.js
- [ ] SEC-002: Fix XSS en programacion.js  
- [ ] SEC-003: Encriptar claves API
- [ ] SEC-004: Implementar backups

### Semana 2
- [ ] SEC-005 a SEC-012: Issues importantes
- [ ] MNT-001: Refactorizar programacion.js
- [ ] Agregar ESLint + Prettier

### Semana 3-4
- [ ] Tests unitarios
- [ ] Documentación
- [ ] Security review final

---

**Última actualización**: 1 de julio de 2026

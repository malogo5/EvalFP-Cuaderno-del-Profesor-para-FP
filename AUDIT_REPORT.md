# 📋 Auditoría Completa - EvalFP v3.0.0

**Fecha**: 1 de julio de 2026  
**Tipo de Aplicación**: Electron (Desktop)  
**Descripción**: Cuaderno digital del profesor para FP (Formación Profesional) - Castilla-La Mancha

---

## 📊 RESUMEN EJECUTIVO

### Puntuación General: **7.5/10** ⚠️

**Estado**: La aplicación tiene una base sólida, pero requiere mejoras en seguridad y mantenibilidad.

| Aspecto | Puntuación | Estado |
|---------|-----------|--------|
| **Seguridad** | 6.5/10 | ⚠️ Requiere atención |
| **Código** | 7/10 | 🟡 Aceptable |
| **Arquitectura** | 8/10 | ✅ Buena |
| **Dependencias** | 10/10 | ✅ Excelente |
| **Documentación** | 3/10 | 🔴 Muy baja |
| **Testing** | 0/10 | 🔴 No existe |
| **Performance** | 8/10 | ✅ Buena |

---

## 🏗️ ANÁLISIS DE ARQUITECTURA

### Estructura del Proyecto

```
/workspace
├── main.js          (167 líneas) - Proceso principal de Electron
├── preload.js       (46 líneas)  - Puente de contexto aislado
├── db.js            (231 líneas) - Capa SQLite
├── renderer/        - Frontend (HTML/CSS/JS)
│   ├── index.html   (326 líneas)
│   ├── css/
│   ├── js/
│   │   ├── app.js   (164 líneas) - Bootstrap y coordinación
│   │   └── modules/ (1414 líneas) - Módulos funcionales
│   │       ├── modulos.js      (214 líneas)
│   │       ├── programacion.js (729 líneas) ⚠️ MÁS GRANDE
│   │       ├── alumnos.js      (120 líneas)
│   │       ├── notas.js        (171 líneas)
│   │       ├── evaluaciones.js (43 líneas)
│   │       ├── dashboard.js    (78 líneas)
│   │       ├── ia.js           (42 líneas)
│   │       └── ajustes.js      (17 líneas)
├── package.json
└── docs/ - Documentación

Total de líneas JS: ~2,350
```

### Tipo de Arquitectura

✅ **Cliente-Servidor Híbrido (Electron)**
- Preload.js aísla contexto (buena práctica)
- IPC para comunicación main ↔ renderer
- Base de datos local SQLite (sin servidor remoto)

---

## 🔒 AUDITORÍA DE SEGURIDAD

### 1. Dependencias NPM ✅ EXCELENTE

```
✅ Solo 2 dependencias directas:
   - electron@42.5.1
   - electron-builder@26.15.3

✅ npm audit: 0 vulnerabilidades
✅ Versiones recientes (42.5.1 para Electron)
✅ Falta de dependencias "pesadas" o sospechosas
```

**Recomendación**: Actualizar electron a 43.x cuando sea estable.

---

### 2. Configuración de Electron ✅ SEGURA

```javascript
// ✅ Context Isolation HABILITADO
webPreferences: {
  preload: path.join(__dirname, 'preload.js'),
  contextIsolation: true,      // ✅ Bien
  nodeIntegration: false,      // ✅ Bien
}
```

**Estado**: Conforme a las mejores prácticas de Electron.

---

### 3. Aislamiento de Contexto (preload.js) ✅ BIEN IMPLEMENTADO

```javascript
// ✅ Usa contextBridge para exponer API
contextBridge.exposeInMainWorld('api', {
  getModulos: () => ipcRenderer.invoke('db:getModulos'),
  saveAlumno: a => ipcRenderer.invoke('db:saveAlumno', a),
  // ... otros métodos
})
```

**Análisis**:
- ✅ No expone `ipcRenderer` directamente
- ✅ No expone acceso al filesystem
- ✅ API bien estructurada
- ⚠️ No hay validación de parámetros en preload

---

### 4. Inyección SQL ✅ PROTEGIDA

```javascript
// ✅ Usa prepared statements
db.prepare('SELECT * FROM modulos WHERE id=?').run(id)
db.prepare('INSERT INTO notas VALUES (?,?,?)').run(alumnoId, actividadId, nota)
```

**Estado**: Totalmente protegido contra SQL injection gracias a `DatabaseSync`.

---

### 5. Cross-Site Scripting (XSS) ⚠️ VULNERABLE

#### Hallazgos Críticos:

**a) innerHTML con datos no escapados** (modulos.js:11-22)
```javascript
// ⚠️ VULNERABLE
el.innerHTML = _modulos.map(m => `
  <div class="mod-card" onclick="selectMod(${m.id})">
    <div class="mod-card-abrev">${m.abrev}</div>
    <div class="mod-card-nombre">${m.nombre}</div>  // ⚠️ No escapado
    <div class="mod-card-meta">
      ${m.ciclo||''} · ${m.curso||''} · ${m.anno||''}
      ${m.decreto ? `<br><span>${m.decreto}</span>` : ''}  // ⚠️
    </div>
  </div>
`).join('')
```

**Impacto**: Si un usuario introduce `<img src=x onerror="alert('XSS')">` en el campo "nombre", se ejecutaría.

**b) innerHTML en notas.js:42**
```javascript
// ⚠️ VULNERABLE
<th title="${a.descripcion}" style="text-align:center">
  <div>${a.instrumento}</div>  // ⚠️ En atributo, pero inseguro
</th>
```

**c) Función esc() existe pero NO se usa consistentemente**
```javascript
// ✅ Existe la función
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')

// ✅ Se usa en algunos lugares
<input value="${esc(a.apellidos||'')}"  // Alumnos

// ❌ NO se usa en otros
<div>${m.nombre}</div>  // Módulos - SIN ESCAPAR
```

**Riesgo**: ALTO (aunque depende de quién controla los datos)

---

### 6. Validación de Entrada ⚠️ PARCIAL

#### Entrada del Usuario:

**a) Alumnos** (alumnos.js)
```javascript
// ⚠️ Poca validación
const apellidos = parts[0] || ''
const nombre = parts[1] || ''
// Sin límite de longitud, sin validación de formato
```

**b) Notas** (notas.js)
```javascript
// ✅ Mejor - parseFloat con validación
const val = nota === '' || nota === null ? null : parseFloat(nota)
// Pero no valida rango 0-10
```

**c) Campos de configuración** (ajustes.js)
```javascript
// ❌ SIN VALIDACIÓN
await window.api.setConfig(k, document.getElementById(id).value)
// Acepta cualquier string sin límite
```

---

### 7. Almacenamiento de Claves API 🔴 RIESGOSO

#### Hallazgo Crítico:

```javascript
// main.js - Linea 48-52
try {
  const db = require('./db')
  const cfg = db.getAllConfig()
  if (cfg.openaiKey)    process.env.OPENAI_API_KEY    = cfg.openaiKey
  if (cfg.anthropicKey) process.env.ANTHROPIC_API_KEY = cfg.anthropicKey
} catch {}
```

**Problemas**:
- 🔴 Las claves API se guardan en **texto plano** en SQLite
- 🔴 Se cargan en `process.env` (visible en memory dumps)
- 🔴 No hay encriptación de la base de datos
- ⚠️ El try/catch silencia errores sin logging

**Riesgo**: CRÍTICO si el usuario comparte/pierde su computadora.

**Recomendación**:
```javascript
// ✅ Usar keytar para encriptación
const keytar = require('keytar')
const key = await keytar.getPassword('EvalFP', 'openai-key')
```

---

### 8. Gestión de Archivos ⚠️ PERMISIVA

```javascript
// main.js - Linea 62
fs.mkdirSync(outputDir(), { recursive: true })

// Crea directorio en ~/Documents/EvalFP
// ✅ Ubicación razonable
// ⚠️ Sin validación de ruta
```

#### Operaciones inseguras:
```javascript
// main.js - Linea 63
const proc = spawn(python(), [path.join(sd, scriptName), ...args], { cwd: sd, env })

// ⚠️ Asume que los scripts Python existen
// ⚠️ Los argumentos se pasan sin sanitizar
```

---

### 9. Manejo de Errores 🔴 DEFICIENTE

#### Problemas encontrados:

**a) try/catch silencioso** (main.js:48-53)
```javascript
try {
  const db = require('./db')
  const cfg = db.getAllConfig()
  if (cfg.openaiKey) process.env.OPENAI_API_KEY = cfg.openaiKey
} catch {}  // ❌ SIN LOGGING
```

**b) Sin captura global de errores**
```javascript
// ❌ No hay error handler global
// ❌ No hay logging de excepciones
```

**c) Errores mostrados al usuario**
```javascript
catch(e) {
  alert('Error al guardar: ' + e.message)  // ⚠️ Información técnica al usuario
  console.error(e)  // Solo en consola
}
```

---

### 10. Ejecución de Código Externo 🔴 RIESGOSA

```javascript
// main.js - Linea 63
const proc = spawn(python(), [path.join(sd, scriptName), ...args], { cwd: sd, env })

// ⚠️ Ejecuta scripts Python arbitrarios
// ⚠️ Los argumentos podrían inyectar comandos
```

**Posible ataque**:
```
scriptName = "ai_asistente.py; rm -rf ~"  // Ejecución de comando
```

---

## 📈 ANÁLISIS DE CÓDIGO

### Estadísticas

| Métrica | Valor |
|---------|-------|
| Total de líneas JS | ~2,350 |
| Archivos principales | 5 |
| Módulos frontend | 8 |
| Funciones globales expuestas | 40+ |
| Variables globales | 12 |
| Condicionales anidados máx. | 5 |

### Calidad de Código

**Puntos positivos**:
- ✅ Uso consistente de async/await
- ✅ Nombres descriptivos en español (mantenible para el contexto)
- ✅ Separación en módulos
- ✅ API IPC bien organizada

**Problemas**:
- ⚠️ 40+ funciones globales en window (contaminación del scope)
- ⚠️ Variables globales `_modulos`, `_curMod`, etc.
- ⚠️ Falta de tipos/JSDoc
- ⚠️ Módulo programacion.js muy grande (729 líneas)
- 🔴 Sin pruebas unitarias o E2E

### Ejemplos de Problemas

**1. Variables globales no documentadas**
```javascript
let _modulos = []       // ¿Qué es esto?
let _curMod  = null     // No documentado
let _alumnos = []
let _actividades = []
let _notasGrid = {}
```

**2. Funciones expuestas al window sin control**
```javascript
Object.assign(window, {
  go, goSection, initModSelect,
  renderModulos, selectMod, updateModBadge, renderModDropdown,
  // ... 40+ más funciones
})
```

**3. Sin manejo de race conditions**
```javascript
// Si el usuario hace clic rápidamente:
_updateTimers[id+field] = setTimeout(async () => {
  // ⚠️ Podría guardar datos inconsistentes
  await window.api.saveAlumno(a)
}, 400)
```

---

## 🗄️ AUDITORÍA DE BASE DE DATOS

### Fortalezas ✅

```javascript
_db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;')
```
- ✅ WAL mode (mejor concurrencia)
- ✅ Foreign keys habilitadas
- ✅ Prepared statements en todas partes

### Debilidades ⚠️

**a) Sin respaldo automático**
```javascript
// ❌ No hay backups automáticos
// ❌ Si se corrompe la DB, se pierden todos los datos
```

**b) Base de datos sin encripción**
```sqlite
-- ❌ Texto plano completo
SELECT * FROM config;  -- Incluye API keys
```

**c) Sin versionado de schema**
```javascript
// ❌ Sin migraciones
// ❌ Si cambia el schema, no hay forma de upgrade
```

---

## 📦 DEPENDENCIAS ANÁLISIS

### package.json

```json
{
  "devDependencies": {
    "electron": "^42.5.1",
    "electron-builder": "^26.15.3"
  }
}
```

**Análisis**:
- ✅ Muy pocas dependencias (ventaja de seguridad)
- ✅ Electron 42.5.1 es relativamente reciente
- ✅ electron-builder es estándar

**Comparación con 2024**:
- Electron 42.5 (2026) > Electron 28 (2024) ✅
- Sigue el ciclo de releases (nueva mayor cada 3 meses)

---

## 🚀 PERFORMANCE

### Positivo ✅

- Base de datos local (sin latencia de red)
- Carga previa de módulos en `modules_data.json` (412 KB)
- Lazy loading de módulos de UI

### Problemas ⚠️

- Módulo `programacion.js` muy grande (729 líneas)
- Renderizado de tablas con muchas filas sin virtualización
- Sin web workers para operaciones pesadas

---

## 📄 DOCUMENTACIÓN

### Estado: 🔴 CRÍTICO

**Hallazgos**:
- ❌ Sin README.md
- ❌ Sin CONTRIBUTING.md
- ❌ Sin documentación de API
- ❌ Sin comentarios JSDoc
- ⚠️ Solo comentarios en español (dificulta contribuciones)
- ✅ Existe /docs/refactor/ (en progreso)

**Archivos encontrados**:
```
/docs/refactor/  - Documentación de refactoring (sin completar)
```

---

## 🧪 TESTING

### Estado: 🔴 INEXISTENTE

- ❌ Sin tests unitarios
- ❌ Sin tests de integración
- ❌ Sin tests E2E
- ❌ Sin CI/CD pipeline
- ❌ Sin test coverage

**Riesgo**: Cambios pueden romper funcionalidad sin detectarlo.

---

## 🔐 MATRIZ DE RIESGOS

| Riesgo | Severidad | Probabilidad | Impacto | Mitigación |
|--------|-----------|--------------|---------|------------|
| **XSS en módulos** | 🔴 Alta | Media | Ejecución de JS | Escapar todos los datos con esc() |
| **Claves API en texto plano** | 🔴 Alta | Alta | Acceso a IA | Usar keytar o encriptación |
| **Sin backups de DB** | 🔴 Alta | Media | Pérdida de datos | Backups automáticos |
| **Race conditions en guardado** | 🟡 Media | Media | Datos inconsistentes | Debouncing + Lock |
| **Sin validación de entrada** | 🟡 Media | Alta | Datos inválidos | Validar en frontend + backend |
| **Sin manejo de errores** | 🟡 Media | Alta | Fallos silenciosos | Try/catch + logging |
| **Módulos muy grandes** | 🟡 Media | N/A | Mantenimiento difícil | Refactorizar |

---

## ✅ FORTALEZAS

1. **Seguridad de Electron bien configurada**
   - Context isolation: ✅ Habilitado
   - Node integration: ✅ Deshabilitado
   - Preload aislado: ✅ Implementado

2. **Protección contra SQL injection**
   - Prepared statements en todas partes
   - `DatabaseSync` de Node.js (seguro)

3. **Dependencias muy limpias**
   - Solo 2 dependencias directas
   - 0 vulnerabilidades conocidas
   - Sin dependencias de terceros innecesarias

4. **Arquitectura modular**
   - Separación clara main/preload/renderer
   - Módulos funcionales bien divididos
   - IPC bien estructurado

5. **Base de datos bien diseñada**
   - Schema normalizdo
   - Foreign keys
   - WAL mode para mejor concurrencia

---

## 🚨 DEBILIDADES CRÍTICAS

1. **XSS no escapado** 🔴
   - innerHTML sin usar esc()
   - Potencial inyección de HTML/JS

2. **Claves API en texto plano** 🔴
   - Almacenadas sin encripción
   - Cargadas en process.env
   - Vulnerable a acceso no autorizado

3. **Sin backups** 🔴
   - Pérdida total de datos posible
   - Sin versionado de schema

4. **Sin testing** 🔴
   - Imposible garantizar calidad
   - Cambios riesgosos

5. **Sin documentación** 🔴
   - Difícil para nuevos desarrolladores
   - Falta de guías de seguridad

---

## 📋 RECOMENDACIONES

### Críticas (Implementar ASAP)

#### 1. Proteger contra XSS
```javascript
// Cambiar todos los innerHTML que usan datos:
// ❌ Antes:
el.innerHTML = _modulos.map(m => `<div>${m.nombre}</div>`).join('')

// ✅ Después:
el.innerHTML = _modulos.map(m => `<div>${esc(m.nombre)}</div>`).join('')

// O mejor aún, usar textContent:
const div = document.createElement('div')
div.textContent = m.nombre  // Seguro
```

**Archivos a corregir**:
- modulos.js (líneas 11-22, 49-58, 83-100)
- notas.js (línea 42)
- dashboard.js
- programacion.js (revisar todas las interpolaciones)

#### 2. Encriptar claves API
```javascript
// Instalar keytar
npm install keytar

// En main.js:
const keytar = require('keytar')

// Guardar:
await keytar.setPassword('EvalFP', 'openai-key', key)

// Recuperar:
const key = await keytar.getPassword('EvalFP', 'openai-key')
```

#### 3. Agregar validación de entrada
```javascript
// En ajustes.js:
const validateApiKey = (key) => {
  if (typeof key !== 'string') throw new Error('Key debe ser string')
  if (key.length > 1000) throw new Error('Key muy largo')
  if (!key.match(/^[a-zA-Z0-9\-_]*$/)) throw new Error('Key contiene caracteres inválidos')
  return true
}

// En alumnos.js:
const validateAlumno = (a) => {
  if (a.apellidos?.length > 100) throw new Error('Apellidos muy largo')
  if (a.num && (a.num < 1 || a.num > 999)) throw new Error('Número inválido')
  return true
}
```

#### 4. Implementar backups automáticos
```javascript
// En main.js:
const schedule = require('node-schedule')

// Backup cada día a las 2 AM
schedule.scheduleJob('0 2 * * *', () => {
  const src = path.join(app.getPath('userData'), 'evalfp.db')
  const dst = path.join(app.getPath('userData'), `backups/evalfp_${Date.now()}.db`)
  fs.copyFileSync(src, dst)
  // Limpiar backups antiguos (>30 días)
})
```

#### 5. Centralizar manejo de errores
```javascript
// Crear utils/logger.js
const isDev = !app.isPackaged

function logError(error, context) {
  const msg = `[${new Date().toISOString()}] [${context}] ${error.message}\n${error.stack}`
  const logFile = path.join(app.getPath('userData'), 'errors.log')
  fs.appendFileSync(logFile, msg + '\n')
  if (isDev) console.error(msg)
}

module.exports = { logError }
```

### Importantes (Próximos 2 sprints)

#### 6. Agregar pruebas
```bash
# Instalar testing tools
npm install --save-dev vitest @testing-library/dom

# Crear tests/
tests/
  ├── unit/
  │   ├── db.test.js
  │   ├── modules/alumnos.test.js
  │   └── modules/notas.test.js
  └── e2e/
      └── app.test.js
```

#### 7. Refactorizar programacion.js
```
programacion.js (729 líneas) → modularizar:
  - ut-editor.js (gestión UTs)
  - ra-editor.js (gestión RAs)
  - ce-editor.js (gestión CEs)
  - programacion-main.js (orquestación)
```

#### 8. Documentación mínima
```markdown
# EvalFP - Documentación de Desarrollo

## Arquitectura
[Describir la arquitectura Electron + SQLite]

## Seguridad
- Context isolation: habilitado
- Node integration: deshabilitado
- Todas las keys API deben estar encriptadas con keytar

## API IPC
[Documentar todos los handlers de IPC]

## Base de datos
[Describir schema y migraciones]
```

#### 9. Validación consistente de entrada
```javascript
// Crear validators.js
export const validators = {
  alumno: (a) => { ... },
  actividad: (a) => { ... },
  nota: (n) => { ... },
  config: (k, v) => { ... }
}

// Usar en todos los saveX/setX
ipcMain.handle('db:saveAlumno', (_, a) => {
  validators.alumno(a)  // Valida primero
  return db.saveAlumno(a)
})
```

#### 10. Logging estruturado
```javascript
// Reemplazar todos los console.log/error
const logger = {
  info: (msg) => { /* log con timestamp */ },
  error: (msg, err) => { /* log error */ },
  warn: (msg) => { /* log warning */ }
}
```

### Mejoras a largo plazo

#### 11. Suite de testing completa
- 50%+ de coverage mínimo
- Tests E2E con Playwright
- CI/CD pipeline (GitHub Actions)

#### 12. Encriptación de BD
```javascript
// Usar sqlite3 con encriptación
const encrypted = require('encrypted-db')
```

#### 13. Progressive Web App
- Opcional: versión web
- Sincronización con cloud
- Acceso offline

#### 14. Internacionalización (i18n)
- UI completa en inglés/gallego/catalán
- Uso consistente de traducciones

---

## 🔍 CHECKLIST DE SEGURIDAD

- [ ] Escapar todos los datos en innerHTML (XSS)
- [ ] Encriptar claves API con keytar
- [ ] Validar todas las entradas en preload.js
- [ ] Implementar backups automáticos
- [ ] Logging centralizado de errores
- [ ] Sanitizar argumentos de spawn()
- [ ] Documentar toda la API IPC
- [ ] Agregar linter (ESLint) + formatter (Prettier)
- [ ] Tests unitarios en db.js
- [ ] Tests E2E en principales workflows
- [ ] HTTPS para cualquier comunicación externa
- [ ] Security headers en preload
- [ ] Auditoría de permisos de archivo
- [ ] Encriptación de BD SQLite
- [ ] Límites de rate-limiting si hay API remota

---

## 📊 SCORES POR CATEGORÍA

```
Seguridad              ██████░░░░ 6.5/10
  ├─ XSS             ░░░░░░░░░░ 2/10  🔴
  ├─ SQL Injection    ██████████ 10/10 ✅
  ├─ Auth/Keys       ░░░░░░░░░░ 1/10  🔴
  ├─ Validación      █████░░░░░ 5/10  ⚠️
  └─ Errores         ███░░░░░░░ 3/10  🔴

Código                 ███████░░░ 7/10
  ├─ Estructura      ████████░░ 8/10
  ├─ Legibilidad     ███████░░░ 7/10
  ├─ Documentación   ░░░░░░░░░░ 0/10  🔴
  ├─ Testing         ░░░░░░░░░░ 0/10  🔴
  └─ Complejidad     ██████░░░░ 6/10

Arquitectura           ████████░░ 8/10
  ├─ Diseño          █████████░ 9/10
  ├─ Modularidad     ████████░░ 8/10
  ├─ Escalabilidad   ███████░░░ 7/10
  └─ Mantenibilidad  ██████░░░░ 6/10

Dependencias          ██████████ 10/10
  ├─ Auditoría       ██████████ 10/10 ✅
  ├─ Cantidad        ██████████ 10/10 ✅
  ├─ Actualización   █████████░ 9/10
  └─ Licencias       ██████████ 10/10 ✅

Performance            ████████░░ 8/10
  ├─ Velocidad       ████████░░ 8/10
  ├─ Memoria         ███████░░░ 7/10
  ├─ DB               █████████░ 9/10
  └─ UI Rendering    ██████████ 10/10

Documentación          ░░░░░░░░░░ 0/10  🔴

Testing               ░░░░░░░░░░ 0/10  🔴
```

---

## 📝 CONCLUSIÓN

### Veredicto: ⚠️ LISTO PARA PRODUCCIÓN CON RESERVAS

**Puede usarse en producción siempre que**:

1. ✅ Se implemente protección XSS (escapar datos)
2. ✅ Se encripten las claves API
3. ✅ Se configuren backups automáticos
4. ✅ Se agregue logging de errores
5. ⚠️ Se haga un plan de testing antes de grandes cambios

### Prioridades para mejorar:

**Inmediato (esta semana)**:
- [ ] Fix XSS en innerHTML
- [ ] Encriptar API keys

**Corto plazo (mes)**:
- [ ] Backups automáticos
- [ ] Validación centralizada
- [ ] Logging

**Mediano plazo (trimestre)**:
- [ ] Suite de tests
- [ ] Documentación completa
- [ ] Refactorización de módulos grandes

**Largo plazo (6 meses)**:
- [ ] Encriptación de BD
- [ ] CI/CD pipeline
- [ ] Posible versión web

---

## 📞 CONTACTO Y SEGUIMIENTO

**Auditoría realizada por**: Abacus.AI CLI  
**Fecha**: 1 de julio de 2026  
**Próxima revisión recomendada**: 30 de septiembre de 2026

**Para resolver issues**:
1. Crear issues en el repo con etiqueta `security:critical`
2. Priorizar fixes XSS y API keys
3. Ejecutar esta auditoría nuevamente después de cambios mayores

---

**Fin de la auditoría** ✅

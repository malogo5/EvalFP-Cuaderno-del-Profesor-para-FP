# 📝 SEC-004: CENTRALIZED LOGGING - IMPLEMENTATION GUIDE

**Categoría**: Important (Auditing & Debugging)  
**Tiempo estimado**: 2 horas  
**Archivos afectados**: 3+  
**Problema**: No hay logging centralizado - errores dispersos en consola

---

## 📋 ANÁLISIS DEL PROBLEMA

### ¿Por qué es importante?

Actualmente, los errores y eventos se registran de forma inconsistente:

```javascript
// Problema 1: console.log sin estructura
console.log('✓ API keys loaded from secure storage')

// Problema 2: Sin contexto de tiempo o nivel
console.error('Error en backup automático:', e.message)

// Problema 3: Sin persistencia - se pierden después
console.warn('⚠ Error initializing backups:', e.message)

// Problema 4: Imposible filtrar por tipo/módulo
catch(e) { console.warn('Error:', e) }
```

**Riesgos**:
1. ❌ Sin auditoría de eventos importantes
2. ❌ Difícil de debuggear problemas en producción
3. ❌ Sin trazabilidad de acciones del usuario
4. ❌ Sin alertas para errores críticos

### Solución: winston logger

`winston` es el estándar para Node.js logging:
- **Niveles**: error, warn, info, debug, verbose, silly
- **Transports**: archivo + consola + simultáneo
- **Estructura**: JSON con timestamp, nivel, módulo, mensaje
- **Rotación**: Archivos por día para fácil auditoría

```javascript
const logger = require('./logger')

logger.info('App started', { module: 'main', version: '3.0.0' })
logger.error('Database error', { code: 'DB001', stack: e.stack })
logger.warn('API key not found', { service: 'openai' })
```

---

## 🔍 ARCHIVOS A CREAR/ACTUALIZAR

### Archivo 1: package.json
**Ubicación**: `/workspace/package.json`

**Cambio**: Agregar dependencia winston

```json
"dependencies": {
  "keytar": "^7.9.0",
  "node-schedule": "^2.1.1",
  "winston": "^3.11.0"
}
```

**Comando**:
```bash
npm install winston
```

---

### Archivo 2: main/logger.js (NUEVO)
**Ubicación**: `/workspace/main/logger.js`

Este archivo centraliza toda la configuración de logging.

**Contenido**:
```javascript
'use strict'
const winston = require('winston')
const path = require('path')
const os = require('os')

// Directorio para logs (misma ubicación que backups)
const logsDir = path.join(os.homedir(), 'Documents', 'EvalFP', 'logs')

// Crear directorio si no existe
const fs = require('fs')
fs.mkdirSync(logsDir, { recursive: true })

// Formato personalizado
const customFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
)

// Logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: customFormat,
  defaultMeta: { service: 'EvalFP' },
  transports: [
    // Error file (solo errores)
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 7, // 7 días
    }),
    // Combined file (todo)
    new winston.transports.File({
      filename: path.join(logsDir, 'combined.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 30, // 30 días
    }),
  ],
})

// Agregar consola en desarrollo
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.printf(({ level, message, timestamp, ...meta }) => {
        const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : ''
        return `${timestamp} [${level}]: ${message} ${metaStr}`
      })
    ),
  }))
}

// Métodos de conveniencia
logger.logError = (message, error = {}) => {
  logger.error(message, {
    errorMessage: error.message,
    errorStack: error.stack,
    ...error,
  })
}

logger.logEvent = (event, data = {}) => {
  logger.info(`EVENT: ${event}`, { event, ...data })
}

module.exports = logger
```

---

### Archivo 3: main.js
**Ubicación**: `/workspace/main.js`

**Cambio 1: Importar logger (línea 1 o después de otros requires)**
```javascript
const logger = require('./main/logger')
```

**Cambio 2: Reemplazar todos los console.log/warn/error**

Ejemplos de cambios:

```javascript
// ANTES
console.log('✓ API keys loaded from secure storage')
// DESPUÉS
logger.info('API keys loaded from secure storage')

// ANTES
console.warn('⚠ Error loading API keys from keytar:', e.message)
// DESPUÉS
logger.logError('Failed to load API keys from keytar', e)

// ANTES
console.log('✓ Automatic backups initialized (daily at 2 AM)')
// DESPUÉS
logger.info('Automatic backups initialized', { schedule: 'daily at 2 AM' })

// ANTES
console.error('❌ Error en backup automático:', e.message)
// DESPUÉS
logger.logError('Automatic backup failed', e)

// ANTES
console.log('✓ Backup created: evalfp_2026-07-01T02-00-00.db')
// DESPUÉS
logger.info('Backup created', { filename: 'evalfp_2026-07-01T02-00-00.db' })

// ANTES
console.log('💾 Backup final antes de cerrar...')
// DESPUÉS
logger.logEvent('GRACEFUL_SHUTDOWN', { message: 'Final backup before closing' })

// ANTES
console.log('✓ API keys saved securely')
// DESPUÉS
logger.info('API keys saved securely')
```

---

### Archivo 4: db.js
**Ubicación**: `/workspace/db.js`

**Cambio**: Agregar logger al inicio y usar en operaciones críticas

```javascript
// Agregar al inicio
const logger = require('./main/logger')

// En try-catch blocks:
logger.logEvent('DATABASE_OPERATION', { operation: 'getAlumnos', moduleId })
```

---

### Archivo 5: preload.js
**Ubicación**: `/workspace/preload.js`

**Cambio**: Agregar logging para IPC calls

```javascript
// Agregar un middleware que log cada IPC call
const originalInvoke = ipcRenderer.invoke
ipcRenderer.invoke = async (channel, ...args) => {
  const logger = require('../main/logger')
  try {
    logger.debug(`IPC invoke: ${channel}`)
    return await originalInvoke(channel, ...args)
  } catch (e) {
    logger.logError(`IPC error on ${channel}`, e)
    throw e
  }
}
```

---

## 📊 NIVELES DE LOG

| Nivel | Cuándo usar | Ejemplo |
|-------|-------------|---------|
| `error` | Fallo que requiere atención | DB corrupted, key load failed |
| `warn` | Situación inesperada pero recuperable | API key not found, retry attempt |
| `info` | Eventos importantes | App started, backup created |
| `debug` | Info para debugging | Database query, file operation |
| `verbose` | Detalles muy específicos | Memory usage, performance metrics |

---

## 🗂️ ESTRUCTURA DE ARCHIVOS DE LOG

```
~/Documents/EvalFP/
├── evalfp.db
├── backups/
│   ├── evalfp_2026-07-01T02-00-00.db
│   └── evalfp_2026-06-30T02-00-00.db
└── logs/  ← NUEVO
    ├── error.log     (solo errores)
    ├── combined.log  (todo)
    ├── error.log.1   (rotación)
    └── combined.log.1
```

---

## 🧪 TESTING MANUAL

### Test 1: Crear archivo de logs
1. Abrir la aplicación
2. Verificar que existe `/Users/[user]/Documents/EvalFP/logs/`

### Test 2: Registrar evento
1. Realizar acción en app (guardar alumno)
2. Verificar en `combined.log`:
```json
{
  "level": "info",
  "message": "Alumno saved",
  "timestamp": "2026-07-01 10:30:45",
  "service": "EvalFP",
  "...": "más metadatos"
}
```

### Test 3: Registrar error
1. Hacer algo que cause error (ej: DB corrupted)
2. Verificar en `error.log`:
```json
{
  "level": "error",
  "message": "Failed to load database",
  "timestamp": "2026-07-01 10:30:50",
  "errorStack": "Error: ...\n at ...",
  "...": "más contexto"
}
```

### Test 4: Rotación de archivos
1. Mantener app abierta por varios días (o simular)
2. Verificar que se crean `combined.log.1`, `combined.log.2`, etc.

---

## 📋 UBICACIONES CLAVE PARA LOGGING

Buscar en estos archivos y agregar logger:

```bash
grep -r "console\\.log\|console\\.error\|console\\.warn" /workspace \
  --include="*.js" | grep -v node_modules | head -20
```

Archivos prioritarios:
1. ✅ main.js (ya tiene muchos console.log)
2. db.js (operaciones de BD)
3. renderer/js/modules/*.js (errores de UI)
4. scripts/Python (Python → log en Node)

---

## 💾 COMMIT

```bash
git add package.json main.js main/logger.js db.js preload.js
git commit -m "feat: add centralized winston logger (SEC-004)

- Created main/logger.js with winston configuration
- Logs stored in ~/Documents/EvalFP/logs/ with rotation
- Error logs and combined logs separate
- Support for error, warn, info, debug levels
- main.js: Replace all console.log with logger calls
- db.js: Add logging for database operations
- preload.js: Log IPC calls
- package.json: Add winston dependency

Provides auditability and debugging capabilities
Enables production issue tracking and analysis

```

---

## ✅ DEFINICIÓN DE COMPLETADO

- [ ] winston instalado en package.json
- [ ] main/logger.js creado con configuración
- [ ] Logs almacenados en ~/Documents/EvalFP/logs/
- [ ] main.js: reemplazados todos los console.* con logger
- [ ] db.js: logging en operaciones críticas
- [ ] preload.js: logging de IPC calls (opcional pero recomendado)
- [ ] Tested: archivos de log se crean
- [ ] Tested: errores se registran en error.log
- [ ] Tested: eventos normales en combined.log
- [ ] Tested: rotación de archivos funciona
- [ ] Commit en repo

---

## 🔗 REFERENCIAS

- **Librería**: https://github.com/winstonjs/winston
- **Rotación**: https://github.com/winstonjs/winston-daily-rotate-file
- **Documentación**: https://github.com/winstonjs/winston#table-of-contents

---

**Tiempo estimado**: 2 horas  
**Dificultad**: ⭐⭐⭐ Medio  
**Riesgo**: Bajo (mejora existente sin cambiar lógica)

¿Listo para implementar? 🎯

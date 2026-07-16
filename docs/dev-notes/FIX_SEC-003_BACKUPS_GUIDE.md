# 💾 SEC-003: AUTOMATIC BACKUPS - IMPLEMENTATION GUIDE

**Categoría**: Important (Security & Data Protection)  
**Tiempo estimado**: 1 hora  
**Archivos afectados**: 2  
**Problema**: No hay backups automáticos de la BD

---

## 📋 ANÁLISIS DEL PROBLEMA

### ¿Por qué es un riesgo?

Actualmente, la base de datos SQLite (`evalfp.db`) se almacena en el directorio del usuario sin ningún respaldo automático:

```javascript
// Vulnerable: Sin backups
const outputDir = () => path.join(os.homedir(), 'Documents', 'EvalFP')
```

**Riesgos**:
1. ❌ Pérdida de datos si el archivo se corrompe
2. ❌ Sin recuperación ante eliminación accidental
3. ❌ Sin histórico de cambios para auditoría
4. ❌ Sin protección ante fallos del sistema

### Solución: node-schedule + node-schedule backup

`node-schedule` permite ejecutar tareas programadas:
- **Backups diarios a las 2 AM** (cuando la app probablemente está cerrada)
- **Limpieza automática** de backups más antiguos que 30 días
- **Rotación de backups** (mantener últimos 10)

```javascript
const schedule = require('node-schedule')

// Ejecutar backup diariamente a las 2 AM
schedule.scheduleJob('0 2 * * *', () => {
  backupDatabase()
})
```

---

## 🔍 ARCHIVOS A ACTUALIZAR

### Archivo 1: package.json
**Ubicación**: `/workspace/package.json`

**Cambio**: Agregar dependencia node-schedule

**Antes**:
```json
"dependencies": {
  "keytar": "^7.9.0"
}
```

**Después**:
```json
"dependencies": {
  "keytar": "^7.9.0",
  "node-schedule": "^2.1.1"
}
```

**Comando**:
```bash
npm install node-schedule
```

---

### Archivo 2: main.js
**Ubicación**: `/workspace/main.js`

**Cambio 1: Importar node-schedule (línea 1)**
```javascript
// Después de otros requires
const schedule = require('node-schedule')
```

**Cambio 2: Agregar función setupBackups() (después de loadApiKeysFromSecureStorage)**
```javascript
// ── Automatic Database Backups ────────────────────────────────────────────────
const backupsDir = () => path.join(os.homedir(), 'Documents', 'EvalFP', 'backups')
const dbPath = () => path.join(os.homedir(), 'Documents', 'EvalFP', 'evalfp.db')

function setupBackups() {
  try {
    // Crear directorio de backups si no existe
    fs.mkdirSync(backupsDir(), { recursive: true })
    
    // Ejecutar backup diario a las 2 AM
    schedule.scheduleJob('0 2 * * *', async () => {
      console.log('📅 Ejecutando backup automático...')
      try {
        await performBackup()
        await cleanOldBackups()
      } catch (e) {
        console.error('❌ Error en backup automático:', e.message)
      }
    })
    
    // También ejecutar backup al cierre (graceful shutdown)
    process.on('SIGINT', async () => {
      console.log('💾 Backup final antes de cerrar...')
      try {
        await performBackup()
      } catch (e) {
        console.error('Error en backup final:', e.message)
      }
      process.exit(0)
    })
    
    console.log('✓ Automatic backups initialized (daily at 2 AM)')
  } catch (e) {
    console.warn('⚠ Error initializing backups:', e.message)
  }
}

async function performBackup() {
  try {
    const db = require('./db')
    const src = dbPath()
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
    const dest = path.join(backupsDir(), `evalfp_${timestamp}.db`)
    
    // Hacer copia del archivo
    fs.copyFileSync(src, dest)
    console.log(`✓ Backup created: ${path.basename(dest)}`)
    return dest
  } catch (e) {
    throw new Error(`Failed to create backup: ${e.message}`)
  }
}

async function cleanOldBackups() {
  try {
    const files = fs.readdirSync(backupsDir())
      .filter(f => f.startsWith('evalfp_') && f.endsWith('.db'))
      .map(f => ({
        name: f,
        path: path.join(backupsDir(), f),
        time: fs.statSync(path.join(backupsDir(), f)).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time) // Newest first
    
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000)
    let deleted = 0
    
    for (const file of files) {
      if (file.time < thirtyDaysAgo) {
        fs.unlinkSync(file.path)
        deleted++
        console.log(`  🗑 Deleted old backup: ${file.name}`)
      }
    }
    
    if (deleted > 0) {
      console.log(`✓ Cleanup: ${deleted} old backups removed`)
    }
  } catch (e) {
    console.warn('⚠ Error cleaning old backups:', e.message)
  }
}
```

**Cambio 3: Llamar setupBackups() en app.whenReady()**
```javascript
app.whenReady().then(async () => {
  await loadApiKeysFromSecureStorage()
  setupBackups()  // ← Agregar esta línea
  createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
```

---

## 🧪 TESTING MANUAL

### Test 1: Crear primer backup
1. Abrir la aplicación
2. Verificar en terminal: `✓ Automatic backups initialized (daily at 2 AM)`
3. Verificar que existe `/Users/[user]/Documents/EvalFP/backups/`

### Test 2: Guardar cambios en BD
1. Agregar un nuevo módulo
2. Guardar un alumno
3. Crear actividades

### Test 3: Verificar que el backup contiene datos
1. Cerrar la aplicación (o esperar SIGINT)
2. Verificar mensaje: `💾 Backup final antes de cerrar...`
3. Verificar que existe archivo `evalfp_YYYY-MM-DDTHH-mm-ss.db`
4. Comparar tamaño del archivo original vs backup (deben ser similares)

### Test 4: Restauración (manual, por si acaso)
```bash
# Si necesita recuperar un backup:
cp ~/Documents/EvalFP/backups/evalfp_2026-07-01T02-00-00.db ~/Documents/EvalFP/evalfp.db
```

---

## 📊 VERIFICACIÓN DE INTEGRIDAD

Después de implementar, verificar:
```bash
# Ver backups creados
ls -lh ~/Documents/EvalFP/backups/

# Ver tamaño de la BD original
ls -lh ~/Documents/EvalFP/evalfp.db

# Verificar que son archivos SQLite válidos
file ~/Documents/EvalFP/backups/evalfp_*.db
```

---

## 💾 COMMIT

```bash
git add package.json main.js
git commit -m "feat: automatic daily database backups with cleanup (SEC-003)

- main.js: Add setupBackups() for 2 AM daily backups
- main.js: Add performBackup() to create timestamped backups
- main.js: Add cleanOldBackups() to remove backups > 30 days
- main.js: Backup on graceful shutdown (SIGINT)
- package.json: Add node-schedule dependency

Backups are stored in ~/Documents/EvalFP/backups/ with timestamps
Automatic cleanup keeps only backups from the last 30 days

Fixes data loss risk and enables recovery scenarios
```

---

## ✅ DEFINICIÓN DE COMPLETADO

- [ ] node-schedule instalado en package.json
- [ ] setupBackups() implementada en main.js
- [ ] performBackup() crea archivos timestamped
- [ ] cleanOldBackups() elimina backups > 30 días
- [ ] setupBackups() llamada en app.whenReady()
- [ ] Backup en SIGINT (cierre graceful)
- [ ] Tested: backups se crean correctamente
- [ ] Tested: archivos tienen datos válidos
- [ ] Tested: limpieza de old backups funciona
- [ ] Commit en repo

---

## 🔗 REFERENCIAS

- **Problema**: SEC-003 en EXECUTION_PLAN_WEEK1-4.md
- **Librería**: https://github.com/node-schedule/node-schedule

---

**Tiempo estimado**: 1 hora  
**Dificultad**: ⭐⭐ Bajo  
**Riesgo**: Muy bajo (no afecta lógica existente)

¿Listo para implementar? 🎯

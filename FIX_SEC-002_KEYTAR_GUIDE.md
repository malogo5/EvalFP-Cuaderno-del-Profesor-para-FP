# 🔒 SEC-002: ENCRYPT API KEYS - IMPLEMENTATION GUIDE

**Categoría**: Crítico  
**Tiempo estimado**: 2 horas  
**Archivos afectados**: 3  
**Problema**: API keys se guardan en plaintext

---

## 📋 ANÁLISIS DEL PROBLEMA

### ¿Por qué es un riesgo?

Actualmente, en `/workspace/renderer/js/modules/ajustes.js`, las API keys se guardan y cargan sin encripción:

```javascript
// Vulnerable: plaintext storage
document.getElementById('save-api-keys').addEventListener('click', async () => {
  const keys = {
    openai: document.getElementById('api-key-openai').value,
    anthropic: document.getElementById('api-key-anthropic').value,
  }
  // Se guardan directamente en BD o env
  process.env.OPENAI_API_KEY = keys.openai
  process.env.ANTHROPIC_API_KEY = keys.anthropic
})
```

**Riesgos**:
1. ❌ Alguien con acceso físico puede leer las keys del archivo/BD
2. ❌ Si la DB se filtra, todas las keys quedan expuestas
3. ❌ Memory dumps pueden revelar las keys
4. ❌ No hay auditoría de quién accede a las keys

### Solución: keytar

`keytar` usa el almacenamiento seguro del SO:
- **Windows**: DPAPI (Data Protection API)
- **macOS**: Keychain
- **Linux**: libsecret

```javascript
// Seguro: almacenamiento encriptado del SO
const keytar = require('keytar')
await keytar.setPassword('EvalFP', 'openai_api_key', keys.openai)
const key = await keytar.getPassword('EvalFP', 'openai_api_key')
```

---

## 🔍 ARCHIVOS A ACTUALIZAR

### Archivo 1: package.json
**Ubicación**: `/workspace/package.json`

**Cambio**: Agregar dependencia keytar

**Antes**:
```json
"dependencies": {
  "electron": "^latest",
  "better-sqlite3": "^latest"
}
```

**Después**:
```json
"dependencies": {
  "electron": "^latest",
  "better-sqlite3": "^latest",
  "keytar": "^7.9.0"
}
```

**Comando**:
```bash
npm install keytar
```

---

### Archivo 2: main.js
**Ubicación**: `/workspace/main.js`

Agregar función para recuperar API keys de keytar al iniciar la app.

**Cambio 1: Importar keytar (línea 1)**
```javascript
// Antes
const { app, BrowserWindow, ipcMain } = require('electron')

// Después
const { app, BrowserWindow, ipcMain } = require('electron')
const keytar = require('keytar')
```

**Cambio 2: Cargar keys en createWindow() (línea ~40)**
```javascript
// Agregar esta función antes de createWindow
async function loadApiKeysFromSecureStorage() {
  try {
    const openaiKey = await keytar.getPassword('EvalFP', 'openai_api_key')
    const anthropicKey = await keytar.getPassword('EvalFP', 'anthropic_api_key')
    
    if (openaiKey) process.env.OPENAI_API_KEY = openaiKey
    if (anthropicKey) process.env.ANTHROPIC_API_KEY = anthropicKey
    
    console.log('✓ API keys loaded from secure storage')
  } catch (e) {
    console.warn('⚠ Error loading API keys from keytar:', e.message)
  }
}

// Modificar createWindow para llamar a loadApiKeysFromSecureStorage
async function createWindow() {
  await loadApiKeysFromSecureStorage()
  const win = new BrowserWindow({...})
  // resto del código
}
```

**Cambio 3: Manejar guardado de keys (agregar después de createWindow)**

Agregar IPC handler para guardar keys con seguridad:

```javascript
ipcMain.handle('save-api-keys', async (event, keys) => {
  try {
    if (keys.openai) {
      await keytar.setPassword('EvalFP', 'openai_api_key', keys.openai)
      process.env.OPENAI_API_KEY = keys.openai
    }
    if (keys.anthropic) {
      await keytar.setPassword('EvalFP', 'anthropic_api_key', keys.anthropic)
      process.env.ANTHROPIC_API_KEY = keys.anthropic
    }
    return { success: true, message: 'Keys saved securely' }
  } catch (e) {
    console.error('Error saving API keys:', e)
    return { success: false, error: e.message }
  }
})
```

---

### Archivo 3: renderer/js/modules/ajustes.js
**Ubicación**: `/workspace/renderer/js/modules/ajustes.js`

**Cambio actual** (línea ~17):
```javascript
async function saveApiKeys() {
  const openai = document.getElementById('api-key-openai').value
  const anthropic = document.getElementById('api-key-anthropic').value
  
  // Vulnerable: se guardaban en proceso
  process.env.OPENAI_API_KEY = openai
  process.env.ANTHROPIC_API_KEY = anthropic
}
```

**Cambio mejorado**:
```javascript
async function saveApiKeys() {
  const openai = document.getElementById('api-key-openai').value
  const anthropic = document.getElementById('api-key-anthropic').value
  
  if (!openai && !anthropic) {
    showToast('Ingresa al menos una API key', 'warning')
    return
  }
  
  try {
    const result = await window.api.saveApiKeys({ openai, anthropic })
    if (result.success) {
      showToast('🔐 API keys guardadas de forma segura', 'success')
      // Limpiar campos si se desea
      // document.getElementById('api-key-openai').value = ''
      // document.getElementById('api-key-anthropic').value = ''
    } else {
      showToast('Error: ' + result.error, 'error')
    }
  } catch (e) {
    showToast('Error al guardar keys: ' + e.message, 'error')
  }
}
```

**Agregar al preload.js**:

En `/workspace/preload.js`, agregar API para guardar keys:

```javascript
// Agregar a contextBridge.exposeInMainWorld('api', {
saveApiKeys: (keys) => ipcRenderer.invoke('save-api-keys', keys),
```

---

## 🧪 TESTING MANUAL

### Test 1: Almacenamiento seguro
1. Abrir **Ajustes**
2. Ingresar OpenAI API key: `sk-test123456`
3. Guardar keys
4. **Verificar**:
   - ✅ Mensaje "API keys guardadas de forma segura"
   - ✅ Key NO aparece en proceso.env como plaintext (verificar con DevTools)

### Test 2: Carga en reinicio
1. Guardar una API key
2. Cerrar y reabrir la aplicación
3. Ir a Ajustes
4. **Verificar**:
   - ✅ Key está recuperada del almacenamiento seguro
   - ✅ No había que introducirla de nuevo

### Test 3: SO específico
- **Windows**: Verificar que DPAPI está siendo usado (en Credential Manager)
- **macOS**: Verificar que Keychain tiene "EvalFP" entries
- **Linux**: Verificar que libsecret está siendo usado

---

## 💾 COMMIT

```bash
git add package.json main.js preload.js renderer/js/modules/ajustes.js
git commit -m "security: encrypt API keys with keytar OS-level storage

- main.js: Add loadApiKeysFromSecureStorage() to recover keys at startup
- main.js: Add IPC handler for secure key storage (save-api-keys)
- preload.js: Expose saveApiKeys API to renderer
- ajustes.js: Use secure storage instead of plaintext process.env
- package.json: Add keytar dependency for OS-level encryption

Fixes SEC-002 vulnerability - prevents plaintext API key storage
Co-Authored-By: Abacus.AI CLI <agent@abacus.ai>"
```

---

## ✅ DEFINICIÓN DE COMPLETADO

- [ ] keytar instalado en package.json
- [ ] main.js carga keys seguramente en startup
- [ ] main.js tiene IPC handler para save-api-keys
- [ ] preload.js expone saveApiKeys a renderer
- [ ] ajustes.js usa saveApiKeys en lugar de process.env
- [ ] Tested: keys se guardan sin plaintext
- [ ] Tested: keys se cargan en reinicio
- [ ] Tested: OS-specific storage funciona
- [ ] Commit en repo
- [ ] Tests pasen

---

## 🔗 REFERENCIAS

- **Problema**: SEC-002 en ISSUES_FOUND.md
- **Contexto**: API Key Management section en AUDIT_REPORT.md
- **Librería**: https://github.com/atom/node-keytar

---

**Tiempo estimado**: 2 horas  
**Dificultad**: ⭐⭐⭐ Medio  
**Riesgo**: Bajo (no afecta lógica existente)

¿Listo para implementar? 🎯

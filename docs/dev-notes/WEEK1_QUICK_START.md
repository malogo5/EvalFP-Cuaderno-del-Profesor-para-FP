# ⚡ QUICK START GUIDE - WEEK 1 SECURITY FIXES

## SEC-001: XSS Prevention (✅ COMPLETED)

```bash
# Status: DONE
git log --oneline | head -1
# Output: 1a22045 security: prevent XSS by escaping user input in innerHTML
```

**Files Modified**:
- renderer/js/modules/modulos.js ✅
- renderer/js/modules/programacion.js ✅
- renderer/js/modules/notas.js ✅

---

## SEC-002: API Key Encryption (📋 READY)

### 1️⃣ Install Dependencies
```bash
npm install keytar
```

### 2️⃣ Modify main.js
Location: `/workspace/main.js` (after line 1)

```javascript
const keytar = require('keytar')

// Add this function before createWindow()
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

// Modify createWindow() to call loadApiKeysFromSecureStorage
async function createWindow() {
  await loadApiKeysFromSecureStorage()
  // ... rest of function
}

// Add IPC handler (after createWindow definition)
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

### 3️⃣ Modify preload.js
Add to `contextBridge.exposeInMainWorld('api', {`:

```javascript
saveApiKeys: (keys) => ipcRenderer.invoke('save-api-keys', keys),
```

### 4️⃣ Modify ajustes.js
Replace `saveApiKeys()` function:

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
    } else {
      showToast('Error: ' + result.error, 'error')
    }
  } catch (e) {
    showToast('Error al guardar keys: ' + e.message, 'error')
  }
}
```

### 5️⃣ Test
```bash
# Open the app
npm start

# Go to Ajustes section
# Enter test API key: sk-test-123
# Click save
# Verify: Message "API keys guardadas de forma segura"
# Restart app and verify key is still there
```

### 6️⃣ Commit
```bash
git add package.json main.js preload.js renderer/js/modules/ajustes.js
git commit -m "security: encrypt API keys with keytar OS-level storage

- main.js: Add loadApiKeysFromSecureStorage() and IPC handler
- preload.js: Expose saveApiKeys API
- ajustes.js: Use secure storage instead of plaintext
- package.json: Add keytar dependency

Fixes SEC-002 vulnerability
```

---

## SEC-003: Automatic Backups (📋 PENDING)

### Overview
Use `node-schedule` to backup database automatically

### Install (when ready)
```bash
npm install node-schedule
```

### Expected Changes
- main.js: Schedule backups every hour
- Create backup directory: `~/.evalfp/backups/`
- Keep last 7 backups

---

## SEC-004: Centralized Logging (📋 PENDING)

### Overview
Use `winston` for structured logging instead of console.log

### Install (when ready)
```bash
npm install winston
```

### Expected Changes
- main.js: Initialize winston logger
- main.js: Replace console.log with logger
- renderer/js/app.js: Optional client-side logging

---

## 📋 TESTING CHECKLIST

### After Each Fix
```bash
# Run the app
npm start

# Test basic functionality
- [ ] App starts without errors
- [ ] Can navigate all sections
- [ ] No console errors (press F12)

# Test the specific fix
- SEC-001: Create XSS payload, verify no alert
- SEC-002: Save API key, restart, verify still there
- SEC-003: Check backup folder after 1 hour
- SEC-004: Check logs for proper format
```

---

## 🔍 DEBUGGING

### If npm install keytar fails
```bash
# On macOS: ensure Xcode Command Line Tools are installed
xcode-select --install

# On Linux: install build dependencies
sudo apt-get install build-essential python3

# On Windows: Install Visual Studio Build Tools
```

### If keytar doesn't work
```bash
# Check if keytar is properly installed
node -e "const k = require('keytar'); console.log('keytar loaded')"

# Check OS keystore
# Windows: Control Panel → Credential Manager
# macOS: Keychain Access app
# Linux: gnome-keyring or kwallet
```

### Clear stored keys
```bash
# Remove keytar entries (if needed for testing)
node -e "const keytar = require('keytar'); keytar.deletePassword('EvalFP', 'openai_api_key')"
```

---

## 📊 TIME TRACKING

Use this to track actual time spent vs estimated:

```
SEC-001: Estimated 2h, Actual 0.75h ✅ DONE
SEC-002: Estimated 2h, Actual ?h
SEC-003: Estimated 1h, Actual ?h
SEC-004: Estimated 2h, Actual ?h
QA Dashboard: Estimated 4h, Actual ?h
```

---

## 🎯 MILESTONE CHECK

When SEC-002 is complete, check:
- [ ] `npm start` launches without errors
- [ ] Can set API keys in Ajustes section
- [ ] Keys persist after app restart
- [ ] No plaintext keys in environment
- [ ] Git commit created
- [ ] Can proceed to SEC-003

---

## 📚 REFERENCE DOCUMENTS

- [EXECUTION_PLAN_WEEK1-4.md](file:///workspace/EXECUTION_PLAN_WEEK1-4.md) - Master timeline
- [FIX_SEC-001_XSS_GUIDE.md](file:///workspace/FIX_SEC-001_XSS_GUIDE.md) - Detailed XSS guide
- [FIX_SEC-002_KEYTAR_GUIDE.md](file:///workspace/FIX_SEC-002_KEYTAR_GUIDE.md) - Detailed keytar guide
- [SEC-001_COMPLETION_REPORT.md](file:///workspace/SEC-001_COMPLETION_REPORT.md) - Completion status
- [SEMANA_1_STATUS.md](file:///workspace/SEMANA_1_STATUS.md) - Weekly progress

---

## 💡 PRO TIPS

1. **Test in isolation**: Make one change, test it, commit it
2. **Keep detailed logs**: Write down what was tested and when
3. **Document issues**: If something breaks, document the fix for later
4. **Review before commit**: `git diff` before committing
5. **Use descriptive messages**: Commit messages should be clear and specific

---

**Last Updated**: 2026-07-01  
**Next Step**: SEC-002 Implementation  
**Estimated Time**: 2 hours

# HOTFIX: Keytar Native Module Error on macOS

## Problem
The app fails on macOS with:
```
Error: dlopen(/Users/isabel/Documents/Claude/Projects/Cuaderno del profesor/evalfp-app/node_modules/keytar/build/Release/keytar.node, 0x0001): 
tried: '.../keytar/build/Release/keytar.node' (slice is not valid mach-o file)
```

**Cause**: The `.node` file is either corrupted or built for a different macOS/Electron version.

---

## Solution 1: Rebuild Keytar (Recommended)

### Step 1: Clean Node Modules
```bash
rm -rf node_modules/keytar
rm -rf node_modules/@types/keytar
```

### Step 2: Rebuild Keytar
```bash
npm rebuild keytar --build-from-source
```

Or force reinstall:
```bash
npm install keytar@7.9.0 --force --build-from-source
```

### Step 3: Verify Build
```bash
ls -la node_modules/keytar/build/Release/keytar.node
# Should show file with normal size (not 0 bytes)
```

### Step 4: Test
```bash
npm start
```

---

## Solution 2: If Rebuild Fails - Use Conditional Import

If keytar cannot be built in your macOS environment, use a graceful fallback:

### Edit `main.js` - Add Conditional Keytar Import

```javascript
'use strict'

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const Database = require('better-sqlite3')
const schedule = require('node-schedule')
const logger = require('./main/logger')
const os = require('os')
const fs = require('fs')

// FALLBACK: Try to load keytar, but don't crash if it fails
let keytar = null
try {
  keytar = require('keytar')
  logger.logEvent('keytar loaded successfully')
} catch (err) {
  logger.logEvent(`Warning: keytar failed to load (${err.message}). Using filesystem fallback.`)
}

// ... rest of the code
```

### Edit `loadApiKeysFromSecureStorage()` Function

```javascript
async function loadApiKeysFromSecureStorage() {
  try {
    if (!keytar) {
      logger.logEvent('Keytar not available. Loading from database.')
      // Fallback to database storage
      const db = new Database(dbPath())
      const cfg = db.prepare('SELECT * FROM cfg').get()
      if (cfg) {
        return {
          openaiKey: cfg.openaiKey || '',
          anthropicKey: cfg.anthropicKey || ''
        }
      }
      return { openaiKey: '', anthropicKey: '' }
    }

    const openaiKey = await keytar.getPassword('EvalFP', 'openai_key') || ''
    const anthropicKey = await keytar.getPassword('EvalFP', 'anthropic_key') || ''
    
    return { openaiKey, anthropicKey }
  } catch (err) {
    logger.logEvent(`Error loading API keys: ${err.message}`)
    return { openaiKey: '', anthropicKey: '' }
  }
}
```

### Edit IPC Handler for `api:saveKeys`

```javascript
ipcMain.handle('api:saveKeys', async (event, keys) => {
  try {
    if (!keytar) {
      // Fallback: save to database
      logger.logEvent('Saving API keys to database (keytar not available)')
      const db = new Database(dbPath())
      db.prepare(`
        UPDATE cfg 
        SET openaiKey = ?, anthropicKey = ?
      `).run(keys.openaiKey || '', keys.anthropicKey || '')
      return { success: true }
    }

    // Use keytar for secure storage
    await keytar.setPassword('EvalFP', 'openai_key', keys.openaiKey || '')
    await keytar.setPassword('EvalFP', 'anthropic_key', keys.anthropicKey || '')
    
    logger.logEvent('API keys saved to keytar successfully')
    return { success: true }
  } catch (err) {
    logger.logEvent(`Error saving API keys: ${err.message}`)
    return { success: false, error: err.message }
  }
})
```

---

## Solution 3: Alternative - Use OS Keychain Directly (macOS Only)

If keytar module won't build, use native macOS commands:

### Create `main/macos-keychain.js`

```javascript
'use strict'

const { execSync } = require('child_process')
const os = require('os')

class MacOSKeychain {
  constructor() {
    this.isSupported = os.platform() === 'darwin'
  }

  setPassword(service, account, password) {
    if (!this.isSupported) return false
    try {
      const cmd = `security add-generic-password -U -a "${account}" -s "${service}" -w "${password.replace(/"/g, '\\"')}"`
      execSync(cmd, { stdio: 'pipe' })
      return true
    } catch (err) {
      throw new Error(`Failed to set password: ${err.message}`)
    }
  }

  getPassword(service, account) {
    if (!this.isSupported) return null
    try {
      const cmd = `security find-generic-password -a "${account}" -s "${service}" -w`
      const password = execSync(cmd, { stdio: 'pipe' }).toString().trim()
      return password
    } catch (err) {
      return null
    }
  }
}

module.exports = new MacOSKeychain()
```

---

## Troubleshooting

### Check Electron Version Compatibility
```bash
npm list electron keytar
```

Ensure versions are compatible. Current support:
- Electron: 42.5.1
- keytar: 7.9.0

### Verify Xcode Tools (Required for Native Build)
```bash
xcode-select --install
```

### Try Alternative Keytar Version
```bash
npm install keytar@7.8.1 --save --build-from-source
```

---

## Quick Checklist for macOS

- [ ] Xcode Command Line Tools installed (`xcode-select --install`)
- [ ] Node.js and npm up to date
- [ ] Remove and rebuild keytar
- [ ] Test with `npm start`
- [ ] If fails, implement fallback solution (Solution 2)

---

## Prevention for Future Installs

Add this to `package.json` scripts:

```json
{
  "scripts": {
    "postinstall": "npm rebuild keytar --build-from-source 2>/dev/null || echo 'Warning: keytar rebuild skipped'"
  }
}
```


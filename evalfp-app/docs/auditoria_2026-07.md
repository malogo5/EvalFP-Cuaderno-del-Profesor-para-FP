# Auditoría EvalFP — Julio 2026

Auditoría completa desde perspectiva de programador y de usuario. Clasificación por severidad: 🔴 Alta · 🟡 Media · 🟢 Baja / Mejora.

---

## PARTE I — PROGRAMADOR

### 1. Bugs / Correctness

**🔴 Backup corrupto en escritura concurrente**
`performBackup()` usa `fs.copyFileSync` para copiar `evalfp.db`. Si better-sqlite3 está escribiendo en ese momento (WAL mode activo), la copia puede quedar inconsistente. La API correcta es `db.backup(destPath)` de better-sqlite3, que hace una copia online y segura.
```js
// ❌ Actual
fs.copyFileSync(src, dest)

// ✅ Correcto
await getDb().backup(dest)
```

**🔴 Backup final nunca se ejecuta en cierre normal**
`setupBackups()` escucha `process.on('SIGINT', ...)` (Ctrl+C en terminal). Pero cuando el usuario cierra la app con Cmd+Q o cierra la ventana, Electron emite `before-quit` / `will-quit`, no SIGINT. El backup de cierre nunca se ejecuta en uso real.
```js
// Añadir en app.whenReady():
app.on('before-quit', async () => { await performBackup() })
```

**🔴 Tabla `cfg` no está en el schema de `db.js`**
`main.js` accede a `SELECT openaiKey, anthropicKey FROM cfg` y `UPDATE cfg SET openaiKey = ?` directamente con una conexión nueva (`new Database(dbPath())`). Esta tabla nunca se crea en `_initSchema()`. En una instalación limpia la query falla silenciosamente y el fallback de API keys no funciona.

**🟡 `tmpDatos` JSON temporal nunca se borra**
En `ipcMain.on('gen-apuntes', ...)`, se escribe un fichero `/tmp/evalfp_mod_*.json` con los datos del módulo. Si `build_apuntes.py` falla o el proceso muere, ese fichero queda huérfano indefinidamente. Añadir limpieza en el callback `close`:
```js
proc.on('close', code => {
  if (tmpDatos) { try { fs.unlinkSync(tmpDatos) } catch(_) {} }
  event.reply(replyChannel, { type:'done', code })
})
```

**🟡 `esc()` no escapa `>`**
```js
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')
// Falta: .replace(/>/g,'&gt;')
```
Aunque raro, omitir `>` puede provocar inyección en atributos HTML y edge cases.

### 2. Seguridad

**🔴 API keys en texto plano en SQLite**
`ajustes.js` llama a `window.api.setConfig('openaiKey', openai)` que guarda la key en la tabla `config` sin cifrar. El canal seguro `window.api.saveApiKeys()` que usa keytar está implementado en `preload.js` e `ipcMain` pero nunca se llama desde `ajustes.js`. Las keys de profesor están expuestas en el fichero SQLite.

**🟡 Sin Content Security Policy**
`renderer/index.html` no tiene `<meta http-equiv="Content-Security-Policy">`. Aunque `contextIsolation: true` y `nodeIntegration: false` son correctos, la ausencia de CSP elimina una capa de defensa en profundidad.
```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'">
```

**🟡 `csrf-token.js` y `session-manager.js` son código fantasma**
Se cargan 600+ líneas de utilidades de seguridad web (CSRF tokens, session timeout) irrelevantes para una app Electron local sin servidor y sin autenticación de usuarios. Añaden superficie de código sin valor. Candidatas a eliminar.

### 3. CI/CD

**🔴 CI usa Node 18, pero better-sqlite3 compilado localmente requiere Node 20+**
`.github/workflows/ci.yml` tiene `node-version: '18'`. `better-sqlite3` compilado en local (MODULE_VERSION 115) requiere Node ~20/22. Los tests unitarios fallarán en el runner de CI con el mismo `ERR_DLOPEN_FAILED` que se resolvió localmente. Cambiar a `node-version: '20'`.

**🔴 ESLint tiene 3 errores que harán fallar el job `lint`**
- `main.js:431` → `no-useless-escape`: `\-` dentro de clase de caracteres `[...]` no necesita escape.
- `ia.js:72` → `no-empty`: bloque `catch (_) {}` vacío.
- `programacion.js:29` → `no-empty`: bloque `catch(e) {}` vacío.

Ninguno de los tres es un bug real, pero la regla ESLint es un error (no warning), por lo que CI falla en cada push.

**🟡 `package-lock.json` no incluye devDependencies nuevas**
`eslint`, `@eslint/js`, `@playwright/test`, `globals`, `vitest`, `electron`, `electron-builder` aparecen en `package.json` pero no en `package-lock.json`. Indica que no se ha ejecutado `npm install` después de añadirlos. El CI ejecuta `npm ci` que requiere coherencia entre ambos ficheros.

### 4. Dependencias

**🔴 5 vulnerabilidades en dependencias (1 crítica)**
```
vitest        → crítica  (cadena: vitest → vite-node → vite → esbuild)
electron ^22  → alta     (18 CVEs, incluyendo heap overflow, ASAR bypass)
vite          → alta
esbuild       → moderada
vite-node     → moderada
```
Electron 22 está muy desactualizado; la versión actual es 43+. `npm audit fix --force` actualizaría a Electron 43 (breaking change, requiere validar).

### 5. Calidad de código

**🟡 `__mocks__/electron.js` es código muerto**
El directorio `__mocks__` se creó pensando en `vi.mock()`, pero el mock real se aplica vía `require.cache` en `tests/unit/setup.js`. El fichero `__mocks__/electron.js` nunca se carga y puede confundir a futuros desarrolladores.

**🟡 91 warnings ESLint (principalmente `no-unused-vars` en `programacion.js`)**
Funciones como `deleteActividadRow`, `saveUtField`, `addUt`, `deleteUt`, etc. están declaradas en `programacion.js` pero ESLint las marca como "never used". Son funciones llamadas desde `onclick` en HTML — ESLint no las detecta porque se enlazan dinámicamente via `registerWindowHandlers`. No son bugs, pero generan ruido.

**🟢 `app (colorido).css` — fichero de backup en producción**
`renderer/css/app (colorido).css` es una variante de diseño que no se usa en ningún `<link>` ni `<script>`. Es código muerto en el directorio de producción.

**🟢 `evalfp.db` vacío (0 bytes) en la raíz del repo**
Existe un fichero `evalfp.db` de 0 bytes en la raíz de `evalfp-app/`. Aunque `*.db` está en `.gitignore`, el fichero físico existe y puede confundir (la DB real está en `~/Documents/EvalFP/evalfp.db`).

**🟢 `requirements.txt` tiene anthropic y openai comentados**
Las dependencias de IA están comentadas en `requirements.txt`. El `build_apuntes.py` las necesita pero el instalador no las incluye por defecto. Un profesor que ejecute `pip install -r requirements.txt` y luego intente generar apuntes recibirá un error críptico de `ModuleNotFoundError`.

---

## PARTE II — USUARIO

### 6. UX — Flujos críticos

**🔴 Las API keys se guardan pero nunca se muestra si están configuradas**
En Ajustes, los campos de API key están siempre vacíos al abrirlos (`loadAjustes()` los vacía explícitamente por seguridad). El resultado: el profesor nunca sabe si tiene una key guardada o no. No hay indicador de estado. Un `✓ Clave configurada` o `Sin clave` junto a cada campo resolvería esto.

**🟡 48 llamadas a `alert()` nativo del sistema**
Se usan `alert()` y `confirm()` del navegador/sistema en 48 y 4 lugares respectivamente. En macOS estos diálogos son modales de sistema que interrumpen completamente el flujo, no coinciden visualmente con la UI oscura de la app, y bloquean el hilo principal. El `<dialog>` HTML ya se usa en un sitio (importar alumnos) — debería extenderse al resto.

**🟡 Informe IA: las notas del alumno hay que introducirlas a mano**
La pestaña "Informe" del Asistente IA pide al profesor que escriba `RA1:7,RA2:5.5,RA3:8`. La app ya tiene esas notas en SQLite, calculadas por módulo y alumno. El campo debería pre-rellenarse automáticamente cuando el profesor selecciona módulo + alumno en el desplegable.

**🟡 Apuntes HTML: sin CTA al terminar la generación**
Cuando `build_apuntes.py` termina, el terminal muestra `✅ Completado`. Pero el archivo HTML generado está en `~/Documents/EvalFP/apuntes/` y el profesor tiene que ir a encontrarlo manualmente. `window.api.openOutput()` existe y abre la carpeta — debería llamarse automáticamente o añadir un botón "📂 Abrir carpeta" al detectar `type === 'done'`.

**🟡 Modal "Añadir módulo" no es un `<dialog>` nativo**
Es un `<div class="modal-overlay">`. Consecuencias: no hay focus trap (Tab puede salir del modal), no se cierra con `Escape`, no es accesible para lectores de pantalla. La transición debería ser a `<dialog>` con `showModal()`.

### 7. UX — Flujos secundarios

**🟡 Pantallas vacías sin guía de acción cuando no hay módulos**
En Programación, Alumnos, Notas, Evaluaciones, Dashboard — si la lista de módulos está vacía, el usuario ve "Selecciona un módulo" pero no hay ninguno. No hay CTA directo a "Añadir un módulo primero". Un empty state con enlace a la sección de Módulos mejoraría la activación de nuevos usuarios.

**🟡 Importar alumnos no detecta duplicados**
`confirmImportAlumnos()` inserta todos los alumnos del textarea sin comprobar si ya existen (mismo nombre/NIA). Si el profesor importa dos veces la misma lista, se duplican todos los alumnos.

**🟢 Sin `aria-label` en botones de emoji**
Botones como `📄 Boletín PDF` o `＋ Añadir módulo` con emoji como ícono principal no tienen `aria-label`. Un lector de pantalla anunciaría el código del emoji, no la acción.

**🟢 Minúscula/Mayúscula en estado de alumnos**
Los estados válidos son `['Activo','Pendiente','Baja']` con primera letra mayúscula (definido en `preload.js`). El HTML muestra opciones en español con acentos. Si el backend cambia o si se intenta guardar `'activo'` (minúsculas), el validador rechaza silenciosamente.

**🟢 Navegación con teclado en modales no funciona del todo**
Los modales de UT/actividades usan `onclick` en overlay para cerrar pero no tienen listener de `keydown` para `Escape`. En notas y alumnos sí hay atajos de teclado (bien implementados), pero la consistencia falla en los modales.

---

## Resumen ejecutivo

| Área | 🔴 Alta | 🟡 Media | 🟢 Baja |
|------|---------|----------|---------|
| Bugs / Correctness | 3 | 2 | — |
| Seguridad | 1 | 2 | — |
| CI/CD | 2 | 1 | — |
| Dependencias | 1 | — | — |
| Calidad de código | — | 2 | 3 |
| UX crítica | 1 | 2 | — |
| UX secundaria | — | 2 | 3 |
| **Total** | **8** | **11** | **6** |

### Top 5 a resolver primero

1. **CI Node version** → cambiar a `node-version: '20'` en `ci.yml` (5 min)
2. **3 errores ESLint** → `\-` → `-`, dos `catch` vacíos con comentario `// intencionado` (10 min)
3. **API keys en texto plano** → usar `window.api.saveApiKeys()` en `ajustes.js` (30 min)
4. **Backup seguro** → reemplazar `copyFileSync` por `db.backup()` + listener `before-quit` (1h)
5. **Tabla `cfg` en schema** → añadir `CREATE TABLE IF NOT EXISTS cfg (openaiKey TEXT, anthropicKey TEXT)` a `_initSchema()` (15 min)

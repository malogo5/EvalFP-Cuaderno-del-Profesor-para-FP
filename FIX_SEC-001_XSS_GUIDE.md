# 🔒 SEC-001: FIX XSS - GUÍA IMPLEMENTACIÓN

**Categoría**: Crítico  
**Tiempo estimado**: 2 horas  
**Archivos afectados**: 3  
**Instancias**: 28+ de innerHTML sin escapar  

---

## 📋 ANÁLISIS DEL PROBLEMA

### ¿Qué es XSS?
Cross-Site Scripting (XSS) - Inyección de código JavaScript malicioso a través de datos de usuario.

### Ejemplo de Ataque
```javascript
// Si un profesor introduce en el nombre de módulo:
nombre = "<img src=x onerror=\"alert('XSS')\">"

// El resultado en DOM sería:
<div>${m.nombre}</div>
// Se convierte en:
<div><img src=x onerror="alert('XSS')"></div>
// ¡SE EJECUTA EL JAVASCRIPT! 🔴
```

### Función esc() existente
```javascript
// Ya existe en app.js línea 69
const esc = s => 
  (s||'').replace(/&/g,'&amp;')
          .replace(/</g,'&lt;')
          .replace(/"/g,'&quot;')

// Convierte caracteres peligrosos en entidades HTML
"<img>" → "&lt;img&gt;" (seguro)
```

---

## 🔍 ARCHIVOS A ACTUALIZAR

### Archivo 1: modulos.js (4 cambios)

**Ubicación**: `renderer/js/modules/modulos.js`

#### Cambio 1: renderModulos() línea 11
**Antes**:
```javascript
el.innerHTML = _modulos.map(m => `
  <div class="mod-card ${_curMod?.id===m.id?'active-mod':''}">
    <button class="mod-card-del">✕</button>
    <div class="mod-card-abrev">${m.abrev}</div>
    <div class="mod-card-nombre">${m.nombre}</div>
    <div class="mod-card-meta">
      ${m.ciclo||''} · ${m.curso||''} · ${m.anno||''}
      ${m.decreto ? `<br><span>${m.decreto}</span>` : ''}
    </div>
  </div>
`).join('')
```

**Después**:
```javascript
el.innerHTML = _modulos.map(m => `
  <div class="mod-card ${_curMod?.id===m.id?'active-mod':''}">
    <button class="mod-card-del">✕</button>
    <div class="mod-card-abrev">${esc(m.abrev)}</div>
    <div class="mod-card-nombre">${esc(m.nombre)}</div>
    <div class="mod-card-meta">
      ${esc(m.ciclo||'')} · ${esc(m.curso||'')} · ${esc(m.anno||'')}
      ${m.decreto ? `<br><span>${esc(m.decreto)}</span>` : ''}
    </div>
  </div>
`).join('')
```

**Cambio**: Agregar `esc()` a: abrev, nombre, ciclo, curso, anno, decreto

---

#### Cambio 2: renderModDropdown() línea 49
**Antes**:
```javascript
dd.innerHTML = _modulos.map(m => `
  <div class="mod-dd-item">
    <span class="mod-dd-abrev">${m.abrev}</span>
    <div class="mod-dd-info">
      <div class="mod-dd-nombre">${m.nombre}</div>
      <div class="mod-dd-meta">${[m.curso, m.grupo].filter(Boolean).join(' · ')}</div>
    </div>
  </div>
`).join('')
```

**Después**:
```javascript
dd.innerHTML = _modulos.map(m => `
  <div class="mod-dd-item">
    <span class="mod-dd-abrev">${esc(m.abrev)}</span>
    <div class="mod-dd-info">
      <div class="mod-dd-nombre">${esc(m.nombre)}</div>
      <div class="mod-dd-meta">${[esc(m.curso), esc(m.grupo)].filter(Boolean).join(' · ')}</div>
    </div>
  </div>
`).join('')
```

**Cambio**: Agregar `esc()` a: abrev, nombre, curso, grupo

---

#### Cambio 3: renderModRasPanel() línea 93-100
**Antes**:
```javascript
html += `
  <div class="card">
    <span style="color:var(--accent2)">${ra.id}</span>
    <span>${ra.nombre}</span>
    ${ra.pond ? `<span>${ra.pond}%</span>` : ''}
  </div>
  ${raCes.length ? `<div>${raCes.map(ce => `
    <span>${ce.id}</span>
    <span>${ce.texto}</span>
  `).join('')}</div>` : ''}
`
```

**Después**:
```javascript
html += `
  <div class="card">
    <span style="color:var(--accent2)">${esc(ra.id)}</span>
    <span>${esc(ra.nombre)}</span>
    ${ra.pond ? `<span>${esc(String(ra.pond))}%</span>` : ''}
  </div>
  ${raCes.length ? `<div>${raCes.map(ce => `
    <span>${esc(ce.id)}</span>
    <span>${esc(ce.texto)}</span>
  `).join('')}</div>` : ''}
`
```

**Cambio**: Agregar `esc()` a: ra.id, ra.nombre, ra.pond, ce.id, ce.texto

---

### Archivo 2: programacion.js (8+ cambios)

**Ubicación**: `renderer/js/modules/programacion.js`

Este archivo es muy grande (729 líneas). Buscar todas las instancias de:
```javascript
`${uts.map(u => `<div>${u.nombre}</div>`)`
```

**Patrón a buscar**:
```
${u.nombre}  →  ${esc(u.nombre)}
${u.horas}   →  ${esc(String(u.horas))}
${ra.nombre} →  ${esc(ra.nombre)}
${ce.texto}  →  ${esc(ce.texto)}
```

**Comando para encontrar**:
```bash
grep -n "\${[^}]*\\.nombre\|\\.[a-z]*}" /workspace/renderer/js/modules/programacion.js | grep innerHTML
```

**Cambios específicos** (aproximadamente líneas 150-700):
- Todas las interpolaciones en templates
- Nombres de UT, RA, CE
- Horas, ponderaciones
- Descripción de criterios

---

### Archivo 3: notas.js (2 cambios)

**Ubicación**: `renderer/js/modules/notas.js`

#### Cambio 1: renderNotasGrid() thead línea 40-42
**Antes**:
```javascript
const thead = `<tr>
  <th>Alumno/a</th>
  ${acts.map(a => `<th title="${a.descripcion}">
    <div>${a.instrumento}</div>
    <div>${a.ut_id||'EV'+a.eval}</div>
  </th>`).join('')}
</tr>`
```

**Después**:
```javascript
const thead = `<tr>
  <th>Alumno/a</th>
  ${acts.map(a => `<th title="${esc(a.descripcion)}">
    <div>${esc(a.instrumento)}</div>
    <div>${esc(a.ut_id)||'EV'+a.eval}</div>
  </th>`).join('')}
</tr>`
```

**Cambio**: Agregar `esc()` a: descripcion, instrumento, ut_id

#### Cambio 2: renderNotasGrid() tbody línea 61
**Antes**:
```javascript
<td class="sticky-col">
  ${esc(al.apellidos||'')}${al.apellidos&&al.nombre?', ':''}${esc(al.nombre||'')}
</td>
```

**Ya está bien** ✅ (ya usa esc())

---

## 🧪 TESTING MANUAL

### Después de cada cambio:

1. **Test XSS en módulos**:
   - Crear nuevo módulo
   - Nombre: `<img src=x onerror="alert('test')">`
   - Si ve "test", ✅ no ha sido patcheado
   - Si NO ve "test", ✅ está patcheado correctamente

2. **Test XSS en RAs**:
   - Editar nombre de RA
   - Valor: `<script>alert('xss')</script>`
   - Verificar que se escapa

3. **Test XSS en notas**:
   - Agregar actividad
   - Instrumento: `<img src=x onerror="alert('nota')">`
   - Verificar que se escapa

---

## 💾 COMMIT

```bash
git add renderer/js/modules/modulos.js
git add renderer/js/modules/programacion.js
git add renderer/js/modules/notas.js
git commit -m "security: prevent XSS by escaping user input in innerHTML

- modulos.js: Escape abrev, nombre, ciclo, curso, anno, decreto
- programacion.js: Escape all UT/RA/CE names and descriptions
- notas.js: Escape instrumento, descripcion, ut_id

Fixes SEC-001 vulnerability"
```

---

## ✅ DEFINICIÓN DE COMPLETADO

- [ ] 28+ instancias de datos escapados con esc()
- [ ] Tested en todos los módulos (modulos, programacion, notas)
- [ ] Validación manual: no se ejecuta JavaScript
- [ ] Commit en repo
- [ ] Tests pasen

---

## 🔗 REFERENCIAS

- **Problema**: SEC-001 en ISSUES_FOUND.md
- **Contexto**: XSS section en AUDIT_REPORT.md
- **Estándar**: OWASP XSS Prevention Cheat Sheet

---

**Tiempo estimado**: 2 horas  
**Dificultad**: ⭐⭐ Fácil  
**Riesgo**: Bajo (buscar/reemplazar simple)

¿Listo para implementar? 🎯

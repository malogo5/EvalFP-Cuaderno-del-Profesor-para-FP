# 🚀 PLAN DE EJECUCIÓN - OPCIÓN B

**Decisión**: Implementar 27 horas de mejoras de seguridad y testing  
**Objetivo**: Publicar v3.0 RC1 seguro en 4 semanas  
**Inicio**: Semana del 1 de julio de 2026  
**Finalización**: Semana del 22 de julio de 2026

---

## 📋 SEMANA 1: SECURITY FIXES (7 horas)

### Objetivo: Resolver 4 vulnerabilidades críticas

#### 1️⃣ SEC-001: Fix XSS (2 horas)
**Archivos afectados**:
- `renderer/js/modules/modulos.js`
- `renderer/js/modules/programacion.js`
- `renderer/js/modules/notas.js`

**Checklist**:
- [ ] Revisar todas las instancias de `innerHTML`
- [ ] Aplicar función `esc()` a todos los datos
- [ ] Testing manual de campos con caracteres especiales
- [ ] Commit: "fix: XSS protection in module rendering"

**Tiempo**: 2 horas

---

#### 2️⃣ SEC-002: Encriptar API Keys (2 horas)
**Archivos afectados**:
- `package.json` (agregar keytar)
- `main.js` (cargar/guardar con keytar)
- `renderer/js/modules/ajustes.js` (validación)

**Checklist**:
- [ ] `npm install keytar`
- [ ] Implementar funciones getPassword/setPassword
- [ ] Actualizar load de API keys en startup
- [ ] Actualizar saveAjustes() para usar keytar
- [ ] Testing manual de guardar/cargar keys
- [ ] Commit: "security: encrypt API keys with keytar"

**Tiempo**: 2 horas

---

#### 3️⃣ SEC-003: Backups Automáticos (1 hora)
**Archivos afectados**:
- `package.json` (agregar node-schedule)
- `main.js` (setup de backups)

**Checklist**:
- [ ] `npm install node-schedule`
- [ ] Crear función setupBackups()
- [ ] Configurar backup diario 2 AM
- [ ] Limpieza automática (>30 días)
- [ ] Testing manual
- [ ] Commit: "feat: automatic daily backups"

**Tiempo**: 1 hora

---

#### 4️⃣ SEC-004: Logging Centralizado (2 horas)
**Archivos afectados**:
- Crear `main/logger.js` (nuevo archivo)
- `main.js` (integrar logger)
- Todos los `try/catch` (usar logger)

**Checklist**:
- [ ] Crear logger.js con winston
- [ ] Implementar logError(), logWarn(), logInfo()
- [ ] Reemplazar todos los console.log/error
- [ ] Crear archivos en userData/logs/
- [ ] Testing de logging
- [ ] Commit: "feat: centralized error logging"

**Tiempo**: 2 horas

---

### Paralelizar: QA Dashboard
Mientras se hacen los fixes, continuar con QA del Dashboard (4 horas)

**Total Semana 1**: 7h security + 4h QA = 11 horas

---

## 📋 SEMANA 2: TESTING BÁSICO (12 horas)

### Objetivo: Implementar tests automatizados

#### 1️⃣ Unit Tests - db.js (4 horas)
**Framework**: Vitest  
**Archivos**:
- Crear `tests/unit/db.test.js`

**Tests a escribir**:
- [ ] addModulo() - inserta y retorna ID
- [ ] getModulos() - retorna array
- [ ] saveAlumno() - inserta/actualiza
- [ ] saveNota() - valida rango 0-10
- [ ] SQL injection protection

**Tiempo**: 4 horas

---

#### 2️⃣ E2E Tests - Workflows (4 horas)
**Framework**: Playwright  
**Archivos**:
- Crear `tests/e2e/main-workflow.test.js`

**Workflows a testear**:
- [ ] Crear módulo
- [ ] Agregar alumno
- [ ] Guardar nota
- [ ] Verificar media
- [ ] Cambiar API key

**Tiempo**: 4 horas

---

#### 3️⃣ Paralelizar: QA IA (4 horas)
Revisión funcional del módulo IA

**Total Semana 2**: 4 + 4 + 4 = 12 horas

---

## 📋 SEMANA 3: VALIDACIÓN + DOCUMENTACIÓN (8 horas)

### Objetivo: Validar entrada y documentar

#### 1️⃣ Input Validation (3 horas)
**Archivos**:
- Crear `renderer/js/utils/validators.js` (nuevo)
- Actualizar `preload.js`
- Actualizar handlers IPC en `main.js`

**Validaciones**:
- [ ] Alumno: apellidos/nombre <100 caracteres
- [ ] Nota: 0-10, número válido
- [ ] Config: length limits, character whitelist
- [ ] UT/RA: ID format validation

**Tiempo**: 3 horas

---

#### 2️⃣ QA Ajustes (4 horas)
Validación funcional completa del módulo Ajustes

---

#### 3️⃣ Documentación Técnica (1 hora)
- Actualizar `/docs/refactor/01_PROJECT_STATUS.md`
- Crear `/docs/refactor/11_SECURITY.md`
- Actualizar `/docs/refactor/07_KNOWN_ISSUES.md`

**Total Semana 3**: 3 + 4 + 1 = 8 horas

---

## 📋 SEMANA 4: RELEASE (2 horas)

### Objetivo: Publicar v3.0 RC1

#### 1️⃣ Release Checks (1 hora)
- [ ] Todos los fixes en main
- [ ] Tests pasan
- [ ] npm audit = 0 vulnerabilidades
- [ ] Versión = 3.0.0-rc.1

---

#### 2️⃣ Publicar (1 hora)
- [ ] Crear tag v3.0.0-rc.1
- [ ] Build final (macOS + Windows)
- [ ] Generar RELEASE_NOTES.md con security fixes
- [ ] Publicar en repositorio

**Total Semana 4**: 2 horas

---

## 🎯 RESUMEN SEMANAL

| Semana | Focus | Horas | Estado |
|--------|-------|-------|--------|
| **1** | 4 Security fixes | 7h | Security |
|  | QA Dashboard | 4h | QA |
| **2** | Unit tests | 4h | Testing |
|  | E2E tests | 4h | Testing |
|  | QA IA | 4h | QA |
| **3** | Input validation | 3h | Quality |
|  | QA Ajustes | 4h | QA |
|  | Documentation | 1h | Docs |
| **4** | Release checks | 1h | Release |
|  | Publish RC1 | 1h | Release |
| **TOTAL** | | **33 horas** | ✅ |

---

## 🔧 DEPENDENCIAS A AGREGAR

```bash
npm install keytar node-schedule winston
npm install --save-dev vitest @vitest/coverage-v8 @playwright/test
```

**En package.json**:
```json
{
  "dependencies": {
    "keytar": "^7.9.0",
    "node-schedule": "^2.1.1",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "vitest": "^1.0.0",
    "@vitest/coverage-v8": "^1.0.0",
    "@playwright/test": "^1.40.0"
  }
}
```

---

## 📅 CALENDARIO ESPECÍFICO

### Semana 1 (1-7 de julio)
```
LUN 1/7:  Kick-off, SEC-001 (XSS fix) - 2h
MAR 2/7:  SEC-002 (API keys) - 2h
MIÉ 3/7:  SEC-003 (Backups) - 1h
JUE 4/7:  SEC-004 (Logging) - 2h
VIE 5/7:  QA Dashboard - 4h
FIN 6-7:  Testing manual

TOTAL: 11h ✅
```

### Semana 2 (8-14 de julio)
```
LUN 8/7:   Setup Vitest - 1h
MAR-MIÉ 9-10/7: Unit tests - 4h
JUE-VIE 11-12/7: E2E tests - 4h
TODO:     QA IA paralelo - 4h

TOTAL: 12h ✅
```

### Semana 3 (15-21 de julio)
```
LUN 15/7:  Input validation - 3h
MAR-VIE 16-19/7: QA Ajustes - 4h
VIE 19/7:  Documentación - 1h
FIN 20-21: Testing final

TOTAL: 8h ✅
```

### Semana 4 (22-28 de julio)
```
LUN 22/7: Release checks, build final - 1h
MAR 23/7: Publicar v3.0 RC1 - 1h
MIÉ+ 24+: Buffer/ajustes/pruebas

TOTAL: 2h ✅
```

---

## ✅ DEFINICIÓN DE ÉXITO

### Por Semana

**Semana 1**:
- ✅ 0 instancias de innerHTML sin escapar
- ✅ API keys encriptadas en sistema operativo
- ✅ Backups creándose automáticamente
- ✅ Logs siendo guardados en userData/logs/

**Semana 2**:
- ✅ 10+ tests unitarios pasando
- ✅ 5+ E2E tests pasando
- ✅ Coverage >30% en db.js

**Semana 3**:
- ✅ Validación en preload rechaza inputs inválidos
- ✅ Dashboard 100% funcional
- ✅ IA 100% funcional
- ✅ Ajustes 100% funcional

**Semana 4**:
- ✅ v3.0.0-rc.1 publicado
- ✅ 0 vulnerabilidades en npm audit
- ✅ Release notes con security fixes

---

## 🚨 RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|-----------|
| Los fixes rompen funcionalidad | Media | Tests exhaustivos después de cada cambio |
| Keytar no funciona en Windows | Baja | Testing en ambos OS |
| Tests toman más de lo planeado | Media | Buffer de 2 horas en Semana 4 |
| Falta tiempo en Semana 1 | Baja | Paralelizar QA Dashboard |

---

## 📊 MÉTRICAS DE ÉXITO

### Antes de Opción B:
```
Vulnerabilidades: 27
Tests: 0
Documentación: 30%
Puntuación: 7.5/10
```

### Después de Opción B (Target):
```
Vulnerabilidades: 0 (críticas fijas)
Tests: 20+
Documentación: 60%
Puntuación: 8.5/10
```

---

## 📞 CONTACTO Y ESCALACIÓN

Si en cualquier semana hay bloqueos:

1. **Semana 1**: Revisar ISSUES_FOUND.md (SEC-001 a SEC-004)
2. **Semana 2**: Revisar TOOLS_AND_SETUP.md (testing setup)
3. **Semana 3**: Revisar DOCS_UPDATE_PLAN.md (documentación)
4. **Semana 4**: Revisar RELEASE_CHECKLIST

---

## 🎯 PRÓXIMO PASO INMEDIATO

**AHORA (antes de las 18:00 hoy)**:
1. Comunicar decisión al equipo
2. Crear milestone en GitHub: "v3.0 RC1 - Security"
3. Asignar tareas a desarrolladores
4. Hacer kick-off meeting

**MAÑANA**:
1. Comenzar SEC-001 (Fix XSS)
2. Setup de Semana 1

---

**Plan creado**: 1 de julio de 2026  
**Duración total**: 33 horas en 4 semanas  
**Target**: v3.0.0-rc.1 seguro y testeado

¿Listo para comenzar Semana 1? 🚀

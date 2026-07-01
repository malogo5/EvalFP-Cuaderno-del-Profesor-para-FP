# 📝 PLAN DE ACTUALIZACIÓN: Docs Existentes

**Objetivo**: Integrar hallazgos de auditoría de seguridad en `/docs/refactor/`

---

## 📄 ARCHIVOS A ACTUALIZAR

### 1. `01_PROJECT_STATUS.md` - ACTUALIZAR

**Cambios recomendados**:

#### Antes:
```markdown
## Estado general

**Versión actual:** 3.0 Beta
**Estado:** Fase de estabilización (QA)
**Arquitectura:** Modular (completada)
```

#### Después:
```markdown
## Estado general

**Versión actual:** 3.0 Beta
**Estado:** Fase de estabilización (QA) + SECURITY AUDIT REQUERIDO
**Arquitectura:** Modular (completada) ✅
**Seguridad:** 6.5/10 ⚠️ (Auditoría: 01/07/2026)
```

---

#### Antes:
```markdown
## Estado de los módulos

| Módulo | Estado |
|---------|---------|
| Arquitectura | ✅ Finalizada |
| Programación | 🟡 Funcional (pendiente rediseño) |
```

#### Después:
```markdown
## Estado de los módulos (Funcional)

| Módulo | Funcional | Seguridad | QA Automatizado |
|---------|-----------|-----------|-----------------|
| Arquitectura | ✅ Finalizada | ✅ | ❌ |
| Programación | 🟡 90% | 🔴 XSS | ❌ |
| Alumnos | ✅ 100% | ⚠️ | ❌ |
| Actividades | ✅ 100% | ✅ | ❌ |
| Notas | ✅ 100% | ⚠️ | ❌ |
| Dashboard | 🟡 60% | ❌ | ❌ |
| IA | 🟡 50% | ❌ | ❌ |
| Ajustes | 🟡 70% | 🔴 Keys | ❌ |
```

---

#### Agregar nueva sección:
```markdown
## Resultados de Auditoría de Seguridad (01/07/2026)

### Hallazgos Críticos
- 🔴 XSS vulnerability en modulos.js, programacion.js, notas.js
- 🔴 API keys almacenadas en texto plano
- 🔴 Sin backups automáticos
- 🔴 Sin logging de errores

### Hallazgos Importantes
- 🟡 Sin validación de entrada en preload
- 🟡 Sin validación de argumentos spawn()
- 🟡 Race conditions en saveAlumno
- 🟡 Módulo programacion.js muy grande (729 líneas)

### Acción Requerida
Ver: `/AUDIT_REPORT.md`, `/ISSUES_FOUND.md`, `/TOOLS_AND_SETUP.md`
```

---

### 2. `07_KNOWN_ISSUES.md` - EXPANDIR

**Agregar nueva sección**:

```markdown
---

# SECURITY ISSUES (01/07/2026 Audit)

## SEC-001: XSS en renderModulos()
**Ubicación**: renderer/js/modules/modulos.js (líneas 11-22)
**Severidad**: 🔴 CRÍTICA
**Tipo**: Cross-Site Scripting
**Descripción**: Los datos no se escapan en innerHTML
**Ejemplo**: Nombre con `<img src=x onerror="alert('XSS')">`
**Solución**: Usar función esc() en todos los datos
**Esfuerzo**: 2 horas
**Roadmap**: v3.0 (antes de RC1)

## SEC-002: API Keys sin encripción
**Ubicación**: main.js (líneas 48-53), ajustes.js
**Severidad**: 🔴 CRÍTICA
**Tipo**: Almacenamiento inseguro de secretos
**Descripción**: Claves API en texto plano en SQLite
**Riesgo**: Acceso no autorizado a OpenAI/Anthropic
**Solución**: Usar librería keytar
**Esfuerzo**: 2 horas
**Roadmap**: v3.0 (antes de RC1)

## SEC-003: Sin backups automáticos
**Ubicación**: main.js
**Severidad**: 🔴 CRÍTICA
**Tipo**: Pérdida de datos
**Descripción**: No hay respaldos automáticos
**Riesgo**: Pérdida catastrófica de todos los datos
**Solución**: Implementar backups con node-schedule
**Esfuerzo**: 1 hora
**Roadmap**: v3.0 (antes de RC1)

## SEC-004: Sin logging de errores
**Ubicación**: Múltiples archivos
**Severidad**: 🔴 CRÍTICA
**Tipo**: Manejo de errores deficiente
**Descripción**: try/catch silenciosos sin logging
**Impacto**: Imposible debuggear problemas
**Solución**: Logging centralizado con winston
**Esfuerzo**: 2 horas
**Roadmap**: v3.0 (antes de RC1)

## SEC-005: Sin validación en preload
**Ubicación**: preload.js
**Severidad**: 🟡 IMPORTANTE
**Tipo**: Falta de validación de entrada
**Solución**: Validar parámetros antes de IPC
**Esfuerzo**: 2 horas
**Roadmap**: v3.0 RC1

[... más security issues ...]
```

---

### 3. `06_QA.md` - TRANSFORMAR

**De QA Manual a QA Completo**:

#### Antes:
```markdown
## Programación

- [x] Guardado
- [x] Persistencia
- [x] Horas UT
```

#### Después:
```markdown
## Programación

### Funcional (Manual)
- [x] Guardado
- [x] Persistencia
- [x] Horas UT
- [x] Añadir UT
- [x] Eliminar UT
- [ ] Cambio del número de evaluaciones

### Seguridad
- [ ] XSS protection (SEC-001)
- [x] SQL Injection (prepared statements)
- [ ] Input validation
- [ ] Logging

### Automatizado
- [ ] Unit tests (db.js)
- [ ] E2E tests (main workflow)
- [ ] Coverage (target: 50%)
```

---

### 4. Crear `11_SECURITY.md` - NUEVO

```markdown
# Seguridad

## Auditoría Realizada
**Fecha**: 01/07/2026
**Duración**: 3 horas de análisis exhaustivo
**Documentación**: /AUDIT_REPORT.md

## Puntuación: 7.5/10 ⚠️

| Aspecto | Puntuación | Estado |
|---------|-----------|--------|
| Seguridad general | 6.5/10 | ⚠️ |
| Electron config | 10/10 | ✅ |
| SQL Injection | 10/10 | ✅ |
| XSS | 2/10 | 🔴 |
| Secrets | 1/10 | 🔴 |

## Hallazgos Críticos (Resolver ASAP)

### 1. XSS Vulnerability (2 horas)
- Ubicación: modulos.js, programacion.js, notas.js
- Solución: Usar esc() en innerHTML

### 2. API Keys sin encripción (2 horas)
- Ubicación: main.js, ajustes.js
- Solución: Usar keytar

### 3. Sin backups (1 hora)
- Ubicación: Toda la app
- Solución: node-schedule

### 4. Sin logging (2 horas)
- Ubicación: Múltiples try/catch
- Solución: winston logger

## Hallazgos Importantes (Próximas 2 semanas)

### 5. Sin validación en preload
### 6. Sin validación de spawn()
### 7. Race conditions
### 8. Módulo muy grande
### 9. Sin tests

## Timeline Recomendado

- **Semana 1**: Críticos (7h)
- **Semana 2-3**: Importantes (11h)
- **Mes 2**: Testing y docs (36h)

## Próximos pasos

- [ ] Implementar 4 fixes críticos
- [ ] Agregar tests básicos
- [ ] Documentar API IPC
- [ ] Setup CI/CD
```

---

### 5. `03_ROADMAP.md` - ACTUALIZAR CON SEGURIDAD

#### Antes:
```markdown
## Versión 3.0

Objetivo:
Finalizar la estabilización y publicar RC1

Pendiente:
- QA completo
- Dashboard
- IA
- Ajustes
```

#### Después:
```markdown
## Versión 3.0

**Duración**: 4 semanas (24 + 20 horas)

### Fase 1: Security (Semana 1)
**Esfuerzo**: 7 horas
- [ ] Fix XSS (2h)
- [ ] Encriptar API keys (2h)
- [ ] Backups automáticos (1h)
- [ ] Logging (2h)

### Fase 2: QA + Testing (Semanas 2-3)
**Esfuerzo**: 11 + 16 horas
- [ ] QA Dashboard, IA, Ajustes
- [ ] Unit tests (db.js)
- [ ] E2E tests
- [ ] Validación de entrada

### Fase 3: Documentación (Semana 3-4)
**Esfuerzo**: 6 horas
- [ ] README con guía de seguridad
- [ ] API IPC documentation
- [ ] CONTRIBUTING.md
- [ ] SECURITY.md

### Fase 4: Release (Semana 4)
- [ ] v3.0 RC1 + Security report

### Fases posteriores: Testing + Docs (20 horas)
- CI/CD pipeline
- Full test coverage
- Documentación técnica completa
```

---

### 6. `05_SPRINTS.md` - REPLANIFICAR

#### Antes:
```markdown
## Sprint 3
Estabilización y QA
Estado: En curso
```

#### Después:
```markdown
## Sprint 3: Estabilización + Seguridad
**Duración**: 4 semanas
**Estado**: En curso (replanificado 01/07/2026)

### Semana 1: Security + QA Dashboard
- [ ] Fix XSS (2h)
- [ ] Encriptar API keys (2h)
- [ ] Backups (1h)
- [ ] Logging (2h)
- [ ] QA Dashboard (4h)
**Total**: 11h

### Semana 2: Testing + QA IA
- [ ] Unit tests (4h)
- [ ] E2E tests (4h)
- [ ] QA IA (4h)
**Total**: 12h

### Semana 3: Validación + QA Ajustes
- [ ] Input validation (2h)
- [ ] Argument sanitization (1h)
- [ ] Fix race conditions (2h)
- [ ] QA Ajustes (4h)
- [ ] Documentación (2h)
**Total**: 11h

### Semana 4: Release Prep
- [ ] Security review final (2h)
- [ ] Release notes (1h)
- [ ] v3.0 RC1 (2h)
**Total**: 5h

**Sprint 3 Total**: ~40 horas

---

## Sprint 4: Refinamiento + Docs
**Duración**: 4 semanas
**Planificado**: Después de RC1

### Semana 1-2: Testing
- [ ] Aumentar coverage a 80%
- [ ] Más E2E tests

### Semana 3-4: Documentación
- [ ] CONTRIBUTING.md
- [ ] API documentation
- [ ] Security guidelines
```

---

### 7. `04_EPICS.md` - AGREGAR ÉPICAS DE SEGURIDAD

```markdown
# Epics

## EPIC-001
Rediseño del Plan de Evaluación
Versión: 3.1

## EPIC-002
Rediseño del módulo IA
Versión: 3.1

---

## EPIC-003 (NUEVO - 01/07/2026)
Seguridad y Testing

### Stories
- SEC-001: Fix XSS
- SEC-002: Encriptar API keys
- SEC-003: Backups automáticos
- SEC-004: Logging centralizado
- TEST-001: Unit tests
- TEST-002: E2E tests
- TEST-003: CI/CD pipeline

Versión: 3.0 (CRÍTICO)
Prioridad: MÁXIMA
```

---

### 8. `08_DECISIONS.md` - AGREGAR DECISIONES DE SEGURIDAD

```markdown
# Decisiones de Arquitectura

## ADR-001
Decisión: No corregir mediante parche el cambio del número de evaluaciones
Motivación: Requiere rediseño completo
Consecuencia: v3.1

---

## ADR-002 (NUEVO - 01/07/2026)
**Fecha**: 01/07/2026

**Decisión**: Priorizar fixes de seguridad ANTES de RC1

**Motivación**:
- 4 vulnerabilidades críticas identificadas
- Riesgo de exposición de datos
- Claves API sin protección

**Consecuencia**:
- +7 horas de trabajo en Sprint 3
- Retraso de RC1: +1 semana (se publica en Semana 4 en lugar de Semana 3)
- Pero v3.0 se publica con seguridad garantizada

**Alternativa rechazada**:
- Publicar RC1 sin seguridad (riesgo CRÍTICO)

---

## ADR-003 (NUEVO - 01/07/2026)
**Fecha**: 01/07/2026

**Decisión**: Implementar testing automatizado a partir de v3.0

**Motivación**:
- QA manual no detectó vulnerabilidades de seguridad
- Sin tests automatizados no se puede garantizar calidad
- Sin CI/CD no hay forma de validar cambios

**Consecuencia**:
- +16 horas de trabajo en Sprint 3
- Pero v3.0 RC1 tendrá base de tests
- v3.1+ serán más seguros

---

## ADR-004 (NUEVO - 01/07/2026)
**Fecha**: 01/07/2026

**Decisión**: Usar keytar para encriptación de API keys

**Motivación**:
- Keys en texto plano es inaceptable
- keytar es estándar de Electron
- Se integra con sistema operativo (Keychain/Credential Manager)

**Consecuencia**:
- Dependencia adicional: keytar
- Mejor seguridad en producción
- Compatible con macOS, Windows, Linux
```

---

## 📝 RESUMEN DE CAMBIOS

| Archivo | Tipo | Cambio |
|---------|------|--------|
| 01_PROJECT_STATUS.md | Actualizar | Agregar security status |
| 03_ROADMAP.md | Actualizar | Incluir security phases |
| 04_EPICS.md | Expandir | Agregar EPIC-003 |
| 05_SPRINTS.md | Replanificar | Integrar security work |
| 06_QA.md | Transformar | Agregar security QA |
| 07_KNOWN_ISSUES.md | Expandir | Agregar security issues |
| 08_DECISIONS.md | Expandir | Agregar ADR 02-04 |
| 09_CHANGELOG.md | Actualizar | Agregar security fixes |
| 11_SECURITY.md | CREAR | Documentación de seguridad |

---

## 🎯 ACCIÓN INMEDIATA

### HOY:
1. [ ] Copiar AUDIT_REPORT.md a /docs/
2. [ ] Copiar ISSUES_FOUND.md a /docs/
3. [ ] Crear 11_SECURITY.md en /docs/refactor/
4. [ ] Actualizar 01_PROJECT_STATUS.md
5. [ ] Actualizar 07_KNOWN_ISSUES.md

### ANTES DE SPRINT 3:
1. [ ] Actualizar 03_ROADMAP.md
2. [ ] Replanificar 05_SPRINTS.md
3. [ ] Expandir 04_EPICS.md
4. [ ] Agregar ADRs a 08_DECISIONS.md

### DESPUÉS DE IMPLEMENTAR FIXES:
1. [ ] Actualizar 06_QA.md con resultados
2. [ ] Actualizar 09_CHANGELOG.md
3. [ ] Publicar 10_RELEASES.md

---

**Última actualización**: 1 de julio de 2026  
**Para**: Integración de auditoría de seguridad en documentación existente

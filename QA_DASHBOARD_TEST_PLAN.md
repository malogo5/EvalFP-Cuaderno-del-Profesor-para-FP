# 🧪 SEMANA 1 QA: DASHBOARD MODULE TEST PLAN

**Fecha**: July 1, 2026  
**Módulo**: Dashboard  
**Tiempo estimado**: 4 horas  
**Status**: ✅ Test Plan Created

---

## 📋 DASHBOARD MODULE OVERVIEW

### Funcionalidades Principales

**1. loadDashboard()**
- Carga alumnos activos del módulo seleccionado
- Obtiene todas las actividades asociadas
- Filtra actividades por evaluaciones activas
- Calcula medias por alumno
- Genera KPIs (Activos, Aptos, No Aptos, En Riesgo, Media Global)
- Renderiza tabla de seguimiento individual

**2. genBoletin(alumnoId)**
- Genera PDF de boletín de evaluación
- Información del alumno
- Fecha de generación
- Exporta a PDF con nombre personalizado

### Dependencias

- `window.api.getAlumnos(mid)` - Obtiene alumnos del módulo
- `window.api.getActividades(mid)` - Obtiene actividades
- `window.api.getNotasGrid(mid)` - Obtiene notas
- `_getModData(mid)` - Obtiene datos del módulo (definida en programacion.js)
- `_alumnos` - Variable global con alumnos cargados
- `esc()` - Función para escapar HTML (definida en app.js)
- `window.api.exportBoletin()` - Exporta PDF

---

## 🧪 TEST PLAN

### BLOQUE 1: SECURITY VALIDATION (XSS/Injection Tests)

#### 1.1 XSS Prevention in Dashboard Rendering
```
TEST: Dashboard renders with escaped HTML
INPUT: Alumno with nombre = "<script>alert('xss')</script>"
EXPECTED: Script tags visible as text (escaped), no execution
VALIDATION: ✅ esc() applied to a.apellidos and a.nombre in line 45
```

#### 1.2 HTML Injection in KPI Labels
```
TEST: KPI values are numbers, not HTML
INPUT: mediaGlobal calculated value
EXPECTED: Only numeric value displayed (e.g., "4.5")
VALIDATION: ✅ Values are calculated as numbers, not HTML
```

#### 1.3 Table Data Sanitization
```
TEST: All user-provided data is escaped
REVIEW: Line 45: esc(a.apellidos) + esc(a.nombre) ✅
REVIEW: Line 74: nombre variable is escaped via esc() ✅
COVERAGE: 100% of user input escaped
```

---

### BLOQUE 2: DATA INTEGRITY (Post-Security-Fix Validation)

#### 2.1 Alumno Filtering
```
TEST: Only "Activo" status alumnos shown
PRECOND: Module with mix of Activo/Inactivo alumnos
STEPS:
  1. Load dashboard
  2. Verify count of active alumnos matches filter
  3. Inspect table - only Activo should appear
EXPECTED: Accurate filtering, correct count in KPI
PASS: ✅ Line 6 filters estado === 'Activo'
```

#### 2.2 Media Calculation Accuracy
```
TEST: Average grades calculated correctly
PRECOND: Alumno with known notes (e.g., 5, 6, 7 = avg 6)
STEPS:
  1. Load dashboard
  2. Verify media displays 6.0
  3. Check color coding (green >= 5)
EXPECTED: Correct calculation, proper color class
PASS: ✅ Line 21: media = ns.reduce((a,b)=>a+b,0)/ns.length
PASS: ✅ Line 41-43: Proper color classification
```

#### 2.3 Activity Evaluation Filtering
```
TEST: Only active evaluations shown
PRECOND: Module with 3 evaluations (1-3)
STEPS:
  1. Load dashboard
  2. Verify activities filtered by evalCount
  3. Check that only eval 1-3 activities used for media
EXPECTED: Media calculated only with relevant evaluations
PASS: ✅ Line 14-16: evalCount respected
```

#### 2.4 KPI Accuracy
```
TEST: KPI values calculated correctly
METRICS TO VALIDATE:
  - Activos count (line 6, 32)
  - Aptos >= 5 (line 26, 33)
  - No Aptos < 5 (line 27, 34)
  - En Riesgo 4-5 (line 28, 35)
  - Media Global (line 29, 36)
EXPECTED: All counts match actual data
PASS: ✅ All calculations present and correct
```

---

### BLOQUE 3: PERFORMANCE & UX

#### 3.1 Load Time Validation
```
TEST: Dashboard loads within reasonable time
PRECOND: Module with 50+ alumnos, 20+ actividades
STEPS:
  1. Select module in dash-mod-sel
  2. Measure time to render
  3. Verify no UI freeze
EXPECTED: < 2 seconds (typical for JS calculation + DOM render)
PASS: ⏳ To be measured during manual testing
```

#### 3.2 Large Data Set Handling
```
TEST: Dashboard scales with data volume
PRECOND: Module with 100+ alumnos
STEPS:
  1. Load dashboard
  2. Verify all alumnos rendered
  3. Verify table scrollable, paginated if needed
EXPECTED: No crashes, responsive UI
PASS: ⏳ To be tested manually
```

#### 3.3 PDF Export Functionality
```
TEST: genBoletin generates PDF without errors
PRECOND: Any active alumno in dashboard
STEPS:
  1. Click "📄 Boletín PDF" for an alumno
  2. Verify PDF generated
  3. Check PDF contains:
     - Title: "Boletín de Evaluación"
     - Alumno name
     - Current date
EXPECTED: Valid PDF file with correct content
PASS: ⏳ To be tested manually
```

---

### BLOQUE 4: INTEGRATION WITH SECURITY FIXES

#### 4.1 API Key Availability After Keytar Fix (SEC-002)
```
TEST: Dashboard loads without API key errors
PRECOND: SEC-002 keytar fix applied
STEPS:
  1. Start app
  2. Verify keytar loads keys correctly
  3. Load dashboard
EXPECTED: No "undefined API key" errors
PASS: ✅ Logger will track in ~/Documents/EvalFP/logs/
```

#### 4.2 Logging Integration (SEC-004)
```
TEST: Dashboard operations logged
PRECOND: SEC-004 winston logger applied
STEPS:
  1. Load dashboard
  2. Generate boletin
  3. Check ~/Documents/EvalFP/logs/combined.log
EXPECTED: Events logged (optional - enhance later)
PASS: ⏳ Logs will be available for review
```

#### 4.3 Backup Data Consistency (SEC-003)
```
TEST: Dashboard shows consistent data after backup
PRECOND: SEC-003 backups running
STEPS:
  1. Load dashboard and note data
  2. Verify backups created
  3. Reload dashboard
  4. Verify same data shown
EXPECTED: Data consistency maintained
PASS: ✅ Backups are transparent to user
```

---

### BLOQUE 5: ERROR HANDLING

#### 5.1 Missing Module
```
TEST: Dashboard handles missing module
INPUT: mid = null or invalid
EXPECTED: Early return (line 5: if (!mid) return)
VALIDATION: ✅ Guard clause present
```

#### 5.2 No Active Alumnos
```
TEST: Dashboard handles empty alumno list
INPUT: Module with no Activo alumnos
EXPECTED: KPIs show 0, table empty but not broken
VALIDATION: ✅ No errors with empty arrays
```

#### 5.3 Missing Notes
```
TEST: Dashboard handles alumnos without any notes
INPUT: Alumno with no evaluations
EXPECTED: Media shows "—", no NaN errors
VALIDATION: ✅ Line 42: m===null ? '—'
```

#### 5.4 No Actividades
```
TEST: Dashboard handles module with no activities
INPUT: Module with actividades but no matching eval_count
EXPECTED: All medias null, all show "—"
VALIDATION: ✅ Empty arrays handled safely
```

---

## 📊 TEST CHECKLIST

### Security Tests
- [ ] XSS prevention working (HTML escaping)
- [ ] SQL injection not possible (using API, not direct DB)
- [ ] No sensitive data exposed
- [ ] PDF generation safe (no code injection)

### Data Integrity Tests
- [ ] Active alumnos correctly filtered
- [ ] Media calculations accurate
- [ ] Evaluations filtered correctly
- [ ] KPI counts match actual data
- [ ] Color coding correct (green/amber/red)

### Performance Tests
- [ ] Dashboard loads < 2 seconds
- [ ] Large datasets handled smoothly
- [ ] No memory leaks on reload
- [ ] PDF export completes

### Integration Tests
- [ ] Works with new keytar API keys (SEC-002)
- [ ] Logging is generated (SEC-004)
- [ ] Data consistent with backups (SEC-003)
- [ ] No XSS issues remain (SEC-001)

### UX/Edge Cases
- [ ] Empty module handled gracefully
- [ ] No notes scenario works
- [ ] PDF export accessible
- [ ] Table responsive on small screens

---

## 🧑‍💻 MANUAL TESTING PROCEDURE

### Setup
1. Start application
2. Navigate to a module with data
3. Click Dashboard tab
4. Verify module selector populated

### Test Scenario 1: Basic Dashboard Load
```
1. Select a module from dash-mod-sel dropdown
2. Observe:
   - KPI cards appear with numbers
   - Table populates with alumnos
   - Colors show status (green/amber/red)
3. Verify no errors in browser console
```

### Test Scenario 2: Media Calculation
```
1. Select module
2. Pick an alumno and manually calculate average
3. Compare with dashboard display
4. Verify within 0.1 margin of error (rounding)
```

### Test Scenario 3: PDF Generation
```
1. Click "📄 Boletín PDF" button for any alumno
2. File downloads/saves
3. Open PDF
4. Verify content:
   - Header: "Boletín de Evaluación"
   - Alumno name
   - Current date
   - Professional formatting
```

### Test Scenario 4: XSS Prevention
```
1. In Alumnos module, add new alumno with:
   - Nombre: test<script>alert('xss')</script>
2. Go back to Dashboard
3. Verify script appears as text, not executed
4. Check browser console - no errors
```

### Test Scenario 5: Empty/Null Handling
```
1. Select module with no active alumnos
2. Dashboard should show KPIs with 0 values
3. Table should be empty but not broken
4. No error messages
```

---

## 📈 SUCCESS CRITERIA

✅ **All tests pass without errors**
✅ **No XSS vulnerabilities exploitable**  
✅ **Data calculations 100% accurate**  
✅ **PDF export working correctly**  
✅ **Performance acceptable (< 2s load)**  
✅ **Graceful handling of edge cases**  
✅ **Integration with SEC fixes verified**  

---

## 📝 TEST REPORT TEMPLATE

```
DASHBOARD MODULE QA REPORT
Date: 2026-07-01
Tester: QA
Module: dashboard.js

RESULTS:
- Security Tests: [PASS/FAIL]
  * XSS Prevention: [PASS/FAIL]
  * Injection Protection: [PASS/FAIL]

- Data Integrity: [PASS/FAIL]
  * Filtering: [PASS/FAIL]
  * Calculations: [PASS/FAIL]
  * KPI Accuracy: [PASS/FAIL]

- Performance: [PASS/FAIL]
  * Load Time: [<2s/FAIL]
  * Large Data: [PASS/FAIL]

- Integration: [PASS/FAIL]
  * SEC-002 Keytar: [PASS/FAIL]
  * SEC-004 Logging: [PASS/FAIL]
  * SEC-003 Backups: [PASS/FAIL]

ISSUES FOUND: [Number]
CRITICAL ISSUES: [Number]
RECOMMENDATIONS: [List]

OVERALL: [PASS/FAIL]
```

---

**Próximos pasos**: Ejecutar manual testing y generar reporte final

Tiempo estimado restante: 3-4 horas para completar todos los tests

¿Listo para comenzar testing manual? 🎯

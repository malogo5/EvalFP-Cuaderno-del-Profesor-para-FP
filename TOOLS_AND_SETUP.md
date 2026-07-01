# 🛠️ Herramientas Recomendadas para EvalFP

## Seguridad

### Obligatorias

#### 1. **keytar** - Encriptación de secretos
```bash
npm install keytar
```
**Para**: Encriptar claves API  
**Uso**: Almacenar OPENAI_API_KEY y ANTHROPIC_API_KEY de forma segura

#### 2. **electron-builder** ✅ (Ya instalado)
**Para**: Compilar app con firmado seguro

#### 3. **snyk** - Auditoría de vulnerabilidades
```bash
npm install -g snyk
snyk test
```

---

## Testing

### Unitarias
```bash
npm install --save-dev vitest @vitest/coverage-v8
```

### E2E
```bash
npm install --save-dev @playwright/test
```

### Mock/Fixtures
```bash
npm install --save-dev sinon
```

---

## Código Quality

### ESLint
```bash
npm install --save-dev eslint eslint-config-airbnb-base eslint-plugin-import
npx eslint --init
```

### Prettier
```bash
npm install --save-dev prettier
```

### Pre-commit hooks
```bash
npm install --save-dev husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

**package.json**:
```json
{
  "lint-staged": {
    "*.js": ["eslint --fix", "prettier --write"],
    "*.html": ["prettier --write"],
    "*.css": ["prettier --write"]
  }
}
```

---

## Logging & Monitoring

### node-schedule (Para backups)
```bash
npm install node-schedule
```

### winston (Logging profesional)
```bash
npm install winston
```

---

## Estructura de carpetas recomendada

```
evalfp/
├── src/
│   ├── main/
│   │   ├── main.js
│   │   ├── ipc.js
│   │   ├── logger.js
│   │   └── validators.js
│   ├── preload.js
│   ├── db.js
│   └── renderer/
│       ├── index.html
│       ├── css/
│       ├── js/
│       │   ├── app.js
│       │   └── modules/
│       │       ├── modulos.js
│       │       ├── alumnos.js
│       │       ├── notas.js
│       │       └── ...
│       └── utils/
│           └── validators.js
├── tests/
│   ├── unit/
│   │   └── db.test.js
│   └── e2e/
│       └── app.test.js
├── .eslintrc.js
├── .prettierrc
├── jest.config.js
├── package.json
└── README.md
```

---

## Scripts de package.json

```json
{
  "scripts": {
    "start": "electron .",
    "dev": "electron . --dev",
    "build:mac": "electron-builder --mac",
    "build:win": "electron-builder --win",
    "build": "npm run build:mac && npm run build:win",
    "test": "vitest",
    "test:e2e": "playwright test",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write .",
    "prebuild": "npm run lint && npm run test",
    "security": "snyk test"
  }
}
```

---

## CI/CD Pipeline (GitHub Actions)

**.github/workflows/security.yml**:
```yaml
name: Security

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '22'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run snyk
        run: npx snyk test
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Run E2E tests
        run: npm run test:e2e
```

---

## Checklist de Seguridad

### Antes de cada release

- [ ] `npm audit` sin vulnerabilidades
- [ ] `snyk test` sin issues
- [ ] ESLint sin warnings
- [ ] Tests pasen (100% de código crítico)
- [ ] XSS check: Todos los datos escapados
- [ ] SQL Injection: Todas las queries usan prepared statements
- [ ] API Keys: Almacenadas con keytar
- [ ] Backups: Verificar que se crean diariamente
- [ ] Logging: Revisar logs de error
- [ ] Dependencias: Actualizar si hay security patches

### Desarrollo

- [ ] Correr `npm run lint:fix` antes de commit
- [ ] Correr `npm test` antes de push
- [ ] Revisar cambios de db.js (riesgos de SQL injection)
- [ ] Revisar cambios en renderer (riesgos de XSS)
- [ ] Validar todas las nuevas entradas de usuario

---

## Documentos a Crear

### README.md
```markdown
# EvalFP v3.0.0

Cuaderno digital del profesor para Formación Profesional

## Instalación

npm install
npm start

## Desarrollo

npm run dev

## Testing

npm test

## Building

npm run build

## Seguridad

Esta aplicación maneja datos educativos sensibles.
- Claves API: Encriptadas con keytar
- Datos: Almacenados localmente en SQLite
- Backups: Automáticos cada día a las 2 AM

Ver SECURITY.md para más detalles.
```

### CONTRIBUTING.md
```markdown
# Contribuir a EvalFP

1. Fork el repo
2. Crea rama: git checkout -b feature/nombre
3. Haz cambios
4. Corre tests: npm test
5. Corre linter: npm run lint
6. Commit: git commit -am "Descripción"
7. Push: git push origin feature/nombre
8. Abre Pull Request

## Código de conducta

Sé respetuoso y constructivo.
```

### SECURITY.md
```markdown
# Seguridad en EvalFP

## Vulnerabilidades

Para reportar vulnerabilidades, NO las publiques públicamente.
Envía email a: [contact email]

## Prácticas de seguridad

1. Claves API se almacenan encriptadas
2. Todos los datos de entrada se validan
3. No ejecutamos código arbitrario
4. Backups automáticos cada día
5. Base de datos con foreign keys

Ver AUDIT_REPORT.md para auditoría completa.
```

---

## Comandos Útiles

### Desarrollo
```bash
npm start              # Ejecutar app
npm run dev           # Modo desarrollo
npm test              # Ejecutar tests
npm run lint          # Verificar código
npm run format        # Formatear código
```

### Seguridad
```bash
npm audit             # Auditar dependencias
npm run security      # Ejecutar snyk
git log --grep="fix"  # Ver fixes de seguridad
```

### Build
```bash
npm run build         # Compilar para todos OS
npm run build:mac     # Solo macOS
npm run build:win     # Solo Windows
```

---

## Versionado Semántico

Usar semver para versionado:
- **MAJOR**: Cambios incompatibles (3.0.0)
- **MINOR**: Nuevas features compatibles (3.1.0)
- **PATCH**: Bug fixes (3.0.1)

---

## Roadmap de Implementación

### Sprint 1 (2 semanas)
- [ ] Implementar todos los fixes críticos
- [ ] Agregar ESLint + Prettier
- [ ] Setup de tests básicos
- [ ] Documentación README

### Sprint 2 (2 semanas)
- [ ] Cobertura de tests 50%+
- [ ] CI/CD pipeline
- [ ] Refactorizar programacion.js
- [ ] CONTRIBUTING.md

### Sprint 3 (2 semanas)
- [ ] Cobertura de tests 80%+
- [ ] E2E tests
- [ ] Documentación completa
- [ ] Security audit 2.0

---

*Última actualización: 1 de julio de 2026*

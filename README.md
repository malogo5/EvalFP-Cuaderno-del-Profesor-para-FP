# EvalFP — Cuaderno del Profesor para FP

[![Licencia: GPL-3.0-or-later](https://img.shields.io/badge/Licencia-GPL--3.0--or--later-blue.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/versión-3.15.0-orange.svg)](CHANGELOG.md)

EvalFP es una aplicación de escritorio Electron para profesorado de Formación Profesional en España. Gestiona programación didáctica, alumnado, notas, evaluaciones, informes y materiales de apoyo en una base de datos SQLite local, sin backend remoto.

**Versión actual:** 3.15.0 · El historial está en el [CHANGELOG](CHANGELOG.md) y lo que viene, en el [ROADMAP](ROADMAP.md).

## Lo esencial

- Funcionamiento local en macOS y Windows.
- Datos de alumnado guardados solo en tu equipo.
- Motor de módulos ampliable con archivos `*_data.py`.
- Generación opcional de materiales con Python e IA.

## Primeros pasos

1. Instala dependencias.
2. Arranca la app en local.
3. Selecciona o crea un módulo.
4. Importa tu alumnado.
5. Empieza a registrar actividades y notas.

```bash
npm install
npm start
```

Si quieres el flujo completo de instalación y uso, abre [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md).

## Funcionalidades

- Gestión de módulos y grupos.
- Alumnado con edición rápida.
- Registro de notas por actividades y evaluaciones.
- Dashboard y boletines.
- Asistente IA opcional para rúbricas, actividades e informes.
- Generación de instaladores para macOS y Windows.

## Desarrollo y pruebas

```bash
npm run prebake
npm test
npm run test:e2e
npm run lint
npm run build:mac
npm run build:win
```

## Estructura principal

- `main.js`, `preload.js`, `db.js`: núcleo de Electron.
- `renderer/`: interfaz de usuario.
- `scripts/`: generación de módulos, plantilla y asistente IA.
- `docs/`: decisiones, guía de desarrollo y notas técnicas.

## Añadir un módulo

1. Crea un archivo nuevo en `scripts/modules/` siguiendo el patrón de `iso_data.py`.
2. Regístralo en `scripts/teacher_config.py`.
3. Ejecuta `npm run prebake`.
4. Vuelve a abrir la app o genera el instalador.

## Documentación útil

- [docs/guia_desarrollo.md](docs/guia_desarrollo.md)
- [docs/decisiones_arquitectura.md](docs/decisiones_arquitectura.md)
- [docs/casos_uso.md](docs/casos_uso.md)
- [INSTALACION_Y_USO.md](INSTALACION_Y_USO.md) — cómo se usa el cuaderno, para profesorado.
- [AUDITORIA_INTEGRAL.md](AUDITORIA_INTEGRAL.md) — auditoría contra la Orden 201/2024 de CLM.
- [tests/e2e/AUDITORIA_CURSO.md](tests/e2e/AUDITORIA_CURSO.md) — auditoría completa de usuario sobre la app real.

## Licencia

EvalFP se distribuye bajo [GNU GPL v3.0 o posterior](LICENSE).

## Estado del proyecto

El cuaderno está terminado y en uso: catálogo completo de Castilla-La Mancha, motor de
calificación único y siete auditorías cerradas con **83 incidencias** corregidas, todas
cubiertas con pruebas.

### Qué está comprobado
- **Normativa**: Orden 201/2024 de CLM, con la modificación de la Orden 55/2026. La regla de
  oro (todos los RA alcanzados), el redondeo de acta, las dos convocatorias, la renuncia, el
  superado parcial por fase de empresa y los topes de convocatorias.
- **Catálogo**: los 91 módulos se dan de alta sin error, con sus 4.444 criterios literales
  del DOCM y las ponderaciones cuadradas.
- **Motor de calificación**: 13.000 combinaciones al azar contra las reglas de la Orden, sin
  una sola infracción. Todas las pantallas —incluido el boletín— calculan con el mismo motor.
- **Datos de menores**: nada sale del ordenador salvo lo que se manda a la IA, anonimizado y
  con consentimiento explícito en cada pantalla. Las claves de API van al llavero del sistema
  o no se guardan.
- **Aguante**: 6 módulos, 180 matrículas y 8.640 notas sin degradación; un apagón a media
  escritura no corrompe la base.
- **Pruebas**: 151 unitarias con Vitest y extremo a extremo con Playwright.

### Qué queda por validar fuera del código
- Un curso completo con alumnado real, de septiembre a junio.
- La sesión de 2ª convocatoria de junio, que es la única que no se puede ensayar
  (guion en [GUION_2A_CONVOCATORIA.md](GUION_2A_CONVOCATORIA.md)).
- Firmar los instaladores para que macOS y Windows dejen de avisar
  (ver [FIRMA.md](FIRMA.md)).

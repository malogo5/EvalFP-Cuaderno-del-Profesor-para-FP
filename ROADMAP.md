# Hoja de ruta de EvalFP

> **Estado: 3.16.0** — aplicación de escritorio (Electron + SQLite), catálogo alineado con
> la normativa vigente para 2026-27 y siete auditorías cerradas. Agosto de 2026.

El detalle de cada versión está en [CHANGELOG.md](CHANGELOG.md); esto es solo el mapa.

## De dónde viene

EvalFP nació como un **libro de Excel** generado con Python (`build_template.py`), con hojas
de evaluación y apuntes en HTML. Llegó a la versión 2.0.1 y se quedó pequeño: un archivo por
módulo, fórmulas frágiles y ninguna forma decente de programar por criterios.

La versión 3 tiró ese enfoque y rehízo el cuaderno como aplicación de escritorio con base de
datos. De la etapa Excel ya no queda código en el repositorio (agosto de 2026): sigue en el
historial de git, en los commits anteriores a la 3.7.0.

## Dónde está ahora

| Área | Estado |
|---|---|
| Catálogo CLM | **130 módulos** · 12 ciclos · **5.964 CE literales**, verificados uno a uno |
| Motor de calificación | Único, en `renderer/js/core/calificacion.js` |
| Normativa de currículo | Decretos 78, 79 y 80 de 2024 · Decreto 79/2025 (CE de Python) |
| Normativa de evaluación | Orden 201/2024, con la modificación de la Orden 55/2026 |
| Normativa de dualidad | Orden 204/2024 |
| Auditorías | Siete, todas cerradas: 78 incidencias resueltas |
| Convocatorias | 1ª y 2ª unificadas (art. 21.5): la prueba de junio es una actividad más |
| Pruebas | 175 unitarias con Vitest · extremo a extremo con Playwright |
| Distribución | DMG (arm64 + x64) e instalador NSIS para Windows 11 |

## Lo que se cerró en agosto de 2026

La revisión completa está en
[INFORME_DISCREPANCIAS_2026-27.md](INFORME_DISCREPANCIAS_2026-27.md), 16 secciones con
cada decisión y su cita normativa. En resumen:

- **Alineación con los Decretos 78, 79 y 80/2024.** Se corrigieron las horas y el curso de
  los 9 módulos de Gestión Administrativa, único ciclo que estaba desactualizado. ASIR, DAM,
  DAW, AD, AF, SMR, Informática de Oficina y Servicios Administrativos ya estaban bien.
- **Trazabilidad de doble cita** en 78 módulos: de qué decreto salen las horas y de cuál los
  RA y CE, con anexo, número y fecha de DOCM.
- **39 módulos transversales nuevos**: Itinerario Personal para la Empleabilidad I y II,
  Inglés Profesional, Digitalización, Sostenibilidad y Proyecto Intermodular.
- **El CE de Python, reconstruido** con el Decreto 79/2025. Antes tenía códigos inventados
  y RA y CE sin fuente oficial.
- **Cotejo literal de los 5.964 criterios** contra el texto de su decreto: 100 % de
  coincidencia. Repetible con `python3 scripts/normativa/cotejar_ce.py`.
- **Orden 55/2026 implementada**: pérdida de la evaluación continua sin conservar
  calificaciones parciales (art. 3.6), convalidaciones (art. 25.7 y 25.11) y las reglas de
  calificación final, con 24 tests.

Dos cosas que conviene no olvidar, porque se dieron por sabidas y eran falsas:

- La corrección de errores del Decreto 80/2024 **es de febrero de 2025, no de septiembre**,
  y no modifica ninguna hora: solo arregla una remisión cruzada.
- Las 400 horas de formación en empresa de grado básico **salen de dentro** de las 2.000 del
  ciclo, no se suman. El Anexo I ya es la tabla ajustada.

## Pendiente de la próxima entrega

**Reconstruir los instaladores.** Hay cambios en la versión de desarrollo que todavía no
están en el DMG ni en el `.exe`: el icono de Notas, la revisión del catálogo y todo lo de la
Orden 55/2026. Se hace al final, cuando el lote de cambios esté cerrado:

```
npm run build:mac      # en el Mac
npm.cmd run build:win  # en la máquina virtual, tras git pull
```

## Lo siguiente

1. **Probarlo en una 2ª convocatoria de verdad.** El modelo de convocatorias (A-5) está
   implementado y cubierto con pruebas, pero la comprobación que no da ninguna máquina es
   usarlo con un grupo real en junio. El paso a paso de esa sesión, con la copia de
   seguridad primero, está en [GUION_2A_CONVOCATORIA.md](GUION_2A_CONVOCATORIA.md).
2. **Firmar los instaladores.** Requiere comprar certificados: 99 USD al año en Apple —con
   exención posible para centros educativos— y unos 200-350 € al año en Windows, donde
   además el aviso de SmartScreen no desaparece hasta acumular descargas. El proyecto ya
   está preparado para firmar en cuanto haya credenciales: ver [FIRMA.md](FIRMA.md).
3. **La capa de pantallas que falta de la Orden 55/2026**: el informe del anexo VIII
   (continuidad con materias pendientes, art. 18.5) y el anexo X-BIS (resolución de exención
   de la fase de empresa, art. 22.5). El cálculo ya está hecho y probado; falta el documento.

## Lo que queda fuera a propósito

- **Los ámbitos de Grado Básico** (Ciencias Aplicadas y Comunicación y Ciencias Sociales,
  códigos 3161 a 3164) y la **Segunda lengua** (0180) de Asistencia a la Dirección. El
  artículo 9 del Decreto 78/2024 los llama «ámbitos **no profesionales**» y los atribuye a
  otro profesorado. No son módulos de este cuaderno. La calificación cualitativa
  IN/SU/BI/NT/SB (art. 25.2) se queda implementada y probada por si alguna vez hace falta.
- **El proyecto intermodular de grado superior** (0379 ASIR, 0492 DAM, 0616 DAW, 0657 AF,
  0664 AD). El Decreto 80/2024 les asigna 55 horas en su Anexo I pero **no desarrolla sus
  resultados de aprendizaje ni sus criterios de evaluación**, y —a diferencia del 79/2024
  para grado medio y del 78/2024 para el básico— **tampoco remite a ningún Real Decreto**.
  Es una laguna de la norma, no del cuaderno.

  Decisión tomada en agosto de 2026: **no se dan de alta**. La alternativa era redactar el
  currículo por cuenta propia, que es justo lo que la regla del proyecto prohíbe y lo que
  una inspección detectaría. Si algún día hiciera falta impartirlos, el punto de partida
  está documentado en la sección 13 del informe.
- **La calificación final de ciclo y la Matrícula de Honor** como pantalla. Los cuadernos de
  EvalFP son de cada docente y de un solo módulo; esa media la calcula la Administración con
  los datos de todo el equipo docente. Las funciones puras (`notaFinalCiclo`,
  `candidatosMatriculaHonor`) quedan en el motor, probadas, por si algún día hicieran falta.

# PROJECT STATUS

> Última actualización: 01/07/2026

---

# Estado general

**Proyecto:** EvalFP

**Versión actual:** 3.0 Beta

**Estado:** Fase de estabilización (QA)

**Arquitectura:** Modular (completada)

---

# Estado de los módulos

| Módulo | Estado |
|---------|---------|
| Arquitectura | ✅ Finalizada |
| Programación | 🟡 Funcional (pendiente rediseño del cambio de evaluaciones) |
| Alumnos | ✅ Validado |
| Actividades | ✅ Funcional |
| Notas | ✅ Validado |
| Dashboard | ⏳ Pendiente de QA |
| IA | ⏳ Pendiente de revisión completa |
| Ajustes | ⏳ Pendiente de QA |

---

# Trabajo realizado

## Refactorización

- Modularización del renderer.
- Modularización del CSS.
- Modularización del JavaScript.
- Separación Main / Renderer.
- Persistencia SQLite.
- Eliminación de dependencias de Excel.

## QA realizado

### Programación

- Horas UT.
- Persistencia.
- Añadir UT.
- Eliminar UT.

### Alumnos

- Alta.
- Edición.
- Eliminación.
- Persistencia.

### Notas

- Guardado.
- Recalculo inmediato de medias.
- Persistencia.

---

# Incidencias importantes

## EPIC-001

Rediseño del Plan de Evaluación.

No se abordará mediante un parche.

Se implementará en la versión 3.1.

---

# Próximo objetivo

Completar el QA de:

- Dashboard.
- IA.
- Ajustes.

---

# Estado del proyecto

Arquitectura        ██████████ 100%

Programación        █████████░ 90%

Alumnos             ██████████ 100%

Actividades         ██████████ 100%

Notas               ██████████ 100%

Dashboard           ██████░░░░ 60%

IA                  █████░░░░░ 50%

Ajustes             ███████░░░ 70%

---

# Próximo hito

Publicar EvalFP 3.0 RC1 tras finalizar la fase de QA.

## Próxima sesión

Al retomar el proyecto:

1. Continuar QA del Dashboard.
2. Revisar el módulo IA.
3. Validar Ajustes.
4. Preparar Release Candidate 1.
# KNOWN ISSUES

## BUG-001
Descripción: saveAlumno fallaba al actualizar con valores undefined.
Estado: ✅ Resuelto
Commit: ff51909

## BUG-002
Descripción: Programación mostraba Σ1176h en ISO.
Causa: dato persistido incorrecto (UT8.horas = 1010).
Estado: ✅ Resuelto

## BUG-003
Descripción: La media no se actualizaba al modificar una nota.
Causa: Se actualizaba la caché pero no el DOM.
Estado: ✅ Resuelto
Commit: f0268a7

## BUG-004

Estado: Pendiente

Prioridad: Alta

Descripción

Al cambiar el número de evaluaciones (3→2→3), la distribución del plan de evaluación deja de ser consistente.

Consecuencias

- Actividades duplicadas.
- Exámenes duplicados.
- Ponderaciones incorrectas.
- No se recupera el estado original.

Observación

No se corregirá mediante un parche.
Será objeto de un rediseño funcional completo en la versión 3.1.
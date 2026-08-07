# Hoja de ruta de EvalFP

> **Estado: 3.15.0** — aplicación de escritorio (Electron + SQLite), catálogo completo de
> Castilla-La Mancha, auditoría integral cerrada y auditoría en vivo (17 incidencias)
> también cerrada. Agosto de 2026.

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
| Catálogo CLM | 91 módulos · 12 ciclos · 4.444 CE literales del DOCM |
| Motor de calificación | Único, en `renderer/js/core/calificacion.js` |
| Normativa | Orden 201/2024, con la modificación de la Orden 55/2026 |
| Auditoría integral | Cerrada · 31 de 31 incidencias resueltas |
| Auditoría en vivo | Cerrada · 17 de 17, usando la aplicación con dos módulos reales |
| Tercera auditoría | Cerrada · 10 de 10: datos personales, carga, catálogo y accesibilidad |
| Cuarta auditoría | Cerrada · 6 de 6, atacando: 13.000 casos al azar y entradas reales |
| Quinta auditoría | Cerrada · 6 de 6: cierres, dos ventanas y corrección desde foto |
| Sexta auditoría | Cerrada · 4 de 4: los scripts de IA, incluida la inyección desde la hoja |
| Séptima auditoría | Cerrada · 4 de 4, usando la aplicación: copias, «Acerca de» y pantallas |
| Convocatorias | 1ª y 2ª unificadas (art. 21.5): la prueba de junio es una actividad más |
| Pruebas | Unitarias con Vitest · extremo a extremo con Playwright |
| Distribución | DMG (arm64 + x64) e instalador NSIS para Windows 11 |

## Pendiente de la próxima entrega

**Reconstruir los instaladores.** Hay cambios en la versión de desarrollo que todavía no
están en el DMG ni en el `.exe`: el icono de Notas y lo que venga de la revisión del
catálogo. Se hace al final, cuando el lote de cambios esté cerrado:

```
npm run build:mac      # en el Mac
npm.cmd run build:win  # en la máquina virtual, tras git pull
```

**Alinear el catálogo con los Decretos 78, 79 y 80/2024.** El catálogo tiene las horas de los
decretos de currículo originales; desde la Ley 3/2022 esos currículos están modificados y hay
módulos transversales nuevos —IPE I y II, Inglés Profesional, Digitalización, Sostenibilidad
y Proyecto Intermodular— que no están. Ojo: el Decreto 80/2024 tiene una corrección de
errores de septiembre de 2025, y los RA y CE se copian del DOCM, nunca del Real Decreto
estatal.

## Lo siguiente

1. **Probarlo en una 2ª convocatoria de verdad.** El modelo de convocatorias (A-5) está
   implementado y cubierto con pruebas, pero la comprobación que no da ninguna máquina es
   usarlo con un grupo real en junio. El paso a paso de esa sesión, con la copia de
   seguridad primero, está en [GUION_2A_CONVOCATORIA.md](GUION_2A_CONVOCATORIA.md).
2. **Firmar los instaladores.** Requiere comprar certificados: 99 USD al año en Apple —con
   exención posible para centros educativos— y unos 200-350 € al año en Windows, donde
   además el aviso de SmartScreen no desaparece hasta acumular descargas. El proyecto ya
   está preparado para firmar en cuanto haya credenciales: ver [FIRMA.md](FIRMA.md).
3. **Los ámbitos de Grado Básico no entran en el catálogo.** Comunicación y Sociedad y
   Ciencias Aplicadas los imparte profesorado de otras especialidades, no de FP, así que
   no son módulos de este cuaderno. La calificación cualitativa IN/SU/BI/NT/SB (art. 25.2)
   se queda implementada y probada por si alguna vez hace falta —se fuerza poniendo
   `ambito: true` en el módulo—, pero no hay nada que verificar con un ciclo real.

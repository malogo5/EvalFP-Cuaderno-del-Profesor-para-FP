# Entrega de la 3.16.0 · pasos que quedan

Todo el trabajo está hecho y verificado en la carpeta. Lo único que falta son tres cosas que
tienen que ejecutarse **en tus máquinas**, no desde aquí.

## Estado verificado (07/08/2026)

| Comprobación | Resultado |
|---|---|
| Versión | 3.16.0 |
| Módulos del catálogo | 130 |
| Criterios de evaluación | 5.964 |
| Cotejo literal contra los decretos | **100,00 %** |
| Tests unitarios | 175 de 175, en 8 ficheros |
| `npx eslint .` | limpio |
| `npm run prebake` | 130 módulos |

## 1. Commitear

Hay un fichero de bloqueo de git que mi shell no puede borrar. Bórralo tú y ya está:

```bash
cd ~/ProyectosCodex/evalfp
rm -f .git/index.lock
```

Antes de confirmar, mira el resumen de lo que va a entrar:

```bash
git status
git diff --stat
```

Y cuando lo veas bien:

```bash
git add -A
git commit -m "feat: catálogo alineado con los Decretos 78/79/80 de 2024 y Orden 55/2026

Revisión completa del catálogo contra la normativa vigente para 2026-27.

Catálogo (91 -> 130 módulos, 5.964 criterios):
- Gestión Administrativa: corregidas horas y curso de sus 9 módulos (D. 79/2024).
  Tres cambian de curso: 0437 y 0439 a 2.º, 0448 a 1.º.
- 39 módulos transversales nuevos (IPE I y II, Inglés Profesional, Digitalización,
  Sostenibilidad y Proyecto Intermodular) en los 9 ciclos que los llevan.
- CE de Python reconstruido con el Decreto 79/2025: códigos oficiales 5098-5101,
  430 h y los 127 criterios literales del Anexo II. Antes tenía códigos inventados.
- Trazabilidad de doble cita en 78 módulos: decreto de las horas y decreto de los
  RA y CE, con anexo, número y fecha de DOCM.
- cotejar_ce.py: cada criterio comparado con el texto de su decreto. 5.964 de 5.964.

Orden 55/2026 (modifica la Orden 201/2024, en vigor desde abril de 2026):
- art. 3.6: la pérdida de la evaluación continua ya no conserva calificaciones
  parciales. Solo cuenta la prueba objetiva, que debe cubrir todos los RA.
- art. 25.7 y 25.11: convalidaciones con y sin nota.
- art. 25.9, 25.10, 25.12 y 18.5: reglas de calificación final y de continuidad.
- La renuncia a convocatoria pasa del art. 25.9 al 25.8 por la renumeración.

Fase de empresa del CE de Python configurable entre 86 y 150 h (D. 79/2025, art. 5.3).

Documentación: INFORME_DISCREPANCIAS_2026-27.md con 16 secciones y cada cita
normativa. ROADMAP, README, MODULOS_PENDIENTES y manual de usuario al día.

175 tests, lint limpio."
```

## 2. Rehacer las distribuciones

`electron-builder` necesita cada sistema operativo nativo, así que esto va en tus máquinas:

```bash
# En el Mac
npm run build:mac

# En la máquina virtual de Windows, después de git pull
npm.cmd run build:win
```

Ambos ejecutan `npm run prebake` antes de empaquetar, así que el catálogo de 130 módulos
entra solo.

## 3. Borrar la copia de seguridad, cuando hayas commiteado

`backup_catalogo_20260807_183357/` ocupa 3,9 MB y es la foto del catálogo antes de la
revisión. **Mientras no confirmes el commit es tu única red fuera de git**, por eso no la he
borrado. Una vez commiteado, el estado anterior queda en el historial y la carpeta sobra:

```bash
rm -rf backup_catalogo_20260807_183357
```

Ya está en `.gitignore`, así que no se va a subir por accidente.

## No queda nada pendiente del catálogo

Los cinco proyectos intermodulares de grado superior (0379 ASIR, 0492 DAM, 0616 DAW,
0657 AF, 0664 AD) **quedan fuera por decisión**, no por olvido. El Decreto 80/2024 les
asigna 55 horas pero no desarrolla sus resultados de aprendizaje ni sus criterios, y
tampoco remite a ningún Real Decreto. Darlos de alta obligaría a inventar el currículo.

Queda documentado en la sección 13 del informe y en el ROADMAP, por si alguien pregunta
alguna vez por qué no están.

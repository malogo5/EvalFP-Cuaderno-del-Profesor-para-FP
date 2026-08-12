# Lo que falta por hacer

Escrito el 8 de agosto de 2026, al cerrar la versión 3.16.0.

El catálogo y la normativa están cerrados: 130 módulos, 5.964 criterios cotejados uno a uno
contra su decreto con el 100 % de coincidencia, 175 tests y la Orden 55/2026 implementada.

> ### ✅ La 3.16.0 está cerrada
> Entregada y verificada en macOS y Windows el 08/08/2026. Nada pendiente de esta versión.
> Lo que queda en este documento es de calendario o sin prisa.

---

## 1. La entrega de la 3.16.0 ✅ CERRADA el 08/08/2026

| | |
|---|---|
| CI | ✅ las cinco fases en verde |
| Commit y push | ✅ subido al remoto |
| Instalador de macOS | ✅ generado y **verificado** |
| Instalador de Windows | ✅ generado y **verificado** |
| Limpieza de git | ✅ hecha en el Mac y en la VM |

Los transversales aparecen en la aplicación instalada en las dos plataformas: el
`prebake` entró bien en el empaquetado y los instaladores llevan el catálogo de 130
módulos. **No queda nada de esta entrega.**

## 2. Cuando toque · calendario

### Probar una 2ª convocatoria de verdad · junio

Es la única comprobación que no da ninguna máquina. El modelo de convocatorias está
implementado y cubierto con pruebas, pero hasta que no se use con un grupo real no está
validado. El paso a paso, con la copia de seguridad primero, está en
[GUION_2A_CONVOCATORIA.md](GUION_2A_CONVOCATORIA.md).

### Revisar el catálogo si sale normativa nueva

```
python3 scripts/normativa/cotejar_ce.py
```

Compara los 5.964 criterios con el texto de su decreto y devuelve código 0 si todo casa.
Tarda un segundo. Pásalo cada vez que toques un módulo o se publique una modificación de
currículo.

---

## 3. Cuando quieras · mejoras sin prisa

### Los dos documentos que faltan de la Orden 55/2026

El cálculo está hecho y probado; falta generar el papel.

- **Anexo VIII** — informe de promoción o continuidad con materias pendientes (art. 18.5).
  La función `puedeContinuarConPendientes()` ya dice si se cumplen las condiciones y por qué
  no, cuando no se cumplen.
- **Anexo X-BIS** — resolución de exención de la fase de empresa, firmada por la dirección
  (art. 22.5). El estado `exenta` ya se guarda; falta el documento.

### Actualizar las acciones del CI

En la última ejecución avisaba de que `actions/checkout@v4` y `actions/setup-node@v4` usan
Node.js 20, que está obsoleto, y GitHub las va a forzar a Node 24. Se arregla subiéndolas a
`@v5` en `.github/workflows/ci.yml`. Todavía no rompe nada.

### Firmar los instaladores

Requiere comprar certificados: 99 USD al año en Apple —con posible exención para centros
educativos— y entre 200 y 350 € al año en Windows, donde además el aviso de SmartScreen no
desaparece hasta acumular descargas. El proyecto ya está preparado para firmar en cuanto
haya credenciales: ver [FIRMA.md](FIRMA.md).

---

## 4. Decidido que no se hace

No son olvidos: están razonados y documentados, por si alguien pregunta.

| Qué | Por qué |
|---|---|
| **Proyecto intermodular de grado superior** (0379 ASIR, 0492 DAM, 0616 DAW, 0657 AF, 0664 AD) | El Decreto 80/2024 les asigna 55 h pero no desarrolla sus RA ni CE, y tampoco remite a ningún Real Decreto, a diferencia del 79/2024 y del 78/2024. Es una laguna de la norma. Darlos de alta obligaría a redactar currículo por cuenta propia. |
| **Ámbitos 3161-3164** de Grado Básico y **Segunda lengua 0180** de AD | El artículo 9 del Decreto 78/2024 los llama «ámbitos no profesionales» y los atribuye a otro profesorado. No son módulos de este cuaderno. |
| **Nota final de ciclo y Matrícula de Honor** como pantalla | Los cuadernos de EvalFP son de cada docente y de un solo módulo; esa media la calcula la Administración con los datos de todo el equipo docente. Las funciones puras quedan en el motor, probadas, por si algún día hicieran falta. |

---

## Dos cosas que conviene no volver a dar por buenas

Aparecieron durante la revisión y las dos eran falsas:

1. **La corrección de errores del Decreto 80/2024 es del 14 de febrero de 2025, no de
   septiembre.** El «2025-09» de la URL es la carpeta del gestor de contenidos de la
   Consejería. Y no modifica ninguna hora: solo arregla una remisión cruzada.
2. **Las 400 horas de formación en empresa de grado básico salen de dentro de las 2.000 del
   ciclo, no se suman.** El artículo 16.1 de la Orden 204/2024 obliga a respetar los anexos
   de los decretos, y el Anexo I del 78/2024 ya suma 2.000 exactas incluyéndolas.

Y una del propio DOCM, que no se ha tocado: la tabla de SMR del Decreto 79/2024 declara
2.000 horas pero sus módulos suman 2.001. Comprobado con dos extractores independientes.
El catálogo coincide con el decreto módulo a módulo; la inconsistencia está en la norma.

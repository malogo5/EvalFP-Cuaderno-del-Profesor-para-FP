# Módulos perdidos del catálogo · 30/07/2026

## Qué falta

El catálogo tiene hoy **54 módulos, todos de Informática y Comunicaciones**.
Faltan los **36 módulos de la familia de Administración y Gestión** más 3 sueltos
que sí existían en la versión de julio (el catálogo tenía **90**).

La prueba está en la propia interfaz: `renderer/js/modules/modulos.js` define 12
pestañas de ciclo en `CAT_CICLO_LABELS`, pero **4 no tienen ni un módulo**, así
que al abrir «Añadir módulo» y pinchar en ellas aparece «No hay módulos»:

| Pestaña del catálogo | Módulos disponibles |
|---|---|
| CFGB Servicios Administrativos (**SA**) | 0 ← vacía |
| CFGM Gestión Administrativa (**GA**) | 0 ← vacía |
| CFGS Administración y Finanzas (**AF**) | 0 ← vacía |
| CFGS Asistencia a la Dirección (**AD**) | 0 ← vacía |
| Las 8 de Informática | 54 ✓ |

## Lista de los módulos que faltan

**SA — Servicios Administrativos (CFGB), 7:** `sa_tid` Tratamiento informático de datos (3001) ·
`sa_tab` Técnicas administrativas básicas (3003) · `sa_ac` Archivo y comunicación (3004) ·
`sa_abo` Aplicaciones básicas de ofimática (3002) · `sa_atc` Atención al cliente (3005) ·
`sa_ppvp` Preparación de pedidos y venta de productos (3006) · `sa_ipe` Itinerario personal para la empleabilidad (3159)

**GA — Gestión Administrativa (CFGM), 8:** `ga_cac` · `ga_oacv` · `ga_ea` · `ga_tii` ·
`ga_tc` · `ga_oarh` · `ga_tdc` · `ga_oagt`

**AF — Administración y Finanzas (CFGS), 10:** `af_gdj` · `af_hrsc` · `af_opi` · `af_piac` ·
`af_cac` · `af_grh` · `af_gf` · `af_cyf` · `af_glc` · `af_se`

**AD — Asistencia a la Dirección (CFGS), 8:** `ad_gdj` · `ad_hrsc` · `ad_opi` · `ad_piac` ·
`ad_cac` Comunicación y atención al cliente (0651) · `ad_pe` Protocolo empresarial (0661) ·
`ad_oee` Organización de eventos empresariales (0662) · `ad_gai` Gestión avanzada de la información (0663)

**Sueltos, 3:** `cfgb_io_ipe` · `ce_ciber_pps` · `ce_iabd_pia`

> Nota: `ad_data` (Acceso a Datos, DAM) sí está y no tiene relación con el ciclo AD.

## No están en el repositorio (comprobado)

- **83 commits** de `main`, la rama `refactor-v2-backup` y `origin/main`: siempre 54 módulos.
- `git log --diff-filter=D` sobre `scripts/modules/*_data.py`: **ningún borrado registrado**.
- `git rev-list --all --objects` buscando `ga_*`, `af_*`, `sa_*`, `ad_pe*`…: **sin resultados**.
- `git fsck --lost-found` y las 73 entradas del reflog: **nada recuperable**.

Conclusión: la historia del repositorio se reescribió y esos ficheros nunca
llegaron a estar en los commits actuales. Git no puede recuperarlos.

## Dónde sí pueden estar

1. **`cuaderno-profesor-archivo-final.zip`** (1,24 GB, 18 jul) — está **en la Papelera**.
   Es el archivo de la carpeta «Cuaderno del profesor», que en julio tenía el catálogo
   con los 90 módulos. **Es la vía más probable de recuperación: no vacíes la Papelera.**
2. GitHub: si alguna vez se subieron antes del `force push`, podrían quedar en un commit
   huérfano accesible por su hash desde la web (Insights → Network, o la API de eventos).
3. Regenerarlos desde el DOCM de Castilla-La Mancha con el mismo formato que
   `scripts/modules/*_data.py` (unas 2-3 h de trabajo por ciclo).

## Cómo recuperarlos del zip (una vez esté accesible)

```bash
cd ~/ProyectosCodex/evalfp
# 1. Extraer solo los módulos que faltan del zip
unzip -j "RUTA/cuaderno-profesor-archivo-final.zip" \
  "*/scripts/modules/sa_*_data.py" "*/scripts/modules/ga_*_data.py" \
  "*/scripts/modules/af_*_data.py" "*/scripts/modules/ad_[gohpcpeg]*_data.py" \
  "*/scripts/modules/cfgb_io_ipe_data.py" "*/scripts/modules/ce_ciber_pps_data.py" \
  "*/scripts/modules/ce_iabd_pia_data.py" -d scripts/modules/
# 2. Regenerar el catálogo prebaked que consume la app
npm run prebake
# 3. Comprobar que vuelven a ser 90
python3 -c "import json;print(len(json.load(open('renderer/modules_data.json'))['index']))"
```

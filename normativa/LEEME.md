# Normativa CLM · fuentes de los RA y CE del catálogo

Los RA y CE de los módulos salen **siempre del decreto de currículo de Castilla-La Mancha
publicado en el DOCM**, nunca del Real Decreto estatal: los RD fijan enseñanzas mínimas y CLM
puede ampliar tanto los criterios de evaluación como las horas.

## Qué hay en esta carpeta

| Fichero | Contenido |
|---|---|
| `CLM_Decreto_83_2014_Servicios_Administrativos.pdf` | currículo de SA (Grado Básico) |
| `CLM_Decreto_43_2013_AF.pdf` | currículo de Administración y Finanzas |
| `CLM_Decreto_41_2013_AD.pdf` | currículo de Asistencia a la Dirección |
| `texto/DOCM_*.txt` | el texto plano de cada decreto, ya normalizado |
| `docm_json/_crudo_*.json` | **todos** los módulos del decreto con sus RA y CE literales |
| `docm_json/_meta_*.json` | capa didáctica: sigla, curso, horas semanales, UT, evaluaciones |
| `docm_json/XX_NNNN.json` | entrada final de `gen_modulo.py` (decreto + metadatos) |
| `oficial_informatica.json` | tabla oficial de códigos, duración, h/semana y curso de los ciclos de Informática |

El decreto de GA (251/2011) se extrajo en el navegador con pdf.js; su texto está en
`texto/DOCM_GA_251_2011.txt`.

## Cómo conseguir un decreto nuevo del DOCM

`mcp__workspace__web_fetch` no sirve con `docm.jccm.es`: devuelve respuesta vacía tanto para el
PDF como para la versión HTML y el enlace ELI. La vía que funciona es el navegador:

1. Localiza el decreto vigente en la ficha del ciclo:
   `educacion.castillalamancha.es/fp/que-estudiar/<ciclo>` → sección **Normativa**.
   Esa misma ficha trae la **tabla de duración y distribución horaria semanal vigente**, que es
   la que hay que usar (suele diferir de la del decreto original).
2. Abre el permalink ELI (`docm.jccm.es/docm/eli/es-cm/d/AÑO/MM/DD/NÚMERO`) y anota el NID.
3. Desde una **pestaña recién abierta** de ese dominio (Chrome bloquea la segunda descarga
   automática de una misma pestaña), descarga el PDF con:

```js
const r = await fetch('/portaldocm/descargarArchivo.do?ruta=AAAA/MM/DD/pdf/NID.pdf&tipo=rutaDocm')
const b = await r.blob(), a = document.createElement('a')
a.href = URL.createObjectURL(b); a.download = 'decreto.pdf'; document.body.appendChild(a); a.click()
```

donde `AAAA/MM/DD` es la **fecha de publicación** y `NID` el identificador con `_` en vez de `/`.

4. `pdftotext -enc UTF-8 -nopgbrk decreto.pdf texto/DOCM_XX.txt`, normaliza los saltos de línea
   y pasa `scripts/parse_docm.py`.

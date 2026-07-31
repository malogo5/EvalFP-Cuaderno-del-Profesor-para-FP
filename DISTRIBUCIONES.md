# Construir las distribuciones

Los instaladores que hay en `dist/` **no se actualizan solos**: llevan dentro una copia
del código y del catálogo del día en que se construyeron. Si abres EvalFP desde
Aplicaciones y no ves algo que sí está en el proyecto, es que toca reconstruir.

Cada sistema se construye en su sistema. Desde macOS se puede intentar el `.exe`, pero
electron-builder necesita Wine para ponerle icono y datos al ejecutable, y en julio se
quedó a medias: apareció la carpeta descomprimida y ningún instalador. Con una máquina
virtual de Windows a mano, sale más limpio hacerlo allí.

## Antes de construir

1. `npm run lint && npm test` en verde.
2. Sube el número de versión en `package.json` si la tanda lo merece. Es lo que nombra
   los archivos (`EvalFP-3.3.1.dmg`) y lo que la app muestra abajo a la izquierda; dejarlo
   quieto significa que el instalador nuevo pisa al viejo y ya no sabes cuál es cuál.
3. Anota los cambios en `CHANGELOG.md`.

## macOS

```
cd ~/ProyectosCodex/evalfp
npm run build:mac
```

Deja en `dist/`:

- `EvalFP-<versión>-arm64.dmg` — Apple Silicon (tu MacBook Air).
- `EvalFP-<versión>.dmg` — Intel.

Abre el DMG, arrastra a Aplicaciones y **sustituye** la copia anterior. Si la tienes en el
Dock, quítala y vuelve a arrastrarla: el icono del Dock apunta a la copia vieja.

La app no está firmada con certificado de Apple, así que la primera vez macOS avisa. Se
abre con clic derecho → Abrir, o desde Ajustes del Sistema → Privacidad y seguridad.

## Windows (en la máquina virtual)

Dentro de Windows 11, una vez:

1. **Node.js 22 LTS** desde nodejs.org (el proyecto pide `>=22.12 <26`).
2. **Python 3** desde python.org, marcando *Add python.exe to PATH* — hace falta para
   regenerar el catálogo antes de empaquetar.
3. **Git** desde git-scm.com.

Y después, cada vez que quieras una versión nueva:

```
git clone https://github.com/malogo5/EvalFP-Cuaderno-del-Profesor-para-FP.git evalfp
cd evalfp
npm install
npm run build:win
```

(Si ya lo tienes clonado, `git pull` en vez de `git clone`.)

Deja en `dist\` el instalador `EvalFP Setup <versión>.exe`, que pregunta dónde instalar y
crea accesos en el escritorio y en el menú de inicio.

Clonar desde GitHub en vez de compartir la carpeta del Mac por Parallels evita el problema
clásico: `node_modules` trae binarios compilados para macOS que en Windows no valen.

## Qué se lleva dentro cada instalador

El código de la app, el catálogo ya generado (`renderer/modules_data.json`) y los scripts
de Python de la IA. **No** lleva Python: para el asistente y la corrección de exámenes hace
falta tenerlo instalado en la máquina donde se use.

Tampoco lleva tus datos. La base de datos vive aparte, en la carpeta de usuario de la app,
y sobrevive a las actualizaciones: instalar encima no borra módulos, alumnado ni notas.

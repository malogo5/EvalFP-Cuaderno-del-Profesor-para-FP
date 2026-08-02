# Firmar los instaladores

Sin firma, EvalFP se instala igual, pero cada equipo nuevo enseña un aviso de
«desarrollador no identificado» que hay que sortear a mano. Este documento
explica qué hace falta para quitarlo y cómo compilar el día que lo tengas.

El proyecto ya está preparado: no hay que tocar código, solo dar de alta las
credenciales como variables de entorno. **Sin credenciales, `npm run build:mac` y
`npm run build:win` siguen funcionando exactamente igual que hasta ahora.**

## Qué hay que comprar

**macOS.** Membresía del Apple Developer Program, 99 USD al año. Los centros
educativos acreditados y las administraciones públicas pueden pedir la exención
de la cuota, así que merece la pena preguntar en el instituto antes de pagarla.
Con la membresía se descarga del portal el certificado *Developer ID
Application*, que es el que sirve para distribuir fuera de la App Store.

**Windows.** Un certificado de firma de código de una autoridad reconocida
(SSL.com, DigiCert, Sectigo…). Los OV rondan los 200-350 € al año. Ojo con una
cosa: **el certificado no quita el aviso de SmartScreen de inmediato**. Desde
2024, Microsoft trata igual a los OV y a los EV, y la pantalla azul solo
desaparece cuando el instalador acumula descargas suficientes para ganarse
reputación. Para un programa que se instala en unos pocos ordenadores de un
departamento, el aviso puede no irse nunca. Si el objetivo es el instituto y no
la distribución masiva, este gasto es el más discutible de los dos.

## macOS: firmar y notarizar

Con el certificado ya instalado en el llavero (doble clic en el `.cer` que
descargas del portal), exporta estas tres variables y compila:

```bash
export APPLE_ID="tu-correo@ejemplo.com"
export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export APPLE_TEAM_ID="XXXXXXXXXX"

npm run build:mac:firmado
```

- La contraseña específica de aplicación **no es** la de tu cuenta Apple: se
  genera en <https://account.apple.com> → Iniciar sesión y seguridad →
  Contraseñas específicas para apps.
- El Team ID sale en <https://developer.apple.com/account> → Membership.
- La notarización sube el DMG a Apple y espera su respuesta: tarda entre dos y
  quince minutos. Es normal que parezca colgado.

`npm run build:mac` (sin `:firmado`) sigue generando el DMG de siempre, sin
firmar y sin esperas.

## Windows: firmar

Con el certificado exportado a un fichero `.pfx`:

```powershell
$env:CSC_LINK = "C:\ruta\a\certificado.pfx"
$env:CSC_KEY_PASSWORD = "la contraseña del pfx"

npm.cmd run build:win
```

electron-builder detecta las dos variables y firma el instalador él solo; no
hace falta un script aparte.

Muchas autoridades ya solo entregan el certificado en un token físico o en un
servicio en la nube, no como `.pfx`. Si es tu caso, la firma se hace con la
herramienta del proveedor después de compilar, y estas variables no aplican.

## Dónde NO poner las credenciales

Ni en `package.json`, ni en un `.env` dentro del repositorio, ni en un commit.
Son claves personales: van en variables de entorno de la sesión, o en el gestor
de secretos del sistema de integración continua si algún día se automatiza.

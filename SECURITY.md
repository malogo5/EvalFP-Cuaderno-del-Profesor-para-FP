# Security Policy

EvalFP trata datos sensibles de alumnado y configuración del profesorado. La seguridad aquí no es un extra, forma parte del diseño del proyecto.

## Qué debes proteger

- Datos de alumnado: nombres, NIA, fechas de nacimiento, notas y observaciones.
- Base de datos local SQLite.
- Claves API de servicios externos, si se usan.
- Copias de seguridad y exportaciones generadas por la app.

## Buenas prácticas

- No compartas la base de datos con datos reales fuera del entorno del centro.
- No subas `.db`, exportaciones reales ni copias de seguridad al repositorio.
- Usa las claves API solo en equipos de confianza.
- Revisa los logs antes de compartirlos, porque pueden contener información operativa.

## Cómo reportar un problema de seguridad

Si encuentras una vulnerabilidad, no la publiques en un issue abierto si puede afectar a datos reales.

1. Describe el problema con el mayor detalle posible.
2. Indica el flujo necesario para reproducirlo.
3. Señala si afecta a datos de alumnado, claves API o integridad de la base de datos.
4. Si puedes, sugiere una mitigación temporal.

## Alcance

EvalFP es una aplicación local de escritorio. Aun así, cualquier fallo que exponga datos, facilite su exfiltración o degrade la integridad de la base debe tratarse como prioritario.

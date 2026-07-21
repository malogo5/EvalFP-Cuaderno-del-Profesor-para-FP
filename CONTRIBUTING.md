# Contribuir a EvalFP

Gracias por interesarte por EvalFP. El proyecto crece con ayuda de docentes y colaboradores que quieran mejorar la herramienta sin perder de vista su uso real en el aula.

## Qué puedes aportar

- Nuevos módulos de FP: crea un `*_data.py` en `scripts/modules/` y regístralo en `scripts/teacher_config.py`.
- Errores y mejoras: abre un issue con pasos claros para reproducir el problema.
- Documentación: correcciones, ejemplos o aclaraciones son tan valiosas como el código.
- Experiencia de uso: si trabajas con EvalFP en un centro, cuéntanos qué falta, qué sobra y qué te haría ahorrar más tiempo.

## Antes de abrir un pull request

1. Usa una rama descriptiva, por ejemplo `feature/modulo-dam` o `fix/calculo-nota-final`.
2. Mantén la compatibilidad con lo ya existente.
3. Evita incluir datos reales de alumnado o copias de base de datos.
4. Revisa [docs/guia_desarrollo.md](docs/guia_desarrollo.md) y [docs/decisiones_arquitectura.md](docs/decisiones_arquitectura.md).
5. Si el cambio toca la interfaz o el flujo, prueba la app en local antes de enviar el PR.

## Qué revisar si tocas código

- `main.js`, `preload.js` y `db.js` para cambios de núcleo.
- `renderer/` para cambios de interfaz.
- `scripts/` para generación de módulos o materiales.
- `tests/` para no dejar la rama sin verificación.

## Código de conducta

Mantén un trato respetuoso y colaborativo. Este proyecto está hecho por y para docentes; el objetivo común es reducir carga administrativa sin añadir complejidad innecesaria.

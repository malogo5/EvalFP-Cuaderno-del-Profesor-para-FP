# Changelog

## [1.0.0-rc1] - 2026-07-29

Esta versión consolida el cierre funcional y arquitectónico principal de EvalFP. El sistema queda reforzado en evaluación, generación de informes, robustez de IA, privacidad y preparación para empaquetado.

### Added
- Ponderaciones dinámicas de RA integradas desde la base de datos local.
- Informes IA con control normativo de mínimos, regla de oro y mensajes humanizados.
- Validación previa de formato de notas en el cliente.
- Banners visuales de error y advertencia en la interfaz de IA.
- Indicadores de carga por fases durante procesos largos.
- Anonimización del alumnado antes de enviar datos a APIs externas.
- Aviso explícito cuando falla la generación de apuntes HTML.
- Exportación automatizada de informes individuales en el flujo masivo.
- Soporte para absentismo crítico y RAs llave en el diagnóstico.
- Resolución de rutas robusta para desarrollo y producción.

### Changed
- El parser de opciones de Python ahora rechaza flags desconocidos y flags sin valor.
- La lógica de CE→RA fue centralizada en un helper único.
- El motor IA añadió control de errores de red, timeouts y fallos de API.
- El flujo IPC fue unificado entre Electron y Python para el informe IA.
- La resolución de rutas internas de los scripts pasó a depender de la ubicación real del archivo, no del directorio de ejecución.

### Fixed
- Se eliminó la duplicación de lógica en varios puntos del backend.
- Se corrigieron casos de suma cero en ponderaciones.
- Se evitó el uso de texto técnico en crudo en la terminal del profesor.
- Se redujo el riesgo de congelación ante fallos de conexión.
- Se corrigieron silencios peligrosos en flags mal escritos.
- Se estabilizó el flujo de apuntes y materiales ante errores internos.

### Notes
- La base de código ha sido validada con comprobaciones estáticas.
- La validación definitiva de producción debe seguir realizándose sobre el binario empaquetado en macOS y Windows.
- Esta release candidate marca el cierre del bloque principal de hardening funcional y técnico.

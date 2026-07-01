# Arquitectura

## Estado

La aplicación ha finalizado la refactorización arquitectónica.

## Arquitectura actual

Electron

├── Main Process
│ ├── IPC
│ ├── SQLite
│ └── IA
│
├── Renderer
│ ├── Programación
│ ├── Alumnos
│ ├── Actividades
│ ├── Notas
│ ├── Dashboard
│ ├── Ajustes
│ └── IA
│
└── SQLite

## Refactorización completada

- CSS modularizado
- JavaScript modularizado
- Separación renderer/main
- IPC organizado
- Persistencia SQLite
- Eliminación de dependencias de Excel

Estado: Estable
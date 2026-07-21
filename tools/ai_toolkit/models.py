from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class FileInfo:
    path: Path
    relative_path: str

    # Información derivada
    name: str
    parent: str
    extension: str

    size: int
    language: str
    category: str


@dataclass(slots=True)
class Project:
    root: Path

    files: list[FileInfo] = field(default_factory=list)

    total_files: int = 0
    total_size: int = 0

    languages: dict[str, int] = field(default_factory=dict)
    categories: dict[str, int] = field(default_factory=dict)

    # Estructura
    directories: set[str] = field(default_factory=set)
    root_files: list[FileInfo] = field(default_factory=list)

    # Agrupaciones
    documentation: list[FileInfo] = field(default_factory=list)
    configuration: list[FileInfo] = field(default_factory=list)
    scripts: list[FileInfo] = field(default_factory=list)
    assets: list[FileInfo] = field(default_factory=list)
    tests: list[FileInfo] = field(default_factory=list)

    # Archivos especiales
    entry_points: list[FileInfo] = field(default_factory=list)

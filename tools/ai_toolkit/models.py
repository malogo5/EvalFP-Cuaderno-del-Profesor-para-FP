from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class FileInfo:
    path: Path
    relative_path: str
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

from pathlib import Path

from ai_toolkit.models import FileInfo, Project
from ai_toolkit.scanner import scan


DOCUMENTATION_FILES = {
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "LICENSE.md",
}

CONFIGURATION_FILES = {
    "package.json",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "tsconfig.json",
    "vite.config.js",
    "vite.config.ts",
    "electron-builder.yml",
    "docker-compose.yml",
    "Dockerfile",
    ".gitignore",
    ".env.example",
}

def analyze(project_root: Path) -> Project:
    """
    Analiza el proyecto y construye un objeto Project
    con toda la información agregada.
    """

    files = scan(project_root)

    project = Project(root=project_root)
    project.files = files

    project.total_files = len(files)
    project.total_size = sum(file.size for file in files)

    _analyze_files(project)

    return project


def _analyze_files(project: Project) -> None:
    """
    Recorre todos los archivos del proyecto y delega
    su clasificación en funciones especializadas.
    """

    for file in project.files:
        _classify_structure(project, file)
        _update_statistics(project, file)
        _classify_documentation(project, file)
        _classify_configuration(project, file)

def _classify_structure(project: Project, file: FileInfo) -> None:
    """
    Clasifica la estructura del proyecto.
    """

    parts = Path(file.relative_path).parts

    if len(parts) == 1:
        project.root_files.append(file)
    else:
        project.directories.add(parts[0])


def _update_statistics(project: Project, file: FileInfo) -> None:
    """
    Actualiza estadísticas generales.
    """

    project.languages[file.language] = (
        project.languages.get(file.language, 0) + 1
    )

    project.categories[file.category] = (
        project.categories.get(file.category, 0) + 1
    )


def _classify_documentation(project: Project, file: FileInfo) -> None:
    """
    Detecta archivos de documentación.
    """

    if (
        file.parent == "docs"
        or file.name in DOCUMENTATION_FILES
        or file.extension in {".md", ".txt", ".pdf"}
    ):
        project.documentation.append(file)

def _classify_configuration(project: Project, file: FileInfo) -> None:
    """
    Detecta archivos de configuración del proyecto.
    """

    if file.name in CONFIGURATION_FILES:
        project.configuration.append(file)

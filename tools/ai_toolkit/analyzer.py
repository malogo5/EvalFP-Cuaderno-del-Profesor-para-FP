from pathlib import Path

from ai_toolkit.models import Project
from ai_toolkit.scanner import scan


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
    Analiza los archivos del proyecto y completa
    la información derivada del modelo Project.
    """

    for file in project.files:
        parts = Path(file.relative_path).parts

        # Archivos en la raíz del proyecto
        if len(parts) == 1:
            project.root_files.append(file)
        else:
            project.directories.add(parts[0])

        # Estadísticas por lenguaje
        project.languages[file.language] = (
            project.languages.get(file.language, 0) + 1
        )

        # Estadísticas por categoría
        project.categories[file.category] = (
            project.categories.get(file.category, 0) + 1
        )

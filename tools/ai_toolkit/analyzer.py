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

    for file in files:
        project.languages[file.language] = (
            project.languages.get(file.language, 0) + 1
        )

        project.categories[file.category] = (
            project.categories.get(file.category, 0) + 1
        )

    return project

import json
from pathlib import Path


DEPENDENCY_MAP = {
    "electron": "Electron",
    "react": "React",
    "vue": "Vue",
    "vite": "Vite",
    "express": "Express",
    "tailwindcss": "Tailwind CSS",
    "typescript": "TypeScript",
}


def detect(path: Path) -> set[str]:
    """
    Detecta tecnologías a partir de un package.json.
    """

    technologies: set[str] = set()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return technologies

    dependencies = {}
    dependencies.update(data.get("dependencies", {}))
    dependencies.update(data.get("devDependencies", {}))

    for package in dependencies:
        technology = DEPENDENCY_MAP.get(package)

        if technology:
            technologies.add(technology)

    return technologies

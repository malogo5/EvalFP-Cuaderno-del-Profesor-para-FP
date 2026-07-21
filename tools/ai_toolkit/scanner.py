from pathlib import Path

from ai_toolkit.models import FileInfo


IGNORED_DIRS = {
    ".git",
    ".evalfp-ai",
    "node_modules",
    ".venv",
    "__pycache__",
    "coverage",
    "playwright-report",
    "test-results",
    "dist",
    "build",
}

IGNORED_FILES = {
    ".DS_Store",
}


LANGUAGE_MAP = {
    ".py": ("Python", "code"),
    ".js": ("JavaScript", "code"),
    ".html": ("HTML", "code"),
    ".css": ("CSS", "code"),
    ".json": ("JSON", "configuration"),
    ".md": ("Markdown", "documentation"),
    ".txt": ("Text", "documentation"),
    ".yml": ("YAML", "configuration"),
    ".yaml": ("YAML", "configuration"),
    ".xml": ("XML", "configuration"),
    ".svg": ("Image", "asset"),
    ".png": ("Image", "asset"),
    ".jpg": ("Image", "asset"),
    ".jpeg": ("Image", "asset"),
    ".ico": ("Image", "asset"),
    ".icns": ("Image", "asset"),
    ".pdf": ("PDF", "documentation"),
}


def scan(project_root: Path) -> list[FileInfo]:

    files: list[FileInfo] = []

    for path in sorted(project_root.rglob("*")):

        if path.is_dir():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        if path.name in IGNORED_FILES:
            continue

        if path.name.startswith(".~lock"):
            continue

        extension = path.suffix.lower()

        language, category = LANGUAGE_MAP.get(
            extension,
            ("Unknown", "other"),
        )

        files.append(
            FileInfo(
                path=path,
                relative_path=str(path.relative_to(project_root)),
                extension=extension or "-",
                size=path.stat().st_size,
                language=language,
                category=category,
            )
        )

    return files

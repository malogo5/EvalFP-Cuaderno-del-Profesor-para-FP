from pathlib import Path


IGNORED = {
    ".git",
    ".evalfp-ai",
    "node_modules",
    ".venv",
    "__pycache__",
    "dist",
    "build",
}


def file_size(path: Path) -> str:
    size = path.stat().st_size

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


def generate(project_root: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    output = output_dir / "PROJECT_INDEX.md"

    with output.open("w", encoding="utf-8") as f:

        f.write("# PROJECT INDEX\n\n")
        f.write(f"Proyecto: **{project_root.name}**\n\n")

        f.write("| Tipo | Archivo | Tamaño |\n")
        f.write("|------|---------|--------|\n")

        for path in sorted(project_root.rglob("*")):

            if any(part in IGNORED for part in path.parts):
                continue

            rel = path.relative_to(project_root)

            if path.is_dir():
                continue

            ext = path.suffix.lower() or "-"

            f.write(
                f"| {ext} | `{rel}` | {file_size(path)} |\n"
            )

    print(f"✓ Generado {output}")

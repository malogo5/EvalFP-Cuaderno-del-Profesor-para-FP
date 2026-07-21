from pathlib import Path

from ai_toolkit.analyzer import analyze


def file_size(size: int) -> str:

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


def generate(project_root: Path, output_dir: Path):

    output_dir.mkdir(parents=True, exist_ok=True)

    output = output_dir / "PROJECT_INDEX.md"

    project = analyze(project_root)

    with output.open("w", encoding="utf-8") as f:

        f.write("# PROJECT INDEX\n\n")
        f.write(f"Proyecto: **{project.root.name}**\n\n")

        f.write(f"Archivos analizados: **{project.total_files}**\n\n")

        f.write("| Lenguaje | Categoría | Archivo | Tamaño |\n")
        f.write("|-----------|-----------|---------|--------|\n")

        for file in project.files:

            f.write(
                f"| {file.language} | "
                f"{file.category} | "
                f"`{file.relative_path}` | "
                f"{file_size(file.size)} |\n"
            )

    print(f"✓ Generado {output}")

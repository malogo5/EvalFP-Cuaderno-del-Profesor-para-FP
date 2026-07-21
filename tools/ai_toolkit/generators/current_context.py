from pathlib import Path

from ai_toolkit.models import Project


def generate(project: Project, output_dir: Path) -> None:
    """
    Genera un resumen del estado actual del proyecto.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    output = output_dir / "CURRENT_CONTEXT.md"

    lines = [
        "# CURRENT CONTEXT",
        "",
        "## Project",
        "",
        f"Root: {project.root}",
        "",
        "## Summary",
        "",
        f"Files: {project.total_files}",
        f"Size: {project.total_size:,} bytes",
        "",
        "## Languages",
        "",
    ]

    for language, count in sorted(
        project.languages.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(f"- {language}: {count}")

    lines.extend(
        [
            "",
            "## Main directories",
            "",
        ]
    )

    for directory in sorted(project.directories):
        lines.append(f"- {directory}")

    lines.extend(
        [
            "",
            "## Documentation",
            "",
        ]
    )

    for file in sorted(project.documentation, key=lambda f: f.relative_path):
        lines.append(f"- {file.relative_path}")

    lines.extend(
        [
            "",
            "## Configuration",
            "",
        ]
    )

    for file in sorted(project.configuration, key=lambda f: f.relative_path):
        lines.append(f"- {file.relative_path}")

    lines.extend(
        [
            "",
            "---",
            "",
            "Generated automatically by AI Toolkit.",
        ]
    )

    output.write_text("\n".join(lines), encoding="utf-8")

    print(f"✓ Generado {output}")

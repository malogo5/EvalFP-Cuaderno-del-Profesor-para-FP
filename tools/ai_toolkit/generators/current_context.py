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

    # Languages
    for language, count in sorted(
        project.languages.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(f"- {language}: {count}")

    # Technologies
    lines.extend(
        [
            "",
            "## Technologies",
            "",
        ]
    )

    for technology in sorted(project.technologies):
        lines.append(f"- {technology}")

    # Main directories
    lines.extend(
        [
            "",
            "## Main directories",
            "",
        ]
    )

    for directory in sorted(project.directories):
        lines.append(f"- {directory}")

    # Documentation (compact summary)
    lines.extend(
        [
            "",
            "## Documentation",
            "",
        ]
    )

    root_docs = []
    doc_dirs = set()
    generated_docs = set()

    for file in project.documentation:
        path = file.relative_path

        if "/" not in path:
            root_docs.append(path)

        elif file.parent.startswith("docs"):
            doc_dirs.add(file.parent + "/")

        elif path.startswith("ia_output/"):
            generated_docs.add("ia_output/")

    lines.append(f"Root documents: {len(root_docs)}")

    if doc_dirs:
        lines.append("")
        lines.append("Documentation directories:")

        for directory in sorted(doc_dirs):
            lines.append(f"- {directory}")

    if generated_docs:
        lines.append("")
        lines.append("Generated documentation:")

        for directory in sorted(generated_docs):
            lines.append(f"- {directory}")

    # Configuration
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

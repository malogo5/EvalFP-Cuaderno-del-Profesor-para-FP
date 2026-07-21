#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_toolkit.analyzer import analyze
from ai_toolkit.generators.project_index import generate as generate_project_index
from ai_toolkit.generators.current_context import generate as generate_current_context

VERSION = "0.3.0"


def prepare():
    project_root = Path.cwd()
    output = project_root / ".evalfp-ai"

    print("Escaneando proyecto...")

    project = analyze(project_root)

    generate_project_index(project, output)
    generate_current_context(project, output)

    print("Proceso finalizado.")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=["prepare"],
    )

    args = parser.parse_args()

    print(f"AI Toolkit v{VERSION}")

    if args.command == "prepare":
        prepare()


if __name__ == "__main__":
    main()

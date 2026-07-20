#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
from pathlib import Path

from ai_toolkit.generators.project_index import generate

VERSION = "0.2.0"


def prepare():
    project_root = Path.cwd()
    output = project_root / ".evalfp-ai"

    print("Escaneando proyecto...")

    generate(project_root, output)

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

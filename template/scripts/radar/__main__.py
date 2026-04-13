"""Entry point: uv run python -m scripts.radar [--deep] [--refresh-themes] [--project-dir DIR]"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="radar",
        description="/radar — automated tech-watch for metadev-protocol projects",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Wider fetch budgets for quarterly SOTA survey mode",
    )
    parser.add_argument(
        "--refresh-themes",
        action="store_true",
        help="Force re-bootstrap of research-themes.yaml from PILOT.md (handled by the skill)",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=None,
        help="Root of the project (default: current working directory)",
    )
    args = parser.parse_args()

    if args.refresh_themes:
        # The skill handles the LLM extraction and calls save_themes().
        # This flag signals to the skill that the user wants to refresh themes.
        # The script itself doesn't do LLM work — print a sentinel and exit.
        print('{"action": "refresh_themes"}')
        sys.exit(0)

    from .core import run

    mode = "deep" if args.deep else "normal"
    report = run(mode=mode, project_dir=args.project_dir)
    print(report.to_json())


if __name__ == "__main__":
    main()

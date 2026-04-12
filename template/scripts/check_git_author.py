#!/usr/bin/env python3
"""Pre-commit hook: reject commits authored by 'Claude' or 'Anthropic'.

metadev-protocol ships ``attribution.commit: ""`` in the generated
``.claude/settings.json`` to suppress AI authorship on every commit.
An author named Claude contradicts that promise — it is always a
git config bug, never a feature.

This hook catches the bug locally before it reaches the history.
"""

from __future__ import annotations

import subprocess
import sys

FORBIDDEN_SUBSTRINGS = ("claude", "anthropic")


def main() -> int:
    try:
        ident = subprocess.check_output(
            ["git", "var", "GIT_AUTHOR_IDENT"], text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0

    name = ident.split("<", 1)[0].strip().lower()
    if any(bad in name for bad in FORBIDDEN_SUBSTRINGS):
        print(
            f"check_git_author: commit author '{name}' is forbidden.\n"
            "  metadev-protocol suppresses AI authorship by design.\n"
            "  Fix your git config:\n"
            "    git config user.name 'Your Name'\n"
            "    git config user.email 'you@example.com'",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

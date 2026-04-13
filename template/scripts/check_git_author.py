#!/usr/bin/env python3
"""Pre-commit / commit-msg hook: reject Claude/Anthropic authorship.

metadev-protocol suppresses AI authorship by design.

Two hook stages, one script:
  pre-commit stage  — called with no args  — checks git author identity
  commit-msg stage  — called with msg file — checks Co-authored-by trailers

See .pre-commit-config.yaml for the two hook entries.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_SUBSTRINGS = ("claude", "anthropic")

_COAUTHOR_RE = re.compile(r"co-authored-by:[^\n]*", re.IGNORECASE)


def check_author() -> str | None:
    """Return error message if the git author identity is forbidden."""
    try:
        ident = subprocess.check_output(
            ["git", "var", "GIT_AUTHOR_IDENT"], text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    name = ident.split("<", 1)[0].strip().lower()
    if any(bad in name for bad in FORBIDDEN_SUBSTRINGS):
        return (
            f"check_git_author: commit author '{name}' is forbidden.\n"
            "  Fix your git config:\n"
            "    git config user.name 'Your Name'\n"
            "    git config user.email 'you@example.com'"
        )
    return None


def check_coauthors(msg_file: Path) -> str | None:
    """Return error message if the commit message has a forbidden Co-authored-by trailer."""
    try:
        content = msg_file.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return None

    for match in _COAUTHOR_RE.finditer(content):
        line = match.group(0)
        if any(bad in line for bad in FORBIDDEN_SUBSTRINGS):
            return (
                "check_git_author: forbidden Co-authored-by trailer:\n"
                f"  {match.group(0)}\n"
                "  Remove it before committing."
            )
    return None


def main() -> int:
    if len(sys.argv) > 1:
        # commit-msg stage: pre-commit passes the message file as first arg
        error = check_coauthors(Path(sys.argv[1]))
    else:
        # pre-commit stage: check author identity
        error = check_author()

    if error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

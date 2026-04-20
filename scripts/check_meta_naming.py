#!/usr/bin/env python3
"""Pre-commit hook: enforce .meta/ filename taxonomy.

Validates that every staged file under .meta/active/ or .meta/archive/
matches the canonical pattern:

    <type>-<YYYY-MM-DD>-<kebab-slug>.md

Allowed types: spec, plan, brainstorm, debate, session, synthesis.
Exempt filenames: .gitkeep (so empty dir markers remain valid).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^(spec|plan|brainstorm|debate|session|synthesis)-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$"
)
EXEMPT = {".gitkeep"}
GUARDED_DIRS = ("active", "archive")


def is_guarded(path: Path) -> bool:
    parts = path.parts
    return len(parts) >= 3 and parts[0] == ".meta" and parts[1] in GUARDED_DIRS


def check(paths: list[str]) -> int:
    errors: list[str] = []
    for raw in paths:
        p = Path(raw)
        if not is_guarded(p):
            continue
        name = p.name
        if name in EXEMPT:
            continue
        if not PATTERN.match(name):
            errors.append(
                f"  {raw}\n"
                f"    expected: <type>-<YYYY-MM-DD>-<slug>.md "
                f"(type ∈ spec|plan|brainstorm|debate|session|synthesis)"
            )
    if errors:
        print(
            "check_meta_naming: invalid filename(s) under .meta/active/ or .meta/archive/:",
            file=sys.stderr,
        )
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1:]))

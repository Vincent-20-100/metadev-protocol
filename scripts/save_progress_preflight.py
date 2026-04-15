"""Run the pre-commit checklist for /save-progress.

Deterministic portion of /save-progress: run pytest, ruff, git status, and
check that no drafts leak at the project root or in .meta/scratch/. Prints a
JSON summary on stdout and exits non-zero on any failure so the skill can
abort before touching .meta/ files.

Usage:
    uv run python scripts/save_progress_preflight.py
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def _run(label: str, cmd: list[str]) -> dict[str, object]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "label": label,
        "cmd": " ".join(cmd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-5:],
        "stderr_tail": result.stderr.strip().splitlines()[-5:],
        "ok": result.returncode == 0,
    }


def _check_no_root_drafts(root: Path) -> dict[str, object]:
    stray: list[str] = []
    for pattern in ("spec-*.md", "plan-*.md", "brainstorm-*.md", "debate-*.md"):
        stray.extend(str(p.relative_to(root)) for p in root.glob(pattern))
    scratch = root / ".meta" / "scratch"
    if scratch.is_dir():
        stray.extend(str(p.relative_to(root)) for p in scratch.glob("*.py"))
    return {
        "label": "no stray drafts at root or code in .meta/scratch/",
        "stray_files": stray,
        "ok": len(stray) == 0,
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    checks = [
        _run("pytest", ["uv", "run", "pytest", "-q"]),
        _run("ruff check", ["uv", "run", "ruff", "check", "."]),
        _run("ruff format --check", ["uv", "run", "ruff", "format", "--check", "."]),
        _run("git status", ["git", "status", "--short"]),
        _check_no_root_drafts(root),
    ]
    all_ok = all(c["ok"] for c in checks)
    summary = {"ok": all_ok, "checks": checks}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic harness audit scorecard — 6 categories, 0-10 each (60 max).

Usage:
    uv run python -m evals.harness_audit --self          # audit this repo
    uv run python -m evals.harness_audit --path PATH     # audit a generated project
    uv run python -m evals.harness_audit --self --json   # JSON output
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

EXPECTED_SKILLS = {
    "brainstorm",
    "debate",
    "orchestrate",
    "plan",
    "research",
    "save-progress",
    "spec",
    "tech-watch",
    "test",
    "vision",
}

EXPECTED_AGENTS = {
    "devils-advocate",
    "code-reviewer",
    "test-engineer",
    "security-auditor",
    "data-analyst",
    "librarian",
}

EXPECTED_META_DIRS = (
    "active",
    "archive",
    "drafts",
    "decisions",
    "references/raw",
    "references/interim",
    "references/synthesis",
)

EXPECTED_SAFETY_SCRIPTS = (
    "audit_public_safety.py",
    "check_git_author.py",
    "check_meta_naming.py",
)

CATEGORY_MAX = 10


def _skills_dir(root: Path, is_meta: bool) -> Path:
    return (
        (root / "template" / ".claude" / "skills")
        if is_meta
        else (root / ".claude" / "skills")
    )


def _agents_dir(root: Path, is_meta: bool) -> Path:
    return (
        (root / "template" / ".claude" / "agents")
        if is_meta
        else (root / ".claude" / "agents")
    )


def check_skills(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    issues: list[tuple[str, int]] = []
    skills_dir = _skills_dir(root, is_meta)
    if not skills_dir.is_dir():
        return [("skills dir missing", CATEGORY_MAX)]

    present = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    missing = EXPECTED_SKILLS - present
    for name in sorted(missing):
        issues.append((f"skill '{name}' missing", 1))

    for name in sorted(present & EXPECTED_SKILLS):
        if not (skills_dir / name / "SKILL.md").is_file():
            issues.append((f"skill '{name}' lacks SKILL.md", 1))

    return issues


def check_agents(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    issues: list[tuple[str, int]] = []
    agents_dir = _agents_dir(root, is_meta)
    if not agents_dir.is_dir():
        return [("agents dir missing", CATEGORY_MAX)]

    present = {p.stem for p in agents_dir.iterdir() if p.suffix == ".md"}
    missing = EXPECTED_AGENTS - present
    for name in sorted(missing):
        issues.append((f"agent '{name}' missing", 2))

    for name in sorted(present & EXPECTED_AGENTS):
        content = (agents_dir / f"{name}.md").read_text(encoding="utf-8")
        if not content.startswith("---"):
            issues.append((f"agent '{name}' missing frontmatter", 1))

    return issues


def check_hosts(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    issues: list[tuple[str, int]] = []
    for stub in ("AGENTS.md", "GEMINI.md"):
        target = root / stub
        if not target.is_file():
            issues.append((f"{stub} missing", 3))
            continue
        content = target.read_text(encoding="utf-8")
        if "CLAUDE.md" not in content:
            issues.append((f"{stub} does not reference CLAUDE.md", 2))

    if not (root / "sync-config.yaml").is_file():
        issues.append(("sync-config.yaml missing", 2))
        return issues

    result = subprocess.run(
        ["uv", "run", "python", "scripts/sync_hosts.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        issues.append(("sync --check reports drift", 2))

    return issues


def check_contract(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    script = root / "scripts" / "check_skills_contract.py"
    if not script.is_file():
        return [("check_skills_contract.py missing", CATEGORY_MAX)]

    result = subprocess.run(
        ["uv", "run", "python", "scripts/check_skills_contract.py"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return [("skills-contract check failed", CATEGORY_MAX)]
    return []


def check_taxonomy(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    issues: list[tuple[str, int]] = []
    meta_root = root / ".meta"
    if not meta_root.is_dir():
        return [(".meta/ missing", CATEGORY_MAX)]

    for sub in EXPECTED_META_DIRS:
        if not (meta_root / sub).is_dir():
            issues.append((f".meta/{sub}/ missing", 2))

    return issues


def check_safety(root: Path, is_meta: bool) -> list[tuple[str, int]]:
    issues: list[tuple[str, int]] = []
    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        return [("scripts/ missing", CATEGORY_MAX)]

    weights = {
        "audit_public_safety.py": 4,
        "check_git_author.py": 3,
        "check_meta_naming.py": 3,
    }
    for name in EXPECTED_SAFETY_SCRIPTS:
        if not (scripts_dir / name).is_file():
            issues.append((f"scripts/{name} missing", weights[name]))

    return issues


CHECKS = (
    ("Skills", check_skills),
    ("Agents", check_agents),
    ("Hosts", check_hosts),
    ("Contract", check_contract),
    ("Taxonomy", check_taxonomy),
    ("Safety", check_safety),
)


def audit(root: Path, is_meta: bool) -> dict:
    categories = []
    total_score = 0
    for name, fn in CHECKS:
        issues = fn(root, is_meta)
        lost = sum(points for _, points in issues)
        score = max(0, CATEGORY_MAX - lost)
        total_score += score
        categories.append(
            {
                "name": name,
                "score": score,
                "max": CATEGORY_MAX,
                "issues": [{"description": d, "points_lost": p} for d, p in issues],
            }
        )

    return {
        "total": {"score": total_score, "max": CATEGORY_MAX * len(CHECKS)},
        "categories": categories,
    }


def format_report(data: dict) -> str:
    lines = []
    lines.append("Harness Audit Scorecard")
    lines.append("=" * 40)
    for cat in data["categories"]:
        lines.append(f"{cat['name']:<12} {cat['score']}/{cat['max']}")
        for issue in cat["issues"]:
            lines.append(f"  - {issue['description']} (-{issue['points_lost']})")
    lines.append("-" * 40)
    lines.append(f"TOTAL        {data['total']['score']}/{data['total']['max']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(prog="harness_audit")
    parser.add_argument(
        "--self",
        dest="self_mode",
        action="store_true",
        help="Audit this repo (meta layout)",
    )
    parser.add_argument("--path", type=Path, help="Path to a generated project")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.self_mode:
        root = Path(__file__).resolve().parent.parent
        is_meta = True
    elif args.path:
        root = args.path.resolve()
        is_meta = False
    else:
        print("ERROR: pass --self or --path", file=sys.stderr)
        return 2

    data = audit(root, is_meta)

    if args.as_json:
        print(json.dumps(data, indent=2))
    else:
        print(format_report(data))

    return 0 if data["total"]["score"] == data["total"]["max"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

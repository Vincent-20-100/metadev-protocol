"""Assert every CLAUDE.md trigger-table row maps to a real artifact.

Invariants (strict mode):
- Every row typed `skill` must map to `.claude/skills/<name>/SKILL.md` in the same tree.
- Every row typed `agent` must map to `.claude/agents/<name>.md` in the same tree.
- Every skill directory and agent file must be referenced by at least one row.
- Meta and template must have identical skill and agent sets (full symmetry).

Modes:
- Default (non-strict): check only the template tree. Useful during the
  dogfooding rollout when meta is still being brought to parity.
- `--strict`: check both trees AND require meta ↔ template symmetry.

Exit 0 on success, 1 on any violation. Violations are printed to stderr.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_RE = re.compile(r"^\|\s*`?/?(?P<name>[\w.-]+)`?\s*\|\s*skill\s*\|", re.MULTILINE)
AGENT_RE = re.compile(r"^\|\s*`?(?P<name>[\w'.-]+)`?\s*\|\s*agent\s*\|", re.MULTILINE)
TRIGGER_TABLE_HEADER = "## Skills & Agents"


def extract_trigger_table(text: str) -> str:
    """Return the text of the Skills & Agents section, up to the next `##` heading."""
    if TRIGGER_TABLE_HEADER not in text:
        return ""
    start = text.index(TRIGGER_TABLE_HEADER)
    tail = text[start + len(TRIGGER_TABLE_HEADER) :]
    next_heading = re.search(r"^##\s", tail, re.MULTILINE)
    end = next_heading.start() if next_heading else len(tail)
    return tail[:end]


def parse_rows(table_text: str) -> tuple[set[str], set[str]]:
    """Return (skill_names, agent_names) referenced in the table."""
    skills = {m.group("name").lstrip("/") for m in SKILL_RE.finditer(table_text)}
    agents = set()
    for match in AGENT_RE.finditer(table_text):
        name = match.group("name").strip("'")
        # Normalize devil's-advocate → devils-advocate (file naming convention)
        name = name.replace("devil's", "devils")
        agents.add(name)
    return skills, agents


def check_tree(
    claude_md: Path, skills_dir: Path, agents_dir: Path, label: str
) -> list[str]:
    """Validate one tree (meta or template). Return list of violation messages."""
    violations: list[str] = []
    if not claude_md.exists():
        violations.append(f"{label}: {claude_md} does not exist")
        return violations

    text = claude_md.read_text(encoding="utf-8")
    table = extract_trigger_table(text)
    if not table:
        violations.append(f"{label}: no '{TRIGGER_TABLE_HEADER}' section found")
        return violations

    referenced_skills, referenced_agents = parse_rows(table)

    actual_skills: set[str] = (
        {p.name for p in skills_dir.iterdir() if p.is_dir()}
        if skills_dir.is_dir()
        else set()
    )
    actual_agents: set[str] = (
        {p.stem for p in agents_dir.iterdir() if p.is_file() and p.suffix == ".md"}
        if agents_dir.is_dir()
        else set()
    )

    for name in sorted(referenced_skills):
        skill_file = skills_dir / name / "SKILL.md"
        if not skill_file.is_file():
            violations.append(
                f"{label}: trigger table references skill `{name}` but {skill_file.name} is missing"
            )

    for name in sorted(referenced_agents):
        agent_file = agents_dir / f"{name}.md"
        if not agent_file.is_file():
            violations.append(
                f"{label}: trigger table references agent `{name}` but {agent_file.name} is missing"
            )

    for name in sorted(actual_skills - referenced_skills):
        violations.append(
            f"{label}: skill directory `{name}/` exists but no row in trigger table references it"
        )

    for name in sorted(actual_agents - referenced_agents):
        violations.append(
            f"{label}: agent file `{name}.md` exists but no row in trigger table references it"
        )

    return violations


def check_parity(
    meta_skills: Path, tpl_skills: Path, meta_agents: Path, tpl_agents: Path
) -> list[str]:
    """Assert meta ↔ template parity for skills and agents."""
    violations: list[str] = []

    def _set(d: Path, want_dir: bool) -> set[str]:
        if not d.is_dir():
            return set()
        if want_dir:
            return {p.name for p in d.iterdir() if p.is_dir()}
        return {p.stem for p in d.iterdir() if p.is_file() and p.suffix == ".md"}

    tpl_s = _set(tpl_skills, want_dir=True)
    meta_s = _set(meta_skills, want_dir=True)
    tpl_a = _set(tpl_agents, want_dir=False)
    meta_a = _set(meta_agents, want_dir=False)

    for name in sorted(tpl_s - meta_s):
        violations.append(
            f"parity: skill `{name}` in template but not in meta (expected full symmetry)"
        )
    for name in sorted(meta_s - tpl_s):
        violations.append(
            f"parity: skill `{name}` in meta but not in template (expected full symmetry)"
        )
    for name in sorted(tpl_a - meta_a):
        violations.append(
            f"parity: agent `{name}` in template but not in meta (expected full symmetry)"
        )
    for name in sorted(meta_a - tpl_a):
        violations.append(
            f"parity: agent `{name}` in meta but not in template (expected full symmetry)"
        )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="check_skills_contract",
        description="Assert every trigger-table row maps to a real skill or agent file.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Check both trees and require meta ↔ template symmetry. Default checks template only.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent

    meta_claude = root / "CLAUDE.md"
    meta_skills = root / ".claude" / "skills"
    meta_agents = root / ".claude" / "agents"

    tpl_claude = root / "template" / "CLAUDE.md.jinja"
    tpl_skills = root / "template" / ".claude" / "skills"
    tpl_agents = root / "template" / ".claude" / "agents"

    is_metadev = tpl_claude.exists()
    violations: list[str] = []

    if is_metadev:
        violations += check_tree(tpl_claude, tpl_skills, tpl_agents, "template")
        if args.strict:
            if meta_claude.exists():
                violations += check_tree(meta_claude, meta_skills, meta_agents, "meta")
            violations += check_parity(meta_skills, tpl_skills, meta_agents, tpl_agents)
    else:
        if meta_claude.exists():
            violations += check_tree(meta_claude, meta_skills, meta_agents, "project")

    if violations:
        print("skills-contract check FAILED:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    mode = "strict" if args.strict else "template-only"
    print(f"skills-contract check OK ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Pre-public safety audit for metadev-protocol.

Three checks defend against accidental secret or sensitive-file leaks:

- **Check A** — Sensitive files tracked in git (denylist match on filenames)
- **Check B** — `.gitignore` coverage for canonical paths
- **Check C** — Secret patterns in tracked file content

Two modes:

- ``--mode=full`` (default): runs A + B + C on the entire tracked tree
- ``--mode=quick FILE ...``: runs C only on the given files (pre-commit)

Exit codes: 0 = clean, 1 = violations found, 2 = usage error.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import PurePosixPath

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SENSITIVE_FILENAME_PATTERNS: list[str] = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa*",
    "id_ed25519*",
    "id_ecdsa*",
    "id_dsa*",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "credentials*",
    "secrets*",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "*.kdbx",
    "service-account*.json",
]

GITIGNORE_CANONICAL_PATHS: list[str] = [
    ".env",
    ".env.local",
    ".env.production",
    "__pycache__/x.pyc",
    ".venv/lib",
    "venv/lib",
    "dummy.pyc",
    ".DS_Store",
    ".idea/workspace.xml",
    ".vscode/settings.json",
    "dist/x",
    "build/x",
    "dummy.egg-info/x",
    ".coverage",
    ".pytest_cache/x",
    ".ruff_cache/x",
    "node_modules/x",
    ".mypy_cache/x",
]

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("OpenAI API key", re.compile(r"sk-[a-zA-Z0-9]{20,}")),
    ("GitHub PAT", re.compile(r"ghp_[a-zA-Z0-9]{36}")),
    ("GitHub OAuth token", re.compile(r"gho_[a-zA-Z0-9]{36}")),
    ("GitHub server token", re.compile(r"ghs_[a-zA-Z0-9]{36}")),
    ("GitHub user-to-server token", re.compile(r"ghu_[a-zA-Z0-9]{36}")),
    ("GitHub refresh token", re.compile(r"ghr_[a-zA-Z0-9]{36}")),
    ("GitHub fine-grained PAT", re.compile(r"github_pat_[a-zA-Z0-9_]{82}")),
    ("AWS access key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("AWS temporary access key", re.compile(r"ASIA[0-9A-Z]{16}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("Google OAuth token", re.compile(r"ya29\.[0-9A-Za-z\-_]+")),
    (
        "Google service-account JSON",
        re.compile(r'"type":\s*"service_account"'),
    ),
    ("Slack token", re.compile(r"xox[baprs]-[a-zA-Z0-9\-]{10,}")),
    (
        "Slack webhook",
        re.compile(
            r"https://hooks\.slack\.com/services/"
            r"T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+"
        ),
    ),
    ("Stripe secret live key", re.compile(r"sk_live_[0-9a-zA-Z]{24,}")),
    ("Stripe restricted live key", re.compile(r"rk_live_[0-9a-zA-Z]{24,}")),
    ("Stripe publishable live key", re.compile(r"pk_live_[0-9a-zA-Z]{24,}")),
    (
        "SendGrid API key",
        re.compile(r"SG\.[a-zA-Z0-9_\-]{22}\.[a-zA-Z0-9_\-]{43}"),
    ),
    ("Mailgun API key", re.compile(r"key-[a-z0-9]{32}")),
    ("Twilio Account SID", re.compile(r"AC[a-f0-9]{32}")),
    ("Twilio API key", re.compile(r"SK[a-f0-9]{32}")),
    ("DigitalOcean personal token", re.compile(r"dop_v1_[a-f0-9]{64}")),
    ("DigitalOcean OAuth token", re.compile(r"doo_v1_[a-f0-9]{64}")),
    ("DigitalOcean refresh token", re.compile(r"dor_v1_[a-f0-9]{64}")),
    ("npm access token", re.compile(r"npm_[a-zA-Z0-9]{36}")),
    ("GitLab PAT", re.compile(r"glpat-[a-zA-Z0-9\-_]{20}")),
    (
        "Discord bot token",
        re.compile(r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}"),
    ),
    ("Telegram bot token", re.compile(r"\d{9,10}:[a-zA-Z0-9_-]{35}")),
    (
        "JSON Web Token",
        re.compile(r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"),
    ),
    (
        "Private key (PEM)",
        re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "PGP private key",
        re.compile(r"-----BEGIN PGP PRIVATE KEY BLOCK-----"),
    ),
    (
        "Bearer auth token",
        re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-.=]{20,}"),
    ),
    (
        "Generic named secret",
        re.compile(
            r"(?i)(api[_-]?key|access[_-]?token|secret[_-]?key|"
            r"auth[_-]?token|client[_-]?secret)"
            r"""["':\s=]+["']?[a-zA-Z0-9_\-]{20,}"""
        ),
    ),
    (
        "Postgres URI with credentials",
        re.compile(r"postgres(?:ql)?://[^:\s]+:[^@\s]+@"),
    ),
    (
        "MongoDB URI with credentials",
        re.compile(r"mongodb(?:\+srv)?://[^:\s]+:[^@\s]+@"),
    ),
    (
        "MySQL URI with credentials",
        re.compile(r"mysql://[^:\s]+:[^@\s]+@"),
    ),
    (
        "Redis URI with credentials",
        re.compile(r"redis://[^:\s]*:[^@\s]+@"),
    ),
    (
        "AMQP URI with credentials",
        re.compile(r"amqps?://[^:\s]+:[^@\s]+@"),
    ),
]

# Paths excluded from secret scanning (relative to repo root).
SCAN_EXCLUDE_PREFIXES: tuple[str, ...] = (
    "scripts/audit_public_safety.py",
    "template/scripts/audit_public_safety.py",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_COLOR = sys.stdout.isatty()


def _red(text: str) -> str:
    return f"\033[91m{text}\033[0m" if _COLOR else text


def _green(text: str) -> str:
    return f"\033[92m{text}\033[0m" if _COLOR else text


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m" if _COLOR else text


def _git_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f for f in result.stdout.splitlines() if f]


def _is_binary(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(8192)
            return b"\x00" in chunk
    except OSError:
        return True


def _is_excluded(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in SCAN_EXCLUDE_PREFIXES)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


@dataclass
class Violations:
    messages: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return len(self.messages) == 0


def check_sensitive_files_tracked() -> Violations:
    """Check A — detect sensitive files tracked in git."""
    v = Violations()
    tracked = _git_tracked_files()
    for filepath in tracked:
        name = PurePosixPath(filepath).name
        for pattern in SENSITIVE_FILENAME_PATTERNS:
            if fnmatch.fnmatch(name, pattern):
                v.messages.append(f"  {filepath}  (matches '{pattern}')")
                break
    return v


def check_gitignore_coverage() -> Violations:
    """Check B — verify canonical paths are covered by .gitignore."""
    v = Violations()
    for path in GITIGNORE_CANONICAL_PATHS:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", path],
            capture_output=True,
        )
        if result.returncode != 0:
            v.messages.append(f"  {path}  (not covered by .gitignore)")
    return v


def check_secret_patterns(files: list[str]) -> Violations:
    """Check C — scan file content for secret patterns."""
    v = Violations()
    for filepath in files:
        if _is_excluded(filepath):
            continue
        if not os.path.isfile(filepath):
            continue
        if _is_binary(filepath):
            continue
        try:
            with open(filepath, encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    for label, pattern in SECRET_PATTERNS:
                        if pattern.search(line):
                            v.messages.append(
                                f"  {filepath}:{lineno}  {label} -> <REDACTED>"
                            )
        except OSError:
            continue
    return v


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def _print_section(title: str, violations: Violations) -> None:
    if violations.clean:
        print(f"  {_green('OK')} {title}")
    else:
        print(f"  {_red('FAIL')} {title}")
        for msg in violations.messages:
            print(_red(msg))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pre-public safety audit.",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "quick"],
        default="full",
        help="full = A+B+C on tracked tree; quick = C only on given files",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to scan (quick mode)",
    )
    args = parser.parse_args(argv)

    if args.mode == "quick" and not args.files:
        print("error: --mode=quick requires at least one file", file=sys.stderr)
        return 2

    print(_bold("Public safety audit") + f"  (mode={args.mode})\n")

    failed = False

    if args.mode == "full":
        va = check_sensitive_files_tracked()
        _print_section("Check A - sensitive files tracked", va)
        if not va.clean:
            failed = True

        vb = check_gitignore_coverage()
        _print_section("Check B - .gitignore coverage", vb)
        if not vb.clean:
            failed = True

        files = _git_tracked_files()
    else:
        files = args.files

    vc = check_secret_patterns(files)
    _print_section("Check C - secret patterns in content", vc)
    if not vc.clean:
        failed = True

    print()
    if failed:
        print(_red("FAIL") + " - violations detected, see above.")
        return 1
    print(_green("PASS") + " - no violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

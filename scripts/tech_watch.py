#!/usr/bin/env python3
"""Tech watch — GitHub repo discovery for AI-coding topics.

Queries the GitHub Search API for recently-active repositories on topics
relevant to metadev-protocol (agentic coding, LLM tooling, copier, etc.)
and appends a structured Markdown report to .meta/references/raw/.

Usage:
    python scripts/tech_watch.py
    python scripts/tech_watch.py --since 7
    python scripts/tech_watch.py --topics claude-code,copier --since 14

Requirements:
    GITHUB_TOKEN env var (or .env file at repo root).
    Token scope: public_repo read access is sufficient.
    Create one at https://github.com/settings/tokens
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_TOPICS = [
    "claude-code",
    "agentic-coding",
    "ai-coding",
    "copier",
    "llm-agents",
    "claude-sdk",
]

RAW_DIR = Path(".meta/references/raw")
SEEN_CACHE = RAW_DIR / ".tech-watch-seen.json"
GITHUB_API = "https://api.github.com/search/repositories"


# ---------------------------------------------------------------------------
# .env parser (~15 lines, no dependencies)
# ---------------------------------------------------------------------------


def load_env(path: Path) -> dict[str, str]:
    """Parse KEY=value pairs from a .env file; ignore comments and blank lines."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


# ---------------------------------------------------------------------------
# Dedup cache
# ---------------------------------------------------------------------------


def load_seen(path: Path) -> set[str]:
    """Load the set of previously seen repo hashes."""
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return set(data)
    except (json.JSONDecodeError, TypeError):
        return set()


def save_seen(path: Path, seen: set[str]) -> None:
    """Persist the seen-repo hash cache."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(seen), indent=2), encoding="utf-8")


def repo_hash(full_name: str) -> str:
    return hashlib.sha256(full_name.encode()).hexdigest()


# ---------------------------------------------------------------------------
# GitHub API
# ---------------------------------------------------------------------------


def github_search(topic: str, since: str, token: str) -> list[dict]:
    """Search GitHub repos for a topic pushed since a given date.

    Returns a list of repo dicts from the GitHub API response.
    Exits with a non-zero status on authentication or network errors.
    """
    query = f"topic:{topic} pushed:>{since}"
    params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": 30})
    url = f"{GITHUB_API}?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "metadev-protocol-tech-watch/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status not in (200, 201):
                sys.exit(f"tech_watch: HTTP {resp.status} from GitHub API")
            return json.loads(resp.read().decode("utf-8")).get("items", [])
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        sys.exit(f"tech_watch: HTTP {exc.code} — {body}")
    except urllib.error.URLError as exc:
        sys.exit(f"tech_watch: Network error — {exc.reason}")


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def _escape_pipe(text: str) -> str:
    return text.replace("|", r"\|")


def format_row(repo: dict) -> str:
    """Format one repo as a Markdown table row."""
    name = repo.get("full_name", "")
    stars = repo.get("stargazers_count", 0)
    pushed = (repo.get("pushed_at") or "")[:10]
    topics = ", ".join(repo.get("topics", [])[:4])
    desc = repo.get("description") or ""
    if len(desc) > 120:
        desc = desc[:119] + "…"
    url = repo.get("html_url", "")
    return (
        f"| {_escape_pipe(name)} "
        f"| {stars} "
        f"| {pushed} "
        f"| {_escape_pipe(topics)} "
        f"| {_escape_pipe(desc)} "
        f"| {url} |"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch trending AI-coding repos from GitHub and append to .meta/references/raw/."
    )
    parser.add_argument(
        "--since",
        type=int,
        default=30,
        metavar="DAYS",
        help="Look back N days (default: 30)",
    )
    parser.add_argument(
        "--topics",
        type=str,
        default=",".join(DEFAULT_TOPICS),
        help="Comma-separated topic list",
    )
    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    since_date = (datetime.now(tz=UTC) - timedelta(days=args.since)).strftime("%Y-%m-%d")
    today = datetime.now(tz=UTC).strftime("%Y-%m-%d")

    # Resolve token
    env = load_env(Path(".env"))
    token = env.get("GITHUB_TOKEN") or __import__("os").environ.get("GITHUB_TOKEN", "")
    if not token:
        sys.exit(
            "tech_watch: GITHUB_TOKEN missing.\n"
            "Set it in .env (copy from .env.example) or export it in your shell.\n"
            "Create a token at https://github.com/settings/tokens (scope: public_repo)"
        )

    # Load dedup cache
    seen = load_seen(SEEN_CACHE)
    new_repos: list[dict] = []

    print(f"tech_watch: querying {len(topics)} topics, since={since_date} …")

    for topic in topics:
        results = github_search(topic, since_date, token)
        for repo in results:
            h = repo_hash(repo["full_name"])
            if h not in seen:
                seen.add(h)
                repo["_matched_topic"] = topic
                new_repos.append(repo)

    # Deduplicate across topics (same repo may appear in multiple)
    seen_names: set[str] = set()
    unique_new: list[dict] = []
    for repo in new_repos:
        if repo["full_name"] not in seen_names:
            seen_names.add(repo["full_name"])
            unique_new.append(repo)

    # Sort by stars desc
    unique_new.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)

    # Build output
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / f"session-{today}-tech-watch.md"

    header = f"""\
---
type: session
date: {today}
slug: tech-watch
status: active
---

# Tech watch — {today}

**Topics:** {", ".join(topics)}
**Window:** last {args.since} days
**New this run:** {len(unique_new)} repos

"""

    if unique_new:
        table_header = (
            "| Repo | Stars | Pushed | Topics | Description | URL |\n"
            "|------|-------|--------|--------|-------------|-----|\n"
        )
        rows = "\n".join(format_row(r) for r in unique_new)
        body = table_header + rows + "\n"
    else:
        body = "_No new repos this run (all results already in seen cache)._\n"

    out_path.write_text(header + body, encoding="utf-8")
    save_seen(SEEN_CACHE, seen)

    print(f"tech_watch: {len(unique_new)} new repos → {out_path}")
    if not unique_new:
        print("tech_watch: dedup cache is working — re-run with --since N to widen the window")


if __name__ == "__main__":
    main()

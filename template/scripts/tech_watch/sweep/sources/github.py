# Adapted from Panniantong/Agent-Reach (MIT License)
# Original: https://github.com/Panniantong/Agent-Reach
# Copyright (c) Panniantong
# Modifications: adapted to Source ABC, uses Item dataclass,
# simplified to single search command.

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from datetime import date

from .base import Item, Source

logger = logging.getLogger(__name__)


class GitHubSource(Source):
    """Fetch GitHub repos via `gh search repos`."""

    tier = 0  # requires gh CLI + auth, but free

    def fetch(self, query: str, limit: int = 10) -> list[Item]:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "search",
                    "repos",
                    query,
                    "--sort",
                    "stars",
                    "--limit",
                    str(limit),
                    "--json",
                    "nameWithOwner,description,stargazersCount,url",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                logger.warning("gh search failed: %s", result.stderr.strip())
                return []
            repos = json.loads(result.stdout)
            today = date.today()
            return [
                Item(
                    url=r["url"],
                    title=r["nameWithOwner"],
                    pitch=(r.get("description") or "")[:200],
                    score_raw=float(r.get("stargazersCount", 0)),
                    discovered=today,
                    source_name="github",
                )
                for r in repos
            ]
        except Exception:
            logger.exception("GitHubSource.fetch failed for query=%r", query)
            return []

    def check(self) -> list[str]:
        issues = []
        if not shutil.which("gh"):
            issues.append("gh CLI not found — install from https://cli.github.com")
        else:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
            if result.returncode != 0:
                issues.append("gh not authenticated — run `gh auth login`")
        return issues

    def can_handle(self, url: str) -> bool:
        return "github.com" in url

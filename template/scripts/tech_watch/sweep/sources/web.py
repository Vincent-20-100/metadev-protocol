from __future__ import annotations

import logging
import subprocess

from .base import Item, Source

logger = logging.getLogger(__name__)


class WebSource(Source):
    """Read arbitrary URLs via Jina Reader (zero-config universal web reader).

    This source does NOT implement fetch() for bulk search — it is a
    single-URL reader used by the skill to deepen a specific card.
    Call read(url) to get the markdown content of any web page.
    """

    tier = 0

    def fetch(self, query: str = "", limit: int = 10) -> list[Item]:
        raise NotImplementedError(
            "WebSource is a reader, not a search source. Use read(url) instead."
        )

    def read(self, url: str) -> str:
        """Fetch and return the markdown content of a URL via Jina Reader."""
        try:
            result = subprocess.run(
                ["curl", "-s", f"https://r.jina.ai/{url}"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                logger.warning("Jina Reader failed for %s: %s", url, result.stderr.strip())
                return ""
            return result.stdout
        except Exception:
            logger.exception("WebSource.read failed for url=%r", url)
            return ""

    def check(self) -> list[str]:
        import shutil

        if not shutil.which("curl"):
            return ["curl not found — required for Jina Reader"]
        return []

    def can_handle(self, url: str) -> bool:
        # handles any URL not claimed by other sources
        return True

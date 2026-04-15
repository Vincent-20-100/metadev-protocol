# Adapted from Panniantong/Agent-Reach (MIT License)
# Original: https://github.com/Panniantong/Agent-Reach
# Copyright (c) Panniantong
# Modifications: adapted to Source ABC, uses Item dataclass,
# separated Reddit into its own thin wrapper.

from __future__ import annotations

import logging
from datetime import date

from .base import Item, Source

logger = logging.getLogger(__name__)


class RSSSource(Source):
    """Fetch items from an RSS/Atom feed via feedparser."""

    tier = 0

    def __init__(self, feed_url: str, user_agent: str = "radar/0.1 (metadev-protocol)"):
        self.feed_url = feed_url
        self.user_agent = user_agent

    def fetch(self, query: str = "", limit: int = 10) -> list[Item]:
        try:
            import feedparser  # optional dep — installed via `uv sync --extra radar`

            feed = feedparser.parse(self.feed_url, agent=self.user_agent)
            if feed.bozo and not feed.entries:
                logger.warning(
                    "RSS parse error for %s: %s", self.feed_url, feed.bozo_exception
                )
                return []

            today = date.today()
            items = []
            for i, entry in enumerate(feed.entries[:limit]):
                url = entry.get("link", "")
                title = entry.get("title", "")
                summary = entry.get("summary", "")[:200]
                if not url or not title:
                    continue
                # score_raw = inverse position (first entry = highest score)
                items.append(
                    Item(
                        url=url,
                        title=title,
                        pitch=summary,
                        score_raw=float(limit - i),
                        discovered=today,
                        source_name="rss",
                    )
                )
            return items
        except ImportError:
            logger.error("feedparser not installed — run `uv sync --extra radar`")
            return []
        except Exception:
            logger.exception("RSSSource.fetch failed for %s", self.feed_url)
            return []

    def check(self) -> list[str]:
        try:
            import feedparser  # noqa: F401

            return []
        except ImportError:
            return ["feedparser not installed — run `uv sync --extra radar`"]

    def can_handle(self, url: str) -> bool:
        return self.feed_url == url

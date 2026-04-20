from __future__ import annotations

import logging
from datetime import date

from .base import Item, Source
from .rss import RSSSource

logger = logging.getLogger(__name__)

_USER_AGENT = "radar/0.1 (metadev-protocol; +https://github.com/Vincent-20-100/metadev-protocol)"


class RedditSource(Source):
    """Fetch hot posts from subreddits via public RSS feeds (no OAuth)."""

    tier = 0

    def __init__(self, subreddits: list[str]):
        self.subreddits = subreddits

    def fetch(self, query: str = "", limit: int = 10) -> list[Item]:
        items: list[Item] = []
        per_sub = max(1, limit // len(self.subreddits)) if self.subreddits else limit
        for sub in self.subreddits:
            feed_url = f"https://www.reddit.com/r/{sub}/hot/.rss"
            source = RSSSource(feed_url, user_agent=_USER_AGENT)
            fetched = source.fetch(limit=per_sub)
            for item in fetched:
                items.append(
                    Item(
                        url=item.url,
                        title=item.title,
                        pitch=item.pitch,
                        score_raw=item.score_raw,
                        discovered=date.today(),
                        source_name="reddit",
                    )
                )
        return items[:limit]

    def check(self) -> list[str]:
        return RSSSource("").check()

    def can_handle(self, url: str) -> bool:
        return "reddit.com" in url

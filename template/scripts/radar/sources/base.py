# Adapted from Panniantong/Agent-Reach (MIT License)
# Original: https://github.com/Panniantong/Agent-Reach
# Copyright (c) Panniantong
# Modifications: renamed Channel → Source, added Item dataclass,
# adapted fetch signature for metadev-protocol /radar skill.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass
class Item:
    """A normalized research item from any source."""

    url: str
    title: str
    pitch: str
    score_raw: float  # native score from source (stars, likes, position)
    discovered: date
    source_name: str  # github | hf | rss | reddit | web

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.url == other.url


class Source(ABC):
    """Abstract base class for all /radar data sources.

    Subclasses implement fetch() to return normalized Items.
    The tier field signals the setup complexity (0 = zero config).
    """

    tier: int = 0  # 0 = no API key, 1 = free key, 2 = paid/complex

    @abstractmethod
    def fetch(self, query: str, limit: int = 10) -> list[Item]:
        """Fetch items matching query. Must not raise — log and return []."""

    def check(self) -> list[str]:
        """Return list of missing prerequisites (empty = ready to use)."""
        return []

    def can_handle(self, url: str) -> bool:
        """Return True if this source owns the given URL (for dedup routing)."""
        return False

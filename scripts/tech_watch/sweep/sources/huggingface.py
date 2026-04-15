from __future__ import annotations

import logging
from datetime import date

from .base import Item, Source

logger = logging.getLogger(__name__)


class HuggingFaceSource(Source):
    """Fetch trending models from HuggingFace Hub (no token needed for public content)."""

    tier = 0

    def fetch(self, query: str = "", limit: int = 10) -> list[Item]:
        try:
            from huggingface_hub import list_models  # optional dep

            kwargs: dict = {"limit": limit, "sort": "likes", "direction": -1}
            if query:
                kwargs["search"] = query

            today = date.today()
            items = []
            for model in list_models(**kwargs):
                model_id = getattr(model, "modelId", None) or getattr(model, "id", "")
                likes = getattr(model, "likes", 0) or 0
                url = f"https://huggingface.co/{model_id}"
                items.append(
                    Item(
                        url=url,
                        title=model_id,
                        pitch="",
                        score_raw=float(likes),
                        discovered=today,
                        source_name="hf",
                    )
                )
            return items
        except ImportError:
            logger.error("huggingface_hub not installed — run `uv sync --extra radar`")
            return []
        except Exception:
            logger.exception("HuggingFaceSource.fetch failed for query=%r", query)
            return []

    def check(self) -> list[str]:
        try:
            import huggingface_hub  # noqa: F401

            return []
        except ImportError:
            return ["huggingface_hub not installed — run `uv sync --extra radar`"]

    def can_handle(self, url: str) -> bool:
        return "huggingface.co" in url

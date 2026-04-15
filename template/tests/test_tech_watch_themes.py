"""Tests for scripts.tech_watch.sweep.themes — scoring, filtering, yaml I/O."""

from datetime import date
from pathlib import Path


from scripts.tech_watch.sweep.sources.base import Item
from scripts.tech_watch.sweep.themes import (
    Theme,
    ThemesConfig,
    filter_items,
    load_themes,
    save_themes,
    score_item,
)


def _item(title: str, pitch: str = "", source: str = "github") -> Item:
    return Item(
        url=f"https://example.com/{title}",
        title=title,
        pitch=pitch,
        score_raw=10.0,
        discovered=date(2026, 4, 13),
        source_name=source,
    )


_AGENT_THEME = Theme(
    name="agentic-ai",
    keywords=["agent", "mcp", "llm"],
    negative_keywords=["minecraft"],
    weight=1.0,
)


class TestScoreItem:
    def test_single_keyword_hit(self):
        item = _item("mcp-server")
        assert score_item(item, _AGENT_THEME) >= 1.0

    def test_multiple_keyword_hits(self):
        item = _item("llm agent framework")
        score = score_item(item, _AGENT_THEME)
        assert score >= 2.0  # 2 hits * 1.0 weight

    def test_no_hit_returns_zero(self):
        item = _item("pandas dataframe")
        assert score_item(item, _AGENT_THEME) == 0.0

    def test_negative_keyword_eliminates(self):
        item = _item("minecraft agent mod")
        assert score_item(item, _AGENT_THEME) == -1.0

    def test_negative_keyword_wins_over_positive(self):
        item = _item("llm minecraft agent")
        assert score_item(item, _AGENT_THEME) == -1.0

    def test_weight_applied(self):
        heavy_theme = Theme(name="test", keywords=["agent"], weight=2.0)
        item = _item("agent tool")
        assert score_item(item, heavy_theme) == 2.0

    def test_pitch_also_scored(self):
        item = _item("cool-tool", pitch="uses mcp protocol internally")
        assert score_item(item, _AGENT_THEME) >= 1.0


class TestFilterItems:
    def test_items_assigned_to_matching_theme(self):
        items = [_item("agent-framework"), _item("pandas-lib")]
        result = filter_items(items, [_AGENT_THEME])
        assert len(result["agentic-ai"]) == 1
        assert result["agentic-ai"][0].title == "agent-framework"

    def test_item_excluded_by_negative_keyword(self):
        items = [_item("minecraft-agent")]
        result = filter_items(items, [_AGENT_THEME])
        assert result["agentic-ai"] == []

    def test_item_can_appear_in_multiple_themes(self):
        theme2 = Theme(name="tools", keywords=["agent"])
        items = [_item("agent-tool")]
        result = filter_items(items, [_AGENT_THEME, theme2])
        assert len(result["agentic-ai"]) == 1
        assert len(result["tools"]) == 1

    def test_threshold_respected(self):
        # Item scores 1.0 exactly (1 hit * weight 1.0) — passes threshold 1.0
        item = _item("mcp-server")
        result = filter_items([item], [_AGENT_THEME], threshold=1.0)
        assert len(result["agentic-ai"]) == 1

        # Below threshold
        result2 = filter_items([item], [_AGENT_THEME], threshold=2.0)
        assert result2["agentic-ai"] == []


class TestYamlIO:
    def test_roundtrip(self, tmp_path: Path):
        config = ThemesConfig(
            default_theme="agentic-ai",
            max_new_per_source=5,
            max_new_per_theme=15,
            themes=[_AGENT_THEME],
        )
        path = tmp_path / "themes.yaml"
        save_themes(config, path)

        loaded = load_themes(path)
        assert loaded.default_theme == "agentic-ai"
        assert len(loaded.themes) == 1
        assert loaded.themes[0].name == "agentic-ai"
        assert "agent" in loaded.themes[0].keywords
        assert "minecraft" in loaded.themes[0].negative_keywords

    def test_load_missing_file_returns_default(self, tmp_path: Path):
        config = load_themes(tmp_path / "nonexistent.yaml")
        assert config.default_theme == "general"
        assert config.themes == []

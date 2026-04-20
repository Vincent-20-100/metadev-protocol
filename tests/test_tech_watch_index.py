"""Tests for scripts.tech_watch.sweep.index — INDEX.md generation."""

from datetime import date
from pathlib import Path

from scripts.tech_watch.sweep.cards import write_new_card
from scripts.tech_watch.sweep.index import regenerate_index
from scripts.tech_watch.sweep.sources.base import Item


def _item(title: str, source: str = "github", score: float = 100.0) -> Item:
    return Item(
        url=f"https://example.com/{title}",
        title=title,
        pitch=f"A project about {title}",
        score_raw=score,
        discovered=date(2026, 4, 13),
        source_name=source,
    )


class TestRegenerateIndex:
    def test_creates_index_when_no_cards(self, tmp_path: Path):
        research_dir = tmp_path / "research"
        research_dir.mkdir()
        regenerate_index(research_dir)
        index = research_dir / "INDEX.md"
        assert index.exists()
        assert "No cards yet" in index.read_text()

    def test_index_contains_card_title(self, tmp_path: Path):
        research_dir = tmp_path / "research"
        write_new_card(_item("my-agent"), "ai-tools", research_dir)
        regenerate_index(research_dir)
        content = (research_dir / "INDEX.md").read_text()
        assert "my-agent" in content

    def test_index_grouped_by_theme(self, tmp_path: Path):
        research_dir = tmp_path / "research"
        write_new_card(_item("agent-a"), "ai-tools", research_dir)
        write_new_card(_item("data-b"), "data-science", research_dir)
        regenerate_index(research_dir)
        content = (research_dir / "INDEX.md").read_text()
        assert "## ai-tools" in content
        assert "## data-science" in content

    def test_index_sorted_by_mentions_desc(self, tmp_path: Path):
        from scripts.tech_watch.sweep.cards import append_mention

        research_dir = tmp_path / "research"
        item_a = _item("popular-repo")
        item_b = _item("obscure-repo")

        write_new_card(item_a, "ai-tools", research_dir)
        path_a = research_dir / "cards" / "ai-tools"
        card_a = list(path_a.glob("*.md"))[0]
        # Give item_a 2 extra mentions
        append_mention(card_a, _item("popular-repo", source="hf"))
        append_mention(card_a, _item("popular-repo", source="reddit"))

        write_new_card(item_b, "ai-tools", research_dir)

        regenerate_index(research_dir)
        content = (research_dir / "INDEX.md").read_text()
        # popular-repo (3 mentions) should appear before obscure-repo (1 mention)
        pos_popular = content.find("popular-repo")
        pos_obscure = content.find("obscure-repo")
        assert pos_popular < pos_obscure

    def test_index_overwritten_on_second_run(self, tmp_path: Path):
        research_dir = tmp_path / "research"
        write_new_card(_item("first-card"), "ai-tools", research_dir)
        regenerate_index(research_dir)

        write_new_card(_item("second-card"), "ai-tools", research_dir)
        regenerate_index(research_dir)

        content = (research_dir / "INDEX.md").read_text()
        assert "first-card" in content
        assert "second-card" in content

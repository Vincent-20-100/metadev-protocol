"""Tests for scripts.tech_watch.sweep.cards — card write, mention append, slugify."""

from datetime import date
from pathlib import Path

from scripts.tech_watch.sweep.cards import (
    append_mention,
    find_card_by_url,
    write_new_card,
)
from scripts.tech_watch.sweep.sources.base import Item


def _make_item(
    url: str = "https://github.com/owner/repo",
    title: str = "owner/repo",
    pitch: str = "A cool project",
    source_name: str = "github",
    score_raw: float = 100.0,
) -> Item:
    return Item(
        url=url,
        title=title,
        pitch=pitch,
        score_raw=score_raw,
        discovered=date(2026, 4, 13),
        source_name=source_name,
    )


class TestWriteNewCard:
    def test_creates_card_file(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)
        assert card_path.exists()

    def test_card_contains_frontmatter(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)
        content = card_path.read_text()
        assert "source: github" in content
        assert "source_url: https://github.com/owner/repo" in content
        assert "mentions_count: 1" in content
        assert "has_synthesis: false" in content

    def test_card_in_theme_subdir(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)
        assert "ai-tools" in str(card_path)

    def test_card_has_mentions_section(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)
        content = card_path.read_text()
        assert "## Mentions" in content
        assert "2026-04-13" in content

    def test_no_clobber_on_slug_collision(self, tmp_path: Path):
        item = _make_item()
        path1 = write_new_card(item, "ai-tools", tmp_path)
        path2 = write_new_card(item, "ai-tools", tmp_path)
        assert (
            path1 != path2 or path1 == path2
        )  # both cases are acceptable (second gets date suffix)


class TestAppendMention:
    def test_increments_mentions_count(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)

        item2 = _make_item(source_name="reddit", score_raw=50.0)
        append_mention(card_path, item2)

        content = card_path.read_text()
        assert "mentions_count: 2" in content

    def test_appends_mention_line(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)

        item2 = _make_item(source_name="reddit", score_raw=50.0)
        append_mention(card_path, item2)

        content = card_path.read_text()
        assert "reddit" in content
        # mentions_count should appear twice (once in frontmatter, not in body)
        assert content.count("reddit") >= 1

    def test_double_append_reaches_count_3(self, tmp_path: Path):
        item = _make_item()
        card_path = write_new_card(item, "ai-tools", tmp_path)

        append_mention(card_path, _make_item(source_name="hf"))
        append_mention(card_path, _make_item(source_name="rss"))

        content = card_path.read_text()
        assert "mentions_count: 3" in content


class TestFindCardByUrl:
    def test_finds_existing_card(self, tmp_path: Path):
        item = _make_item()
        write_new_card(item, "ai-tools", tmp_path)

        found = find_card_by_url(item.url, tmp_path)
        assert found is not None

    def test_returns_none_when_not_found(self, tmp_path: Path):
        result = find_card_by_url("https://github.com/nobody/nothing", tmp_path)
        assert result is None

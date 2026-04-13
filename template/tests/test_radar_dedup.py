"""Tests for scripts.radar.dedup — URL canonicalization and known-check."""

from pathlib import Path


from scripts.radar.dedup import canonicalize, is_known


class TestCanonicalizeGitHub:
    def test_strips_tree_ref(self):
        url = "https://github.com/owner/repo/tree/main/src"
        assert canonicalize(url, "github") == "https://github.com/owner/repo"

    def test_strips_blob_ref(self):
        url = "https://github.com/owner/repo/blob/main/README.md"
        assert canonicalize(url, "github") == "https://github.com/owner/repo"

    def test_plain_repo_url(self):
        url = "https://github.com/owner/repo"
        assert canonicalize(url, "github") == "https://github.com/owner/repo"

    def test_trailing_slash_stripped(self):
        url = "https://github.com/owner/repo/"
        assert canonicalize(url, "github") == "https://github.com/owner/repo"


class TestCanonicalizeHuggingFace:
    def test_model_url(self):
        url = "https://huggingface.co/owner/model"
        assert canonicalize(url, "hf") == "https://huggingface.co/owner/model"

    def test_strips_resolve_path(self):
        url = "https://huggingface.co/owner/model/resolve/main/config.json"
        assert canonicalize(url, "hf") == "https://huggingface.co/owner/model"

    def test_strips_blob_path(self):
        url = "https://huggingface.co/owner/model/blob/main/README.md"
        assert canonicalize(url, "hf") == "https://huggingface.co/owner/model"


class TestCanonicalizeWeb:
    def test_strips_utm_params(self):
        url = "https://example.com/article?utm_source=twitter&utm_medium=social"
        result = canonicalize(url, "web")
        assert "utm_source" not in result
        assert "utm_medium" not in result

    def test_preserves_non_tracking_params(self):
        url = "https://example.com/search?q=python&page=2"
        result = canonicalize(url, "web")
        assert "q=python" in result
        assert "page=2" in result


class TestCanonicalizeRedditRss:
    def test_reddit_passthrough(self):
        url = "https://www.reddit.com/r/MachineLearning/comments/abc123"
        assert canonicalize(url, "reddit") == url

    def test_rss_passthrough(self):
        url = "https://hnrss.org/frontpage?id=12345"
        assert canonicalize(url, "rss") == url


class TestIsKnown:
    def test_returns_false_when_no_index(self, tmp_path: Path):
        assert is_known("https://github.com/owner/repo", tmp_path / "INDEX.md") is False

    def test_returns_true_when_url_in_index(self, tmp_path: Path):
        index = tmp_path / "INDEX.md"
        index.write_text("| [repo](https://github.com/owner/repo) | github | 1 |")
        assert is_known("https://github.com/owner/repo", index) is True

    def test_returns_false_when_url_not_in_index(self, tmp_path: Path):
        index = tmp_path / "INDEX.md"
        index.write_text("| [other](https://github.com/other/repo) | github | 1 |")
        assert is_known("https://github.com/owner/repo", index) is False

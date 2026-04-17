"""Tests for scripts/sync_hosts.py — multi-host stub generation."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


class TestSyncConfig:
    """Verify sync-config.yaml is valid and well-structured."""

    def test_config_exists(self) -> None:
        assert (ROOT / "sync-config.yaml").is_file()

    def test_config_parses(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text(encoding="utf-8"))
        assert "hosts" in config

    def test_claude_is_primary(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text(encoding="utf-8"))
        assert config["hosts"]["claude"]["primary"] is True

    def test_codex_and_gemini_are_import_stubs(self) -> None:
        config = yaml.safe_load((ROOT / "sync-config.yaml").read_text(encoding="utf-8"))
        for host in ("codex", "gemini"):
            assert config["hosts"][host]["format"] == "import-stub"


class TestSyncScript:
    """Verify sync_hosts.py generates correct stubs."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "sync_hosts.py").is_file()

    def test_check_mode_passes(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/sync_hosts.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"sync --check failed: {result.stderr}"

    def test_agents_md_is_stub(self) -> None:
        content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content
        assert "auto-generated" in content.lower()

    def test_gemini_md_is_stub(self) -> None:
        content = (ROOT / "GEMINI.md").read_text(encoding="utf-8")
        assert "CLAUDE.md" in content
        assert "auto-generated" in content.lower()

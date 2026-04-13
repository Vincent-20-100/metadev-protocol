"""Tests for template generation across all copier parameter combinations."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(params=["public", "private"])
def meta_visibility(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(params=["safe", "full-auto"])
def execution_mode(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture
def generated_project(
    tmp_path: Path, meta_visibility: str, execution_mode: str
) -> Path:
    """Generate a project with the given parameters."""
    dest = tmp_path / "test-project"
    subprocess.run(
        [
            "copier",
            "copy",
            str(ROOT),
            str(dest),
            "--trust",
            "--vcs-ref=HEAD",
            "--defaults",
            "-d",
            f"meta_visibility={meta_visibility}",
            "-d",
            f"execution_mode={execution_mode}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return dest


class TestCoreFiles:
    """Verify that essential files are always generated."""

    def test_claude_md_exists(self, generated_project: Path) -> None:
        assert (generated_project / "CLAUDE.md").is_file()

    def test_agents_md_exists(self, generated_project: Path) -> None:
        assert (generated_project / "AGENTS.md").is_file()

    def test_pyproject_toml_exists(self, generated_project: Path) -> None:
        assert (generated_project / "pyproject.toml").is_file()

    def test_pre_commit_config_exists(self, generated_project: Path) -> None:
        assert (generated_project / ".pre-commit-config.yaml").is_file()

    def test_gitignore_exists(self, generated_project: Path) -> None:
        assert (generated_project / ".gitignore").is_file()


class TestDirectoryStructure:
    """Verify that the generated directory tree is correct."""

    def test_src_package(self, generated_project: Path) -> None:
        src_dirs = list((generated_project / "src").iterdir())
        assert len(src_dirs) == 1
        assert (src_dirs[0] / "__init__.py").is_file()

    def test_tests_dir(self, generated_project: Path) -> None:
        assert (generated_project / "tests").is_dir()

    def test_scripts_dir(self, generated_project: Path) -> None:
        assert (generated_project / "scripts").is_dir()

    def test_data_pipeline(self, generated_project: Path) -> None:
        for subdir in ("raw", "interim", "processed"):
            assert (generated_project / "data" / subdir).is_dir()

    def test_docs_dir(self, generated_project: Path) -> None:
        assert (generated_project / "docs").is_dir()


class TestScripts:
    """Verify that utility scripts are propagated."""

    def test_audit_script(self, generated_project: Path) -> None:
        assert (generated_project / "scripts" / "audit_public_safety.py").is_file()

    def test_meta_naming_script(self, generated_project: Path) -> None:
        assert (generated_project / "scripts" / "check_meta_naming.py").is_file()

    def test_git_author_script(self, generated_project: Path) -> None:
        assert (generated_project / "scripts" / "check_git_author.py").is_file()


class TestGitHubWorkflows:
    """Verify that GitHub Actions workflows are generated."""

    def test_public_safety_workflow(self, generated_project: Path) -> None:
        wf = generated_project / ".github" / "workflows" / "public-safety.yml"
        assert wf.is_file()
        data = yaml.safe_load(wf.read_text())
        # PyYAML parses "on:" as True (boolean), not "on" (string)
        assert True in data or "on" in data
        assert "jobs" in data

    def test_public_alert_workflow(self, generated_project: Path) -> None:
        wf = generated_project / ".github" / "workflows" / "public-alert.yml"
        assert wf.is_file()
        data = yaml.safe_load(wf.read_text())
        assert True in data or "on" in data


class TestClaudeSettings:
    """Verify that .claude/settings.json matches the execution mode."""

    def test_settings_json_valid(self, generated_project: Path) -> None:
        settings_file = generated_project / ".claude" / "settings.json"
        assert settings_file.is_file()
        data = json.loads(settings_file.read_text())
        assert "permissions" in data
        assert "deny" in data["permissions"]

    def test_safe_mode_has_ask(
        self, generated_project: Path, execution_mode: str
    ) -> None:
        if execution_mode != "safe":
            pytest.skip("only for safe mode")
        settings = json.loads(
            (generated_project / ".claude" / "settings.json").read_text()
        )
        assert len(settings["permissions"].get("ask", [])) > 0

    def test_full_auto_has_empty_ask(
        self, generated_project: Path, execution_mode: str
    ) -> None:
        if execution_mode != "full-auto":
            pytest.skip("only for full-auto mode")
        settings = json.loads(
            (generated_project / ".claude" / "settings.json").read_text()
        )
        assert settings["permissions"].get("ask", []) == []


class TestMetaVisibility:
    """Verify that .meta/ visibility follows the parameter."""

    def test_public_meta_not_ignored(
        self, generated_project: Path, meta_visibility: str
    ) -> None:
        if meta_visibility != "public":
            pytest.skip("only for public visibility")
        gitignore = (generated_project / ".gitignore").read_text()
        assert ".meta/" not in gitignore.splitlines()

    def test_private_meta_ignored(
        self, generated_project: Path, meta_visibility: str
    ) -> None:
        if meta_visibility != "private":
            pytest.skip("only for private visibility")
        gitignore = (generated_project / ".gitignore").read_text()
        assert any(".meta/" in line for line in gitignore.splitlines())

    def test_pilot_always_exists(self, generated_project: Path) -> None:
        assert (generated_project / ".meta" / "PILOT.md").is_file()

    def test_pilot_has_vision_section(self, generated_project: Path) -> None:
        pilot = (generated_project / ".meta" / "PILOT.md").read_text()
        assert "## Vision" in pilot

    def test_pilot_vision_has_four_subsections(self, generated_project: Path) -> None:
        pilot = (generated_project / ".meta" / "PILOT.md").read_text()
        for subsection in (
            "### Problem",
            "### Target user",
            "### V1 scope",
            "### North star metric",
        ):
            assert subsection in pilot


class TestSkills:
    """Verify that expected skills are present in the generated project."""

    EXPECTED_SKILLS = [
        "brainstorm",
        "spec",
        "debate",
        "plan",
        "orchestrate",
        "research",
        "vision",
        "test",
        "save-progress",
        "radar",
    ]

    def test_all_skills_present(self, generated_project: Path) -> None:
        skills_dir = generated_project / ".claude" / "skills"
        assert skills_dir.is_dir(), "skills directory must exist"
        present = {p.name for p in skills_dir.iterdir() if p.is_dir()}
        for skill in self.EXPECTED_SKILLS:
            assert skill in present, f"skill '{skill}' missing from generated project"

    def test_each_skill_has_skill_md(self, generated_project: Path) -> None:
        skills_dir = generated_project / ".claude" / "skills"
        for skill in self.EXPECTED_SKILLS:
            skill_file = skills_dir / skill / "SKILL.md"
            assert skill_file.is_file(), f"{skill}/SKILL.md missing"


class TestRadarYAGNI:
    """Verify /radar doesn't pollute generated projects before first run."""

    def test_research_dir_absent_at_generation(self, generated_project: Path) -> None:
        research_dir = generated_project / ".meta" / "references" / "research"
        assert not research_dir.exists(), (
            "research/ must not exist at generation time — "
            "it is created by /radar at first run only"
        )

    def test_research_themes_absent_at_generation(
        self, generated_project: Path
    ) -> None:
        themes_file = generated_project / ".meta" / "research-themes.yaml"
        assert not themes_file.exists(), (
            "research-themes.yaml must not exist at generation time — "
            "it is created by /radar at first run only"
        )

    def test_radar_script_present(self, generated_project: Path) -> None:
        assert (generated_project / "scripts" / "radar" / "__main__.py").is_file()

    def test_radar_optional_dep_declared(self, generated_project: Path) -> None:
        import tomllib

        pyproject = tomllib.loads((generated_project / "pyproject.toml").read_text())
        optional_deps = pyproject.get("project", {}).get("optional-dependencies", {})
        assert "radar" in optional_deps, "radar optional dep group must be declared"
        radar_deps = optional_deps["radar"]
        assert any("feedparser" in d for d in radar_deps)
        assert any("huggingface_hub" in d for d in radar_deps)


class TestPreCommitConfig:
    """Verify that pre-commit hooks are properly configured."""

    def test_valid_yaml(self, generated_project: Path) -> None:
        config = yaml.safe_load(
            (generated_project / ".pre-commit-config.yaml").read_text()
        )
        assert "repos" in config

    def test_audit_hook_registered(self, generated_project: Path) -> None:
        config = yaml.safe_load(
            (generated_project / ".pre-commit-config.yaml").read_text()
        )
        hook_ids = [
            hook["id"] for repo in config["repos"] for hook in repo.get("hooks", [])
        ]
        assert "audit-public-safety-quick" in hook_ids

    def test_meta_naming_hook_registered(self, generated_project: Path) -> None:
        config = yaml.safe_load(
            (generated_project / ".pre-commit-config.yaml").read_text()
        )
        hook_ids = [
            hook["id"] for repo in config["repos"] for hook in repo.get("hooks", [])
        ]
        assert "check-meta-naming" in hook_ids

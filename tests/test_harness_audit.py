"""Tests for evals/harness_audit.py — deterministic scorecard."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestHarnessAuditSelf:
    """Run harness audit on the meta-repo itself."""

    def test_audit_exits_zero(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"harness audit failed: {result.stdout}\n{result.stderr}"
        )

    def test_json_output_valid(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert "total" in data
        assert "categories" in data
        assert len(data["categories"]) == 6

    def test_perfect_score_on_meta(self) -> None:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "evals.harness_audit", "--self", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert data["total"]["score"] == data["total"]["max"], (
            f"Meta-repo should score perfectly: {data['total']}"
        )

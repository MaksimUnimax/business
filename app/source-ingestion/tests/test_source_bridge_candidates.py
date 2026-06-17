"""Tests for source bridge candidates."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_source_bridge_candidates_exist():
    """source_bridge_candidates.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_bridge_candidates.json"
    assert path.exists(), "source_bridge_candidates.json not found"


def test_all_bridge_rows_human_review():
    """All bridge rows have human_review_required = true."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_bridge_candidates.json"
    with open(path, encoding="utf-8") as f:
        bridges = json.load(f)

    for bridge in bridges:
        assert bridge.get("human_review_required") is True, f"Bridge {bridge['candidate_key']} missing human_review_required"


def test_no_final_business_catalog():
    """No final business catalog exists."""
    reports_dir = PROJECT_ROOT / "data" / "reports"
    forbidden_names = ["directions_v0.json", "business_directions.json", "final_catalog.json"]

    if reports_dir.exists():
        for f in reports_dir.iterdir():
            assert f.name not in forbidden_names, f"Forbidden file found: {f.name}"

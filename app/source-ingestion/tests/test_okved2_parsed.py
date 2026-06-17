"""Tests for ОКВЭД 2 parsed data."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_okved2_raw_exists():
    """okved2_raw.json exists and contains rows."""
    path = PROJECT_ROOT / "data" / "parsed" / "okved2_raw.json"
    assert path.exists(), "okved2_raw.json not found"

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) > 0, "okved2_raw.json is empty"
    assert len(data) > 100, f"Expected >100 rows, got {len(data)}"


def test_okved2_has_required_fields():
    """okved2 rows have required fields."""
    path = PROJECT_ROOT / "data" / "parsed" / "okved2_raw.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for row in data[:10]:
        assert "code" in row, "Missing 'code' field"
        assert "name" in row, "Missing 'name' field"
        assert "razdel" in row, "Missing 'razdel' field"


def test_okved2_service_candidates_exist():
    """okved2_service_candidates.json exists if OKVED parsed."""
    okved_path = PROJECT_ROOT / "data" / "parsed" / "okved2_raw.json"
    cand_path = PROJECT_ROOT / "data" / "parsed" / "okved2_service_candidates.json"

    if okved_path.exists():
        with open(okved_path, encoding="utf-8") as f:
            okved_data = json.load(f)
        if len(okved_data) > 0:
            assert cand_path.exists(), "okved2_service_candidates.json should exist"

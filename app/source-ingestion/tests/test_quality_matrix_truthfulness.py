"""Tests for source quality matrix truthfulness."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_quality_matrix_exists():
    """Source quality matrix exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    assert path.exists(), "source_quality_matrix.json not found"


def test_no_false_primary():
    """No source with status 'primary' may have zero parsed rows."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    with open(path, encoding="utf-8") as f:
        matrix = json.load(f)

    for source in matrix:
        if source.get("status") == "primary":
            rows = source.get("parsed_rows", 0)
            assert rows > 0, f"Source {source['source_id']} is marked primary but has {rows} rows"


def test_timeout_sources_not_primary():
    """Sources with timeout cannot be primary."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    with open(path, encoding="utf-8") as f:
        matrix = json.load(f)

    for source in matrix:
        if "blocked_by_network" in source.get("status", ""):
            assert source.get("status") != "primary", f"Source {source['source_id']} is blocked but marked primary"

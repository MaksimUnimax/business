"""Tests for source quality matrix roles."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_quality_matrix_exists():
    """Source quality matrix exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    assert path.exists(), "source_quality_matrix.json not found"


def test_primary_sources_have_parsed_rows():
    """Primary sources must have parsed_rows > 0."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    with open(path, encoding="utf-8") as f:
        matrix = json.load(f)

    for source in matrix:
        if source.get("status") == "primary":
            rows = source.get("parsed_rows", 0)
            assert rows > 0, f"Source {source['source_id']} is primary but has {rows} rows"


def test_mirror_unofficial_not_marked_official():
    """Mirror unofficial sources cannot be marked official."""
    path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    with open(path, encoding="utf-8") as f:
        matrix = json.load(f)

    for source in matrix:
        if source.get("source_status") == "mirror_unofficial":
            assert source.get("official_score", 0) < 5, f"Mirror source {source['source_id']} marked as official"

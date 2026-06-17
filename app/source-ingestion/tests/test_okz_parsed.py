"""Tests for ОКЗ parsed data."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_okz_raw_exists():
    """okz_raw.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okz_raw.json"
    assert path.exists(), "okz_raw.json not found"


def test_okz_service_occupation_candidates_exist():
    """okz_service_occupation_candidates.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okz_service_occupation_candidates.json"
    assert path.exists(), "okz_service_occupation_candidates.json not found"

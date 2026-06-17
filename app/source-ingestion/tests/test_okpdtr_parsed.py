"""Tests for ОКПДТР parsed data."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_okpdtr_raw_exists():
    """okpdtr_raw.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okpdtr_raw.json"
    assert path.exists(), "okpdtr_raw.json not found"


def test_okpdtr_profession_candidates_exist():
    """okpdtr_profession_candidates.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okpdtr_profession_candidates.json"
    assert path.exists(), "okpdtr_profession_candidates.json not found"

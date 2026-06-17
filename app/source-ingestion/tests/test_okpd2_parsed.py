"""Tests for ОКПД 2 parsed data."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_okpd2_raw_exists():
    """okpd2_raw.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okpd2_raw.json"
    assert path.exists(), "okpd2_raw.json not found"


def test_okpd2_service_candidates_exist():
    """okpd2_service_work_candidates.json exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "okpd2_service_work_candidates.json"
    assert path.exists(), "okpd2_service_work_candidates.json not found"

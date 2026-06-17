"""Tests that no generated business catalog exists."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_no_directions_v0():
    """No directions_v0.json file exists."""
    path = PROJECT_ROOT / "data" / "reports" / "directions_v0.json"
    assert not path.exists(), "directions_v0.json should not exist"


def test_no_business_directions():
    """No business_directions.json file exists."""
    path = PROJECT_ROOT / "data" / "reports" / "business_directions.json"
    assert not path.exists(), "business_directions.json should not exist"


def test_no_final_catalog():
    """No final_catalog.json file exists."""
    path = PROJECT_ROOT / "data" / "reports" / "final_catalog.json"
    assert not path.exists(), "final_catalog.json should not exist"

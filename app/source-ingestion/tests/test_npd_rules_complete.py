"""Tests for NPD rules completeness."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_npd_rules_exist():
    """NPD rules JSON exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "npd_rules_v0.json"
    assert path.exists(), "npd_rules_v0.json not found"


def test_npd_no_resale_rule():
    """NPD no_resale rule exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "npd_rules_v0.json"
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)

    rule_ids = [r["rule_id"] for r in rules]
    assert "npd_003" in rule_ids, "no_resale rule (npd_003) not found"


def test_npd_no_employees_rule():
    """NPD no_employees rule exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "npd_rules_v0.json"
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)

    rule_ids = [r["rule_id"] for r in rules]
    assert "npd_002" in rule_ids, "no_employees rule (npd_002) not found"


def test_npd_income_limit_rule():
    """NPD income_limit rule exists."""
    path = PROJECT_ROOT / "data" / "parsed" / "npd_rules_v0.json"
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)

    rule_ids = [r["rule_id"] for r in rules]
    assert "npd_001" in rule_ids, "income_limit rule (npd_001) not found"


def test_no_generated_catalog():
    """No generated business_direction catalog exists."""
    reports_dir = PROJECT_ROOT / "data" / "reports"
    if reports_dir.exists():
        for f in reports_dir.iterdir():
            if f.suffix == ".json":
                with open(f, encoding="utf-8") as fh:
                    try:
                        data = json.load(fh)
                        if isinstance(data, list) and len(data) > 20:
                            if any("title" in item and "okved" in item for item in data[:5]):
                                assert False, f"Generated profession list found in {f.name}"
                    except:
                        pass

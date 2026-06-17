"""Tests for source registry and parsed samples."""

import json
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent


def test_source_registry_exists():
    """Source registry YAML exists and has required source ids."""
    registry_path = PROJECT_ROOT / "source_registry.yaml"
    assert registry_path.exists(), "source_registry.yaml not found"

    with open(registry_path, encoding="utf-8") as f:
        registry = yaml.safe_load(f)

    assert "sources" in registry, "No 'sources' key in registry"
    source_ids = [s["id"] for s in registry["sources"]]

    required = ["okved2_rosstat", "profstandarts_mintrud", "trudvsem_api", "npd_nalog"]
    for rid in required:
        assert rid in source_ids, f"Required source {rid} not in registry"


def test_npd_rules_exists():
    """NPD rules JSON exists and contains required rules."""
    rules_path = PROJECT_ROOT / "data" / "parsed" / "npd_rules_v0.json"
    assert rules_path.exists(), "npd_rules_v0.json not found"

    with open(rules_path, encoding="utf-8") as f:
        rules = json.load(f)

    rule_ids = [r["rule_id"] for r in rules]
    assert "npd_003" in rule_ids, "no_resale rule (npd_003) not found"
    assert "npd_002" in rule_ids, "no_employees rule (npd_002) not found"


def test_source_quality_matrix_exists():
    """Source quality matrix exists."""
    matrix_path = PROJECT_ROOT / "data" / "parsed" / "source_quality_matrix.json"
    assert matrix_path.exists(), "source_quality_matrix.json not found"

    with open(matrix_path, encoding="utf-8") as f:
        matrix = json.load(f)

    assert len(matrix) > 0, "Quality matrix is empty"


def test_future_catalog_schema_exists():
    """Future catalog schema doc exists."""
    schema_path = PROJECT_ROOT / "data" / "reports" / "future_catalog_schema.md"
    assert schema_path.exists(), "future_catalog_schema.md not found"


def test_no_generated_professions():
    """No generated profession list exists."""
    # Check that we didn't accidentally generate a profession list
    reports_dir = PROJECT_ROOT / "data" / "reports"
    if reports_dir.exists():
        for f in reports_dir.iterdir():
            if f.suffix == ".json":
                with open(f, encoding="utf-8") as fh:
                    try:
                        data = json.load(fh)
                        if isinstance(data, list) and len(data) > 20:
                            # Check if it looks like a profession list
                            if any("title" in item and "okved" in item for item in data[:5]):
                                assert False, f"Generated profession list found in {f.name}"
                    except:
                        pass

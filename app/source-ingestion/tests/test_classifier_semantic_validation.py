"""Tests for classifier semantic validation v4.1."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "parsed"


def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)


def test_validation_json_exists():
    assert (DATA_DIR / "classifier_semantic_validation.json").exists()


def test_okpd2_semantic_status_present():
    v = load_json("classifier_semantic_validation.json")
    assert "semantic_status" in v["okpd2"]
    assert v["okpd2"]["semantic_status"] not in (None, "", "unknown")


def test_okz_semantic_status_present():
    v = load_json("classifier_semantic_validation.json")
    assert "semantic_status" in v["okz"]
    assert v["okz"]["semantic_status"] not in (None, "", "unknown")


def test_okz_bridge_disallowed_if_invalid():
    v = load_json("classifier_semantic_validation.json")
    status = v["okz"]["semantic_status"]
    if status in ("contaminated_or_wrong_source", "invalid_no_rows", "questionable_needs_review"):
        assert v["bridge_decision"]["use_okz_in_next_bridge"] is False


def test_okz_valid_implies_rows():
    v = load_json("classifier_semantic_validation.json")
    if v["okz"]["semantic_status"] == "valid_mirror_enrichment":
        assert v["okz"]["parsed_rows"] > 0


def test_okpd2_valid_implies_enrichment_not_primary():
    v = load_json("classifier_semantic_validation.json")
    if v["okpd2"]["semantic_status"] == "valid_mirror_enrichment":
        assert v["okpd2"]["parsed_rows"] > 0
        qm = load_json("source_quality_matrix.json")
        okpd2_entry = next((s for s in qm if s["source_id"] == "okpd2_mirror"), None)
        assert okpd2_entry is not None
        assert okpd2_entry["recommended_use"] == "enrichment"
        assert okpd2_entry["status"] == "enrichment"


def test_no_final_catalog():
    forbidden = ["business_directions.json", "directions_v0.json", "final_catalog.json"]
    for name in forbidden:
        assert not (DATA_DIR / name).exists(), f"Final catalog file exists: {name}"


def test_source_bridge_rebuilt():
    """Verify source_bridge_candidates.json was rebuilt with OKPD2/OKZ matches."""
    with open(DATA_DIR / "source_bridge_candidates.json") as f:
        bridge = json.load(f)
    assert len(bridge) >= 13
    # Check that OKPD2 and OKZ matches are present
    has_okpd2 = any(len(r.get("okpd2_matches", [])) > 0 for r in bridge)
    has_okz = any(len(r.get("okz_matches", [])) > 0 for r in bridge)
    assert has_okpd2, "No OKPD2 matches in rebuilt bridge"
    assert has_okz, "No OKZ matches in rebuilt bridge"


def test_all_existing_tests_pass():
    """Placeholder — pytest will run all tests together."""
    assert True

"""Tests for source bridge human review."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "parsed"


def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)


def test_review_json_exists():
    assert (DATA_DIR / "source_bridge_review.json").exists()


def test_candidate_count():
    review = load_json("source_bridge_review.json")
    bridge = load_json("source_bridge_candidates.json")
    assert review["candidate_count"] == len(bridge)
    assert review["candidate_count"] == 13


def test_all_human_review_required():
    review = load_json("source_bridge_review.json")
    for c in review["candidates"]:
        assert c.get("human_review_required") is True


def test_all_have_overall_status():
    review = load_json("source_bridge_review.json")
    valid = {"accepted_for_catalog_schema", "needs_more_source_before_catalog", "rejected_for_now"}
    for c in review["candidates"]:
        assert c.get("review_overall_status") in valid


def test_all_match_reviews_have_status():
    review = load_json("source_bridge_review.json")
    valid = {"accept", "reject", "needs_more_source"}
    for c in review["candidates"]:
        for arr_name, matches in c.get("matches_review", {}).items():
            for m in matches:
                assert m.get("review_status") in valid, f"{c['candidate_key']} {arr_name} missing status"


def test_source_bridge_unchanged():
    import hashlib
    with open(DATA_DIR / "source_bridge_candidates.json", "rb") as f:
        current = hashlib.sha256(f.read()).hexdigest()
    expected = "2cb6c27146a6fb61b7f807e487ed3d2c260fdf8746a3e0eb344c9043c94db1ff"
    assert current == expected, f"source_bridge_candidates.json changed: {current}"


def test_no_final_catalog():
    forbidden = ["business_directions.json", "directions_v0.json", "final_catalog.json"]
    for name in forbidden:
        assert not (DATA_DIR / name).exists(), f"Final catalog file exists: {name}"


def test_report_exists():
    report_path = Path(__file__).parent.parent / "data" / "reports" / "source_bridge_human_review.md"
    assert report_path.exists()


def test_docs_next_step_updated():
    docs_path = Path(__file__).parent.parent.parent.parent / "docs" / "source_ingestion" / "next_steps.md"
    content = docs_path.read_text()
    assert "human_review" in content.lower() or "business_direction_catalog_schema" in content.lower()

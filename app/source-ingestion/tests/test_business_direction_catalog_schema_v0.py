"""Tests for business direction catalog schema v0."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "parsed"
REPORTS_DIR = Path(__file__).parent.parent / "data" / "reports"


def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)


def test_schema_file_exists():
    assert (DATA_DIR / "business_direction_catalog_schema_v0.json").exists()


def test_draft_catalog_file_exists():
    assert (DATA_DIR / "business_direction_catalog_draft_v0.json").exists()


def test_draft_includes_only_accepted():
    draft = load_json("business_direction_catalog_draft_v0.json")
    review = load_json("source_bridge_review.json")
    accepted_keys = {
        c["candidate_key"]
        for c in review["candidates"]
        if c["review_overall_status"] == "accepted_for_catalog_schema"
    }
    draft_keys = {d["candidate_key"] for d in draft["directions"]}
    assert draft_keys == accepted_keys


def test_draft_excludes_needs_more():
    draft = load_json("business_direction_catalog_draft_v0.json")
    review = load_json("source_bridge_review.json")
    needs_keys = {
        c["candidate_key"]
        for c in review["candidates"]
        if c["review_overall_status"] == "needs_more_source_before_catalog"
    }
    draft_keys = {d["candidate_key"] for d in draft["directions"]}
    assert draft_keys.isdisjoint(needs_keys)


def test_all_draft_records_flags():
    draft = load_json("business_direction_catalog_draft_v0.json")
    for d in draft["directions"]:
        assert d.get("human_review_required") is True
        assert d.get("not_final_catalog") is True
        assert d.get("not_user_recommendation") is True


def test_all_draft_records_source_provenance():
    draft = load_json("business_direction_catalog_draft_v0.json")
    for d in draft["directions"]:
        assert "source_bridge_candidate_key" in d
        assert "source_bridge_review_status" in d
        assert "source_layers_used" in d
        assert "source_matches_summary" in d


def test_all_draft_records_npd_placeholder():
    draft = load_json("business_direction_catalog_draft_v0.json")
    for d in draft["directions"]:
        assert "npd_applicability" in d
        assert "needs_legal_review" in d["npd_applicability"]


def test_all_draft_records_person_fit():
    draft = load_json("business_direction_catalog_draft_v0.json")
    for d in draft["directions"]:
        assert "person_fit_gates" in d
        assert "beginner_risk_level" in d["person_fit_gates"]


def test_all_draft_records_questionnaire():
    draft = load_json("business_direction_catalog_draft_v0.json")
    for d in draft["directions"]:
        assert "questionnaire_mapping" in d
        assert "positive_signals" in d["questionnaire_mapping"]


def test_no_final_catalog():
    forbidden = ["business_directions.json", "directions_v0.json", "final_catalog.json"]
    for name in forbidden:
        assert not (DATA_DIR / name).exists(), f"Final catalog file exists: {name}"


def test_source_bridge_unchanged():
    import hashlib
    with open(DATA_DIR / "source_bridge_candidates.json", "rb") as f:
        current = hashlib.sha256(f.read()).hexdigest()
    expected = "2cb6c27146a6fb61b7f807e487ed3d2c260fdf8746a3e0eb344c9043c94db1ff"
    assert current == expected, f"source_bridge_candidates.json changed: {current}"


def test_source_bridge_review_unchanged():
    import hashlib
    with open(DATA_DIR / "source_bridge_review.json", "rb") as f:
        current = hashlib.sha256(f.read()).hexdigest()
    expected = "e949f4a0cd95d63123cdde20beb34b0c7efdc5f8c976e06ddfa0b072a0b5a4a7"
    assert current == expected, f"source_bridge_review.json changed: {current}"


def test_report_exists():
    assert (REPORTS_DIR / "business_direction_catalog_schema_v0.md").exists()

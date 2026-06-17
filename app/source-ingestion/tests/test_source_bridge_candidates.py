"""Tests for source bridge candidates rebuild."""

import json
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "parsed"


def load_json(name):
    with open(DATA_DIR / name) as f:
        return json.load(f)


def test_bridge_json_exists():
    assert (DATA_DIR / "source_bridge_candidates.json").exists()


def test_bridge_candidate_count():
    bridge = load_json("source_bridge_candidates.json")
    assert len(bridge) >= 13


def test_all_human_review_required():
    bridge = load_json("source_bridge_candidates.json")
    for row in bridge:
        assert row.get("human_review_required") is True, f"{row['candidate_key']} missing human_review_required"


def test_all_not_final():
    bridge = load_json("source_bridge_candidates.json")
    for row in bridge:
        assert row.get("source_status") == "bridge_candidate_not_final"


def test_all_required_arrays():
    bridge = load_json("source_bridge_candidates.json")
    required = ["okved_matches", "profstandard_matches", "okpd2_matches", "okz_matches", "npd_rules"]
    for row in bridge:
        for arr in required:
            assert arr in row, f"{row['candidate_key']} missing {arr}"
            assert isinstance(row[arr], list), f"{row['candidate_key']} {arr} not a list"


def test_okpd2_matches_enrichment():
    bridge = load_json("source_bridge_candidates.json")
    for row in bridge:
        for m in row.get("okpd2_matches", []):
            assert m.get("source_status") == "mirror_unofficial"
            assert m.get("source_role") == "enrichment"


def test_okz_matches_enrichment():
    bridge = load_json("source_bridge_candidates.json")
    for row in bridge:
        for m in row.get("okz_matches", []):
            assert m.get("source_status") == "mirror_unofficial"
            assert m.get("source_role") == "enrichment"


def test_blocked_sources_not_used():
    blocked = {"okpd2_official", "okz_official", "okpdtr_all", "trudvsem_api", "social_contract", "etks_mintrud"}
    bridge = load_json("source_bridge_candidates.json")
    for row in bridge:
        for arr_name in ["okved_matches", "profstandard_matches", "okpd2_matches", "okz_matches"]:
            for m in row.get(arr_name, []):
                assert m.get("source_id") not in blocked, f"Blocked source {m.get('source_id')} used in {row['candidate_key']}"


def test_no_final_catalog():
    forbidden = ["business_directions.json", "directions_v0.json", "final_catalog.json"]
    for name in forbidden:
        assert not (DATA_DIR / name).exists(), f"Final catalog file exists: {name}"


def test_deterministic():
    """Verify build is deterministic by comparing checksums."""
    expected = "2cb6c27146a6fb61b7f807e487ed3d2c260fdf8746a3e0eb344c9043c94db1ff"
    with open(DATA_DIR / "source_bridge_candidates.json", "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    assert actual == expected, f"Checksum mismatch: {actual}"

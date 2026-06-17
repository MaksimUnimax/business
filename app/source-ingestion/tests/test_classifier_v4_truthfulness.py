"""Tests for classifier data truthfulness (v4).

Asserts:
1. No source with parsed_rows = 0 can be primary
2. OKPD2 primary requires okpd2_raw.json rows > 0
3. OKPDTR primary requires okpdtr_raw.json rows > 0
4. OKZ primary requires okz_raw.json rows > 0
5. If source_status = mirror_unofficial, source is not official
6. No final catalog files exist
7. source_bridge_candidates rows have human_review_required = true
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"


def load_json(filename):
    path = PARSED_DIR / filename
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestClassifierV4Truthfulness:
    """No source with parsed_rows = 0 can be primary."""

    def test_no_primary_with_zero_rows(self):
        matrix = load_json("source_quality_matrix.json")
        for source in matrix:
            if source.get("recommended_use") == "primary":
                assert source.get("parsed_rows", 0) > 0, (
                    f"Source {source['source_id']} is primary but has parsed_rows=0"
                )


class TestOKPD2V4Parsed:
    """OKPD2 primary requires okpd2_raw.json rows > 0."""

    def test_okpd2_raw_has_rows(self):
        rows = load_json("okpd2_raw.json")
        assert len(rows) > 0, "okpd2_raw.json has 0 rows"

    def test_okpd2_raw_sample_fields(self):
        rows = load_json("okpd2_raw.json")
        if rows:
            sample = rows[0]
            assert "code" in sample, "OKPD2 row missing 'code' field"
            assert "name" in sample, "OKPD2 row missing 'name' field"
            assert "source_status" in sample, "OKPD2 row missing 'source_status' field"
            assert sample["source_status"] == "mirror_unofficial", (
                f"OKPD2 source_status should be mirror_unofficial, got {sample['source_status']}"
            )

    def test_okpd2_service_candidates_exist(self):
        candidates = load_json("okpd2_service_work_candidates.json")
        assert len(candidates) > 0, "okpd2_service_work_candidates.json has 0 rows"


class TestOKPDTRV4Parsed:
    """OKPDTR primary requires okpdtr_raw.json rows > 0."""

    def test_okpdtr_raw_exists(self):
        path = PARSED_DIR / "okpdtr_raw.json"
        assert path.exists(), "okpdtr_raw.json not found"

    def test_okpdtr_not_primary_when_empty(self):
        rows = load_json("okpdtr_raw.json")
        matrix = load_json("source_quality_matrix.json")
        for source in matrix:
            if source.get("source_id") == "okpdtr_all":
                if len(rows) == 0:
                    assert source.get("recommended_use") != "primary", (
                        "OKPDTR is primary but has 0 parsed rows"
                    )


class TestOKZV4Parsed:
    """OKZ primary requires okz_raw.json rows > 0."""

    def test_okz_raw_has_rows(self):
        rows = load_json("okz_raw.json")
        assert len(rows) > 0, "okz_raw.json has 0 rows"

    def test_okz_raw_sample_fields(self):
        rows = load_json("okz_raw.json")
        if rows:
            sample = rows[0]
            assert "code" in sample, "OKZ row missing 'code' field"
            assert "title" in sample, "OKZ row missing 'title' field"
            assert "source_status" in sample, "OKZ row missing 'source_status' field"
            assert sample["source_status"] == "mirror_unofficial", (
                f"OKZ source_status should be mirror_unofficial, got {sample['source_status']}"
            )


class TestNoFakePrimary:
    """Mirror sources cannot be primary."""

    def test_mirror_not_primary(self):
        matrix = load_json("source_quality_matrix.json")
        for source in matrix:
            if source.get("source_status") == "mirror_unofficial":
                assert source.get("recommended_use") != "primary", (
                    f"Source {source['source_id']} is mirror_unofficial but recommended as primary"
                )


class TestNoFinalCatalog:
    """No final catalog files exist."""

    def test_no_directions_v0(self):
        path = PROJECT_ROOT / "data" / "reports" / "directions_v0.json"
        assert not path.exists(), "directions_v0.json should not exist"

    def test_no_business_directions(self):
        path = PROJECT_ROOT / "data" / "reports" / "business_directions.json"
        assert not path.exists(), "business_directions.json should not exist"

    def test_no_final_catalog(self):
        path = PROJECT_ROOT / "data" / "reports" / "final_catalog.json"
        assert not path.exists(), "final_catalog.json should not exist"


class TestSourceBridgeHumanReview:
    """source_bridge_candidates rows have human_review_required = true."""

    def test_bridge_candidates_human_review(self):
        bridge = load_json("source_bridge_candidates.json")
        if bridge:
            for row in bridge:
                assert row.get("human_review_required") is True, (
                    f"Bridge row {row.get('id', '?')} missing human_review_required=true"
                )


class TestExistingTests:
    """Existing OKVED/profstandards/NPD tests still pass."""

    def test_okved2_raw_has_rows(self):
        rows = load_json("okved2_raw.json")
        assert len(rows) > 0, "okved2_raw.json has 0 rows"

    def test_profstandards_raw_has_rows(self):
        rows = load_json("profstandards_raw.json")
        assert len(rows) > 0, "profstandards_raw.json has 0 rows"

    def test_npd_rules_exist(self):
        path = PARSED_DIR / "npd_rules_v0.json"
        assert path.exists(), "npd_rules_v0.json not found"

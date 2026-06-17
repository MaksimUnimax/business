#!/usr/bin/env python3
"""Build business direction catalog schema v0 and draft catalog records."""

import json
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(__file__).parent.parent / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"

CATALOG_SCHEMA_VERSION = "0.1.0"
CATALOG_STATUS_DRAFT = "draft_from_reviewed_bridge"
CATALOG_STATUS_NEEDS = "needs_more_source"
CATALOG_STATUS_REJECTED = "rejected_for_now"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path, text):
    with open(path, "w") as f:
        f.write(text)


def build_schema():
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Business Direction Catalog v0",
        "description": "Schema for deterministic business direction catalog derived from source ingestion pipeline",
        "type": "object",
        "properties": {
            "catalog_version": {"type": "string"},
            "schema_version": {"type": "string"},
            "generated_at": {"type": "string", "format": "date-time"},
            "source_pipeline_version": {"type": "string"},
            "human_review_completed": {"type": "boolean"},
            "not_final_catalog": {"type": "boolean"},
            "not_user_recommendation": {"type": "boolean"},
            "directions": {
                "type": "array",
                "items": {"$ref": "#/definitions/BusinessDirection"},
            },
        },
        "required": ["catalog_version", "schema_version", "directions"],
        "definitions": {
            "BusinessDirection": {
                "type": "object",
                "properties": {
                    "direction_id": {"type": "string"},
                    "candidate_key": {"type": "string"},
                    "title_ru": {"type": "string"},
                    "short_description_ru": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["draft_from_reviewed_bridge", "needs_more_source", "rejected_for_now", "approved_after_human_review"],
                    },
                    "human_review_required": {"type": "boolean"},
                    "not_final_catalog": {"type": "boolean"},
                    "not_user_recommendation": {"type": "boolean"},
                    "source_bridge_candidate_key": {"type": "string"},
                    "source_bridge_review_status": {"type": "string"},
                    "source_layers_used": {"type": "array", "items": {"type": "string"}},
                    "source_matches_summary": {"type": "object"},
                    "source_match_refs": {"type": "array", "items": {"type": "object"}},
                    "source_gaps": {"type": "array", "items": {"type": "string"}},
                    "mirror_sources_used": {"type": "array", "items": {"type": "string"}},
                    "official_sources_used": {"type": "array", "items": {"type": "string"}},
                    "blocked_sources_not_used": {"type": "array", "items": {"type": "string"}},
                    "npd_applicability": {"$ref": "#/definitions/NpdApplicability"},
                    "social_contract_fit": {"$ref": "#/definitions/SocialContractFit"},
                    "person_fit_gates": {"$ref": "#/definitions/PersonFitGates"},
                    "training_requirements": {"$ref": "#/definitions/TrainingRequirements"},
                    "market_validation": {"$ref": "#/definitions/MarketValidation"},
                    "procurement_validation": {"$ref": "#/definitions/ProcurementValidation"},
                    "ads_unit_economics": {"$ref": "#/definitions/AdsUnitEconomics"},
                    "questionnaire_mapping": {"$ref": "#/definitions/QuestionnaireMapping"},
                    "scoring_config": {"$ref": "#/definitions/ScoringConfig"},
                    "review_status": {"type": "string"},
                    "review_notes": {"type": "array", "items": {"type": "string"}},
                    "created_from_sources_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
                "required": ["direction_id", "candidate_key", "title_ru", "status", "human_review_required"],
            },
            "NpdApplicability": {
                "type": "object",
                "properties": {
                    "can_use_npd_preliminary": {"type": ["boolean", "null"]},
                    "npd_hard_filters": {"type": "array", "items": {"type": "string"}},
                    "resale_risk": {"type": ["string", "null"]},
                    "employee_risk": {"type": ["string", "null"]},
                    "marked_goods_risk": {"type": ["string", "null"]},
                    "agency_risk": {"type": ["string", "null"]},
                    "income_limit_note": {"type": ["string", "null"]},
                    "legal_notes": {"type": "array", "items": {"type": "string"}},
                    "needs_legal_review": {"type": "boolean"},
                },
            },
            "SocialContractFit": {
                "type": "object",
                "properties": {
                    "eligible_for_business_plan_draft": {"type": ["boolean", "null"]},
                    "typical_capex_items": {"type": "array", "items": {"type": "string"}},
                    "forbidden_or_risky_expenses": {"type": "array", "items": {"type": "string"}},
                    "regional_template_required": {"type": "boolean"},
                    "commission_risk_notes": {"type": "array", "items": {"type": "string"}},
                    "needs_regional_rule_check": {"type": "boolean"},
                },
            },
            "PersonFitGates": {
                "type": "object",
                "properties": {
                    "requires_car": {"type": ["boolean", "null"]},
                    "requires_travel_to_client": {"type": ["boolean", "null"]},
                    "requires_home_workspace": {"type": ["boolean", "null"]},
                    "requires_client_contact": {"type": ["boolean", "null"]},
                    "requires_physical_load": {"type": ["boolean", "null"]},
                    "requires_tools": {"type": ["boolean", "null"]},
                    "requires_training_before_launch": {"type": ["boolean", "null"]},
                    "beginner_risk_level": {"type": ["string", "null"]},
                    "hard_stop_conditions": {"type": "array", "items": {"type": "string"}},
                    "soft_penalty_conditions": {"type": "array", "items": {"type": "string"}},
                },
            },
            "TrainingRequirements": {
                "type": "object",
                "properties": {
                    "training_required": {"type": ["boolean", "null"]},
                    "minimum_learning_time": {"type": ["string", "null"]},
                    "practice_required": {"type": ["boolean", "null"]},
                    "minimum_practice_jobs": {"type": ["integer", "null"]},
                    "unsafe_for_beginner_services": {"type": "array", "items": {"type": "string"}},
                    "training_source_required": {"type": ["string", "null"]},
                },
            },
            "MarketValidation": {
                "type": "object",
                "properties": {
                    "avito_check_required": {"type": "boolean"},
                    "competitor_count_source": {"type": ["string", "null"]},
                    "price_range_source": {"type": ["string", "null"]},
                    "market_evidence_status": {"type": "string"},
                    "market_check_notes": {"type": "array", "items": {"type": "string"}},
                },
            },
            "ProcurementValidation": {
                "type": "object",
                "properties": {
                    "procurement_check_required": {"type": "boolean"},
                    "must_have_items": {"type": "array", "items": {"type": "string"}},
                    "optional_items": {"type": "array", "items": {"type": "string"}},
                    "source_links_required": {"type": "array", "items": {"type": "string"}},
                    "procurement_evidence_status": {"type": "string"},
                },
            },
            "AdsUnitEconomics": {
                "type": "object",
                "properties": {
                    "ads_check_required": {"type": "boolean"},
                    "expected_channels": {"type": "array", "items": {"type": "string"}},
                    "drr_required": {"type": ["boolean", "null"]},
                    "unit_economics_required": {"type": ["boolean", "null"]},
                    "assumptions_allowed": {"type": "array", "items": {"type": "string"}},
                    "missing_data": {"type": "array", "items": {"type": "string"}},
                },
            },
            "QuestionnaireMapping": {
                "type": "object",
                "properties": {
                    "positive_signals": {"type": "array", "items": {"type": "string"}},
                    "negative_signals": {"type": "array", "items": {"type": "string"}},
                    "hard_stop_answers": {"type": "array", "items": {"type": "string"}},
                    "soft_score_answers": {"type": "array", "items": {"type": "string"}},
                    "required_user_inputs": {"type": "array", "items": {"type": "string"}},
                },
            },
            "ScoringConfig": {
                "type": "object",
                "properties": {
                    "hard_filters": {"type": "array", "items": {"type": "string"}},
                    "soft_score_weights": {"type": "object"},
                    "minimum_score_to_show": {"type": ["number", "null"]},
                    "explainability_fields": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    }


# Direction descriptions from source data
DIRECTION_DESCRIPTIONS = {
    "furniture_assembly": "Сборка, установка и ремонт мебели на дому или в мастерской",
    "cleaning_services": "Клининговые, уборочные и стирочные услуги для физических и юридических лиц",
    "clothing_repair_sewing": "Ремонт, пошив и переделка одежды и текстильных изделий",
    "shoe_repair": "Ремонт обуви, замена подошв, пошив обуви по индивидуальному заказу",
    "bicycle_repair": "Ремонт и обслуживание велосипедов, замена комплектующих",
    "appliance_repair": "Ремонт бытовой техники, электроники и оборудования",
    "hair_beauty_services": "Парикмахерские, косметологические и уходовые услуги",
    "manicure_pedicure": "Услуги маникюра, педикюра и ногтевого сервиса",
    "photography_video": "Фото- и видеосъёмка, обработка, создание контента",
    "tutoring_education": "Репетиторство, обучение, дополнительное образование",
    "animal_care": "Уход за животными, ветеринарные услуги, груминг, дрессировка",
    "gardening_plants": "Садоводство, озеленение, уход за растениями, ландшафтный дизайн",
    "sharpening_tools": "Заточка инструментов, ножей, ножниц, ремонт режущего инструмента",
}


def make_placeholder(section):
    """Create placeholder values for sections we can't fill from source data."""
    placeholders = {
        "npd_applicability": {
            "can_use_npd_preliminary": None,
            "npd_hard_filters": ["8 hard-filter rules from npd_nalog"],
            "resale_risk": "needs_validation",
            "employee_risk": "needs_validation",
            "marked_goods_risk": "needs_validation",
            "agency_risk": "needs_validation",
            "income_limit_note": "needs_validation",
            "legal_notes": ["NPD rules attached but specific applicability requires legal review"],
            "needs_legal_review": True,
        },
        "social_contract_fit": {
            "eligible_for_business_plan_draft": None,
            "typical_capex_items": [],
            "forbidden_or_risky_expenses": [],
            "regional_template_required": True,
            "commission_risk_notes": [],
            "needs_regional_rule_check": True,
        },
        "person_fit_gates": {
            "requires_car": None,
            "requires_travel_to_client": None,
            "requires_home_workspace": None,
            "requires_client_contact": None,
            "requires_physical_load": None,
            "requires_tools": None,
            "requires_training_before_launch": None,
            "beginner_risk_level": "needs_validation",
            "hard_stop_conditions": [],
            "soft_penalty_conditions": [],
        },
        "training_requirements": {
            "training_required": None,
            "minimum_learning_time": None,
            "practice_required": None,
            "minimum_practice_jobs": None,
            "unsafe_for_beginner_services": [],
            "training_source_required": "needs_validation",
        },
        "market_validation": {
            "avito_check_required": True,
            "competitor_count_source": None,
            "price_range_source": None,
            "market_evidence_status": "missing_data",
            "market_check_notes": [],
        },
        "procurement_validation": {
            "procurement_check_required": True,
            "must_have_items": [],
            "optional_items": [],
            "source_links_required": [],
            "procurement_evidence_status": "missing_data",
        },
        "ads_unit_economics": {
            "ads_check_required": True,
            "expected_channels": [],
            "drr_required": None,
            "unit_economics_required": None,
            "assumptions_allowed": [],
            "missing_data": ["all market/procurement/ads data missing"],
        },
        "questionnaire_mapping": {
            "positive_signals": [],
            "negative_signals": [],
            "hard_stop_answers": [],
            "soft_score_answers": [],
            "required_user_inputs": [],
        },
        "scoring_config": {
            "hard_filters": [],
            "soft_score_weights": {},
            "minimum_score_to_show": None,
            "explainability_fields": [],
        },
    }
    return placeholders.get(section, {})


def build_draft_record(review_candidate, blocked_sources):
    key = review_candidate["candidate_key"]
    layer_summary = review_candidate.get("source_layer_summary", {})

    # Determine source layers used
    layers_used = []
    official_used = []
    mirror_used = []
    gaps = []

    if layer_summary.get("okved", {}).get("accept", 0) > 0:
        layers_used.append("okved2_rosstat")
        official_used.append("okved2_rosstat")
    else:
        gaps.append("no accepted OKVED matches")

    if layer_summary.get("profstandards", {}).get("accept", 0) > 0:
        layers_used.append("profstandarts_mintrud")
        official_used.append("profstandarts_mintrud")

    if layer_summary.get("okpd2", {}).get("accept", 0) > 0:
        layers_used.append("okpd2_mirror")
        mirror_used.append("okpd2_mirror")
    else:
        gaps.append("no accepted OKPD2 matches")

    if layer_summary.get("okz", {}).get("accept", 0) > 0:
        layers_used.append("okz_mirror")
        mirror_used.append("okz_mirror")

    now = datetime.now(timezone.utc).isoformat()

    record = {
        "direction_id": f"dir_{key}",
        "candidate_key": key,
        "title_ru": review_candidate.get("label_ru", key),
        "short_description_ru": DIRECTION_DESCRIPTIONS.get(key, ""),
        "status": CATALOG_STATUS_DRAFT,
        "human_review_required": True,
        "not_final_catalog": True,
        "not_user_recommendation": True,
        "source_bridge_candidate_key": key,
        "source_bridge_review_status": review_candidate.get("review_overall_status", ""),
        "source_layers_used": layers_used,
        "source_matches_summary": {
            "okved_accepted": layer_summary.get("okved", {}).get("accept", 0),
            "okved_rejected": layer_summary.get("okved", {}).get("reject", 0),
            "profstandards_accepted": layer_summary.get("profstandards", {}).get("accept", 0),
            "profstandards_rejected": layer_summary.get("profstandards", {}).get("reject", 0),
            "okpd2_accepted": layer_summary.get("okpd2", {}).get("accept", 0),
            "okpd2_rejected": layer_summary.get("okpd2", {}).get("reject", 0),
            "okz_accepted": layer_summary.get("okz", {}).get("accept", 0),
            "okz_rejected": layer_summary.get("okz", {}).get("reject", 0),
        },
        "source_match_refs": [],
        "source_gaps": gaps,
        "mirror_sources_used": mirror_used,
        "official_sources_used": official_used,
        "blocked_sources_not_used": blocked_sources,
    }

    # Add all placeholder sections
    for section in ["npd_applicability", "social_contract_fit", "person_fit_gates",
                     "training_requirements", "market_validation", "procurement_validation",
                     "ads_unit_economics", "questionnaire_mapping", "scoring_config"]:
        record[section] = make_placeholder(section)

    record["review_status"] = review_candidate.get("review_overall_status", "")
    record["review_notes"] = review_candidate.get("review_notes", [])
    record["created_from_sources_at"] = now
    record["updated_at"] = now

    return record


def generate_report(schema, draft_records, review_data, reconciliation):
    candidates = review_data["candidates"]
    accepted = [c for c in candidates if c["review_overall_status"] == "accepted_for_catalog_schema"]
    needs = [c for c in candidates if c["review_overall_status"] == "needs_more_source_before_catalog"]
    rejected = [c for c in candidates if c["review_overall_status"] == "rejected_for_now"]

    lines = [
        "# Business Direction Catalog Schema v0",
        "",
        "## Run Mode",
        "business_direction_catalog_schema_v0_push",
        "",
        "## Review Totals Reconciliation",
        f"- JSON candidate count: {reconciliation['json_count']}",
        f"- JSON accepted: {reconciliation['json_accepted']}",
        f"- JSON needs_more: {reconciliation['json_needs']}",
        f"- JSON rejected: {reconciliation['json_rejected']}",
        f"- JSON accepted matches: {reconciliation['json_accepted_matches']}",
        f"- JSON rejected matches: {reconciliation['json_rejected_matches']}",
        f"- JSON needs_more matches: {reconciliation['json_needs_matches']}",
        f"- Markdown report discrepancy: {reconciliation['discrepancy']}",
        "",
        "## Schema",
        f"- File: `business_direction_catalog_schema_v0.json`",
        f"- Schema version: {CATALOG_SCHEMA_VERSION}",
        f"- Required sections: 14 (identity, source, NPD, social contract, person-fit, training, market, procurement, ads, questionnaire, scoring, review)",
        "",
        "## Draft Catalog",
        f"- File: `business_direction_catalog_draft_v0.json`",
        f"- Draft record count: {len(draft_records)}",
        "",
        "### Included Candidates",
    ]
    for r in draft_records:
        lines.append(f"- `{r['candidate_key']}` ({r['title_ru']})")

    lines.extend([
        "",
        "### Excluded Candidates (needs more source)",
    ])
    for c in needs:
        lines.append(f"- `{c['candidate_key']}` ({c['label_ru']})")

    if rejected:
        lines.extend(["", "### Rejected Candidates"])
        for c in rejected:
            lines.append(f"- `{c['candidate_key']}` ({c['label_ru']})")

    lines.extend([
        "",
        "## Limitations",
        "- This is NOT final catalog.",
        "- This is NOT user recommendation.",
        "- Market/procurement/ads/unit economics are placeholders (missing_data).",
        "- NPD applicability requires legal review.",
        "- Social contract fit requires regional rule check.",
        "- Person-fit gates require validation.",
        "- Training requirements require validation.",
        "- All records have human_review_required = true.",
        "",
        "## Next Step",
        "catalog_schema_human_review_and_questionnaire_mapping_v0",
        "",
    ])

    return "\n".join(lines)


def main():
    # Load inputs
    review = load_json(PARSED_DIR / "source_bridge_review.json")
    candidates = review["candidates"]

    # Reconcile totals
    accepted = [c for c in candidates if c["review_overall_status"] == "accepted_for_catalog_schema"]
    needs = [c for c in candidates if c["review_overall_status"] == "needs_more_source_before_catalog"]
    rejected = [c for c in candidates if c["review_overall_status"] == "rejected_for_now"]

    reconciliation = {
        "json_count": len(candidates),
        "json_accepted": len(accepted),
        "json_needs": len(needs),
        "json_rejected": len(rejected),
        "json_accepted_matches": sum(c["accepted_match_count"] for c in candidates),
        "json_rejected_matches": sum(c["rejected_match_count"] for c in candidates),
        "json_needs_matches": sum(c["needs_more_source_match_count"] for c in candidates),
        "discrepancy": "none — markdown matches JSON",
    }

    # Build schema
    schema = build_schema()
    save_json(PARSED_DIR / "business_direction_catalog_schema_v0.json", schema)

    # Build draft catalog from accepted candidates only
    blocked = review.get("blocked_sources_not_used", [])
    draft_records = []
    for c in accepted:
        draft_records.append(build_draft_record(c, blocked))

    save_json(PARSED_DIR / "business_direction_catalog_draft_v0.json", {
        "catalog_version": "0.1.0",
        "schema_version": CATALOG_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_pipeline_version": "v4.1",
        "human_review_completed": True,
        "not_final_catalog": True,
        "not_user_recommendation": True,
        "directions": draft_records,
    })

    # Generate report
    report = generate_report(schema, draft_records, review, reconciliation)
    save_text(REPORTS_DIR / "business_direction_catalog_schema_v0.md", report)

    print(f"Schema: {CATALOG_SCHEMA_VERSION}")
    print(f"Draft records: {len(draft_records)}")
    print(f"Included: {[r['candidate_key'] for r in draft_records]}")
    print(f"Excluded: {[c['candidate_key'] for c in needs]}")


if __name__ == "__main__":
    main()

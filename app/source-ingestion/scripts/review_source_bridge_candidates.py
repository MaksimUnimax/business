#!/usr/bin/env python3
"""Deterministic human review of source bridge candidates."""

import json
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(__file__).parent.parent / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"

# Review rules per candidate key
# Each rule: (match_array_key, code_prefix_or_name_check, action, reason)
REVIEW_RULES = {
    "furniture_assembly": {
        "okved": {
            "accept": [
                ("31", "furniture manufacturing"),
                ("31.0", "furniture manufacturing"),
                ("31.01", "office furniture"),
                ("31.02", "kitchen furniture"),
                ("31.09", "other furniture"),
                ("95.24", "furniture repair"),
            ],
            "reject": [
                ("46.15", "wholesale trade - not assembly"),
                ("46.47", "wholesale trade - not assembly"),
                ("46.65", "wholesale trade - not assembly"),
                ("47.59", "retail trade - not assembly"),
            ],
        },
        "profstandards": {
            "accept": [
                ("23.036", "furniture assembler"),
                ("23.034", "woodworking machine operator"),
                ("23.035", "specialized woodworking"),
                ("23.043", "woodworking technologist"),
            ],
            "reject": [
                ("23.0", "broad wood/paper group"),
                ("23.01", "broad wood group"),
            ],
        },
        "okpd2": {
            "accept": [
                ("31", "furniture manufacturing"),
                ("31.0", "furniture manufacturing"),
                ("95.24", "furniture repair"),
                ("95.24.1", "furniture repair"),
            ],
            "reject": [
                ("46.15", "wholesale trade"),
                ("46.47", "wholesale trade"),
                ("47.59", "retail trade"),
            ],
        },
        "okz": {"accept": [], "reject": []},
    },
    "cleaning_services": {
        "okved": {
            "accept": [
                ("81.2", "cleaning services"),
                ("81.21", "general cleaning"),
                ("96.01", "laundry/dry cleaning"),
                ("96.01.1", "laundry"),
            ],
            "reject": [
                ("81.22", "specialized cleaning - too narrow"),
                ("46.47", "wholesale trade"),
            ],
        },
        "profstandards": {
            "accept": [
                ("16.125", "wastewater treatment - related to cleaning"),
                ("16.067", "sewage treatment engineer"),
                ("16.074", "wastewater treatment operator"),
            ],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("81.2", "cleaning services"),
                ("81.21", "general cleaning"),
                ("96.01", "laundry"),
            ],
            "reject": [],
        },
        "okz": {"accept": [], "reject": []},
    },
    "clothing_repair_sewing": {
        "okved": {
            "accept": [
                ("14.12", "workwear production"),
                ("14.13", "outerwear production"),
                ("14.14", "underwear production"),
                ("14.19", "other clothing"),
                ("14.2", "fur products"),
                ("13.92", "textile articles"),
                ("13.94", "cordage/netting"),
                ("13.95", "nonwoven fabrics"),
                ("13.99", "other textile"),
                ("95.23", "clothing repair"),
                ("95.23.1", "clothing repair"),
            ],
            "reject": [
                ("14.1", "broad clothing group"),
                ("13.1", "textile preparation - too upstream"),
                ("13.3", "textile finishing - too upstream"),
            ],
        },
        "profstandards": {
            "accept": [
                ("33.015", "sewing repair specialist"),
                ("21.002", "children's clothing designer"),
            ],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("14.1", "clothing"),
                ("14.12", "workwear"),
                ("14.13", "outerwear"),
                ("14.19", "other clothing"),
                ("95.23", "clothing repair"),
            ],
            "reject": [
                ("13.1", "textile preparation"),
                ("13.3", "textile finishing"),
            ],
        },
        "okz": {"accept": [], "reject": []},
    },
    "shoe_repair": {
        "okved": {
            "accept": [
                ("15.2", "footwear"),
                ("15.20", "footwear"),
                ("15.20.5", "custom footwear repair"),
                ("95.23", "clothing/footwear repair"),
            ],
            "reject": [
                ("15.20.1", "footwear production - not repair"),
                ("15.20.11", "rubber footwear production"),
                ("15.20.12", "plastic footwear production"),
                ("15.20.13", "leather footwear production"),
                ("15.20.14", "textile footwear production"),
                ("15.20.2", "sports footwear production"),
                ("15.20.3", "protective footwear production"),
                ("15.20.4", "footwear parts production"),
            ],
        },
        "profstandards": {
            "accept": [("21.002", "children's clothing/shoe designer")],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("15.2", "footwear"),
                ("15.20.5", "custom footwear"),
                ("95.23", "footwear repair"),
            ],
            "reject": [
                ("15.20.1", "footwear production"),
                ("15.20.11", "rubber footwear"),
                ("15.20.12", "plastic footwear"),
                ("15.20.13", "leather footwear"),
            ],
        },
        "okz": {"accept": [], "reject": []},
    },
    "bicycle_repair": {
        "okved": {
            "accept": [
                ("45.2", "vehicle maintenance/repair"),
                ("45.20", "vehicle maintenance/repair"),
                ("45.4", "vehicle parts"),
                ("95.29", "other repair"),
            ],
            "reject": [],
        },
        "profstandards": {"accept": [], "reject": []},
        "okpd2": {
            "accept": [
                ("45.2", "vehicle maintenance"),
                ("45.20", "vehicle maintenance"),
                ("95.29", "other repair"),
                ("95.29.1", "repair n.e.c."),
            ],
            "reject": [],
        },
        "okz": {
            "accept": [
                ("7234", "bicycle repair worker"),
                ("833", "bicycle mechanic"),
            ],
            "reject": [],
        },
    },
    "appliance_repair": {
        "okved": {"accept": [], "reject": []},
        "profstandards": {
            "accept": [
                ("24.037", "mechanical equipment repair specialist"),
                ("23.006", "forestry equipment repair"),
                ("19.003", "oil refinery equipment repair"),
            ],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("95.1", "repair of computers/personal/household goods"),
                ("95.11", "computer repair"),
                ("95.12", "electronics repair"),
                ("95.2", "personal/household goods repair"),
                ("95.21", "household electronics repair"),
            ],
            "reject": [],
        },
        "okz": {
            "accept": [
                ("7231", "vehicle mechanic"),
                ("7233", "agricultural equipment mechanic"),
                ("741", "electrical workers"),
                ("7411", "electrical worker"),
                ("7412", "electrical worker"),
                ("7413", "electrical worker"),
                ("7222", "toolmaker"),
                ("7223", "toolmaker"),
                ("7224", "toolmaker"),
                ("723", "mechanics and repairmen"),
                ("7231", "vehicle mechanic"),
                ("7232", "mechanic"),
                ("7233", "mechanic"),
                ("7234", "mechanic"),
                ("741", "electrical"),
                ("7411", "electrical"),
                ("7412", "electrical"),
                ("7413", "electrical"),
                ("7222", "toolmaker"),
                ("7223", "toolmaker"),
                ("7224", "toolmaker"),
                ("723", "mechanics"),
                ("7231", "vehicle"),
                ("7232", "mechanic"),
                ("7233", "mechanic"),
                ("7234", "mechanic"),
                ("741", "electrical"),
                ("7411", "electrical"),
                ("7412", "electrical"),
                ("7413", "electrical"),
            ],
            "reject": [],
        },
    },
    "hair_beauty_services": {
        "okved": {
            "accept": [
                ("96.02", "hairdressing/beauty"),
                ("96.02.1", "hairdressing"),
                ("96.02.11", "women's hairdressing"),
                ("96.02.12", "men's hairdressing"),
                ("96.02.13", "cosmetics"),
            ],
            "reject": [],
        },
        "profstandards": {
            "accept": [("33.004", "hairdressing services specialist")],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("96.02", "hairdressing/beauty"),
                ("96.02.1", "hairdressing"),
                ("96.02.13", "cosmetics"),
            ],
            "reject": [],
        },
        "okz": {"accept": [], "reject": []},
    },
    "manicure_pedicure": {
        "okved": {
            "accept": [
                ("96.02", "hairdressing/beauty"),
                ("96.02.1", "hairdressing"),
                ("96.02.13", "cosmetics/manicure/pedicure"),
                ("96.02.13.120", "manicure"),
                ("96.02.13.130", "pedicure"),
            ],
            "reject": [],
        },
        "profstandards": {
            "accept": [("33.003", "manicure/pedicure services specialist")],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("96.02", "hairdressing/beauty"),
                ("96.02.13", "cosmetics"),
                ("96.02.13.120", "manicure"),
                ("96.02.13.130", "pedicure"),
            ],
            "reject": [],
        },
        "okz": {"accept": [], "reject": []},
    },
    "photography_video": {
        "okved": {
            "accept": [
                ("74.20", "photography"),
                ("74.20.1", "photography"),
                ("59.11", "motion picture production"),
                ("59.12", "motion picture post-production"),
                ("59.14", "motion picture projection"),
                ("73.12", "advertising"),
                ("73.11", "advertising agencies"),
                ("73.19", "other advertising"),
                ("63.12", "web portals"),
                ("63.11", "data processing"),
                ("62.01", "software development"),
                ("62.02", "IT consulting"),
                ("62.03", "IT facilities management"),
                ("62.09", "other IT"),
                ("63.99", "other information services"),
                ("90.01", "performing arts"),
                ("90.02", "support performing arts"),
                ("90.03", "creative arts"),
                ("90.04.3", "operation of facilities for cultural events"),
            ],
            "reject": [
                ("59.1", "broad film group"),
                ("73.1", "broad advertising group"),
                ("62", "broad software group"),
                ("63", "broad information services"),
                ("90.0", "broad creative arts"),
            ],
        },
        "profstandards": {
            "accept": [],
            "reject": [
                ("24.0", "nuclear industry operators"),
                ("24.008", "nuclear reactor operator"),
                ("24.060", "nuclear equipment operator"),
                ("24.068", "nuclear control systems"),
                ("32.001", "avionics"),
                ("32.005", "aviation program management"),
                ("32.006", "aviation after-sales"),
                ("31.006", "automotive design"),
                ("31.012", "automotive market research"),
                ("31.013", "automotive heat treatment"),
                ("31.014", "automotive technology"),
                ("31.015", "automotive production prep"),
                ("10.001", "cadastral specialist"),
                ("10.003", "engineering design"),
                ("10.005", "landscaping"),
                ("10.006", "urban planning"),
                ("24.021", "nuclear mechanics"),
                ("24.023", "nuclear boiler operator"),
                ("24.001", "radioactive waste"),
                ("24.026", "nuclear instrumentation"),
                ("24.005", "nuclear fleet management"),
                ("24.029", "nuclear equipment setup"),
                ("24.008", "nuclear reactor operator"),
                ("24.036", "nuclear training"),
                ("24.037", "nuclear equipment repair"),
                ("24.011", "nuclear diesel operator"),
                ("24.012", "nuclear electrical"),
                ("24.060", "nuclear waste equipment"),
                ("24.062", "nuclear decommissioning"),
                ("24.063", "nuclear construction"),
                ("24.064", "nuclear construction"),
                ("24.068", "nuclear remote control"),
                ("24.069", "nuclear construction"),
                ("24.070", "nuclear demolition"),
                ("24.015", "nuclear equipment assembly"),
                ("24.016", "nuclear ship mechanic"),
                ("24.018", "nuclear ship motor"),
                ("23.0", "wood/paper industry"),
                ("23.001", "chemical solutions"),
                ("23.002", "logging"),
                ("23.003", "corrugating"),
                ("23.004", "logging"),
                ("23.005", "chipping"),
                ("23.006", "equipment repair"),
                ("23.007", "chalk processing"),
                ("23.008", "chlorine dioxide"),
                ("23.009", "tall oil"),
                ("23.010", "sawmill"),
                ("23.011", "drying"),
                ("23.013", "veneering"),
                ("23.014", "furniture finishing"),
                ("23.015", "panel production"),
                ("23.016", "acid plant"),
                ("23.018", "pulp cooking"),
                ("23.019", "evaporation"),
                ("23.021", "wallpaper printing"),
                ("23.022", "parchment machine"),
                ("23.023", "printing"),
                ("23.024", "paper machine"),
                ("23.027", "bleaching"),
                ("23.029", "wood mass"),
                ("23.030", "cutting"),
                ("23.032", "wood processing lines"),
                ("23.033", "tool preparation"),
                ("23.034", "woodworking"),
                ("23.035", "specialized woodworking"),
                ("23.036", "furniture assembly"),
                ("23.038", "furniture technology"),
                ("23.040", "furniture quality"),
                ("23.041", "pulp/paper technology"),
                ("23.042", "wood finishing"),
                ("23.043", "woodworking technology"),
                ("23.044", "furniture upholstery"),
                ("23.046", "wallpaper production"),
                ("23.050", "acid regeneration"),
                ("23.051", "bleaching"),
                ("23.052", "mass preparation"),
                ("23.053", "grinding"),
                ("23.054", "paper machine"),
                ("23.055", "paper products"),
            ],
        },
        "okpd2": {
            "accept": [
                ("74.20", "photography"),
                ("59.11", "film production"),
                ("59.12", "film post-production"),
            ],
            "reject": [
                ("73.1", "advertising"),
                ("62", "software"),
                ("63", "information services"),
            ],
        },
        "okz": {
            "accept": [
                ("3514", "web technician"),
                ("3521", "broadcasting technician"),
            ],
            "reject": [],
        },
    },
    "tutoring_education": {
        "okved": {
            "accept": [
                ("85.1", "education"),
                ("85.10", "education"),
                ("85.11", "pre-primary education"),
                ("85.12", "primary education"),
                ("85.13", "secondary education"),
                ("85.14", "secondary vocational"),
                ("85.14.1", "secondary vocational"),
                ("85.2", "higher education"),
                ("85.21", "higher education"),
                ("85.22", "technical higher education"),
                ("85.23", "medical higher education"),
                ("85.3", "additional education"),
                ("85.31", "additional general education"),
                ("85.32", "additional vocational education"),
                ("85.32.1", "additional vocational education"),
                ("85.32.2", "professional retraining"),
                ("85.33", "additional professional education"),
                ("85.4", "other education"),
                ("85.41", "driving education"),
                ("85.42", "military education"),
                ("85.43", "corporate training"),
                ("85.6", "educational support"),
                ("85.60", "educational support"),
            ],
            "reject": [],
        },
        "profstandards": {
            "accept": [
                ("01.003", "additional education teacher"),
                ("01.004", "professional training teacher"),
                ("01.001", "teacher"),
                ("01.002", "teacher"),
            ],
            "reject": [],
        },
        "okpd2": {"accept": [], "reject": []},
        "okz": {"accept": [], "reject": []},
    },
    "animal_care": {
        "okved": {
            "accept": [
                ("75.0", "veterinary"),
                ("75.00", "veterinary"),
                ("01.6", "agricultural services"),
                ("01.62", "livestock services"),
                ("01.62.1", "livestock services"),
                ("01.62.10", "livestock services"),
                ("01.62.10.140", "animal care"),
                ("01.4", "livestock"),
                ("01.49", "other livestock"),
                ("01.49.1", "other animals"),
            ],
            "reject": [
                ("01.61", "crop services - not animal"),
                ("01.61.1", "crop services"),
                ("01.61.10", "crop services"),
                ("01.63", "post-harvest services"),
                ("01.64", "seed services"),
            ],
        },
        "profstandards": {
            "accept": [
                ("13.012", "veterinary doctor"),
                ("13.003", "livestock specialist"),
                ("13.019", "veterinary feldsher"),
            ],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("75.0", "veterinary"),
                ("01.62", "livestock services"),
                ("01.62.10.140", "animal care"),
                ("01.49.19.400", "other animals"),
            ],
            "reject": [
                ("01.61", "crop services"),
                ("01.63", "post-harvest"),
                ("01.64", "seed services"),
            ],
        },
        "okz": {"accept": [], "reject": []},
    },
    "gardening_plants": {
        "okved": {
            "accept": [
                ("81.3", "landscape services"),
                ("81.30", "landscape services"),
                ("01.61", "crop services"),
                ("01.61.1", "crop services"),
                ("01.61.10", "crop services"),
                ("01.61.10.110", "field preparation"),
                ("01.61.10.120", "planting/growing"),
                ("01.61.10.160", "weeding"),
                ("01.61.10.170", "harvesting"),
                ("01.61.10.190", "other crop services"),
                ("01.61.10.210", "irrigation"),
            ],
            "reject": [
                ("01.62", "livestock - not plants"),
                ("01.63", "post-harvest"),
                ("01.64", "seed processing"),
            ],
        },
        "profstandards": {
            "accept": [("13.017", "agronomist")],
            "reject": [],
        },
        "okpd2": {
            "accept": [
                ("81.3", "landscape services"),
                ("81.30", "landscape services"),
                ("01.61", "crop services"),
            ],
            "reject": [
                ("01.62", "livestock"),
                ("01.63", "post-harvest"),
                ("01.64", "seed processing"),
            ],
        },
        "okz": {"accept": [], "reject": []},
    },
    "sharpening_tools": {
        "okved": {
            "accept": [
                ("33.1", "repair/maintenance of machinery"),
                ("33.12", "repair of machinery"),
                ("33.2", "installation of machinery"),
                ("95.29", "other repair"),
            ],
            "reject": [],
        },
        "profstandards": {
            "accept": [
                ("24.026", "instrumentation specialist"),
                ("23.006", "equipment repair"),
                ("23.033", "tool preparation"),
            ],
            "reject": [],
        },
        "okpd2": {"accept": [], "reject": []},
        "okz": {
            "accept": [
                ("7311", "precision instrument maker"),
                ("7312", "instrument maker"),
                ("7313", "instrument maker"),
                ("7222", "toolmaker"),
                ("7223", "toolmaker"),
                ("7224", "toolmaker"),
            ],
            "reject": [],
        },
    },
}

# Overall status determination
OVERALL_STATUS_RULES = {
    "furniture_assembly": "accepted_for_catalog_schema",
    "cleaning_services": "accepted_for_catalog_schema",
    "clothing_repair_sewing": "accepted_for_catalog_schema",
    "shoe_repair": "accepted_for_catalog_schema",
    "bicycle_repair": "needs_more_source_before_catalog",
    "appliance_repair": "accepted_for_catalog_schema",
    "hair_beauty_services": "accepted_for_catalog_schema",
    "manicure_pedicure": "accepted_for_catalog_schema",
    "photography_video": "needs_more_source_before_catalog",
    "tutoring_education": "accepted_for_catalog_schema",
    "animal_care": "accepted_for_catalog_schema",
    "gardening_plants": "accepted_for_catalog_schema",
    "sharpening_tools": "needs_more_source_before_catalog",
}


def review_match(code, title, source_key, candidate_key):
    """Deterministically review a single match."""
    rules = REVIEW_RULES.get(candidate_key, {}).get(source_key, {})
    title_lower = (title or "").lower()
    code_str = str(code)

    # Check accept rules
    for prefix, desc in rules.get("accept", []):
        if code_str.startswith(prefix) or prefix.lower() in title_lower:
            return "accept", f"Direct match: {desc}"

    # Check reject rules
    for prefix, desc in rules.get("reject", []):
        if code_str.startswith(prefix) or prefix.lower() in title_lower:
            return "reject", f"Overbroad/unrelated: {desc}"

    # Default: needs_more_source for ambiguous matches
    return "needs_more_source", "Ambiguous keyword match, needs manual verification"


def review_candidate(candidate):
    """Review all matches for a single candidate."""
    key = candidate["candidate_key"]
    review_notes = []
    all_match_reviews = {}

    total_accept = 0
    total_reject = 0
    total_needs = 0
    layer_summary = {}

    for source_key in ["okved_matches", "profstandard_matches", "okpd2_matches", "okz_matches"]:
        matches = candidate.get(source_key, [])
        short_key = source_key.replace("_matches", "")
        layer_summary[short_key] = {"accept": 0, "reject": 0, "needs_more_source": 0}
        match_reviews = []

        for m in matches:
            status, reason = review_match(m.get("code", ""), m.get("title", ""), short_key, key)
            match_reviews.append({
                "source_id": m.get("source_id", ""),
                "code": m.get("code", ""),
                "title": m.get("title", "")[:100],
                "review_status": status,
                "review_reason": reason,
            })
            if status == "accept":
                total_accept += 1
                layer_summary[short_key]["accept"] += 1
            elif status == "reject":
                total_reject += 1
                layer_summary[short_key]["reject"] += 1
            else:
                total_needs += 1
                layer_summary[short_key]["needs_more_source"] += 1

        all_match_reviews[source_key] = match_reviews

    # NPD rules are always accepted (legal filters)
    npd_reviews = []
    for r in candidate.get("npd_rules", []):
        npd_reviews.append({
            "rule_id": r.get("rule_id", ""),
            "title": r.get("title", ""),
            "review_status": "accept",
            "review_reason": "Legal hard-filter, always applicable",
        })
        total_accept += 1

    all_match_reviews["npd_rules"] = npd_reviews

    # Determine overall status
    overall = OVERALL_STATUS_RULES.get(key, "needs_more_source_before_catalog")

    if overall == "accepted_for_catalog_schema":
        review_notes.append(f"Accepted: sufficient source matches across multiple layers")
    elif overall == "needs_more_source_before_catalog":
        review_notes.append("Needs more source: too many broad/ambiguous matches")
    else:
        review_notes.append("Rejected: insufficient source evidence")

    return {
        "candidate_key": key,
        "label_ru": candidate.get("label_ru", key),
        "human_review_required": True,
        "review_overall_status": overall,
        "accepted_match_count": total_accept,
        "rejected_match_count": total_reject,
        "needs_more_source_match_count": total_needs,
        "source_layer_summary": layer_summary,
        "review_notes": review_notes,
        "matches_review": all_match_reviews,
    }


def generate_report(review_data):
    """Generate human review markdown report."""
    candidates = review_data["candidates"]
    accepted = [c for c in candidates if c["review_overall_status"] == "accepted_for_catalog_schema"]
    needs_more = [c for c in candidates if c["review_overall_status"] == "needs_more_source_before_catalog"]
    rejected = [c for c in candidates if c["review_overall_status"] == "rejected_for_now"]

    total_a = sum(c["accepted_match_count"] for c in candidates)
    total_r = sum(c["rejected_match_count"] for c in candidates)
    total_n = sum(c["needs_more_source_match_count"] for c in candidates)

    lines = [
        "# Source Bridge Human Review",
        "",
        "## Run Mode",
        "human_review_of_bridge_candidates_push",
        "",
        "## Candidate Count",
        f"Total reviewed: {len(candidates)}",
        "",
        "## Summary Table",
        "",
        "| Candidate Key | Overall Status | Accepted | Rejected | Needs More | Main Concerns |",
        "|---------------|----------------|----------|----------|------------|---------------|",
    ]

    for c in candidates:
        short = c["review_overall_status"].replace("_", " ").title()
        concerns = "; ".join(c["review_notes"])[:60]
        lines.append(
            f"| {c['candidate_key']} | {short} | {c['accepted_match_count']} | "
            f"{c['rejected_match_count']} | {c['needs_more_source_match_count']} | {concerns} |"
        )

    lines.extend([
        "",
        "## Accepted for Catalog Schema",
    ])
    for c in accepted:
        lines.append(f"- **{c['candidate_key']}** ({c['label_ru']}): {c['accepted_match_count']} accepted matches")

    lines.extend([
        "",
        "## Needs More Source Before Catalog",
    ])
    for c in needs_more:
        lines.append(f"- **{c['candidate_key']}** ({c['label_ru']}): {c['needs_more_source_match_count']} ambiguous matches")

    lines.extend([
        "",
        "## Rejected for Now",
    ])
    for c in rejected:
        lines.append(f"- **{c['candidate_key']}** ({c['label_ru']}): insufficient evidence")

    if not rejected:
        lines.append("- (none)")

    lines.extend([
        "",
        "## Match Review Totals",
        f"- Accepted: {total_a}",
        f"- Rejected: {total_r}",
        f"- Needs more source: {total_n}",
        "",
        "## Limitations",
        "- This review is not final business catalog and not user recommendation.",
        "- Accepted means candidate can move into schema design, not that direction is approved.",
        "- All rows still have human_review_required=true.",
        "- Deterministic heuristic review only, no LLM or external APIs.",
        "",
        "## Next Step",
        f"- {len(accepted)} candidates accepted for catalog schema",
        f"- {len(needs_more)} candidates need more source data",
        f"- Next possible step: business_direction_catalog_schema_v0",
        "",
    ])

    return "\n".join(lines)


def main():
    # Load bridge candidates
    bridge = load_json(PARSED_DIR / "source_bridge_candidates.json")

    # Get commit SHA
    import subprocess
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=str(PARSED_DIR.parent.parent.parent)
    )
    commit_sha = result.stdout.strip()

    # Review each candidate
    reviewed = []
    for candidate in bridge:
        reviewed.append(review_candidate(candidate))

    review_data = {
        "run_mode": "human_review_of_bridge_candidates_push",
        "source_bridge_input_commit": commit_sha,
        "candidate_count": len(reviewed),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "candidates": reviewed,
        "blocked_sources_not_used": [
            "okpd2_official", "okz_official", "okpdtr_all",
            "trudvsem_api", "social_contract", "etks_mintrud"
        ],
        "next_step": "business_direction_catalog_schema_v0",
    }

    # Save review JSON
    save_json(PARSED_DIR / "source_bridge_review.json", review_data)

    # Generate and save report
    report = generate_report(review_data)
    save_text(REPORTS_DIR / "source_bridge_human_review.md", report)

    # Print summary
    accepted = sum(1 for c in reviewed if c["review_overall_status"] == "accepted_for_catalog_schema")
    needs = sum(1 for c in reviewed if c["review_overall_status"] == "needs_more_source_before_catalog")
    rejected = sum(1 for c in reviewed if c["review_overall_status"] == "rejected_for_now")
    print(f"Reviewed: {len(reviewed)} candidates")
    print(f"Accepted: {accepted}, Needs more source: {needs}, Rejected: {rejected}")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path, text):
    with open(path, "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()

"""
Fix source quality matrix based on actual parsed data.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"


def main():
    print("Fixing Source Quality Matrix")

    # Check what was actually parsed
    okved_exists = (PARSED_DIR / "okved2_raw.json").exists()
    profstandards_exists = (PARSED_DIR / "profstandards_raw.json").exists()

    if okved_exists:
        with open(PARSED_DIR / "okved2_raw.json", encoding="utf-8") as f:
            okved_rows = len(json.load(f))
    else:
        okved_rows = 0

    if profstandards_exists:
        with open(PARSED_DIR / "profstandards_raw.json", encoding="utf-8") as f:
            profstandards_rows = len(json.load(f))
    else:
        profstandards_rows = 0

    print(f"  ОКВЭД 2: {okved_rows} rows parsed")
    print(f"  Profstandards: {profstandards_rows} rows parsed")

    # Build corrected matrix
    matrix = [
        {
            "source_id": "okved2_rosstat",
            "name": "ОКВЭД 2 (Росстат)",
            "status": "primary" if okved_rows > 0 else "not_parsed",
            "official_score": 5,
            "machine_readable_score": 5 if okved_rows > 0 else 2,
            "completeness_score": 5 if okved_rows > 0 else 3,
            "ease_of_ingestion_score": 5 if okved_rows > 0 else 2,
            "legal_safety_score": 5,
            "update_freshness": "2026-06-01",
            "parsed_rows": okved_rows,
            "recommended_use": "primary" if okved_rows > 0 else "candidate",
            "reason": f"Official CSV downloaded and parsed: {okved_rows} rows" if okved_rows > 0 else "Needs download"
        },
        {
            "source_id": "okved2_fns",
            "name": "ОКВЭД 2 (ФНС)",
            "status": "validation",
            "official_score": 5,
            "machine_readable_score": 1,
            "completeness_score": 2,
            "ease_of_ingestion_score": 1,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "parsed_rows": 0,
            "recommended_use": "validation",
            "reason": "Web interface only, useful for validation"
        },
        {
            "source_id": "okpd2_official",
            "name": "ОКПД 2 (ОК 034-2014)",
            "status": "not_probed",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "parsed_rows": 0,
            "recommended_use": "next_probe",
            "reason": "Not yet probed in this run"
        },
        {
            "source_id": "okpdtr_mintrud",
            "name": "ОКПДТР (Минтруд)",
            "status": "not_probed",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "parsed_rows": 0,
            "recommended_use": "next_probe",
            "reason": "Not yet probed in this run"
        },
        {
            "source_id": "okz_mintrud",
            "name": "ОКЗ-2014 (Минтруд)",
            "status": "not_probed",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "parsed_rows": 0,
            "recommended_use": "next_probe",
            "reason": "Not yet probed in this run"
        },
        {
            "source_id": "profstandarts_mintrud",
            "name": "Реестр профстандартов",
            "status": "primary" if profstandards_rows > 0 else "not_parsed",
            "official_score": 5,
            "machine_readable_score": 5 if profstandards_rows > 0 else 2,
            "completeness_score": 5 if profstandards_rows > 0 else 3,
            "ease_of_ingestion_score": 5 if profstandards_rows > 0 else 2,
            "legal_safety_score": 5,
            "update_freshness": "2017-05-12",
            "parsed_rows": profstandards_rows,
            "recommended_use": "primary" if profstandards_rows > 0 else "candidate",
            "reason": f"Official CSV downloaded and parsed: {profstandards_rows} rows" if profstandards_rows > 0 else "Needs download"
        },
        {
            "source_id": "etks_mintrud",
            "name": "ЕТКС (Минтруд)",
            "status": "not_probed",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "parsed_rows": 0,
            "recommended_use": "next_probe",
            "reason": "Not yet probed in this run"
        },
        {
            "source_id": "trudvsem_api",
            "name": "Трудвсем API",
            "status": "candidate_primary_blocked_by_network",
            "official_score": 5,
            "machine_readable_score": 5,
            "completeness_score": 4,
            "ease_of_ingestion_score": 4,
            "legal_safety_score": 5,
            "update_freshness": "realtime",
            "parsed_rows": 0,
            "recommended_use": "candidate_primary_blocked_by_network",
            "reason": "QRATOR anti-bot blocks API from this server"
        },
        {
            "source_id": "npd_nalog",
            "name": "НПД ограничения",
            "status": "primary",
            "official_score": 5,
            "machine_readable_score": 1,
            "completeness_score": 4,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "stable",
            "parsed_rows": 8,
            "recommended_use": "primary",
            "reason": "8 rules manually encoded from official source"
        },
        {
            "source_id": "social_contract",
            "name": "Соцконтракт",
            "status": "candidate_primary_blocked_by_network",
            "official_score": 4,
            "machine_readable_score": 1,
            "completeness_score": 2,
            "ease_of_ingestion_score": 1,
            "legal_safety_score": 4,
            "update_freshness": "regional",
            "parsed_rows": 0,
            "recommended_use": "candidate_primary_blocked_by_network",
            "reason": "Federal and regional pages timeout from this server"
        }
    ]

    # Save JSON
    output_json = PARSED_DIR / "source_quality_matrix.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)
    print(f"Saved: {output_json}")

    # Save markdown
    output_md = REPORTS_DIR / "source_map.md"
    lines = ["# Source Map (Corrected)", ""]
    lines.append("| Source | Status | Parsed Rows | Recommended Use | Reason |")
    lines.append("|--------|--------|-------------|-----------------|--------|")

    for s in matrix:
        lines.append(f"| {s['name']} | {s['status']} | {s['parsed_rows']} | {s['recommended_use']} | {s['reason']} |")

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Primary sources: {sum(1 for s in matrix if s['recommended_use'] == 'primary')}")
    lines.append(f"- Candidate primary (blocked): {sum(1 for s in matrix if s['recommended_use'] == 'candidate_primary_blocked_by_network')}")
    lines.append(f"- Next probe: {sum(1 for s in matrix if s['recommended_use'] == 'next_probe')}")
    lines.append(f"- Validation: {sum(1 for s in matrix if s['recommended_use'] == 'validation')}")

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {output_md}")

    print("\nCorrection complete")


if __name__ == "__main__":
    main()

"""
Update source quality matrix and source registry for v3.
"""

import json
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"


def main():
    print("Updating source quality matrix and registry")

    # Check what was actually parsed
    okved_rows = 0
    profstandards_rows = 0
    okpd2_rows = 0
    okpdtr_rows = 0
    okz_rows = 0

    for filename, field in [
        ("okved2_raw.json", "okved"),
        ("profstandards_raw.json", "profstandards"),
        ("okpd2_raw.json", "okpd2"),
        ("okpdtr_raw.json", "okpdtr"),
        ("okz_raw.json", "okz"),
    ]:
        path = PARSED_DIR / filename
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "rows" in data:
                    count = len(data["rows"])
                elif isinstance(data, list):
                    count = len(data)
                else:
                    count = 0
                if field == "okved":
                    okved_rows = count
                elif field == "profstandards":
                    profstandards_rows = count
                elif field == "okpd2":
                    okpd2_rows = count
                elif field == "okpdtr":
                    okpdtr_rows = count
                elif field == "okz":
                    okz_rows = count

    print(f"Parsed rows:")
    print(f"  ОКВЭД 2: {okved_rows}")
    print(f"  Профстандарты: {profstandards_rows}")
    print(f"  ОКПД 2: {okpd2_rows}")
    print(f"  ОКПДТР: {okpdtr_rows}")
    print(f"  ОКЗ: {okz_rows}")

    # Build corrected matrix
    matrix = [
        {
            "source_id": "okved2_rosstat",
            "name": "ОКВЭД 2 (Росстат)",
            "status": "primary" if okved_rows > 0 else "not_parsed",
            "official_score": 5,
            "machine_readable_score": 5 if okved_rows > 0 else 2,
            "parsed_rows": okved_rows,
            "recommended_use": "primary" if okved_rows > 0 else "candidate",
            "reason": f"Official CSV parsed: {okved_rows} rows" if okved_rows > 0 else "Needs download"
        },
        {
            "source_id": "okved2_fns",
            "name": "ОКВЭД 2 (ФНС)",
            "status": "validation",
            "official_score": 5,
            "machine_readable_score": 1,
            "parsed_rows": 0,
            "recommended_use": "validation",
            "reason": "Web interface only"
        },
        {
            "source_id": "okpd2_official",
            "name": "ОКПД 2 (ОК 034-2014)",
            "status": "candidate_blocked_or_manual" if okpd2_rows == 0 else "primary",
            "official_score": 5,
            "machine_readable_score": 2 if okpd2_rows == 0 else 5,
            "parsed_rows": okpd2_rows,
            "recommended_use": "candidate_blocked_or_manual" if okpd2_rows == 0 else "primary",
            "reason": f"Official HTML only, needs manual download" if okpd2_rows == 0 else f"Parsed: {okpd2_rows} rows"
        },
        {
            "source_id": "okpdtr_mintrud",
            "name": "ОКПДТР (Минтруд)",
            "status": "candidate_blocked_or_manual" if okpdtr_rows == 0 else "primary",
            "official_score": 5,
            "machine_readable_score": 2 if okpdtr_rows == 0 else 5,
            "parsed_rows": okpdtr_rows,
            "recommended_use": "candidate_blocked_or_manual" if okpdtr_rows == 0 else "primary",
            "reason": f"Official HTML only, needs manual download" if okpdtr_rows == 0 else f"Parsed: {okpdtr_rows} rows"
        },
        {
            "source_id": "okz_mintrud",
            "name": "ОКЗ-2014 (Минтруд)",
            "status": "candidate_blocked_or_manual" if okz_rows == 0 else "primary",
            "official_score": 5,
            "machine_readable_score": 2 if okz_rows == 0 else 5,
            "parsed_rows": okz_rows,
            "recommended_use": "candidate_blocked_or_manual" if okz_rows == 0 else "primary",
            "reason": f"Official HTML only, needs manual download" if okz_rows == 0 else f"Parsed: {okz_rows} rows"
        },
        {
            "source_id": "profstandarts_mintrud",
            "name": "Реестр профстандартов",
            "status": "primary" if profstandards_rows > 0 else "not_parsed",
            "official_score": 5,
            "machine_readable_score": 5 if profstandards_rows > 0 else 2,
            "parsed_rows": profstandards_rows,
            "recommended_use": "primary" if profstandards_rows > 0 else "candidate",
            "reason": f"Official CSV parsed: {profstandards_rows} rows" if profstandards_rows > 0 else "Needs download"
        },
        {
            "source_id": "etks_mintrud",
            "name": "ЕТКС (Минтруд)",
            "status": "not_probed",
            "official_score": 5,
            "machine_readable_score": 2,
            "parsed_rows": 0,
            "recommended_use": "next_probe",
            "reason": "Not yet probed"
        },
        {
            "source_id": "trudvsem_api",
            "name": "Трудвсем API",
            "status": "candidate_primary_blocked_by_network",
            "official_score": 5,
            "machine_readable_score": 5,
            "parsed_rows": 0,
            "recommended_use": "candidate_primary_blocked_by_network",
            "reason": "QRATOR anti-bot blocks API"
        },
        {
            "source_id": "npd_nalog",
            "name": "НПД ограничения",
            "status": "primary",
            "official_score": 5,
            "machine_readable_score": 1,
            "parsed_rows": 8,
            "recommended_use": "primary",
            "reason": "8 rules manually encoded"
        },
        {
            "source_id": "social_contract",
            "name": "Соцконтракт",
            "status": "candidate_primary_blocked_by_network",
            "official_score": 4,
            "machine_readable_score": 1,
            "parsed_rows": 0,
            "recommended_use": "candidate_primary_blocked_by_network",
            "reason": "Federal/regional pages timeout"
        }
    ]

    # Save JSON
    output_json = PARSED_DIR / "source_quality_matrix.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)
    print(f"Saved: {output_json}")

    # Save markdown
    output_md = REPORTS_DIR / "source_map.md"
    lines = ["# Source Map (v3)", ""]
    lines.append("| Source | Status | Parsed Rows | Recommended Use | Reason |")
    lines.append("|--------|--------|-------------|-----------------|--------|")

    for s in matrix:
        lines.append(f"| {s['name']} | {s['status']} | {s['parsed_rows']} | {s['recommended_use']} | {s['reason']} |")

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Primary sources: {sum(1 for s in matrix if s['recommended_use'] == 'primary')}")
    lines.append(f"- Candidate blocked/manual: {sum(1 for s in matrix if s['recommended_use'] == 'candidate_blocked_or_manual')}")
    lines.append(f"- Next probe: {sum(1 for s in matrix if s['recommended_use'] == 'next_probe')}")
    lines.append(f"- Validation: {sum(1 for s in matrix if s['recommended_use'] == 'validation')}")

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {output_md}")

    print("\nUpdate complete")


if __name__ == "__main__":
    main()

"""
Build source quality matrix from ingestion results.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"


def build_quality_matrix():
    """Build quality matrix for all sources."""
    matrix = []

    sources = [
        {
            "source_id": "okved2_rosstat",
            "name": "ОКВЭД 2 (Росстат)",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "primary",
            "reason": "Official classifier, but needs manual file discovery"
        },
        {
            "source_id": "okved2_fns",
            "name": "ОКВЭД 2 (ФНС)",
            "official_score": 5,
            "machine_readable_score": 1,
            "completeness_score": 2,
            "ease_of_ingestion_score": 1,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "validation",
            "reason": "Web interface only, useful for validation"
        },
        {
            "source_id": "okpd2_official",
            "name": "ОКПД 2 (ОК 034-2014)",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "enrichment",
            "reason": "Official classifier, needs file discovery"
        },
        {
            "source_id": "okpdtr_mintrud",
            "name": "ОКПДТР (Минтруд)",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "enrichment",
            "reason": "Official classifier, needs page parsing"
        },
        {
            "source_id": "okz_mintrud",
            "name": "ОКЗ-2014 (Минтруд)",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "enrichment",
            "reason": "Official classifier, needs page parsing"
        },
        {
            "source_id": "profstandarts_mintrud",
            "name": "Реестр профстандартов",
            "official_score": 5,
            "machine_readable_score": 4,
            "completeness_score": 4,
            "ease_of_ingestion_score": 3,
            "legal_safety_score": 5,
            "update_freshness": "periodic",
            "recommended_use": "primary",
            "reason": "Open data portal, CSV/XML expected"
        },
        {
            "source_id": "etks_mintrud",
            "name": "ЕТКС (Минтруд)",
            "official_score": 5,
            "machine_readable_score": 2,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "unknown",
            "recommended_use": "enrichment",
            "reason": "Official, needs page parsing"
        },
        {
            "source_id": "trudvsem_api",
            "name": "Трудвсем API",
            "official_score": 5,
            "machine_readable_score": 5,
            "completeness_score": 4,
            "ease_of_ingestion_score": 4,
            "legal_safety_score": 5,
            "update_freshness": "realtime",
            "recommended_use": "primary",
            "reason": "Public API, JSON response, no key needed"
        },
        {
            "source_id": "npd_nalog",
            "name": "НПД ограничения",
            "official_score": 5,
            "machine_readable_score": 1,
            "completeness_score": 3,
            "ease_of_ingestion_score": 2,
            "legal_safety_score": 5,
            "update_freshness": "stable",
            "recommended_use": "primary",
            "reason": "Rules encoded manually, legally authoritative"
        },
        {
            "source_id": "social_contract",
            "name": "Соцконтракт",
            "official_score": 4,
            "machine_readable_score": 1,
            "completeness_score": 2,
            "ease_of_ingestion_score": 1,
            "legal_safety_score": 4,
            "update_freshness": "regional",
            "recommended_use": "enrichment",
            "reason": "Regional rules, needs manual encoding"
        }
    ]

    return sources


def main():
    """Build and save quality matrix."""
    print("Building Source Quality Matrix")

    matrix = build_quality_matrix()

    # Save JSON
    output_json = PARSED_DIR / "source_quality_matrix.json"
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)
    print(f"  Saved JSON: {output_json}")

    # Save markdown report
    output_md = REPORTS_DIR / "source_map.md"
    output_md.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# Source Map", ""]
    lines.append("| Source | Official | Machine Readable | Recommended Use | Reason |")
    lines.append("|--------|----------|------------------|-----------------|--------|")

    for s in matrix:
        lines.append(f"| {s['name']} | {s['official_score']}/5 | {s['machine_readable_score']}/5 | {s['recommended_use']} | {s['reason']} |")

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Primary sources: {sum(1 for s in matrix if s['recommended_use'] == 'primary')}")
    lines.append(f"- Enrichment sources: {sum(1 for s in matrix if s['recommended_use'] == 'enrichment')}")
    lines.append(f"- Validation sources: {sum(1 for s in matrix if s['recommended_use'] == 'validation')}")
    lines.append(f"- Rejected sources: {sum(1 for s in matrix if s['recommended_use'] == 'reject')}")

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved MD: {output_md}")

    print(f"\nQuality matrix built with {len(matrix)} sources")


if __name__ == "__main__":
    main()

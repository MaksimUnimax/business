"""
Parse ОКПДТР from available sources.
If no machine-readable source found, mark as needing manual download.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okpdtr"
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"

# Candidate keywords
PROFESSION_KEYWORDS = [
    "сборщик", "мебель", "ремонт", "слесарь", "электрик", "сантехник",
    "швея", "портной", "обувщик", "парикмахер", "косметик", "маникюр",
    "педикюр", "уборщик", "клининг", "чистильщик", "заточник", "веломеханик",
    "механик", "мастер", "фотограф", "оператор", "педагог", "инструктор",
    "животновод", "садовник",
]


def is_profession_candidate(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in PROFESSION_KEYWORDS)


def main():
    print("Parsing ОКПДТР")

    # Check if we have any structured data
    json_file = RAW_DIR / "okpdtr_source.json"
    csv_file = RAW_DIR / "okpdtr_source.csv"

    if csv_file.exists():
        print(f"Found CSV: {csv_file}")
        # Parse CSV
        import csv
        rows = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"Parsed {len(rows)} rows from CSV")
    elif json_file.exists():
        print(f"Found JSON: {json_file}")
        with open(json_file, encoding="utf-8") as f:
            rows = json.load(f)
        print(f"Parsed {len(rows)} rows from JSON")
    else:
        print("No machine-readable ОКПДТР source found")
        print("Creating placeholder with source status")

        # Create placeholder
        raw_json = PARSED_DIR / "okpdtr_raw.json"
        with open(raw_json, "w", encoding="utf-8") as f:
            json.dump({
                "status": "needs_manual_download",
                "source_urls_tried": [
                    "https://mintrud.gov.ru/opendata",
                    "https://profstandart.rosmintrud.ru/",
                    "https://base.garant.ru/71166760/",
                ],
                "classifier_version": "ok_016_2025_or_ok_016_94",
                "source_status": "official_html_only",
                "rows": [],
            }, f, ensure_ascii=False, indent=2)
        print(f"Saved: {raw_json}")

        # Create empty candidates
        cand_json = PARSED_DIR / "okpdtr_profession_candidates.json"
        with open(cand_json, "w", encoding="utf-8") as f:
            json.dump([], f)
        print(f"Saved: {cand_json}")

        return

    # If we have rows, parse them
    parsed_rows = []
    for r in rows:
        parsed_rows.append({
            "source": "okpdtr",
            "code": r.get("code", r.get("Code", "")),
            "title": r.get("title", r.get("Title", r.get("name", ""))),
            "type": r.get("type", "unknown"),
            "tariff_grade": r.get("tariff_grade", ""),
            "okz_related_code": r.get("okz_related_code", ""),
            "classifier_version": "unknown",
            "source_status": "mirror_unofficial",
        })

    # Save raw
    raw_json = PARSED_DIR / "okpdtr_raw.json"
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(parsed_rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {raw_json}")

    # Profession candidates
    candidates = []
    for r in parsed_rows:
        if is_profession_candidate(r["title"]):
            candidates.append({
                "source": "okpdtr",
                "code": r["code"],
                "title": r["title"],
                "type": r["type"],
                "matched_keywords": [kw for kw in PROFESSION_KEYWORDS if kw in r["title"].lower()],
                "source_status": r["source_status"],
            })

    cand_json = PARSED_DIR / "okpdtr_profession_candidates.json"
    with open(cand_json, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"Saved: {cand_json}")
    print(f"Profession candidates: {len(candidates)}")


if __name__ == "__main__":
    main()

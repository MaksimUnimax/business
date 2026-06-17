"""
Parse ОКЗ from available sources.
If no machine-readable source found, mark as needing manual download.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okz"
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"

# Candidate keywords
OCCUPATION_KEYWORDS = [
    "ремонт", "услуг", "персональн", "рабочие", "квалифицированные",
    "сфера обслуживания", "производство", "ремесленники", "операторы",
    "водители", "уход", "образование", "здравоохранение", "техники",
    "электрики", "строители", "ремонтники",
]


def is_occupation_candidate(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in OCCUPATION_KEYWORDS)


def main():
    print("Parsing ОКЗ")

    # Check if we have any structured data
    json_file = RAW_DIR / "okz_source.json"
    csv_file = RAW_DIR / "okz_source.csv"

    if csv_file.exists():
        print(f"Found CSV: {csv_file}")
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
        print("No machine-readable ОКЗ source found")
        print("Creating placeholder with source status")

        # Create placeholder
        raw_json = PARSED_DIR / "okz_raw.json"
        with open(raw_json, "w", encoding="utf-8") as f:
            json.dump({
                "status": "needs_manual_download",
                "source_urls_tried": [
                    "https://mintrud.gov.ru/opendata",
                    "https://profstandart.rosmintrud.ru/",
                    "https://base.garant.ru/79729182/",
                ],
                "source_status": "official_html_only",
                "rows": [],
            }, f, ensure_ascii=False, indent=2)
        print(f"Saved: {raw_json}")

        # Create empty candidates
        cand_json = PARSED_DIR / "okz_service_occupation_candidates.json"
        with open(cand_json, "w", encoding="utf-8") as f:
            json.dump([], f)
        print(f"Saved: {cand_json}")

        return

    # If we have rows, parse them
    parsed_rows = []
    for r in rows:
        parsed_rows.append({
            "source": "okz",
            "code": r.get("code", r.get("Code", "")),
            "title": r.get("title", r.get("Title", r.get("name", ""))),
            "parent_code": r.get("parent_code", ""),
            "group_level": r.get("group_level", ""),
            "source_status": "mirror_unofficial",
        })

    # Save raw
    raw_json = PARSED_DIR / "okz_raw.json"
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(parsed_rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {raw_json}")

    # Occupation candidates
    candidates = []
    for r in parsed_rows:
        if is_occupation_candidate(r["title"]):
            candidates.append({
                "source": "okz",
                "code": r["code"],
                "title": r["title"],
                "matched_keywords": [kw for kw in OCCUPATION_KEYWORDS if kw in r["title"].lower()],
                "source_status": r["source_status"],
            })

    cand_json = PARSED_DIR / "okz_service_occupation_candidates.json"
    with open(cand_json, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"Saved: {cand_json}")
    print(f"Occupation candidates: {len(candidates)}")


if __name__ == "__main__":
    main()

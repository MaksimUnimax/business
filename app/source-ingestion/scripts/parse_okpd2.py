"""
Parse ОКПД 2 from available sources.
If no machine-readable source found, mark as needing manual download.
"""

import json
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okpd2"
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"

# Service candidate keywords
SERVICE_KEYWORDS = [
    "ремонт", "услуг", "работ", "чистк", "уборк", "клининг", "пошив",
    "одежд", "обув", "мебел", "изготовление", "производство изделий",
    "бытов", "персональн", "образован", "обучен", "фото", "видео",
    "уход", "животн", "растен", "техническое обслуживание", "парикмах",
    "космет", "маникюр", "педикюр", "велосип", "инструмент", "заточка",
]


def is_service_candidate(name: str) -> bool:
    name_lower = name.lower()
    return any(kw in name_lower for kw in SERVICE_KEYWORDS)


def main():
    print("Parsing ОКПД 2")

    # Check if we have any structured data
    json_file = RAW_DIR / "okpd2_source.json"
    csv_file = RAW_DIR / "okpd2_source.csv"

    if csv_file.exists():
        print(f"Found CSV: {csv_file}")
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
        print("No machine-readable ОКПД 2 source found")
        print("Creating placeholder with source status")

        # Create placeholder indicating manual download needed
        rows = []

        # Save raw with status
        raw_json = PARSED_DIR / "okpd2_raw.json"
        with open(raw_json, "w", encoding="utf-8") as f:
            json.dump({
                "status": "needs_manual_download",
                "source_urls_tried": [
                    "https://docs.cntd.ru/document/1200116381",
                    "https://base.garant.ru/70474890/",
                    "https://www.consultant.ru/document/cons_doc_LAW_163680/",
                ],
                "source_status": "official_html_only",
                "rows": [],
            }, f, ensure_ascii=False, indent=2)
        print(f"Saved: {raw_json}")

        # Create empty candidates
        cand_json = PARSED_DIR / "okpd2_service_work_candidates.json"
        with open(cand_json, "w", encoding="utf-8") as f:
            json.dump([], f)
        print(f"Saved: {cand_json}")

        return

    # If we have rows, parse them
    parsed_rows = []
    for r in rows:
        parsed_rows.append({
            "source": "okpd2",
            "code": r.get("code", r.get("Code", "")),
            "name": r.get("name", r.get("Name", "")),
            "parent_code": r.get("parent_code", ""),
            "level": r.get("level", ""),
            "source_status": "mirror_unofficial",
        })

    # Save raw
    raw_json = PARSED_DIR / "okpd2_raw.json"
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(parsed_rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {raw_json}")

    # Service candidates
    candidates = []
    for r in parsed_rows:
        if is_service_candidate(r["name"]):
            candidates.append({
                "source": "okpd2",
                "code": r["code"],
                "name": r["name"],
                "candidate_type": "service/work",
                "matched_keywords": [kw for kw in SERVICE_KEYWORDS if kw in r["name"].lower()],
                "source_status": r["source_status"],
            })

    cand_json = PARSED_DIR / "okpd2_service_work_candidates.json"
    with open(cand_json, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"Saved: {cand_json}")
    print(f"Service/work candidates: {len(candidates)}")


if __name__ == "__main__":
    main()

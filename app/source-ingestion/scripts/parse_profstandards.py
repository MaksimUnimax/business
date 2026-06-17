"""
Parse profstandards CSV into normalized JSON and service candidates.
"""

import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "mintrud_profstandards"
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"

# Service candidate keywords
SERVICE_KEYWORDS = [
    "мебел", "ремонт", "чистк", "клининг", "парикмах", "космет",
    "маникюр", "педикюр", "пошив", "одежд", "обув", "велосип",
    "животн", "педагог", "дополнительное образование", "фото", "видео",
    "садов", "растен", "слесар", "электрик", "сантехник",
    "строительств", "отделк", "монтаж", "обслуживан",
    "перевозк", "доставк", "грузооборот",
    "обработк", "переработк", "упаковк",
    "консульт", "обучен", "подготовк",
    "програм", "разработк", "дизайн",
    "уборк", "стирк", "пран",
]


def is_service_candidate(name: str, area: str, ptype: str) -> bool:
    """Check if name/area/type matches service keywords."""
    combined = f"{name} {area} {ptype}".lower()
    return any(kw in combined for kw in SERVICE_KEYWORDS)


def main():
    print("Parsing profstandards")

    data_file = RAW_DIR / "data.csv"
    if not data_file.exists():
        print("ERROR: data.csv not found")
        return

    rows = []
    with open(data_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar='"')
        for row in reader:
            if row.get("standard_number"):
                rows.append({
                    "source": "profstandarts_mintrud",
                    "number": row.get("number", ""),
                    "standard_number": row.get("standard_number", ""),
                    "standard_code": row.get("standard_code", ""),
                    "professional_area": row.get("professional_area", ""),
                    "professional_type": row.get("professional_type", ""),
                    "standard_name": row.get("standard_name", ""),
                    "order_Mintrud": row.get("order_Mintrud", ""),
                })

    print(f"Parsed {len(rows)} rows")

    # Save raw JSON
    raw_json = PARSED_DIR / "profstandards_raw.json"
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {raw_json}")

    # Service candidates
    candidates = []
    for r in rows:
        if is_service_candidate(
            r["standard_name"],
            r["professional_area"],
            r["professional_type"],
        ):
            candidates.append({
                "source": "profstandarts_mintrud",
                "standard_number": r["standard_number"],
                "standard_code": r["standard_code"],
                "professional_area": r["professional_area"],
                "professional_type": r["professional_type"],
                "standard_name": r["standard_name"],
                "matched_keywords": [kw for kw in SERVICE_KEYWORDS if kw in f"{r['standard_name']} {r['professional_area']} {r['professional_type']}".lower()],
            })

    cand_json = PARSED_DIR / "profstandards_service_candidates.json"
    with open(cand_json, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"Saved: {cand_json}")
    print(f"Service candidates: {len(candidates)}")

    # Summary
    print("\nSummary:")
    print(f"  Total rows: {len(rows)}")
    areas = set(r["professional_area"] for r in rows)
    print(f"  Professional areas: {len(areas)}")
    for a in sorted(areas)[:10]:
        print(f"    - {a}")


if __name__ == "__main__":
    main()

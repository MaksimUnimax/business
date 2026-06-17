"""
Parse ОКВЭД 2 CSV into normalized JSON and CSV.
"""

import csv
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okved"
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"
PARSED_DIR.mkdir(parents=True, exist_ok=True)

# Service candidate keywords
SERVICE_KEYWORDS = [
    "ремонт", "услуг", "чистк", "уборк", "пошив", "одежд", "обув",
    "мебел", "образован", "фото", "видео", "парикмах", "космет",
    "уход", "животн", "растен", "производство изделий", "изготовление",
    "бытов", "персональн", "техническое обслуживание", "ремонт компьютеров",
    "ремонт бытовой техники", "клининг", "стирк", "пран",
    "строительств", "отделк", "монтаж", "эксплуатаци",
    "транспорт", "перевозк", "логистик", "склад",
    "обработк", "переработк", "упаковк",
    "консульт", "подбор", "подготовк", "обучен", "обуч",
    "програм", "разработк", "дизайн",
    "содержан", "обслуживан", "обслуг",
]


def parse_code_level(code: str) -> str:
    """Determine level from code structure."""
    code = code.strip()
    if not code or not code[0].isalpha():
        return "unknown"
    parts = code.split(".")
    if len(parts) == 1:
        return "section"
    elif len(parts) == 2:
        return "class"
    elif len(parts) == 3:
        return "subclass"
    elif len(parts) == 4:
        return "group"
    elif len(parts) == 5:
        return "subgroup"
    return "unknown"


def is_service_candidate(name: str) -> bool:
    """Check if name matches service keywords."""
    name_lower = name.lower()
    return any(kw in name_lower for kw in SERVICE_KEYWORDS)


def main():
    print("Parsing ОКВЭД 2")

    data_file = RAW_DIR / "data_latest.csv"
    if not data_file.exists():
        print("ERROR: data_latest.csv not found")
        return

    rows = []
    with open(data_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')
        for row in reader:
            if len(row) >= 3:
                razdel = row[0].strip()
                code = row[1].strip()
                name = row[2].strip()
                if code and name:
                    rows.append({
                        "razdel": razdel,
                        "code": code,
                        "name": name,
                        "level": parse_code_level(code),
                        "parent_code": ".".join(code.split(".")[:-1]) if "." in code else "",
                    })

    print(f"Parsed {len(rows)} rows")

    # Save raw JSON
    raw_json = PARSED_DIR / "okved2_raw.json"
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {raw_json}")

    # Save raw CSV
    raw_csv = PARSED_DIR / "okved2_raw.csv"
    with open(raw_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["razdel", "code", "name", "level", "parent_code"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {raw_csv}")

    # Normalize
    normalized = []
    for r in rows:
        normalized.append({
            "source": "okved2_rosstat",
            "code": r["code"],
            "name": r["name"],
            "section": r["razdel"],
            "level": r["level"],
            "parent_code": r["parent_code"],
        })

    norm_json = PARSED_DIR / "okved2_normalized.json"
    with open(norm_json, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    print(f"Saved: {norm_json}")

    # Service candidates
    candidates = []
    for r in rows:
        if is_service_candidate(r["name"]):
            candidates.append({
                "source": "okved2_rosstat",
                "code": r["code"],
                "name": r["name"],
                "section": r["razdel"],
                "level": r["level"],
                "matched_keywords": [kw for kw in SERVICE_KEYWORDS if kw in r["name"].lower()],
            })

    cand_json = PARSED_DIR / "okved2_service_candidates.json"
    with open(cand_json, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"Saved: {cand_json}")
    print(f"Service candidates: {len(candidates)}")

    # Summary
    print("\nSummary:")
    print(f"  Total rows: {len(rows)}")
    print(f"  Levels: {set(r['level'] for r in rows)}")
    print(f"  Sections: {set(r['razdel'] for r in rows)}")
    print(f"  Service candidates: {len(candidates)}")


if __name__ == "__main__":
    main()

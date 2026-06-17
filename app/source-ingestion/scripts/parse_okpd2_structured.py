#!/usr/bin/env python3
"""Parse OKPD2 (ОК 034-2014) from downloaded xlsx."""
import json
import os
import re
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "okpd2")
PARSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "parsed")

SERVICE_WORK_KEYWORDS = [
    "ремонт", "услуг", "работ", "чистк", "уборк", "клининг", "пошив", "одежд",
    "обув", "мебел", "изготовление", "бытов", "персональн", "образован", "фото",
    "видео", "уход", "животн", "растен", "техническое обслуживание", "парикмах",
    "космет", "маникюр", "педикюр", "велосип", "заточка", "инструмент",
]


def infer_level(code):
    parts = code.split(".")
    return len(parts)


def infer_parent(code):
    parts = code.split(".")
    if len(parts) <= 1:
        return None
    return ".".join(parts[:-1])


def classify_candidate(name):
    name_lower = name.lower()
    for kw in SERVICE_WORK_KEYWORDS:
        if kw in name_lower:
            if any(w in name_lower for w in ["услуг", "обслужив"]):
                return "service"
            if any(w in name_lower for w in ["работ", "ремонт", "изготовлен"]):
                return "work"
            return "service"
    return "unknown"


def parse():
    xlsx_path = os.path.join(RAW_DIR, "okpd_classifikators.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"ERROR: {xlsx_path} not found")
        return 0

    df = pd.read_excel(xlsx_path, header=None)
    raw_rows = []
    parsed_rows = 0

    for idx in range(7, len(df)):
        row = df.iloc[idx]
        code = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        name = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""

        if re.match(r"^\d{2}(\.\d+)*$", code):
            level = infer_level(code)
            parent_code = infer_parent(code)
            candidate_type = classify_candidate(name)

            raw_rows.append({
                "code": code,
                "name": name,
                "parent_code": parent_code,
                "level": level,
                "source_url": "https://classifikators.ru/okpd",
                "source_status": "mirror_unofficial",
                "source_file": "okpd_classifikators.xlsx",
                "candidate_type": candidate_type,
            })
            parsed_rows += 1

    os.makedirs(PARSED_DIR, exist_ok=True)

    with open(os.path.join(PARSED_DIR, "okpd2_raw.json"), "w", encoding="utf-8") as f:
        json.dump(raw_rows, f, ensure_ascii=False, indent=2)

    with open(os.path.join(PARSED_DIR, "okpd2_raw.csv"), "w", encoding="utf-8") as f:
        f.write("code,name,parent_code,level,source_url,source_status,source_file,candidate_type\n")
        for r in raw_rows:
            f.write(f"{r['code']},{r['name']},{r['parent_code'] or ''},{r['level']},{r['source_url']},{r['source_status']},{r['source_file']},{r['candidate_type']}\n")

    candidates = [r for r in raw_rows if r["candidate_type"] != "unknown"]
    with open(os.path.join(PARSED_DIR, "okpd2_service_work_candidates.json"), "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    normalized = []
    for r in raw_rows:
        normalized.append({
            "code": r["code"],
            "name": r["name"],
            "parent_code": r["parent_code"],
            "level": r["level"],
            "source_url": r["source_url"],
            "source_status": r["source_status"],
            "source_file": r["source_file"],
            "candidate_type": r["candidate_type"],
        })
    with open(os.path.join(PARSED_DIR, "okpd2_normalized.json"), "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"OKPD2 parsed: {parsed_rows} rows, {len(candidates)} service/work candidates")
    return parsed_rows


if __name__ == "__main__":
    parse()

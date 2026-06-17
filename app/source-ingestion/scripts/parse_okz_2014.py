#!/usr/bin/env python3
"""Parse OKZ (ОК 010-2014) from downloaded xlsx."""
import json
import os
import re
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "okz")
PARSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "parsed")

OCCUPATION_KEYWORDS = [
    "ремонт", "услуг", "персональн", "рабочие", "сфера обслуживания",
    "производство", "ремесленники", "уход", "образование", "техники",
    "электрики", "строители", "ремонтники", "водители",
]


def infer_group_level(code):
    length = len(code)
    if length <= 2:
        return "major_group"
    elif length == 3:
        return "sub_major_group"
    elif length == 4:
        return "minor_group"
    else:
        return "unit_group"


def infer_parent(code):
    if len(code) <= 2:
        return None
    return code[:-1]


def classify_candidate(name):
    name_lower = name.lower()
    for kw in OCCUPATION_KEYWORDS:
        if kw in name_lower:
            return "occupation"
    return "unknown"


def parse():
    xlsx_path = os.path.join(RAW_DIR, "okz_classifikators.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"ERROR: {xlsx_path} not found")
        return 0

    df = pd.read_excel(xlsx_path, header=None)
    raw_rows = []
    parsed_rows = 0

    for idx in range(7, len(df)):
        row = df.iloc[idx]
        code = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        name = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""

        if re.match(r"^\d{2,4}$", code):
            group_level = infer_group_level(code)
            parent_code = infer_parent(code)
            candidate_type = classify_candidate(name)

            raw_rows.append({
                "code": code,
                "title": name,
                "parent_code": parent_code,
                "group_level": group_level,
                "source_url": "https://classifikators.ru/okz",
                "source_status": "mirror_unofficial",
                "source_file": "okz_classifikators.xlsx",
                "candidate_type": candidate_type,
            })
            parsed_rows += 1

    os.makedirs(PARSED_DIR, exist_ok=True)

    with open(os.path.join(PARSED_DIR, "okz_raw.json"), "w", encoding="utf-8") as f:
        json.dump(raw_rows, f, ensure_ascii=False, indent=2)

    with open(os.path.join(PARSED_DIR, "okz_raw.csv"), "w", encoding="utf-8") as f:
        f.write("code,title,parent_code,group_level,source_url,source_status,source_file,candidate_type\n")
        for r in raw_rows:
            f.write(f"{r['code']},{r['title']},{r['parent_code'] or ''},{r['group_level']},{r['source_url']},{r['source_status']},{r['source_file']},{r['candidate_type']}\n")

    candidates = [r for r in raw_rows if r["candidate_type"] != "unknown"]
    with open(os.path.join(PARSED_DIR, "okz_service_occupation_candidates.json"), "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    normalized = []
    for r in raw_rows:
        normalized.append({
            "code": r["code"],
            "title": r["title"],
            "parent_code": r["parent_code"],
            "group_level": r["group_level"],
            "source_url": r["source_url"],
            "source_status": r["source_status"],
            "source_file": r["source_file"],
            "candidate_type": r["candidate_type"],
        })
    with open(os.path.join(PARSED_DIR, "okz_normalized.json"), "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"OKZ parsed: {parsed_rows} rows, {len(candidates)} occupation candidates")
    return parsed_rows


if __name__ == "__main__":
    parse()

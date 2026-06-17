#!/usr/bin/env python3
"""Parse OKPDTR-2025 (ОК 016-2025).

If structured file exists, parse it. Otherwise, create empty result with status
manual_download_required.
"""
import json
import os
import re
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "okpdtr")
PARSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "parsed")

PROFESSION_KEYWORDS = [
    "сборщик", "мебел", "ремонт", "мастер", "слесарь", "электрик", "сантехник",
    "швея", "портной", "обувщик", "парикмахер", "косметик", "маникюр", "педикюр",
    "уборщик", "чистильщик", "заточник", "механик", "веломеханик", "фотограф",
    "оператор", "педагог", "инструктор", "садовник", "животновод",
]


def parse():
    os.makedirs(PARSED_DIR, exist_ok=True)

    # Check for any downloaded xlsx/xls/csv files
    found_file = None
    if os.path.exists(RAW_DIR):
        for f in os.listdir(RAW_DIR):
            if f.endswith(('.xlsx', '.xls', '.csv')):
                found_file = os.path.join(RAW_DIR, f)
                break

    if found_file:
        # Parse the file
        try:
            df = pd.read_excel(found_file, header=None) if found_file.endswith(('.xlsx', '.xls')) else pd.read_csv(found_file, header=None)
            raw_rows = []
            for idx, row in df.iterrows():
                code = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
                title = str(row.iloc[1]).strip() if len(df.columns) > 1 and pd.notna(row.iloc[1]) else ""

                if re.match(r"^\d{2}(\.\d+)*$", code) or re.match(r"^\d{6}$", code):
                    title_lower = title.lower()
                    is_profession = any(kw in title_lower for kw in PROFESSION_KEYWORDS)

                    raw_rows.append({
                        "code": code,
                        "title": title,
                        "type": "worker_profession" if is_profession else "employee_position",
                        "tariff_grade": None,
                        "classifier_version": "ok_016_2025",
                        "source_url": f"classifikators.ru or downloaded file",
                        "source_status": "mirror_unofficial",
                        "source_file": os.path.basename(found_file),
                    })

            with open(os.path.join(PARSED_DIR, "okpdtr_raw.json"), "w", encoding="utf-8") as f:
                json.dump(raw_rows, f, ensure_ascii=False, indent=2)

            with open(os.path.join(PARSED_DIR, "okpdtr_raw.csv"), "w", encoding="utf-8") as f:
                f.write("code,title,type,tariff_grade,classifier_version,source_url,source_status,source_file\n")
                for r in raw_rows:
                    f.write(f"{r['code']},{r['title']},{r['type']},{r['tariff_grade'] or ''},{r['classifier_version']},{r['source_url']},{r['source_status']},{r['source_file']}\n")

            profession_candidates = [r for r in raw_rows if r["type"] == "worker_profession"]
            with open(os.path.join(PARSED_DIR, "okpdtr_profession_candidates.json"), "w", encoding="utf-8") as f:
                json.dump(profession_candidates, f, ensure_ascii=False, indent=2)

            with open(os.path.join(PARSED_DIR, "okpdtr_normalized.json"), "w", encoding="utf-8") as f:
                json.dump(raw_rows, f, ensure_ascii=False, indent=2)

            print(f"OKPDTR parsed: {len(raw_rows)} rows, {len(profession_candidates)} profession candidates")
            return len(raw_rows)
        except Exception as e:
            print(f"Parse error: {e}")

    # No file found - create empty result
    empty_rows = []
    with open(os.path.join(PARSED_DIR, "okpdtr_raw.json"), "w", encoding="utf-8") as f:
        json.dump(empty_rows, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PARSED_DIR, "okpdtr_raw.csv"), "w", encoding="utf-8") as f:
        f.write("code,title,type,tariff_grade,classifier_version,source_url,source_status,source_file\n")
    with open(os.path.join(PARSED_DIR, "okpdtr_profession_candidates.json"), "w", encoding="utf-8") as f:
        json.dump([], f)
    with open(os.path.join(PARSED_DIR, "okpdtr_normalized.json"), "w", encoding="utf-8") as f:
        json.dump([], f)

    print("OKPDTR: 0 rows parsed (no structured file available)")
    return 0


if __name__ == "__main__":
    parse()

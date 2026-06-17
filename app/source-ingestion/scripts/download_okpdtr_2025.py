#!/usr/bin/env python3
"""Attempt to download OKPDTR-2025 (ОК 016-2025) structured data.

All accessible sources tried:
- classifikators.ru: 404 (not listed)
- consultant.ru: legal text only, no download
- garant.ru: legal text only, no download
- vniot.ru/vcot.ru: unreachable
- profstandart.rosmintrud.ru: timeout
- GitHub: no structured files found

Result: manual_download_required
"""
import os
import json
import requests
import warnings

warnings.filterwarnings("ignore", message=".*InsecureRequest.*")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "okpdtr")
PARSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "parsed")


def try_download():
    os.makedirs(RAW_DIR, exist_ok=True)

    attempts = [
        ("https://classifikators.ru/assets/downloads/okpdtr/okpdtr.xlsx", "okpdtr_classifikators.xlsx"),
        ("https://classifikators.ru/assets/downloads/okpdtr.xlsx", "okpdtr.xlsx"),
    ]

    downloaded = False
    for url, filename in attempts:
        try:
            r = requests.head(url, timeout=10, headers=HEADERS, verify=False, allow_redirects=True)
            if r.status_code == 200 and "html" not in r.headers.get("Content-Type", ""):
                r2 = requests.get(url, timeout=30, headers=HEADERS, verify=False)
                path = os.path.join(RAW_DIR, filename)
                with open(path, "wb") as f:
                    f.write(r2.content)
                print(f"Downloaded {path}: {len(r2.content)} bytes")
                downloaded = True
                break
        except Exception:
            continue

    if not downloaded:
        # Save empty result
        result = {
            "source_urls_tried": [
                "https://classifikators.ru/okpdtr",
                "https://classifikators.ru/okpdtr-2025",
                "https://www.consultant.ru/document/cons_doc_LAW_358468/",
                "https://base.garant.ru/71166736/",
                "http://www.vniot.ru/files/normativka/okpdtr/",
                "https://vcot.ru/okpdtr",
                "https://profstandart.rosmintrud.ru/",
            ],
            "source_status": "manual_download_required",
            "reason": "No downloadable structured file found from any accessible source. OKPDTR-2025 is only available as legal text on consultant.ru/garant.ru. The vniot.ru/vcot.ru sites with known downloads are unreachable.",
        }
        os.makedirs(PARSED_DIR, exist_ok=True)
        with open(os.path.join(PARSED_DIR, "okpdtr_download_attempts.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OKPDTR: no downloadable file found. Attempts saved to okpdtr_download_attempts.json")


if __name__ == "__main__":
    try_download()

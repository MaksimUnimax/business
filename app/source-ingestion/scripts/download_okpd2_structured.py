#!/usr/bin/env python3
"""Download OKPD2 (ОК 034-2014) structured data from classifikators.ru mirror."""
import os
import requests
import warnings

warnings.filterwarnings("ignore", message=".*InsecureRequest.*")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}

SOURCE_URL = "https://classifikators.ru/okpd"
DOWNLOAD_URL = "https://classifikators.ru/assets/downloads/okpd/okpd.xlsx"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "okpd2")


def download():
    os.makedirs(RAW_DIR, exist_ok=True)
    r = requests.get(DOWNLOAD_URL, timeout=30, headers=HEADERS, verify=False)
    r.raise_for_status()
    path = os.path.join(RAW_DIR, "okpd_classifikators.xlsx")
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded {path}: {len(r.content)} bytes")
    return path


if __name__ == "__main__":
    download()

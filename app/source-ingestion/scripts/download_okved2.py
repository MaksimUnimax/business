"""
Download ОКВЭД 2 from Rosstat discovered links.
"""

import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okved"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "source-ingestion-probe/0.1 (research; educational project)"
}

# Discovered links from previous run
LINKS = [
    "https://rosstat.gov.ru/opendata/7708234640-okvedva",
    "https://rosstat.gov.ru/opendata/list.csv",
]


def fetch_url(url, timeout=30):
    """Fetch URL with safe headers."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=False, allow_redirects=True)
        return resp
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    print("Downloading ОКВЭД 2 from Rosstat")
    print("=" * 60)

    for i, url in enumerate(LINKS):
        print(f"\n[{i+1}] Trying: {url}")
        resp = fetch_url(url)
        if resp:
            print(f"  Status: {resp.status_code}")
            print(f"  Content-Type: {resp.headers.get('Content-Type', 'unknown')}")
            print(f"  Size: {len(resp.content)} bytes")

            # Determine extension
            ct = resp.headers.get("Content-Type", "")
            if "csv" in ct or url.endswith(".csv"):
                ext = "csv"
            elif "xml" in ct or url.endswith(".xml"):
                ext = "xml"
            elif "html" in ct:
                ext = "html"
            else:
                ext = "dat"

            filename = f"okved2_source_{i}.{ext}"
            filepath = RAW_DIR / filename
            filepath.write_bytes(resp.content)
            print(f"  Saved: {filepath}")

            # Also try to find actual data file links if this is HTML
            if ext == "html":
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "lxml")
                links = soup.find_all("a", href=True)
                for a in links:
                    href = a["href"]
                    if any(x in href.lower() for x in [".csv", ".xml", ".xls", "okved"]):
                        print(f"  Found link: {href}")
        else:
            print(f"  FAILED")


if __name__ == "__main__":
    main()

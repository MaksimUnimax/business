"""
Probe and download ОКПДТР (ОК 016-2025 or ОК 016-94) from official sources.
"""

import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okpdtr"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "source-ingestion-probe/0.1 (research; educational project)"}

# Official sources to try
SOURCES = [
    {
        "name": "mintrud_okpdtr",
        "url": "https://mintrud.gov.ru/opendata",
        "type": "html",
    },
    {
        "name": "profstandart_okpdtr",
        "url": "https://profstandart.rosmintrud.ru/obshchiy-informatsionnyy-blok/natsionalnyy-reestr-professionalnykh-standartov/reestr-professionalnykh-standartov/",
        "type": "html",
    },
    {
        "name": "garant_okpdtr",
        "url": "https://base.garant.ru/71166760/",
        "type": "html",
    },
]


def fetch_url(url, timeout=30):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=False, allow_redirects=True)
        return resp
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    print("Probing ОКПДТР sources")
    print("=" * 60)

    for src in SOURCES:
        print(f"\n[{src['name']}] {src['url']}")
        resp = fetch_url(src["url"])
        if resp:
            print(f"  Status: {resp.status_code}")
            print(f"  Content-Type: {resp.headers.get('Content-Type', 'unknown')}")
            print(f"  Size: {len(resp.content)} bytes")

            filename = f"okpdtr_{src['name']}.html"
            filepath = RAW_DIR / filename
            filepath.write_bytes(resp.content)
            print(f"  Saved: {filepath}")
        else:
            print(f"  FAILED")


if __name__ == "__main__":
    main()

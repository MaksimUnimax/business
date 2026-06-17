"""
Probe and download ОКПД 2 (ОК 034-2014) from official sources.
"""

import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "okpd2"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "source-ingestion-probe/0.1 (research; educational project)"}

# Official/legal sources to try
SOURCES = [
    {
        "name": "docs.cntd.ru",
        "url": "https://docs.cntd.ru/document/1200116381",
        "type": "html",
    },
    {
        "name": "construction.ru",
        "url": "https://base.garant.ru/70474890/",
        "type": "html",
    },
    {
        "name": "pravo.gov.ru",
        "url": "http://www.pravo.gov.ru/proxy/ips/?searchres=&npa=631794",
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
    print("Probing ОКПД 2 sources")
    print("=" * 60)

    for src in SOURCES:
        print(f"\n[{src['name']}] {src['url']}")
        resp = fetch_url(src["url"])
        if resp:
            print(f"  Status: {resp.status_code}")
            print(f"  Content-Type: {resp.headers.get('Content-Type', 'unknown')}")
            print(f"  Size: {len(resp.content)} bytes")

            filename = f"okpd2_{src['name']}.html"
            filepath = RAW_DIR / filename
            filepath.write_bytes(resp.content)
            print(f"  Saved: {filepath}")

            # Check for CSV/XML links
            if resp.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "lxml")
                links = soup.find_all("a", href=True)
                data_links = [a for a in links if any(x in a["href"].lower() for x in [".csv", ".xml", ".xls", "okpd"])]
                if data_links:
                    print(f"  Found {len(data_links)} data links")
                    for a in data_links[:5]:
                        print(f"    - {a['href']}")
        else:
            print(f"  FAILED")


if __name__ == "__main__":
    main()

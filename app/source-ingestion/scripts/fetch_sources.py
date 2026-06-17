"""
Main source ingestion script for business direction catalog.
Probes official sources for machine-readable data.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PARSED_DIR = DATA_DIR / "parsed"

HEADERS = {
    "User-Agent": "source-ingestion-probe/0.1 (research; educational project)"
}


def fetch_url(url, timeout=30, verify_ssl=True):
    """Fetch URL with safe headers."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, verify=verify_ssl)
        return resp
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        # Try without SSL verification as fallback
        if verify_ssl:
            print(f"  Retrying without SSL verification...")
            try:
                resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, verify=False)
                return resp
            except Exception as e2:
                print(f"  ERROR retry: {e2}")
        return None


def probe_okved2_rosstat():
    """Probe Rosstat for ОКВЭД 2 data."""
    print("\n=== ОКВЭД 2 (Росстат) ===")
    url = "https://rosstat.gov.ru/folder/11210"
    resp = fetch_url(url)
    if not resp:
        return {"status": "fetch_failed", "source_url": url}

    print(f"  Status: {resp.status_code}")
    print(f"  Content-Type: {resp.headers.get('Content-Type', 'unknown')}")

    soup = BeautifulSoup(resp.text, "lxml")
    links = soup.find_all("a", href=True)
    data_links = [a for a in links if any(ext in a["href"].lower() for ext in [".csv", ".xml", ".xls", ".xlsx", ".json", "okved"])]

    result = {
        "source_id": "okved2_rosstat",
        "status": "partial",
        "access_method": "html",
        "machine_readable": "partial",
        "source_url": url,
        "http_status": resp.status_code,
        "data_links_found": len(data_links),
        "sample_links": [a["href"] for a in data_links[:10]],
        "issues": []
    }

    if not data_links:
        result["issues"].append("No direct CSV/XML/XLS links found on folder page")

    # Save raw HTML
    raw_path = RAW_DIR / "okved"
    raw_path.mkdir(parents=True, exist_ok=True)
    (raw_path / "rosstat_folder.html").write_text(resp.text, encoding="utf-8")

    return result


def probe_okved2_fns():
    """Probe FNS Мой ОКВЭД service."""
    print("\n=== ОКВЭД 2 (ФНС) ===")
    url = "https://service.nalog.ru/okved/"
    resp = fetch_url(url)
    if not resp:
        return {"status": "fetch_failed", "source_url": url}

    print(f"  Status: {resp.status_code}")

    result = {
        "source_id": "okved2_fns",
        "status": "partial",
        "access_method": "html",
        "machine_readable": "no",
        "source_url": url,
        "http_status": resp.status_code,
        "issues": ["Web interface only, no machine-readable export detected"]
    }

    raw_path = RAW_DIR / "okved"
    raw_path.mkdir(parents=True, exist_ok=True)
    (raw_path / "fns_okved.html").write_text(resp.text, encoding="utf-8")

    return result


def probe_profstandarts():
    """Probe Минтруд profstandards open data."""
    print("\n=== Профстандарты (Минтруд) ===")
    url = "https://mintrud.gov.ru/opendata/7710914971-reestr_profstandartov"
    resp = fetch_url(url)
    if not resp:
        return {"status": "fetch_failed", "source_url": url}

    print(f"  Status: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "lxml")
    links = soup.find_all("a", href=True)
    data_links = [a for a in links if any(ext in a["href"].lower() for ext in [".csv", ".xml", ".xls", ".xlsx", ".json"])]

    result = {
        "source_id": "profstandarts_mintrud",
        "status": "partial",
        "access_method": "csv",
        "machine_readable": "yes",
        "source_url": url,
        "http_status": resp.status_code,
        "data_links_found": len(data_links),
        "sample_links": [a["href"] for a in data_links[:10]],
        "issues": []
    }

    if not data_links:
        result["issues"].append("No CSV/XML links found on open data page")

    raw_path = RAW_DIR / "mintrud_profstandards"
    raw_path.mkdir(parents=True, exist_ok=True)
    (raw_path / "opendata_page.html").write_text(resp.text, encoding="utf-8")

    return result


def probe_trudvsem():
    """Probe Trudvsem API."""
    print("\n=== Трудвсем API ===")
    base_url = "https://trudvsem.ru"
    api_url = f"{base_url}/opendata/api"

    # Try to fetch API docs
    resp = fetch_url(api_url)
    if not resp:
        return {"status": "fetch_failed", "source_url": api_url}

    print(f"  API docs status: {resp.status_code}")

    # Try a simple search query
    search_url = f"{base_url}/api/v1/vacancy/search"
    params = {"text": "сборщик мебели", "region": "7400000000000", "size": 5}
    resp2 = fetch_url(f"{search_url}?{'&'.join(f'{k}={v}' for k,v in params.items())}")

    result = {
        "source_id": "trudvsem_api",
        "status": "partial",
        "access_method": "api",
        "machine_readable": "yes",
        "source_url": api_url,
        "search_url": search_url,
        "http_status": resp.status_code,
        "search_status": resp2.status_code if resp2 else "failed",
        "issues": []
    }

    if resp2 and resp2.status_code == 200:
        try:
            data = resp2.json()
            result["sample_keys"] = list(data.keys()) if isinstance(data, dict) else []
            result["sample_count"] = len(data.get("vacancies", data.get("data", []))) if isinstance(data, dict) else 0
        except:
            result["issues"].append("Response not JSON")

    raw_path = RAW_DIR / "trudvsem"
    raw_path.mkdir(parents=True, exist_ok=True)
    (raw_path / "api_docs.html").write_text(resp.text, encoding="utf-8")
    if resp2:
        (raw_path / "search_sample.json").write_text(resp2.text, encoding="utf-8")

    return result


def encode_npd_rules():
    """Encode НПД restrictions from official source."""
    print("\n=== НПД Ограничения ===")

    rules = [
        {
            "rule_id": "npd_001",
            "title": "Лимит дохода 2.4 млн руб/год",
            "hard_stop": True,
            "condition": "Годовой доход не более 2 400 000 руб",
            "allowed_examples": ["Услуги до 2.4 млн/год"],
            "blocked_examples": ["Превышение лимита дохода"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не более 2 400 000 рублей в налоговом периоде",
            "notes": "Ст. 4 422-ФЗ"
        },
        {
            "rule_id": "npd_002",
            "title": "Нельзя нанимать сотрудников по трудовому договору",
            "hard_stop": True,
            "condition": "Нельзя привлекать лиц по трудовым договорам",
            "allowed_examples": ["Работа один", "Подрядчики-ИП"],
            "blocked_examples": ["Наем сотрудников по ТД"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не привлекать лиц по трудовым договорам",
            "notes": "Ст. 4 422-ФЗ"
        },
        {
            "rule_id": "npd_003",
            "title": "Нельзя перепродавать товары (кроме личного)",
            "hard_stop": True,
            "condition": "Нельзя перепродавать товары, кроме имущества личного пользования",
            "allowed_examples": ["Продажа своих услуг", "Продажа б/у личных вещей"],
            "blocked_examples": ["Перепродажа новых товаров", "Торговля оптом"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не заниматься перепродажей товаров",
            "notes": "Ст. 2 422-ФЗ"
        },
        {
            "rule_id": "npd_004",
            "title": "Нельзя продавать подакцизные товары",
            "hard_stop": True,
            "condition": "Запрет на подакцизные товары",
            "allowed_examples": ["Услуги", "Неподакцизная продукция"],
            "blocked_examples": ["Алкоголь", "Табак", "Бензин"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не реализовывать подакцизные товары",
            "notes": "Ст. 2 422-ФЗ"
        },
        {
            "rule_id": "npd_005",
            "title": "Нельзя продавать товары с обязательной маркировкой",
            "hard_stop": True,
            "condition": "Запрет на товары с ЧЗП (кроме собственного производства)",
            "allowed_examples": ["Собственная продукция", "Услуги"],
            "blocked_examples": ["Маркированные товары (одежда, обувь, и т.д.)"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не реализовывать товары, подлежащие обязательной маркировке",
            "notes": "Ст. 2 422-ФЗ, исключение для собственного производства"
        },
        {
            "rule_id": "npd_006",
            "title": "Нельзя извлекать и продавать полезные ископаемые",
            "hard_stop": True,
            "condition": "Запрет на добычу/продажу полезных ископаемых",
            "allowed_examples": ["Услуги", "Переработка"],
            "blocked_examples": ["Добыча песка", "Добыча гравия"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не добывать и не реализовывать полезные ископаемые",
            "notes": "Ст. 2 422-ФЗ"
        },
        {
            "rule_id": "npd_007",
            "title": "Нельзя действовать как агент/комиссионер/поверенный",
            "hard_stop": True,
            "condition": "Запрет на посреднические схемы от имени принципала",
            "allowed_examples": ["Собственные услуги", "Собственное производство"],
            "blocked_examples": ["Продажа от имени другого лица", "Комиссионная торговля"],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "Не реализовывать товары по договору поручения, комиссии или агентскому договору",
            "notes": "Ст. 2 422-ФЗ"
        },
        {
            "rule_id": "npd_008",
            "title": "Ставки НПД 4% (физлица) и 6% (юрлица/ИП)",
            "hard_stop": False,
            "condition": "Ставка налога",
            "allowed_examples": ["4% для физлиц", "6% для ИП/юрлиц"],
            "blocked_examples": [],
            "source_url": "https://npd.nalog.ru/",
            "source_quote_short": "4% для физических лиц, 6% для юридических лиц и ИП",
            "notes": "Ст. 10 422-ФЗ"
        }
    ]

    output_path = PARSED_DIR / "npd_rules_v0.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)

    print(f"  Encoded {len(rules)} NPD rules")
    return {
        "source_id": "npd_nalog",
        "status": "encoded",
        "rules_count": len(rules),
        "source_urls": ["https://npd.nalog.ru/"],
        "issues": []
    }


def probe_social_contract():
    """Probe social contract rules."""
    print("\n=== Соцконтракт ===")

    # Try federal source
    url = "https://mintrud.gov.ru/social/social_contract"
    resp = fetch_url(url)

    result = {
        "source_id": "social_contract",
        "status": "probe_needed",
        "access_method": "html",
        "machine_readable": "no",
        "source_urls": [],
        "issues": []
    }

    if resp and resp.status_code == 200:
        result["source_urls"].append(url)
        result["http_status"] = resp.status_code

        soup = BeautifulSoup(resp.text, "lxml")
        text = soup.get_text()
        if "250 000" in text or "350 000" in text:
            result["amounts_found"] = True

        raw_path = RAW_DIR / "social_contract"
        raw_path.mkdir(parents=True, exist_ok=True)
        (raw_path / "mintrud_page.html").write_text(resp.text, encoding="utf-8")
    else:
        result["issues"].append("Federal page not accessible")

    # Try Chelyabinsk regional
    chel_url = "https://chelobraz.ru/podderzhka-malogo-biznesa/konkursy-i-granty/sotskontrakt/"
    resp2 = fetch_url(chel_url)
    if resp2 and resp2.status_code == 200:
        result["source_urls"].append(chel_url)
        raw_path = RAW_DIR / "social_contract"
        raw_path.mkdir(parents=True, exist_ok=True)
        (raw_path / "chelyabinsk_page.html").write_text(resp2.text, encoding="utf-8")
    else:
        result["issues"].append("Chelyabinsk regional page not accessible")

    return result


def main():
    """Run all source probes."""
    print("Source Ingestion Probe")
    print("=" * 60)
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")

    # Ensure directories exist
    for d in [RAW_DIR, PARSED_DIR, DATA_DIR / "reports"]:
        d.mkdir(parents=True, exist_ok=True)

    results = {}

    # Probe sources
    results["okved2_rosstat"] = probe_okved2_rosstat()
    results["okved2_fns"] = probe_okved2_fns()
    results["profstandarts_mintrud"] = probe_profstandarts()
    results["trudvsem_api"] = probe_trudvsem()
    results["npd_nalog"] = encode_npd_rules()
    results["social_contract"] = probe_social_contract()

    # Save all results
    output_path = DATA_DIR / "ingestion_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Results saved to {output_path}")

    return results


if __name__ == "__main__":
    main()

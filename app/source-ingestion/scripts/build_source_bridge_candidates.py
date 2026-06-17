#!/usr/bin/env python3
"""Rebuild source_bridge_candidates.json with validated OKPD2 and OKZ enrichment."""

import json
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
PARSED_DIR = DATA_DIR / "parsed"
REPORTS_DIR = DATA_DIR / "reports"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path, text):
    with open(path, "w") as f:
        f.write(text)


def keyword_match(name, keywords):
    name_lower = name.lower()
    return any(kw.lower() in name_lower for kw in keywords)


# Keyword buckets per candidate key
KEYWORD_RULES = {
    "furniture_assembly": {
        "okved": ["мебель", "сборка", "установка", "монтаж мебели", "ремонт мебели"],
        "profstandards": ["мебел", "сборщик изделий мебели", "станочник деревообработки"],
        "okpd2": ["мебел", "сборка мебели", "установка мебели"],
        "okz": ["сборщик", "мебельщик", "столяр", "плотник"],
    },
    "cleaning_services": {
        "okved": ["уборка", "чистка", "клининг", "стирка", "химическая чистка"],
        "profstandards": ["уборк", "чистк", "клининг"],
        "okpd2": ["уборка", "чистка", "клининг", "стирка", "химическая чистка"],
        "okz": ["уборщик", " cleaners"],
    },
    "clothing_repair_sewing": {
        "okved": ["одежд", "пошив", "шитье", "швея", "портной", "ремонт одежды", "текстиль"],
        "profstandards": ["швея", "портной", "пошив", "одежд"],
        "okpd2": ["пошив", "шитье", "ремонт одежды", "изготовление одежды"],
        "okz": ["швея", "портной", "закройщик"],
    },
    "shoe_repair": {
        "okved": ["обувь", "ремонт обуви", "обувщик"],
        "profstandards": ["обув", "ремонт обуви"],
        "okpd2": ["обувь", "ремонт обуви", "пошив обуви"],
        "okz": ["обувщик", "ремонтник обуви"],
    },
    "bicycle_repair": {
        "okved": ["велосипед", "ремонт велосипедов"],
        "profstandards": ["велосипед"],
        "okpd2": ["велосипед", "ремонт велосипедов"],
        "okz": ["ремонтник велосипедов", "механик"],
    },
    "appliance_repair": {
        "okved": ["бытовая техника", "электрические приборы", "ремонт приборов", "ремонт электроники"],
        "profstandards": ["ремонт", "обслуживание оборудования"],
        "okpd2": ["ремонт бытовых", "ремонт электроники", "ремонт приборов", "техническое обслуживание"],
        "okz": ["ремонтник", "электрик", "слесарь-ремонтник"],
    },
    "hair_beauty_services": {
        "okved": ["парикмахер", "косметолог", "уход за внешностью", "красота"],
        "profstandards": ["парикмахер", "косметолог", "стилист"],
        "okpd2": ["парикмахер", "косметик", "уход за внешностью", "косметолог"],
        "okz": ["парикмахер", "косметолог", "5141", "5142"],
    },
    "manicure_pedicure": {
        "okved": ["маникюр", "педикюр", "ногтев", "косметическ"],
        "profstandards": ["маникюр", "педикюр"],
        "okpd2": ["маникюр", "педикюр", "ногтев"],
        "okz": ["маникюр", "педикюр"],
    },
    "photography_video": {
        "okved": ["фото", "фотограф", "видеосъемка", "видеограф"],
        "profstandards": ["фотограф", "видеооператор", "оператор"],
        "okpd2": ["фото", "видеосъемка", "фотоуслуги"],
        "okz": ["фотограф", "видеооператор", "оператор"],
    },
    "tutoring_education": {
        "okved": ["обучение", "репетитор", "педагог", "преподаватель", "образование"],
        "profstandards": ["педагог", "преподаватель", "учитель", "обучение"],
        "okpd2": ["обучение", "репетитор", "образовательн"],
        "okz": ["учитель", "преподаватель", "педагог", "репетитор"],
    },
    "animal_care": {
        "okved": ["животн", "уход за животными", "груминг", "дрессировка", "ветеринар"],
        "profstandards": ["ветеринар", "зоотехник", "животн"],
        "okpd2": ["уход за животными", "ветеринар", "груминг", "дрессировка"],
        "okz": ["ветеринар", "зоотехник", "кинолог"],
    },
    "gardening_plants": {
        "okved": ["растен", "сад", "озеленение", "уход за растениями", "садовник", "ландшафт"],
        "profstandards": ["садовник", "озеленение", "ландшафт", "агроном"],
        "okpd2": ["озеленение", "уход за растениями", "ландшафт"],
        "okz": ["садовник", "озеленитель", "агроном"],
    },
    "sharpening_tools": {
        "okved": ["заточка", "инструмент", "ножи", "ремонт инструмента"],
        "profstandards": ["заточник", "инструмент", "слесарь"],
        "okpd2": ["заточка", "ремонт инструмента", "изготовление инструмента"],
        "okz": ["заточник", "инструментальщик"],
    },
}

# NPD legal filter rules (simplified)
NPD_RULES = [
    {"rule_id": "npd_01", "title": "Запрет на торговлю подакцизными товарами", "type": "restriction"},
    {"rule_id": "npd_02", "title": "Запрет на добычу полезных ископаемых", "type": "restriction"},
    {"rule_id": "npd_03", "title": "Запрет на игорный бизнес", "type": "restriction"},
    {"rule_id": "npd_04", "title": "Ограничения по видам деятельности", "type": "restriction"},
    {"rule_id": "npd_05", "title": "Запрет на производство алкоголя", "type": "restriction"},
    {"rule_id": "npd_06", "title": "Запрет на производство табачных изделий", "type": "restriction"},
    {"rule_id": "npd_07", "title": "Ограничения по численности работников", "type": "restriction"},
    {"rule_id": "npd_08", "title": "Ограничения по доходу", "type": "restriction"},
]


def match_source_rows(rows, keywords, source_id, source_role, source_status, max_matches=20):
    matches = []
    for row in rows:
        if len(matches) >= max_matches:
            break
        name = row.get("name") or row.get("title", "")
        code = row.get("code", "")
        if keyword_match(name, keywords):
            confidence = "high" if any(kw.lower() in name.lower() for kw in keywords if len(kw) > 4) else "medium"
            matches.append({
                "source_id": source_id,
                "source_role": source_role,
                "source_status": source_status,
                "code": code,
                "title": name[:120],
                "match_reason": f"keyword match: {[kw for kw in keywords if kw.lower() in name.lower()][:3]}",
                "match_type": "keyword",
                "confidence": confidence,
            })
    return matches


def build_bridge():
    # Load sources
    okved2 = load_json(PARSED_DIR / "okved2_service_candidates.json")
    profstandards = load_json(PARSED_DIR / "profstandards_service_candidates.json")
    okpd2 = load_json(PARSED_DIR / "okpd2_service_work_candidates.json")
    okz = load_json(PARSED_DIR / "okz_service_occupation_candidates.json")

    # Load semantic validation
    sv = load_json(PARSED_DIR / "classifier_semantic_validation.json")
    use_okpd2 = sv["bridge_decision"]["use_okpd2_in_next_bridge"]
    use_okz = sv["bridge_decision"]["use_okz_in_next_bridge"]

    assert use_okpd2, "OKPD2 not allowed in bridge"
    assert use_okz, "OKZ not allowed in bridge"

    bridge = []

    for key, rules in KEYWORD_RULES.items():
        okved_matches = match_source_rows(okved2, rules["okved"], "okved2_rosstat", "primary", "official_download")
        prof_matches = match_source_rows(profstandards, rules["profstandards"], "profstandarts_mintrud", "primary", "official_download")
        okpd2_matches = match_source_rows(okpd2, rules["okpd2"], "okpd2_mirror", "enrichment", "mirror_unofficial")
        okz_matches = match_source_rows(okz, rules["okz"], "okz_mirror", "enrichment", "mirror_unofficial")

        # Determine confidence
        total_matches = len(okved_matches) + len(prof_matches) + len(okpd2_matches) + len(okz_matches)
        has_primary = len(okved_matches) > 0 or len(prof_matches) > 0
        has_enrichment = len(okpd2_matches) > 0 or len(okz_matches) > 0

        if has_primary and total_matches >= 3:
            confidence = "high"
        elif has_primary or total_matches >= 2:
            confidence = "medium"
        else:
            confidence = "low"

        # Label mapping
        label_map = {
            "furniture_assembly": "Сборка и ремонт мебели",
            "cleaning_services": "Клининговые и уборочные услуги",
            "clothing_repair_sewing": "Ремонт и пошив одежды",
            "shoe_repair": "Ремонт обуви",
            "bicycle_repair": "Ремонт велосипедов",
            "appliance_repair": "Ремонт бытовой техники и электроники",
            "hair_beauty_services": "Парикмахерские и косметические услуги",
            "manicure_pedicure": "Маникюр и педикюр",
            "photography_video": "Фото- и видеосъёмка",
            "tutoring_education": "Репетиторство и обучение",
            "animal_care": "Уход за животными",
            "gardening_plants": "Садоводство и озеленение",
            "sharpening_tools": "Заточка инструментов",
        }

        row = {
            "candidate_key": key,
            "label_ru": label_map.get(key, key),
            "human_review_required": True,
            "source_status": "bridge_candidate_not_final",
            "confidence": confidence,
            "okved_matches": okved_matches,
            "profstandard_matches": prof_matches,
            "okpd2_matches": okpd2_matches,
            "okz_matches": okz_matches,
            "npd_rules": NPD_RULES,
            "blocked_sources_not_used": sv["bridge_decision"]["blocked_sources"],
            "missing_sources": ["okpdtr_all", "etks_mintrud"],
            "notes": [
                f"OKPD2 enrichment: {len(okpd2_matches)} matches",
                f"OKZ enrichment: {len(okz_matches)} matches",
                "All rows require human review",
                "This is NOT final catalog",
            ],
        }
        bridge.append(row)

    # Save bridge
    save_json(PARSED_DIR / "source_bridge_candidates.json", bridge)

    # Generate report
    report = generate_report(bridge, sv)
    save_text(REPORTS_DIR / "source_bridge_report.md", report)

    # Compute checksum
    with open(PARSED_DIR / "source_bridge_candidates.json", "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()

    print(f"Bridge rebuilt: {len(bridge)} candidates")
    print(f"Checksum: {checksum}")
    return bridge, checksum


def generate_report(bridge, sv):
    lines = [
        "# Source Bridge Report",
        "",
        "## Run Mode",
        "rebuild_source_bridge_with_okpd2_okz_push",
        "",
        "## Source Layers Used",
        "- OKVED2 Rosstat (primary): 981 service candidates",
        "- Profstandards Mintrud (primary): 519 service candidates",
        "- NPD legal hard filters (legal_filter): 8 rules",
        "- OKPD2 mirror (enrichment, validated): 7173 service/work candidates",
        "- OKZ mirror (enrichment, validated): 188 occupation candidates",
        "",
        "## Blocked Source Layers",
        "- OKPD2 official (no machine-readable parsed source)",
        "- OKZ official (no machine-readable parsed source)",
        "- OKPDTR (parsed_rows = 0, manual_download_required)",
        "- Trudvsem (blocked by QRATOR)",
        "- Social contract (not parsed)",
        "- ETKS (not parsed)",
        "",
        "## Bridge Candidate Count",
        f"Total: {len(bridge)}",
        "",
        "## Per Candidate Summary",
        "",
    ]

    for row in bridge:
        key = row["candidate_key"]
        okved = len(row["okved_matches"])
        prof = len(row["profstandard_matches"])
        okpd2 = len(row["okpd2_matches"])
        okz = len(row["okz_matches"])
        conf = row["confidence"]
        lines.append(f"### {key}")
        lines.append(f"- OKVED2 matches: {okved}")
        lines.append(f"- Profstandard matches: {prof}")
        lines.append(f"- OKPD2 enrichment matches: {okpd2}")
        lines.append(f"- OKZ enrichment matches: {okz}")
        lines.append(f"- Confidence: {conf}")
        lines.append(f"- Human review required: yes")
        lines.append("")

    lines.extend([
        "## Limitations",
        "- Bridge is NOT final catalog",
        "- All rows require human review",
        "- OKPD2 and OKZ are mirror_unofficial enrichment, not official primary",
        "- No LLM or external APIs used in matching",
        "- Deterministic keyword matching only",
        "",
        "## Next Step",
        "Human review of bridge candidates, then optionally business_direction_catalog_schema_v0",
        "",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    build_bridge()

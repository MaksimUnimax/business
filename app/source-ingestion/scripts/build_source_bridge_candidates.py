"""
Build source bridge candidates from parsed data.
Links sources by text similarity/keyword matching.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PARSED_DIR = PROJECT_ROOT / "data" / "parsed"

# Bridge candidate keys with keywords
BRIDGE_KEYS = {
    "furniture_assembly": ["мебел", "сборщик мебели", "assembly"],
    "cleaning_services": ["уборк", "клининг", "чистк", "cleaning"],
    "clothing_repair_sewing": ["пошив", "одежд", "ремонт одежды", "sewing"],
    "shoe_repair": ["обув", "ремонт обуви", "shoe"],
    "bicycle_repair": ["велосип", "веломеханик", "bicycle"],
    "appliance_repair": ["бытов", "техник", "ремонт техники", "appliance"],
    "hair_beauty_services": ["парикмах", "космет", "hair", "beauty"],
    "manicure_pedicure": ["маникюр", "педикюр", "manicure"],
    "photography_video": ["фото", "видео", "photography"],
    "tutoring_education": ["обучен", "образован", "педагог", "tutoring"],
    "animal_care": ["животн", "уход", "animal"],
    "gardening_plants": ["садов", "растен", "gardening"],
    "sharpening_tools": ["заточ", "инструмент", "sharpening"],
}


def load_candidates(filename):
    path = PARSED_DIR / filename
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


def match_to_bridge(items, bridge_key, keywords):
    """Match items to bridge candidate by keywords."""
    matches = []
    for item in items:
        text = " ".join(str(v) for v in item.values()).lower()
        if any(kw in text for kw in keywords):
            matches.append(item)
    return matches


def main():
    print("Building source bridge candidates")

    # Load all candidate files
    okved_candidates = load_candidates("okved2_service_candidates.json")
    profstandards_candidates = load_candidates("profstandards_service_candidates.json")
    okpd2_candidates = load_candidates("okpd2_service_work_candidates.json")
    okpdtr_candidates = load_candidates("okpdtr_profession_candidates.json")
    okz_candidates = load_candidates("okz_service_occupation_candidates.json")

    print(f"Loaded candidates:")
    print(f"  ОКВЭД 2: {len(okved_candidates)}")
    print(f"  Профстандарты: {len(profstandards_candidates)}")
    print(f"  ОКПД 2: {len(okpd2_candidates)}")
    print(f"  ОКПДТР: {len(okpdtr_candidates)}")
    print(f"  ОКЗ: {len(okz_candidates)}")

    # Build bridge candidates
    bridges = []
    for key, keywords in BRIDGE_KEYS.items():
        bridge = {
            "candidate_key": key,
            "okved_matches": match_to_bridge(okved_candidates, key, keywords),
            "okpd2_matches": match_to_bridge(okpd2_candidates, key, keywords),
            "okpdtr_matches": match_to_bridge(okpdtr_candidates, key, keywords),
            "okz_matches": match_to_bridge(okz_candidates, key, keywords),
            "profstandard_matches": match_to_bridge(profstandards_candidates, key, keywords),
            "confidence": "low",
            "human_review_required": True,
            "notes": [],
        }

        # Calculate confidence
        total_matches = (
            len(bridge["okved_matches"])
            + len(bridge["okpd2_matches"])
            + len(bridge["okpdtr_matches"])
            + len(bridge["okz_matches"])
            + len(bridge["profstandard_matches"])
        )

        if total_matches >= 5:
            bridge["confidence"] = "high"
        elif total_matches >= 2:
            bridge["confidence"] = "medium"
        else:
            bridge["confidence"] = "low"

        bridges.append(bridge)

    # Save bridge candidates
    output = PARSED_DIR / "source_bridge_candidates.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(bridges, f, ensure_ascii=False, indent=2)
    print(f"Saved: {output}")

    # Print summary
    print("\nBridge summary:")
    for b in bridges:
        total = (
            len(b["okved_matches"])
            + len(b["okpd2_matches"])
            + len(b["okpdtr_matches"])
            + len(b["okz_matches"])
            + len(b["profstandard_matches"])
        )
        print(f"  {b['candidate_key']}: {total} matches ({b['confidence']})")


if __name__ == "__main__":
    main()

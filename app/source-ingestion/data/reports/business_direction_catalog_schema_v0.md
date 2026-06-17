# Business Direction Catalog Schema v0

## Run Mode
business_direction_catalog_schema_v0_push

## Review Totals Reconciliation
- JSON candidate count: 13
- JSON accepted: 10
- JSON needs_more: 3
- JSON rejected: 0
- JSON accepted matches: 218
- JSON rejected matches: 23
- JSON needs_more matches: 281
- Markdown report discrepancy: none — markdown matches JSON

## Schema
- File: `business_direction_catalog_schema_v0.json`
- Schema version: 0.1.0
- Required sections: 14 (identity, source, NPD, social contract, person-fit, training, market, procurement, ads, questionnaire, scoring, review)

## Draft Catalog
- File: `business_direction_catalog_draft_v0.json`
- Draft record count: 10

### Included Candidates
- `furniture_assembly` (Сборка и ремонт мебели)
- `cleaning_services` (Клининговые и уборочные услуги)
- `clothing_repair_sewing` (Ремонт и пошив одежды)
- `shoe_repair` (Ремонт обуви)
- `appliance_repair` (Ремонт бытовой техники и электроники)
- `hair_beauty_services` (Парикмахерские и косметические услуги)
- `manicure_pedicure` (Маникюр и педикюр)
- `tutoring_education` (Репетиторство и обучение)
- `animal_care` (Уход за животными)
- `gardening_plants` (Садоводство и озеленение)

### Excluded Candidates (needs more source)
- `bicycle_repair` (Ремонт велосипедов)
- `photography_video` (Фото- и видеосъёмка)
- `sharpening_tools` (Заточка инструментов)

## Limitations
- This is NOT final catalog.
- This is NOT user recommendation.
- Market/procurement/ads/unit economics are placeholders (missing_data).
- NPD applicability requires legal review.
- Social contract fit requires regional rule check.
- Person-fit gates require validation.
- Training requirements require validation.
- All records have human_review_required = true.

## Next Step
catalog_schema_human_review_and_questionnaire_mapping_v0

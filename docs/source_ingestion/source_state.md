# Source Ingestion State

This is the current source-ingestion state, copied from `app/source-ingestion/` files as of v4.1 (2026-06-17).

Canonical data lives in `app/source-ingestion/data/parsed/source_quality_matrix.json`.

## Completed Milestones

1. Source download and parsing (v4) — completed
2. Semantic validation v4.1 — completed
3. Source bridge rebuild with validated OKPD2/OKZ — completed
4. Human review of bridge candidates — completed
5. Business direction catalog schema v0 — completed

## Source Bridge Human Review — COMPLETED

All 13 bridge candidates reviewed. 10 accepted for catalog schema, 3 need more source.

## Business Direction Catalog Schema v0 — COMPLETED

- Schema JSON: `business_direction_catalog_schema_v0.json` (14 sections, JSON Schema draft-07)
- Draft catalog: `business_direction_catalog_draft_v0.json` (10 draft records)
- Only accepted bridge candidates included
- All records: `human_review_required: true`, `not_final_catalog: true`, `not_user_recommendation: true`
- Market/procurement/ads/unit economics are placeholders (missing_data)

## Source Status Table

| Source | Role | Status | Parsed Rows | Used in Bridge? | Notes |
|--------|------|--------|-------------|-----------------|-------|
| ОКВЭД 2 (Росстат) | primary | primary | 3034 | yes | Official classifier |
| Реестр профстандартов (Минтруд) | primary | primary | 949 | yes | Official open data |
| НПД ограничения (ФНС) | primary (legal) | primary | 8 | yes | 8 legal hard-filter rules |
| ОКПД 2 (mirror) | enrichment | enrichment | 20387 | yes | Semantic validation passed |
| ОКЗ-2014 (mirror) | enrichment | enrichment | 608 | yes | Semantic validation passed |
| ОКПДТР | manual_download_required | blocked | 0 | no | All sources failed |
| ЕТКС | not_probed | not_probed | 0 | no | Not yet probed |
| Трудвсем | blocked | blocked | 0 | no | QRATOR blocks API |
| Соцконтракт | blocked | blocked | 0 | no | Pages unreachable |

## Next Step

`catalog_schema_human_review_and_questionnaire_mapping_v0`

Review schema structure, validate draft records, map questionnaire fields, fill person-fit gates.

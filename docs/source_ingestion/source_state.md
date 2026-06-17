# Source Ingestion State

This is the current source-ingestion state, copied from `app/source-ingestion/` files as of v4.1 (2026-06-17).

Canonical data lives in `app/source-ingestion/data/parsed/source_quality_matrix.json`.

## Completed Milestones

1. Source download and parsing (v4) — completed
2. Semantic validation v4.1 — completed
3. Source bridge rebuild with validated OKPD2/OKZ — completed
4. Human review of bridge candidates — completed

## Semantic Validation (v4.1) — COMPLETED

Both OKPD2 and OKZ have been semantically validated and are used in the source bridge:

- **OKPD2**: `valid_mirror_enrichment` — 373 expected service/product patterns found. Used as enrichment in bridge.
- **OKZ**: `valid_mirror_enrichment` — 269 occupation rows found. Used as enrichment in bridge.
- **Cross-contamination**: None detected.

## Source Bridge Human Review — COMPLETED

All 13 bridge candidates have been reviewed with deterministic heuristics:

- **Accepted for catalog schema**: 10 candidates
- **Needs more source before catalog**: 3 candidates (bicycle_repair, photography_video, sharpening_tools)
- **Rejected for now**: 0 candidates

Review file: `app/source-ingestion/data/parsed/source_bridge_review.json`
Review report: `app/source-ingestion/data/reports/source_bridge_human_review.md`

## Source Status Table

| Source | Role | Status | Parsed Rows | Candidate Rows | Provenance | Used in Bridge? | Notes |
|--------|------|--------|-------------|----------------|------------|-----------------|-------|
| ОКВЭД 2 (Росстат) | primary | primary | 3034 | 981 service candidates | official CSV download | yes | Official classifier, primary source layer |
| Реестр профстандартов (Минтруд) | primary | primary | 949 | 519 service candidates | official CSV download | yes | Official open data portal, primary source layer |
| НПД ограничения (ФНС) | primary (legal filters) | primary | 8 (8 rules) | 8 legal hard-filter rules | manually encoded from official source | yes | Legal hard filters attached to all bridge candidates |
| ОКПД 2 (classifikators.ru mirror) | enrichment | enrichment | 20387 | 7173 service/work candidates | mirror xlsx from classifikators.ru | yes (enrichment) | Semantic validation v4.1 passed; mirror_unofficial |
| ОКЗ-2014 (classifikators.ru mirror) | enrichment | enrichment | 608 | 188 occupation candidates | mirror xlsx from classifikators.ru | yes (enrichment) | Semantic validation v4.1 passed; mirror_unofficial |
| ОКВЭД 2 (ФНС) | validation | validation | 0 | 0 | official HTML only | no | Web interface only |
| ОКПД 2 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКЗ-2014 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКПДТР (ОК 016-2025) | manual download required | manual_download_required | 0 | 0 | no structured file available | no | All accessible sources failed |
| ЕТКС (Минтруд) | next probe | not_probed | 0 | 0 | not yet probed | no | Not yet probed |
| Трудвсем API (Работа России) | blocked | blocked | 0 | 0 | QRATOR anti-bot blocks API | no | Server blocks API requests |
| Соцконтракт | blocked | blocked | 0 | 0 | federal/regional pages timeout | no | Pages unreachable from this server |

## Source Bridge Status

Source bridge has been **rebuilt** and **human-reviewed**.

- **Bridge candidates**: 13
- **All rows**: `human_review_required: true`
- **Bridge is NOT final business catalog**
- **Accepted for catalog schema**: 10 candidates
- **Needs more source**: 3 candidates

## Next Step

`business_direction_catalog_schema_v0`

10 candidates are accepted for catalog schema design. 3 candidates need additional source data.

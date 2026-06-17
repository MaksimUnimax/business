# Source Ingestion State

This is the current source-ingestion state, copied from `app/source-ingestion/` files as of v4.1 (2026-06-17).

Canonical data lives in `app/source-ingestion/data/parsed/source_quality_matrix.json`.

## Completed Milestones

1. Source download and parsing (v4) — completed
2. Semantic validation v4.1 — completed
3. Source bridge rebuild with validated OKPD2/OKZ — completed

## Semantic Validation (v4.1) — COMPLETED

Both OKPD2 and OKZ have been semantically validated and are used in the source bridge:

- **OKPD2**: `valid_mirror_enrichment` — 373 expected service/product patterns found (95.11, 95.2, 96.01, 96.02). Used as enrichment in bridge.
- **OKZ**: `valid_mirror_enrichment` — 269 occupation rows found, code 5141 (Парикмахеры) confirmed present. Used as enrichment in bridge.
- **Cross-contamination**: None detected. No code or name overlap between OKPD2 and OKZ.

## Source Status Table

| Source | Role | Status | Parsed Rows | Candidate Rows | Provenance | Used in Bridge? | Notes |
|--------|------|--------|-------------|----------------|------------|-----------------|-------|
| ОКВЭД 2 (Росстат) | primary | primary | 3034 | 981 service candidates | official CSV download | yes | Official classifier, primary source layer |
| Реестр профстандартов (Минтруд) | primary | primary | 949 | 519 service candidates | official CSV download | yes | Official open data portal, primary source layer |
| НПД ограничения (ФНС) | primary (legal filters) | primary | 8 (8 rules) | 8 legal hard-filter rules | manually encoded from official source | yes | Legal hard filters attached to all bridge candidates |
| ОКПД 2 (classifikators.ru mirror) | enrichment | enrichment | 20387 | 7173 service/work candidates | mirror xlsx from classifikators.ru | yes (enrichment) | Semantic validation v4.1 passed; mirror_unofficial |
| ОКЗ-2014 (classifikators.ru mirror) | enrichment | enrichment | 608 | 188 occupation candidates | mirror xlsx from classifikators.ru | yes (enrichment) | Semantic validation v4.1 passed; mirror_unofficial |
| ОКВЭД 2 (ФНС) | validation | validation | 0 | 0 | official HTML only | no | Web interface only, no machine-readable data |
| ОКПД 2 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКЗ-2014 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКПДТР (ОК 016-2025) | manual download required | manual_download_required | 0 | 0 | no structured file available | no | All accessible sources failed (see errors) |
| ЕТКС (Минтруд) | next probe | not_probed | 0 | 0 | not yet probed | no | Not yet probed |
| Трудвсем API (Работа России) | blocked | blocked | 0 | 0 | QRATOR anti-bot blocks API | no | Server blocks API requests |
| Соцконтракт | blocked | blocked | 0 | 0 | federal/regional pages timeout | no | Pages unreachable from this server |

## Source Bridge Status

Source bridge has been **rebuilt** with validated OKPD2 and OKZ enrichment layers.

- **Bridge candidates**: 13
- **All rows**: `human_review_required: true`
- **Bridge is NOT final business catalog**
- **All rows are `bridge_candidate_not_final` status**

## Next Step

`human_review_of_bridge_candidates`

Review each of 13 bridge candidate keys. Mark source matches as accept/reject/needs_more_source.

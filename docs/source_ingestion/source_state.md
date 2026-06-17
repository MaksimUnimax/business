# Source Ingestion State

This is the current source-ingestion state, copied from `app/source-ingestion/` files as of v4.1 (2026-06-17).

Canonical data lives in `app/source-ingestion/data/parsed/source_quality_matrix.json`.

## Semantic Validation (v4.1)

Both OKPD2 and OKZ have been semantically validated before bridge rebuild:

- **OKPD2**: `valid_mirror_enrichment` — 373 expected service/product patterns found (95.11, 95.2, 96.01, 96.02). Safe for enrichment use.
- **OKZ**: `valid_mirror_enrichment` — 269 occupation rows found, code 5141 (Парикмахеры) confirmed present. The original concern about 9602/9603 contamination was refuted — these codes only exist in OKPD2, not in OKZ.
- **Cross-contamination**: None detected. No code or name overlap between OKPD2 and OKZ.
- **Bridge decision**: Both OKPD2 and OKZ are allowed in next bridge rebuild.

## Source Status Table

| Source | Role | Status | Parsed Rows | Candidate Rows | Provenance | Can Be Used in Bridge Now? | Notes |
|--------|------|--------|-------------|----------------|------------|---------------------------|-------|
| ОКВЭД 2 (Росстат) | primary | primary | 3034 | 981 service candidates | official CSV download | yes | Official classifier, fully parsed |
| Реестр профстандартов (Минтруд) | primary | primary | 949 | 519 service candidates | official CSV download | yes | Official open data portal |
| НПД ограничения (ФНС) | primary (legal filters) | primary | 8 (8 rules) | 8 legal hard-filter rules | manually encoded from official source | yes | Rules manually encoded from npd.nalog.ru |
| ОКПД 2 (classifikators.ru mirror) | enrichment | enrichment | 20387 | 7173 service/work candidates | mirror xlsx from classifikators.ru | yes (enrichment only) | Semantic validation v4.1 passed |
| ОКЗ-2014 (classifikators.ru mirror) | enrichment | enrichment | 608 | 188 occupation candidates | mirror xlsx from classifikators.ru | yes (enrichment only) | Semantic validation v4.1 passed; 9602/9603 concern refuted |
| ОКВЭД 2 (ФНС) | validation | validation | 0 | 0 | official HTML only | no | Web interface only, no machine-readable data |
| ОКПД 2 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКЗ-2014 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКПДТР (ОК 016-2025) | manual download required | manual_download_required | 0 | 0 | no structured file available | no | All accessible sources failed (see errors) |
| ЕТКС (Минтруд) | next probe | not_probed | 0 | 0 | not yet probed | no | Not yet probed |
| Трудвсем API (Работа России) | blocked | blocked | 0 | 0 | QRATOR anti-bot blocks API | no | Server blocks API requests |
| Соцконтракт | blocked | blocked | 0 | 0 | federal/regional pages timeout | no | Pages unreachable from this server |

## Source Bridge Status

The existing source bridge has 13 candidates but was **not rebuilt** with OKPD2/OKZ v4 data. The bridge is not the final catalog.

## Next Technical Step

`rebuild_source_bridge_with_okpd2_and_okz`

Semantic validation v4.1 completed. OKPD2 and OKZ are validated and allowed for next bridge rebuild. The bridge should be rebuilt including OKPD2 enrichment and OKZ occupation data.

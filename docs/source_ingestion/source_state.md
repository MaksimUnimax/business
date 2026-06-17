# Source Ingestion State

This is the current source-ingestion state, copied from `app/source-ingestion/` files as of v4 (2026-06-17).

Canonical data lives in `app/source-ingestion/data/parsed/source_quality_matrix.json`.

## Source Status Table

| Source | Role | Status | Parsed Rows | Candidate Rows | Provenance | Can Be Used in Bridge Now? | Notes |
|--------|------|--------|-------------|----------------|------------|---------------------------|-------|
| ОКВЭД 2 (Росстат) | primary | primary | 3034 | 981 service candidates | official CSV download | yes | Official classifier, fully parsed |
| Реестр профстандартов (Минтруд) | primary | primary | 949 | 519 service candidates | official CSV download | yes | Official open data portal |
| НПД ограничения (ФНС) | primary (legal filters) | primary | 8 (8 rules) | 8 legal hard-filter rules | manually encoded from official source | yes | Rules manually encoded from npd.nalog.ru |
| ОКПД 2 (classifikators.ru mirror) | enrichment | enrichment | 20387 | 7173 service/work candidates | mirror xlsx from classifikators.ru | yes (enrichment only) | Unofficial mirror; NOT official primary source |
| ОКЗ-2014 (classifikators.ru mirror) | enrichment candidate | enrichment | 608 | 188 occupation candidates | mirror xlsx from classifikators.ru | **NO** — semantic validation required | Suspicious service-like rows detected; see warnings below |
| ОКВЭД 2 (ФНС) | validation | validation | 0 | 0 | official HTML only | no | Web interface only, no machine-readable data |
| ОКПД 2 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКЗ-2014 (official) | blocked | blocked | 0 | 0 | official source has no download | no | No machine-readable download available |
| ОКПДТР (ОК 016-2025) | manual download required | manual_download_required | 0 | 0 | no structured file available | no | All accessible sources failed (see errors) |
| ЕТКС (Минтруд) | next probe | not_probed | 0 | 0 | not yet probed | no | Not yet probed |
| Трудвсем API (Работа России) | blocked | blocked | 0 | 0 | QRATOR anti-bot blocks API | no | Server blocks API requests |
| Соцконтракт | blocked | blocked | 0 | 0 | federal/regional pages timeout | no | Pages unreachable from this server |

## Known Data-Quality Warnings

### OKZ: Suspicious Service-Like Rows

The OKZ mirror (classifikators.ru) parsed 608 rows with 188 occupation candidates. However, sample inspection revealed **suspicious service-like rows** that appear to be service descriptions rather than proper occupation entries:

- `9602 Парикмахерские и аналогичные услуги` (hairdressing and similar services)
- `9603 Услуги по уходу за животными` (animal care services)

These entries suggest contamination of the OKZ data with service-oriented classifications. **OKZ must NOT be used in source_bridge until semantic validation is completed.**

### OKPD2: Mirror Source

OKPD2 was parsed from `classifikators.ru` mirror XLSX. This is an unofficial mirror, not an official government source. OKPD2 can be used for enrichment only, not as a primary official source.

### Source Bridge Status

The existing source bridge has 13 candidates but was **not rebuilt** with OKPD2/OKZ v4 data. The bridge is not the final catalog.

## Next Technical Step

`classifier_semantic_validation_v4_1`

This step will validate OKPD2 and OKZ semantics, detect contamination, and decide whether the next bridge should include or exclude OKZ.

# Source Map (v4.1)

## Correction Note
Previous v3 decision said OKPD2/OKPDTR/OKZ parsed, but parsed_rows were 0.
Corrected status: OKPD2/OKPDTR/OKZ not parsed until v4 produces rows.

## Semantic Validation (v4.1)

OKPD2 and OKZ have been semantically validated:

- **OKPD2**: valid_mirror_enrichment — 373 expected service/product patterns found. Safe for enrichment.
- **OKZ**: valid_mirror_enrichment — 269 occupation rows found, code 5141 (Парикмахеры) confirmed. Original 9602/9603 concern refuted (these codes only exist in OKPD2).
- **Cross-contamination**: None. No code or name overlap between OKPD2 and OKZ.

## Source Status

| Source | Status | Parsed Rows | Recommended Use | Source Status | Reason |
|--------|--------|-------------|-----------------|---------------|--------|
| ОКВЭД 2 (Росстат) | primary | 3034 | primary | official_download | Official CSV parsed |
| ОКВЭД 2 (ФНС) | validation | 0 | validation | official_html | Web interface only |
| ОКПД 2 (classifikators.ru) | enrichment | 20387 | enrichment | mirror_unofficial | Mirror xlsx parsed |
| ОКПД 2 (official) | blocked | 0 | blocked | blocked | No machine-readable download |
| ОКПДТР (ОК 016-2025) | manual_download_required | 0 | manual_download_required | manual_download_required | No structured file available |
| ОКЗ-2014 (classifikators.ru) | enrichment | 608 | enrichment | mirror_unofficial | Mirror xlsx parsed |
| ОКЗ-2014 (official) | blocked | 0 | blocked | blocked | No machine-readable download |
| Реестр профстандартов | primary | 949 | primary | official_download | Official CSV parsed |
| ЕТКС (Минтруд) | not_probed | 0 | next_probe | not_probed | Not yet probed |
| Трудвсем API | blocked | 0 | blocked | blocked | QRATOR anti-bot blocks API |
| НПД ограничения | primary | 8 | primary | official | 8 rules manually encoded |
| Соцконтракт | blocked | 0 | blocked | blocked | Federal/regional pages timeout |

## Summary

- Primary sources: 3 (ОКВЭД 2, Профстандарты, НПД)
- Enrichment sources: 2 (ОКПД 2 mirror, ОКЗ mirror)
- Blocked: 4 (ОКПД official, Трудвсем, Соцконтракт, ОКПДТР manual)
- Manual download required: 1 (ОКПДТР)
- Next probe: 1 (ЕТКС)
- Validation: 1 (ОКВЭД 2 ФНС)

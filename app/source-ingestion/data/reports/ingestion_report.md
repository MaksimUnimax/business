# Source Ingestion Report v4

## Run Mode
classifier_download_parse_v4

## Correction Note
Previous v3 decision said OKPD2 parsed, but parsed_rows were 0.
Previous v3 decision said OKPDTR parsed, but parsed_rows were 0.
Previous v3 decision said OKZ parsed, but parsed_rows were 0.
Corrected status: OKPD2/OKPDTR/OKZ not parsed until v4 produces rows.

## Summary

Fourth run successfully parsed ОКПД 2 and ОКЗ from classifikators.ru mirror (unofficial).
ОКПДТР remains unavailable as structured file from any accessible source.

## Source Results

### ОКПД 2 (ОК 034-2014)
- **Status**: enrichment (mirror_unofficial)
- **Source URLs tried**:
  - https://classifikators.ru/okpd (mirror, xlsx available)
  - https://classifikators.ru/assets/downloads/okpd/okpd.xlsx (downloaded)
  - https://www.consultant.ru/document/cons_doc_LAW_163753/ (no download)
  - https://base.garant.ru/10900200/ (no download)
  - https://www.pravo.gov.ru/ (404)
- **Access method**: xlsx download from classifikators.ru mirror
- **Download status**: success (685KB xlsx)
- **Source file**: okpd_classifikators.xlsx
- **Source status**: mirror_unofficial (classifikators.ru is not official)
- **Parsed rows**: 20387
- **Fields detected**: code, name, parent_code, level, source_url, source_status, source_file, candidate_type
- **Service/work candidates**: 7173
- **Sample candidates**:
  - 95.11.10.100: Ремонт и техническое обслуживание бытовых компьютеров
  - 95.11.20.100: Ремонт и техническое обслуживание бытовых радиоэлектронной аппаратуры
  - 95.12.00.000: Ремонт и техническое обслуживание бытовой электроники
  - 95.21.10.000: Ремонт бытовых электрических приборов
  - 96.01.11.000: Стирка и химическая чистка текстильных и меховых изделий

### ОКПДТР (ОК 016-2025)
- **Status**: manual_download_required
- **Classifier version**: ok_016_2025 (attempted)
- **Source URLs tried**:
  - https://classifikators.ru/okpdtr (404)
  - https://classifikators.ru/okpdtr-2025 (404)
  - https://www.consultant.ru/document/cons_doc_LAW_358468/ (no download, legal text only)
  - https://base.garant.ru/71166736/ (no download, legal text only)
  - http://www.vniot.ru/files/normativka/okpdtr/ (DNS fail - host unreachable)
  - https://vcot.ru/okpdtr (connection refused)
  - https://profstandart.rosmintrud.ru/ (timeout)
  - GitHub search: no structured files found
- **Access method**: HTML/legal text only
- **Download status**: failure (no machine-readable file available)
- **Source status**: manual_download_required
- **Parsed rows**: 0
- **Issue**: OKPDTR-2025 structured files (xlsx/xls/csv) are not available from any server-accessible source. The classifier is only published as legal text. Manual download from profstandart.rosmintrud.ru or vniot.ru required.

### ОКЗ (ОК 010-2014)
- **Status**: enrichment (mirror_unofficial)
- **Source URLs tried**:
  - https://classifikators.ru/okz (mirror, xlsx available)
  - https://classifikators.ru/assets/downloads/okz/okz.xlsx (downloaded)
  - https://mintrud.gov.ru/ (no download)
  - http://www.vniot.ru/files/normativka/okz/ (DNS fail)
  - https://vcot.ru/okz (connection refused)
- **Access method**: xlsx download from classifikators.ru mirror
- **Download status**: success (34KB xlsx)
- **Source file**: okz_classifikators.xlsx
- **Source status**: mirror_unofficial (classifikators.ru is not official)
- **Parsed rows**: 608
- **Fields detected**: code, title, parent_code, group_level, source_url, source_status, source_file, candidate_type
- **Occupation candidates**: 188
- **Sample candidates**:
  - 74: Работники, занятые в области искусства
  - 741: Дизайнеры
  - 7411: Графические дизайнеры
  - 7412: Дизайнеры интерьеров
  - 7413: Дизайнеры промышленные

### Source Bridge Candidates
- **Bridge candidates count**: will be updated after bridge rebuild
- **All human_review_required**: yes
- **Issues**: Bridge not rebuilt in v4 (task scope is source download/parse only)

## Quality Matrix Summary

| Source | Status | Parsed Rows | Source Status | Use |
|--------|--------|-------------|---------------|-----|
| ОКВЭД 2 (Росстат) | primary | 3034 | official_download | primary |
| ОКВЭД 2 (ФНС) | validation | 0 | official_html | validation |
| ОКПД 2 (mirror) | enrichment | 20387 | mirror_unofficial | enrichment |
| ОКПД 2 (official) | blocked | 0 | blocked | blocked |
| ОКПДТР | manual_download_required | 0 | manual_download_required | manual_download_required |
| ОКЗ (mirror) | enrichment | 608 | mirror_unofficial | enrichment |
| ОКЗ (official) | blocked | 0 | blocked | blocked |
| Профстандарты | primary | 949 | official_download | primary |
| ЕТКС | not_probed | 0 | not_probed | next_probe |
| Трудвсем | blocked | 0 | blocked | blocked |
| НПД | primary | 8 | official | primary |
| Соцконтракт | blocked | 0 | blocked | blocked |

## Files Created

- scripts/download_okpd2_structured.py
- scripts/parse_okpd2_structured.py
- scripts/download_okpdtr_2025.py
- scripts/parse_okpdtr_2025.py
- scripts/download_okz_2014.py
- scripts/parse_okz_2014.py
- data/raw/okpd2/okpd_classifikators.xlsx
- data/raw/okz/okz_classifikators.xlsx
- data/raw/okpdtr/okpdtr_download_attempts.json
- data/parsed/okpd2_raw.json
- data/parsed/okpd2_raw.csv
- data/parsed/okpd2_normalized.json
- data/parsed/okpd2_service_work_candidates.json
- data/parsed/okpdtr_raw.json
- data/parsed/okpdtr_raw.csv
- data/parsed/okpdtr_normalized.json
- data/parsed/okpdtr_profession_candidates.json
- data/parsed/okz_raw.json
- data/parsed/okz_raw.csv
- data/parsed/okz_normalized.json
- data/parsed/okz_service_occupation_candidates.json

## Files Changed

- data/parsed/source_quality_matrix.json
- data/reports/source_map.md
- data/reports/ingestion_report.md (this file)
- data/reports/ingestion_errors.md

## Next Steps

1. Manual download of ОКПДТР from profstandart.rosmintrud.ru or vniot.ru
2. Rebuild source_bridge_candidates.json with new OKPD2/OKZ data
3. Run bridge review with human_review_required
4. Probe ЕТКС for additional profession data

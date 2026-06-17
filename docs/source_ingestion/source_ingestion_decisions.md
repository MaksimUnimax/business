# Source Ingestion Decisions

This document records key decisions made during source ingestion work and explains the reasoning behind each.

## Decision Log

### D1: A source cannot be primary if parsed_rows = 0

**Decision**: Only sources with actual parsed data can be classified as "primary" for the catalog.

**Rationale**: A source with 0 parsed rows provides no usable data. Claiming it as primary creates false expectations about data availability.

**Applied to**: ОКПДТР (0 rows, manual_download_required), ЕТКС (0 rows, not_probed), Трудвсем (0 rows, blocked).

### D2: Mirror sources must not be called "official"

**Decision**: Sources from `classifikators.ru` or similar mirrors must be tagged as `mirror_unofficial`, never as `official`.

**Rationale**: Mirror sites are not authoritative. They may contain errors, outdated data, or modifications. Using "official" for mirror data would misrepresent its provenance.

**Applied to**: ОКПД 2 mirror, ОКЗ mirror.

### D3: OKPD2 mirror can be enrichment only

**Decision**: ОКПД 2 data from classifikators.ru mirror is usable for enrichment only, not as a primary source.

**Rationale**: The official ОКПД 2 source (pravo.gov.ru, consultant.ru) has no machine-readable download. The mirror provides data, but its unofficial provenance limits its role to enrichment.

### D4: OKZ mirror is blocked from bridge until semantic validation

**Decision**: ОКЗ data must not be included in the source bridge until semantic validation is completed.

**Rationale**: OKZ sample data contained suspicious service-like rows (e.g., "9602 Парикмахерские и аналогичные услуги", "9603 Услуги по уходу за животными") that appear to be service classifications rather than proper occupation entries. This suggests data contamination that must be resolved before use.

### D5: OKPDTR remains manual download

**Decision**: ОКПДТР (ОК 016-2025) requires manual download from profstandart.rosmintrud.ru or vniot.ru.

**Rationale**: All server-accessible sources failed: classifikators.ru (404), consultant.ru (no download), garant.ru (no download), vniot.ru (DNS failure), vcot.ru (connection refused), profstandart.rosmintrud.ru (timeout). The classifier is only available as legal text, not as structured data.

### D6: Existing source bridge is not final catalog

**Decision**: The current source bridge (13 candidates) is not the final business catalog.

**Rationale**: The bridge was built before OKPD2/OKZ v4 data became available. It has not been rebuilt with new classifier data. Treating it as final would exclude valuable enrichment sources and potentially include contaminated OKZ data.

## Forbidden Conclusions

The following conclusions must NOT be drawn from current data:

1. **Do NOT create final business catalog yet.** The source ingestion is still in progress. OKPD2 enrichment needs integration, OKZ needs validation, and OKPDTR needs manual download.

2. **Do NOT use OKZ for occupations until validated.** Suspicious service-like rows indicate contamination that must be resolved.

3. **Do NOT treat classifikators.ru mirror as official source.** All mirror data is enrichment-only.

4. **Do NOT treat Avito/procurement/ad checks as done from source-ingestion.** These are separate research tasks not covered by the source ingestion pipeline.

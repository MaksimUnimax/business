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

**Status**: COMPLETED. OKPD2 is used as enrichment in the rebuilt bridge.

### D4: OKZ mirror validated for bridge use (v4.1)

**Decision**: ОКЗ data is validated and included in the source bridge as enrichment.

**Rationale**: Semantic validation v4.1 confirmed:
- OKZ has correct occupation code 5141 (Парикмахеры)
- 269 occupation rows found matching expected OKZ patterns
- The original concern about 9602/9603 contamination was **refuted** — these codes only exist in OKPD2, not in OKZ
- No cross-contamination with OKPD2 detected

**Status**: COMPLETED. OKZ is used as enrichment in the rebuilt bridge.

### D5: OKPDTR remains manual download

**Decision**: ОКПДТР (ОК 016-2025) requires manual download from profstandart.rosmintrud.ru or vniot.ru.

**Rationale**: All server-accessible sources failed: classifikators.ru (404), consultant.ru (no download), garant.ru (no download), vniot.ru (DNS failure), vcot.ru (connection refused), profstandart.rosmintrud.ru (timeout). The classifier is only available as legal text, not as structured data.

**Status**: OPEN. OKPDTR is blocked from bridge until manual download is completed.

### D6: Source bridge rebuilt with validated layers (v4.1)

**Decision**: Source bridge (`source_bridge_candidates.json`) has been rebuilt using all validated source layers: OKVED2, Profstandards, NPD, OKPD2 enrichment, OKZ enrichment.

**Rationale**: Semantic validation confirmed OKPD2 and OKZ are valid enrichment sources. Bridge was rebuilt with deterministic keyword matching. All 13 candidates have `human_review_required: true`.

**Status**: COMPLETED. Bridge is not final catalog — requires human review.

### D7: Semantic validation completed (v4.1)

**Decision**: OKPD2 and OKZ semantic validation completed. Both classifiers are valid and included in bridge.

**Rationale**:
- OKPD2: 373 expected service/product patterns found. Service-like names (услуги, ремонт) are expected for OKPD2.
- OKZ: 269 occupation rows found. Code 5141 (Парикмахеры) confirmed. Original 9602/9603 concern was a false positive — these codes exist only in OKPD2.
- No cross-contamination between OKPD2 and OKZ.

**Status**: COMPLETED.

## Forbidden Conclusions

The following conclusions must NOT be drawn from current data:

1. **Do NOT create final business catalog yet.** The bridge is a review layer, not a recommendation. Human review must be completed first.

2. **Do NOT treat classifikators.ru mirror as official source.** All mirror data is enrichment-only.

3. **Bridge candidate does not equal approved business direction.** All bridge rows require human review before any direction is considered validated.

4. **Do NOT generate business recommendations or user-fit scoring from bridge alone.** The bridge is raw source-matched candidates, not a business plan.

5. **Do NOT treat Avito/procurement/ad checks as done from source-ingestion.** These are separate research tasks not covered by the source ingestion pipeline.

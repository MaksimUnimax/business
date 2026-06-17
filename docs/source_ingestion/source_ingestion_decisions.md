# Source Ingestion Decisions

This document records key decisions made during source ingestion work and explains the reasoning behind each.

## Decision Log

### D1: A source cannot be primary if parsed_rows = 0

**Decision**: Only sources with actual parsed data can be classified as "primary" for the catalog.

**Rationale**: A source with 0 parsed rows provides no usable data. Claiming it as primary creates false expectations about data availability.

**Applied to**: ОКПДТР (0 rows, manual_download_required), ЕТКС (0 rows, not_probed), Трудвсем (0 rows, blocked).

### D2: Mirror sources must not be called "official"

**Decision**: Sources from `classifikators.ru` or similar mirrors must be tagged as `mirror_unofficial`, never as `official`.

**Rationale**: Mirror sites are not authoritative. Using "official" for mirror data would misrepresent its provenance.

**Status**: COMPLETED. Applied to OKPD2 mirror and OKZ mirror.

### D3: OKPD2 mirror can be enrichment only

**Decision**: ОКПД 2 data from classifikators.ru mirror is usable for enrichment only, not as a primary source.

**Status**: COMPLETED. OKPD2 used as enrichment in rebuilt bridge.

### D4: OKZ mirror validated for bridge use (v4.1)

**Decision**: ОКЗ data is validated and included in the source bridge as enrichment.

**Status**: COMPLETED. OKZ used as enrichment in rebuilt bridge.

### D5: OKPDTR remains manual download

**Decision**: ОКПДТР (ОК 016-2025) requires manual download from profstandart.rosmintrud.ru or vniot.ru.

**Status**: OPEN. Blocked from bridge until manual download completed.

### D6: Source bridge rebuilt with validated layers (v4.1)

**Decision**: Source bridge rebuilt using all validated source layers: OKVED2, Profstandards, NPD, OKPD2 enrichment, OKZ enrichment.

**Status**: COMPLETED. Bridge is not final catalog — requires human review.

### D7: Semantic validation completed (v4.1)

**Decision**: OKPD2 and OKZ semantic validation completed. Both classifiers are valid and included in bridge.

**Status**: COMPLETED.

### D8: Human review completed for bridge candidates

**Decision**: All 13 bridge candidates reviewed with deterministic heuristics. 10 accepted for catalog schema, 3 need more source.

**Rationale**: Review checked each source match for direct relevance to candidate key. Overbroad matches (generic trade/wholesale, unrelated profstandards) were rejected. Ambiguous matches flagged as needs_more_source.

**Status**: COMPLETED. Bridge is not final catalog. Accepted candidates can proceed to schema design.

## Forbidden Conclusions

1. **Do NOT create final business catalog yet.** Human review is complete but schema design and catalog construction are separate steps.

2. **Do NOT treat classifikators.ru mirror as official source.** All mirror data is enrichment-only.

3. **Bridge candidate does not equal approved business direction.** Accepted means eligible for schema design, not final approval.

4. **Do NOT generate business recommendations or user-fit scoring from bridge alone.** The bridge is raw source-matched candidates.

5. **Do NOT treat Avito/procurement/ad checks as done from source-ingestion.**

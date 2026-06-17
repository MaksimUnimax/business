# Source Ingestion Decisions

## Decision Log

### D1: A source cannot be primary if parsed_rows = 0
**Status**: COMPLETED.

### D2: Mirror sources must not be called "official"
**Status**: COMPLETED. Applied to OKPD2 and OKZ mirrors.

### D3: OKPD2 mirror can be enrichment only
**Status**: COMPLETED.

### D4: OKZ mirror validated for bridge use (v4.1)
**Status**: COMPLETED.

### D5: OKPDTR remains manual download
**Status**: OPEN. Blocked from bridge.

### D6: Source bridge rebuilt with validated layers (v4.1)
**Status**: COMPLETED.

### D7: Semantic validation completed (v4.1)
**Status**: COMPLETED.

### D8: Human review completed for bridge candidates
**Status**: COMPLETED. 10 accepted, 3 need more source, 0 rejected.

### D9: Business direction catalog schema v0 created
**Decision**: Created JSON Schema v0 and draft catalog records for 10 accepted bridge candidates.
**Rationale**: Schema defines 14 sections (identity, source, NPD, social contract, person-fit, training, market, procurement, ads, questionnaire, scoring, review). Draft records fill only source-derived fields; all other fields are placeholders.
**Status**: COMPLETED. Schema is draft. Draft records are not final approved directions.

## Forbidden Conclusions

1. **Do NOT create final business catalog yet.** Schema human review and questionnaire mapping are required first.
2. **Do NOT treat draft records as approved directions.** All have `not_user_recommendation: true`.
3. **Do NOT generate business recommendations from schema alone.**
4. **Market/procurement/ads/unit economics are placeholders** — require separate validation steps.

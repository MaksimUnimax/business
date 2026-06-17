# Source Ingestion Decisions

## Decision Log

### D1-D7: Previous decisions (completed)
See prior versions for D1 (parsed_rows=0 can't be primary), D2 (mirrors not official), D3 (OKPD2 enrichment only), D4 (OKZ validated), D5 (OKPDTR manual), D6 (bridge rebuilt), D7 (semantic validation completed).

### D8: Human review completed for bridge candidates
**Status**: COMPLETED. 10 accepted, 3 need more source, 0 rejected.

### D9: Catalog schema v0 created
**Decision**: Created JSON Schema v0 and draft catalog records for 10 accepted bridge candidates.
**Rationale**: Schema defines 14 sections (identity, source, NPD, social contract, person-fit, training, market, procurement, ads, questionnaire, scoring, review). Draft records fill only source-derived fields; all other fields are placeholders (missing_data/null).
**Status**: COMPLETED. Draft is not final catalog.

## Forbidden Conclusions

1. **Do NOT create final business catalog yet.** Schema + draft created. Next step is human review of schema and questionnaire mapping.
2. **Do NOT treat draft records as approved directions.** All have `not_user_recommendation: true`.
3. **Do NOT generate business recommendations from schema alone.**
4. **Market/procurement/ads/unit economics are placeholders** — require separate validation steps.

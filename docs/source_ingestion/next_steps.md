# Next Steps

## Completed Steps

1. **Source download and parsing (v4)** — COMPLETED
   - OKPD2 parsed from classifikators.ru mirror: 20387 rows
   - OKZ parsed from classifikators.ru mirror: 608 rows
   - OKPDTR: manual download required (all sources failed)

2. **Semantic validation v4.1** — COMPLETED
   - OKPD2: `valid_mirror_enrichment`
   - OKZ: `valid_mirror_enrichment`
   - Cross-contamination: none

3. **Source bridge rebuild** — COMPLETED
   - Bridge rebuilt with validated OKPD2 and OKZ enrichment
   - 13 candidates, all `human_review_required: true`
   - Bridge is NOT final catalog

## Current Next Step

`human_review_of_bridge_candidates`

### What This Step Does

Review each of 13 bridge candidate keys and their source matches to determine which matches are valid and which need refinement.

### Acceptance Criteria

- Review each of 13 bridge candidate keys
- Mark source matches as accept/reject/needs_more_source
- Check overbroad matches, especially profstandards and OKZ broad groups
- Keep `human_review_required=true` on all rows
- Do not create final business catalog unless a separate schema prompt is approved

### After Human Review

Next possible step: `business_direction_catalog_schema_v0`

## After Executor Push

After this documentation is pushed, **ChatGPT must independently verify GitHub state** — confirm the docs are visible on GitHub and that no unintended files were changed.

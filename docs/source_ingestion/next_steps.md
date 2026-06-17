# Next Steps

## Completed: Semantic Validation v4.1

Semantic validation of OKPD2 and OKZ classifiers has been completed:

- **OKPD2**: `valid_mirror_enrichment` — safe for enrichment use
- **OKZ**: `valid_mirror_enrichment` — safe for enrichment use; original 9602/9603 concern refuted
- **Cross-contamination**: None detected
- **Bridge decision**: Both OKPD2 and OKZ allowed in next bridge

## Current Next Step

`rebuild_source_bridge_with_okpd2_and_okz`

### What This Step Does

Rebuild `source_bridge_candidates.json` to include OKPD2 enrichment data and OKZ occupation data.

### Acceptance Criteria

- OKPD2 service/work candidates integrated into bridge
- OKZ occupation candidates integrated into bridge
- Existing OKVED2 and Profstandards data preserved
- All bridge candidates reviewed with human_review_required flag
- No final catalog created

### Blocked Items

- OKPDTR: 0 rows, manual download required from profstandart.rosmintrud.ru or vniot.ru
- ЕТКС: not yet probed

## After Executor Push

After this documentation is pushed, **ChatGPT must independently verify GitHub state** — confirm the docs are visible on GitHub and that no unintended files were changed.

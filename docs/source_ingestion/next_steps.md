# Next Steps

## Current Next Step

`classifier_semantic_validation_v4_1`

### What This Step Does

Validate the semantic quality of OKPD2 and OKZ mirror data before integrating into the source bridge.

### Acceptance Criteria

- Validate OKPD2 semantics: confirm service/work candidates are correctly classified
- Validate OKZ semantics: confirm occupation candidates are proper occupations, not service descriptions
- Detect OKPD2/OKZ contamination: identify any rows that belong to a different classification domain
- Decide whether next bridge should include or exclude OKZ based on validation results
- **Do NOT rebuild bridge in semantic validation run** — this step is analysis only

### Blocked Items

- OKZ: 188 occupation candidates require semantic validation before any bridge use
- OKPDTR: 0 rows, manual download required from profstandart.rosmintrud.ru or vniot.ru

## After Executor Push

After this documentation is pushed, **ChatGPT must independently verify GitHub state** — confirm the docs are visible on GitHub and that no unintended files were changed.

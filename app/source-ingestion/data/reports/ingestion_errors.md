# Ingestion Errors (v4)

## OKPDTR-2025: No Structured File Available

**Date**: 2026-06-17
**Classifier**: ОКПДТР (ОК 016-2025)
**Status**: manual_download_required
**Error**: No downloadable structured file found from any accessible source.

**Sources tried**:
1. classifikators.ru/okpdtr → 404 (not listed)
2. classifikators.ru/okpdtr-2025 → 404
3. consultant.ru/document/cons_doc_LAW_358468/ → 200 but no download links (legal text only)
4. base.garant.ru/71166736/ → 200 but no download links (legal text only)
5. vniot.ru → DNS resolution failure (host unreachable)
6. vcot.ru → Connection refused
7. profstandart.rosmintrud.ru → Connection timeout
8. GitHub search → No structured files found

**Root cause**: OKPDTR-2025 is a recently updated classifier (ОК 016-2025). The structured data (xlsx/xls/csv) appears to only be available through:
- profstandart.rosmintrud.ru (timeout from this server)
- vniot.ru (DNS failure)
- vcot.ru (connection refused)

**Resolution**: Manual download required from one of these sources, or wait for them to become accessible.

## Previous v3 Incorrect Decision

**Date**: 2026-06-17
**Error**: v3 report stated "OKPD2 parsed_rows = 0" but the quality matrix listed it as "candidate_blocked_or_manual" with parsed_rows = 0. This was inconsistent.
**Correction**: v4 confirms OKPD2 has 20,387 rows from mirror source. OKPDTR has 0 rows. OKZ has 608 rows from mirror source.

## Network Issues

- vniot.ru: DNS resolution failure
- vcot.ru: Connection refused
- profstandart.rosmintrud.ru: Connection timeout
- docs.cntd.ru: Connection timeout
- fst.gov.ru: DNS resolution failure

# Classifier Semantic Validation v4.1

## Run Mode
classifier_semantic_validation_v4_1

## Summary

Semantic validation of OKPD2 and OKZ mirror classifiers before source bridge rebuild.

## OKPD2 Result

- **Status**: valid_mirror_enrichment
- **Parsed rows**: 20387
- **Expected patterns found**: 95.11 (computer repair), 95.2 (appliance repair), 96.01 (laundry), 96.02 (hairdressing)
- **Source**: classifikators.ru mirror, mirror_unofficial
- **Conclusion**: OKPD2 is a valid classifier of products/services/works. Service-like names (услуги, ремонт, стирка) are expected for OKPD2. Safe for enrichment use.

## OKZ Result

- **Status**: valid_mirror_enrichment
- **Parsed rows**: 608
- **Expected occupation codes found**: 5141 (Парикмахеры), 5142 (Косметологи), 514 (service workers)
- **Occupation rows found**: 269 rows match occupation terms
- **Original concern (9602/9603)**: Confirmed ABSENT from OKZ data. These codes only exist in OKPD2.
- **Source**: classifikators.ru mirror, mirror_unofficial
- **Conclusion**: OKZ is a valid occupation classifier. The original concern about service contamination was unfounded.

## Suspicious Examples (Refuted)

| Code | Original Concern | Actual Finding |
|------|-----------------|----------------|
| 9602 | "Парикмахерские и аналогичные услуги" in OKZ | Code only exists in OKPD2, not in OKZ. OKZ has 5141 "Парикмахеры". |
| 9603 | "Услуги по уходу за животными" in OKZ | Code only exists in OKPD2, not in OKZ. |

## Allowed Sources for Next Bridge

| Source | Role | Status |
|--------|------|--------|
| ОКВЭД 2 (Росстат) | primary | primary |
| Реестр профстандартов | primary | primary |
| НПД ограничения | primary (legal) | primary |
| ОКПД 2 (mirror) | enrichment | enrichment |
| ОКЗ-2014 (mirror) | enrichment | enrichment |

## Blocked Sources

| Source | Reason |
|--------|--------|
| ОКПД 2 (official) | No machine-readable download |
| ОКЗ-2014 (official) | No machine-readable download |
| ОКПДТР | Manual download required |
| Трудвсем | QRATOR blocks API |
| ЕТКС | Not yet probed |
| Соцконтракт | Pages unreachable |

## Decision

**A**: OKPD2 and OKZ validated; proceed to rebuild source bridge with OKPD2 and OKZ.

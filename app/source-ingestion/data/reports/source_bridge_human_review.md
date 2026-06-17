# Source Bridge Human Review

## Run Mode
human_review_of_bridge_candidates_push

## Candidate Count
Total reviewed: 13

## Summary Table

| Candidate Key | Overall Status | Accepted | Rejected | Needs More | Main Concerns |
|---------------|----------------|----------|----------|------------|---------------|
| furniture_assembly | Accepted For Catalog Schema | 11 | 9 | 34 | Accepted: sufficient source matches across multiple layers |
| cleaning_services | Accepted For Catalog Schema | 11 | 0 | 14 | Accepted: sufficient source matches across multiple layers |
| clothing_repair_sewing | Accepted For Catalog Schema | 27 | 13 | 10 | Accepted: sufficient source matches across multiple layers |
| shoe_repair | Accepted For Catalog Schema | 29 | 0 | 10 | Accepted: sufficient source matches across multiple layers |
| bicycle_repair | Needs More Source Before Catalog | 9 | 0 | 29 | Needs more source: too many broad/ambiguous matches |
| appliance_repair | Accepted For Catalog Schema | 16 | 0 | 29 | Accepted: sufficient source matches across multiple layers |
| hair_beauty_services | Accepted For Catalog Schema | 17 | 0 | 8 | Accepted: sufficient source matches across multiple layers |
| manicure_pedicure | Accepted For Catalog Schema | 12 | 0 | 14 | Accepted: sufficient source matches across multiple layers |
| photography_video | Needs More Source Before Catalog | 9 | 0 | 58 | Needs more source: too many broad/ambiguous matches |
| tutoring_education | Accepted For Catalog Schema | 27 | 0 | 5 | Accepted: sufficient source matches across multiple layers |
| animal_care | Accepted For Catalog Schema | 25 | 0 | 24 | Accepted: sufficient source matches across multiple layers |
| gardening_plants | Accepted For Catalog Schema | 15 | 1 | 23 | Accepted: sufficient source matches across multiple layers |
| sharpening_tools | Needs More Source Before Catalog | 10 | 0 | 23 | Needs more source: too many broad/ambiguous matches |

## Accepted for Catalog Schema
- **furniture_assembly** (Сборка и ремонт мебели): 11 accepted matches
- **cleaning_services** (Клининговые и уборочные услуги): 11 accepted matches
- **clothing_repair_sewing** (Ремонт и пошив одежды): 27 accepted matches
- **shoe_repair** (Ремонт обуви): 29 accepted matches
- **appliance_repair** (Ремонт бытовой техники и электроники): 16 accepted matches
- **hair_beauty_services** (Парикмахерские и косметические услуги): 17 accepted matches
- **manicure_pedicure** (Маникюр и педикюр): 12 accepted matches
- **tutoring_education** (Репетиторство и обучение): 27 accepted matches
- **animal_care** (Уход за животными): 25 accepted matches
- **gardening_plants** (Садоводство и озеленение): 15 accepted matches

## Needs More Source Before Catalog
- **bicycle_repair** (Ремонт велосипедов): 29 ambiguous matches
- **photography_video** (Фото- и видеосъёмка): 58 ambiguous matches
- **sharpening_tools** (Заточка инструментов): 23 ambiguous matches

## Rejected for Now
- (none)

## Match Review Totals
- Accepted: 218
- Rejected: 23
- Needs more source: 281

## Limitations
- This review is not final business catalog and not user recommendation.
- Accepted means candidate can move into schema design, not that direction is approved.
- All rows still have human_review_required=true.
- Deterministic heuristic review only, no LLM or external APIs.

## Next Step
- 10 candidates accepted for catalog schema
- 3 candidates need more source data
- Next possible step: business_direction_catalog_schema_v0

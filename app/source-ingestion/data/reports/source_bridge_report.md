# Source Bridge Report

## Run Mode
rebuild_source_bridge_with_okpd2_okz_push

## Source Layers Used
- OKVED2 Rosstat (primary): 981 service candidates
- Profstandards Mintrud (primary): 519 service candidates
- NPD legal hard filters (legal_filter): 8 rules
- OKPD2 mirror (enrichment, validated): 7173 service/work candidates
- OKZ mirror (enrichment, validated): 188 occupation candidates

## Blocked Source Layers
- OKPD2 official (no machine-readable parsed source)
- OKZ official (no machine-readable parsed source)
- OKPDTR (parsed_rows = 0, manual_download_required)
- Trudvsem (blocked by QRATOR)
- Social contract (not parsed)
- ETKS (not parsed)

## Bridge Candidate Count
Total: 13

## Per Candidate Summary

### furniture_assembly
- OKVED2 matches: 13
- Profstandard matches: 13
- OKPD2 enrichment matches: 20
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### cleaning_services
- OKVED2 matches: 9
- Profstandard matches: 5
- OKPD2 enrichment matches: 3
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### clothing_repair_sewing
- OKVED2 matches: 20
- Profstandard matches: 2
- OKPD2 enrichment matches: 20
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### shoe_repair
- OKVED2 matches: 10
- Profstandard matches: 1
- OKPD2 enrichment matches: 20
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### bicycle_repair
- OKVED2 matches: 3
- Profstandard matches: 0
- OKPD2 enrichment matches: 20
- OKZ enrichment matches: 7
- Confidence: high
- Human review required: yes

### appliance_repair
- OKVED2 matches: 0
- Profstandard matches: 20
- OKPD2 enrichment matches: 3
- OKZ enrichment matches: 14
- Confidence: high
- Human review required: yes

### hair_beauty_services
- OKVED2 matches: 4
- Profstandard matches: 1
- OKPD2 enrichment matches: 12
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### manicure_pedicure
- OKVED2 matches: 9
- Profstandard matches: 1
- OKPD2 enrichment matches: 8
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### photography_video
- OKVED2 matches: 16
- Profstandard matches: 20
- OKPD2 enrichment matches: 20
- OKZ enrichment matches: 3
- Confidence: high
- Human review required: yes

### tutoring_education
- OKVED2 matches: 20
- Profstandard matches: 4
- OKPD2 enrichment matches: 0
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### animal_care
- OKVED2 matches: 20
- Profstandard matches: 5
- OKPD2 enrichment matches: 16
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### gardening_plants
- OKVED2 matches: 18
- Profstandard matches: 1
- OKPD2 enrichment matches: 12
- OKZ enrichment matches: 0
- Confidence: high
- Human review required: yes

### sharpening_tools
- OKVED2 matches: 3
- Profstandard matches: 20
- OKPD2 enrichment matches: 0
- OKZ enrichment matches: 2
- Confidence: high
- Human review required: yes

## Limitations
- Bridge is NOT final catalog
- All rows require human review
- OKPD2 and OKZ are mirror_unofficial enrichment, not official primary
- No LLM or external APIs used in matching
- Deterministic keyword matching only

## Next Step
Human review of bridge candidates, then optionally business_direction_catalog_schema_v0

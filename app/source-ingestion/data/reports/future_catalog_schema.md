# Future Catalog Schema

## Business Direction Structure

This document describes how raw source data maps into the future `business_direction` catalog.

## Schema

```yaml
business_direction:
  id: string  # unique identifier
  title: string  # human-readable name
  
  source_basis:
    okved_codes:  # ОКВЭД 2 codes
      - code: string
        name: string
        relevance: high/medium/low
    
    okpd2_codes:  # ОКПД 2 codes (what is produced/sold)
      - code: string
        name: string
        type: service/work/product
    
    okpdtr_codes:  # ОКПДТР (professions/positions)
      - code: string
        title: string
        type: worker_profession/employee_position
    
    okz_codes:  # ОКЗ (occupation groups)
      - code: string
        title: string
        group_level: string
    
    profstandard_ids:  # Professional standards
      - id: string
        title: string
        professional_area: string
    
    etks_entries:  # ЕТКС (qualification characteristics)
      - profession: string
        description: string
        requirements: string
    
    trudvsem_titles:  # Real job titles from labor market
      - title: string
        frequency: number  # how often this title appears
        region: string
  
  npd_rules:  # НПД (self-employment) restrictions
    resale: allowed/blocked/conditional
    own_production: allowed/blocked/conditional
    employees: allowed/blocked/conditional
    marked_goods: allowed/blocked/conditional
    excisable_goods: allowed/blocked/conditional
    agency: allowed/blocked/conditional
    income_limit: 2400000  # annual RUB limit
  
  social_contract_rules:  # Social contract financing
    max_amount: number  # maximum financing amount
    allowed_expenses:
      - string
    risky_expenses:
      - string
    forbidden_expenses:
      - string
    business_plan_required: boolean
    reporting_required: boolean
    activity_period_months: number
  
  extraction_status:
    source_backed: boolean  # at least one source provides data
    human_review_required: boolean  # needs manual verification
    sources_used:
      - source_id: string
        confidence: high/medium/low
```

## Source-to-Field Mapping

| Field | Primary Source | Enrichment Source | Validation Source |
|-------|---------------|-------------------|-------------------|
| okved_codes | okved2_rosstat | okved2_fns | - |
| okpd2_codes | okpd2_official | - | - |
| okpdtr_codes | okpdtr_mintrud | etks_mintrud | - |
| okz_codes | okz_mintrud | - | - |
| profstandard_ids | profstandarts_mintrud | - | - |
| etks_entries | etks_mintrud | okpdtr_mintrud | - |
| trudvsem_titles | trudvsem_api | - | - |
| npd_rules | npd_nalog | - | - |
| social_contract_rules | social_contract | - | - |

## Data Flow

```
Raw Sources → Parsed Samples → Quality Matrix → Business Direction Catalog
     ↓              ↓                ↓                    ↓
  CSV/XML/JSON   JSON files     source_quality     business_direction
  HTML pages     npd_rules      matrix.json        YAML/JSON catalog
```

## Next Steps

1. Complete source ingestion for all probe targets
2. Build parsers for each machine-readable source
3. Create mapping rules from source fields to catalog fields
4. Implement catalog builder that merges sources
5. Add human review workflow for ambiguous mappings

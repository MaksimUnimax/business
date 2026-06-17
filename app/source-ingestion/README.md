# Source Ingestion Probe

Proof-of-concept for sourcing machine-readable data for a business direction catalog.

## Purpose

Find and verify specific machine-readable sources for building a catalog of:
- Business activities (виды деятельности)
- Services/works (услуги/работы)
- Professions/occupations (профессии/занятия)
- Professional standards (профстандарты)
- Real job names (реальные названия работ)
- NPD restrictions (ограничения НПД)
- Social contract rules (правила соцконтракта)

## What This Does NOT Do

- Does NOT generate profession lists from LLM
- Does NOT create business plans
- Does NOT scrape Avito/Ozon
- Does NOT use browser automation

## Sources Probed

| Source | Status | Machine Readable | Use |
|--------|--------|------------------|-----|
| ОКВЭД 2 (Росстат) | partial | partial | primary |
| ОКВЭД 2 (ФНС) | partial | no | validation |
| ОКПД 2 | needs_investigation | partial | enrichment |
| ОКПДТР | probe_needed | partial | enrichment |
| ОКЗ-2014 | probe_needed | partial | enrichment |
| Профстандарты | probe_needed | yes | primary |
| ЕТКС | probe_needed | partial | enrichment |
| Трудвсем API | probe_needed | yes | primary |
| НПД ограничения | encoded | no | primary |
| Соцконтракт | probe_needed | no | enrichment |

## Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/fetch_sources.py
python scripts/build_source_quality_matrix.py
pytest -q
```

## Output

- `source_registry.yaml` - All sources with metadata
- `data/ingestion_result.json` - Probe results
- `data/parsed/source_quality_matrix.json` - Quality scores
- `data/parsed/npd_rules_v0.json` - Encoded NPD rules
- `data/reports/source_map.md` - Source summary
- `data/reports/future_catalog_schema.md` - Catalog schema

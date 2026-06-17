> **Current source status is documented in [`../../docs/source_ingestion/source_state.md`](../../docs/source_ingestion/source_state.md).**

# Source Ingestion

Scripts, data, and tests for ingesting machine-readable classifier and source data for a business direction catalog.

## Purpose

- Download and parse classifier data (ОКВЭД 2, ОКПД 2, ОКЗ, ОКПДТР, Профстандарты)
- Build source quality matrix
- Generate source bridge candidates

## What This Does NOT Do

- Does NOT generate profession lists from LLM
- Does NOT create business plans
- Does NOT scrape Avito/Ozon
- Does NOT use browser automation

## Structure

- `source_registry.yaml` — all sources with metadata
- `scripts/` — download, parse, and build scripts
- `data/raw/` — downloaded source files
- `data/parsed/` — parsed JSON/CSV outputs
- `data/reports/` — ingestion reports and source map
- `tests/` — pytest test suite

## Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/fetch_sources.py
python scripts/build_source_quality_matrix.py
pytest -q
```

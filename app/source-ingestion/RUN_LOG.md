# Source Ingestion Probe Run Log

## Run Date
2026-06-17

## Run Mode
source_ingestion_probe_for_business_direction_catalog

## Environment
- user: root
- workdir: /opt/market-intel/source-ingestion-probe
- python_version: 3.10.12
- node_version: v22.22.2

## Commands Executed

### 1. Environment Check
```bash
pwd && whoami && uname -a && python3 --version && node --version && npm --version && git --version
```

### 2. Project Setup
```bash
mkdir -p /opt/market-intel/source-ingestion-probe
cd /opt/market-intel/source-ingestion-probe
git init
mkdir -p scripts data/{raw,mintrud_profstandards,trudvsem,okved,okpd2,okpdtr,okz,etks,npd_restrictions,social_contract,parsed,reports} tests
```

### 3. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Source Probes
```bash
python scripts/fetch_sources.py
```

### 5. Build Quality Matrix
```bash
python scripts/build_source_quality_matrix.py
```

### 6. Run Tests
```bash
pytest -q
```

## Key Findings

1. **ОКВЭД 2 (Росстат)**: Folder page accessible, but no direct CSV/XML links found
2. **Трудвсем API**: API endpoint accessible, search query works
3. **Профстандарты**: Open data page accessible, CSV links need discovery
4. **НПД правила**: Manually encoded from official source
5. **Соцконтракт**: Federal and regional pages probed

## Source Status Summary

| Source | Status | Machine Readable |
|--------|--------|------------------|
| ОКВЭД 2 | partial | partial |
| ОКПД 2 | needs_investigation | partial |
| ОКПДТР | probe_needed | partial |
| ОКЗ | probe_needed | partial |
| Профстандарты | probe_needed | yes |
| ЕТКС | probe_needed | partial |
| Трудвсем | probe_needed | yes |
| НПД | encoded | no |
| Соцконтракт | probe_needed | no |

## Files Created

- README.md
- RUN_LOG.md
- requirements.txt
- source_registry.yaml
- scripts/fetch_sources.py
- scripts/build_source_quality_matrix.py
- tests/test_source_registry.py
- data/parsed/npd_rules_v0.json
- data/parsed/source_quality_matrix.json
- data/reports/source_map.md
- data/reports/future_catalog_schema.md

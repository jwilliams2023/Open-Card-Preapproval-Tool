# Directory Structure

This document outlines the current directory structure for the Open Card Preapproval Tool project. Future structure plans are included at the end for reference.

## Current Structure

```
Open-Card-Preapproval-Tool/
├── README.md
├── CHANGELOG.md
├── DIRECTORY_STRUCTURE.md
├── QUICK_START.md
├── requirements.txt
├── run_scraper.py
├── run_extractor.py
├── src/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── reddit_scraper.py
│   └── extractors/
│       ├── __init__.py
│       ├── llm_extractor.py
│       ├── llm_filter.py
│       ├── rule_extractor.py
│       └── strict_filter.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── legacy/
└── notebooks/
    └── data_exploration.ipynb
```

- `src/scrapers/`: Data collection modules (Reddit only for now)
- `src/extractors/`: Data extraction and filtering modules
- `data/raw/`: Raw scraped data (CSV)
- `data/processed/`: (empty, for future use)
- `data/legacy/`: Historical data files from previous runs
- `notebooks/`: Jupyter notebooks for analysis

## Future Structure (Planned)

_The following is a proposed structure for when the project expands to multiple sources, backend, frontend, and production deployment._

```
Open-Card-Preapproval-Tool/
├── ... (current files)
├── src/
│   ├── models/
│   ├── api/
│   ├── database/
│   ├── utils/
│   └── tests/
├── frontend/
├── scripts/
├── config/
├── docs/
├── .github/
├── docker/
└── ...
```

See the README and roadmap for more details on future plans. 
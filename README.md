# Open Card Preapproval Tool

A credit card approval analysis tool that collects, extracts, and analyzes approval/denial data from Reddit to understand approval factors and predict approval likelihood. (Multi-source support is a future goal.)

## Project Vision

**Goal:** Build a tool that analyzes credit card approval data from real user experiences to understand what factors lead to approvals vs denials, and eventually create a prediction model for approval likelihood.

**Current Focus:** Proof-of-concept (POC) using Reddit as the data source for the Chase Freedom Unlimited card.

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

## How to Use

See QUICK_START.md for step-by-step instructions.

## Data Flow

1. **Scraping:** Reddit posts → CSV files in `data/raw/`
2. **Extraction:** (if implemented) LLM/rule-based extraction → processed data
3. **Analysis:** Jupyter notebook for data exploration

## File Descriptions

- `run_scraper.py`: Main entry point for data collection
- `run_extractor.py`: Main entry point for data processing (if implemented)
- `src/scrapers/reddit_scraper.py`: Reddit scraping logic
- `src/extractors/llm_extractor.py`: LLM-powered data extraction
- `src/extractors/rule_extractor.py`: Rule-based data extraction
- `src/extractors/llm_filter.py`: LLM-based content filtering
- `src/extractors/strict_filter.py`: Strict content filtering
- `notebooks/data_exploration.ipynb`: Data analysis and visualization

## Contributing

This is a personal project currently in POC phase. Future contributions welcome once the basic architecture is established.

---

## Future Plans (Not Yet Implemented)

- Multi-source scraping (forums, review sites, social media)
- Modular scraper architecture for multiple cards and sources
- FastAPI backend and Supabase database
- React + Tailwind frontend
- CI/CD, Docker, and production deployment
- Source-specific data quality metrics

See DIRECTORY_STRUCTURE.md for future architecture ideas.

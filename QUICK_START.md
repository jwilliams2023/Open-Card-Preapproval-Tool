# Quick Start Guide

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

### 1. Setup Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install praw python-dotenv requests pandas
```

### 2. Configure Environment Variables
Create a `.env` file with your Reddit API credentials:
```
REDDIT_APP_ID=your_reddit_app_id
REDDIT_APP_SECRET=your_reddit_app_secret
REDDIT_APP_NAME=your_app_name
```

### 3. Run the Scraper
```bash
# Activate virtual environment
source venv/bin/activate

# Run the scraper
python run_scraper.py
```

This will:
- Scrape Freedom Unlimited posts from r/CreditCards
- Save data to `data/raw/freedom_unlimited_approval_data_YYYYMMDD_HHMMSS.csv`
- Include metadata: Source, Card_Name, Scraped_At

### 4. Run the Extractor (if implemented)
```bash
# Run the LLM extractor
python run_extractor.py
```

### 5. Analyze Data
```bash
# Open Jupyter notebook
jupyter notebook notebooks/data_exploration.ipynb
```

## File Descriptions

- `run_scraper.py`: Main entry point for data collection
- `run_extractor.py`: Main entry point for data processing (if implemented)
- `src/scrapers/reddit_scraper.py`: Reddit scraping logic
- `src/extractors/llm_extractor.py`: LLM-powered data extraction
- `src/extractors/rule_extractor.py`: Rule-based data extraction
- `src/extractors/llm_filter.py`: LLM-based content filtering
- `src/extractors/strict_filter.py`: Strict content filtering
- `notebooks/data_exploration.ipynb`: Data analysis and visualization 
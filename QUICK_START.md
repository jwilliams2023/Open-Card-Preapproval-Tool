# Quick Start Guide

## Current Structure

```
Open-Card-Preapproval-Tool/
├── README.md                 # Project documentation
├── CHANGELOG.md             # Version history
├── DIRECTORY_STRUCTURE.md   # Future structure planning
├── QUICK_START.md           # This file
├── requirements.txt         # Python dependencies
├── run_scraper.py          # Main script to run scraper
├── run_extractor.py        # Main script to run extractor
├── src/                    # Source code
│   ├── __init__.py
│   ├── scrapers/          # Data collection
│   │   ├── __init__.py
│   │   └── reddit_scraper.py
│   └── extractors/        # Data processing
│       ├── __init__.py
│       ├── llm_extractor.py
│       └── rule_extractor.py
├── data/                   # Data storage
│   ├── raw/               # Raw scraped data
│   └── processed/         # Cleaned data
└── notebooks/             # Jupyter notebooks
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

### 4. Run the Extractor (Coming Soon)
```bash
# Run the LLM extractor
python run_extractor.py
```

### 5. Analyze Data
```bash
# Open Jupyter notebook
jupyter notebook notebooks/data_exploration.ipynb
```

## Key Improvements Made

1. **Modular Structure**: Code organized into `src/scrapers/` and `src/extractors/`
2. **Proper Data Organization**: Raw data goes to `data/raw/`, processed to `data/processed/`
3. **Timestamped Files**: Each scrape gets a unique timestamp
4. **Metadata Tracking**: Source, card name, and scrape time included
5. **Easy Execution**: Simple `run_scraper.py` script
6. **Future-Ready**: Structure supports adding more scrapers and extractors

## Next Steps

1. **Add More Cards**: Expand beyond Freedom Unlimited
2. **Add More Sources**: Forums, review sites, social media
3. **Improve Extraction**: Better LLM prompts and validation
4. **Add FastAPI Backend**: For API endpoints
5. **Add Database**: Supabase integration
6. **Add Frontend**: React + Tailwind interface

## File Descriptions

- `run_scraper.py`: Main entry point for data collection
- `run_extractor.py`: Main entry point for data processing
- `src/scrapers/reddit_scraper.py`: Reddit-specific scraping logic
- `src/extractors/llm_extractor.py`: LLM-powered data extraction
- `src/extractors/rule_extractor.py`: Rule-based data extraction
- `notebooks/data_exploration.ipynb`: Data analysis and visualization 
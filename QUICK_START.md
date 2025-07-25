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

## Complete Data Processing Workflow

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

### 3. Scrape Reddit Data
```bash
# Run the scraper
python run_scraper.py
```
This creates: `data/raw/freedom_unlimited_approval_data_YYYYMMDD_HHMMSS.csv`

### 4. Extract Structured Data
```bash
# Run the complete extraction pipeline
python run_extractor.py
```

This runs:
1. **Rule-based extraction** → `data/processed/rule_extracted_data_YYYYMMDD_HHMMSS.csv`
2. **LLM-based extraction** → `data/processed/llm_extracted_data_YYYYMMDD_HHMMSS.csv` (if Ollama is running)
3. **Data preparation** → `data/processed/model_ready_data_YYYYMMDD_HHMMSS.csv`

### 5. Create Comprehensive Dataset (Optional)
```bash
# Create dataset with original posts and all extracted features
python src/extractors/comprehensive_dataset.py
```

This creates: `data/processed/comprehensive_dataset_YYYYMMDD_HHMMSS.csv`

### 6. Analyze Data
```bash
# Open Jupyter notebook
jupyter notebook notebooks/data_exploration.ipynb
```

## Data Flow

1. **Scraping**: Reddit posts → `data/raw/` (CSV with Title, URL, Body, Source, Card_Name, Scraped_At)
2. **Rule Extraction**: Raw posts → `data/processed/` (extracts Income, Credit Score, Approval Amount using regex)
3. **LLM Extraction**: Rule-extracted data → `data/processed/` (fills missing fields using Mistral LLM)
4. **Analysis**: Processed data → Insights via Jupyter notebook

## File Descriptions

- `run_scraper.py`: Main entry point for data collection
- `run_extractor.py`: Main entry point for data processing pipeline
- `src/scrapers/reddit_scraper.py`: Reddit scraping logic
- `src/extractors/rule_extractor.py`: Rule-based field extraction (regex patterns)
- `src/extractors/llm_extractor.py`: LLM-powered data extraction (requires Ollama)
- `src/extractors/llm_filter.py`: LLM-based content filtering
- `src/extractors/strict_filter.py`: Strict content filtering
- `notebooks/data_exploration.ipynb`: Data analysis and visualization

## Extracted Fields

- **Income**: Annual income (numeric)
- **Credit Score**: FICO score (3-digit number)
- **Approval Amount**: Credit limit (numeric)
- **Age**: User age (numeric, LLM only)
- **Credit History Length**: Length in months/years (numeric, LLM only)
- **Hard Pulls Count**: Recent inquiries (numeric, LLM only) 
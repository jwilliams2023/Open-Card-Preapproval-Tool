# Directory Structure

This document outlines the recommended directory structure for the Open Card Preapproval Tool project, following professional development practices while maintaining simplicity for personal work.

## Current Structure (POC Phase)

```
Open-Card-Preapproval-Tool/
├── README.md                 # Project documentation
├── CHANGELOG.md             # Version history and changes
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── scraper.py              # Reddit data collection
├── llm_extractor.py        # LLM-powered data extraction
├── extract_fields.py       # Rule-based field extraction
├── llm_filter.py           # LLM-based content filtering
├── strict_filter.py        # Strict content filtering
├── data_cleaning.ipynb     # Data analysis notebook
├── data/                   # Data storage
│   ├── raw/               # Raw scraped data
│   ├── processed/         # Cleaned and processed data
│   └── models/            # Trained models (future)
└── venv/                  # Virtual environment
```

## Recommended Future Structure (Professional)

```
Open-Card-Preapproval-Tool/
├── README.md                 # Project documentation
├── CHANGELOG.md             # Version history
├── LICENSE                  # Project license
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Project configuration
├── setup.py                # Package setup (if needed)
├── .github/                # GitHub specific files
│   ├── workflows/          # CI/CD workflows
│   └── ISSUE_TEMPLATE.md   # Issue templates
├── docs/                   # Documentation
│   ├── api/               # API documentation
│   ├── deployment/        # Deployment guides
│   └── development/       # Development guides
├── src/                    # Source code
│   ├── __init__.py
│   ├── scrapers/          # Data collection modules
│   │   ├── __init__.py
│   │   ├── reddit_scraper.py
│   │   └── base_scraper.py
│   ├── extractors/        # Data extraction modules
│   │   ├── __init__.py
│   │   ├── llm_extractor.py
│   │   ├── rule_extractor.py
│   │   └── base_extractor.py
│   ├── models/            # ML models and training
│   │   ├── __init__.py
│   │   ├── prediction_model.py
│   │   ├── feature_engineering.py
│   │   └── evaluation.py
│   ├── api/               # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── middleware/
│   │   └── dependencies/
│   ├── database/          # Database models and connections
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── migrations/
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── helpers.py
│   └── tests/             # Test files
│       ├── __init__.py
│       ├── test_scrapers/
│       ├── test_extractors/
│       ├── test_models/
│       └── test_api/
├── frontend/              # React frontend (future)
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── tailwind.config.js
├── data/                  # Data storage
│   ├── raw/              # Raw scraped data
│   ├── processed/        # Cleaned data
│   ├── models/           # Trained models
│   └── exports/          # Data exports
├── notebooks/            # Jupyter notebooks
│   ├── data_exploration.ipynb
│   ├── model_development.ipynb
│   └── analysis.ipynb
├── scripts/              # Utility scripts
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
├── config/               # Configuration files
│   ├── logging.yaml
│   ├── database.yaml
│   └── models.yaml
└── docker/               # Docker configuration (future)
    ├── Dockerfile
    ├── docker-compose.yml
    └── .dockerignore
```

## Migration Strategy

### Phase 1: Basic Restructuring (Current)
1. Create `src/` directory
2. Move existing Python files into appropriate subdirectories
3. Add `__init__.py` files
4. Update imports

### Phase 2: Backend Development
1. Add `api/` directory with FastAPI structure
2. Create `database/` directory for Supabase integration
3. Add `utils/` for common functionality
4. Implement proper configuration management

### Phase 3: Frontend Development
1. Create `frontend/` directory
2. Set up React + Vite + Tailwind
3. Add build and deployment scripts

### Phase 4: Production Readiness
1. Add CI/CD workflows in `.github/`
2. Create Docker configuration
3. Add comprehensive documentation
4. Implement proper testing structure

## File Naming Conventions

- **Python files**: snake_case (e.g., `reddit_scraper.py`)
- **Directories**: snake_case (e.g., `data_processing/`)
- **Classes**: PascalCase (e.g., `RedditScraper`)
- **Functions/Variables**: snake_case (e.g., `extract_credit_score`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)

## Import Structure

```python
# Absolute imports (preferred)
from src.scrapers.reddit_scraper import RedditScraper
from src.extractors.llm_extractor import LLMExtractor
from src.utils.config import get_config

# Relative imports (within same package)
from .base_scraper import BaseScraper
from ..utils.helpers import clean_text
```

## Environment Management

- `.env`: Local development (gitignored)
- `.env.example`: Template for required variables
- `config/`: Configuration files for different environments
- `requirements.txt`: Production dependencies
- `requirements-dev.txt`: Development dependencies

This structure balances professional development practices with the simplicity needed for personal project development. 
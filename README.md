# Open Card Preapproval Tool

A comprehensive credit card approval analysis tool that collects, extracts, and analyzes approval/denial data from multiple sources to understand approval factors and predict approval likelihood.

## Project Vision

**Goal**: Build a comprehensive tool that analyzes credit card approval data from multiple sources (Reddit, forums, review sites, etc.) to understand what factors lead to approvals vs denials, ultimately creating a prediction model for credit card approval likelihood across different cards and issuers.

**Use Case**: Users can input their financial profile (income, credit score, age, etc.) and get predictions on approval likelihood for different credit cards based on aggregated real user experiences from multiple platforms.

**Data Sources Strategy**: Start with Reddit as a POC, then expand to other sources like:
- Reddit (r/CreditCards, r/personalfinance, etc.)
- Credit card forums (MyFICO, CreditBoards, etc.)
- Review sites (Credit Karma, NerdWallet, etc.)
- Social media platforms (Twitter, Facebook groups)
- Credit card application threads
- Bank-specific forums and communities

## Current POC (Development Phase)

### What We Have Now
- **Reddit Scraping**: Collects Freedom Unlimited approval/denial posts from r/CreditCards (POC starting point)
- **LLM Data Extraction**: Uses Ollama + Mistral to extract structured data from posts
- **Data Processing**: Filters and cleans extracted data for analysis
- **Basic Analysis**: Jupyter notebook for initial data exploration

### Current Tech Stack
- **Scraping**: PRAW (Reddit API) - POC source
- **LLM**: Ollama + Mistral (local)
- **Data Processing**: Python + pandas
- **Storage**: CSV files
- **Analysis**: Jupyter notebooks

### Key Files
- `scraper.py` - Reddit data collection for Freedom Unlimited posts (POC)
- `llm_extractor.py` - LLM-powered extraction of income, credit score, age, etc.
- `extract_fields.py` - Rule-based field extraction
- `llm_filter.py` - LLM-based content filtering
- `strict_filter.py` - Strict content filtering
- `data_cleaning.ipynb` - Data analysis and visualization
- `requirements.txt` - Python dependencies

### Current Data Schema
Extracted fields from Reddit posts:
- Income (numeric)
- Credit Score (3-digit number)
- Age (years)
- Credit History Length (months/years)
- Hard Pulls Count (recent inquiries)
- Approval Status (approved/denied)
- Post Title & Body
- Source Platform (Reddit for now)
- Card Name (Freedom Unlimited for now)

## Future Architecture

### Development Stack (Local)
| Layer | Tool(s) | Purpose |
|-------|---------|---------|
| Model Inference | Ollama + Mistral/LLaMA | Local LLM for classifying posts from multiple sources |
| ML Experiments | Weights & Biases | Track models, metrics, and outputs |
| ML Code | Python, pandas, scikit-learn | Data prep, modeling, feature engineering |
| Backend API | FastAPI (local) | Serve predictions / data via API |
| Database | Supabase | Store extracted data from multiple sources + results |
| Frontend | React + Vite + Tailwind | UI for display, search, visualizations |
| Hosting (Frontend) | Netlify | Deploy dev UI |
| Version Control | GitHub | Track all source code |

### Production Stack (Deployable)
| Layer | Tool(s) | Purpose |
|-------|---------|---------|
| Model Inference | Ollama (self-host) or OpenAI API | Serve LLM remotely (via API) |
| ML Experiments | Weights & Biases | Keep using to track new model versions |
| Model Serving | FastAPI + Render/Railway | Deployed backend API |
| Database | Supabase (hosted) | Scalable Postgres DB + auth |
| Frontend | React + Tailwind (on Netlify) | Public user interface |
| CI/CD | GitHub Actions | Auto-deploy frontend/backend |
| (Optional) | LangChain | For scalable pipelines with LLMs |

## Development Roadmap

### Phase 1: POC Enhancement (Current)
- [x] Basic Reddit scraping (Freedom Unlimited)
- [x] LLM data extraction
- [x] Data cleaning pipeline
- [ ] Expand to multiple credit cards on Reddit
- [ ] Improve extraction accuracy
- [ ] Add data validation
- [ ] Create modular scraper architecture

### Phase 2: Multi-Source Data Collection
- [ ] Design unified data collection framework
- [ ] Add forum scrapers (MyFICO, CreditBoards)
- [ ] Add review site scrapers (Credit Karma, NerdWallet)
- [ ] Add social media scrapers (Twitter, Facebook groups)
- [ ] Implement source-specific data cleaning
- [ ] Create data source validation and quality checks

### Phase 3: Backend Development
- [ ] Structure code into modules (scrapers/, extractors/, models/)
- [ ] Create FastAPI backend with endpoints
- [ ] Set up Supabase database schema for multi-source data
- [ ] Add authentication
- [ ] Create unified data ingestion pipeline

### Phase 4: ML Pipeline
- [ ] Integrate Weights & Biases for experiment tracking
- [ ] Build feature engineering pipeline for multi-source data
- [ ] Train initial prediction models
- [ ] Add model evaluation metrics
- [ ] Create model versioning system
- [ ] Implement source-specific model weights

### Phase 5: Frontend Development
- [ ] Create React + Vite + Tailwind frontend
- [ ] Build data visualization dashboard
- [ ] Add user input forms for predictions
- [ ] Create search and filter functionality
- [ ] Add source attribution and data quality indicators
- [ ] Add responsive design

### Phase 6: Production Deployment
- [ ] Set up CI/CD with GitHub Actions
- [ ] Deploy backend to Render/Railway
- [ ] Deploy frontend to Netlify
- [ ] Add monitoring and logging
- [ ] Performance optimization
- [ ] Implement rate limiting for scrapers

## Getting Started

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Reddit API credentials (for POC)

### Installation
```bash
# Clone repository
git clone https://github.com/jwilliams2023/Open-Card-Preapproval-Tool.git
cd Open-Card-Preapproval-Tool

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Reddit API credentials
```

### Environment Variables
Create a `.env` file with:
```
REDDIT_APP_ID=your_reddit_app_id
REDDIT_APP_SECRET=your_reddit_app_secret
REDDIT_APP_NAME=your_app_name
```

### Running the POC
```bash
# 1. Scrape Reddit data (POC)
python scraper.py

# 2. Extract structured data with LLM
python llm_extractor.py

# 3. Analyze data (Jupyter notebook)
jupyter notebook data_cleaning.ipynb
```

## Data Flow

1. **Multi-Source Scraping**: Various platforms → Raw data files
2. **Source-Specific Processing**: Raw data → Platform-specific structured data
3. **Unified Extraction**: Platform data → Standardized structured data (LLM)
4. **Cleaning**: Structured data → Clean dataset
5. **Analysis**: Clean data → Insights & visualizations
6. **Modeling**: Clean data → Prediction models
7. **API**: Models → Predictions via FastAPI
8. **Frontend**: API → User interface

## Key Features (Planned)

### For Users
- Input financial profile (income, credit score, age, etc.)
- Get approval likelihood predictions for different cards
- View historical approval data and trends from multiple sources
- Compare different credit cards across issuers
- Get personalized recommendations
- See data source attribution and quality metrics

### For Developers
- Multi-source data scraping pipeline
- Unified data processing framework
- ML model training and evaluation
- API for predictions and data access
- Comprehensive logging and monitoring
- Easy deployment and scaling
- Source-specific data quality monitoring

## Contributing

This is a personal project currently in POC phase. Future contributions welcome once the basic architecture is established.

## Notes for Future Development

- **Data Privacy**: Ensure all scraped data is anonymized and used responsibly
- **Rate Limiting**: Respect all platform API limits and implement proper delays
- **Legal Compliance**: Follow terms of service for all data sources
- **Model Accuracy**: Focus on interpretable models for credit decisions
- **Scalability**: Design for handling multiple sources and large datasets
- **User Experience**: Make the tool intuitive for non-technical users
- **Data Quality**: Implement source-specific quality metrics and validation

## Links

- **Repository**: https://github.com/jwilliams2023/Open-Card-Preapproval-Tool
- **Current Focus**: POC data gathering from Reddit
- **Next Milestone**: Multi-source data collection framework

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup and documentation
- Comprehensive README with expanded multi-source vision
- Professional changelog structure
- Directory structure planning document

### Changed
- Removed emojis from README for professional appearance
- Restructured documentation for better clarity
- Updated project vision to include multiple data sources beyond Reddit
- Expanded roadmap to include multi-source data collection phase

## [0.1.0] - 2025-01-XX

### Added
- Basic Reddit scraping functionality for Freedom Unlimited posts (POC starting point)
- LLM-powered data extraction using Ollama + Mistral
- Rule-based field extraction for credit data
- Data cleaning and filtering pipelines
- Jupyter notebook for data analysis
- Requirements.txt with all dependencies
- Git repository setup with initial commit

### Technical Details
- **Scraper**: PRAW-based Reddit API integration (POC source)
- **LLM Integration**: Local Ollama server with Mistral model
- **Data Processing**: Pandas-based data manipulation
- **Storage**: CSV file format for data persistence
- **Analysis**: Jupyter notebook environment

### Project Vision
- **Current**: Reddit-only POC for Freedom Unlimited card
- **Future**: Multi-source data collection from forums, review sites, social media
- **Goal**: Comprehensive credit card approval prediction across all major cards and issuers

### Known Issues
- Limited to Freedom Unlimited card only
- Single data source (Reddit)
- Manual data extraction process
- No automated data validation
- Basic error handling

### Future Enhancements
- Expand to multiple credit cards
- Add multiple data sources (forums, review sites, social media)
- Implement automated data validation
- Add LLM-powered data verification and correction
- Add FastAPI backend
- Integrate Supabase database
- Create React frontend
- Add ML model training pipeline
- Implement source-specific data quality metrics 
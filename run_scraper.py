#!/usr/bin/env python3
"""
Main script to run the Reddit scraper
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scrapers.reddit_scraper import main

if __name__ == "__main__":
    main() 
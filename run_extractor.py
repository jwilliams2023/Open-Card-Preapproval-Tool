#!/usr/bin/env python3
"""
Main script to run the LLM extractor
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from extractors.llm_extractor import main

if __name__ == "__main__":
    main() 
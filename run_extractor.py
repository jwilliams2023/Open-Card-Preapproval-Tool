#!/usr/bin/env python3
"""
Main script to run data extraction pipeline
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from extractors.rule_extractor import main as run_rule_extractor
from extractors.llm_extractor import main as run_llm_extractor
from extractors.data_preparer import main as run_data_preparer

def main():
    """Run the complete extraction pipeline"""
    print("=== Reddit Data Extraction Pipeline ===")
    
    # Step 1: Rule-based extraction
    print("\n1. Running rule-based extraction...")
    run_rule_extractor()
    
    # Step 2: LLM-based extraction (optional)
    print("\n2. Running LLM-based extraction...")
    print("Note: This requires Ollama to be running with Mistral model")
    try:
        run_llm_extractor()
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        print("Make sure Ollama is running with Mistral model")
    
    # Step 3: Data preparation for ML
    print("\n3. Preparing data for machine learning...")
    run_data_preparer()
    
    print("\n=== Extraction Pipeline Complete ===")
    print("Check data/processed/ for output files")
    print("- rule_extracted_data_*.csv: Basic extracted fields")
    print("- llm_extracted_data_*.csv: LLM-enhanced data (if available)")
    print("- model_ready_data_*.csv: Final ML-ready dataset")

if __name__ == "__main__":
    main() 
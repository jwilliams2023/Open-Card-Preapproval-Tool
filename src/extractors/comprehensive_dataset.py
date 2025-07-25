import pandas as pd
import re
import numpy as np
from datetime import datetime
import os

def extract_approval_status(text):
    """Extract approval status from text"""
    text_lower = str(text).lower()
    
    # Approval indicators
    approval_keywords = [
        'approved', 'approval', 'got approved', 'was approved', 'got it',
        'accepted', 'successful', 'got the card', 'received the card'
    ]
    
    # Denial indicators
    denial_keywords = [
        'denied', 'denial', 'rejected', 'rejection', 'got denied', 'was denied',
        'declined', 'not approved', 'didn\'t get approved'
    ]
    
    # Check for approval
    for keyword in approval_keywords:
        if keyword in text_lower:
            return 'approved'
    
    # Check for denial
    for keyword in denial_keywords:
        if keyword in text_lower:
            return 'denied'
    
    return 'unknown'

def extract_features_from_text(text):
    """Extract features from text content"""
    text_lower = str(text).lower()
    
    features = {}
    
    # Student indicators
    features['is_student'] = any(word in text_lower for word in ['student', 'college', 'university', 'school'])
    
    # First card indicators
    features['is_first_card'] = any(word in text_lower for word in ['first card', 'first credit card', 'first cc', 'beginner'])
    
    # Chase relationship indicators
    features['has_chase_account'] = any(word in text_lower for word in ['chase account', 'chase banking', 'chase customer'])
    
    # Income indicators
    features['mentions_income'] = any(word in text_lower for word in ['income', 'salary', 'earn', 'make'])
    
    # Credit score indicators
    features['mentions_credit_score'] = any(word in text_lower for word in ['credit score', 'fico', 'score'])
    
    # Length of text (proxy for detail level)
    features['text_length'] = len(text)
    
    return features

def create_comprehensive_dataset(input_file, output_file=None):
    """Create comprehensive dataset with original posts and all extracted features"""
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Original shape: {df.shape}")
    
    # Step 1: Extract approval status
    print("Extracting approval status...")
    df['approval_status'] = df.apply(lambda row: extract_approval_status(f"{row['Title']} {row['Body']}"), axis=1)
    
    # Step 2: Extract text features
    print("Extracting text features...")
    text_features = df.apply(lambda row: extract_features_from_text(f"{row['Title']} {row['Body']}"), axis=1)
    text_features_df = pd.DataFrame(text_features.tolist())
    df = pd.concat([df, text_features_df], axis=1)
    
    # Step 3: Clean and convert extracted fields
    print("Cleaning extracted fields...")
    
    # Clean income (remove $ and commas, convert to numeric)
    df['income_clean'] = pd.to_numeric(df['Extracted Income'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    
    # Clean credit score (convert to numeric)
    df['credit_score_clean'] = pd.to_numeric(df['Extracted Credit Score'], errors='coerce')
    
    # Clean approval amount (remove $ and commas, convert to numeric)
    df['approval_amount_clean'] = pd.to_numeric(df['Extracted Approval Amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    
    # Step 4: Create target variable
    print("Creating target variable...")
    df['target'] = (df['approval_status'] == 'approved').astype(int)
    
    # Step 5: Create comprehensive dataset with all information
    print("Creating comprehensive dataset...")
    
    # Select columns for comprehensive view
    comprehensive_columns = [
        # Original post data
        'Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At',
        
        # Extracted fields (raw)
        'Extracted Income', 'Extracted Credit Score', 'Extracted Approval Amount',
        
        # Cleaned numeric fields
        'income_clean', 'credit_score_clean', 'approval_amount_clean',
        
        # Approval classification
        'approval_status', 'target',
        
        # Text features
        'is_student', 'is_first_card', 'has_chase_account', 
        'mentions_income', 'mentions_credit_score', 'text_length'
    ]
    
    # Create comprehensive dataset
    comprehensive_df = df[comprehensive_columns].copy()
    
    # Fill missing values for display
    comprehensive_df['income_clean'] = comprehensive_df['income_clean'].fillna('Not extracted')
    comprehensive_df['credit_score_clean'] = comprehensive_df['credit_score_clean'].fillna('Not extracted')
    comprehensive_df['approval_amount_clean'] = comprehensive_df['approval_amount_clean'].fillna('Not extracted')
    
    # Convert boolean columns to Yes/No for readability
    boolean_cols = ['is_student', 'is_first_card', 'has_chase_account', 'mentions_income', 'mentions_credit_score']
    for col in boolean_cols:
        comprehensive_df[col] = comprehensive_df[col].map({True: 'Yes', False: 'No'})
    
    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/processed/comprehensive_dataset_{timestamp}.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save comprehensive dataset
    comprehensive_df.to_csv(output_file, index=False)
    
    # Print summary
    print(f"\n=== Comprehensive Dataset Summary ===")
    print(f"Final shape: {comprehensive_df.shape}")
    print(f"Columns: {list(comprehensive_df.columns)}")
    print(f"Approval status distribution:")
    print(comprehensive_df['approval_status'].value_counts())
    print(f"Target distribution:")
    print(comprehensive_df['target'].value_counts())
    print(f"\nSample of extracted data:")
    print(comprehensive_df[['Title', 'approval_status', 'income_clean', 'credit_score_clean', 'is_student', 'is_first_card']].head(5))
    print(f"\nSaved to: {output_file}")
    
    return output_file


# =============================================================================
# FUTURE ENHANCEMENT: LLM-Powered Data Verification & Quality Control
# =============================================================================
# 
# This section contains commented-out code for future LLM verification features.
# In a production environment, this would be implemented as a separate module
# with proper error handling, logging, and configuration management.
#
# TODO: Implement when LLM infrastructure is production-ready
# TODO: Add unit tests for verification functions
# TODO: Create configuration file for verification parameters
# TODO: Add monitoring and alerting for verification failures
# =============================================================================
#
# FUTURE FUNCTION: verify_extractions_with_llm(df, llm_client=None)
# Use LLM to verify and improve extracted data quality.
# This function would:
# 1. Review each row's extracted fields for accuracy
# 2. Suggest missing data points that could be extracted
# 3. Provide confidence scores for each extraction
# 4. Flag potential errors or inconsistencies
# 5. Generate quality metrics for the dataset
#
# FUTURE FUNCTION: generate_quality_report(df)
# Generate comprehensive quality report for the dataset.
# This would include:
# - Extraction success rates
# - Confidence score distributions
# - Data completeness metrics
# - Quality trends over time
# - Recommendations for improvement
#
# FUTURE FUNCTION: create_verified_dataset(input_file, output_file=None, enable_llm_verification=False)
# Create dataset with optional LLM verification.
# This is the main function that would be called in production.
# It orchestrates the entire data preparation and verification pipeline.
#
# Example usage (future):
# df = create_verified_dataset('input.csv', enable_llm_verification=True)
# This would run the current comprehensive dataset creation + LLM verification
# =============================================================================


def main():
    """Main function to create comprehensive dataset"""
    # Find the most recent processed data file
    processed_files = [f for f in os.listdir('data/processed') if f.endswith('.csv') and 'rule_extracted' in f]
    if not processed_files:
        print("No rule-extracted data files found in data/processed/")
        print("Run rule_extractor.py first to create processed data")
        return
    
    # Use the most recent file
    latest_file = sorted(processed_files)[-1]
    input_file = f'data/processed/{latest_file}'
    
    print(f"Creating comprehensive dataset from {input_file}...")
    output_file = create_comprehensive_dataset(input_file)
    print(f"Comprehensive dataset created: {output_file}")

if __name__ == "__main__":
    main() 
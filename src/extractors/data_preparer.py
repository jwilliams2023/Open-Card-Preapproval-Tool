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

def prepare_model_data(input_file, output_file=None):
    """Prepare extracted data for machine learning"""
    
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
    
    # Step 5: Filter for usable data
    print("Filtering for usable data...")
    # Keep only rows with known approval status and at least some extracted data
    usable_df = df[
        (df['approval_status'] != 'unknown') &
        (
            (df['income_clean'].notna()) |
            (df['credit_score_clean'].notna()) |
            (df['approval_amount_clean'].notna())
        )
    ].copy()
    
    print(f"Usable data shape: {usable_df.shape}")
    
    # Step 6: Create final model-ready features
    print("Creating final features...")
    
    # Select and rename features for ML
    model_features = [
        'income_clean',
        'credit_score_clean', 
        'approval_amount_clean',
        'is_student',
        'is_first_card',
        'has_chase_account',
        'mentions_income',
        'mentions_credit_score',
        'text_length',
        'target'
    ]
    
    # Create final dataset
    final_df = usable_df[model_features].copy()
    
    # Fill missing values with appropriate defaults
    final_df['income_clean'] = final_df['income_clean'].fillna(final_df['income_clean'].median())
    final_df['credit_score_clean'] = final_df['credit_score_clean'].fillna(final_df['credit_score_clean'].median())
    final_df['approval_amount_clean'] = final_df['approval_amount_clean'].fillna(0)  # 0 if no approval amount
    
    # Convert boolean columns to int
    boolean_cols = ['is_student', 'is_first_card', 'has_chase_account', 'mentions_income', 'mentions_credit_score']
    for col in boolean_cols:
        final_df[col] = final_df[col].astype(int)
    
    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/processed/model_ready_data_{timestamp}.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save model-ready data
    final_df.to_csv(output_file, index=False)
    
    # Print summary
    print(f"\n=== Model Ready Data Summary ===")
    print(f"Final shape: {final_df.shape}")
    print(f"Features: {list(final_df.columns)}")
    print(f"Target distribution:")
    print(final_df['target'].value_counts())
    print(f"\nMissing values:")
    print(final_df.isnull().sum())
    print(f"\nData types:")
    print(final_df.dtypes)
    print(f"\nSaved to: {output_file}")
    
    return output_file

def main():
    """Main function to run data preparation"""
    # Find the most recent processed data file
    processed_files = [f for f in os.listdir('data/processed') if f.endswith('.csv') and 'rule_extracted' in f]
    if not processed_files:
        print("No rule-extracted data files found in data/processed/")
        print("Run rule_extractor.py first to create processed data")
        return
    
    # Use the most recent file
    latest_file = sorted(processed_files)[-1]
    input_file = f'data/processed/{latest_file}'
    
    print(f"Preparing model data from {input_file}...")
    output_file = prepare_model_data(input_file)
    print(f"Model preparation completed: {output_file}")

if __name__ == "__main__":
    main() 
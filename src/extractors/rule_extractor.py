import pandas as pd
import re
import os
from datetime import datetime

def extract_fields_from_csv(input_file, output_file=None):
    """Extract structured fields from Reddit posts using regex patterns"""
    
    # Load dataset
    df = pd.read_csv(input_file)
    
    # Define regex patterns
    income_pattern = re.compile(r'income.*?(\$?\d{2,3}[,]?\d{3})', re.IGNORECASE)
    score_pattern = re.compile(r'(credit score|fico).*?(\d{3})', re.IGNORECASE)
    approval_pattern = re.compile(r'(approved for|starting limit|credit limit of|limit of)\s*\$?(\d{2,3}[,]?\d{3,4})', re.IGNORECASE)

    # Prepare new columns
    df['Extracted Income'] = ''
    df['Extracted Credit Score'] = ''
    df['Extracted Approval Amount'] = ''

    # Extraction loop
    for idx, row in df.iterrows():
        combined_text = f"{str(row['Title'])} {str(row['Body'])}"

        income_match = income_pattern.search(combined_text)
        score_match = score_pattern.search(combined_text)
        approval_match = approval_pattern.search(combined_text)

        if income_match:
            df.at[idx, 'Extracted Income'] = income_match.group(1).replace(',', '').replace('$', '')
        
        if score_match:
            df.at[idx, 'Extracted Credit Score'] = score_match.group(2)
        
        if approval_match:
            df.at[idx, 'Extracted Approval Amount'] = approval_match.group(2).replace(',', '')

    # Keep only posts where at least one field was found
    final_df = df[
        (df['Extracted Income'] != '') |
        (df['Extracted Credit Score'] != '') |
        (df['Extracted Approval Amount'] != '')
    ]

    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/processed/rule_extracted_data_{timestamp}.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save final structured dataset
    final_df.to_csv(output_file, index=False)

    print(f"Saved {len(final_df)} posts with at least one extracted field to {output_file}")
    return output_file

def main():
    """Main function to run the rule extractor"""
    # Find the most recent raw data file
    raw_files = [f for f in os.listdir('data/raw') if f.endswith('.csv')]
    if not raw_files:
        print("No raw data files found in data/raw/")
        return
    
    # Use the most recent file
    latest_file = sorted(raw_files)[-1]
    input_file = f'data/raw/{latest_file}'
    
    print(f"Processing {input_file}...")
    output_file = extract_fields_from_csv(input_file)
    print(f"Rule extraction completed: {output_file}")

if __name__ == "__main__":
    main()

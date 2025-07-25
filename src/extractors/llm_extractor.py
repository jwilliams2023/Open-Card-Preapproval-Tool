import pandas as pd
import requests
import re
import time
import os
from datetime import datetime

def extract_with_llm(input_file, output_file=None):
    """Extract structured data from Reddit posts using LLM"""
    
    df = pd.read_csv(input_file)

    # Track how many were filled by LLM
    llm_income_fills = 0
    llm_score_fills = 0
    llm_age_fills = 0
    llm_history_fills = 0
    llm_pulls_fills = 0

    # Add new columns if missing
    for col in ['Extracted Age', 'Extracted Credit History Length', 'Extracted Hard Pulls']:
        if col not in df.columns:
            df[col] = ''

    for idx, row in df.iterrows():
        missing_fields = []

        if pd.isna(row['Extracted Income']):
            missing_fields.append('income')
        if pd.isna(row['Extracted Credit Score']):
            missing_fields.append('credit score')
        if pd.isna(row['Extracted Age']):
            missing_fields.append('age')
        if pd.isna(row['Extracted Credit History Length']):
            missing_fields.append('credit history length')
        if pd.isna(row['Extracted Hard Pulls']):
            missing_fields.append('hard pulls count')

        if not missing_fields:
            continue  # Skip if nothing is missing

        prompt = f"""You are extracting structured data from Reddit posts.

Post Title: "{row['Title']}"
Post Body: "{row['Body']}"

Extract the following fields if present:
- Income (numeric, no symbols)
- Credit Score (3-digit number)
- Age (numeric, in years)
- Credit History Length (in months or years, return numeric only)
- Hard Pulls Count (numeric, count of recent hard inquiries)

If a field is missing, leave it blank.

Respond ONLY in this exact format:
Income: [amount or blank]
Credit Score: [score or blank]
Age: [age or blank]
Credit History Length: [length or blank]
Hard Pulls Count: [count or blank]
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt}
        )

        output = response.text.strip().lower()
        print(f"[{idx + 1}/{len(df)}] Model output:\n{output}\n")

        # Extract numbers using regex from LLM output
        income_match = re.search(r'income:\s*(\d+)', output)
        score_match = re.search(r'credit score:\s*(\d+)', output)
        age_match = re.search(r'age:\s*(\d+)', output)
        history_match = re.search(r'credit history length:\s*(\d+)', output)
        pulls_match = re.search(r'hard pulls count:\s*(\d+)', output)

        if income_match and pd.isna(row['Extracted Income']):
            df.at[idx, 'Extracted Income'] = income_match.group(1)
            llm_income_fills += 1
        if score_match and pd.isna(row['Extracted Credit Score']):
            df.at[idx, 'Extracted Credit Score'] = score_match.group(1)
            llm_score_fills += 1
        if age_match and pd.isna(row['Extracted Age']):
            df.at[idx, 'Extracted Age'] = age_match.group(1)
            llm_age_fills += 1
        if history_match and pd.isna(row['Extracted Credit History Length']):
            df.at[idx, 'Extracted Credit History Length'] = history_match.group(1)
            llm_history_fills += 1
        if pulls_match and pd.isna(row['Extracted Hard Pulls']):
            df.at[idx, 'Extracted Hard Pulls'] = pulls_match.group(1)
            llm_pulls_fills += 1

        time.sleep(0.2)  # Avoid hammering Ollama

    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/processed/llm_extracted_data_{timestamp}.csv'
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save updated dataset
    df.to_csv(output_file, index=False)

    print(f"LLM filled: {llm_income_fills} income, {llm_score_fills} scores, {llm_age_fills} ages, {llm_history_fills} histories, {llm_pulls_fills} hard pulls")
    print(f"Updated dataset saved to {output_file}")
    return output_file

def main():
    """Main function to run the LLM extractor"""
    # Find the most recent processed data file
    processed_files = [f for f in os.listdir('data/processed') if f.endswith('.csv')]
    if not processed_files:
        print("No processed data files found in data/processed/")
        print("Run rule_extractor.py first to create processed data")
        return
    
    # Use the most recent file
    latest_file = sorted(processed_files)[-1]
    input_file = f'data/processed/{latest_file}'
    
    print(f"Processing {input_file} with LLM...")
    output_file = extract_with_llm(input_file)
    print(f"LLM extraction completed: {output_file}")

if __name__ == "__main__":
    main()

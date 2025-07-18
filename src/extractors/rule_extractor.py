import pandas as pd
import re

# Load strict filtered dataset
df = pd.read_csv('strict_filtered_data.csv')

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

# Save final structured dataset
final_df.to_csv('extracted_data.csv', index=False)

print(f"Saved {len(final_df)} posts with at least one extracted field to extracted_data.csv")

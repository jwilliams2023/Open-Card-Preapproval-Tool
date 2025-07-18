import pandas as pd

# Load your LLM-filtered dataset
df = pd.read_csv('filtered_data.csv')

# Keywords or patterns likely indicating useful datapoints
strict_keywords = [
    'income',
    'credit score',
    'fico',
    'approved for',
    'approval amount',
    'limit of',
    'starting limit',
    'denied with',
    'denial with',
    'credit limit',
    'approved with',
    'denied due to',
]

filtered_rows = []

for _, row in df.iterrows():
    combined_text = f"{str(row['Title']).lower()} {str(row['Body']).lower()}"
    
    if any(keyword in combined_text for keyword in strict_keywords):
        filtered_rows.append(row)

# Save the stricter filtered dataset
strict_df = pd.DataFrame(filtered_rows)
strict_df.to_csv('strict_filtered_data.csv', index=False)

print(f"Saved {len(strict_df)} high-quality posts to strict_filtered_data.csv")

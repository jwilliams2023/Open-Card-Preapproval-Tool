import requests
import pandas as pd
import time

df = pd.read_csv('freedom_unlimited_approval_data.csv')
filtered_rows = []

for idx, row in df.iterrows():
    title = row['Title']
    body = row['Body']
    prompt = f"""You are classifying Reddit posts.

Post Title: "{title}"
Post Body: "{body}"

Does this post clearly describe a Chase Freedom Unlimited (CFU) approval or denial experience? Answer only YES or NO."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt}
    )

    output = response.text.strip().lower()

    print(f"[{idx + 1}/{len(df)}] Model output: {output}")

    if "yes" in output:
        filtered_rows.append(row)

    time.sleep(0.2)  # Optional: avoid hammering the API

filtered_df = pd.DataFrame(filtered_rows)
filtered_df.to_csv('filtered_data.csv', index=False)

print(f"Saved {len(filtered_rows)} relevant posts to filtered_data.csv")

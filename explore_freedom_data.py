"""
Freedom Cards Data Exploration
Copy these code blocks into VS Code notebook cells to explore the data
"""

# =============================================================================
# CELL 1: Setup and Imports
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

print("Freedom Cards Data Exploration")
print("=" * 50)

# =============================================================================
# CELL 2: Load Data and Basic Stats
# =============================================================================
# Load the raw Freedom cards data
df = pd.read_csv('data/raw/freedom_cards_approval_data_20250718_185150.csv')

print(f"Total posts collected: {len(df):,}")
print(f"\nCard distribution:")
print(df['Card_Name'].value_counts())
print(f"\nData columns: {list(df.columns)}")
print(f"\nDate range: {df['Scraped_At'].min()} to {df['Scraped_At'].max()}")

# =============================================================================
# CELL 3: Data Quality Check
# =============================================================================
print("=== DATA QUALITY CHECK ===")
print(f"Missing values per column:")
print(df.isnull().sum())

print(f"\nText length statistics:")
df['title_length'] = df['Title'].str.len()
df['body_length'] = df['Body'].str.len()
print(f"Title length - Mean: {df['title_length'].mean():.1f}, Median: {df['title_length'].median():.1f}")
print(f"Body length - Mean: {df['body_length'].mean():.1f}, Median: {df['body_length'].median():.1f}")

# =============================================================================
# CELL 4: Freedom Unlimited vs Freedom Flex Comparison
# =============================================================================
print("=== FREEDOM UNLIMITED VS FREEDOM FLEX COMPARISON ===")

# Filter out generic Freedom posts
freedom_df = df[df['Card_Name'].isin(['Freedom Unlimited', 'Freedom Flex'])].copy()

print(f"\nPost counts:")
print(freedom_df['Card_Name'].value_counts())

print(f"\nText length comparison:")
print(freedom_df.groupby('Card_Name')[['title_length', 'body_length']].mean())

# =============================================================================
# CELL 5: Visualize Card Distribution
# =============================================================================
plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
card_counts = df['Card_Name'].value_counts()
plt.pie(card_counts.values, labels=card_counts.index, autopct='%1.1f%%')
plt.title('Distribution of Cards')

plt.subplot(1, 2, 2)
freedom_counts = freedom_df['Card_Name'].value_counts()
plt.bar(freedom_counts.index, freedom_counts.values, color=['#1f77b4', '#ff7f0e'])
plt.title('Freedom Unlimited vs Freedom Flex')
plt.ylabel('Number of Posts')

plt.tight_layout()
plt.show()

# =============================================================================
# CELL 6: Approval Status Analysis
# =============================================================================
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

# Apply to both title and body
freedom_df['approval_status'] = freedom_df.apply(
    lambda row: extract_approval_status(f"{row['Title']} {row['Body']}"), axis=1
)

print("=== APPROVAL STATUS ANALYSIS ===")
print(freedom_df.groupby(['Card_Name', 'approval_status']).size().unstack(fill_value=0))

# =============================================================================
# CELL 7: Approval Rate Visualization
# =============================================================================
approval_summary = freedom_df.groupby(['Card_Name', 'approval_status']).size().unstack(fill_value=0)
approval_summary['approval_rate'] = approval_summary['approved'] / (approval_summary['approved'] + approval_summary['denied'])

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
approval_summary[['approved', 'denied']].plot(kind='bar', stacked=True)
plt.title('Approval vs Denial Counts by Card')
plt.ylabel('Number of Posts')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
approval_summary['approval_rate'].plot(kind='bar', color=['#1f77b4', '#ff7f0e'])
plt.title('Approval Rate by Card')
plt.ylabel('Approval Rate')
plt.xticks(rotation=45)
plt.ylim(0, 1)

plt.tight_layout()
plt.show()

print(f"\nApproval rates:")
print(approval_summary['approval_rate'])

# =============================================================================
# CELL 8: Sample Posts Analysis
# =============================================================================
print("=== SAMPLE POSTS ANALYSIS ===")

for card in ['Freedom Unlimited', 'Freedom Flex']:
    print(f"\n--- {card} Sample Posts ---")
    card_posts = freedom_df[freedom_df['Card_Name'] == card].head(3)
    
    for idx, row in card_posts.iterrows():
        print(f"\nTitle: {row['Title']}")
        print(f"Status: {row['approval_status']}")
        print(f"Body preview: {row['Body'][:200]}...")
        print("-" * 80)

# =============================================================================
# CELL 9: Summary Statistics
# =============================================================================
print("=== SUMMARY STATISTICS ===")
print(f"\nTotal posts analyzed: {len(freedom_df):,}")
print(f"Freedom Unlimited posts: {len(freedom_df[freedom_df['Card_Name'] == 'Freedom Unlimited']):,}")
print(f"Freedom Flex posts: {len(freedom_df[freedom_df['Card_Name'] == 'Freedom Flex']):,}")

print(f"\nApproval status breakdown:")
print(freedom_df['approval_status'].value_counts())

print(f"\nApproval rates by card:")
for card in ['Freedom Unlimited', 'Freedom Flex']:
    card_data = freedom_df[freedom_df['Card_Name'] == card]
    approved = len(card_data[card_data['approval_status'] == 'approved'])
    denied = len(card_data[card_data['approval_status'] == 'denied'])
    total = approved + denied
    rate = approved / total if total > 0 else 0
    print(f"  {card}: {approved}/{total} ({rate:.1%})")

print("\n" + "="*50)
print("Copy these code blocks into VS Code notebook cells!")
print("Each section marked with 'CELL X:' should be a separate cell.") 
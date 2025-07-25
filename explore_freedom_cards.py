# Cell 1: Import libraries and load data
import pandas as pd

# Load the raw Freedom cards data
df = pd.read_csv('data/raw/freedom_cards_approval_data_20250718_185150.csv')

print(f"Total posts collected: {len(df):,}")
print(f"\nCard distribution:")
print(df['Card_Name'].value_counts())
print(f"\nData columns: {list(df.columns)}")

# Cell 2: Data quality check
print("\nDATA QUALITY CHECK")
print(f"Missing values per column:")
print(df.isnull().sum())

print(f"\nText length statistics:")
df['title_length'] = df['Title'].str.len()
df['body_length'] = df['Body'].str.len()
print(f"Title length - Mean: {df['title_length'].mean():.1f}, Median: {df['title_length'].median():.1f}")
print(f"Body length - Mean: {df['body_length'].mean():.1f}, Median: {df['body_length'].median():.1f}")

# Cell 3: Compare Freedom Unlimited vs Freedom Flex
print("\nFREEDOM UNLIMITED VS FREEDOM FLEX COMPARISON")
freedom_df = df[df['Card_Name'].isin(['Freedom Unlimited', 'Freedom Flex'])].copy()

print(f"\nPost counts:")
print(freedom_df['Card_Name'].value_counts())

print(f"\nText length comparison:")
print(freedom_df.groupby('Card_Name')[['title_length', 'body_length']].mean())

# Cell 4: Approval status analysis
def extract_approval_status(text):
    text_lower = str(text).lower()
    
    approval_keywords = ['approved', 'approval', 'got approved', 'was approved', 'got it', 'accepted', 'successful', 'got the card', 'received the card']
    denial_keywords = ['denied', 'denial', 'rejected', 'rejection', 'got denied', 'was denied', 'declined', 'not approved', 'didn\'t get approved']
    
    for keyword in approval_keywords:
        if keyword in text_lower:
            return 'approved'
    
    for keyword in denial_keywords:
        if keyword in text_lower:
            return 'denied'
    
    return 'unknown'

freedom_df['approval_status'] = freedom_df.apply(lambda row: extract_approval_status(f"{row['Title']} {row['Body']}"), axis=1)

print("\nAPPROVAL STATUS ANALYSIS")
print(freedom_df.groupby(['Card_Name', 'approval_status']).size().unstack(fill_value=0))

# Cell 5: Summary statistics
print("\nSUMMARY STATISTICS")
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

# Cell 6: Sample posts
print("\nSAMPLE POSTS")
for card in ['Freedom Unlimited', 'Freedom Flex']:
    print(f"\n{card} Sample Posts")
    card_posts = freedom_df[freedom_df['Card_Name'] == card].head(2)
    
    for idx, row in card_posts.iterrows():
        print(f"\nTitle: {row['Title']}")
        print(f"Status: {row['approval_status']}")
        print(f"Body preview: {row['Body'][:150]}...")
        print("-" * 60) 
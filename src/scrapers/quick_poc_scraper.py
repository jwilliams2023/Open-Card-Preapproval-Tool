import praw
import csv
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

def check_existing_posts():
    """Check what posts we already have to avoid duplicates"""
    existing_urls = set()
    
    # Check all existing CSV files in data/raw
    if os.path.exists('data/raw'):
        for filename in os.listdir('data/raw'):
            if filename.endswith('.csv'):
                try:
                    df = pd.read_csv(f'data/raw/{filename}')
                    if 'URL' in df.columns:
                        existing_urls.update(df['URL'].tolist())
                except:
                    continue
    
    return existing_urls

def scrape_quick_poc_freedom_cards():
    """Quick POC scraper for Freedom Unlimited and Freedom Flex with tighter filtering"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Search all relevant subreddits for Freedom cards
    subreddits = ['CreditCards', 'Chase', 'churning', 'personalfinance']

    # Focused search phrases for POC
    search_phrases = [
        # Freedom Unlimited - specific approval/denial/preapproval
        '"Freedom Unlimited" approved',
        '"Freedom Unlimited" denied',
        '"Freedom Unlimited" preapproved',
        '"Freedom Unlimited" pre-approval',
        'CFU approved',
        'CFU denied',
        'CFU preapproved',
        
        # Freedom Flex - specific approval/denial/preapproval
        '"Freedom Flex" approved',
        '"Freedom Flex" denied',
        '"Freedom Flex" preapproved',
        '"Freedom Flex" pre-approval',
        'CFF approved',
        'CFF denied',
        'CFF preapproved',
        
        # Generic but specific
        'Chase Freedom approved',
        'Chase Freedom denied',
        'Chase Freedom preapproved'
    ]

    existing_urls = check_existing_posts()
    seen_post_ids = set()
    
    # Create data/raw directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/raw/poc_freedom_cards_{timestamp}.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At'])

        total_posts = 0
        max_posts = 200  # Limit for POC
        
        for subreddit_name in subreddits:
            if total_posts >= max_posts:
                break
                
            print(f"\nSearching subreddit: r/{subreddit_name}")
            subreddit = reddit.subreddit(subreddit_name)
            
            for phrase in search_phrases:
                if total_posts >= max_posts:
                    break
                    
                print(f"  Searching for: {phrase}")
                
                # Only search 'new' for POC to get recent posts
                try:
                    for post in subreddit.search(phrase, sort='new', limit=50):  # Reduced limit
                        if post.id in seen_post_ids or post.url in existing_urls:
                            continue
                        seen_post_ids.add(post.id)

                        title_lower = post.title.lower()
                        body_lower = post.selftext.lower()
                        combined_text = f"{title_lower} {body_lower}"

                        # Comprehensive card detection logic
                        card_detected = None
                        
                        # Check for Freedom Unlimited variations
                        freedom_unlimited_terms = [
                            'freedom unlimited', 'cfu', 'chase freedom unlimited',
                            'freedom unlimited card', 'cfu card'
                        ]
                        
                        # Check for Freedom Flex variations  
                        freedom_flex_terms = [
                            'freedom flex', 'cff', 'chase freedom flex',
                            'freedom flex card', 'cff card'
                        ]
                        
                        # Check for Freedom cards (exclude premium cards)
                        premium_exclusions = ['sapphire', 'preferred', 'reserve', 'csr', 'csp', 'ink', 'business']
                        
                        if not any(exclusion in combined_text for exclusion in premium_exclusions):
                            # Check Freedom Unlimited first
                            if any(term in combined_text for term in freedom_unlimited_terms):
                                card_detected = 'Freedom Unlimited'
                            # Check Freedom Flex if Unlimited not found
                            elif any(term in combined_text for term in freedom_flex_terms):
                                card_detected = 'Freedom Flex'
                            # Check generic Freedom only if no specific card mentioned
                            elif 'freedom' in combined_text:
                                if not any(term in combined_text for term in freedom_unlimited_terms + freedom_flex_terms):
                                    card_detected = 'Freedom (Generic)'

                        # Tighter approval/denial/preapproval detection
                        outcome_keywords = [
                            'approved', 'denied', 'preapproved', 'pre-approval', 'pre approval',
                            'rejected', 'rejection', 'got approved', 'got denied',
                            'instant approval', 'application approved', 'application denied'
                        ]

                        # Must have both card mention AND outcome keywords
                        relevant = False
                        if card_detected:
                            # Check if outcome keywords are present
                            if any(kw in combined_text for kw in outcome_keywords):
                                # Additional quality check: must have substantial content or clear outcome
                                if len(post.selftext) > 50 or any(kw in title_lower for kw in outcome_keywords):
                                    relevant = True

                        if relevant and card_detected:
                            writer.writerow([
                                post.title, 
                                post.url, 
                                post.selftext,
                                f'Reddit-{subreddit_name}',
                                card_detected,
                                datetime.now().isoformat()
                            ])
                            total_posts += 1
                            print(f"    Saved post: {post.title[:50]}... ({card_detected})")
                            
                            if total_posts >= max_posts:
                                break
                
                except Exception as e:
                    print(f"    Error searching {phrase} in {subreddit_name}: {e}")
                    continue

    print(f"\nQuick POC scraping completed!")
    print(f"Total posts collected: {total_posts}")
    print(f"Results saved to: {filename}")
    return filename

def main():
    """Main function to run the quick POC scraper"""
    print("Starting Quick POC Reddit scraper for Freedom Unlimited and Freedom Flex...")
    print("Limited to 200 posts for quick testing...")
    filename = scrape_quick_poc_freedom_cards()
    print(f"Quick POC scraping completed. Data saved to: {filename}")

if __name__ == "__main__":
    main() 
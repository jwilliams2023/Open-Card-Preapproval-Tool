import praw
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

def scrape_enhanced_freedom_cards_posts():
    """Enhanced scraper for Freedom Unlimited and Freedom Flex approval/denial posts from multiple Reddit subreddits"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Multiple subreddits to search
    subreddits = [
        'CreditCards',
        'churning', 
        'personalfinance',
        'Chase'
    ]

    # Enhanced search phrases specifically for Freedom Unlimited and Freedom Flex
    search_phrases = [
        # Freedom Unlimited specific
        '"Freedom Unlimited" approved',
        '"Freedom Unlimited" denied', 
        '"Freedom Unlimited" approval',
        '"Freedom Unlimited" rejection',
        '"Freedom Unlimited" instant approval',
        '"Freedom Unlimited" got approved',
        '"Freedom Unlimited" got denied',
        'CFU approved',
        'CFU denied',
        'CFU approval',
        'CFU rejection',
        'CFU instant approval',
        'Chase Freedom Unlimited approved',
        'Chase Freedom Unlimited denied',
        
        # Freedom Flex specific
        '"Freedom Flex" approved',
        '"Freedom Flex" denied',
        '"Freedom Flex" approval', 
        '"Freedom Flex" rejection',
        '"Freedom Flex" instant approval',
        '"Freedom Flex" got approved',
        '"Freedom Flex" got denied',
        'CFF approved',
        'CFF denied',
        'CFF approval',
        'CFF rejection',
        'CFF instant approval',
        'Chase Freedom Flex approved',
        'Chase Freedom Flex denied',
        
        # Generic Freedom searches (will be filtered later)
        'Chase Freedom approved',
        'Chase Freedom denied',
        'Chase Freedom approval',
        'Chase Freedom rejection',
        'Freedom approved',
        'Freedom denied',
        'Freedom approval',
        'Freedom rejection',
        
        # Application specific terms
        'Freedom Unlimited application',
        'Freedom Flex application',
        'CFU application',
        'CFF application',
        'Chase Freedom application',
        
        # Status check terms
        'Freedom Unlimited status',
        'Freedom Flex status',
        'CFU status',
        'CFF status',
        
        # Credit limit terms
        'Freedom Unlimited credit limit',
        'Freedom Flex credit limit',
        'CFU credit limit',
        'CFF credit limit',
        
        # Income/credit score mentions
        'Freedom Unlimited income',
        'Freedom Flex income',
        'CFU income',
        'CFF income',
        'Freedom Unlimited credit score',
        'Freedom Flex credit score',
        'CFU credit score',
        'CFF credit score'
    ]

    seen_post_ids = set()
    
    # Create data/raw directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/raw/enhanced_freedom_cards_data_{timestamp}.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At'])

        total_posts = 0
        
        for subreddit_name in subreddits:
            print(f"\nSearching subreddit: r/{subreddit_name}")
            subreddit = reddit.subreddit(subreddit_name)
            
            for phrase in search_phrases:
                print(f"  Searching for: {phrase}")
                
                # Search with different sort methods to get more posts
                for sort_method in ['new', 'top', 'hot']:
                    try:
                        for post in subreddit.search(phrase, sort=sort_method, limit=500):
                            if post.id in seen_post_ids:
                                continue
                            seen_post_ids.add(post.id)

                            title_lower = post.title.lower()
                            body_lower = post.selftext.lower()
                            combined_text = f"{title_lower} {body_lower}"

                            # Enhanced card detection logic
                            card_detected = None
                            
                            # Check for Freedom Unlimited (exclude Sapphire mentions)
                            if ('freedom unlimited' in combined_text or 'cfu' in combined_text) and 'sapphire' not in combined_text:
                                card_detected = 'Freedom Unlimited'
                            
                            # Check for Freedom Flex (only if Unlimited not found and no Sapphire)
                            elif card_detected is None and ('freedom flex' in combined_text or 'cff' in combined_text) and 'sapphire' not in combined_text:
                                card_detected = 'Freedom Flex'
                            
                            # Generic Freedom only if no specific card and no Sapphire
                            elif card_detected is None and 'freedom' in combined_text and 'sapphire' not in combined_text:
                                if 'unlimited' not in combined_text and 'flex' not in combined_text:
                                    card_detected = 'Freedom (Generic)'

                            # Enhanced approval/denial language detection
                            approval_keywords = [
                                'approved', 'denied', 'approval', 'rejected', 'rejection',
                                'application approved', 'application denied',
                                'got approved', 'got denied', 'was approved', 'was denied',
                                'instant approval', 'instantly denied', 'instant denied',
                                'approved for', 'denied for', 'approved with', 'denied with',
                                'credit limit', 'approved limit', 'denied limit',
                                'income', 'credit score', 'fico', 'vantage'
                            ]

                            # Check if card mention and approval/denial keywords are present
                            relevant = False

                            if card_detected:
                                # Check if approval/denial keywords are present
                                if any(kw in combined_text for kw in approval_keywords):
                                    relevant = True
                                
                                # Also include posts that mention the card and have substantial content
                                if len(post.selftext) > 100:  # Posts with substantial body text
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
                                print(f"    Saved post: {post.title[:60]}... ({card_detected})")
                    
                    except Exception as e:
                        print(f"    Error searching {phrase} in {subreddit_name}: {e}")
                        continue

    print(f"\nEnhanced scraping completed!")
    print(f"Total posts collected: {total_posts}")
    print(f"Results saved to: {filename}")
    return filename

def main():
    """Main function to run the enhanced scraper"""
    print("Starting Enhanced Reddit scraper for Freedom Unlimited and Freedom Flex...")
    print("Searching multiple subreddits with expanded search terms...")
    filename = scrape_enhanced_freedom_cards_posts()
    print(f"Enhanced scraping completed. Data saved to: {filename}")

if __name__ == "__main__":
    main() 
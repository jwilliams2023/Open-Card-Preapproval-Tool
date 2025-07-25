import praw
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

def scrape_freedom_cards_posts():
    """Scrape Freedom Unlimited and Freedom Flex approval/denial posts from Reddit"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit = reddit.subreddit('CreditCards')

    # Search phrases for both Freedom cards
    search_phrases = [
        # Freedom Unlimited
        '"Freedom Unlimited" approved',
        '"Freedom Unlimited" denied',
        '"Freedom Unlimited" approval',
        '"Freedom Unlimited" instant approval',
        '"Freedom Unlimited" rejection',
        '"Freedom Unlimited" reject',
        'CFU approved',
        'CFU denied',
        'CFU approval',
        'CFU rejection',
        'CFU reject',
        
        # Freedom Flex
        '"Freedom Flex" approved',
        '"Freedom Flex" denied',
        '"Freedom Flex" approval',
        '"Freedom Flex" instant approval',
        '"Freedom Flex" rejection',
        '"Freedom Flex" reject',
        'CFF approved',
        'CFF denied',
        'CFF approval',
        'CFF rejection',
        'CFF reject',
        
        # Generic Freedom searches
        'Chase Freedom approved',
        'Chase Freedom denied',
        'Chase Freedom approval',
        'Chase Freedom rejection'
    ]

    seen_post_ids = set()
    
    # Create data/raw directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/raw/freedom_cards_approval_data_{timestamp}.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At'])

        for phrase in search_phrases:
            print(f"Searching for: {phrase}")
            for post in subreddit.search(phrase, sort='new', limit=1000):
                if post.id in seen_post_ids:
                    continue
                seen_post_ids.add(post.id)

                title_lower = post.title.lower()
                body_lower = post.selftext.lower()
                combined_text = f"{title_lower} {body_lower}"

                # Card detection logic - be more strict about Freedom cards only
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

                # Approval/denial language
                approval_keywords = [
                    'approved', 'denied', 'approval',
                    'rejected', 'rejection',
                    'application approved', 'application denied',
                    'got approved', 'got denied',
                    'instant approval', 'instantly denied'
                ]

                # Check if card mention and approval/denial keywords are near each other
                relevant = False

                if card_detected:
                    # Check if approval/denial keywords are present
                    if any(kw in combined_text for kw in approval_keywords):
                        relevant = True

                if relevant and card_detected:
                    writer.writerow([
                        post.title, 
                        post.url, 
                        post.selftext,
                        'Reddit',
                        card_detected,
                        datetime.now().isoformat()
                    ])
                    print(f"Saved post: {post.title} ({card_detected})")

    print(f"Finished. Results saved to {filename}")
    return filename

def main():
    """Main function to run the scraper"""
    print("Starting Reddit scraper for Freedom cards (Unlimited + Flex)...")
    filename = scrape_freedom_cards_posts()
    print(f"Scraping completed. Data saved to: {filename}")

if __name__ == "__main__":
    main()

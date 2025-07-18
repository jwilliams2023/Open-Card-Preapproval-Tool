import praw
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

def scrape_freedom_unlimited_posts():
    """Scrape Freedom Unlimited approval/denial posts from Reddit"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit = reddit.subreddit('CreditCards')

    search_phrases = [
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
        'CFU reject'
    ]

    seen_post_ids = set()
    
    # Create data/raw directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data/raw/freedom_unlimited_approval_data_{timestamp}.csv'

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

                # Card mention keywords
                card_keywords = ['freedom unlimited', 'cfu']

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

                for keyword in card_keywords:
                    idx_title = title_lower.find(keyword)
                    idx_body = body_lower.find(keyword)

                    if idx_title != -1:
                        snippet = title_lower[max(0, idx_title - 50): idx_title + 50]
                        if any(kw in snippet for kw in approval_keywords):
                            relevant = True

                    if idx_body != -1:
                        snippet = body_lower[max(0, idx_body - 50): idx_body + 50]
                        if any(kw in snippet for kw in approval_keywords):
                            relevant = True

                if relevant:
                    writer.writerow([
                        post.title, 
                        post.url, 
                        post.selftext,
                        'Reddit',
                        'Freedom Unlimited',
                        datetime.now().isoformat()
                    ])
                    print(f"Saved post: {post.title}")

    print(f"Finished. Results saved to {filename}")
    return filename

def main():
    """Main function to run the scraper"""
    print("Starting Reddit scraper for Freedom Unlimited posts...")
    filename = scrape_freedom_unlimited_posts()
    print(f"Scraping completed. Data saved to: {filename}")

if __name__ == "__main__":
    main()

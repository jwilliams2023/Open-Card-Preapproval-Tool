import praw
import csv
from dotenv import load_dotenv
import os
from datetime import datetime

def simple_test():
    """Simple test to see what Reddit search actually returns"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit = reddit.subreddit('CreditCards')
    
    # Test different search approaches
    test_searches = [
        ('CFU approved', 'CFU approved'),
        ('Freedom Unlimited approved', 'Freedom Unlimited approved'),
        ('Freedom approved', 'Freedom approved'),
        ('Chase Freedom approved', 'Chase Freedom approved')
    ]

    filename = 'data/raw/simple_test.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Search_Phrase', 'Title', 'URL', 'Body', 'Has_Freedom', 'Has_Approved'])

        for search_name, search_phrase in test_searches:
            print(f"\n=== Testing: {search_name} ===")
            
            try:
                # Try different approaches
                print(f"Searching: {search_phrase}")
                
                # Method 1: Basic search
                posts = list(subreddit.search(search_phrase, sort='new', limit=10))
                print(f"Found {len(posts)} posts with basic search")
                
                for post in posts:
                    title_lower = post.title.lower()
                    body_lower = post.selftext.lower()
                    combined = f"{title_lower} {body_lower}"
                    
                    has_freedom = any(term in combined for term in ['freedom', 'cfu', 'cff'])
                    has_approved = 'approved' in combined
                    
                    writer.writerow([
                        search_name,
                        post.title,
                        post.url,
                        post.selftext[:200] + "..." if len(post.selftext) > 200 else post.selftext,
                        has_freedom,
                        has_approved
                    ])
                    
                    print(f"  Title: {post.title}")
                    print(f"    Has Freedom: {has_freedom}")
                    print(f"    Has Approved: {has_approved}")
                    print(f"    URL: {post.url}")
                    print()
                
            except Exception as e:
                print(f"Error with {search_name}: {e}")

    print(f"\nSimple test completed. Results saved to: {filename}")

def main():
    print("Running simple Reddit search test...")
    simple_test()

if __name__ == "__main__":
    main() 
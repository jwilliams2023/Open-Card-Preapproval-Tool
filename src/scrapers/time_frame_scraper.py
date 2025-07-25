import praw
import csv
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

def scrape_time_frame_test():
    """Test different Reddit time frames to find best data"""
    
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('REDDIT_APP_ID')
    client_secret = os.getenv('REDDIT_APP_SECRET')
    user_agent = os.getenv('REDDIT_APP_NAME')

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Test subreddit
    subreddit_name = 'CreditCards'
    subreddit = reddit.subreddit(subreddit_name)

    # Test search phrase
    test_phrase = 'Freedom Unlimited approved'
    
    # Reddit time frames to test
    time_frames = [
        ('day', 'day'),
        ('week', 'week'), 
        ('month', 'month'),
        ('year', 'year'),
        ('all', 'all')
    ]

    # Create output directory
    os.makedirs('data/raw', exist_ok=True)
    
    # Use fixed filename
    filename = 'data/raw/time_frame_test.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Time_Frame', 'Title', 'URL', 'Body', 'Source', 'Card_Name', 'Scraped_At'])

        total_posts = 0
        
        for time_name, time_param in time_frames:
            print(f"\nTesting time frame: {time_name}")
            
            try:
                # Search with specific time frame
                for post in subreddit.search(test_phrase, sort='top', time_filter=time_param, limit=50):
                    title_lower = post.title.lower()
                    body_lower = post.selftext.lower()
                    combined_text = f"{title_lower} {body_lower}"

                    # Card detection logic
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

                    # Outcome detection
                    outcome_keywords = [
                        'approved', 'denied', 'preapproved', 'pre-approval', 'pre approval',
                        'rejected', 'rejection', 'got approved', 'got denied',
                        'instant approval', 'application approved', 'application denied'
                    ]

                    # Quality check
                    relevant = False
                    if card_detected:
                        if any(kw in combined_text for kw in outcome_keywords):
                            if len(post.selftext) > 50 or any(kw in title_lower for kw in outcome_keywords):
                                relevant = True

                    if relevant and card_detected:
                        writer.writerow([
                            time_name,
                            post.title, 
                            post.url, 
                            post.selftext,
                            f'Reddit-{subreddit_name}',
                            card_detected,
                            datetime.now().isoformat()
                        ])
                        total_posts += 1
                        print(f"  Found: {post.title[:60]}... ({card_detected})")
            
            except Exception as e:
                print(f"  Error with {time_name}: {e}")
                continue

    print(f"\nTime frame test completed!")
    print(f"Total posts found: {total_posts}")
    print(f"Results saved to: {filename}")
    
    # Analyze results by time frame
    if total_posts > 0:
        df = pd.read_csv(filename)
        print(f"\nPosts by time frame:")
        print(df['Time_Frame'].value_counts())
    
    return filename

def main():
    """Main function to run the time frame test"""
    print("Testing different Reddit time frames for Freedom card data...")
    print("Searching: 'Freedom Unlimited approved' in r/CreditCards")
    print("Testing: day, week, month, year, all")
    filename = scrape_time_frame_test()
    print(f"Time frame test completed. Data saved to: {filename}")

if __name__ == "__main__":
    main() 
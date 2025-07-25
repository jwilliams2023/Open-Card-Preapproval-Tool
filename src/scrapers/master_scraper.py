import praw
import csv
import os
import json
import pandas as pd
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import argparse

lock = Lock()
results = []
new_posts_counter = 0

# Load environment variables
load_dotenv()
client_id = os.getenv('REDDIT_APP_ID')
client_secret = os.getenv('REDDIT_APP_SECRET')
user_agent = os.getenv('REDDIT_APP_NAME')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

def get_master_file():
    master_file = 'data/raw/freedom_cards_dataset.csv'
    os.makedirs('data/raw', exist_ok=True)
    
    # Only create header if file doesn't exist
    if not os.path.exists(master_file):
        with open(master_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'URL', 'Body', 'Source', 'Card_Name', 'Decision', 'Scraped_At'])
    
    return master_file

def get_existing_urls(master_file):
    existing_urls = set()
    if os.path.exists(master_file):
        try:
            df = pd.read_csv(master_file)
            if 'URL' in df.columns:
                existing_urls.update(df['URL'].tolist())
        except Exception as e:
            print(f"Error reading master file: {e}")
    return existing_urls

def detect_card(text):
    text = text.lower()
    premium_exclusions = ['sapphire', 'preferred', 'reserve', 'csr', 'csp', 'ink', 'business', 'amex', 'gold']
    if any(x in text for x in premium_exclusions):
        return None

    freedom_unlimited_terms = ['freedom unlimited', 'cfu', 'chase freedom unlimited', 'freedom unlimited card', 'cfu card']
    freedom_flex_terms = ['freedom flex', 'cff', 'chase freedom flex', 'freedom flex card', 'cff card']

    if any(term in text for term in freedom_unlimited_terms):
        return 'Freedom Unlimited'
    elif any(term in text for term in freedom_flex_terms):
        return 'Freedom Flex'
    elif 'freedom' in text:
        return 'Freedom (Generic)'
    return None

def detect_decision(text):
    text = text.lower()
    if 'denied' in text or 'rejected' in text:
        return 'Denied'
    if 'preapproved' in text or 'pre-approval' in text:
        return 'Pre-Approved'
    if 'approved' in text or 'got approved' in text:
        return 'Approved'
    return 'Unknown'

def is_card_contextually_relevant(text, card_terms, decision_terms):
    tokens = text.lower().split()
    for i, token in enumerate(tokens):
        if any(card in token for card in card_terms):
            window = tokens[max(i - 12, 0):i + 13]
            if any(decision in w for decision in decision_terms for w in window):
                return True
    return False

def process_phrase(subreddit_name, phrase, existing_urls, master_file, max_new_posts):
    global new_posts_counter
    subreddit = reddit.subreddit(subreddit_name)
    seen_post_ids = set()

    for sort_method in ['new', 'top']:
        try:
            for post in subreddit.search(phrase, sort=sort_method, limit=100):
                with lock:
                    if new_posts_counter >= max_new_posts:
                        return

                if post.id in seen_post_ids or post.url in existing_urls:
                    continue
                seen_post_ids.add(post.id)

                post_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                if post_time < datetime.now(timezone.utc) - timedelta(days=180):
                    continue

                combined_text = f"{post.title.lower()} {post.selftext.lower()}"
                card_name = detect_card(combined_text)
                decision = detect_decision(combined_text)

                card_terms = ['freedom unlimited', 'cfu', 'freedom flex', 'cff']
                decision_terms = ['approved', 'denied', 'rejected', 'preapproved', 'pre-approval']

                if card_name and decision != 'Unknown':
                    # Less strict filtering - just check for basic relevance
                    if len(post.selftext) > 30 and not any(x in combined_text for x in ['amex', 'gold', 'sapphire', 'csp', 'csr']):
                            with lock:
                                # Clean the text to avoid CSV parsing issues
                                clean_title = post.title.replace('\n', ' ').replace('\r', ' ')
                                clean_body = post.selftext.replace('\n', ' ').replace('\r', ' ')
                                results.append([
                                    clean_title, post.url, clean_body,
                                    f'Reddit-{subreddit_name}', card_name,
                                    decision, datetime.now().isoformat()
                                ])
                                existing_urls.add(post.url)
                                new_posts_counter += 1
                                print(f"Added ({new_posts_counter}): {post.title[:60]}...")
                    else:
                        print(f"Skipped: not contextually relevant - {post.title[:50]}")
                else:
                    print(f"Skipped: no card match or unclear decision - {post.title[:50]}")

        except Exception as e:
            print(f"Error with phrase '{phrase}' in r/{subreddit_name}: {e}")

def scrape_all(args):
    with open('scraper_config.json') as f:
        config = json.load(f)

    subreddits = config['subreddits']
    search_phrases = config['search_phrases']

    master_file = get_master_file()
    existing_urls = get_existing_urls(master_file)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for subreddit in subreddits:
            for phrase in search_phrases:
                futures.append(executor.submit(process_phrase, subreddit, phrase, existing_urls, master_file, args.max_posts))
        for _ in as_completed(futures):
            pass

    # Append new results to existing file
    with open(master_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print(f"\nScraping complete. {new_posts_counter} new posts added.")
    total_posts = sum(1 for line in open(master_file)) - 1
    print(f"Total posts in master file: {total_posts}")

def main():
    parser = argparse.ArgumentParser(description="Reddit Scraper for Freedom Cards")
    parser.add_argument('--max-posts', type=int, default=500, help="Max number of new posts to collect")
    parser.add_argument('--threads', type=int, default=4, help="Number of parallel threads")
    args = parser.parse_args()

    scrape_all(args)

if __name__ == '__main__':
    main()

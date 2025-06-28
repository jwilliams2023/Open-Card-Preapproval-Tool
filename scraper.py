import praw
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv('REDDIT_APP_ID')
client_secret = os.getenv('REDDIT_APP_SECRET')
user_agent = os.getenv('REDDIT_APP_NAME')

# Initialize Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Access subreddit
subreddit = reddit.subreddit('CreditCards')

# Open CSV file to write results
with open('flex_approval_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['Title', 'URL', 'Body'])

    # Search and filter posts
    for post in subreddit.search('Chase Freedom Flex', sort='new', limit=100):
        if post.link_flair_text and 'Data Point' in post.link_flair_text:
            writer.writerow([post.title, post.url, post.selftext])
            print(f"Saved post: {post.title}")

print("Finished. Results saved to flex_approval_data.csv")

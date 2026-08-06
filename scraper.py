import os
import re
import praw

# Tickers to ignore that are common words
BLACKLIST = {"A", "I", "TECH", "BULL", "BEAR", "MEME", "ON", "IT", "ALL", "ARE", "FOR", "AND", "OR", "IN", "TO", "AT", "BY", "AN", "IS", "AS", "IF", "OF", "US", "WE", "HE", "ME", "SO", "DO", "NO", "UP", "GO", "A", "B", "C", "DD"}

def get_reddit_instance():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", "TradingBot/0.1 by /u/yourusername")
    
    if not client_id or not client_secret:
        print("WARNING: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables are not set.")
        print("Using mock data for testing purposes.")
        return None
        
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def extract_tickers(text):
    # Match $TICKER or just TICKER if it's 2-5 capital letters
    tickers = set()
    
    # Match $TICKER
    matches_dollar = re.findall(r'\$([A-Z]{1,5})\b', text)
    tickers.update(matches_dollar)
    
    # Match plain words that look like tickers
    matches_plain = re.findall(r'\b([A-Z]{2,5})\b', text)
    for m in matches_plain:
        if m not in BLACKLIST:
            tickers.add(m)
            
    return list(tickers)

def fetch_wallstreetbets_posts(limit=100):
    reddit = get_reddit_instance()
    
    data = []
    
    if not reddit:
        # Mock data based on the video
        return [
            {"text": "I really think TSLA is going to the moon!", "tickers": ["TSLA"]},
            {"text": "GME earnings are coming up, I'm buying calls.", "tickers": ["GME"]},
            {"text": "SPY puts are the play today, market is crashing.", "tickers": ["SPY"]},
            {"text": "TSLA is looking terrible right now, I'm shorting.", "tickers": ["TSLA"]},
            {"text": "AAPL to 200 soon?", "tickers": ["AAPL"]},
            {"text": "I lost all my money on GME.", "tickers": ["GME"]},
            {"text": "Tech is down today.", "tickers": []}
        ]

    subreddit = reddit.subreddit("wallstreetbets")
    for submission in subreddit.hot(limit=limit):
        combined_text = submission.title + " " + submission.selftext
        tickers = extract_tickers(combined_text)
        if tickers:
            data.append({
                "text": combined_text,
                "tickers": tickers
            })
            
    return data

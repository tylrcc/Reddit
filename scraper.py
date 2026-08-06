import os
import re
import praw
import logging
import yfinance as yf
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

BLACKLIST = {"A", "I", "TECH", "BULL", "BEAR", "MEME", "ON", "IT", "ALL", "ARE", "FOR", "AND", "OR", "IN", "TO", "AT", "BY", "AN", "IS", "AS", "IF", "OF", "US", "WE", "HE", "ME", "SO", "DO", "NO", "UP", "GO", "A", "B", "C", "DD", "WSB", "YOLO", "CEO"}

VALID_TICKERS_CACHE = set()
INVALID_TICKERS_CACHE = set()

def is_valid_ticker(ticker):
    """Uses yfinance to strictly validate if a ticker actually exists."""
    if ticker in VALID_TICKERS_CACHE:
        return True
    if ticker in INVALID_TICKERS_CACHE:
        return False
        
    try:
        t = yf.Ticker(ticker)
        # Fetching a single day of history is a fast way to check if ticker exists
        hist = t.history(period="1d")
        if not hist.empty:
            VALID_TICKERS_CACHE.add(ticker)
            return True
        else:
            INVALID_TICKERS_CACHE.add(ticker)
            return False
    except Exception:
        INVALID_TICKERS_CACHE.add(ticker)
        return False

def get_reddit_instance():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", "TradingBot/0.2 by /u/yourusername")
    
    if not client_id or not client_secret:
        logger.warning("REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables are not set. Using mock data.")
        return None
        
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def extract_tickers(text):
    tickers = set()
    
    matches_dollar = re.findall(r'\$([A-Z]{1,5})\b', text)
    tickers.update(matches_dollar)
    
    matches_plain = re.findall(r'\b([A-Z]{2,5})\b', text)
    for m in matches_plain:
        if m not in BLACKLIST:
            tickers.add(m)
            
    # Strictly validate against yfinance
    valid_tickers = [t for t in tickers if is_valid_ticker(t)]
    return valid_tickers

def fetch_wallstreetbets_posts(config):
    reddit = get_reddit_instance()
    data = []
    
    if not reddit:
        # Provide a static mock if API isn't set up
        return [
            {"text": "I really think TSLA is going to the moon!", "tickers": ["TSLA"]},
            {"text": "GME earnings are coming up, I'm buying calls.", "tickers": ["GME"]},
            {"text": "SPY puts are the play today, market is crashing.", "tickers": ["SPY"]},
            {"text": "AAPL to 200 soon?", "tickers": ["AAPL"]},
            {"text": "Tech is down today.", "tickers": []}
        ]

    subreddit_name = config.get("subreddit", "wallstreetbets")
    limit = config.get("fetch_limit", 100)
    max_age_hours = config.get("max_post_age_hours", 24)
    
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=limit):
            post_time = datetime.fromtimestamp(submission.created_utc, timezone.utc)
            if post_time < cutoff_time:
                continue
                
            combined_text = submission.title + " " + submission.selftext
            tickers = extract_tickers(combined_text)
            if tickers:
                data.append({
                    "text": combined_text,
                    "tickers": tickers
                })
    except Exception as e:
        logger.error(f"Error fetching from Reddit: {e}")
            
    return data

import os
import json
import logging
from datetime import datetime, timezone

from scraper import fetch_wallstreetbets_posts
from sentiment import FinBERTSentiment
from strategy import calculate_scores, get_top_recommendation

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("main")

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {}

def save_results(scores, top_ticker, top_data, filename):
    result_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "top_ticker": top_ticker,
        "top_data": top_data,
        "all_scores": scores
    }
    
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
        
    history.append(result_data)
    
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
    logger.info(f"Results saved to {filename}")

def main():
    logger.info("Starting Reddit WallStreetBets Trading Bot")
    config = load_config()
    
    # 1. Scrape posts
    logger.info("Scraping Reddit...")
    posts = fetch_wallstreetbets_posts(config.get("reddit", {}))
    logger.info(f"Fetched {len(posts)} posts mentioning tickers.")
    
    # 2. Analyze Sentiment
    logger.info("Analyzing Sentiment with FinBERT...")
    sentiment_analyzer = FinBERTSentiment(config.get("sentiment", {}))
    
    analyzed_data = []
    for post in posts:
        if not post["tickers"]:
            continue
        sentiment = sentiment_analyzer.analyze(post["text"])
        analyzed_data.append({
            "text": post["text"],
            "tickers": post["tickers"],
            "sentiment": sentiment
        })
        
    # 3. Calculate Scores
    logger.info("Calculating Strategy Scores...")
    scores = calculate_scores(analyzed_data)
    
    for ticker, data in scores.items():
        logger.info(f"Ticker: {ticker} | Bullish: {data['bullish']} | Bearish: {data['bearish']} | Score: {data['score']}")
        
    # 4. Recommendation
    logger.info("Generating Recommendation...")
    top_ticker, top_data = get_top_recommendation(scores)
    
    if top_ticker:
        logger.info(f"TOP PICK OF THE DAY: {top_ticker}")
        logger.info(f"Score: {top_data['score']} (Bullish: {top_data['bullish']}, Bearish: {top_data['bearish']})")
    else:
        logger.info("No tickers found with positive scores today.")
        
    # 5. Save results
    save_results(scores, top_ticker, top_data, config.get("output", {}).get("results_file", "results.json"))

if __name__ == "__main__":
    main()

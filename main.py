from scraper import fetch_wallstreetbets_posts
from sentiment import FinBERTSentiment
from strategy import calculate_scores, get_top_recommendation

def main():
    print("--- Reddit WallStreetBets Trading Bot ---")
    
    # 1. Scrape posts
    print("\n[1] Scraping WallStreetBets...")
    posts = fetch_wallstreetbets_posts(limit=50)
    print(f"Fetched {len(posts)} posts mentioning tickers.")
    
    # 2. Analyze Sentiment
    print("\n[2] Analyzing Sentiment with FinBERT...")
    sentiment_analyzer = FinBERTSentiment()
    
    analyzed_data = []
    for post in posts:
        # We only want to analyze if there are actual tickers
        if not post["tickers"]:
            continue
            
        sentiment = sentiment_analyzer.analyze(post["text"])
        analyzed_data.append({
            "text": post["text"],
            "tickers": post["tickers"],
            "sentiment": sentiment
        })
        
    # 3. Calculate Scores
    print("\n[3] Calculating Strategy Scores...")
    scores = calculate_scores(analyzed_data)
    
    # Print out all scores
    for ticker, data in scores.items():
        print(f"Ticker: {ticker} | Bullish: {data['bullish']} | Bearish: {data['bearish']} | Score: {data['score']}")
        
    # 4. Recommendation
    print("\n[4] Generating Recommendation...")
    top_ticker, top_data = get_top_recommendation(scores)
    
    if top_ticker:
        print(f"\n*** TOP PICK OF THE DAY: {top_ticker} ***")
        print(f"Score: {top_data['score']} (Bullish: {top_data['bullish']}, Bearish: {top_data['bearish']})")
        print("Note: Be careful out there, this strategy might just follow the hype!")
    else:
        print("\nNo tickers found with positive scores today.")

if __name__ == "__main__":
    main()

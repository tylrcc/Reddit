def calculate_scores(analyzed_data):
    """
    analyzed_data: list of dicts
    [
        {"text": "...", "tickers": ["TSLA"], "sentiment": "bullish"}
    ]
    """
    scores = {}
    
    for item in analyzed_data:
        sentiment = item["sentiment"]
        for ticker in item["tickers"]:
            if ticker not in scores:
                scores[ticker] = {"bullish": 0, "bearish": 0, "neutral": 0}
                
            if sentiment == "bullish":
                scores[ticker]["bullish"] += 1
            elif sentiment == "bearish":
                scores[ticker]["bearish"] += 1
            else:
                scores[ticker]["neutral"] += 1

    # Calculate final score: Bullish - Bearish
    for ticker in scores:
        scores[ticker]["score"] = scores[ticker]["bullish"] - scores[ticker]["bearish"]
        
    return scores

def get_top_recommendation(scores):
    if not scores:
        return None, None
        
    best_ticker = None
    best_score = -float('inf')
    
    for ticker, data in scores.items():
        if data["score"] > best_score:
            best_score = data["score"]
            best_ticker = ticker
            
    return best_ticker, scores.get(best_ticker)

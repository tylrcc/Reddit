from strategy import calculate_scores, get_top_recommendation

def test_calculate_scores():
    analyzed_data = [
        {"tickers": ["AAPL", "TSLA"], "sentiment": "bullish"},
        {"tickers": ["AAPL"], "sentiment": "bullish"},
        {"tickers": ["TSLA"], "sentiment": "bearish"}
    ]
    scores = calculate_scores(analyzed_data)
    assert scores["AAPL"]["score"] == 2
    assert scores["TSLA"]["score"] == 0

def test_get_top_recommendation():
    scores = {
        "AAPL": {"score": 2, "bullish": 2, "bearish": 0},
        "TSLA": {"score": 0, "bullish": 1, "bearish": 1}
    }
    ticker, data = get_top_recommendation(scores)
    assert ticker == "AAPL"
    assert data["score"] == 2

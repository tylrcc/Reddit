from scraper import extract_tickers

def test_extract_tickers_with_mock_yfinance(monkeypatch):
    # Mock is_valid_ticker to always return True for testing extraction logic
    monkeypatch.setattr("scraper.is_valid_ticker", lambda x: True)
    
    text = "I love $AAPL and think TSLA will go up, but TECH is bad."
    tickers = extract_tickers(text)
    
    # TECH is in blacklist, shouldn't be extracted as plain. 
    # AAPL and TSLA should be.
    assert "AAPL" in tickers
    assert "TSLA" in tickers
    assert "TECH" not in tickers

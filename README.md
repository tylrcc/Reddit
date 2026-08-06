<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=Reddit%20Trading%20Bot&fontSize=70&fontAlignY=38&desc=AI-Powered%20Sentiment%20Analysis%20for%20WallStreetBets&descAlignY=58&descAlign=50" alt="header" />
</div>

<p align="center">
  <em>An automated trading algorithm that scrapes r/WallStreetBets, processes financial text using NLP (FinBERT), and ranks stock tickers based on community sentiment.</em>
</p>

## Overview

The **Reddit Trading Bot** is a Python-based algorithmic trading tool that attempts to quantify market sentiment on the popular subreddit `r/wallstreetbets`. 

By harnessing the power of [FinBERT](https://huggingface.co/ProsusAI/finbert), a pre-trained NLP model specifically fine-tuned for financial sentiment classification, the bot scans daily posts, identifies mentioned stock tickers, and scores them as **Bullish** or **Bearish**. 

> **Disclaimer:** This project was built to test hypotheses around retail trading sentiment and lookahead biases. As demonstrated in extensive backtesting, blindly following retail hype often yields negative alpha. **Use this software strictly for educational and research purposes.**

## How the Strategy Works

The strategy is built on a simple yet powerful pipeline:

1. **Data Ingestion**: Uses `praw` to scrape the top/hottest posts and comments over a rolling 24-hour window from `r/wallstreetbets`.
2. **Entity Extraction**: Employs Regex filtering to isolate valid stock tickers (e.g., `$TSLA`, `AAPL`). It actively filters out noise like "TECH", "BULL", or "MEME" which are often mistaken as ETFs by naive bots.
3. **Sentiment Classification**: Passes the context surrounding each ticker into **FinBERT**. The model outputs a high-confidence label: `Positive`, `Negative`, or `Neutral`.
4. **Scoring Algorithm**: For each ticker, the bot calculates a net sentiment score:
   
   $$\text{Net Score} = \sum \text{Bullish Mentions} - \sum \text{Bearish Mentions}$$
   
5. **Execution Signal**: The ticker with the highest Net Score is outputted as the top pick of the day.

### Example Output
```yaml
 Reddit WallStreetBets Trading Bot 

[1] Scraping WallStreetBets...
Fetched 142 posts mentioning tickers.

[2] Analyzing Sentiment with FinBERT...
Model loaded successfully.

[3] Calculating Strategy Scores...
Ticker: TSLA | Bullish: 12 | Bearish: 4 | Score: 8
Ticker: GME  | Bullish: 2  | Bearish: 5 | Score: -3
Ticker: SPY  | Bullish: 8  | Bearish: 12| Score: -4
Ticker: AAPL | Bullish: 18 | Bearish: 2 | Score: 16

[4] Generating Recommendation...
*** TOP PICK OF THE DAY: AAPL ***
Score: 16 (Bullish: 18, Bearish: 2)
```

## Tech Stack

- **[Python 3.10+](https://www.python.org/)** Core programming language
- **[HuggingFace Transformers](https://huggingface.co/docs/transformers/index)** For executing FinBERT pipelines
- **[PyTorch](https://pytorch.org/)** ML Framework backend for FinBERT
- **[PRAW](https://praw.readthedocs.io/en/stable/)** Reddit API Wrapper for data scraping
- **[Pandas](https://pandas.pydata.org/)** Data manipulation and tracking
- **[yfinance](https://pypi.org/project/yfinance/)** Strict market validation for scraped tickers
- **[Pytest](https://docs.pytest.org/en/stable/)** Unit testing framework

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tylrcc/Reddit.git
   cd Reddit
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Credentials:**
   Obtain a Reddit Developer API key from [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps). Set them as environment variables:
   ```bash
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   ```
   *(If you run the bot without these, it will default to a mock dataset for testing).*

5. **Run the Bot:**
   ```bash
   python main.py
   ```

## Backtesting Insights & The "Lookahead Bias"

When backtesting this strategy, it is incredibly easy to accidentally introduce **Lookahead Bias** (using tomorrow's data to predict today's trades). 
If the bot observes community reaction *after* a market move has already occurred and uses that to "buy" the stock before the news spread, it fakes an incredibly high return (e.g., +1,000% CAGR).
When corrected, the reality is that **shorting the most mentioned stocks** or **buying the most hyped stocks** both generally underperform the S&P 500. This bot is a testament to those findings.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/tylrcc/Reddit/issues).

## License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

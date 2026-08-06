import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

class FinBERTSentiment:
    def __init__(self, config):
        model_name = config.get("model_name", "ProsusAI/finbert")
        logger.info(f"Loading FinBERT model: {model_name}...")
        try:
            self.classifier = pipeline("sentiment-analysis", model=model_name)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load FinBERT model: {e}")
            raise
            
        self.max_length = config.get("max_length", 1500)

    def analyze(self, text):
        truncated = text[:self.max_length] 
        try:
            result = self.classifier(truncated)
            label = result[0]['label']
            if label == "positive":
                return "bullish"
            elif label == "negative":
                return "bearish"
            else:
                return "neutral"
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return "neutral"

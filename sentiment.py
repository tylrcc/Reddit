import torch
from transformers import pipeline

class FinBERTSentiment:
    def __init__(self):
        print("Loading FinBERT model...")
        # ProsusAI/finbert outputs 'positive', 'negative', 'neutral'
        self.classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        print("Model loaded successfully.")

    def analyze(self, text):
        # Truncate text to max length for BERT (usually 512 tokens). 
        # Since this is character-based truncation, 1500 chars is safe.
        truncated = text[:1500] 
        result = self.classifier(truncated)
        
        # result is a list of dicts like [{'label': 'positive', 'score': 0.9}]
        label = result[0]['label']
        if label == "positive":
            return "bullish"
        elif label == "negative":
            return "bearish"
        else:
            return "neutral"

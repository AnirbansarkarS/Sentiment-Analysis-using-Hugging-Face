import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from config import Config

class SentimentAnalyzer:
    """Sentiment analysis using Hugging Face API."""
    
    def __init__(self):
        self.config = Config()
        self.headers = {
            "Authorization": f"Bearer {self.config.HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def query_api(self, text: str, model_name: str = None) -> Optional[Dict]:
        """Query Hugging Face API for sentiment analysis."""
        
        if not self.config.HUGGINGFACE_API_TOKEN:
            raise ValueError("Hugging Face API token not found. Please set HUGGINGFACE_API_TOKEN in .env file")
        
        # Select model URL
        if model_name and model_name in self.config.MODELS:
            api_url = f"https://api-inference.huggingface.co/models/{self.config.MODELS[model_name]}"
        else:
            api_url = self.config.API_URL
        
        payload = {"inputs": text}
        
        try:
            response = requests.post(api_url, headers=self.headers, json=payload)
            
            if response.status_code == 503:  # Model loading
                time.sleep(10)  # Wait for model to load
                response = requests.post(api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def analyze_sentiment(self, text: str, model_name: str = None) -> Dict:
        """Analyze sentiment and return formatted results."""
        
        if not text.strip():
            return {
                "error": "Please enter some text to analyze",
                "sentiment": None,
                "confidence": 0,
                "all_scores": []
            }
        
        if len(text) > self.config.MAX_TEXT_LENGTH:
            return {
                "error": f"Text too long. Maximum {self.config.MAX_TEXT_LENGTH} characters allowed.",
                "sentiment": None,
                "confidence": 0,
                "all_scores": []
            }
        
        result = self.query_api(text, model_name)
        
        if result is None:
            return {
                "error": "Failed to get response from API. Please try again.",
                "sentiment": None,
                "confidence": 0,
                "all_scores": []
            }
        
        try:
            if isinstance(result, list) and len(result) > 0:
                scores = result[0]
                
                # Sort by confidence score
                sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
                
                top_prediction = sorted_scores[0]
                sentiment = self._normalize_label(top_prediction['label'])
                confidence = top_prediction['score']
                
                return {
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "all_scores": sorted_scores,
                    "error": None
                }
            else:
                return {
                    "error": "Unexpected API response format",
                    "sentiment": None,
                    "confidence": 0,
                    "all_scores": []
                }
                
        except (KeyError, IndexError, TypeError) as e:
            return {
                "error": f"Error processing API response: {str(e)}",
                "sentiment": None,
                "confidence": 0,
                "all_scores": []
            }
    
    def analyze_batch(self, texts: List[str], model_name: str = None) -> List[Dict]:
        """Analyze sentiment for multiple texts."""
        results = []
        
        for text in texts:
            result = self.analyze_sentiment(text, model_name)
            results.append(result)
            time.sleep(0.1)  # Rate limiting
        
        return results
    
    def _normalize_label(self, label: str) -> str:
        """Normalize sentiment labels across different models."""
        label_lower = label.lower()
        
        if 'pos' in label_lower or label_lower in ['positive', '5 stars', '4 stars']:
            return 'Positive'
        elif 'neg' in label_lower or label_lower in ['negative', '1 star', '2 stars']:
            return 'Negative'
        elif 'neu' in label_lower or label_lower in ['neutral', '3 stars']:
            return 'Neutral'
        else:
            return label.title()
    
    def get_sentiment_emoji(self, sentiment: str) -> str:
        """Get emoji representation of sentiment."""
        emoji_map = {
            'Positive': '😊',
            'Negative': '😞',
            'Neutral': '😐',
            'Joy': '😄',
            'Sadness': '😢',
            'Anger': '😠',
            'Fear': '😨',
            'Surprise': '😮'
        }
        return emoji_map.get(sentiment, '🤔')
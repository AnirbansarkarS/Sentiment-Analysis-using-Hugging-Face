import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the sentiment analysis app."""
    
    # API Configuration
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
    API_URL = os.getenv('API_URL', 'https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest')
    BACKUP_API_URL = os.getenv('BACKUP_API_URL', 'https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment')
    
    # App Configuration
    APP_TITLE = "Sentiment Analysis Dashboard"
    APP_DESCRIPTION = "Analyze sentiment of text using Hugging Face transformers"
    
    # Supported models
    MODELS = {
        "Twitter RoBERTa": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "BERT Multilingual": "nlptown/bert-base-multilingual-uncased-sentiment",
        "DistilBERT": "distilbert-base-uncased-finetuned-sst-2-english",
        "RoBERTa": "roberta-base-openai-detector"
    }
    
    # UI Configuration
    MAX_TEXT_LENGTH = 5000
    BATCH_SIZE = 10
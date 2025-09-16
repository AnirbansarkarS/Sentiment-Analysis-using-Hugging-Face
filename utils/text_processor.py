import re
import pandas as pd
from typing import List, Dict

class TextProcessor:
    """Text preprocessing and analysis utilities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and preprocess text."""
        if not isinstance(text, str):
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions and hashtags (optional)
        # text = re.sub(r'@[A-Za-z0-9_]+', '', text)
        # text = re.sub(r'#[A-Za-z0-9_]+', '', text)
        
        return text.strip()
    
    @staticmethod
    def extract_text_stats(text: str) -> Dict:
        """Extract basic statistics from text."""
        if not text:
            return {
                "character_count": 0,
                "word_count": 0,
                "sentence_count": 0,
                "avg_word_length": 0
            }
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0
        }
    
    @staticmethod
    def split_into_chunks(text: str, chunk_size: int = 500) -> List[str]:
        """Split long text into smaller chunks for analysis."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @staticmethod
    def create_results_dataframe(results: List[Dict], texts: List[str] = None) -> pd.DataFrame:
        """Create a pandas DataFrame from sentiment analysis results."""
        data = []
        
        for i, result in enumerate(results):
            row = {
                'Text': texts[i] if texts else f"Text {i+1}",
                'Sentiment': result.get('sentiment', 'Unknown'),
                'Confidence': result.get('confidence', 0),
                'Error': result.get('error', None)
            }
            
            # Add individual label scores
            if result.get('all_scores'):
                for score in result['all_scores']:
                    label = score['label']
                    row[f'{label}_Score'] = score['score']
            
            data.append(row)
        
        return pd.DataFrame(data)
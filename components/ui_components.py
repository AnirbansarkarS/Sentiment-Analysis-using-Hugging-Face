import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd

class UIComponents:
    """Custom UI components for the Streamlit app."""
    
    @staticmethod
    def render_header():
        """Render app header."""
        st.set_page_config(
            page_title="Sentiment Analysis Dashboard",
            page_icon="😊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🎭 Sentiment Analysis Dashboard")
        st.markdown("""
        Analyze the sentiment of text using state-of-the-art transformer models from Hugging Face.
        Choose from different models and get detailed sentiment predictions with confidence scores.
        """)
    
    @staticmethod
    def render_sidebar():
        """Render sidebar with model selection and settings."""
        st.sidebar.header("⚙️ Settings")
        
        # Model selection
        from config import Config
        config = Config()
        
        model_names = list(config.MODELS.keys())
        selected_model = st.sidebar.selectbox(
            "Select Model",
            model_names,
            help="Choose the sentiment analysis model to use"
        )
        
        # Analysis options
        st.sidebar.subheader("Analysis Options")
        show_confidence = st.sidebar.checkbox("Show Confidence Scores", value=True)
        show_all_predictions = st.sidebar.checkbox("Show All Predictions", value=True)
        
        # Advanced settings
        with st.sidebar.expander("Advanced Settings"):
            batch_processing = st.checkbox("Enable Batch Processing", value=False)
            auto_clean_text = st.checkbox("Auto Clean Text", value=True)
        
        return {
            "selected_model": selected_model,
            "show_confidence": show_confidence,
            "show_all_predictions": show_all_predictions,
            "batch_processing": batch_processing,
            "auto_clean_text": auto_clean_text
        }
    
    @staticmethod
    def render_sentiment_result(result: Dict, show_confidence: bool = True, show_all: bool = True):
        """Render sentiment analysis result."""
        if result.get('error'):
            st.error(f"Error: {result['error']}")
            return
        
        sentiment = result.get('sentiment')
        confidence = result.get('confidence', 0)
        
        if sentiment:
            # Main result
            from utils.sentiment_analyzer import SentimentAnalyzer
            analyzer = SentimentAnalyzer()
            emoji = analyzer.get_sentiment_emoji(sentiment)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; border-radius: 10px; 
                           background: linear-gradient(45deg, #f0f0f0, #ffffff); 
                           border: 2px solid #e0e0e0;">
                    <h2>{emoji} {sentiment}</h2>
                    {f"<p><strong>Confidence:</strong> {confidence:.2%}</p>" if show_confidence else ""}
                </div>
                """, unsafe_allow_html=True)
            
            # Confidence meter
            if show_confidence:
                st.subheader("📊 Confidence Score")
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=confidence * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Confidence %"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "gray"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            # All predictions
            if show_all and result.get('all_scores'):
                st.subheader("📈 All Predictions")
                scores_df = pd.DataFrame(result['all_scores'])
                
                fig_bar = px.bar(
                    scores_df,
                    x='label',
                    y='score',
                    title="Sentiment Predictions",
                    color='score',
                    color_continuous_scale='RdYlGn'
                )
                fig_bar.update_layout(
                    xaxis_title="Sentiment",
                    yaxis_title="Confidence Score",
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    @staticmethod
    def render_batch_results(results: List[Dict], texts: List[str]):
        """Render batch processing results."""
        if not results:
            return
        
        st.subheader("📊 Batch Analysis Results")
        
        # Summary statistics
        valid_results = [r for r in results if not r.get('error')]
        
        if valid_results:
            sentiments = [r['sentiment'] for r in valid_results]
            sentiment_counts = pd.Series(sentiments).value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Sentiment Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(
                    x=sentiment_counts.index,
                    y=sentiment_counts.values,
                    title="Sentiment Counts",
                    color=sentiment_counts.values,
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed results table
        from utils.text_processor import TextProcessor
        processor = TextProcessor()
        
        results_df = processor.create_results_dataframe(results, texts)
        
        st.subheader("📋 Detailed Results")
        st.dataframe(results_df, use_container_width=True)
        
        # Download button for results
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="sentiment_analysis_results.csv",
            mime="text/csv"
        )
    
    @staticmethod
    def render_text_stats(stats: Dict):
        """Render text statistics."""
        st.subheader("📝 Text Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Characters", stats['character_count'])
        
        with col2:
            st.metric("Words", stats['word_count'])
        
        with col3:
            st.metric("Sentences", stats['sentence_count'])
        
        with col4:
            st.metric("Avg Word Length", f"{stats['avg_word_length']:.1f}")
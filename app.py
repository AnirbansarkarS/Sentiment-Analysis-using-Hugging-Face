import streamlit as st
import time
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.text_processor import TextProcessor
from components.ui_components import UIComponents
from config import Config

def main():
    """Main application function."""
    
    # Initialize components
    ui = UIComponents()
    analyzer = SentimentAnalyzer()
    processor = TextProcessor()
    config = Config()
    
    # Render header
    ui.render_header()
    
    # Render sidebar and get settings
    settings = ui.render_sidebar()
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["Single Text Analysis", "Batch Analysis", "File Upload"])
    
    with tab1:
        st.header("📝 Single Text Analysis")
        
        # Text input
        input_method = st.radio(
            "Choose input method:",
            ("Text Area", "Text Input"),
            horizontal=True
        )
        
        if input_method == "Text Area":
            user_text = st.text_area(
                "Enter text to analyze:",
                height=150,
                placeholder="Type or paste your text here...",
                help=f"Maximum {config.MAX_TEXT_LENGTH} characters"
            )
        else:
            user_text = st.text_input(
                "Enter text to analyze:",
                placeholder="Type your text here...",
                help=f"Maximum {config.MAX_TEXT_LENGTH} characters"
            )
        
        # Analysis button
        if st.button("🔍 Analyze Sentiment", type="primary"):
            if user_text:
                with st.spinner("Analyzing sentiment..."):
                    # Clean text if enabled
                    if settings['auto_clean_text']:
                        user_text = processor.clean_text(user_text)
                    
                    # Show text statistics
                    stats = processor.extract_text_stats(user_text)
                    ui.render_text_stats(stats)
                    
                    # Perform analysis
                    result = analyzer.analyze_sentiment(user_text, settings['selected_model'])
                    
                    # Display results
                    ui.render_sentiment_result(
                        result,
                        settings['show_confidence'],
                        settings['show_all_predictions']
                    )
            else:
                st.warning("Please enter some text to analyze.")
    
    with tab2:
        st.header("📊 Batch Analysis")
        
        # Batch input
        st.markdown("Enter multiple texts, one per line:")
        batch_text = st.text_area(
            "Batch texts:",
            height=200,
            placeholder="Text 1\nText 2\nText 3\n...",
            help="Each line will be analyzed separately"
        )
        
        if st.button("🔍 Analyze Batch", type="primary"):
            if batch_text:
                texts = [line.strip() for line in batch_text.split('\n') if line.strip()]
                
                if texts:
                    with st.spinner(f"Analyzing {len(texts)} texts..."):
                        # Clean texts if enabled
                        if settings['auto_clean_text']:
                            texts = [processor.clean_text(text) for text in texts]
                        
                        # Perform batch analysis
                        results = analyzer.analyze_batch(texts, settings['selected_model'])
                        
                        # Display results
                        ui.render_batch_results(results, texts)
                else:
                    st.warning("Please enter at least one text to analyze.")
            else:
                st.warning("Please enter texts to analyze.")
    
    with tab3:
        st.header("📁 File Upload Analysis")
        
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt', 'csv'],
            help="Upload a .txt file or .csv file with text data"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.type == "text/plain":
                    # Handle text file
                    content = str(uploaded_file.read(), "utf-8")
                    
                    st.text_area("File Content:", content, height=200, disabled=True)
                    
                    if st.button("🔍 Analyze File Content", type="primary"):
                        with st.spinner("Analyzing file content..."):
                            # Clean text if enabled
                            if settings['auto_clean_text']:
                                content = processor.clean_text(content)
                            
                            # Split into chunks if too long
                            if len(content) > config.MAX_TEXT_LENGTH:
                                chunks = processor.split_into_chunks(content, config.MAX_TEXT_LENGTH)
                                st.info(f"Text split into {len(chunks)} chunks for analysis")
                                
                                results = analyzer.analyze_batch(chunks, settings['selected_model'])
                                ui.render_batch_results(results, chunks)
                            else:
                                result = analyzer.analyze_sentiment(content, settings['selected_model'])
                                ui.render_sentiment_result(
                                    result,
                                    settings['show_confidence'],
                                    settings['show_all_predictions']
                                )
                
                elif uploaded_file.type == "text/csv":
                    # Handle CSV file
                    import pandas as pd
                    df = pd.read_csv(uploaded_file)
                    
                    st.subheader("CSV Preview")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    text_columns = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if text_columns:
                        selected_column = st.selectbox(
                            "Select text column for analysis:",
                            text_columns
                        )
                        
                        if st.button("🔍 Analyze CSV Column", type="primary"):
                            texts = df[selected_column].dropna().astype(str).tolist()
                            
                            with st.spinner(f"Analyzing {len(texts)} texts from CSV..."):
                                # Clean texts if enabled
                                if settings['auto_clean_text']:
                                    texts = [processor.clean_text(text) for text in texts]
                                
                                results = analyzer.analyze_batch(texts[:50], settings['selected_model'])  # Limit to 50 for demo
                                ui.render_batch_results(results, texts[:50])
                    else:
                        st.warning("No text columns found in the CSV file.")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: small;">
        Built with ❤️ using Streamlit and Hugging Face Transformers
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
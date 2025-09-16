Sentiment Analysis Dashboard

A modern web application for sentiment analysis using Hugging Face transformers and Streamlit.

🎭 Features

Multiple Models: Choose from various pre-trained sentiment analysis models
Real-time Analysis: Get instant sentiment predictions with confidence scores
Batch Processing: Analyze multiple texts simultaneously
File Support: Upload and analyze TXT or CSV files
Interactive Visualizations: View results through charts and graphs
Export Results: Download analysis results as CSV files
Responsive Design: Works on desktop and mobile devices
Error Handling: Comprehensive error handling with helpful messages

🚀 Quick Start
Prerequisites

Python 3.8 or higher
A Hugging Face account (free)

Installation

Clone or download the project

bash   git clone <your-repo-url>
   cd sentiment-analysis-app

Create a virtual environment

bash   python -m venv sentiment-env
   
   # On Windows:
   sentiment-env\Scripts\activate
   
   # On macOS/Linux:
   source sentiment-env/bin/activate

Install dependencies

bash   pip install -r requirements.txt

Get your Hugging Face API token

Go to Hugging Face Settings - Tokens
Click "New token"
Give it a name (e.g., "sentiment-analysis")
Select "Read" role
Click "Generate a token"
Copy the token (starts with hf_)


Configure your API token
Create a .env file in the project root:

bash   echo "HUGGINGFACE_API_TOKEN=hf_your_token_here" > .env
Or create it manually:
env   HUGGINGFACE_API_TOKEN=hf_your_actual_token_here

Run the application

bash   streamlit run app.py

Open your browser

Navigate to http://localhost:8501
The app will guide you through token setup if needed



📁 Project Structure
sentiment-analysis-app/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── utils/
│   ├── __init__.py
│   ├── sentiment_analyzer.py  # Sentiment analysis logic
│   └── text_processor.py      # Text preprocessing utilities
├── components/
│   ├── __init__.py
│   └── ui_components.py       # Custom UI components
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
🔧 Usage
Single Text Analysis

Select the "Single Text Analysis" tab
Enter your text in the text area or input field
Choose your preferred model from the sidebar
Click "🔍 Analyze Sentiment"
View the results with confidence scores and visualizations

Batch Analysis

Go to the "Batch Analysis" tab
Enter multiple texts (one per line)
Click "🔍 Analyze Batch"
Get comprehensive analytics for all texts
Download results as CSV

File Upload

Switch to the "File Upload" tab
Upload a TXT or CSV file
For CSV files, select the text column to analyze
The app handles large files by splitting them into chunks
View and export the results

🤖 Available Models
ModelBest ForLanguage SupportTwitter RoBERTaSocial media text, informal languageEnglishBERT MultilingualGeneral text, multiple languages104 languagesDistilBERTFast inference, general purposeEnglishRoBERTa BaseGeneral purpose, high accuracyEnglish
🛠️ Troubleshooting
❌ API Error 401 - Invalid Credentials
This is the most common issue. Here's how to fix it:
Step 1: Get a Valid API Token

Visit Hugging Face Settings - Tokens
Log in to your account (create one if needed - it's free)
Click "New token"
Name: sentiment-analysis-app
Role: Select "Read" (this is sufficient)
Click "Generate a token"
Copy the token immediately (you won't see it again)

Step 2: Verify Token Format

Should start with hf_
Should be about 37 characters long
Example: hf_abcdefghijklmnopqrstuvwxyz1234567890

Step 3: Configure the Token
Option A: Using .env file (Recommended)
bash# Create .env file in project root
echo "HUGGINGFACE_API_TOKEN=hf_your_token_here" > .env
Option B: Using Streamlit Secrets (For deployment)
bash# Create .streamlit/secrets.toml
mkdir -p .streamlit
echo 'HUGGINGFACE_API_TOKEN = "hf_your_token_here"' > .streamlit/secrets.toml
Option C: Manual Entry

Run the app without a token
Enter it in the provided input field when prompted
This works for the current session only

🔄 Other Common Issues
"Model is loading" message

Solution: Wait 10-30 seconds and try again
Cause: Hugging Face models need time to initialize on first use

Rate limit exceeded

Solution: Wait a few minutes between requests
Free accounts: Limited to a few hundred requests per month
Upgrade: Consider Hugging Face Pro for higher limits

Connection timeout

Solution: Check internet connection and try again
Alternative: Try a different model from the sidebar dropdown

Empty or unexpected results

Check: Make sure your text contains actual content
Verify: Text should be in a language supported by the chosen model

🧪 Test Your Setup
Create a test script to verify everything works:
python# test_api.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('HUGGINGFACE_API_TOKEN')

headers = {"Authorization": f"Bearer {token}"}
url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
data = {"inputs": "I love this product!"}

response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
Expected output:
Status: 200
Response: [[{'label': 'LABEL_2', 'score': 0.8}, {'label': 'LABEL_0', 'score': 0.1}, {'label': 'LABEL_1', 'score': 0.1}]]
📦 Dependencies
The main dependencies include:
txtstreamlit>=1.28.0          # Web app framework
requests>=2.31.0           # HTTP requests
python-dotenv>=1.0.0       # Environment variables
pandas>=2.0.0              # Data manipulation
plotly>=5.15.0             # Interactive charts
transformers>=4.30.0       # Hugging Face transformers
torch>=2.0.0               # PyTorch (for transformers)
numpy>=1.24.0              # Numerical computing
🌐 Deployment
Streamlit Cloud

Push your code to GitHub
Connect your repo to Streamlit Cloud
Add your HUGGINGFACE_API_TOKEN to secrets
Deploy with one click

Local Network
bashstreamlit run app.py --server.address 0.0.0.0 --server.port 8501
Docker (Optional)
dockerfileFROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Development Setup
bash# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest tests/

# Format code
black .
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Hugging Face for providing the transformer models
Streamlit for the amazing web app framework
Plotly for interactive visualizations
The open-source community for various Python libraries used

📞 Support
If you encounter any issues:

Check this README for common solutions
Search existing issues on GitHub
Create a new issue with:

Your Python version
Error messages (without your API token)
Steps to reproduce the problem



🔗 Useful Links

Hugging Face Documentation
Streamlit Documentation
Get Hugging Face API Token
Hugging Face Models


Built with ❤️ using Streamlit and Hugging Face Transformers
Star this repo if it helped you! ⭐

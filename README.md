Sentiment Analysis Dashboard

A modern web application for sentiment analysis using Hugging Face transformers and Streamlit.

## Features

- 🎭 Multiple pre-trained sentiment analysis models
- 📊 Interactive visualizations and confidence scores
- 📝 Single text and batch processing
- 📁 File upload support (TXT, CSV)
- 🎨 Clean, modern UI with real-time analysis
- 📈 Detailed analytics and downloadable results

## Setup Instructions

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd sentiment-analysis-app

Install dependencies

bash   pip install -r requirements.txt

Set up Hugging Face API

Get your API token from Hugging Face
Create a .env file and add your token:



     HUGGINGFACE_API_TOKEN=your_token_here

Run the application

bash   streamlit run app.py

Open your browser
Navigate to http://localhost:8501

Usage
Single Text Analysis

Enter text in the text area or input field
Choose your preferred model from the sidebar
Click "Analyze Sentiment" to get results

Batch Analysis

Enter multiple texts (one per line)
Get comprehensive analytics for all texts
Download results as CSV

File Upload

Upload TXT or CSV files
Analyze entire documents or specific columns
Handle large texts with automatic chunking

Models Available

Twitter RoBERTa (recommended for social media text)
BERT Multilingual (supports multiple languages)
DistilBERT (faster inference)
RoBERTa Base (general purpose)

API Configuration
The app uses Hugging Face's Inference API. Make sure you have:

A valid Hugging Face account
An API token with appropriate permissions
Sufficient API quota for your usage

Contributing

Fork the repository
Create a feature branch
Make your changes
Submit a pull request

License
This project is licensed under the MIT License.

## 9. .gitignore
```gitignore
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Streamlit
.streamlit/

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Data files
*.csv
*.txt
uploads/
Getting Started

Install Python 3.8+
Create a virtual environment:

bash   python -m venv sentiment-env
   source sentiment-env/bin/activate  # On Windows: sentiment-env\Scripts\activate

Install dependencies:

bash   pip install -r requirements.txt

Get Hugging Face API token:

Visit https://huggingface.co/settings/tokens
Create a new token with read permissions
Add it to your .env file


Run the app:

bash   streamlit run app.py
The application will be available at http://localhost:8501
Troubleshooting
API Error 401 - Invalid Credentials
This error means your Hugging Face API token is missing, incorrect, or expired. Here's how to fix it:
Step 1: Get a Valid API Token

Go to Hugging Face Settings - Tokens
Log in to your account
Click "New token"
Give it a name (e.g., "sentiment-analysis-app")
Select "Read" role (this is sufficient for using the API)
Click "Generate a token"
Copy the token immediately (you won't be able to see it again)

Step 2: Configure the Token
Option 1: Using .env file (Recommended)
bash# Create a .env file in your project root
echo "HUGGINGFACE_API_TOKEN=hf_your_token_here" > .env
Option 2: Using Streamlit Secrets (For deployment)
bash# Create .streamlit/secrets.toml
mkdir -p .streamlit
echo 'HUGGINGFACE_API_TOKEN = "hf_your_token_here"' > .streamlit/secrets.toml
Option 3: Temporary Manual Entry

Run the app and enter your token in the provided input field
This will work for the current session only

Step 3: Verify Token Format

Tokens should start with hf_
They are typically 37 characters long
Example format: hf_abcdefghijklmnopqrstuvwxyz1234567890

Common Issues
Issue: "Model is loading" message

Solution: Wait 10-20 seconds and try again. Hugging Face models need time to initialize.

Issue: Rate limit exceeded

Solution: Wait a few minutes between requests. Free accounts have limited API calls.
Upgrade: Consider upgrading to Hugging Face Pro for higher limits.

Issue: Connection timeout

Solution: Check your internet connection and try again.
Alternative: Try a different model from the dropdown.

Issue: Empty or no results

Solution: Make sure your text contains actual content and is not just whitespace.

API Token Permissions
Make sure your token has the correct permissions:

✅ Read access: Required for using the inference API
❌ Write access: Not needed for this application
❌ Admin access: Not needed for this application

Testing Your Setup
You can test if everything is working by running this simple test:
pythonimport requests

token = "hf_your_token_here"  # Replace with your actual token
headers = {"Authorization": f"Bearer {token}"}
url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
data = {"inputs": "I love this product!"}

response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
Expected output:
Status: 200
Response: [[{'label': 'LABEL_2', 'score': 0.8}, {'label': 'LABEL_0', 'score': 0.1}, {'label': 'LABEL_1', 'score': 0.1}]]
Key Features

Multiple Models: Choose from different transformer models optimized for various use cases
Real-time Analysis: Get instant sentiment predictions with confidence scores
Batch Processing: Analyze multiple texts simultaneously
File Support: Upload and analyze text files or CSV datasets
Interactive Visualizations: View results through charts and graphs
Export Results: Download analysis results as CSV files
Responsive Design: Works on desktop and mobile devices

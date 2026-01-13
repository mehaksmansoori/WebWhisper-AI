🔮 WebWhisper AI - Intelligent Website Chatbot
An intelligent chatbot that extracts insights from any website using advanced NLP techniques. Simply provide a URL, and WebWhisper AI will analyze the content and answer your questions naturally.
Show Image
✨ Features

🔍 Smart Web Scraping - Automatically extracts relevant content from any website
🤖 AI-Powered Analysis - Uses Google's FLAN-T5 model for intelligent responses
💬 Natural Conversations - Chat interface for intuitive Q&A
⚡ Real-time Processing - Get instant answers to your questions
📊 Content Statistics - View analysis metrics and chat history
🎨 Beautiful UI - Modern, responsive design with smooth animations

🚀 Live Demo
Try it now: WebWhisper AI on Streamlit Cloud
🛠️ Tech Stack

Frontend: Streamlit
NLP Model: Google FLAN-T5 (via Hugging Face)
Web Scraping: BeautifulSoup4, Requests
AI Framework: Transformers, PyTorch
Language: Python 3.8+

📋 Prerequisites

Python 3.8 or higher
pip package manager
Internet connection (for web scraping and model download)

🔧 Installation
Local Setup

Clone the repository

bash   git clone https://github.com/yourusername/webwhisper-ai.git
   cd webwhisper-ai

Create a virtual environment (recommended)

bash   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate

Install dependencies

bash   pip install -r requirements.txt

Run the application

bash   streamlit run streamlit-app.py

Open in browser

The app will automatically open at http://localhost:8501
If not, navigate to the URL shown in your terminal



☁️ Deploy to Streamlit Cloud
Quick Deployment Steps

Push to GitHub

bash   git add .
   git commit -m "Initial commit"
   git push origin main

Deploy on Streamlit Cloud

Go to share.streamlit.io
Sign in with your GitHub account
Click "New app"
Select your repository, branch (main), and main file (streamlit-app.py)
Click "Deploy"


Wait for deployment (usually 2-5 minutes)

Streamlit Cloud will automatically install dependencies from requirements.txt
Your app will be live at https://[your-app-name].streamlit.app



Important Notes for Deployment

⚠️ First Load Time: The first time a user accesses your app, it may take 30-60 seconds to download the FLAN-T5 model
💾 Resource Limits: Streamlit Cloud free tier has memory limits (~1GB). FLAN-T5-base works well within these limits
🔄 Auto-updates: The app automatically redeploys when you push changes to GitHub

📖 Usage Guide
Basic Workflow

Enter Website URL

Navigate to the sidebar
Enter any website URL (e.g., https://example.com)
Click "🚀 Analyze Website"


Wait for Analysis

WebWhisper will scrape and process the content
You'll see a success message when ready


Start Chatting

Ask questions in natural language
Examples:

"What is this website about?"
"What services are offered?"
"Who is the target audience?"


Manage Your Session

Use "🗑️ Clear Chat" to reset conversation
Use "🔄 New Website" to analyze a different URL



Example Questions

📝 "Summarize the main content"
🎯 "What problems does this solve?"
💼 "What are the pricing options?"
⭐ "What are the key features?"
👥 "Who created this?"

🏗️ Project Structure
webwhisper-ai/
│
├── streamlit-app.py      # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── console.py           # (Optional) Console utilities
🔍 How It Works

Web Scraping

Uses requests to fetch website HTML
BeautifulSoup4 parses and extracts text content
Removes irrelevant elements (scripts, styles, navigation)


Text Processing

Cleans and normalizes extracted text
Truncates to optimal length for model processing
Preserves context and meaning


AI Question Answering

User question + website context sent to FLAN-T5 model
Model generates natural language response
Answer displayed in chat interface


State Management

Streamlit session state maintains conversation history
Context cached for efficient multi-turn conversations



⚙️ Configuration
Model Selection
The app uses google/flan-t5-base by default. You can modify this in the load_model() function:
pythonmodel_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",  # Change model here
    device=-1
)
Alternative Models:

google/flan-t5-small - Faster, less accurate
google/flan-t5-large - More accurate, slower (may exceed Streamlit Cloud limits)

Content Length
Adjust maximum content length in the clean_text() function:
pythonmax_length = 2000  # Increase or decrease as needed
🐛 Troubleshooting
Common Issues
Problem: Model takes too long to load

Solution: This is normal on first load. The model (~900MB) is cached after the first download.

Problem: "Error fetching website"

Solution: Check if the URL is accessible and properly formatted (include https://)

Problem: Out of memory on Streamlit Cloud

Solution: Use flan-t5-small instead of flan-t5-base, or reduce max_length in text cleaning

Problem: Poor quality answers

Solution: Try rephrasing your question or asking more specific questions

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
👨‍💻 Author
Mehak Shaikh Mansoori

Created for: Relinns Technologies Assessment
Role: NLP Engineer

🙏 Acknowledgments

Streamlit - For the amazing web framework
Hugging Face - For the Transformers library and models
Google - For the FLAN-T5 model
BeautifulSoup - For web scraping capabilities


🔮 Future Enhancements

 Support for multiple websites in one session
 Export chat history
 Advanced filtering options for web scraping
 Multi-language support
 Integration with more NLP models
 PDF and document upload support
 Conversation memory across sessions


Made with ❤️ by Mehak Shaikh Mansoori

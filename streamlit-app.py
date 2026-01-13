"""
==============================================
WEBWHISPER AI - STREAMLIT INTERFACE
An intelligent chatbot that extracts insights from any website
Created by: Mehak Shaikh Mansoori
For: Relinns Technologies Assessment
==============================================
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="WebWhisper AI - Intelligent Website Chatbot",
    page_icon="🔮",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(120deg, #1f77b4, #8e44ad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        font-weight: bold;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
    }
    .info-box {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    .feature-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1f77b4;
    }
    .stats-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def scrape_website(url):
    """Scrape website content and extract readable text."""
    try:
        with st.spinner(f"🔍 WebWhisper is analyzing {url}..."):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            text = soup.get_text()
            return text, None
            
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching website: {e}"
    except Exception as e:
        return None, f"Error parsing website: {e}"


def clean_text(text):
    """Clean and normalize extracted text."""
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    max_length = 2000
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


@st.cache_resource
def load_model():
    """Load the Hugging Face model (cached for performance)."""
    try:
        model_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1
        )
        return model_pipeline, None
    except Exception as e:
        return None, f"Error loading model: {e}"


def ask_model(question, context, model_pipeline):
    """Generate answer using Hugging Face model."""
    try:
        prompt = f"""Based on the following website content, answer the question.

Website Content:
{context}

Question: {question}

Answer:"""
        
        response = model_pipeline(
            prompt,
            max_new_tokens=150,
            min_new_tokens=20,
            do_sample=False
        )
        
        answer = response[0]['generated_text'].strip()
        
        if not answer:
            return "I couldn't generate a proper answer. Please try rephrasing your question."
        
        return answer
        
    except Exception as e:
        return f"Error generating response: {e}"


def main():
    # Header with branding
    st.markdown('<h1 class="main-header">🔮 WebWhisper AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">✨ Whispers insights from any website ✨</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration Panel")
        
        website_url = st.text_input(
            "🌐 Website URL",
            value="https://botpenguin.com/",
            help="Enter the website URL to analyze",
            placeholder="https://example.com"
        )
        
        if st.button("🚀 Analyze Website", type="primary", use_container_width=True):
            if website_url:
                # Clear previous chat history
                st.session_state.messages = []
                st.session_state.context = None
                st.session_state.url_loaded = False
                st.rerun()
        
        st.markdown("---")
        
        # Stats display
        if 'context' in st.session_state and st.session_state.context:
            st.markdown("### 📊 Analysis Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stats-box">
                    <h3 style="color: #1f77b4; margin: 0;">{len(st.session_state.context)}</h3>
                    <p style="margin: 0; font-size: 0.8rem;">Characters</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stats-box">
                    <h3 style="color: #8bc34a; margin: 0;">{len(st.session_state.messages)}</h3>
                    <p style="margin: 0; font-size: 0.8rem;">Messages</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
        
        # Features section
        st.markdown("### ✨ Features")
        st.markdown("""
        <div class="feature-card">
            🔍 <strong>Smart Scraping</strong><br>
            <small>Extracts key content from any website</small>
        </div>
        <div class="feature-card">
            🤖 <strong>AI-Powered</strong><br>
            <small>Uses FLAN-T5 NLP model</small>
        </div>
        <div class="feature-card">
            💬 <strong>Natural Chat</strong><br>
            <small>Conversational Q&A interface</small>
        </div>
        <div class="feature-card">
            ⚡ <strong>Real-time</strong><br>
            <small>Instant answers to your questions</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 👨‍💻 Developer")
        st.write("**Mehak Shaikh Mansoori**")
        st.write("*Relinns Technologies*")
        st.write("NLP Engineer Assessment")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'context' not in st.session_state:
        st.session_state.context = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'url_loaded' not in st.session_state:
        st.session_state.url_loaded = False
    
    # Load model (cached)
    if st.session_state.model is None:
        with st.spinner("🔄 Initializing WebWhisper AI (this may take a minute)..."):
            model, error = load_model()
            if error:
                st.error(f"❌ {error}")
                st.info("💡 **Tip:** Make sure you have installed: `pip install transformers torch`")
                st.stop()
            st.session_state.model = model
            st.success("✅ WebWhisper AI is ready!")
    
    # Load website content if not already loaded
    if not st.session_state.url_loaded and website_url:
        raw_text, error = scrape_website(website_url)
        
        if error:
            st.error(f"❌ {error}")
        else:
            cleaned_context = clean_text(raw_text)
            
            if not cleaned_context:
                st.error("❌ No content could be extracted from this website.")
            else:
                st.session_state.context = cleaned_context
                st.session_state.url_loaded = True
                st.success(f"✅ Successfully analyzed {len(cleaned_context)} characters from the website!")
                
                # Display website preview
                with st.expander("📄 View Extracted Content Preview"):
                    st.text_area(
                        "Content Preview (First 500 characters)",
                        value=cleaned_context[:500] + "...",
                        height=200,
                        disabled=True
                    )
    
    # Main chat interface
    if st.session_state.context:
        st.markdown("### 💬 Chat with WebWhisper")
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🔮 WebWhisper:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        user_question = st.chat_input("💭 Ask me anything about this website...")
        
        if user_question:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Generate response
            with st.spinner("🔮 WebWhisper is thinking..."):
                answer = ask_model(
                    user_question,
                    st.session_state.context,
                    st.session_state.model
                )
            
            # Add bot response to history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Rerun to display new messages
            st.rerun()
        
        # Action buttons
        if st.session_state.messages:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
            with col2:
                if st.button("🔄 New Website", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.context = None
                    st.session_state.url_loaded = False
                    st.rerun()
    
    else:
        # Welcome screen when no website is loaded
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>🚀 How to Get Started</h3>
                <ol>
                    <li><strong>Enter URL:</strong> Paste a website URL in the sidebar</li>
                    <li><strong>Analyze:</strong> Click "Analyze Website" button</li>
                    <li><strong>Chat:</strong> Ask questions about the content!</li>
                </ol>
                <p><em>WebWhisper will extract and understand the website content for you.</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 💡 Example Questions")
            example_questions = [
                "🔍 What is this website about?",
                "📋 What services are offered?",
                "⭐ What are the main features?",
                "💼 Who is the target audience?",
                "🎯 What problems does it solve?",
            ]
            
            for question in example_questions:
                st.markdown(f"- {question}")
        
        with col2:
            st.markdown("""
            <div class="info-box" style="background-color: #e8f5e9; border-left-color: #4caf50;">
                <h3>🎯 Why WebWhisper AI?</h3>
                <ul>
                    <li><strong>Instant Understanding:</strong> Quickly grasp website content</li>
                    <li><strong>Smart Analysis:</strong> AI-powered insights</li>
                    <li><strong>Save Time:</strong> No need to read entire websites</li>
                    <li><strong>Ask Anything:</strong> Natural language Q&A</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box" style="background-color: #e3f2fd; border-left-color: #2196f3;">
                <h3>🔧 Technical Stack</h3>
                <ul>
                    <li>🤖 <strong>NLP:</strong> FLAN-T5 (Hugging Face)</li>
                    <li>🕷️ <strong>Scraping:</strong> BeautifulSoup4</li>
                    <li>🎨 <strong>Interface:</strong> Streamlit</li>
                    <li>🐍 <strong>Language:</strong> Python 3.8+</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
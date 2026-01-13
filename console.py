"""
==============================================
WEBWHISPER AI - CONSOLE VERSION
An intelligent chatbot that extracts insights from any website
Created by: Mehak Shaikh Mansoori
For: Relinns Technologies Assessment
==============================================

STEP-BY-STEP EXPLANATION OF IMPLEMENTATION
==============================================

STEP 1: ENVIRONMENT SETUP
- Imported required libraries: requests (HTTP), BeautifulSoup (HTML parsing), re (text cleaning)
- Imported transformers from Hugging Face for local model inference
- Used pipeline API for simplified model interaction
- Selected 'google/flan-t5-base' model (lightweight, suitable for Q&A tasks)

STEP 2: WEBSITE DATA EXTRACTION
- Created scrape_website() function that:
  * Sends GET request to provided URL with timeout
  * Parses HTML using BeautifulSoup with 'html.parser'
  * Removes script, style, and navigation tags for cleaner text
  * Extracts all visible text content
  * Implements error handling for network issues

STEP 3: DATA PROCESSING
- Created clean_text() function that:
  * Removes extra whitespace and newlines
  * Normalizes spaces to single space
  * Strips leading/trailing whitespace
  * Limits text to 2000 characters to prevent model overload
  * Returns cleaned, truncated text suitable for model input

STEP 4: NLP / CHATBOT IMPLEMENTATION
- Created ask_model() function that:
  * Uses Hugging Face transformers pipeline with 'text2text-generation' task
  * Constructs prompt combining website context and user question
  * Uses FLAN-T5 model which is trained for instruction-following
  * Generates response with max_length=200, min_length=20
  * Returns model-generated answer

STEP 5: CONSOLE-BASED INTERACTION
- Created run_chatbot() function that:
  * Implements infinite loop for continuous interaction
  * Accepts user input via input()
  * Checks for 'exit' command to break loop
  * Calls ask_model() for each question
  * Prints formatted responses
  * Handles empty inputs gracefully

STEP 6: CODE QUALITY & DOCUMENTATION
- Organized code into clear functions with single responsibilities
- Added comprehensive docstrings for each function
- Included inline comments explaining key operations
- Implemented try-except blocks for error handling
- Added main() function as entry point
- Used __name__ == "__main__" pattern for script execution

BONUS FEATURES IMPLEMENTED:
- HTTP error handling with try-except and status code checking
- Empty response validation
- Graceful handling of invalid URLs
- User-friendly error messages
- Startup confirmation message
- Clean exit mechanism
- Branded console interface with ASCII art

MODEL CHOICE RATIONALE:
- FLAN-T5-base: Instruction-tuned model, excellent for Q&A
- Runs locally without API token requirement
- Balanced between performance and resource usage
- 220M parameters - efficient for CPU inference
- Alternative: Can easily switch to flan-t5-large for better quality

USAGE:
1. Install dependencies: pip install requests beautifulsoup4 transformers torch
2. Run script: python webwhisper_console.py
3. Script will load model and scrape website automatically
4. Type questions about the website content
5. Type 'exit' to quit

==============================================
"""

import requests
from bs4 import BeautifulSoup
import re
from transformers import pipeline
import warnings

# Suppress warnings for cleaner console output
warnings.filterwarnings('ignore')


def print_banner():
    """Display WebWhisper AI branding banner."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🔮  W E B W H I S P E R   A I  🔮              ║
║                                                          ║
║          Whispers insights from any website              ║
║                                                          ║
║          Created by: Mehak Shaikh Mansoori               ║
║          For: Relinns Technologies Assessment            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def scrape_website(url):
    """
    Scrape website content and extract readable text.
    
    Args:
        url (str): The website URL to scrape
        
    Returns:
        str: Extracted text content from the website
        None: If scraping fails
    """
    try:
        # Send HTTP GET request with timeout
        print(f"🔍 WebWhisper is analyzing {url}...")
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and navigation elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Extract all text content
        text = soup.get_text()
        
        return text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"❌ Error parsing website: {e}")
        return None


def clean_text(text):
    """
    Clean and normalize extracted text.
    
    Args:
        text (str): Raw text from website
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Limit text length to avoid model overload (keep first 2000 chars)
    # This ensures we stay within model's context window
    max_length = 2000
    if len(text) > max_length:
        text = text[:max_length] + "..."
        print(f"ℹ️  Text truncated to {max_length} characters for optimal processing.")
    
    return text


def ask_model(question, context, model_pipeline):
    """
    Generate answer using Hugging Face model based on context and question.
    
    Args:
        question (str): User's question
        context (str): Website content as context
        model_pipeline: Hugging Face pipeline object
        
    Returns:
        str: Model-generated answer
    """
    try:
        # Construct prompt with context and question
        # FLAN-T5 works well with instruction-style prompts
        prompt = f"""Based on the following website content, answer the question.

Website Content:
{context}

Question: {question}

Answer:"""
        
        # Generate response using the model
        response = model_pipeline(
            prompt,
            max_new_tokens=150,
            min_new_tokens=20,
            do_sample=False
        )
        
        # Extract generated text from response
        answer = response[0]['generated_text'].strip()
        
        # Handle empty responses
        if not answer:
            return "I couldn't generate a proper answer. Please try rephrasing your question."
        
        return answer
        
    except Exception as e:
        return f"❌ Error generating response: {e}"


def run_chatbot(context, model_pipeline):
    """
    Run the console-based chatbot loop.
    
    Args:
        context (str): Website content to use as knowledge base
        model_pipeline: Hugging Face pipeline object
    """
    print("\n" + "="*60)
    print("✅ WebWhisper AI is ready!")
    print("="*60)
    print("\n💡 Tips:")
    print("   • Ask questions about the website content")
    print("   • Type 'exit' to quit")
    print("   • Type 'help' for example questions")
    print("\n" + "="*60 + "\n")
    
    # Continuous interaction loop
    while True:
        # Get user input
        user_question = input("👤 You: ").strip()
        
        # Check for exit command
        if user_question.lower() == 'exit':
            print("\n" + "="*60)
            print("👋 Thank you for using WebWhisper AI. Goodbye!")
            print("="*60)
            break
        
        # Show help
        if user_question.lower() == 'help':
            print("\n📋 Example questions you can ask:")
            print("   • What is this website about?")
            print("   • What services does this website offer?")
            print("   • What are the main features?")
            print("   • Tell me about the company")
            print("   • What problems does it solve?\n")
            continue
        
        # Skip empty inputs
        if not user_question:
            print("⚠️  Please enter a question.\n")
            continue
        
        # Generate and print response
        print("\n🔮 WebWhisper: ", end="")
        answer = ask_model(user_question, context, model_pipeline)
        print(answer + "\n")


def main():
    """
    Main function to orchestrate the chatbot workflow.
    """
    # Display banner
    print_banner()
    
    # Configuration
    website_url = "https://botpenguin.com/"
    
    print("\n" + "="*60)
    print("Starting WebWhisper AI initialization...")
    print("="*60 + "\n")
    
    # STEP 1: Scrape website
    raw_text = scrape_website(website_url)
    
    if not raw_text:
        print("❌ Failed to scrape website. Exiting.")
        return
    
    # STEP 2: Clean and process text
    cleaned_context = clean_text(raw_text)
    
    if not cleaned_context:
        print("❌ No content extracted from website. Exiting.")
        return
    
    print(f"✅ Successfully extracted {len(cleaned_context)} characters of content.\n")
    
    # STEP 3: Load NLP model
    print("🔄 Loading AI model (this may take a minute)...")
    print("   Model: FLAN-T5-base (Hugging Face)")
    print("   Task: Text-to-Text Generation\n")
    
    try:
        # Initialize text generation pipeline with FLAN-T5 model
        # FLAN-T5 is instruction-tuned and works well for Q&A tasks
        model_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1  # Use CPU (-1), set to 0 for GPU
        )
        print("✅ Model loaded successfully!\n")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("\n💡 Please install required packages:")
        print("   pip install transformers torch")
        return
    
    # STEP 4: Run chatbot
    run_chatbot(cleaned_context, model_pipeline)


if __name__ == "__main__":
    main()

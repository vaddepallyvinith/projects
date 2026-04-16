# Neural PDF Reader

A sleek, intuitive web application that allows you to upload PDF documents and converse with them using Google's powerful Gemini AI capabilities. 

Built with a premium dark-mode glassmorphic user interface to provide a top-tier aesthetic and reading experience.

## Features
- **Native PDF Context Processing**: Upload PDFs directly to the Gemini Context Window for near-instant full-document memory.
- **Premium Glassmorphic UI**: Beautiful dark-mode design with glowing gradients and interactive hover animations.
- **Responsive Chat Interface**: Clean chat bubbles separating user and bot responses with built-in markdown text rendering.
- **Lightweight Backend**: Driven by Flask for incredibly fast and lightweight execution.

## Prerequisites

- Python 3.8+
- An API Key from Google AI Studio ([Get it here](https://aistudio.google.com/app/apikey))

## Setup Instructions

1. **Activate the Virtual Environment**
   Navigate to the project directory and load standard dependencies:
   ```bash
   cd /home/vinith/Python/mychatbot
   source venv/bin/activate
   ```

2. **Add Your API Key**
   Ensure you have a file named `.env` in the root directory (alongside `app.py`). Add your Gemini API key inside it like this:
   ```env
   API_KEY=your_actual_api_key_here
   ```

3. **Install Dependencies**
   (If you haven't already installed them in your virtual environment):
   ```bash
   pip install flask python-dotenv google-generativeai
   ```

## Running the Application

1. From within your activated virtual environment, start the server:
   ```bash
   python3 app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
3. Click the **"Select PDF"** button, select your document, and click **"Initialize Context"**.
4. Once initialized, ask the bot anything about the content of your PDF!

## Architecture files
- `app.py`: The Flask server routing logic and Gemini File upload orchestrator.
- `rag_chatbot.py`: A command-line fallback version of the chatbot.
- `templates/index.html`: The HTML, CSS, and vanilla JS for the graphical interface. 


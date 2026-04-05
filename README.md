# Classical Language Query Assistant

This app uses modern AI models to answer grammatical and syntactic questions about Latin and Greek passages. It's designed for use in research and pedagogy, especially in classical language instruction.

## Features
- Supports Syntax and Morphology question sets
- Pulls questions live from shared Google Docs
- Uses Claude 3, GPT-3.5, and other fallback models via OpenRouter
- Automatically attributes which model answered each question

## How to Run
1. Clone or download this repo  
2. Install dependencies and launch the app:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

The app will open automatically in your browser with a public Gradio link.

## Configuration
API keys, model priorities, and document URLs can be adjusted in `config.py`.

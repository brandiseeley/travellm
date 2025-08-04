# Time Travel LLM - 1861

A simple RAG system that answers questions as if you're talking to someone from 1861, using historical newspaper articles.

## Quick Start

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Set up your OpenAI API key:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the web app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Go to http://localhost:8000

5. **Ask questions!**
   Try questions like:
   - "How can I treat a fever?"
   - "What's happening with the war?"
   - "What's the latest news from Washington?"

## How it works

The system uses:
- Local 1861 newspaper articles (from `data/articles_1861_sample/`)
- Library of Congress API for additional historical context
- OpenAI embeddings and GPT-4 for responses
- A conversational interface that responds as someone from 1861

## Files

- `app.py` - Simple Flask web interface
- `src/rag.py` - Main RAG system
- `data/` - Historical newspaper articles
- `prototype.ipynb` - Development notebook 
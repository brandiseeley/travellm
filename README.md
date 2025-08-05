# Time Travel LLM - 1861

> Note: For submission writeup and loom video, see `WRITEUP.md`!

A simple RAG system that answers questions as if you're talking to someone from 1861, using historical newspaper articles.

### Installing Dependencies & API Setup

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Set up your OpenAI API key:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_api_key_here
   LANGSMITH_API_KEY=your_api_key_here
   ```

   You only need the OpenAI API key and may run the app without tracing if you want.

### Creating Embeddings

1. **Create a postgres database called `historical_documents`

2. Configure `data/fetch_data.py` with a `YEAR` and `MAX_ARTICLES`. You can choose a year between 1780-1960. Run `fetch_data.py`. Otherwise, you may use the `demo_articles_1861` directory and skip this step, though this directory only contains 50 articles.

3. Set `PATH` within `embed_articles.py` to the new directory that's been created within `data`. Alternatively, set it as `"../data/demo_articles_1861"`. Run `embed_articles.py` from the `src` directory.

## Run the web app

1. From the root directory, run `python app.py`

2. Visit [http://localhost:8000](http://localhost:8000) in your browser

3. **Ask questions!**
   Try questions like:
   - "How can I treat a fever?"
   - "What's happening with the war?"
   - "What's the latest news from Washington?"

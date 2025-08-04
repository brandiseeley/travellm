import os
import sys
from dotenv import load_dotenv
from ragas.testset import TestsetGenerator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, JSONLoader
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Load the articles from the directory using the same approach as embed_articles.py
path = "../data/articles_1861_sample"

def metadata_func(record, metadata):
    metadata["newspaper_name"] = record.get("newspaper_name")
    metadata["date"] = record.get("date")
    
    return metadata

directory_loader = DirectoryLoader(
    path,
    glob="*.json",
    loader_cls=JSONLoader,
    loader_kwargs={
        "jq_schema": '.',
        "content_key": "article",
        "metadata_func": metadata_func,
    }
)

article_resources = directory_loader.load()

# Set up LLM and embedding models
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini", temperature=0.1))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

# Create testset generator
generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)

# Generate synthetic dataset
print("Generating synthetic dataset...")
dataset = generator.generate_with_langchain_docs(article_resources[:20], testset_size=5)

# Save the dataset as JSON
import pandas as pd
df = dataset.to_pandas()
df.to_json("../data/synthetic_dataset.json", orient="records", indent=2)
print(f"Dataset saved with {len(dataset)} examples to data/synthetic_dataset.json")
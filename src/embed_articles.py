import tiktoken
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

# Load the articles from the directory
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

# Chunk the articles

def tiktoken_len(text):
    tokens = tiktoken.encoding_for_model("gpt-4o").encode(
        text,
    )
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 750,
    chunk_overlap = 0,
    length_function = tiktoken_len,
)

article_resource_chunks = text_splitter.split_documents(article_resources)

# print('here', article_resource_chunks[0].page_content)
# print('here again', article_resource_chunks[0].metadata['newspaper_name'])
# print('here again', article_resource_chunks[0].metadata['date'])

# Connect to the database

load_dotenv()

# Database connection parameters
connection_string = "postgresql://postgres:postgres@localhost:5432/historical_documents"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create PGVector instance
vectorstore = PGVector(
    collection_name="newspaper_articles",
    connection=connection_string,
    embeddings=embeddings,
    use_jsonb=True,
)

def embed_and_store_articles(article_chunks, batch_size=100):
    """
    Embed article chunks using OpenAI text-embeddings-3-small and store in PGVector.
    
    Args:
        article_chunks: List of document chunks to embed
        batch_size: Number of chunks to process in each batch
    """
    try:
        # Process chunks in batches
        for i in range(0, len(article_chunks), batch_size):
            batch = article_chunks[i:i + batch_size]
            
            # Add documents to PGVector (this handles embeddings automatically)
            vectorstore.add_documents(batch)
            
            print(f"Processed batch {i//batch_size + 1}/{(len(article_chunks) + batch_size - 1)//batch_size}")
    
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    embed_and_store_articles(article_resource_chunks)


import tiktoken
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
import openai

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader

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

DB_CONFIG = {
    "dbname": "historical_documents",
    "user": "postgres",
    "host": "localhost",
    "port": 5432,
}

def embed_and_store_articles(article_chunks, batch_size=100):
    """
    Embed article chunks using OpenAI text-embeddings-3-small and store in database.
    
    Args:
        article_chunks: List of document chunks to embed
        batch_size: Number of chunks to process in each batch
    """
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Connect to database
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Process chunks in batches
        for i in range(0, len(article_chunks), batch_size):
            batch = article_chunks[i:i + batch_size]
            
            # Prepare texts for embedding
            texts = [chunk.page_content for chunk in batch]
            
            # Get embeddings from OpenAI
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            # Insert embeddings into database
            for j, chunk in enumerate(batch):
                embedding = response.data[j].embedding
                metadata = chunk.metadata
                
                # Parse date if it exists
                date_value = None
                year_value = None
                if metadata.get("date"):
                    try:
                        date_obj = datetime.strptime(metadata["date"], "%Y-%m-%d")
                        date_value = date_obj.date()
                        year_value = date_obj.year
                    except (ValueError, TypeError):
                        # If date parsing fails, try to extract year from the date string
                        try:
                            year_value = int(metadata["date"][:4])
                        except (ValueError, IndexError):
                            year_value = None
                
                cursor.execute("""
                    INSERT INTO newspaper_articles 
                    (embedding, date, newspaper_name, year, article) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    embedding,
                    date_value,
                    metadata.get("newspaper_name"),
                    year_value,
                    chunk.page_content
                ))
            
            # Commit batch
            conn.commit()
            print(f"Processed batch {i//batch_size + 1}/{(len(article_chunks) + batch_size - 1)//batch_size}")
    
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    embed_and_store_articles(article_resource_chunks)


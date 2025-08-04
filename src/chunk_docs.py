import os
from dotenv import load_dotenv

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
from langchain_openai.embeddings import OpenAIEmbeddings

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load the articles from the directory
path = "../data/articles_1861_sample"

directory_loader = DirectoryLoader(
    path,
    glob="*.json",
    loader_cls=JSONLoader,
    loader_kwargs={
        "jq_schema": '"Newspaper: \(.newspaper_name)\nDate: \(.date)\n\n\(.article)"',
        "text_content": True,
    }
)

article_resources = directory_loader.load()

# print(article_resources[0])

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

# Embed the chunks

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
client = QdrantClient(":memory:")

client.create_collection(
    collection_name="articles_1861",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="articles_1861",
    embedding=embedding_model,
)

vector_store.add_documents(documents=article_resource_chunks)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_loaders import DirectoryLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
import os

# Handle import for both direct execution and module import
try:
    from .multiquery_retriever import multiquery_retriever
except ImportError:
    from multiquery_retriever import multiquery_retriever

# Load and chunk documents (same process as embed_articles.py)
def load_and_chunk_documents():
    """Load articles and create chunks for BM25Retriever"""
    PATH = os.path.join(os.path.dirname(__file__), "..", "data", "articles_1861_sample")
    
    def metadata_func(record, metadata):
        metadata["newspaper_name"] = record.get("newspaper_name")
        metadata["date"] = record.get("date")
        return metadata
    
    directory_loader = DirectoryLoader(
        PATH,
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
        tokens = tiktoken.encoding_for_model("gpt-4o").encode(text)
        return len(tokens)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=0,
        length_function=tiktoken_len,
    )
    
    return text_splitter.split_documents(article_resources)

# Create BM25Retriever with proper chunks
document_chunks = load_and_chunk_documents()
bm25_retriever = BM25Retriever.from_documents(document_chunks)

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, multiquery_retriever], weights=[0.5, 0.5]
)
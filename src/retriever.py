from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
connection_string = "postgresql://postgres:postgres@localhost:5432/historical_documents"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Connect to existing table
vectorstore = PGVector(
    collection_name="newspaper_articles",
    connection=connection_string,
    embeddings=embeddings,
    use_jsonb=True,
)

# Simple similarity search retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # return top 5 results
)

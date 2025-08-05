from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
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

# Create the base retriever
base_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # return top 5 results
)

# Create LLM for query generation
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create MultiQueryRetriever
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, 
    llm=llm
)

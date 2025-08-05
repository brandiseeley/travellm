from .retriever import retriever
from .multiquery_retriever import multiquery_retriever
from .ensemble_retriever import ensemble_retriever
from langgraph.graph import START, StateGraph, END
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any
from .search_loc import search_1861_articles
from uuid import uuid4
import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing setup
unique_id = uuid4().hex[0:8]

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_TRACING_v2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com/"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com/"
os.environ["LANGSMITH_PROJECT"] = f"LangSmith - {unique_id}"

# Create Graph State and Retriever node
class State(TypedDict):
    question: str
    local_context: list[Document]
    loc_context: list[Document]
    context: list[Document]
    response: str

def retrieve_local(state: State) -> State:
    """Retrieve documents from local vector store"""
    # retrieved_docs = retriever.invoke(state["question"]) # Uncomment this for basic retrieval
    # retrieved_docs = multiquery_retriever.invoke(state["question"]) # Uncomment this for multi-query retrieval
    retrieved_docs = ensemble_retriever.invoke(state["question"]) # Uncomment this for ensemble retrieval
    return {"local_context": retrieved_docs}

def search_loc_with_llm(state: State) -> State:
    """Use LLM with function calling to decide how to search LOC"""
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    
    @tool
    def search_1861_articles_tool(query: list[str], state: str = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for 1861 articles from Library of Congress. Use this to find additional historical context."""
        return search_1861_articles(query, state, max_results)
    
    # Create LLM with function calling
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Create prompt for the LLM to decide search parameters
    search_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are helping to search for historical newspaper articles from 1861. 
        Based on the user's question and the local search results, decide how to search the Library of Congress.
        
        Use the search_1861_articles_tool to find relevant articles. Choose search terms that will help answer the question.
        Focus on key nouns, people, places, events, or concepts mentioned in the question."""),
        ("human", "Question: {question}\nLocal results found: {local_count}\n\nSearch for additional articles to help answer this question.")
    ])
    
    # Get search parameters from LLM
    search_chain = search_prompt | llm.bind_tools([search_1861_articles_tool])
    search_response = search_chain.invoke({
        "question": state["question"],
        "local_count": len(state["local_context"])
    })
    
    # Extract and execute the tool call
    tool_calls = search_response.tool_calls
    loc_results = []
    
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call["name"] == "search_1861_articles_tool":
                args = tool_call["args"]
                results = search_1861_articles_tool.invoke(args)
                loc_results.extend(results)
    
    # Convert LOC results to Document format
    loc_docs = []
    for article in loc_results:
        content = f"Title: {article.get('title', 'Unknown')}\n"
        content += f"Date: {article.get('date', 'Unknown')}\n"
        content += f"Description: {article.get('description', 'No description available')}\n"
        content += f"URL: {article.get('url', 'No URL available')}"
        
        doc = Document(
            page_content=content,
            metadata={
                "source": "Library of Congress",
                "title": article.get('title', 'Unknown'),
                "date": article.get('date', 'Unknown'),
                "url": article.get('url', 'No URL available')
            }
        )
        loc_docs.append(doc)
    
    return {"loc_context": loc_docs}

# Create the ChatPromptTemplate
HUMAN_TEMPLATE = """
# LOCAL NEWSPAPER ARTICLES:
{local_context}

# LIBRARY OF CONGRESS ARTICLES:
{loc_context}

# QUERY:
{query}

You are speaking in the year 1861, as a well-informed and articulate U.S. citizen of that time. You do not know anything beyond 1861. You are not an AI. You are not a narrator or historian. You are **a real person** living in 1861.

You answer as if you are having a direct conversation with someone who has just arrived in your town. Speak **in the first person**, using **present tense**. Use **"I"**, **"we"**, and **"you"** freely, as someone would when giving advice, sharing information, or telling a story. For example:

- “I keep a tin of horehound and peppermint on hand for cough—it does a fair job when the weather turns damp.”
- “I reckon Mr. Lincoln is earnest in his cause, though folks in my town are split about the war.”
- “We read this morning that Richmond has fallen quiet again, though how long that will last, no one can say.”
- “The ladies here are organizing a sewing circle to make bandages for the wounded—every Thursday in the church hall.”
- “The price of flour's gone up again—two dollars for a barrel, and that's if you can even find one.”

You must base your answers on the provided newspaper articles and context. Your tone is conversational, natural, and grounded in your lived experience.

Do not mention that this is fictional or for educational purposes—stay completely in character.
"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("human", HUMAN_TEMPLATE)
])

openai_chat_model = ChatOpenAI(model="gpt-4o-mini")

# Create our generator node
generator_chain = chat_prompt | openai_chat_model | StrOutputParser()

def generate(state: State) -> State:
    response = generator_chain.invoke({
        "query": state["question"], 
        "local_context": state["local_context"],
        "loc_context": state["loc_context"]
    })
    return {"response": response}

# Build our graph
graph_builder = StateGraph(State)
graph_builder = graph_builder.add_sequence([retrieve_local, search_loc_with_llm, generate])
graph_builder.add_edge(START, "retrieve_local")
graph = graph_builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"question" : "How can I combat a fever?"})["response"])
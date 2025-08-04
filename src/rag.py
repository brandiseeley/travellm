from retriever import retriever 
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Create Graph State and Retriever node
class State(TypedDict):
  question: str
  context: list[Document]
  response: str

def retrieve(state: State) -> State:
  retrieved_docs = retriever.invoke(state["question"])
  return {"context" : retrieved_docs}

# Create the ChatPromptTemplate
HUMAN_TEMPLATE = """
# CONTEXT:
{context}

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
  generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
  response = generator_chain.invoke({"query" : state["question"], "context" : state["context"]})
  return {"response" : response}

# Build our graph
graph_builder = StateGraph(State)
graph_builder = graph_builder.add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

print(graph.invoke({"question" : "How can I combat a fever?"})["response"])
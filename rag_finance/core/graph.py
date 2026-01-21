import logging
from typing import Any

from langchain_core.prompts import PromptTemplate
from langgraph.graph import START, StateGraph

from rag_finance.core.index import load_pdf, store_pages
from rag_finance.core.models import llm, State
from rag_finance.core.prompts import custom_rag_prompt

logger = logging.getLogger(__name__)

FILE_NAME = "Nubank_2025-06-20.pdf"


async def retrieve(state: State) -> State:
    pages = await load_pdf(FILE_NAME)
    vector_store = store_pages(pages)
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State, prompt: PromptTemplate = custom_rag_prompt, model: Any = llm) -> dict:
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = model.invoke(messages)
    return {"answer": response.content}

async def question(question: str) -> str:
    logger.info(f"Processing question: {question}")
    
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    result = await graph.ainvoke({"question": question})
    
    answer = result["answer"]
    logger.info(f"Full answer: {answer}")

    return answer

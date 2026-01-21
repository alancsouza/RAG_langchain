from typing import List, TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


llm = init_chat_model("gpt-4o-mini", model_provider="openai")

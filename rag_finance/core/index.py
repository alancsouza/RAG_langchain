from typing import Any, List
from os.path import join

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

FILE_PATH = "rag_finance/data"


async def load_pdf(file_name: str) -> List[Document]:
    file_path = join(FILE_PATH, file_name)
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)

    return pages


def store_pages(pages: List[Document], enbedings: Any = OpenAIEmbeddings) -> InMemoryVectorStore:
    return InMemoryVectorStore.from_documents(pages, enbedings())

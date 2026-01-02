from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List


def build_faiss_index(
    docs: List[Document],
    embedding_model,
):
    """
    Build FAISS vector store from documents
    """
    vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="./chroma_db",
    )

    return vectorstore

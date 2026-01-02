from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_documents(
    docs: List[Document],
    chunk_size: int = 700,
    chunk_overlap: int = 100,
) -> List[Document]:
    """
    Split documents into token-sized chunks
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,  # token approximation (safe default)
    )

    chunked_docs = splitter.split_documents(docs)

    # Add chunk index for traceability
    for i, doc in enumerate(chunked_docs):
        doc.metadata["chunk_id"] = i

    return chunked_docs

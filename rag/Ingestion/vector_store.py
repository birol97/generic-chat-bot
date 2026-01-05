# rag/Ingestion/vector_store.py

import json
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma

def filter_complex_metadata(docs: List[Document]) -> List[Document]:
    """
    Chroma ONLY allows scalar metadata.
    Convert images(list) → JSON string.
    """
    safe_docs = []

    for doc in docs:
        safe_meta = {}

        for k, v in doc.metadata.items():
            if k == "images":
                # 🔑 CRITICAL FIX
                safe_meta["images"] = json.dumps(v or [])
            elif isinstance(v, (str, int, float, bool)) or v is None:
                safe_meta[k] = v

        safe_docs.append(
            Document(
                page_content=doc.page_content,
                metadata=safe_meta,
            )
        )

    return safe_docs


def build_faiss_index(docs: List[Document], embedding_model):
    # ✅ MUST BE CALLED HERE
    safe_docs = filter_complex_metadata(docs)

    vectorstore = Chroma.from_documents(
        documents=safe_docs,
        embedding=embedding_model,
        persist_directory="./chroma_db",
    )

    return vectorstore

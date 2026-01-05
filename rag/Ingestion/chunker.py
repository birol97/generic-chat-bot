from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import copy
import json


def chunk_documents(docs, chunk_size=700, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunked_docs = splitter.split_documents(docs)

    for i, doc in enumerate(chunked_docs):
        doc.metadata["chunk_id"] = i

        images = doc.metadata.get("images", [])

        # 🔒 FORCE SAFE FORMAT
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except Exception:
                images = []

        if not isinstance(images, list):
            images = []

        # 🔑 THIS IS CRITICAL
        doc.metadata["images"] = images

    return chunked_docs

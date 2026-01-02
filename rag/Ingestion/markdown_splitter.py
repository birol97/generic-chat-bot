from typing import List
from chunker import chunk_documents
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

from document_loader import MarkdownDocumentLoader


def split_by_headers(docs: List[Document]) -> List[Document]:
    headers_to_split_on = [
    ("###", "subsubsection"),
    ("##", "subsection"),
    ("#", "section"),
    ]


    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    split_docs: List[Document] = []

    for doc in docs:
        sections = splitter.split_text(doc.page_content)

        for section in sections:
            section.metadata.update(doc.metadata)

            section.metadata["header_path"] = " > ".join(
                filter(
                    None,
                    [
                        section.metadata.get("section"),
                        section.metadata.get("subsection"),
                        section.metadata.get("subsubsection"),
                    ],
                )
            )

            section = inject_headers(section)
            split_docs.append(section)

    return split_docs


def inject_headers(doc: Document) -> Document:
    header_map = [
        ("section", "# "),
        ("subsection", "## "),
        ("subsubsection", "### "),
    ]

    lines = []

    for key, prefix in header_map:
        value = doc.metadata.get(key)
        if value:
            lines.append(f"{prefix}{value}")

    if lines:
        doc.page_content = "\n".join(lines) + "\n" + doc.page_content

    return doc


if __name__ == "__main__":
    from pathlib import Path

    base_dir = Path(__file__).resolve().parent.parent.parent
    loader = MarkdownDocumentLoader(base_dir / "docs" / "cv")
    docs = loader.load()
    print(repr(docs[0].page_content[:200]))

    split_docs = split_by_headers(docs)
    chunked_docs = chunk_documents(split_docs)
    
    print(f"Loaded docs: {len(docs)}")
    print(f"Header split docs: {len(split_docs)}")
    print(f"Token chunks: {len(chunked_docs)}\n")

    print("Sample chunk:")
    print(chunked_docs[0].page_content[:300])
    print(chunked_docs[0].metadata)

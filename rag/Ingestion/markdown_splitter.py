from typing import List
from pathlib import Path
import re

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

from document_loader import MarkdownDocumentLoader
from chunker import chunk_documents


IMAGE_REGEX = re.compile(r"!\[.*?\]\((.*?)\)")


def extract_images_from_text(
    text: str, markdown_file: Path
) -> List[str]:
    """
    Extract image paths from markdown and resolve them
    relative to the markdown file.
    """
    images = []

    for match in IMAGE_REGEX.finditer(text):
        raw_path = match.group(1)

        resolved = (markdown_file.parent / raw_path).resolve()
        if resolved.exists():
            images.append(str(resolved))

    return images


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

        # 👇 inherit everything EXCEPT images
        base_metadata = {
            k: v for k, v in doc.metadata.items() if k != "images"
        }

        for section in sections:
            section.metadata = {
                **base_metadata,
                **section.metadata,
            }

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
            section = attach_images_to_chunk(section)
            split_docs.append(section)

    return split_docs


IMAGE_PATTERN = re.compile(r"!\[.*?\]\((.*?)\)")
def attach_images_to_chunk(doc: Document) -> Document:
    matches = IMAGE_PATTERN.findall(doc.page_content)

    images = []
    for path in matches:
        images.append(path.replace("../", ""))

    doc.metadata["images"] = images
    return doc

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
    base_dir = Path(__file__).resolve().parent.parent.parent
    loader = MarkdownDocumentLoader(base_dir / "docs" / "cv")
    docs = loader.load()

    split_docs = split_by_headers(docs)
    chunked_docs = chunk_documents(split_docs)

    print(f"Loaded docs: {len(docs)}")
    print(f"Header split docs: {len(split_docs)}")
    print(f"Token chunks: {len(chunked_docs)}\n")

    print("Sample chunk:")
    print(chunked_docs[0].page_content[:300])
    print(chunked_docs[0].metadata)

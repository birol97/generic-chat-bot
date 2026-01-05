from langchain_core.documents import Document
from typing import List
import re
def dedupe_documents(docs: List[Document]) -> List[Document]:
    seen = set()
    unique = []

    for doc in docs:
        key = (
            doc.metadata.get("file_name"),
            doc.metadata.get("header_path"),
            doc.page_content.strip(),
        )

        if key not in seen:
            seen.add(key)
            unique.append(doc)

    return unique
def normalize_pdf_text(text: str) -> str:
    # Fix spaced characters: "F a z" → "Faz"
    text = re.sub(r"(?<=\w)\s(?=\w)", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()    
def normalize_images(docs):
    for doc in docs:
        images = doc.metadata.get("images", [])

        # Convert JSON string → list
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except Exception:
                images = []

        doc.metadata["images"] = images

    return docs
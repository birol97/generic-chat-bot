from pathlib import Path
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document


class MarkdownDocumentLoader:
    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)

        if not self.docs_path.exists():
            raise FileNotFoundError(f"Docs path not found: {docs_path}")

    def load(self) -> List[Document]:
        loader = DirectoryLoader(
            path=str(self.docs_path),
            glob="**/*.md",
            loader_cls=TextLoader,          # ✅ KEEP MARKDOWN
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
        )

        documents = loader.load()

        # Normalize metadata (KEEP THIS)
        for doc in documents:
            doc.metadata = {
                "source": doc.metadata.get("source"),
                "file_name": Path(doc.metadata.get("source", "")).name,
                "file_type": "markdown",
            }

        return documents


if __name__ == "__main__":
    loader = MarkdownDocumentLoader("./docs")
    docs = loader.load()

    print(repr(docs[0].page_content[:200]))
    print(docs[0].metadata)

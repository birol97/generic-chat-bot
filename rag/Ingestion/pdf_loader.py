from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path

class PDFDocumentLoader:
    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)

    def load(self) -> list[Document]:
        documents = []

        for pdf in self.docs_path.glob("**/*.pdf"):
            loader = PyPDFLoader(str(pdf))
            pages = loader.load()

            for page in pages:
                page.metadata = {
                    "source": str(pdf),
                    "file_name": pdf.name,
                    "file_type": "pdf",
                    "page": page.metadata.get("page"),
                }
                documents.append(page)

        return documents

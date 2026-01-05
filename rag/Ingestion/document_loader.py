from pathlib import Path
from typing import List
import re
import json
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

IMAGE_REGEX = re.compile(r"!\[.*?\]\((.*?)\)")

class MarkdownDocumentLoader:
    def __init__(self, docs_root: str, markdown_subdir="cv", images_subdir="images"):
        self.docs_root = Path(docs_root).resolve()
        self.markdown_dir = self.docs_root / markdown_subdir
        self.images_dir = self.docs_root / images_subdir

        if not self.markdown_dir.exists():
            raise FileNotFoundError(f"Markdown dir not found: {self.markdown_dir}")

    def load(self) -> List[Document]:
        loader = DirectoryLoader(
            path=str(self.markdown_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
        )

        documents = loader.load()
        
        for doc in documents:
            source_path = (self.docs_root / doc.metadata["source"]).resolve()

            raw_images = IMAGE_REGEX.findall(doc.page_content)
            resolved_images = []

            for img in raw_images:
                # 🔑 Resolve relative to the markdown file location
                img_path = (source_path.parent / img).resolve()

                if img_path.exists():
                    resolved_images.append(
                    str(img_path.relative_to(self.docs_root))
                    )

            doc.metadata = {
                "source": str(source_path.relative_to(self.docs_root)),
                "file_name": source_path.name,
                "file_type": "markdown",
                "images": json.dumps(resolved_images),
                }
            print(doc.metadata)
        return documents


if __name__ == "__main__":
    loader = MarkdownDocumentLoader("./docs")
    docs = loader.load()

    
    print(docs[1].metadata)

import fitz  # PyMuPDF
import json
from pathlib import Path
from langchain_core.documents import Document
from typing import List

class PDFDocumentLoader:
    def __init__(self, pdf_dir: Path, image_output_dir: Path):
        self.pdf_dir = pdf_dir
        self.image_output_dir = image_output_dir
        self.image_output_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Document]:
        documents = []

        for pdf_path in self.pdf_dir.glob("**/*.pdf"):
            doc = fitz.open(pdf_path)

            for page_index, page in enumerate(doc):
                text = page.get_text().strip()
                images = []

                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    ext = base_image["ext"]

                    img_name = f"{pdf_path.stem}_page{page_index+1}_{img_index}.{ext}"
                    img_path = self.image_output_dir / img_name

                    with open(img_path, "wb") as f:
                        f.write(image_bytes)

                    images.append(f"images/pdf/{img_name}")

                if text:
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": str(pdf_path.relative_to(self.pdf_dir.parent)),
                                "file_name": pdf_path.name,
                                "page": page_index + 1,
                                "file_type": "pdf",
                                # 🔑 CRITICAL FIX
                                "images": json.dumps(images),
                            },
                        )
                    )

        # Debug proof
        for d in documents[:3]:
            print("IMAGES IN DOC (STRING):", d.metadata.get("images"))

        return documents

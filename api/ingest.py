from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import tempfile

from rag.Ingestion.pdf_loader import PDFDocumentLoader
from rag.Ingestion.chunker import chunk_documents
from rag.retrieval.vectorstore import get_vectorstore
from rag.Ingestion.utils import dedupe_documents,normalize_images,normalize_pdf_text

router = APIRouter()

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    base_dir = Path(__file__).resolve().parent.parent.parent
    print(base_dir)
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files supported"}

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / file.filename

        # Save uploaded PDF to temporary directory
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Load and chunk documents
        loader = PDFDocumentLoader(
            pdf_dir=pdf_path.parent,
            image_output_dir=Path("docs/images/pdf"),
        )
        docs = loader.load()
        for doc in docs:
            doc.page_content = normalize_pdf_text(doc.page_content)
        docs = chunk_documents(docs)

        # Fix metadata so Chroma doesn't crash
        for doc in docs:
            for k, v in doc.metadata.items():
                if isinstance(v, list):
                    # Convert list to comma-separated string
                    doc.metadata[k] = ", ".join(map(str, v))

        # Add to vectorstore and persist
        vectorstore = get_vectorstore()
        vectorstore.add_documents(docs)
        

    return {
        "status": "ok",
        "chunks_added": len(docs),
        "file": file.filename,
    }

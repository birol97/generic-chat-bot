from pathlib import Path
from dotenv import load_dotenv
from pdf_loader import PDFDocumentLoader
from document_loader import MarkdownDocumentLoader
from markdown_splitter import split_by_headers
from chunker import chunk_documents
from embedder import get_embedding_model
from vector_store import build_faiss_index


def run_ingestion():
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    # 1. Load
    loader = MarkdownDocumentLoader(base_dir / "docs" / "cv")
    pdf_loader =   PDFDocumentLoader(base_dir / "docs" / "contracts")
    docs = loader.load()
    pdf_docs = pdf_loader.load()

    # 2. Split
    header_docs = split_by_headers(docs)
    combined_docs =  header_docs + pdf_docs
    # 3. Chunk
    chunked_docs = chunk_documents(combined_docs)
    
    # 4. Embed + Store
    embedding_model = get_embedding_model()
    vectorstore = build_faiss_index(chunked_docs, embedding_model)

    print(f"Documents: {len(docs)}")
    print(f"Chunks: {len(chunked_docs)}")
    print(f"PDF docs: {len(pdf_docs)}")
    print("FAISS index built successfully ✅")

    return vectorstore


if __name__ == "__main__":
    load_dotenv()

    run_ingestion()

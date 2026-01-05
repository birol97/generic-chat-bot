from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional, List

from rag.retrieval.rag_chain import ask_me

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="RAG Document Chat")

app.mount(
    "/images",
    StaticFiles(directory=BASE_DIR / "docs" / "images"),
    name="images",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

class Evidence(BaseModel):
    file: str = "unknown"
    header_path: Optional[str] = None
    content: str
    images: List[str] = Field(default_factory=list)

class ChatResponse(BaseModel):
    answer: str
    evidence: List[Evidence]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ask_me(req.question)

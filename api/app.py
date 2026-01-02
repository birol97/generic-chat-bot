from fastapi import FastAPI
from pydantic import BaseModel
from rag.retrieval.rag_chain import ask_me
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
app = FastAPI(title="CV RAG Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    question: str
class Evidence(BaseModel):
    file: str
    header_path: Optional[str]
    content: str
class ChatResponse(BaseModel):
    answer: str
    evidence: list[Evidence]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = ask_me(req.question)
    return result

from typing import Dict, List
import json
import rag.config
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


PERSIST_DIR = "chroma_db"


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )

def build_rag_chain(vectorstore: Chroma):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an assistant answering questions based ONLY on the provided context.

Context:
{context}

Question:
{question}

Rules:
- Use only the context
- If the answer is not in the context, say "I don't know"
- Be concise and factual
"""
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever

def build_evidence(docs, max_chars=300):
    evidence = []

    for doc in docs:
        images = doc.metadata.get("images", [])

        if not isinstance(images, list):
            images = []

        evidence.append({
            "file": doc.metadata.get("file_name", "unknown"),
            "header_path": doc.metadata.get("header_path"),
            "content": doc.page_content[:max_chars],
            "images": images,
        })

    return evidence



    
from typing import List
from langchain_core.documents import Document
def dedupe_docs(docs: List[Document]) -> List[Document]:
    seen = set()
    unique_docs = []

    for doc in docs:
        key = (
            doc.metadata.get("file_name"),
            doc.metadata.get("header_path"),
            doc.page_content.strip(),
        )
        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    return unique_docs

def extract_images(docs: List[Document]) -> List[str]:
    images = set()

    for doc in docs:
        imgs = doc.metadata.get("images", [])
        for img in imgs:
            images.add(img)

    return list(images)

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
# 🔑 THIS IS THE CLEAN PUBLIC API
def ask_me(question: str) -> Dict:
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model,
    )

    chain, retriever = build_rag_chain(vectorstore)

    docs = retriever.invoke(question)
    
    docs = normalize_images(docs) 
    for d in docs:
        if d.metadata.get("file_type") == "pdf":
            print("RETRIEVED PDF IMAGES:", d.metadata.get("images"))

    answer = chain.invoke(question)
    
    evidence = build_evidence(docs)
    print(answer)
    print(evidence)
    return {
        "answer": answer,
        "evidence": evidence,
    }
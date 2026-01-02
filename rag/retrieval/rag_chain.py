from typing import Dict, List

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
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

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

def build_evidence(docs: List[Document], max_chars: int = 300):
    evidence = []

    for doc in docs:
        evidence.append({
            "file": doc.metadata.get("file_name"),
            "header_path": doc.metadata.get("header_path"),
            "content": doc.page_content[:max_chars].strip()
        })

    return evidence

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

    # Retrieve docs explicitly (for sources)
    docs = retriever.invoke(question)

    answer = chain.invoke(question)

    sources = list(
        {
            doc.metadata.get("file_name")
            for doc in docs
            if "file_name" in doc.metadata
        }
    )
    evidence = build_evidence(docs)  

    return {
        "answer": answer,
        "evidence": evidence,
    }

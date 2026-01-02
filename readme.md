# CV RAG Chatbot 🤖📄

An **enterprise-style Retrieval-Augmented Generation (RAG) chatbot** that answers questions about a CV, contracts, and documents using **FastAPI + LangChain + FAISS**, with **evidence grounding** and **optional image support** (e.g. diploma scans).

This project is designed as a **clean, extensible reference implementation** for document-based AI assistants.

---

## ✨ Features

* 🔍 **Semantic Search (RAG)** using FAISS
* 🧠 **LLM-grounded answers** (answers only from provided context)
* 📄 **Markdown ingestion** (CV, experience, education)
* 📑 **PDF ingestion** (contracts, long documents)
* 🧩 **Header-aware chunking** (section → subsection → subsubsection)
* 🖼 **Image evidence support** (e.g. diplomas shown with answers)
* 🌐 **FastAPI backend**
* 💬 **Simple web chatbot UI**
* 🧾 **Evidence returned per answer** (file + header path)

---

## 🏗 Architecture Overview

```
User Question
     │
     ▼
Retriever (FAISS Vector DB)
     │
     ▼
Relevant Chunks (Text + Image metadata)
     │
     ├─► LLM (text only)
     │        │
     │        ▼
     │    Final Answer
     │
     └─► UI renders related images (proof)
```

> ⚠️ The LLM **never reasons over images**. Images are attached as evidence only.

---

## 📂 Project Structure

```
doc-chatbot/
├── api/
│   └── app.py                 # FastAPI app
├── rag/
│   ├── Ingestion/
│   │   ├── document_loader.py # Markdown loader
│   │   ├── pdf_loader.py      # PDF loader
│   │   ├── image_loader.py    # Image metadata loader
│   │   ├── markdown_splitter.py
│   │   ├── chunker.py
│   │   └── run_ingestion.py
│   ├── embedder.py
│   ├── vector_store.py
│   └── rag_chain.py
├── docs/
│   ├── cv/                    # Markdown CV files
│   ├── contracts/             # PDF documents
│   └── images/                # Evidence images (e.g. diplomas)
├── ui/
│   └── index.html              # Web chatbot UI
├── .env
├── requirements.txt
└── README.md
```

---

## 📄 Supported Document Formats

### Markdown (Structured)

Best for:

* CVs
* Profiles
* Technical documentation

**Recommended format:**

```md
# Education
## University Education
### General Summary
- ...
```

### PDF (Unstructured)

Best for:

* Contracts
* Long agreements
* Legal documents

PDFs are split by **page → chunked → embedded**.

### Images (Evidence)

Best for:

* Diplomas
* Certificates
* Signed pages

Images are indexed with **semantic descriptions** and returned when relevant.

---

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/doc-chatbot.git
cd doc-chatbot
```

### 2️⃣ Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Environment Variables

Create `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 🧠 Ingest Documents

```bash
python rag/Ingestion/run_ingestion.py
```

Output:

```
Documents: X
Chunks: Y
FAISS index built successfully ✅
```

---

## 🌐 Run API Server

```bash
uvicorn api.app:app --reload
```

API runs at:

```
http://127.0.0.1:8000
```

---

## 💬 Run Web UI

Open in browser:

```
ui/index.html
```

Ask questions like:

* "What is my education background?"
* "Do I have a master degree?"
* "Which technologies have I worked with?"

---

## 📤 API Example

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Do I have a master degree?"}'
```

Response:

```json
{
  "answer": "Yes, Birol holds an MSc in Computing from Dublin City University.",
  "evidence": [
    {
      "file": "education.md",
      "header_path": "Education > Master Education",
      "content": "..."
    }
  ],
  "images": [
    {
      "src": "/static/education/msc_diploma.png",
      "alt": "MSc Diploma"
    }
  ]
}
```

---

## 🛡 Design Principles

* ❌ No hallucinations
* 🔒 Answers only from context
* 📎 Evidence-first design
* 🧱 Modular loaders per document type
* 📈 Easily extensible

---

## 🧪 Recommended Improvements

* Confidence scoring
* Document versioning
* Role-based access (HR / Legal)
* OCR for scanned PDFs
* UI filters per document type

---

## 📜 License

MIT License

---

## 👤 Author

**Birol Kılıç**
Computer Engineer · RAG Systems · Backend & AI

---

If you find this useful ⭐ the repo and feel free to extend it.

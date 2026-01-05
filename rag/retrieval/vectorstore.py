import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# --- Safe persistent directory in home folder ---
PERSIST_DIR = "./chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)  # create folder if missing
load_dotenv()

# --- Embeddings setup ---
embeddings = OpenAIEmbeddings()  # or your preferred embedding function

# --- Vectorstore getter ---
def get_vectorstore():
    """
    Returns a Chroma vectorstore instance, creating the persistent directory if needed.
    """
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )

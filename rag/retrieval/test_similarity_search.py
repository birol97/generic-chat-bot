from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def main():
    # 1. Load embedding model (MUST be same as ingestion)
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # 2. Load existing Chroma index
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model,
    )

    # 3. Test query
    query = "Where did I do my Master Education?"

    results = vectorstore.similarity_search(
        query=query,
        k=3
    )

    print(f"\nQuery: {query}\n")
    for i, doc in enumerate(results):
        print(f"Result {i+1}")
        print("-" * 40)
        print(doc.page_content)
        print("Metadata:", doc.metadata)
        print()


if __name__ == "__main__":
    main()

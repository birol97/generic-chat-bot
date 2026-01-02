from rag.retrieval.rag_chain import ask_me

if __name__ == "__main__":
    result = ask_me("Tell me about my projects")

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for s in result["sources"]:
        print("-", s)


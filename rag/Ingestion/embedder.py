from langchain_openai import OpenAIEmbeddings


def get_embedding_model():
    """
    Returns OpenAI embedding model
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

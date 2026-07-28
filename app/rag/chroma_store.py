import chromadb
from chromadb.utils import embedding_functions
from app.config import settings


def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


class PolicyVectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.embedding_fn = get_embedding_function()
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, docs: list, ids: list, metadatas: list = None):
        """
        docs: list[str] raw text chunks
        ids: list[str] unique chunk ids
        metadatas: list[dict] optional per-chunk metadata (e.g. {"source": "visiting_hours.txt"})
        """
        self.collection.add(documents=docs, ids=ids, metadatas=metadatas or [{} for _ in docs])

    def query(self, query_text: str, top_k: int = 3) -> dict:
        results = self.collection.query(query_texts=[query_text], n_results=top_k)
        return {
            "documents": results.get("documents", [[]])[0],
            "metadatas": results.get("metadatas", [[]])[0],
            "distances": results.get("distances", [[]])[0],
        }

    def count(self) -> int:
        return self.collection.count()


policy_store = PolicyVectorStore()

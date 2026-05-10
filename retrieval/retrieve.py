import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="shl_assessments"
)


def keyword_score(query, item):

    query_words = query.lower().split()

    text = (
        item["name"] + " " +
        item["description"] + " " +
        item["test_type"]
    ).lower()

    score = 0

    for word in query_words:

        if word in text:
            score += 1

    return score


def search_assessments(query, top_k=10):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20
    )

    candidates = results["metadatas"][0]

    # Hybrid reranking
    reranked = sorted(
        candidates,
        key=lambda x: keyword_score(query, x),
        reverse=True
    )

    return reranked[:top_k]
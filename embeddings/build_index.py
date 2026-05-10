import json
import chromadb

from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="shl_assessments"
)

# Load SHL catalog
with open("catalog/shl_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Insert assessments into ChromaDB
for idx, item in enumerate(data):

    text = item["name"] + " " + item["description"]

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(idx)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[item]
    )

print("ChromaDB index created successfully")
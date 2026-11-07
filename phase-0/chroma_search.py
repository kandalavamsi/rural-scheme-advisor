import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("BAAI/bge-m3")

# Connect to existing database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Access existing collection
collection = client.get_collection(
    name="government_schemes"
)

# Accept user query
query = input("Enter your question: ")

# Generate query embedding
query_embedding = model.encode(query).tolist()

# Search ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# Display results
print("\nSearch Results:\n")

for i in range(len(results["ids"][0])):

    print("Document ID:", results["ids"][0][i])

    print("Document:", results["documents"][0][i])

    print("Metadata:", results["metadatas"][0][i])

    print("Distance:", results["distances"][0][i])

    print("-" * 60)
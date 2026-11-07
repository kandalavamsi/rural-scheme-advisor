
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="government_schemes_cosine")

query = input("Enter your question: ")
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=4
)

MAX_DISTANCE = 0.40

print("\nRelevant Search Results:\n")

found_relevant = False

for i in range(len(results["ids"][0])):

    distance = results["distances"][0][i]

    if distance <= MAX_DISTANCE:
        found_relevant = True

        print("Document ID:", results["ids"][0][i])
        print("Document:", results["documents"][0][i])
        print("Distance:", round(distance, 4))
        print("-" * 60)

if not found_relevant:
    print("No sufficiently relevant documents found.")
    print("Please try a different question.")

import chromadb 
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("BAAI/bge-m3")

#Connect to database
client=chromadb.PersistentClient(path='./chroma_db')

collection=client.get_collection(name="government_schemes_cosine")

query=input("Enter your question: ")

query_embedding=model.encode(query).tolist()

#search with metadata filtering
results=collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    where={"topic":"Verification"}
)


# Display results
print("\nFiltered Search Results:\n")

for i in range(len(results["ids"][0])):

    print("Document ID:", results["ids"][0][i])
    print("Document:", results["documents"][0][i])
    print("Metadata:", results["metadatas"][0][i])
    print("Distance:", results["distances"][0][i])
    print("-" * 60)
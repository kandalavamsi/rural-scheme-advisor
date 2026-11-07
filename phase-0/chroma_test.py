import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model=SentenceTransformer("BAAI/bge-m3")

# Initialize ChromaDB
client=chromadb.PersistentClient(path='./chroma_db')



# Create a new collection with cosine distance
collection = client.get_or_create_collection(
    name="government_schemes_cosine",
    metadata={"hnsw:space": "cosine"}
)


# Sample documents
documents = [
    "PM-KISAN provides financial assistance to eligible farmer families.",
    "Farmers can register for PM-KISAN through the official portal.",
    "Aadhaar details are required for PM-KISAN beneficiary verification.",
    "Farmers can check their PM-KISAN payment status online."
]

#generate embeddings
embeddings=model.encode(documents).tolist()

# Insert records
collection.add(
    ids=["doc1", "doc2", "doc3", "doc4"],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"scheme": "PM-KISAN", "topic": "Financial Assistance"},
        {"scheme": "PM-KISAN", "topic": "Registration"},
        {"scheme": "PM-KISAN", "topic": "Verification"},
        {"scheme": "PM-KISAN", "topic": "Payment Status"}
    ]
)

print("Documents inserted successfully!")
print("Total records:", collection.count())

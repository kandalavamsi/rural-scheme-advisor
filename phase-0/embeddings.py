from sentence_transformers import SentenceTransformer
import numpy as np 
 
#Load the embedding model
model=SentenceTransformer('BAAI/bge-m3')

sentences=[
    "Farmers can apply for PM-KISAN.",
    "PM-KISAN provides financial assistance to eligible farmers.",
    "Students can apply for scholarships.",
    "The government provides housing assistance to rural families.",
    "Farmers need land ownership records for scheme registration."
]

# Generate embeddings
embeddings=model.encode(sentences)

print("Number of sentences", len(sentences))
print("Embedding shape", embeddings.shape)

print("\n First sentence:")
print(sentences[0])

print("\n Its embedding:")
print(embeddings[0])

print("\n Embedding dimensions:", len(embeddings[0]))


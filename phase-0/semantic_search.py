from sentence_transformers import SentenceTransformer
import numpy as np 

# Load embedding model
model=SentenceTransformer('BAAI/bge-m3')

documents=[ 
    "Farmers can register for PM-KISAN through the official portal.",
    "PM-KISAN provides financial assistance to eligible farmer families.",
    "Farmers need land ownership records for PM-KISAN registration.",
    "The government provides housing assistance to rural families.",
    "Students can apply for government scholarships.",
    "Eligible farmers receive financial support under PM-KISAN.",
    "Farmers can check their PM-KISAN beneficiary status online.",
    "Aadhaar details are required for PM-KISAN beneficiary verification.",
    "Rural households can apply for housing assistance under PMAY-G.",
    "The government provides employment opportunities under MGNREGA.",
    "Farmers can obtain information about crop insurance schemes.",
    "PM Fasal Bima Yojana provides crop insurance coverage to farmers."

]

#convert documents into embeddings

document_embeddings=model.encode(documents)

query=input("\nEnter your question: ")

#convert query into embedding

query_embedding=model.encode([query])[0]

#calculate cosine similarity
similarities=np.dot(document_embeddings,query_embedding)/(np.linalg.norm(document_embeddings,axis=1)* np.linalg.norm(query_embedding))

#rank documents by similarity
ranked_indices=np.argsort(similarities)[::-1]

print("\nTop 3 relevant documents:\n")

for index in ranked_indices[:3]:
    print("Document:", documents[index])
    print("Similarity:", round(float(similarities[index]), 4))
    print("-" * 60)

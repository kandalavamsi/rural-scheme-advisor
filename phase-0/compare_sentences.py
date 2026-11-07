from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("BAAI/bge-m3")

sentences = [
    "Farmers can apply for PM-KISAN.",
    "Eligible farmers receive financial assistance under PM-KISAN.",
    "Students can apply for government scholarships."
]

embeddings = model.encode(sentences)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity = np.dot(embeddings[i], embeddings[j]) / (
            np.linalg.norm(embeddings[i]) *
            np.linalg.norm(embeddings[j])
        )

        print(f"\nSentence {i + 1}: {sentences[i]}")
        print(f"Sentence {j + 1}: {sentences[j]}")
        print("Cosine similarity:", round(float(similarity), 4))
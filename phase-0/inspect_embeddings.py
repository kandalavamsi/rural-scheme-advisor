from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

sentence = "Farmers can apply for PM-KISAN."

# Tokenize the sentence
tokens = model.tokenizer(
    sentence,
    return_tensors="pt"
)

token_ids = tokens["input_ids"][0]

print("Token IDs:")
print(token_ids.tolist())

print("\nTokens:")
print(model.tokenizer.convert_ids_to_tokens(token_ids))

# Generate sentence embedding
embedding = model.encode(sentence)

print("\nSentence embedding:")
print(embedding)

print("\nEmbedding shape:")
print(embedding.shape)

print("\nFirst 10 dimensions:")
print(embedding[:10])
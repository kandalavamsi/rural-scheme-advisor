
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).resolve().parents[1]

CHROMA_DIR = ROOT_DIR / "chroma_db"

MODEL_NAME = "BAAI/bge-m3"
COLLECTION_NAME = "pm_kisan_mvp"

TOP_K = 5

TEST_QUESTIONS = [
    "What are the eligibility exclusions under PM-KISAN?",
    "How is the benefit handled when agricultural land is jointly held?",
    "What special land ownership certificate is required for tribal families in Manipur?"
]


def main():
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    print("Collection records:", collection.count())

    for question in TEST_QUESTIONS:
        query_embedding = model.encode(
            question,
            normalize_embeddings=True
        )

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        print("\n" + "=" * 80)
        print("QUESTION:", question)
        print("=" * 80)

        for rank, (chunk_id, document, metadata, distance) in enumerate(
            zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ),
            start=1
        ):
            similarity = 1 - distance

            print(f"\nResult {rank}")
            print("Chunk ID:", chunk_id)
            print("Similarity:", round(similarity, 4))
            print("Source:", metadata["source_title"])
            print("Source ID:", metadata["source_id"])
            print("Scope:", metadata["document_scope"])
            print("Jurisdiction:", metadata["jurisdiction"])
            print("Page:", metadata["page_start"])
            print("Text:", document[:500].replace("\n", " "))


if __name__ == "__main__":
    main()

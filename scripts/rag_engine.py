
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

CHROMA_DIR = ROOT_DIR / "chroma_db"
COLLECTION_NAME = "pm_kisan_mvp"

EMBEDDING_MODEL = "BAAI/bge-m3"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

TOP_K = 5


class RAGEngine:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        print("Connecting to ChromaDB...")
        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.chroma_client.get_collection(
            name=COLLECTION_NAME
        )

        self.groq_client = Groq(api_key=api_key)

        print("RAG engine initialized.")

    def retrieve(self, question):
        query_embedding = self.embedding_model.encode(
            question,
            normalize_embeddings=True
        )

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_chunks.append({
                "text": document,
                "metadata": metadata,
                "similarity": round(1 - distance, 4)
            })

        return retrieved_chunks

    def generate_answer(self, question, retrieved_chunks):
        if not retrieved_chunks:
            return "I could not find relevant evidence in the available documents."

        context_parts = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk["metadata"]

            context_parts.append(
                f"""
[EVIDENCE {index}]
Source ID: {metadata["source_id"]}
Document: {metadata["source_title"]}
Document date: {metadata["document_date"] or "Not specified"}
Scope: {metadata["document_scope"]}
Jurisdiction: {metadata["jurisdiction"]}
Page: {metadata["page_start"]}
Content status: {metadata["content_status"]}

Text:
{chunk["text"]}
"""
            )

        context = "\n".join(context_parts)

        system_prompt = """
You are Rural Scheme Advisor, an assistant that answers questions
about Indian government schemes using retrieved official documents.

Follow these rules strictly:

1. Answer only using the supplied evidence.
2. Do not invent eligibility rules, dates, amounts, or procedures.
3. Cite factual claims using this format:
   [Source ID, page number]
   Example: [Source 9, p. 1]
4. Do not create citations for information absent from the evidence.
5. If evidence is insufficient, explicitly say so.
6. Clearly distinguish national provisions from state-specific provisions.
7. Never apply a state-specific provision to all of India.
8. Pay attention to document dates and content status.
9. Historical documents must not be presented as verified current rules.
10. If the evidence does not establish current applicability,
    explicitly state that current applicability needs verification.
11. If sources appear to differ, describe the difference and
    identify the documents rather than silently reconciling them.
12. Use clear, straightforward language.

Do not use outside knowledge to fill gaps.
"""

        response = self.groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{question}\n\n"
                        f"Retrieved evidence:\n{context}"
                    )
                }
            ],
            temperature=0.1,
            max_completion_tokens=1200
        )

        return response.choices[0].message.content

    def ask(self, question):
        retrieved_chunks = self.retrieve(question)

        answer = self.generate_answer(
            question,
            retrieved_chunks
        )

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "source_id": chunk["metadata"]["source_id"],
                    "title": chunk["metadata"]["source_title"],
                    "page": chunk["metadata"]["page_start"],
                    "scope": chunk["metadata"]["document_scope"],
                    "jurisdiction": chunk["metadata"]["jurisdiction"],
                    "similarity": chunk["similarity"]
                }
                for chunk in retrieved_chunks
            ]
        }


if __name__ == "__main__":
    engine = RAGEngine()

    while True:
        question = input("\nAsk a PM-KISAN question (or type 'exit'): ")

        if question.strip().lower() == "exit":
            break

        if not question.strip():
            continue

        result = engine.ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nRETRIEVED SOURCES:")

        for source in result["sources"]:
            print(
                f"Source {source['source_id']} | "
                f"{source['title']} | "
                f"Page {source['page']} | "
                f"{source['scope']} | "
                f"{source['jurisdiction']} | "
                f"Similarity: {source['similarity']}"
            )

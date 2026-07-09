import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path.home() / "ai-engineering-lab" / "01_llm_api_logger" / ".env")
client = OpenAI()


def embed(text):
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(resp.data[0].embedding)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# The "documents" — our little knowledge base
DOCUMENTS = [
    "The cheetah is the fastest land animal, reaching 70 mph.",
    "Affordable airfare can be found by booking flights months in advance.",
    "Photosynthesis lets plants convert sunlight into energy.",
    "The stock market fell sharply amid recession fears.",
    "Dogs are loyal companions and need daily exercise.",
    "Python is a popular programming language for data science.",
    "The Great Wall of China is over 13,000 miles long.",
    "Regular exercise improves cardiovascular health.",
    "Espresso is a concentrated form of coffee.",
    "Electric cars are becoming more common as battery costs fall.",
]

# ---- PHASE 1: INDEX (done once) ----
print("Indexing documents (embedding each one)...")
doc_vectors = [embed(doc) for doc in DOCUMENTS]
print(f"Indexed {len(DOCUMENTS)} documents.\n")


# ---- PHASE 2: SEARCH (per query) ----
def search(query, top_k=3):
    query_vec = embed(query)
    scored = []
    for doc, vec in zip(DOCUMENTS, doc_vectors):
        sim = cosine_similarity(query_vec, vec)
        scored.append((sim, doc))
    scored.sort(reverse=True)  # highest similarity first
    return scored[:top_k]


def main():
    while True:
        query = input("Search (or 'quit'): ").strip()
        if query.lower() in ("quit", "exit", ""):
            break
        results = search(query)
        print(f"\nTop matches for {query!r}:")
        for sim, doc in results:
            print(f"  [{sim:.3f}] {doc}")
        print()


if __name__ == "__main__":
    main()

from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("supply_chain_docs")


def search(query, k=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    print("\nQUERY:", query)
    print("=" * 70)

    for i in range(len(results["documents"][0])):
        print(f"\nResult {i + 1}")
        print("File:", results["metadatas"][0][i]["filename"])
        print("Page:", results["metadatas"][0][i]["page"])
        print("Distance:", results["distances"][0][i])
        print("Text:")
        print(results["documents"][0][i][:500])


if __name__ == "__main__":
    search("What is the defect penalty for Kaveri Metals?")
    search("Who approves a purchase order worth 1.4 crore?")
    search("Which supplier has the highest spend and what is their on-time delivery?")
from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

DATA_DIR = Path("data")
DB_DIR = "chroma_db"

# 1. Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

all_chunks = []

for pdf_path in DATA_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_path)

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks = splitter.split_text(text)

        for chunk_number, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "text": chunk,
                "filename": pdf_path.name,
                "page": page_number,
                "chunk_id": f"{pdf_path.stem}_p{page_number}_c{chunk_number}"
            })

print(f"Created {len(all_chunks)} chunks.")

# 2. Load free local embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. Create persistent ChromaDB
client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(
    name="supply_chain_docs"
)

# 4. Generate embeddings
texts = [item["text"] for item in all_chunks]

print("Creating embeddings...")
embeddings = model.encode(
    texts,
    show_progress_bar=True
).tolist()

# 5. Store everything in ONE collection
collection.add(
    ids=[item["chunk_id"] for item in all_chunks],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "filename": item["filename"],
            "page": item["page"]
        }
        for item in all_chunks
    ]
)

print("\nDatabase built successfully!")
print("Collection:", collection.name)
print("Documents stored:", collection.count())
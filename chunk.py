from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path("data")

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

print(f"Total chunks created: {len(all_chunks)}")

print("\n--- SAMPLE CHUNKS ---")

for chunk in all_chunks[:3]:
    print("\n" + "=" * 60)
    print("ID:", chunk["chunk_id"])
    print("File:", chunk["filename"])
    print("Page:", chunk["page"])
    print("Length:", len(chunk["text"]))
    print(chunk["text"][:500])

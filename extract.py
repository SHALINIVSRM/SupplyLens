from pathlib import Path
from pypdf import PdfReader


DATA_DIR = Path("data")


def extract_pdfs():
    documents = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the data folder.")
        return documents

    for pdf_path in pdf_files:
        reader = PdfReader(pdf_path)

        print("\n" + "=" * 60)
        print(f"File: {pdf_path.name}")
        print(f"Page count: {len(reader.pages)}")
        print("=" * 60)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            documents.append({
                "text": text,
                "filename": pdf_path.name,
                "page": page_number
            })

            if page_number == 1:
                print("\nFirst 300 characters:")
                print(text[:300])

    return documents


if __name__ == "__main__":
    documents = extract_pdfs()

    print("\n" + "=" * 60)
    print(f"Total pages extracted: {len(documents)}")
    print("=" * 60)
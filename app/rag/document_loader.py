import os
import sys
import hashlib

from app.rag.chroma_store import policy_store


def chunk_text(text: str, chunk_size: int = 100, overlap: int = 10) -> list:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks


def extract_pdf_text(filepath: str) -> str:
    """Extract text from a PDF using pypdf. Works for text-based PDFs
    (most hospital policy/brochure PDFs). Scanned/image-only PDFs will
    return little or no text -- run those through OCR first."""
    from pypdf import PdfReader

    reader = PdfReader(filepath)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)
    return "\n".join(text_parts)


def load_directory(directory: str):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        lower = filename.lower()

        if lower.endswith((".txt", ".md")):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif lower.endswith(".pdf"):
            text = extract_pdf_text(filepath)
            if not text.strip():
                print(f"WARNING: No extractable text in {filename} "
                      f"(likely a scanned/image PDF -- skipping). "
                      f"Run OCR first if you need this file indexed.")
                continue
        else:
            continue

        chunks = chunk_text(text)
        if not chunks:
            print(f"Skipping {filename}: no content after chunking")
            continue

        ids = [
            hashlib.md5(f"{filename}-{i}".encode()).hexdigest()
            for i in range(len(chunks))
        ]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
        policy_store.add_documents(docs=chunks, ids=ids, metadatas=metadatas)
        print(f"Loaded {len(chunks)} chunks from {filename}")

    print(f"Total documents in collection: {policy_store.count()}")


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "./policy_docs"
    load_directory(target_dir)

from docx import Document
from textwrap import wrap
import os

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return full_text

def save_chunks_to_file(text, file_handle, chunk_size=1000):
    chunks = wrap(text, width=chunk_size)
    for chunk in chunks:
        file_handle.write(chunk.replace("\n", " ").strip() + "\n")

output_path = "data/docs.txt"
os.makedirs("data", exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    for doc_path in [
        "source_documents/doc1.docx",
        "source_documents/doc2.docx",
        "source_documents/doc3.docx"
    ]:
        print(f"Processing {doc_path}...")
        full_text = extract_text_from_docx(doc_path)
        save_chunks_to_file(full_text, f)
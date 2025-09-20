# scripts/ingest.py
import os
import sqlite3
from pypdf import PdfReader

PDF_DIR = "data/pdfs"
DB_PATH = "data/safety.db"
CHUNK_WORDS = 200

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        chunk TEXT
    )
    """)
    conn.commit()
    conn.close()

def chunk_text(text, max_words=CHUNK_WORDS):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words]).strip()

def ingest_pdfs(pdf_dir=PDF_DIR):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    files = sorted([f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")])
    if not files:
        print("No PDFs found in", pdf_dir)
        return
    for filename in files:
        path = os.path.join(pdf_dir, filename)
        print("Processing:", filename)
        try:
            reader = PdfReader(path)
        except Exception as e:
            print("  Failed to open", filename, e)
            continue
        full_text = []
        for page in reader.pages:
            try:
                txt = page.extract_text()
                if txt:
                    full_text.append(txt)
            except Exception:
                continue
        text = "\n".join(full_text)
        if not text.strip():
            print("  No text extracted for", filename)
            continue
        for chunk in chunk_text(text):
            cur.execute("INSERT INTO chunks (source, chunk) VALUES (?, ?)", (filename, chunk))
        conn.commit()
    conn.close()
    print("Ingest complete. DB:", DB_PATH)

if __name__ == "__main__":
    create_db()
    ingest_pdfs()

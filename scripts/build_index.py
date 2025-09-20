# scripts/build_index.py
import sqlite3, numpy as np, os, random
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm

DB_PATH = "data/safety.db"
FAISS_OUT = "data/safety.index"
IDS_OUT = "data/safety.index.ids.npy"
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH = 64
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

def load_chunks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, chunk FROM chunks ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    ids = [r[0] for r in rows]
    texts = [r[1] for r in rows]
    return ids, texts

def build_index():
    ids, texts = load_chunks()
    if not texts:
        print("No chunks found in DB. Run ingest first.")
        return
    model = SentenceTransformer(MODEL_NAME)
    all_emb = []
    for i in tqdm(range(0, len(texts), BATCH), desc="Embedding"):
        batch = texts[i:i+BATCH]
        emb = model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        all_emb.append(emb.astype('float32'))
    embeddings = np.vstack(all_emb)
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    os.makedirs(os.path.dirname(FAISS_OUT), exist_ok=True)
    faiss.write_index(index, FAISS_OUT)
    np.save(IDS_OUT, np.array(ids))
    print("Saved FAISS index ->", FAISS_OUT)
    print("Saved ID mapping ->", IDS_OUT)

if __name__ == "__main__":
    build_index()

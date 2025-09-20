# scripts/search_baseline.py
import sqlite3, numpy as np, faiss, argparse, json
from sentence_transformers import SentenceTransformer

DB_PATH = "data/safety.db"
FAISS_OUT = "data/safety.index"
IDS_OUT = "data/safety.index.ids.npy"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(FAISS_OUT)
ids = np.load(IDS_OUT, allow_pickle=True)

def fetch_metadata(chunk_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, source, chunk FROM chunks WHERE id=?", (chunk_id,))
    r = cur.fetchone()
    conn.close()
    if r:
        return {"id": r[0], "source": r[1], "text": r[2]}
    return None

def baseline_search(query, k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        chunk_id = int(ids[idx])
        meta = fetch_metadata(chunk_id)
        meta["score"] = float(score)
        results.append(meta)
    return results

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--q", required=True)
    p.add_argument("--k", type=int, default=5)
    args=p.parse_args()
    out = baseline_search(args.q, k=args.k)
    print(json.dumps(out, indent=2))

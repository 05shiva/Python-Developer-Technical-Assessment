# scripts/search_rerank.py
import sqlite3, numpy as np, faiss, argparse, json
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

DB_PATH = "data/safety.db"
FAISS_OUT = "data/safety.index"
IDS_OUT = "data/safety.index.ids.npy"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(FAISS_OUT)
ids = np.load(IDS_OUT, allow_pickle=True)

def build_bm25():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, chunk FROM chunks ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    id_list = [r[0] for r in rows]
    tokenized = [ [t.lower() for t in word_tokenize(r[1])] for r in rows ]
    bm25 = BM25Okapi(tokenized)
    id_to_pos = {cid:pos for pos,cid in enumerate(id_list)}
    return bm25, id_to_pos

bm25, id_to_pos = build_bm25()

def fetch_metadata(chunk_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, source, chunk FROM chunks WHERE id=?", (chunk_id,))
    r = cur.fetchone()
    conn.close()
    if r:
        return {"id": r[0], "source": r[1], "text": r[2]}
    return None

def hybrid_rerank(query, faiss_top_n=100, k=5, alpha=0.6):
    q_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, faiss_top_n)
    vec_scores = D[0]
    idxs = I[0]
    query_tokens = [t.lower() for t in word_tokenize(query)]
    bm25_scores_all = bm25.get_scores(query_tokens)
    candidates = []
    for vec_score, idx in zip(vec_scores, idxs):
        if idx < 0:
            continue
        cid = int(ids[idx])
        pos = id_to_pos[cid]
        bscore = float(bm25_scores_all[pos])
        meta = fetch_metadata(cid)
        meta["vec_score"] = float(vec_score)
        meta["bm25"] = bscore
        candidates.append(meta)
    if not candidates:
        return []
    vs = np.array([c["vec_score"] for c in candidates])
    bs = np.array([c["bm25"] for c in candidates])
    vsn = (vs - vs.min()) / (vs.max() - vs.min() + 1e-9)
    bsn = (bs - bs.min()) / (bs.max() - bs.min() + 1e-9)
    final = alpha*vsn + (1-alpha)*bsn
    for i,c in enumerate(candidates):
        c["final_score"] = float(final[i])
    candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return candidates[:k]

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--q", required=True)
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--alpha", type=float, default=0.6)
    args=p.parse_args()
    out = hybrid_rerank(args.q, faiss_top_n=100, k=args.k, alpha=args.alpha)
    print(json.dumps(out, indent=2))

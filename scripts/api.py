# scripts/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from scripts.search_baseline import baseline_search
from scripts.search_rerank import hybrid_rerank
from scripts.answer_util import extractive_answer

app = FastAPI(title="Mini RAG + Reranker")

ABSTAIN_HYBRID = 0.12
ABSTAIN_BASELINE = 0.20

class AskReq(BaseModel):
    q: str
    k: int = 3
    mode: str = "hybrid"

@app.post("/ask")
def ask(req: AskReq):
    q = req.q
    k = req.k
    mode = req.mode.lower()
    if mode == "baseline":
        contexts = baseline_search(q, k=k)
        top_score = contexts[0]["score"] if contexts else 0.0
        if top_score < ABSTAIN_BASELINE:
            return {"answer": None, "contexts": contexts, "reranker_used": "baseline", "reason": "low_confidence", "top_score": float(top_score)}
        top = contexts[0]
        answer = extractive_answer(q, top["text"])
        citation = {"id": top["id"], "source": top["source"]}
        return {"answer": answer, "contexts": contexts, "reranker_used": "baseline", "citation": citation}
    else:
        contexts = hybrid_rerank(q, faiss_top_n=100, k=k, alpha=0.6)
        top_score = contexts[0]["final_score"] if contexts else 0.0
        if top_score < ABSTAIN_HYBRID:
            return {"answer": None, "contexts": contexts, "reranker_used": "hybrid", "reason": "low_confidence", "top_score": float(top_score)}
        top = contexts[0]
        answer = extractive_answer(q, top["text"])
        citation = {"id": top["id"], "source": top["source"]}
        return {"answer": answer, "contexts": contexts, "reranker_used": "hybrid", "citation": citation}

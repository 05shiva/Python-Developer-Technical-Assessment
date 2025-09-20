# scripts/answer_util.py
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')

def extractive_answer(query, chunk_text, max_sentences=2):
    sents = sent_tokenize(chunk_text)
    if not sents:
        return ""
    q_tokens = set([t.lower() for t in word_tokenize(query)])
    scored = []
    for s in sents:
        stoks = set([t.lower() for t in word_tokenize(s)])
        overlap = len(q_tokens & stoks)
        scored.append((overlap, s))
    scored.sort(reverse=True)
    selected = [s for sc,s in scored[:max_sentences] if sc>0]
    if selected:
        return " ".join(selected)
    return sents[0] if sents else (chunk_text[:200] + "...")

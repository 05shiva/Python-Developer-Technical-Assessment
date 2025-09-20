# eval/run_eval.py
import json, requests, pandas as pd
Q=json.load(open("eval/questions.json"))
rows=[]
url="http://127.0.0.1:8000/ask"
for q in Q:
    for mode in ("baseline","hybrid"):
        r = requests.post(url, json={"q":q,"k":1,"mode":mode}).json()
        rows.append({
            "question": q,
            "mode": mode,
            "answer": r.get("answer"),
            "abstain": r.get("answer") is None,
            "top_source": (r.get("citation") or {}).get("source"),
            "top_score": r.get("top_score")
        })
df = pd.DataFrame(rows)
df.to_csv("eval/results.csv", index=False)
print(df)
print("Saved eval/results.csv")

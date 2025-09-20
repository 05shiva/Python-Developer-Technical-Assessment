import json
import csv

# Load JSON
with open("assessment_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Open CSV file to write
with open("results_table.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Question", "Answer", "Citation", "Reranker Used", "Score"])

    for item in data:
        question = item.get("question", "")
        
        # Choose 'hybrid' answer if available, else fallback to 'baseline'
        answer_info = item.get("hybrid") or item.get("baseline")
        if not answer_info:
            continue

        answer_text = answer_info.get("answer", "")
        citation = answer_info.get("citation", {}).get("source", "")
        reranker = answer_info.get("reranker_used", "")
        
        # Try to get final_score from the first context (or leave empty)
        contexts = answer_info.get("contexts", [])
        score = contexts[0].get("final_score") if contexts else ""
        
        writer.writerow([question, answer_text, citation, reranker, score])

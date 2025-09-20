# save as scripts/run_assessment.py
import requests
import json

# Replace with your 8 assessment questions
questions = [
    "What is lockout-tagout?",
    "What are the safety requirements for milling machines?",
    "What are the main hazards of grinding machines?",
    "Describe the safety procedures for conveyor systems.",
    "Explain the safety requirements for power press brakes.",
    "What are the OSHA guidelines for drill presses?",
    "Describe the guarding methods for food slicers.",
    "Explain energy isolating devices in machinery."
]

api_url = "http://127.0.0.1:8000/ask"
output_file = "assessment_results.json"

results = []

for q in questions:
    question_result = {"question": q, "baseline": {}, "hybrid": {}}
    for mode in ["baseline", "hybrid"]:
        payload = {"q": q, "k": 3, "mode": mode}
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            question_result[mode] = {
                "answer": data.get("answer"),
                "contexts": data.get("contexts"),
                "reranker_used": data.get("reranker_used"),
                "citation": data.get("citation")
            }
        else:
            question_result[mode] = {"error": f"HTTP {response.status_code}"}
    results.append(question_result)

# Save to JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Assessment results saved to {output_file}")

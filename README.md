# Python-Developer-Technical-Assessment
Overview

This repository contains my solution for the Python Developer Technical Assessment. It demonstrates skills in:

Data ingestion and chunking

Generating embeddings and building a vector index

Baseline search and hybrid reranking

RESTful API development

The system answers 8 safety-related questions by retrieving relevant information from provided sources.assement/
├── scripts/
│ ├── api.py
│ ├── run_assessment.py
│ └── table.py
├── data/
│ ├── assessment_results.json
│ └── sources.json
├── results_table.csv
└── README.md

- `scripts/`: Contains Python scripts for running the assessment.
  - `run_assessment.py`: Executes all assessment queries and saves results in JSON.
  - `table.py`: Converts JSON results into a CSV table (`results_table.csv`).
  - `api.py`: FastAPI backend to query assessment questions.
- `data/`: Contains raw assessment results (`assessment_results.json`) and source documents (`sources.json`).
- `results_table.csv`: CSV table containing all questions, answers, citations, reranker used, and scores.
- `README.md`: This file.

## Setup Instructions 
```bash
1. **Clone the repository**  

git clone https://github.com/05shiva/Python-Developer-Technical-Assessment.git
cd assement
2. pip install -r requirements.txt
3. python -m uvicorn scripts.api:app --reload --port 8000
4.python scripts/run_assessment.py
5.python scripts/table.py
```
## Learning 


Through this assessment, I improved my understanding of:

- **Data Pipelines**: Efficiently chunking and embedding source documents.
- **Search & Reranking**: Combining vector similarity with BM25 scoring for hybrid retrieval.
- **API Development**: Building a working RESTful API to serve ML-powered answers.

This project helped me gain experience integrating multiple components into a coherent system and handling real-world text data.
## Two Example curl Requests
### Easy:
curl -X POST "http://127.0.0.1:8000/ask" \
-H "Content-Type: application/json" \
-d '{"q":"What is lockout-tagout?","k":3,"mode":"hybrid"}'
### Tricky:
curl -X POST "http://127.0.0.1:8000/ask" \
-H "Content-Type: application/json" \
-d '{"q":"Explain energy isolating devices in machinery.","k":5,"mode":"hybrid"}'

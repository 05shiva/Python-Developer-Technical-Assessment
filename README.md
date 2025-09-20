# Python-Developer-Technical-Assessment
This repository contains the code, data, and results for the Python Developer Technical Assessment.
assement/
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

1. **Clone the repository**  
```bash
git clone https://github.com/05shiva/Python-Developer-Technical-Assessment.git
cd assement
2. pip install -r requirements.txt
3. python -m uvicorn scripts.api:app --reload --port 8000
4.python scripts/run_assessment.py
5.python scripts/table.py



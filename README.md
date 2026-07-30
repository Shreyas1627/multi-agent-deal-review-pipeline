# 📑 Multi-Agent Deal Review Pipeline

> An enterprise-grade, deterministic multi-agent workflow for reviewing financial deal documents, validating compliance against explicit policy rules, and generating evidence-backed executive reports with prioritized risk analysis.

Built using **LangGraph**, **LangChain**, **OpenAI**, and **Pydantic Structured Outputs**.

---

## ✨ Features

- 🤖 Multi-agent architecture with specialized responsibilities
- 📄 Automated financial term extraction
- ✅ Rule-based compliance validation
- ⚠️ Prioritized risk assessment
- 📊 Executive summary generation
- 📌 Clause/page-level evidence traceability
- 🛡️ Deterministic workflow using LangGraph state management
- 📦 Structured JSON outputs with Pydantic

---

# 🏗️ Architecture

The workflow decomposes document review into specialized agents operating over a shared state.

```text
               Deal Document
                      +
              Policy Rules (JSON)
                      │
                      ▼
        ┌────────────────────────┐
        │     Orchestrator       │
        │ (Shared State Manager) │
        └──────────┬─────────────┘
                   │
                   ▼
      ┌──────────────────────────┐
      │ 1. Term Extraction Agent │
      │ Extract key deal terms   │
      │ + clause/page citations  │
      └──────────┬───────────────┘
                 │
                 ▼
     ┌───────────────────────────┐
     │2. Compliance Review Agent │
     │ Compare against policy    │
     │ PASS / FAIL /             │
     │ NEEDS_HUMAN_REVIEW        │
     └──────────┬────────────────┘
                │
                ▼
      ┌──────────────────────────┐
      │3. Risk & Summary Agent   │
      │ Prioritize risks         │
      │ Generate executive report│
      └──────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ Structured JSON Report │
        └────────────────────────┘
```

---

# 🛠 Tech Stack

- **Python 3.10+**
- **LangGraph**
- **LangChain**
- **OpenAI GPT Models**
- **Pydantic**
- **python-dotenv**

---

# 📂 Project Structure

```text
multi-agent-deal-review-pipeline/
│
├── agents/
│   ├── term_extraction.py
│   ├── compliance_review.py
│   └── risk_summary.py
│
├── models/
│   └── schemas.py
│
├── graph/
│   └── workflow.py
│
├── data/
│   ├── sample_deal.txt
│   ├── edge_case_deal.txt
│   └── policy_rules.json
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Python **3.10+**
- OpenAI API Key

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-deal-review-pipeline.git

cd multi-agent-deal-review-pipeline
```

### 2. Create a virtual environment

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4o-mini
```

---

# ▶️ Running the Pipeline

Run the application:

```bash
python main.py
```

The pipeline executes against:

- Standard deal document
- Edge-case deal document

and generates a structured review report for each.

---

# 📋 Workflow

### 1️⃣ Term Extraction Agent

Extracts:

- Financial terms
- Clauses
- Section references
- Page citations

Output includes evidence for every extracted field.

---

### 2️⃣ Compliance Review Agent

Compares extracted terms against policy rules.

Each rule receives one of:

- ✅ PASS
- ❌ FAIL
- ⚠️ NEEDS_HUMAN_REVIEW

Every decision includes supporting evidence.

---

### 3️⃣ Risk & Summary Agent

Produces:

- Executive summary
- Prioritized risks
- Overall compliance status
- Recommended actions

---

# 📤 Output

Example high-level JSON structure:

```json
{
  "executive_summary": "...",
  "overall_status": "PASS",
  "risks": [
    {
      "severity": "High",
      "issue": "...",
      "recommendation": "..."
    }
  ],
  "compliance_results": [
    {
      "rule": "...",
      "status": "PASS",
      "evidence": "Clause 5.2, Page 8"
    }
  ]
}
```

---

# ⚙️ Assumptions

- Every extracted term must reference an explicit clause, section, or page.
- Policy rules are supplied as structured JSON.
- Documents are provided as raw text extracts.
- Compliance decisions are evidence-backed.

---

# 🚨 Failure Handling

The pipeline is designed to fail safely.

### Structured Output Validation

Each agent uses **Pydantic** with:

```python
.with_structured_output()
```

to enforce schema consistency between workflow nodes.

### Exception Handling

Every agent is wrapped with exception handling.

If any of the following occur:

- API timeout
- Rate limit
- Parsing error
- Unexpected response

the error is appended to:

```python
state["errors"]
```

The orchestrator then safely terminates the workflow without crashing.

---

# ⚠️ Ambiguity Handling

The system automatically flags uncertain cases as:

```text
NEEDS_HUMAN_REVIEW
```

Examples include:

- Missing clauses
- Undefined values (e.g., "TBD")
- Ambiguous legal language
- Missing references
- Incomplete financial terms

---

# 📌 Current Limitations

- Supports **raw text (.txt)** inputs only.
- OCR/PDF ingestion is not included.
- Mathematical financial calculations (e.g., DSCR verification) rely on LLM reasoning and can be enhanced using dedicated computation tools.

---

# 🔮 Future Improvements

- PDF & OCR document ingestion
- Vector database for clause retrieval
- Parallel agent execution
- Human-in-the-loop review interface
- Audit logs and workflow visualization
- Financial calculation engine
- RAG-powered policy retrieval
- Support for multiple document formats

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

Developed using **LangGraph**, **LangChain**, **OpenAI**, and **Pydantic** to demonstrate a deterministic multi-agent workflow for enterprise financial document review.

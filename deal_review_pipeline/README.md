# Multi-Agent Deal Review Pipeline

An enterprise-grade, deterministic multi-agent workflow designed to review financial deal documents, evaluate compliance against explicit policy rules, and generate an evidence-backed executive report with prioritized risk analysis. Built using **LangGraph**, **LangChain**, and **Pydantic** structured outputs.

---

## 1. Architecture & Workflow

The pipeline decouples complex document analysis into specialized agents working over a shared state memory:


[Deal Document + Policy Rules JSON]
│
▼
┌─────────────────┐
│  Orchestrator   │  <── Manages Shared State & Execution Flow
└────────┬────────┘
│
▼
1. Term Extraction Agent   ──> Extracts terms + clause/page citations
│
▼
2. Compliance Review Agent ──> Checks terms vs. rules (PASS / FAIL / NEEDS_HUMAN_REVIEW)
│
▼
3. Risk & Summary Agent    ──> Prioritizes risks & builds executive summary
│
▼
┌─────────────────┐
│  Final Report   │  ──> Unified structured JSON output
└─────────────────┘

---

## 2. Setup & Execution Instructions

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Installation
1. Clone the repository and navigate into the folder:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/multi-agent-deal-review-pipeline.git](https://github.com/YOUR_USERNAME/multi-agent-deal-review-pipeline.git)
   cd multi-agent-deal-review-pipeline

   Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activa

Install dependencies:

Bash
pip install -r requirements.txt

Configure your .env file in the project root:

Code snippet
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4o-mini  

Running the Pipeline
Execute main.py to run the pipeline across both the normal test case and the edge case:

Bash
python main.py

3. Assumptions, Failure Handling & Limitations
Key Assumptions
Traceability: Every extracted term and compliance evaluation must reference an explicit clause, section, or page number.

Ambiguity Escalation: Any missing terms, undefined indexes (e.g., "TBD"), or ambiguous language automatically flag a compliance rule as NEEDS_HUMAN_REVIEW.

Failure-Handling Strategy
Structured Pydantic Enforcement: Agents utilize .with_structured_output() to guarantee contract validity between workflow nodes.

State Error Catching: Each agent node is wrapped in exception handlers. If an API timeout, rate limit, or parsing failure occurs, the error string is logged to state["errors"], and the orchestrator safely terminates the pipeline without crashing.

Limitations
Currently accepts raw text extracts (.txt); production deployment would require an OCR/PDF ingestion pre-processing agent for scanned documents.

Compliance checks rely on structured LLM evaluation against rules; mathematical ratio verifications (e.g., complex DSCR formulas) could be enhanced by integrating a dedicated Code/Math Execution Tool.


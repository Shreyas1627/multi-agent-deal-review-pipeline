import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import RiskAndSummaryOutput
from src.state import DealReviewState


def run_risk_agent(state: DealReviewState) -> DealReviewState:
    """
    Risk and Summary Agent:
    Identifies and prioritizes risks, flags missing/ambiguous info, and produces 
    an executive summary with follow-up actions.
    """
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
    structured_llm = llm.with_structured_output(RiskAndSummaryOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior Chief Risk Officer and Executive Deal Summarizer.
Analyze the extracted deal terms and the compliance review matrix to produce:
1. Prioritized Risks: Classify risks into Financial, Legal, Operational, or Compliance categories. Assign severity (High/Medium/Low) and recommend clear mitigations.
2. Executive Summary: A concise, executive-level overview of the deal, its material terms, compliance posture, and key risks.
3. Recommended Next Steps: Actionable follow-up steps for the underwriting/deal team (especially addressing any failed rules or missing information)."""),
        ("user", """Extracted Terms:
{extracted_terms}

Compliance Matrix:
{compliance_matrix}

Generate the risk analysis and executive summary.""")
    ])

    chain = prompt | structured_llm

    try:
        extracted_str = state["extraction_output"].model_dump_json(indent=2) if state["extraction_output"] else "{}"
        compliance_str = state["compliance_output"].model_dump_json(indent=2) if state["compliance_output"] else "{}"
        
        risk_result = chain.invoke({
            "extracted_terms": extracted_str,
            "compliance_matrix": compliance_str
        })
        state["risk_summary_output"] = risk_result
        state["status"] = "Risk Analysis Completed"
    except Exception as e:
        state["errors"].append(f"Risk Agent Error: {str(e)}")
        state["status"] = "Risk Analysis Failed"

    return state
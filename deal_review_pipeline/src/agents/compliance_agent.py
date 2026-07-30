import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import ComplianceReviewOutput
from src.state import DealReviewState


def run_compliance_agent(state: DealReviewState) -> DealReviewState:
    """
    Compliance Review Agent:
    Checks extracted terms against an explicit policy rule set, returning pass, fail,
    or needs human review, with evidence and rationale.
    """
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    structured_llm = llm.with_structured_output(ComplianceReviewOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a rigorous Compliance Review Officer.
You will receive:
1. Extracted terms from a deal document (with source references).
2. A JSON policy/compliance rule set.

Your task is to evaluate EACH policy rule against the extracted terms:
- Status choices: "PASS", "FAIL", or "NEEDS_HUMAN_REVIEW".
- Use "NEEDS_HUMAN_REVIEW" if the document is ambiguous, mentions "TBD", or lacks enough detail to prove compliance.
- Evidence: Quote or cite the extracted term value supporting your decision.
- Source Reference: Include the section or clause reference from the extracted terms.
- Rationale: Briefly explain why it passed, failed, or requires review.
- Overall Status: Set to APPROVED if all pass, REJECTED if any fail, or ESCALATED_FOR_REVIEW if any need human review."""),
        ("user", """Extracted Terms:
{extracted_terms}

Policy Rule Set:
{policy_rules}

Perform the compliance review.""")
    ])

    chain = prompt | structured_llm

    try:
        extracted_terms_str = state["extraction_output"].model_dump_json(indent=2) if state["extraction_output"] else "No terms extracted."
        compliance_result = chain.invoke({
            "extracted_terms": extracted_terms_str,
            "policy_rules": state["policy_rules_json"]
        })
        state["compliance_output"] = compliance_result
        state["status"] = "Compliance Review Completed"
    except Exception as e:
        state["errors"].append(f"Compliance Agent Error: {str(e)}")
        state["status"] = "Compliance Review Failed"

    return state
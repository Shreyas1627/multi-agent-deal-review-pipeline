import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import TermExtractionOutput
from src.state import DealReviewState


def run_extraction_agent(state: DealReviewState) -> DealReviewState:
    """
    Term Extraction Agent:
    Extracts material terms from the deal document and preserves references 
    to supporting clauses or sections.
    """
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    structured_llm = llm.with_structured_output(TermExtractionOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert financial and legal Term Extraction Agent.
Your job is to carefully read a commercial deal document and extract all material terms including:
- Parties involved
- Monetary values and principal amounts
- Dates and timelines
- Interest rates or fee structures
- Obligations and financial covenants
- Collateral, exclusions, and legal conditions

CRITICAL REQUIREMENTS:
1. Traceability: For EVERY extracted term, you MUST provide the exact source reference (e.g., "Section 2.1", "Clause 3.2", "Page 1").
2. Uncertainty: If a term is vague, incomplete, or marked "TBD", set confidence to "Low" or "Medium" and add notes in ambiguity_notes.
3. Missing Terms: List any standard commercial terms that appear to be missing from the document."""),
        ("user", "Analyze the following deal document:\n\n{deal_text}")
    ])

    chain = prompt | structured_llm

    try:
        extraction_result = chain.invoke({"deal_text": state["deal_document_text"]})
        state["extraction_output"] = extraction_result
        state["status"] = "Extraction Completed"
    except Exception as e:
        state["errors"].append(f"Extraction Agent Error: {str(e)}")
        state["status"] = "Extraction Failed"

    return state
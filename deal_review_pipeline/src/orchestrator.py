from langgraph.graph import StateGraph, END
from src.state import DealReviewState
from src.schemas import FinalDealReport
from src.agents.extraction_agent import run_extraction_agent
from src.agents.compliance_agent import run_compliance_agent
from src.agents.risk_agent import run_risk_agent


def finalize_report(state: DealReviewState) -> DealReviewState:
    """
    Orchestrator Node:
    Combines agent outputs into one coherent final report and handles fallback state if errors occurred.
    """
    if state["errors"] or not (state["extraction_output"] and state["compliance_output"] and state["risk_summary_output"]):
        state["status"] = f"Pipeline Completed with Errors: {', '.join(state['errors'])}"
        return state

    report = FinalDealReport(
        deal_title="Commercial Deal Evaluation Report",
        term_extraction=state["extraction_output"],
        compliance_review=state["compliance_output"],
        risk_and_summary=state["risk_summary_output"]
    )
    
    state["final_report"] = report
    state["status"] = "Pipeline Successfully Completed"
    return state


def build_deal_review_graph():
    """
    Constructs and compiles the LangGraph StateGraph for the Multi-Agent Deal Review Pipeline.
    """
    workflow = StateGraph(DealReviewState)

    # Add Nodes
    workflow.add_node("TermExtraction", run_extraction_agent)
    workflow.add_node("ComplianceReview", run_compliance_agent)
    workflow.add_node("RiskAndSummary", run_risk_agent)
    workflow.add_node("FinalizeReport", finalize_report)

    # Define Sequential Flow
    workflow.set_entry_point("TermExtraction")
    workflow.add_edge("TermExtraction", "ComplianceReview")
    workflow.add_edge("ComplianceReview", "RiskAndSummary")
    workflow.add_edge("RiskAndSummary", "FinalizeReport")
    workflow.add_edge("FinalizeReport", END)

    return workflow.compile()
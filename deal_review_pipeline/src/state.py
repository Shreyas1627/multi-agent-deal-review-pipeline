from typing import TypedDict, Optional, List, Dict, Any
from src.schemas import (
    TermExtractionOutput,
    ComplianceReviewOutput,
    RiskAndSummaryOutput,
    FinalDealReport
)


class DealReviewState(TypedDict):
    # Inputs
    deal_document_text: str
    policy_rules_json: str
    
    # Shared Workflow State (Agent Outputs)
    extraction_output: Optional[TermExtractionOutput]
    compliance_output: Optional[ComplianceReviewOutput]
    risk_summary_output: Optional[RiskAndSummaryOutput]
    final_report: Optional[FinalDealReport]
    
    # Error & Execution Tracking
    errors: List[str]
    status: str
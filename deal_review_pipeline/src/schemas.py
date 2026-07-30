from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ==========================================
# 1. TERM EXTRACTION SCHEMAS
# ==========================================
class ExtractedTerm(BaseModel):
    term_name: str = Field(description="Name of the term (e.g., Loan Amount, Interest Rate, Covenants)")
    value: str = Field(description="Extracted value or description of the term")
    source_reference: str = Field(description="Section, clause, or page reference for traceability")
    confidence: Literal["High", "Medium", "Low"] = Field(description="Confidence level of extraction")
    ambiguity_notes: Optional[str] = Field(default=None, description="Notes if the term is ambiguous or unclear")


class TermExtractionOutput(BaseModel):
    parties: List[str] = Field(default_factory=list, description="Parties involved in the deal")
    extracted_terms: List[ExtractedTerm] = Field(default_factory=list, description="List of material terms extracted")
    missing_critical_terms: List[str] = Field(default_factory=list, description="Critical terms that appear to be missing")


# ==========================================
# 2. COMPLIANCE REVIEW SCHEMAS
# ==========================================
class ComplianceCheckResult(BaseModel):
    rule_id: str = Field(description="Identifier of the policy rule being checked")
    rule_description: str = Field(description="Description of the compliance rule")
    status: Literal["PASS", "FAIL", "NEEDS_HUMAN_REVIEW"] = Field(description="Compliance evaluation status")
    evidence: str = Field(description="Quote or extracted term supporting this determination")
    source_reference: str = Field(description="Clause or section reference")
    rationale: str = Field(description="Explanation of why it passed, failed, or needs review")


class ComplianceReviewOutput(BaseModel):
    compliance_matrix: List[ComplianceCheckResult] = Field(default_factory=list)
    overall_compliance_status: Literal["APPROVED", "REJECTED", "ESCALATED_FOR_REVIEW"]


# ==========================================
# 3. RISK & SUMMARY SCHEMAS
# ==========================================
class RiskItem(BaseModel):
    risk_category: Literal["Financial", "Legal", "Operational", "Compliance"] = Field(description="Category of risk")
    severity: Literal["High", "Medium", "Low"] = Field(description="Priority/Severity of the risk")
    description: str = Field(description="Detailed explanation of the risk")
    mitigation_or_followup: str = Field(description="Recommended follow-up action or mitigation")


class RiskAndSummaryOutput(BaseModel):
    prioritized_risks: List[RiskItem] = Field(default_factory=list)
    executive_summary: str = Field(description="Concise executive summary of the deal and review findings")
    recommended_next_steps: List[str] = Field(default_factory=list, description="Actionable follow-up steps")


# ==========================================
# 4. FINAL REPORT SCHEMA
# ==========================================
class FinalDealReport(BaseModel):
    deal_title: str
    term_extraction: TermExtractionOutput
    compliance_review: ComplianceReviewOutput
    risk_and_summary: RiskAndSummaryOutput
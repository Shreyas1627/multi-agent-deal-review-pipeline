import os
import json
from dotenv import load_dotenv
from src.orchestrator import build_deal_review_graph
from src.state import DealReviewState

# Load API keys from .env
load_dotenv()


def run_pipeline_on_file(deal_file_path: str, rules_file_path: str, test_name: str):
    print(f"\n==================================================")
    print(f"RUNNING PIPELINE: {test_name}")
    print(f"==================================================")

    with open(deal_file_path, "r", encoding="utf-8") as f:
        deal_text = f.read()

    with open(rules_file_path, "r", encoding="utf-8") as f:
        policy_rules = f.read()

    # Initialize State
    initial_state = DealReviewState(
        deal_document_text=deal_text,
        policy_rules_json=policy_rules,
        extraction_output=None,
        compliance_output=None,
        risk_summary_output=None,
        final_report=None,
        errors=[],
        status="Starting"
    )

    # Run Graph
    app = build_deal_review_graph()
    final_state = app.invoke(initial_state)

    # Print Summary Results
    print(f"\n[STATUS]: {final_state['status']}")

    if final_state["errors"]:
        print("\n[ERRORS ENCOUNTERED]:")
        for error in final_state["errors"]:
            print(f" - {error}")
        return

    report = final_state["final_report"]
    print(f"\n--- EXECUTIVE SUMMARY ---")
    print(report.risk_and_summary.executive_summary)

    print(f"\n--- COMPLIANCE MATRIX ---")
    print(f"Overall Status: {report.compliance_review.overall_compliance_status}")
    for item in report.compliance_review.compliance_matrix:
        print(f" [{item.status}] {item.rule_id}: {item.rule_description}")
        print(f"        Evidence: '{item.evidence}' ({item.source_reference})")
        print(f"        Rationale: {item.rationale}")

    print(f"\n--- PRIORITIZED RISKS ---")
    for risk in report.risk_and_summary.prioritized_risks:
        print(f" [{risk.severity} - {risk.risk_category}] {risk.description}")
        print(f"        Mitigation: {risk.mitigation_or_followup}")

    # Optionally save full structured report to disk
    output_filename = f"report_{test_name.lower().replace(' ', '_')}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    print(f"\nFull structured JSON report saved to: {output_filename}")


if __name__ == "__main__":
    # Get the absolute directory where main.py is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    rules_path = os.path.join(BASE_DIR, "data", "policy_rules.json")
    normal_deal_path = os.path.join(BASE_DIR, "data", "sample_deal_normal.txt")
    edge_deal_path = os.path.join(BASE_DIR, "data", "sample_deal_edge.txt")

    # 1. Test Normal Case
    run_pipeline_on_file(normal_deal_path, rules_path, "Normal Case")

    # 2. Test Edge Case
    run_pipeline_on_file(edge_deal_path, rules_path, "Edge Case")
#!/usr/bin/env python3
"""
Root entrypoint for the SOC Operations Tabletop Incident Triage Simulator (CLI).
Supports interactive terminal mode or automated flags for automated auditing and CI.
"""

import sys
import os
import argparse

# Ensure current working directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cli.console import ConsoleInterface
from src.core.baseline_auditor import BaselineAuditor
from src.core.asset_manager import AssetManager
from src.playbooks.playbook_registry import PlaybookRegistry
from src.core.engine import TabletopSession
from src.core.report_generator import AfterActionReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description="SOC Operations & Threat Detection - Tabletop Incident Triage Simulator"
    )
    parser.add_argument("--audit", action="store_true", help="Run read-only baseline security audit on sample config")
    parser.add_argument("--config", type=str, default=None, help="Path to custom sshd_config to audit")
    parser.add_argument("--baseline", type=str, default=None, help="Path to custom baseline JSON file")
    parser.add_argument("--list-scenarios", action="store_true", help="List all available tabletop scenarios")
    parser.add_argument("--list-playbooks", action="store_true", help="List all documented Incident Response Playbooks")
    parser.add_argument("--list-assets", action="store_true", help="Display asset inventory")
    parser.add_argument("--auto-simulate", type=str, default=None, help="Run an automated benchmark simulation on scenario ID (e.g. SCN-SSH-001)")

    args = parser.parse_args()

    if args.audit:
        auditor = BaselineAuditor(baseline_path=args.baseline)
        config_path = args.config or os.path.join("fixtures", "linux_fixtures", "sshd_config_sample.txt")
        report = auditor.audit_config(config_path)
        print(f"\n[+] {report.read_only_notice}\n")
        print(f"Target Host: {report.target_host} | Compliance Score: {report.compliance_score}%")
        print(f"Checks: {report.total_checks} | Passed: {report.passed_checks} | Failed: {report.failed_checks} | Policy: {report.policy_review_checks}\n")
        for f in report.findings:
            line_str = f"Line {f.evidence_line_number}" if f.evidence_line_number else "N/A"
            print(f"- [{f.check_id}] {f.setting_name}: observed '{f.observed_value}' vs recommended '{f.recommended_value}'")
            print(f"  Severity: {f.severity} | Class: {f.classification} | {line_str}")
            print(f"  Rationale: {f.rationale}")
            print(f"  Safe Remediation: {f.safe_remediation}\n")
        return

    if args.list_scenarios:
        reg = PlaybookRegistry()
        print("\nAvailable Tabletop Scenarios:")
        for s in reg.get_all_scenarios():
            print(f"  - [{s['id']}] {s['title']} (Asset: {s.get('target_asset_id')}, Severity: {s['initial_severity']})")
        return

    if args.list_playbooks:
        reg = PlaybookRegistry()
        print("\nAvailable Incident Response Playbooks (NIST SP 800-61r2):")
        for p in reg.get_all_playbooks():
            print(f"  - [{p.id}] {p.title} (v{p.version}) - Threat: {p.primary_threat}")
        return

    if args.list_assets:
        am = AssetManager()
        print("\nAsset Inventory:")
        for a in am.get_all_assets():
            print(f"  - [{a.asset_id}] {a.hostname} ({a.environment}, Criticality: {a.criticality.upper()}, Owner: {a.owner_role})")
        return

    if args.auto_simulate:
        reg = PlaybookRegistry()
        am = AssetManager()
        auditor = BaselineAuditor()
        scn = reg.get_scenario_by_id(args.auto_simulate)
        if not scn:
            print(f"Error: Scenario '{args.auto_simulate}' not found.")
            sys.exit(1)

        print(f"Running automated benchmark simulation for {scn['title']}...")
        session = TabletopSession(scn, am)
        while not session.is_completed:
            cur = session.current_inject
            # Pick recommended option
            rec_opt = next((o for o in cur.options if o.is_recommended), cur.options[0])
            session.process_decision(rec_opt.id)

        score_res = session.evaluate_session()
        audit_rep = auditor.audit_config("fixtures/linux_fixtures/sshd_config_sample.txt")
        gen = AfterActionReportGenerator(session, score_res, audit_rep)
        os.makedirs("reports", exist_ok=True)
        gen.export_markdown(f"reports/AAR_{session.scenario_id}.md")
        gen.export_json(f"reports/AAR_{session.scenario_id}.json")
        print(f"Simulation completed! Score: {score_res.total_score}/{score_res.max_possible_score} ({score_res.score_percentage}%) - Grade: {score_res.grade}")
        print(f"Reports written to reports/AAR_{session.scenario_id}.md and .json")
        return

    # Default: Interactive console menu
    cli = ConsoleInterface()
    cli.main_menu()


if __name__ == "__main__":
    main()

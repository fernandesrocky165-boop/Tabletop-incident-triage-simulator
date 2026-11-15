# SOC Operations & Threat Detection: Tabletop Incident Triage Simulator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/standard-NIST%20SP%20800--61%20Rev.%202-red.svg)](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
[![MITRE ATT&CK](https://img.shields.io/badge/framework-MITRE%20ATT%26CK-orange.svg)](https://attack.mitre.org/)
[![Tests Status](https://img.shields.io/badge/tests-15%2F15%20passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade cybersecurity incident response simulation, assessment, and baseline audit platform engineered for **RedKross Internship Task 2: SOC Operations & Threat Detection — Incident Response Playbook**.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Capabilities](#key-capabilities)
3. [System Architecture](#system-architecture)
4. [RedKross Fixtures Integration](#redkross-fixtures-integration)
5. [Installation & Setup](#installation--setup)
6. [Execution & Usage](#execution--usage)
   - [Web Dashboard GUI](#1-web-dashboard-gui)
   - [Interactive Terminal CLI](#2-interactive-terminal-cli)
   - [Read-Only Baseline Auditor](#3-read-only-baseline-auditor)
   - [Automated Benchmark Simulation](#4-automated-benchmark-simulation)
7. [Incident Response Playbooks Catalog](#incident-response-playbooks-catalog)
8. [Testing & Verification Evidence](#testing--verification-evidence)
9. [After-Action Report (AAR) Deliverables](#after-action-report-aar-deliverables)
10. [Submission Assets & Video Guide](#submission-assets--video-guide)
11. [References & Standards](#references--standards)

---

## Project Overview

In a modern Security Operations Center (SOC), incident responders must rapidly triage security alerts, prioritize critical enterprise assets, preserve volatile forensic evidence, execute precise containment actions with minimal operational collateral disruption, and apply verified system hardening.

This project delivers a **Tabletop Incident Triage Simulator** that:
- Aligns directly with the **NIST SP 800-61 Rev. 2** Computer Security Incident Handling Guide.
- Integrates the supplied **RedKross Linux configuration fixtures** and asset inventory.
- Implements a dedicated **Read-Only Baseline Security Auditor** distinguishing definite mismatches from policy-dependent settings.
- Features multi-vector tabletop scenarios (SSH Brute Force & Root Compromise, Web Shell RCE, Insider Data Exfiltration).
- Provides an automated **Scoring & After-Action Report (AAR)** engine exportable to Markdown, JSON, and PDF.
- Delivers both an interactive **Web Dashboard GUI** and a full **Terminal CLI**.

---

## Key Capabilities

- **NIST SP 800-61 Rev. 2 Lifecycle Engine**: Progressive phase tracking through *Detection & Triage*, *Investigation & Forensics*, *Containment*, *Eradication & Remediation*, *Recovery*, and *Post-Incident Activity*.
- **Dynamic Scenario Injector**: Simulates realistic SIEM alerts, auth logs, process spawns, and network telemetry arriving dynamically with timestamp offsets (`T+00:00`, `T+00:15`, `T+00:35`, etc.).
- **Triage Matrix & Context-Aware Asset Scoring**: Cross-references `asset_inventory.csv` to calculate asset-weighted incident priority scores (`P1 - Critical`, `P2 - High`, `P3 - Medium`, `P4 - Low`).
- **Read-Only Baseline Security Auditor**: Parses SSH daemon configurations line-by-line with exact line number tracking, evaluates observed settings against baseline policies, separates definite mismatches from policy-dependent variables, and produces safe remediation suggestions without modifying target host files.
- **Incident Commander Scoring Model**: Evaluates triage accuracy, SLA response timeliness, volatile memory/log preservation rate, and penalizes indiscriminate collateral service disruption.
- **Dual Interface**:
  - **Web GUI**: Modern Cyber SOC dark theme dashboard with live telemetry terminal, decision buttons, progress stepper, and print-ready AAR view.
  - **CLI**: Interactive colored ANSI terminal console supporting interactive play and automated benchmark execution.

---

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                              USER INTERFACES                                      |
|                                                                                   |
|    +-----------------------------+           +------------------------------+     |
|    |      Flask Web GUI          |           |      Terminal CLI            |     |
|    | (Cyber SOC Dark Dashboard)  |           | (Interactive & CI/CD Mode)   |     |
|    +--------------+--------------+           +--------------+---------------+     |
+-------------------|-----------------------------------------|---------------------+
                    |                                         |
+-------------------|-----------------------------------------|---------------------+
|                   v                                         v                     |
|                               CORE ENGINE LAYER                                   |
|                                                                                   |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   |   TabletopSession     |   |    AssetManager      |   |  BaselineAuditor   |   |
|   | - NIST Phase Stepper  |   | - Context Risk Score |   | - Read-Only Parser |   |
|   | - Inject Sequencer    |   | - Asset Inventory    |   | - Definite vs      |   |
|   | - Decision Evaluator  |   |   (AST-001..AST-004) |   |   Policy Checker   |   |
|   +-----------+-----------+   +----------+-----------+   +---------+----------+   |
|               |                          |                         |              |
|               +-------------------+      |                         |              |
|                                   |      |                         |              |
|                                   v      v                         |              |
|                      +--------------------------+                  |              |
|                      |  Triage Scoring Engine   |                  |              |
|                      | - Accuracy & Timeliness  |                  |              |
|                      | - Forensics Preservation |                  |              |
|                      | - Collateral Penalty     |                  |              |
|                      +------------+-------------+                  |              |
|                                   |                                |              |
|                                   v                                v              |
|                      +--------------------------------------------------+         |
|                      |        AfterActionReportGenerator (AAR)          |         |
|                      |   Exports: Markdown, JSON, HTML & Print / PDF    |         |
|                      +--------------------------------------------------+         |
+-----------------------------------------------------------------------------------+
                                            |
+-------------------------------------------|---------------------------------------+
|                                           v                                       |
|                                 DATA & FIXTURES LAYER                             |
|                                                                                   |
|  +-----------------------------+  +--------------------------------------------+  |
|  |     RedKross Fixtures       |  |          Playbook & Scenario Data          |  |
|  | - asset_inventory.csv       |  | - IR-PB-001: Linux SSH Compromise          |  |
|  | - linux_baseline.json       |  | - IR-PB-002: Web Application Exploit       |  |
|  | - sshd_config_sample.txt    |  | - IR-PB-003: Insider Data Exfiltration     |  |
|  | - sshd_config_hardened_...  |  | - SCN-SSH-001, SCN-WEB-002, SCN-EXFIL-003  |  |
|  +-----------------------------+  +--------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## RedKross Fixtures Integration

The platform natively ingests and evaluates all 5 resources provided in `fixtures/linux_fixtures/`:

| Fixture File | Role in the Simulator & Auditor |
|---|---|
| `asset_inventory.csv` | Loaded by `AssetManager` to determine host ownership, environment, SSH admin authorization, backup status, and criticality weighting (`AST-001` through `AST-004`). |
| `linux_baseline.json` | Serves as the authoritative policy standard (`synthetic-linux-baseline-v1`) against which host configuration parameters (`LIN-01` to `LIN-07`) are verified. |
| `sshd_config_sample.txt` | Target unhardened configuration fixture parsed by `BaselineAuditor`, identifying line numbers and configuration defects. |
| `sshd_config_hardened_reference.txt` | Trusted reference configuration used in tabletop eradication steps and side-by-side diff viewers. |
| `hardening_task_notes.txt` | Defines strict operational directives: read-only checking, line/field evidence reporting, definite mismatch vs policy distinction, and safe remediation recommendations without automated tampering. |

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher.
- `pip` package manager.
- Git (for cloning and repository management).

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/SOC-Tabletop-Incident-Triage-Simulator.git
cd SOC-Tabletop-Incident-Triage-Simulator

# 2. (Optional) Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Execution & Usage

### 1. Web Dashboard GUI
Launch the web interface for an interactive SOC experience:
```bash
python run_web.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```
- **Dashboard (`/`)**: Active alert stats, scenario launcher, and asset inventory overview.
- **Tabletop Room (`/tabletop`)**: Interactive simulation room with NIST phase progression, terminal log stream, real-time timer, and decision evaluation.
- **Playbooks Library (`/playbooks`)**: Interactive SOPs, checklists, and escalation paths.
- **Baseline Auditor (`/auditor`)**: Live read-only configuration checker with side-by-side fixture diff.
- **After-Action Reports (`/reports/<scenario_id>`)**: Comprehensive debriefing with printable PDF view.

---

### 2. Interactive Terminal CLI
For command-line triage exercises:
```bash
python run_cli.py
```
Provides an interactive menu with options to launch simulations, run baseline audits, inspect assets, and browse playbooks.

---

### 3. Read-Only Baseline Auditor
Execute a passive audit against the sample configuration fixture:
```bash
python run_cli.py --audit
```
Or specify custom configuration and baseline files:
```bash
python run_cli.py --audit --config path/to/sshd_config --baseline path/to/baseline.json
```

**Sample Output:**
```
[+] READ-ONLY AUDIT NOTICE: This checker performs passive analysis only. No system files or operational configurations were altered.

Target Host: lab-linux-01 | Compliance Score: 14.3%
Checks: 7 | Passed: 1 | Failed: 1 | Policy: 5

- [LIN-01] PermitRootLogin: observed 'yes' vs recommended 'no'
  Severity: HIGH | Class: Definite Mismatch | Line 3
  Rationale: Direct root login over SSH bypasses non-repudiation and exposes the superuser account to brute-force credential stuffing.
  Safe Remediation: Set 'PermitRootLogin no' in /etc/ssh/sshd_config. Require unprivileged users to authenticate with key pairs and escalate privileges using sudo.

- [LIN-02] PasswordAuthentication: observed 'yes' vs recommended 'no_or_controlled'
  Severity: MEDIUM | Class: Policy-Dependent Setting | Line 4
  Rationale: Password-based SSH authentication is vulnerable to interception, offline dictionary attacks, and credential spraying.
  Safe Remediation: Set 'PasswordAuthentication no' once authorized SSH public keys are configured and verified. For legacy needs, require MFA.

- [LIN-03] PermitEmptyPasswords: observed 'no' vs recommended 'no'
  Severity: PASS | Class: Compliant / Pass | Line 6
  Rationale: Empty passwords permit unauthenticated remote interactive shell access, leading to catastrophic compromise.
  Safe Remediation: Explicitly set 'PermitEmptyPasswords no'. Ensure all system accounts enforce non-empty credentials.
...
```

---

### 4. Automated Benchmark Simulation
Run a non-interactive simulation benchmark and generate After-Action Reports:
```bash
python run_cli.py --auto-simulate SCN-SSH-001
```
Reports are automatically compiled into `reports/AAR_SCN-SSH-001.md` and `reports/AAR_SCN-SSH-001.json`.

---

## Incident Response Playbooks Catalog

| Playbook ID | Playbook Title | Target Asset | Primary Threat & MITRE ATT&CK Mapping |
|---|---|---|---|
| **IR-PB-001** | Linux Host Compromise & SSH Hardening | `lab-linux-01` (`AST-001`) | SSH Brute-Force (`T1110.001`), Valid Accounts (`T1078.003`), Rogue Cryptominer (`T1496`), Remote Services (`T1021.004`) |
| **IR-PB-002** | Web Application Exploit & Reverse Shell | `lab-web-01` (`AST-003`) | Exploit Public Application (`T1190`), Web Shell (`T1505.003`), Unix Shell Execution (`T1059.004`), Credential Access (`T1552.001`) |
| **IR-PB-003** | Data Exfiltration & Insider Threat | `lab-archive-01` (`AST-004`) | SFTP Alternative Protocol Exfiltration (`T1048.002`), Leaked Credentials (`T1078.002`), Discovery (`T1083`) |

Full SOP documentation and step-by-step checklists are available in [docs/PLAYBOOKS_GUIDE.md](file:///c:/Users/vibhas%20pawar/OneDrive/Desktop/RedKross%20Task%202%20Assignment%20Resources/docs/PLAYBOOKS_GUIDE.md).

---

## Testing & Verification Evidence

The system includes an automated test suite verifying asset loading, configuration parsing, line-number tracking, definite mismatch detection, scoring calculations, and report generation.

Run all tests:
```bash
python -m unittest discover tests -v
```

**Verification Results:**
```
test_contextual_impact_evaluation (tests.test_asset_manager.TestAssetManager.test_contextual_impact_evaluation) ... ok
test_high_criticality_filter (tests.test_asset_manager.TestAssetManager.test_high_criticality_filter) ... ok
test_inventory_loaded (tests.test_asset_manager.TestAssetManager.test_inventory_loaded) ... ok
test_lookup_by_hostname (tests.test_asset_manager.TestAssetManager.test_lookup_by_hostname) ... ok
test_lookup_by_id (tests.test_asset_manager.TestAssetManager.test_lookup_by_id) ... ok
test_audit_findings_classification (tests.test_baseline_auditor.TestBaselineAuditor.test_audit_findings_classification) ... ok
test_parse_sshd_config_line_numbers (tests.test_baseline_auditor.TestBaselineAuditor.test_parse_sshd_config_line_numbers) ... ok
test_read_only_guarantee (tests.test_baseline_auditor.TestBaselineAuditor.test_read_only_guarantee) ... ok
test_linux_compromise_playbook_schema (tests.test_playbooks.TestPlaybooks.test_linux_compromise_playbook_schema) ... ok
test_playbooks_registered (tests.test_playbooks.TestPlaybooks.test_playbooks_registered) ... ok
test_scenarios_registered (tests.test_playbooks.TestPlaybooks.test_scenarios_registered) ... ok
test_report_export (tests.test_report_generator.TestReportGenerator.test_report_export) ... ok
test_optimal_decision_progression (tests.test_simulation_engine.TestSimulationEngine.test_optimal_decision_progression) ... ok
test_session_initialization (tests.test_simulation_engine.TestSimulationEngine.test_session_initialization) ... ok
test_suboptimal_decision_penalties (tests.test_simulation_engine.TestSimulationEngine.test_suboptimal_decision_penalties) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.016s

OK (100% Passing)
```

Detailed test evidence and logs are documented in [docs/TEST_EVIDENCE.md](file:///c:/Users/vibhas%20pawar/OneDrive/Desktop/RedKross%20Task%202%20Assignment%20Resources/docs/TEST_EVIDENCE.md).

---

## After-Action Report (AAR) Deliverables

Upon completing a tabletop exercise, the system generates a standardized incident report:
- Sample Markdown Report: `reports/AAR_SCN-SSH-001.md`
- Sample JSON Data: `reports/AAR_SCN-SSH-001.json`
- Includes:
  1. Executive Summary & Incident Classification
  2. Asset Environmental Assessment (Criticality, Ownership, Admin access)
  3. Performance Grading & Metrics (Accuracy, SLA rate, Forensic rate, Collateral penalties)
  4. Chronological Decision Audit Trail
  5. Baseline Configuration Hardening Findings (Line-by-line evidence, definite vs policy mismatches, safe remediation)
  6. Strategic Lessons Learned & MITRE ATT&CK Mapping

---

## Submission Assets & Video Guide

To fulfill the internship submission criteria:
1. **GitHub Setup & Upload Guide:** Step-by-step instructions for publishing this repository to your friend's GitHub account are provided in [docs/GITHUB_UPLOAD_GUIDE.md](file:///c:/Users/vibhas%20pawar/OneDrive/Desktop/RedKross%20Task%202%20Assignment%20Resources/docs/GITHUB_UPLOAD_GUIDE.md).
2. **5–8 Minute Video Presentation Script:** A word-for-word, minute-by-minute recording walkthrough with visual slide-by-slide guidance is documented in [docs/VIDEO_PRESENTATION_SCRIPT.md](file:///c:/Users/vibhas%20pawar/OneDrive/Desktop/RedKross%20Task%202%20Assignment%20Resources/docs/VIDEO_PRESENTATION_SCRIPT.md).

---

## References & Standards
- [NIST SP 800-61 Rev. 2: Computer Security Incident Handling Guide](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/)
- [CIS Linux Benchmark & OpenSSH Hardening Guidelines](https://www.cisecurity.org/benchmark/ubuntu_linux)
- [RFC 4253: The Secure Shell (SSH) Transport Layer Protocol](https://datatracker.ietf.org/doc/html/rfc4253)

---

## License
This project is open-source and licensed under the [MIT License](LICENSE).

# System Architecture & Technical Specification

## 1. Overview
The **SOC Operations Tabletop Incident Triage Simulator** is an enterprise-grade cyber incident response simulation, assessment, and baseline audit platform. It was engineered specifically to address **RedKross Task 2: SOC Operations & Threat Detection - Incident Response Playbook**.

The platform simulates realistic multi-phase cybersecurity intrusions against registered assets, challenges security analysts with high-stakes triage decisions, evaluates actions against NIST and MITRE standards, conducts passive configuration audits, and produces publication-ready After-Action Reports (AAR).

---

## 2. Architecture Diagram

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

## 3. Core Component Design

### 3.1 Tabletop Simulation Engine (`src/core/engine.py`)
- **State Machine**: Tracks phase progression through all six NIST SP 800-61 Rev. 2 phases:
  1. *Detection & Triage*
  2. *Investigation & Forensics*
  3. *Containment*
  4. *Eradication & Remediation*
  5. *Recovery*
  6. *Post-Incident Activity (AAR)*
- **Inject Delivery**: Sequences telemetry logs, network connection tables, and SIEM alerts with realistic timestamp offsets (`T+00:00`, `T+00:15`, etc.).
- **Decision Engine**: Evaluates analyst actions, applying score adjustments, time increments, evidence preservation flags, and collateral disruption penalties.

### 3.2 Asset Correlation Manager (`src/core/asset_manager.py`)
- Reads `fixtures/linux_fixtures/asset_inventory.csv`.
- Dynamically assigns risk weights:
  - High Criticality (`lab-linux-01`, `lab-web-01`) = 1.5x multiplier.
  - Medium Criticality (`lab-linux-02`, `lab-archive-01`) = 1.2x multiplier.
- Computes context-aware incident priority (`P1 - Critical`, `P2 - High`, `P3 - Medium`, `P4 - Low`).

### 3.3 Read-Only Baseline Security Auditor (`src/core/baseline_auditor.py`)
- Directly implements the requirements from RedKross fixture notes (`hardening_task_notes.txt`).
- **Read-Only Guarantee**: Never modifies or writes to target configuration files.
- **Line-by-Line Tokenizer**: Retains exact line numbers and raw evidence strings from `sshd_config_sample.txt`.
- **Classification Engine**:
  - **Definite Mismatch**: Objective security defects (`PermitRootLogin yes`).
  - **Policy-Dependent Setting**: Configurations requiring organization policy alignment (`MaxAuthTries 12`, `ClientAliveInterval 0`, `AllowUsers *`).
  - **Compliant / Pass**: Settings matching hardened requirements (`PermitEmptyPasswords no`).
- **Safe Remediation Engine**: Generates copy-paste safe shell commands and directives without automated execution.

### 3.4 Scoring & Evaluation Engine (`src/models/scoring.py`)
- **Triage Accuracy (%)**: Ratio of correct playbook actions executed.
- **Forensic Preservation (%)**: Validates whether memory, sockets, and logs were dumped prior to disruptive actions (quarantine, power cycle).
- **Collateral Disruption (Points)**: Penalizes analysts who shut down non-target networks or wipe operational databases.
- **SLA Timeliness (%)**: Evaluates total simulated time against incident severity deadlines.
- **Incident Commander Grading**:
  - `S`: Master Incident Commander (&ge; 90%)
  - `A`: Senior SOC Analyst (&ge; 80%)
  - `B`: SOC Analyst II - Proficient (&ge; 70%)
  - `C`: Junior Analyst - Supervised (&ge; 60%)
  - `F`: Training Remediation Required (&lt; 60%)

---

## 4. MITRE ATT&CK & NIST Alignment

| NIST SP 800-61 Phase | MITRE ATT&CK Tactic | Simulator Inject & Verification |
|---|---|---|
| **Detection & Triage** | Initial Access (`TA0001`), Credential Access (`TA0006`) | Correlate brute force logs on `lab-linux-01`, evaluate asset inventory, calculate P1 priority. |
| **Investigation** | Execution (`TA0002`), Discovery (`TA0007`) | Identify `/tmp/.x_miner`, capture volatile memory, examine open sockets without tipping adversary. |
| **Containment** | Lateral Movement (`TA0008`), C2 (`TA0011`) | Surgical iptables isolation, kill rogue PTS session without taking down production platform. |
| **Eradication** | Defense Evasion (`TA0005`), Persistence (`TA0003`) | Run read-only baseline auditor, apply reference hardened config, validate with `sshd -t`. |
| **Recovery** | Impact (`TA0040`) | Restore clean system state, verify service availability, activate 72h heightened SIEM monitoring. |
| **Post-Incident** | Governance & Continuous Improvement | Export After-Action Report (AAR) with full audit trail and remediation roadmap. |

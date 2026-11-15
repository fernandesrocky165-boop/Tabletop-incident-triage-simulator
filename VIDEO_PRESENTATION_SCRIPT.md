# 5–8 Minute Video Presentation Script

Use this comprehensive walkthrough script to record the required **5–8 minute video presentation** for the RedKross Task 2 Submission.

---

## Video Quick Reference
- **Target Duration:** 5:30 to 7:00 minutes.
- **Recording Tools:** OBS Studio, Loom, Clipchamp, or Windows Game Bar (`Win + G`).
- **Screen Setup:**
  1. Have browser open at `http://127.0.0.1:5000` (Web Dashboard).
  2. Have terminal / PowerShell open in project root.
  3. Have VS Code open displaying project structure and `README.md`.

---

## Detailed Minute-by-Minute Script

```
+-----------------------------------------------------------------------------------------+
| [0:00 - 1:00] PART 1: Introduction & Assignment Objective                              |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
Display the **Web Dashboard** (`http://127.0.0.1:5000`) or the **README.md** title banner.

### What to say:
> "Hello everyone, my name is [Your Friend's Name], and today I am presenting my submission for **RedKross Task 2: SOC Operations & Threat Detection - Incident Response Playbook**.
>
> In modern Security Operations Centers, responding to cyber incidents requires rapid triage, structured playbooks, and careful containment to avoid collateral damage. For this task, I designed and implemented **SOC-TriageSim: an Enterprise Incident Response Playbook and Tabletop Incident Triage Simulator**.
>
> The project incorporates the provided **RedKross configuration fixtures**, implements a passive **Read-Only Baseline Security Auditor**, models real-world enterprise assets from `asset_inventory.csv`, aligns directly with the **NIST SP 800-61 Rev. 2** framework and **MITRE ATT&CK**, and provides both an interactive **Web Dashboard** and a scriptable **CLI tool**."

```
+-----------------------------------------------------------------------------------------+
| [1:00 - 2:15] PART 2: Architecture & RedKross Fixtures Integration                     |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
Switch to VS Code or GitHub file tree. Show:
1. `fixtures/linux_fixtures/asset_inventory.csv`
2. `fixtures/linux_fixtures/linux_baseline.json`
3. `fixtures/linux_fixtures/sshd_config_sample.txt`

### What to say:
> "Let's first examine the architecture and how the supplied RedKross resources were utilized.
>
> In `fixtures/linux_fixtures`, we have:
> - `asset_inventory.csv`, containing registered enterprise hosts including `lab-linux-01`, a high-criticality training platform asset.
> - `linux_baseline.json` and `sshd_config_sample.txt`, detailing observed SSH daemon configurations against recommended baseline standards.
>
> In compliance with the hardening task notes, I built a read-only baseline auditor located in `src/core/baseline_auditor.py`. It inspects configuration files line-by-line without altering the host, and critically distinguishes between **Definite Mismatches**—such as `PermitRootLogin yes`—and **Policy-Dependent Settings** like `MaxAuthTries` and `AllowUsers`."

```
+-----------------------------------------------------------------------------------------+
| [2:15 - 3:30] PART 3: Demonstration of the Read-Only Baseline Auditor                  |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
1. Open Terminal and run:
   ```bash
   python run_cli.py --audit
   ```
2. Switch to browser tab: `http://127.0.0.1:5000/auditor` to show the visual auditor UI with side-by-side config comparison.

### What to say:
> "Here is our Read-Only Baseline Auditor in action.
>
> When we run `python run_cli.py --audit`, the tool parses `sshd_config_sample.txt`. Notice how it reports:
> - The exact line number for each setting (e.g., Line 3 for `PermitRootLogin`).
> - The exact classification: `PermitRootLogin yes` is flagged as a **Definite Mismatch** with High severity, accompanied by an explanation of why direct root access breaks non-repudiation.
> - `PasswordAuthentication`, `MaxAuthTries`, and `AllowUsers` are classified as **Policy-Dependent Settings**, guiding administrators on organizational policy requirements.
> - And crucially, it highlights the **READ-ONLY AUDIT NOTICE**, ensuring that no automated, unverified changes are made to production systems.
>
> In the Web GUI, we also have an interactive side-by-side diff comparing the unhardened sample with the reference hardened configuration."

```
+-----------------------------------------------------------------------------------------+
| [3:30 - 5:15] PART 4: Live Tabletop Incident Triage Simulation                         |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
Navigate in browser to: `http://127.0.0.1:5000/tabletop` -> Click **Launch Exercise** on **Linux SSH Brute-Force & Root Compromise on lab-linux-01**.
Walk through the live injects:
1. Show Inject 1: SIEM alert on 1,200 failed logins. Click option A (Triage priority).
2. Show Inject 2: Root compromise detected. Show the telemetry stream box. Choose Option A (Dump volatile RAM and preserve artifacts).
3. Show Inject 3: Lateral movement attempt. Choose Option A (Targeted host firewall quarantine).
4. Show Inject 4: Forensic baseline check. Choose Option A (Audit sshd_config).
5. Show Inject 5: Eradication and syntax validation (`sshd -t`). Choose Option A.

### What to say:
> "Now let's launch the Tabletop Incident Triage Simulator. We will select **Scenario 1: Linux SSH Brute-Force & Root Compromise on lab-linux-01**.
>
> As we begin, the top phase stepper shows our progress across the NIST lifecycle:
> - **Inject 1 (Triage):** Over 1,200 failed SSH logins are detected. We look up `lab-linux-01` in the asset inventory, confirm it is a High-criticality Platform host, and escalate to P1 Critical. Notice the immediate score delta: +15 points.
> - **Inject 2 (Investigation):** An adversary succeeds in logging in as root due to the unhardened configuration, spawning a hidden cryptominer `/tmp/.x_miner`. Rather than panic and prematurely reboot the server—which would destroy volatile RAM—we preserve forensic memory and process tables.
> - **Inject 3 (Containment):** The attacker attempts lateral movement to `lab-archive-01`. We apply targeted host iptables rules and terminate the attacker session with zero collateral damage to benign platform services.
> - **Inject 4 & 5 (Eradication & Remediation):** We trigger our read-only audit to identify the root cause, rotate credentials, apply the hardened baseline directives, and validate syntax with `sshd -t`."

```
+-----------------------------------------------------------------------------------------+
| [5:15 - 6:30] PART 5: After-Action Report (AAR) & Automated Testing                     |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
1. Show the generated **After-Action Report** screen (`http://127.0.0.1:5000/reports/SCN-SSH-001`). Point out the Grade (S - Master Incident Commander), Timeliness SLA, and Chronological Audit Trail.
2. Switch to Terminal and run:
   ```bash
   python -m unittest discover tests -v
   ```

### What to say:
> "Upon completion, the simulator automatically compiles a comprehensive **After-Action Report (AAR)**, exportable to Markdown, JSON, and PDF. It records:
> - Overall triage score: 100/100, Grade S.
> - SLA compliance rate: completed in 45 simulated minutes against a 75-minute SLA.
> - 100% forensic integrity rate with 0 collateral disruption penalties.
> - A complete chronological decision audit trail and root-cause baseline findings.
>
> Finally, to prove software reliability, our automated test suite comprises 15 unit tests covering the asset manager, baseline auditor, simulation engine, playbooks, and report generator. As we run `python -m unittest discover tests -v`, all 15 tests pass in under 0.03 seconds."

```
+-----------------------------------------------------------------------------------------+
| [6:30 - 7:00] PART 6: Conclusion & Submission Wrap-Up                                   |
+-----------------------------------------------------------------------------------------+
```

### What to show on screen:
Show the GitHub repository page or project `README.md`.

### What to say:
> "To conclude: this project provides a complete, production-ready solution for RedKross Task 2:
> 1. Full source code, fixtures, and documentation are committed to GitHub.
> 2. The system can be executed interactively via the Web GUI or CLI.
> 3. Standard Incident Response Playbooks are documented and mapped to MITRE ATT&CK.
> 4. All instructions to reproduce are provided in the README.
>
> Thank you for your time, and I look forward to your evaluation!"

---

## Presentation Checklist Before Recording
- [ ] Run `python run_web.py` so the web interface is already accessible.
- [ ] Clean up terminal screen with `cls` (Windows).
- [ ] Test audio input levels.
- [ ] Upload video to YouTube (Unlisted), Google Drive (Anyone with link can view), or Loom.
- [ ] Paste repository URL and video URL into the Task 2 Submission Sheet.

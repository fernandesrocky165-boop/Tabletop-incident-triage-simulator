# SOC Incident Response Playbooks Guide

This guide documents the enterprise Incident Response Playbooks implemented within the Tabletop Triage Simulator. Each playbook is structured in compliance with **NIST SP 800-61 Rev. 2** (Computer Security Incident Handling Guide).

---

## Playbook Catalog

1. **IR-PB-001**: Linux Host Compromise & SSH Hardening Playbook
2. **IR-PB-002**: Web Application Breach & Reverse Shell Response Playbook
3. **IR-PB-003**: Data Exfiltration & Insider Threat Response Playbook

---

## 1. IR-PB-001: Linux Host Compromise & SSH Hardening

### 1.1 Scope & Threat Classification
- **Target Systems:** Linux platform hosts (`lab-linux-01` / `AST-001`), training infrastructure, bastion servers.
- **Threat Vector:** Distributed SSH password brute-forcing, credential stuffing, root password compromise, rogue mining processes (`/tmp/.x_miner`).
- **MITRE Tactics:** Initial Access, Credential Access, Execution, Persistence, Defense Evasion.

### 1.2 Severity Escalation Matrix
| Severity Tier | Trigger Conditions | SLA Window | Notification Channel | Designated Responders |
|---|---|---|---|---|
| **P1 - Critical** | Successful root login, active unauthorized shell, cryptominer execution | &le; 15 min | Secure Out-of-Band Bridge | SOC Lead, CISO, Platform Infrastructure Lead, Legal |
| **P2 - High** | Sustained credential brute-force (> 500 attempts/10m), unpatched vulnerable SSH config | &le; 30 min | Slack `#soc-incidents` | SOC Analyst Tier 2, Platform Admin |

### 1.3 Phase-by-Phase Operating Procedure

#### Phase 1: Detection & Triage
1. **SIEM Ingestion:** Monitor `auth.log` / `secure` for high failure counts from single or rotating IPs.
2. **Asset Correlation:** Search `asset_inventory.csv` for target host (`lab-linux-01`). Check if `ssh_admin_required = True` and note criticality (`High`).
3. **Priority Calculation:** Base severity (High) &times; Criticality (1.5x) = **P1 Critical**.

#### Phase 2: Investigation & Evidence Preservation
1. **Volatile Artifact Collection:**
   ```bash
   # Capture active connections and listening ports
   ss -tulpn > /var/log/forensics_sockets.txt
   # List active processes with full arguments
   ps auxf > /var/log/forensics_procs.txt
   # Check last logins and current pts sessions
   who -a; w; last -n 20
   ```
2. **Malware Attribution:**
   - Locate rogue binaries (e.g. `/tmp/.x_miner`).
   - Extract SHA-256 hash for Threat Intelligence lookup:
     ```bash
     sha256sum /tmp/.x_miner
     ```
3. **CRITICAL RULE:** Do NOT reboot or power cycle the machine before capturing memory and network state.

#### Phase 3: Containment
1. **Host-Level Firewall Quarantine:** Drop all attacker and non-SOC ingress/egress while maintaining administrative management:
   ```bash
   iptables -A INPUT -s 198.51.100.44 -j DROP
   iptables -A OUTPUT -d 203.0.113.88 -j DROP
   ```
2. **Session Severance:** Terminate adversary's active pseudoterminal:
   ```bash
   pkill -KILL -u root -t pts/2
   kill -9 14910 # Kill rogue child process
   ```

#### Phase 4: Forensic Baseline Audit (Read-Only)
Run the passive configuration checker to identify configuration defects that enabled the compromise:
```bash
python run_cli.py --audit --config fixtures/linux_fixtures/sshd_config_sample.txt
```
- **Definite Mismatch Identified:** `PermitRootLogin yes` (Line 3) - Allowed direct root interactive access.
- **Policy Mismatches Identified:**
  - `MaxAuthTries 12` (Line 8) - Permitted excessive password attempts per session.
  - `ClientAliveInterval 0` (Line 9) - Allowed orphaned sessions to remain alive forever.
  - `AllowUsers *` (Line 10) - Allowed any account to negotiate SSH.

#### Phase 5: Eradication & Remediation
1. Purge malware binaries and rogue cron jobs:
   ```bash
   rm -f /tmp/.x_miner
   crontab -r -u root
   ```
2. Deploy hardened SSH configuration based on `sshd_config_hardened_reference.txt`:
   ```text
   Port 22
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   PermitEmptyPasswords no
   X11Forwarding no
   MaxAuthTries 4
   ClientAliveInterval 300
   ClientAliveCountMax 2
   AllowUsers trainee-admin
   ```
3. Validate configuration syntax before restarting:
   ```bash
   sshd -t
   systemctl reload sshd
   ```
4. Rotate all administrative passwords and revoke authorized keys.

#### Phase 6: Recovery & Post-Incident Review
1. Confirm administrative SSH access using key-authenticated unprivileged user.
2. Verify platform team operational workloads.
3. Generate After-Action Report (AAR) using the Simulator engine.

---

## 2. IR-PB-002: Web Application Breach & Reverse Shell

- **Target System:** Web Application Server (`lab-web-01` / `AST-003`).
- **Threat Vector:** Unrestricted file upload leading to web shell execution (`/uploads/cache_sync.php`) and interactive reverse shell.
- **Key Containment:** Sever outbound C2 connection, isolate web tier from backend database networks, mount uploads with `noexec`.
- **Eradication:** Delete web shell, patch MIME/extension validation in application code, rotate database credentials.

---

## 3. IR-PB-003: Data Exfiltration & Insider Threat

- **Target System:** Records Archive Server (`lab-archive-01` / `AST-004`).
- **Threat Vector:** Abnormal off-hours SFTP transfer of encrypted archive datasets (45GB) to external VPS using compromised credentials.
- **Key Containment:** Immediate TCP socket termination, block destination IP at border firewall, lock compromised backup service account.
- **Eradication:** Revoke leaked private keys across all corporate systems, trace source workstation, package forensic logs for legal counsel.

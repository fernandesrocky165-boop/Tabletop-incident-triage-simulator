# GitHub Repository Setup & Upload Guide

This guide explains step-by-step how to publish this project to **your friend's GitHub account** so that:
1. All commit author credits display **your friend's name and email**.
2. The repository is public and accessible to the RedKross grading evaluators.
3. Both the GitHub repository URL and video link can be submitted to the Task 2 Submission Sheet.

---

## Method 1: Push from Terminal (Recommended & Cleanest)

### Step 1: Have Your Friend Create a New GitHub Repository
1. Log in to your friend's GitHub account at [https://github.com](https://github.com).
2. Click the **+** (plus icon) in the top right corner and select **New repository**.
3. Fill in:
   - **Repository name:** `SOC-Tabletop-Incident-Triage-Simulator` (or `RedKross-Task-2-SOC-Simulator`)
   - **Description:** `SOC Operations & Threat Detection - Tabletop Incident Triage Simulator & Hardening Auditor (RedKross Task 2)`
   - **Public / Private:** Select **Public** (Evaluators need public access to review code).
   - **Do NOT check** "Add a README file", ".gitignore", or "license" (we already have all of these ready in the workspace).
4. Click **Create repository**.
5. Copy the HTTPS repository URL, which looks like:
   `https://github.com/<friend-username>/SOC-Tabletop-Incident-Triage-Simulator.git`

---

### Step 2: Configure Local Git Author Identity (Your Friend's Name)
Run these commands in PowerShell inside the workspace directory (`C:\Users\vibhas pawar\OneDrive\Desktop\RedKross Task 2 Assignment Resources`):

```powershell
# Set local author name and email for this repository only (does not affect your global config)
git config user.name "Friend's Full Name"
git config user.email "friend_email@example.com"
```

Verify that local author is set to your friend:
```powershell
git config user.name
git config user.email
```

---

### Step 3: Initialize Git and Commit All Files
Run the following in PowerShell:

```powershell
# Initialize git repository
git init -b main

# Stage all files
git add .

# Create initial commit with friend as author
git commit -m "feat: complete SOC Operations Tabletop Incident Triage Simulator & Hardening Auditor (RedKross Task 2)"
```

---

### Step 4: Link Remote & Push to Friend's GitHub
Replace `<REPO_URL>` with your friend's repository URL:

```powershell
git remote add origin https://github.com/<friend-username>/SOC-Tabletop-Incident-Triage-Simulator.git
git branch -M main
git push -u origin main
```

#### Authentication Note:
When PowerShell prompts for credentials:
- **Username:** Your friend's GitHub username.
- **Password:** A **GitHub Personal Access Token (Classic)** with `repo` scope (GitHub no longer accepts raw account passwords for git push).

#### How your friend generates a Personal Access Token (PAT):
1. On GitHub, click top-right profile avatar &rarr; **Settings**.
2. Scroll to bottom of left sidebar &rarr; **Developer settings** &rarr; **Personal access tokens** &rarr; **Tokens (classic)**.
3. Click **Generate new token (classic)**.
4. Note: `RedKross Submission`.
5. Expiration: 30 days.
6. Select scopes: Check **`repo`** (Full control of private and public repositories).
7. Click **Generate token**.
8. Copy the token (starts with `ghp_...`) and paste it as the password when prompted in the terminal.

---

## Method 2: Push Using Personal Access Token Directly in URL
If you want to push without interactive authentication prompts:

```powershell
git push https://<TOKEN>@github.com/<friend-username>/SOC-Tabletop-Incident-Triage-Simulator.git main
```
*(Replace `<TOKEN>` with your friend's GitHub token and `<friend-username>` with their GitHub username).*

---

## Method 3: Uploading via GitHub Web Interface (Alternative)
If terminal authentication is restricted:
1. Open the created repository on your friend's GitHub.
2. Click **Add file** &rarr; **Upload files**.
3. Drag and drop all project folders (`src/`, `web/`, `fixtures/`, `tests/`, `docs/`, `run_cli.py`, `run_web.py`, `requirements.txt`, `README.md`).
4. Enter commit message: `feat: initial release of SOC tabletop triage simulator`.
5. Click **Commit changes**.

---

## Final Verification Checklist Before Submission
- [ ] Visit `https://github.com/<friend-username>/SOC-Tabletop-Incident-Triage-Simulator` in an Incognito window to confirm it is **Publicly accessible**.
- [ ] Check that `fixtures/linux_fixtures/` contains the 5 original fixtures.
- [ ] Check that `README.md` renders cleanly on the repository homepage.
- [ ] Verify that commit history displays your friend's name and GitHub profile.
- [ ] Paste the GitHub repository URL into the **Task 2 Submission Sheet**.
- [ ] Record the 5–8 minute video following `docs/VIDEO_PRESENTATION_SCRIPT.md` and paste the video URL into the submission sheet.

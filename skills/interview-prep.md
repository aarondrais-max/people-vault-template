---
name: interview-prep
description: Pre-screen prep for a named candidate + req. Reads candidate page, req page, source files. Outputs structured prep notes with fit flags and suggested questions.
user_invocable: true
trigger: "interview-prep, prep for screen, prep for interview, interview questions for, how should we interview, scorecard for"
---

You are the interview prep skill for the People Team Knowledge Vault.
Given a candidate name and req ID (or inferred from today's calendar), produce structured prep notes.

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md`.

## Step 0: Identify Target

If invoked with explicit candidate + req: use those.
If invoked without arguments: check today's calendar (if Calendar MCP is available) for recruiter screens. For each screen found, run prep.

## Step 1: Read Vault Context

For each candidate + req pair:

### 1a. Req page
Read `[VAULT_PATH]/wiki/reqs/[req-id].md`. Extract:
- Role requirements and must-haves
- HM Preferences (must-haves, anti-patterns)
- Referral Bullets (proxy for ideal profile)
- Active pipeline state

### 1b. Candidate page (Tier 1 only)
Read `[VAULT_PATH]/wiki/candidates/[name].md` if it exists. Extract:
- Background summary
- Any existing screen notes
- Flags (competing offers, comp expectations, constraints)
- Timeline

If no candidate page exists yet: proceed with ATS data only (Step 2).

### 1c. Source files (optional but high value)
If candidate page lists source files (meeting notes, email threads), read the most recent one.

## Step 2: Gather ATS Data (optional)

If Greenhouse MCP is available:
- Search for the candidate by name + req ID
- Pull resume text and application details
- Pull any existing scorecard submissions

If Greenhouse is not available: proceed with vault data only and note the gap.

## Step 3: Analyze Fit

Compare candidate profile against req requirements:

**Strengths (where candidate clearly meets bar):**
- [bullet]

**Gaps / risks (where bar is uncertain or unmet):**
- [bullet]

**Flags (things to probe specifically):**
- [bullet — be specific, e.g., "No enterprise deal closing mentioned — ask for specific size/complexity"]

**Competing process risk:**
- [If flags section mentions other active processes, note timeline implication]

## Step 4: Write Prep Notes

```markdown
---
title: Interview Prep — [Candidate Name] / [R-XXXXX]
type: query
created: YYYY-MM-DD
req: R-XXXXX
candidate: [Full Name]
stage: [rps / hm / final / offer]
---

# Interview Prep: [Candidate Name]
**Role:** [R-XXXXX] — [Role Title]
**Screen time:** [time if known from calendar]
**Prepared:** [YYYY-MM-DD HH:MM]

## Profile Snapshot
[3–4 sentences: who they are, current role, most relevant experience, why they applied or were sourced]

## Fit Assessment
**Strong signals:**
- [bullet]

**Gaps to probe:**
- [bullet]

**Flags:**
- [bullet]

## Suggested Questions

1. **[Question topic]** — [The question]
   *What to listen for:* [what a good vs weak answer sounds like]

2. **[Question topic]** — [The question]
   *What to listen for:* [what a good vs weak answer sounds like]

3. **[Question topic]** — [The question]
   *What to listen for:* [what a good vs weak answer sounds like]

4. **[Question topic]** — [The question]
   *What to listen for:* [what a good vs weak answer sounds like]

5. **Comp alignment check** — "What does your current total comp look like, and what are you targeting in your next role?"
   *What to listen for:* Alignment to our range ([range from req page if available]); any hard minimums; equity expectations.

## Must-Confirm Items
- [ ] [Item from HM Preferences that must be verified — e.g., "Confirm enterprise deal sizes — HM requires 6-figure closes"]
- [ ] [Item — e.g., "Right-to-work / visa status if applicable"]
- [ ] [Item — e.g., "Start date availability if this one moves fast"]

## Quick Reference — HM Must-Haves
[Copy the must-haves from the req page — quick reference during the call]

## Sources Used
- [List of files read]
```

## Step 5: Save Output

Save to `[VAULT_PATH]/queries/interview-prep-YYYY-MM-DD.md`.

If multiple candidates today, save all prep in one file with separate sections.

## Step 6: Log

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD] interview-prep | Screen prep
- Candidates prepped: [count]
- Reqs covered: [list]
- ATS data available: yes / no
- Output: queries/interview-prep-YYYY-MM-DD.md
```

## Rules
- Pull from ATS only if MCP is available — never fabricate candidate data
- Gaps and flags should be specific, not generic ("Ask about enterprise experience" is bad; "Candidate lists SMB SaaS deals only — ask for deal size and complexity of largest 3 closes" is good)
- Keep the full prep file under 80 lines per candidate
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
